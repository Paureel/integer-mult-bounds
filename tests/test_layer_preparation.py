"""Independent recurrence unrolling and boundaries for preparation estimates."""
from dataclasses import replace
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from certify import Parameters, network
from prepare_layers import (guard, packed_exponents, check_parameters,
                            complex_search, scenarios, BIT_SAVING)


class LayerPreparation(unittest.TestCase):
    def test_guard_against_actual_stopping_and_piece_count(self):
        for h in (25,50):
            for beta in (Q(1,100),Q(1,5),Q(1,2),Q(9,10),Q(999,1000)):
                g = guard(beta,h=h)
                m,s,E,C0 = (g[k] for k in ('m','s','E','C0'))
                for power in (1,3,8):
                    d = m**power
                    size = d
                    levels = 0
                    while size**beta.denominator >= d**beta.numerator:
                        size //= m
                        levels += 1
                    depth = 8*size
                    for _ in range(levels):
                        depth = s*depth+E
                    layer = (m-1)*(1+power)*depth+18*d
                    exponent = g['C1']
                    self.assertLess(layer**exponent.denominator,
                                    C0**exponent.denominator*d**exponent.numerator)

    def test_guard_rejects_missing_hypotheses(self):
        for beta in (Q(0),Q(1),Q(-1,2)):
            with self.assertRaises(ValueError):guard(beta)
        for zeta in (Q(0),Q(-1)):
            with self.assertRaises(ValueError):guard(Q(1,2),zeta)

    def test_recurrence_below_equal_and_above_tau(self):
        # m=16, tau=1/2, B=2,4,8: sigma=1/4,1/2,3/4 exactly.
        # Use d=m^16 so every exponent comparison has integral powers.
        m,tau,power = 16,Q(1,2),16
        d,K = m**power,m**(power//4)
        for branch,sigma in ((Q(1,2),Q(0)),(1,Q(0)),(2,Q(1,4)),
                             (4,Q(1,2)),(8,Q(3,4))):
            for beta in (Q(1,4),Q(1,2),Q(3,4)):
                exp = packed_exponents(tau,sigma,beta,Q(1,4))
                stop = m**int(power*beta)
                for root_power in (0,3,8,16):
                    size=m**root_power
                    nodes=[]
                    while size>=stop:
                        nodes.append(size)
                        size//=m
                    total=Q(size)
                    for node in reversed(nodes):
                        work=isqrt(node*K)
                        self.assertEqual(work*work,node*K)
                        total=branch*total+work+1
                    leaf=branch**len(nodes)*size
                    internal=total-leaf
                    e=power*exp['internal']
                    f=power*exp['leaf']
                    self.assertEqual(e.denominator,1)
                    self.assertEqual(f.denominator,1)
                    constant=2*(power+1)*max(Q(1),Q(branch,4))
                    self.assertLessEqual(internal,constant*m**int(e))
                    self.assertLessEqual(leaf,m**int(f))

    def test_old_conditions_imply_new_internal_condition(self):
        for tau in (Q(1,4),Q(1,2),Q(3,4)):
            for sigma in (Q(0),Q(1,4),Q(1,2),Q(3,4)):
                for beta in (Q(1,10),Q(1,2),Q(9,10)):
                    for c in (Q(1,100),Q(1,10)):
                        old=max(sigma,tau*(1+c/beta))
                        new=packed_exponents(tau,sigma,beta,c)['internal']
                        self.assertLessEqual(new,old)

    def test_complex_only_positivity_and_unique_optimum(self):
        c=complex_search()
        self.assertEqual(c['winner_h'],25)
        self.assertEqual(c['certified_saving'],Q(418,10**12))
        self.assertGreater(c['saving_lower'],c['tail_upper'])
        n=network(25)
        self.assertLess(n['Lc'],n['N'])
        self.assertGreater(2*n['Lc'],n['N'])
        self.assertEqual(n['Wc']*n['m']-n['sc'],2*(n['N']-n['Lc']))
        self.assertEqual(n['eta_c'],Q(14,3464399375))
        for h in range(7,30):
            if h==9:continue
            self.assertEqual(network(h)['eta_c']>0,h>=22)

    def test_complex_scalar_coefficients_and_binary_complements(self):
        # Intersection orbits cover every source/target pair. No matching or
        # parity assumption on h is involved in this original complex motif.
        h=25
        left=set(range(3))
        for intersection in range(4):
            right=set(range(intersection))|set(range(3,6-intersection))
            central=Q(intersection-1,2)
            side=-central if intersection in (0,2) else 0
            self.assertEqual(central+side,int(intersection==3))
            if intersection in (0,2):
                self.assertEqual(len(left&right)%2,0)
                self.assertTrue(set(range(h))-(left|right))
            self.assertEqual(len(right)%2,1)

    def test_hypothetical_targets_cannot_pass_existing_primitive(self):
        rows=scenarios()
        self.assertFalse(rows['existing_59_control']['recurrence']['hypothetical'])
        for key in ('hypothetical_39','hypothetical_34'):
            row=rows[key]
            self.assertIn('NOT A MULTIPLICATION RESULT',row['status'])
            self.assertGreater(row['existing_primitive_internal_exponent'],1)
            p=Parameters(**row['parameters'])
            with self.assertRaises(ValueError):check_parameters(p,row['guard'])
            with self.assertRaises(ValueError):
                check_parameters(replace(p,C1=Q(1)),row['guard'],
                                 hypothetical_theta=BIT_SAVING)
            with self.assertRaises(ValueError):
                check_parameters(replace(p,sigma=Q(1,2)),row['guard'],
                                 hypothetical_theta=BIT_SAVING)
            altered=dict(row['guard'],C0=1)
            with self.assertRaises(ValueError):
                check_parameters(p,altered,hypothetical_theta=BIT_SAVING)


if __name__=='__main__':unittest.main()
