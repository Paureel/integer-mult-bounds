"""Reservation invariants, full recurrence controls and exact witness checks."""
from dataclasses import replace
from fractions import Fraction as Q
from itertools import product
from math import isqrt
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from compact_control_layer import (allocation,ceil_log,repair_bound,
    layer_exponents,parameters,check,certificate)
from certify import network
from prepare_layers import guard
from search_network import log_integer_bounds


class CompactControlLayer(unittest.TestCase):
    def test_reserved_bits_are_existing_disjoint_chunks(self):
        for d in (1,8,64,1000):
            for D in (1,d//2 or 1,d):
                for K in (1,8,128):
                    plan=allocation(d,D,K,6,4,8)
                    self.assertLessEqual(plan['preprocessed_chunks'],D)
                    self.assertEqual(plan['preprocessed_chunks']+plan['active_chunks'],D)
                    if plan['mode']=='recursive':
                        self.assertEqual(plan['reserved_chunks']+plan['active_chunks'],D)
                        self.assertGreaterEqual(plan['front_chunks']*K,2*d*6)
                        self.assertGreaterEqual(plan['back_chunks']*K,d*6)
                    self.assertLess(plan['front_slack_bits'],K)
                    self.assertLess(plan['back_slack_bits'],K)

    def test_whole_row_padding_and_nested_splitting_preserve_compact_ranges(self):
        # Explicit tagged records: front fields, active coordinates and back
        # fields remain full Cartesian ranges in each row of every child.
        W,depth,rows=3,2,10
        divisor=W**depth;padded=((rows+divisor-1)//divisor)*divisor
        self.assertLess(padded,2*rows)
        suffix=list(product(range(2),range(2),range(4),range(2)))
        stream={(r,s):(r,s) if r<rows else None for r in range(padded) for s in suffix}
        def recurse(current,count,left):
            for row in range(count):
                self.assertEqual({s for r,s in current if r==row},set(suffix))
            if not left:return current
            self.assertEqual(count%W,0)
            children=[]
            for role in range(W):
                child={(r//W,s):value for (r,s),value in current.items() if r%W==role}
                self.assertEqual(len(child)*W,len(current))
                children.append(recurse(child,count//W,left-1))
            return {(g*W+w,s):value for w,child in enumerate(children)
                    for (g,s),value in child.items()}
        self.assertEqual(recurse(stream,padded,depth),stream)
        self.assertEqual({k:v for k,v in stream.items() if k[0]<rows},
                         {(r,s):(r,s) for r in range(rows) for s in suffix})

    def test_rotation_streaming_two_piece_algorithm(self):
        # Prefix controls can be far wider than the target. Simulate the
        # two streaming piece tapes and variable per-prefix merge lengths.
        Qtarget=4;suffix=3;prefixes=257
        one=[];two=[]
        for prefix in range(prefixes):
            a=(prefix*prefix+3*prefix+1)%Qtarget
            rows=[(prefix,y,s) for y in range(Qtarget) for s in range(suffix)]
            cut=(Qtarget-a)*suffix
            one.extend(rows[:cut]);two.extend(rows[cut:])
        i=j=0;out=[]
        for prefix in range(prefixes):
            a=(prefix*prefix+3*prefix+1)%Qtarget
            out.extend(two[j:j+a*suffix]);j+=a*suffix
            out.extend(one[i:i+(Qtarget-a)*suffix]);i+=(Qtarget-a)*suffix
        self.assertEqual((i,j),(len(one),len(two)))
        for index,record in enumerate(out):
            prefix=index//(Qtarget*suffix);target=(index//suffix)%Qtarget
            a=(prefix*prefix+3*prefix+1)%Qtarget
            self.assertEqual(record,(prefix,(target-a)%Qtarget,index%suffix))

    def test_repair_density_with_explicit_common_cutoff(self):
        for p in (2,3,16,1000):
            K=8*(p-1).bit_length()+16
            row=repair_bound(p,p,K)
            self.assertLessEqual(row['late_bad_fraction_upper'],Q(5,128*p**3))
            with self.assertRaises(ValueError):repair_bound(p,p,K-1)

    def test_stopped_recurrence_with_all_exponent_orderings(self):
        m=16;tau=Q(1,2);power=16;d=m**power;G=16
        for branch,sigma in ((2,Q(1,4)),(4,Q(1,2)),(8,Q(3,4))):
            for beta in (Q(1,4),Q(1,2),Q(3,4)):
                ex=layer_exponents(tau,sigma,beta,Q(1,4))
                stop=m**int(power*beta);size=d;levels=[]
                while size>=stop:levels.append(size);size//=m
                F=Q(size)
                for e in reversed(levels):F=branch*F+isqrt(G*e)+1
                leaf=branch**len(levels)*size
                ci=power*ex['internal'];cl=power*ex['leaf']
                self.assertEqual(ci.denominator,1);self.assertEqual(cl.denominator,1)
                self.assertLessEqual(F-leaf,8*(power+1)*max(1,Q(branch,4))*m**int(ci))
                self.assertLessEqual(leaf,m**int(cl))
                self.assertEqual(ex['preprocessing'],Q(3,4))

    def test_parameters_and_milestones(self):
        c=certificate();main=c['main'];p=parameters()
        self.assertEqual(main['minimum_margin'],Q(333833,4*10**15))
        self.assertGreater(main['absorption_gap'],0)
        self.assertGreater(p.kappa,Q(1,2**34))
        self.assertLess(c['scoped_ceiling']['upper'],Q(1,2**33))
        self.assertGreater(c['scoped_ceiling']['witness_fraction_of_upper'],Q(99,100))
        self.assertEqual(main['recurrence']['preprocessing'],Q(4,5))
        for row in c['milestones'].values():self.assertGreater(row['absorption_gap'],0)
        n=network(25)
        self.assertLess(log_integer_bounds(n['m'])[1],Q(966,100))
        self.assertGreater(n['eta_c'],Q(418,10**12)*Q(966,100))

    def test_missing_reservation_guard_and_final_slack_are_rejected(self):
        p=parameters()
        for bad in (replace(p,c=Q(1,10**20)),replace(p,C1=Q(2)),
                    replace(p,kappa=Q(1,2**33)),replace(p,sigma=Q(1,2)),
                    replace(p,lamp=1-Q(418,10**12))):
            with self.assertRaises(ValueError):check(bad)


if __name__=='__main__':unittest.main()
