"""Exact address controls for the short-guard reduction, not a fast gatherer."""
from fractions import Fraction as Q
from pathlib import Path
import itertools
import random
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_short_guards import (guard_width,gather_order,gather,ungather,
    active_mask,rotate_gadget,exceptional,compact_add,gathered_add,repair_budget,
    reduction_exponents,monotone_lengths,monotone_stream_obstruction,certificate)


class ShortGuards(unittest.TestCase):
    def test_gather_is_exact_bit_permutation_including_boundary_offsets(self):
        for f,K in ((1,3),(2,3),(3,3),(4,2)):
            for rho in range(K):
                for g in range(1,K+1):
                    order=gather_order(f,K,rho,g)
                    self.assertEqual(sorted(order),list(range(f*K)))
                    width=f*K-(f-1)*g
                    for j in range(f-1):
                        for t in range(g):
                            self.assertEqual(gather(1<<(rho+j*K+t),order),
                                             1<<(width+j*g+t))
                    for value in range(1<<(f*K)):
                        self.assertEqual(ungather(gather(value,order),order),value)
                    # Even when rho=K-1, the omitted highest selected bit
                    # belongs to the spectator field and is never a guard.
                    self.assertLess(order.index(rho+(f-1)*K),width)

    def test_exhaustive_small_modular_rotations_and_exceptional_repair(self):
        for n,g in ((1,3),(2,2),(3,1)):
            size=1<<(n*g)
            for x,y,z in itertools.product(range(size),repeat=3):
                out=rotate_gadget(x,y,z,n,g)
                self.assertEqual(rotate_gadget(*out,n,g,inverse=True),(x,y,z))
                self.assertEqual(exceptional(y,z,n,g),exceptional(out[1],out[2],n,g))
                self.assertEqual(compact_add(x,y,z,n,g),
                                 (x,y^active_mask(x,n,g),z))

    def test_real_guard_boundaries_and_dirty_auxiliary_values(self):
        # One used six-bit segment, arbitrary top segment. Exercise every
        # low guard, including both ends of the good interval and wraparound.
        rng=random.Random(109)
        good=bad=0
        n,g=2,6
        for control,y0,z0 in itertools.product(range(2),range(64),range(64)):
            x=control|(rng.randrange(64)<<6)
            y=y0|(rng.randrange(64)<<6)
            z=z0|(rng.randrange(64)<<6)
            out=rotate_gadget(x,y,z,n,g)
            is_bad=exceptional(y,z,n,g)
            self.assertEqual(is_bad,exceptional(out[1],out[2],n,g))
            if is_bad:bad+=1
            else:
                good+=1
                self.assertEqual(out,(x,y^control,z))
            self.assertEqual(compact_add(x,y,z,n,g),(x,y^active_mask(x,n,g),z))
        self.assertGreater(good,0)
        self.assertGreater(bad,0)

    def test_whole_reduction_preserves_spectators_and_restores_dirty_scratch(self):
        rng=random.Random(10959)
        shapes=[(f,K,rho,g) for f,K in ((1,3),(2,3),(3,3),(4,7),(6,9))
                for rho in (0,K-1) for g in (1,K)]
        shapes.extend(((4,9,8,6),(5,12,7,8)))
        for f,K,rho,g in shapes:
            for _ in range(100):
                x,y,z=(rng.getrandbits(f*K) for _ in range(3))
                mask=sum(((x>>(rho+j*K))&1)<<(rho+j*K) for j in range(f))
                self.assertEqual(gathered_add(x,y,z,f,K,rho,g),(x,y^mask,z))

    def test_logarithmic_guards_make_repair_negligible(self):
        for p in (2,3,7,16,17,100,1024,10**6,2**100+1):
            row=repair_budget(p,p)
            self.assertGreaterEqual(1<<guard_width(p),64*p**4)
            self.assertLessEqual(row['bad_fraction_upper'],Q(5,4*p**3))
            self.assertLessEqual(row['normalized_repair_at_A_equal_p_R_at_least_p'],
                                 Q(5,2*p**2))
        for p in (0,1,2.5):
            with self.assertRaises(ValueError):guard_width(p)
        for shape in ((0,2,0,1),(2,2,2,1),(2,2,0,3)):
            with self.assertRaises(ValueError):gather_order(*shape)

    def test_conditional_targets_do_not_certify_the_missing_gatherer(self):
        result=certificate()
        self.assertIn('NO NEW KAPPA',result['status'])
        targets=result['conditional_targets']
        self.assertEqual({x['target'] for x in targets.values()},{Q(1,2**39),Q(1,2**34)})
        for row in targets.values():
            self.assertIn('UNPROVED',row['exponents']['status'])
            self.assertLess(row['exponents']['layer'],1)
        # A faster active exponent for gathering does not automatically
        # speed up the compact butterfly used by the reduction.
        ex=reduction_exponents(Q(9,10),Q(4,5),Q(1,2),Q(1,10),Q(3,4),Q(0))
        self.assertEqual(ex['gathering'],Q(31,40))
        self.assertEqual(ex['compact_gadget'],Q(9,10))
        self.assertEqual(ex['layer'],Q(9,10))
        with self.assertRaises(ValueError):
            reduction_exponents(Q(9,10),Q(4,5),Q(1,2),Q(1,10),Q(1),Q(0))

    def test_restricted_transpose_stream_bound_and_its_scope(self):
        for a,b in ((1,1),(1,3),(2,2),(3,2)):
            A,B=1<<a,1<<b
            transpose=[v*A+u for u in range(A) for v in range(B)]
            inc,dec=monotone_lengths(transpose)
            self.assertEqual((inc,dec),(A+B-1,min(A,B)))
            bound=monotone_stream_obstruction(a,b)
            self.assertGreaterEqual(bound['required_global_monotone_streams_at_least']
                                    *(A+B-1),A*B)
            self.assertIn('not all linear-time',bound['scope'])
        # Internal row/column permutations need not preserve the exact LIS,
        # but the coarse bound works for both stream directions.
        for rows in itertools.permutations(range(4)):
            for cols in itertools.permutations(range(4)):
                permutation=[cols[v]*4+rows[u] for u in range(4) for v in range(4)]
                self.assertLessEqual(max(monotone_lengths(permutation)),7)


if __name__=='__main__':unittest.main()
