"""Scalar cancellation, dirty scratch, and rational private-path rank checks."""
from fractions import Fraction as Q
from pathlib import Path
import itertools
import random
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_cancellation import (PointCancellation,candidate_counts,line_projection,
    private_path_bound,local_exclusion_identity,eulerian_pairs,leave_one_out_control,certificate)
from audit_fused_block import rational_rank,matrix_product
from dag_network import exact_invocation,shared_scalar_model


def subtract(a,b):return [[x-y for x,y in zip(row,col)] for row,col in zip(a,b)]
def identity(n):return [[Q(i==j) for j in range(n)] for i in range(n)]


class CancellationAudit(unittest.TestCase):
    def test_all_intersection_sizes_and_binary_scalar_domain(self):
        for h in (6,7,8,10):
            c=PointCancellation(h)
            row=c.verify()
            self.assertEqual(row['additions'],6*len(c.triples)-h)
            for t,T in enumerate(c.triples):
                for s,S in enumerate(c.triples):
                    j=len(set(S)&set(T))
                    self.assertEqual((j+int(s==t))%2,int(j==1))
                    # The coefficient cancels, but the physical diagonal
                    # path is still present and cannot be erased by a frame
                    # checker that sees only final GF(2) coefficients.
                self.assertEqual((c.coefficients[c.outputs[t]]>>t)&1,0)
                self.assertEqual((c.reachable[c.outputs[t]]>>t)&1,1)

    def test_private_paths_have_distinct_physical_edges(self):
        c=PointCancellation(8);code=c.compile()
        triples=code['triples'];paths=code['private_diagonal_edges']
        self.assertEqual(len(paths),len(triples))
        self.assertEqual(len({slot for _,_,slot in paths}),len(triples))
        self.assertEqual(len({node for _,node,_ in paths}),len(triples))
        for source,target,_ in paths:
            self.assertEqual(c.args[target][1],source)
            self.assertEqual(target,c.outputs[source])
        self.assertEqual(code['roles'],7*len(triples)-8)

    def test_complete_dirty_input_basis_forward_and_reverse(self):
        code=PointCancellation(6).compile()
        for inverse in (False,True):
            row=exact_invocation(6,inverse,code)
            self.assertTrue(row['exact_linear_map'])

    def test_three_stage_scalar_network_with_shared_dirty_auxiliary_banks(self):
        row=shared_scalar_model(6,seed=109,code=PointCancellation(6).compile())
        self.assertTrue(row['bank_exchange'])
        self.assertTrue(row['all_scratch_restored'])

    def test_line_complement_distance_exceeds_signed_rank_change(self):
        for h in (6,7,8,10):
            for T in list(itertools.combinations(range(h),3))[:4]:
                P=line_projection(h,T);C=subtract(identity(h),P)
                self.assertEqual(matrix_product(P,P),P)
                self.assertEqual(rational_rank(P),1)
                self.assertEqual(rational_rank(C),h-1)
                self.assertEqual(rational_rank(subtract(C,P)),h)
                self.assertEqual(rational_rank(subtract(C,P))-(h-2),2)
                self.assertEqual(private_path_bound(h)['endpoint_difference_rank'],h)

    def test_arbitrary_internal_matrices_cannot_erase_private_path_excess(self):
        rng=random.Random(10959)
        h=4;P=line_projection(h,(0,1,2));C=subtract(identity(h),P)
        for _ in range(24):
            # Internal labels need not be projections, symmetric, nested,
            # or full rank; the proof uses rank subadditivity only.
            interior=[[[Q(rng.randrange(-2,3),rng.randrange(1,4)) for _ in range(h)]
                       for _ in range(h)] for _ in range(2)]
            chain=[P]+interior+[C]
            charge=sum(rational_rank(subtract(b,a)) for a,b in zip(chain,chain[1:]))
            self.assertGreaterEqual(charge,h)
            self.assertGreaterEqual(charge-(rational_rank(C)-rational_rank(P)),2)

    def test_local_total_star_formula_has_the_same_private_diagonal(self):
        for n in (4,5,7,9):
            row=local_exclusion_identity(n)
            self.assertTrue(row['exact'])
            self.assertEqual(row['outputs'],row['private_diagonal_terms'])

    def test_large_counts_and_scoped_rejection(self):
        row=candidate_counts(50)
        self.assertEqual(row['side_roles'],137150)
        self.assertEqual(row['additions'],117550)
        self.assertEqual(row['rank_sum_lower_bound_without_negative_source_charge'],
                         row['optimistic_shared_W']*row['m'])
        self.assertEqual(row['deficit_upper_bound'],0)
        result=certificate()
        self.assertEqual(result['partial_replacement']['maximum_integer_targets'],1149)
        self.assertIn('NO NEW KAPPA',result['status'])
        self.assertIn('Not a lower bound on all cancellation circuits',result['scope'])

    def test_leave_one_out_removes_self_terms_but_has_disjoint_bad_paths(self):
        for n in (5,7,9):
            order=eulerian_pairs(n)
            self.assertEqual(set(order),set(itertools.combinations(range(n),2)))
        for h in (6,8,10):
            row=leave_one_out_control(h)
            self.assertTrue(row['edge_disjoint'])
            self.assertTrue(row['no_explicit_self_term'])
            self.assertEqual(row['matched_nonorthogonal_paths'],row['inputs'])
            self.assertEqual(row['side_roles'],12*row['inputs']-6*h)

    def test_distinct_nonorthogonal_lines_have_the_same_excess(self):
        h=6;P=line_projection(h,(0,1,2))
        for T in ((0,1,3),(3,4,5)):
            C=subtract(identity(h),line_projection(h,T))
            self.assertEqual(rational_rank(subtract(C,P)),h)
        # Intersection one gives orthogonality and zero excess, which is
        # exactly why the published cancellation-free paths remain valid.
        C=subtract(identity(h),line_projection(h,(0,3,4)))
        self.assertEqual(rational_rank(subtract(C,P)),h-2)


if __name__=='__main__':unittest.main()
