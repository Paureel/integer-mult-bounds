"""Parity-butterfly operator checks and the coordinate cut-rank boundary."""
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_fused_block import (layout,fused_numerator,directional_numerator,
    sandwich_numerator,finite_identity_checks,cut_controls,cut_rank,
    walsh_matrix,pointwise_matrix,matrix_product,rational_rank)


class FusedBlock(unittest.TestCase):
    def test_all_small_basis_inputs(self):
        result=finite_identity_checks()
        self.assertEqual(result['exhaustive_basis_inputs'],168)
        self.assertEqual(result['coordinate_layer_calls'],3)
        self.assertEqual(result['minimum_coordinate_calls_from_cut_budget'],2)

    def test_nonzero_payloads_and_wide_spectators(self):
        rng=random.Random(109)
        for f,K,rho,extra in ((2,2,1,2),(3,2,0,1)):
            x,y,bits=layout(f,K,rho,extra)
            state=[(rng.randrange(-16,17),rng.randrange(-16,17)) for _ in range(1<<bits)]
            fused,fd=fused_numerator(state,x,y)
            direct,dd=directional_numerator(state,[(1<<a)|(1<<b) for a,b in zip(x,y)])
            self.assertEqual([(z[0]*dd,z[1]*dd) for z in fused],
                             [(z[0]*fd,z[1]*fd) for z in direct])

    def test_spectator_fibers_are_preserved(self):
        f,K,rho,extra=2,2,1,1
        x,y,bits=layout(f,K,rho,extra)
        active=sum(1<<i for i in x+y)
        source=0b101010101
        state=[(int(i==source),0) for i in range(1<<bits)]
        fused,_=fused_numerator(state,x,y)
        self.assertTrue(all(not any(z) or (i&~active)==(source&~active)
                            for i,z in enumerate(fused)))

    def test_invalid_overlapping_or_missing_axes(self):
        state=[(0,0)]*4
        for x,y in (([0],[0]),([] ,[]),([0],[2]),([0,1],[1])):
            with self.assertRaises(ValueError):fused_numerator(state,x,y)
        with self.assertRaises(ValueError):sandwich_numerator(state,[0],[1],3)

    def test_cut_controls_and_arbitrary_child_axis_sets(self):
        self.assertEqual(len(cut_controls()),6)
        e,roles=3,2
        for active in range(1,8):
            child=walsh_matrix(e,roles,active,role=1)
            budget=0
            for bit in range(e):
                value=cut_rank(child,e,bit)
                self.assertEqual(value,(1<<e-1) if active>>bit&1 else 0)
                budget+=value
            self.assertEqual(budget,(1<<e-1)*active.bit_count())

    def test_pointwise_mixing_and_cancellation_do_not_break_bound(self):
        e=2
        child=walsh_matrix(e,2,1,role=0)
        free=pointwise_matrix(e,((1,1),(0,1)))
        for bit in range(e):
            self.assertEqual(cut_rank(free,e,bit),0)
            self.assertLessEqual(cut_rank(matrix_product(child,free),e,bit),
                                 cut_rank(child,e,bit))
        # Squaring a coordinate Walsh operator is scalar identity on that
        # role; the cut rank decreases. The proof uses <=, not additivity.
        self.assertEqual(cut_rank(matrix_product(child,child),e,0),0)

    def test_noncoordinate_movement_is_outside_free_class(self):
        # Address XOR x <- x XOR y is a permutation, but not pointwise. It
        # has nonzero cut rank, precisely the resource the obstruction omits.
        permutation=[[0]*4 for _ in range(4)]
        for source in range(4):
            target=source^((source>>1)&1)
            permutation[target][source]=1
        self.assertEqual(cut_rank(permutation,2,0),1)
        self.assertEqual(cut_rank(permutation,2,1),0)
        self.assertEqual(rational_rank(permutation),4)


if __name__=='__main__':unittest.main()
