"""Exact small operators and scoped rank obstructions for fusion searches."""
from fractions import Fraction as Q
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_sparse_fusion import (signature,phase_value,minimum_words,
    polar_columns,binary_rank,mixes_commute,finite_audit,central_gate_screen,
    candidate_budgets)


def direction_numerator(state,v,sign=1):
    # Exact Gaussian integer arithmetic here: all values stay below 2^53.
    return [(1+sign*1j)*z+(1-sign*1j)*state[x^v]
            for x,z in enumerate(state)]


def product_numerator(state,directions):
    for v,sign in directions:
        state=direction_numerator(state,v,sign)
    return state


class SparseFusion(unittest.TestCase):
    def test_every_phase_signature_and_rank_lower_bound(self):
        words=minimum_words(3)
        values=set()
        for phase,word in words.items():
            function=tuple(sum(sign*((v&x).bit_count()%2) for v,sign in word)%4
                           for x in range(8))
            self.assertEqual(function,tuple(phase_value(3,phase,x) for x in range(8)))
            values.add(function)
            self.assertGreaterEqual(len(word),binary_rank(polar_columns(3,phase)))
        self.assertEqual(len(values),512)

    def test_six_to_one_as_full_operators(self):
        seven=[(v,1) for v in range(1,8)]
        six=[(v,1) for v in range(2,8)]
        for i in range(8):
            state=[int(i==j) for j in range(8)]
            self.assertEqual(product_numerator(state,seven),[128*z for z in state])
            inverse=direction_numerator(state,1,-1)
            self.assertEqual(product_numerator(state,six),[32*z for z in inverse])

    def test_collective_symmetry_as_full_operators(self):
        columns=[63^(1<<i) for i in range(6)]
        for initial in (0,1,17,63):
            state=[int(i==initial) for i in range(64)]
            self.assertEqual(product_numerator(state,[(v,1) for v in columns]),
                             product_numerator(state,[(1<<i,1) for i in range(6)]))
        for active in range(1,64):
            selected=[v for i,v in enumerate(columns) if active>>i&1]
            phase=signature(6,[(v,1) for v in selected])
            self.assertEqual(binary_rank(polar_columns(6,phase)),len(selected))

    def test_mixing_criterion_against_fourier_blocks(self):
        phases=[signature(3,[(1,1)]),signature(3)]
        gates=(((1,0),(1,1)),((1,0),(0,-1)),((1,1),(0,1)))
        for G in gates:
            actual=True
            for x in range(8):
                diagonal=[1j**phase_value(3,p,x) for p in phases]
                for i in range(2):
                    for j in range(2):
                        if G[i][j]*diagonal[j]!=diagonal[i]*G[i][j]:actual=False
            self.assertEqual(mixes_commute(G,phases),actual)
        self.assertTrue(mixes_commute(gates[0],[phases[0],phases[0]]))

    def test_bounded_controls_and_central_frame_obstruction(self):
        finite=finite_audit()
        self.assertEqual(finite['gl3_invertible_matrices'],168)
        self.assertEqual(finite['gl3_phase_preserving_pairs'],102)
        central=central_gate_screen()
        self.assertEqual(central['baseline_incident_rank'],56500)
        self.assertEqual(central['minimum_sampled_changed_rank'],57000)
        self.assertEqual(central['density_minus_center_count'],66)
        self.assertEqual(central['joint_frame_pairs'],4096)
        self.assertEqual(central['joint_baseline'],112350)
        self.assertEqual(central['joint_minimum_changed_rank'],112850)

    def test_targets_require_a_substantial_new_primitive(self):
        for row in candidate_budgets().values():
            theta=row['maximum_spacing_exponent_at_current_active_saving']
            self.assertGreater(theta,0)
            self.assertLess(theta,Q(1,10**8))
            b=row['necessary_active_saving_for_alternative']
            self.assertGreater(b,Q(49,100000))
            self.assertLess(b,Q(51,100000))


if __name__=='__main__':unittest.main()
