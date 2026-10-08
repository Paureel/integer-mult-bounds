"""Rational rank density, full edge accounting, and scoped local optimality."""
from fractions import Fraction as Q
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_joint_frames import (matrix,eye,zero,sub,scale,product,rank,
    span_projection,paired_invocation,score_graph,invocation_counts,
    central_score,central_lower_bound,rational_controls,certificate)
from audit_cancellation import line_projection
from dag_network import exact_invocation
from paired_network import circuit


class JointFrames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.graph=paired_invocation(6)

    def test_exact_paired_scalar_map_with_arbitrary_scratch(self):
        code=circuit(6).program()
        for inverse in (False,True):
            self.assertTrue(exact_invocation(6,inverse,code)['exact_linear_map'])

    def test_full_physical_edge_accounting(self):
        g=self.graph;n=invocation_counts(6,g['R']);scores=score_graph(g)
        self.assertEqual(g['R'],164)
        self.assertEqual(scores,dict(X=100,Y=100,side=984,center=108))
        self.assertEqual(sum(scores.values()),n['total_rank'])
        self.assertEqual(n['total_rank'],1292)

    def test_general_projection_construction_agrees_with_triple_formula(self):
        for h in (6,10):
            for T in ((0,1,2),(1,3,4)):
                t=tuple(int(i in T) for i in range(h))
                P=span_projection([t],h)
                self.assertEqual(P,matrix(line_projection(h,T)))
                self.assertEqual(product(P,P),P)
        rows=[(1,1,1,0,0,0),(1,1,0,1,0,0),(1,0,1,0,1,0)]
        P=span_projection(rows,6)
        self.assertEqual(rank(P),3)
        self.assertEqual(product(P,P),P)

    def test_rank_update_column_and_row_defects_are_both_needed(self):
        A=matrix(((1,0),(0,0)))
        for u in ((1,0),(0,1),(1,1)):
            for v in ((1,0),(0,1),(1,1)):
                uv=matrix([[x*y for y in v] for x in u])
                col_out=int(u[1]!=0);row_out=int(v[1]!=0)
                self.assertGreaterEqual(rank(sub(A,uv)),col_out+row_out)
        # One-sided escape need not raise rank by one. A symmetric-only
        # update argument would be incorrect for general rational frames.
        self.assertEqual(rank(sub(A,matrix(((0,0),(1,0))))),1)

    def test_joint_internal_changes_pay_all_incident_edges(self):
        g=self.graph;h=g['h'];I=eye(h);Z=zero(h)
        P=matrix(line_projection(h,(0,1,2)))
        E=matrix([[int(i==0 and j==1) for j in range(h)] for i in range(h)])
        D,A,C,B=P,sub(I,E),scale(P,Q(2,3)),I
        changes=dict(zip(g['central'],(D,A,C,B)))
        # Change copy and injection frames too, not just four central gates.
        changes.update({(4,0):E,(8,0):sub(I,P),(11,0):Z})
        score=score_graph(g,changes)
        self.assertGreaterEqual(score['side'],g['R']*h)
        self.assertGreaterEqual(score['X']+score['Y']+score['center'],
                                central_score(h,D,A,C,B))
        self.assertGreaterEqual(sum(score.values()),
                                g['R']*h+central_score(h,D,A,C,B))

    def test_general_rational_density_and_central_controls(self):
        controls=rational_controls(10)
        self.assertEqual(controls['matrix_controls'],12)
        self.assertEqual(controls['baseline_central_score'],2460)
        for row in controls['central_controls']:
            self.assertGreaterEqual(row['score']-2460,row['lower_excess'])
            self.assertGreaterEqual(row['lower_excess'],0)
        I=eye(10);Z=zero(10)
        self.assertEqual(central_lower_bound(10,I,Z),0)
        self.assertGreater(central_lower_bound(10,Z,I),0)

    def test_published_loss_and_scope(self):
        c=certificate();n=c['published_invocation']
        self.assertEqual(n['total_rank'],27388000)
        self.assertEqual(n['center_return_loss'],2500)
        self.assertEqual(n['density_minus_center_roles'],342)
        self.assertIn('NO NEW KAPPA',c['status'])
        self.assertIn('Retains active-factor embedding',c['scope'])
        self.assertIn('cross-invocation',c['scope'])

    def test_boundary_mutations_are_rejected_by_local_scorer(self):
        with self.assertRaises(ValueError):
            score_graph(self.graph,{('in',0):zero(6)})


if __name__=='__main__':unittest.main()
