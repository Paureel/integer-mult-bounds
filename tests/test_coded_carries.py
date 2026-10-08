"""Exact carry-code identities and small controls for the flat-code bound."""
from pathlib import Path
import itertools
import random
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_coded_carries import (coded_flat,coded_factored,direct,carry_pattern,
    branch_offset,offset_support,affine_agreement_control,valuation_pivots,
    affine_path_maps,order_control,certificate)


class CodedCarries(unittest.TestCase):
    def test_exact_codes_on_every_small_basis_and_control(self):
        for n,g,K in ((1,1,2),(1,2,3),(2,1,2)):
            size=1<<(n*K)
            for controls in itertools.product(range(1<<g),repeat=n):
                for source in range(size):
                    state=[int(y==source) for y in range(size)]
                    self.assertEqual(coded_flat(state,controls,g,K),direct(state,controls,g,K))
                    self.assertEqual(coded_factored(state,controls,g,K),direct(state,controls,g,K))

    def test_codes_restore_all_dirty_gaps_on_larger_arrays(self):
        rng=random.Random(109)
        for controls,g,K in (((1,3),2,4),((1,2,3),2,3),((1,1,1),1,4)):
            size=1<<(len(controls)*K)
            state=[rng.randrange(-100,101) for _ in range(size)]
            expected=direct(state,controls,g,K)
            self.assertEqual(coded_flat(state,controls,g,K),expected)
            self.assertEqual(coded_factored(state,controls,g,K),expected)
            active=sum(((1<<g)-1)<<(j*K) for j in range(len(controls)))
            for y in range(size):
                destination=(y+branch_offset(controls,g,K,carry_pattern(y,controls,g,K)))%size
                self.assertEqual(y&~active,destination&~active)

    def test_distinct_translation_branches_are_exponential(self):
        for n,K in ((1,3),(2,3),(3,3),(4,3)):
            self.assertEqual(len(offset_support(n,K)),1<<n)
            offsets={branch_offset([1]*n,1,K,s) for s in range(1<<n)}
            self.assertEqual(offsets,offset_support(n,K))

    def test_exhaustive_affine_agreement_including_boundary_case(self):
        for n,K in ((1,2),(2,2),(3,2),(1,3),(2,3),(3,3)):
            row=affine_agreement_control(n,K)
            self.assertEqual(row['maximum_agreement']*(1<<row['minimum_flat_affine_movement_gates']),
                             row['addresses'])
        # With only one gap bit and one selected bit, the target is itself
        # affine. The K>=3 hypothesis must not be silently discarded.
        self.assertEqual(affine_agreement_control(1,2)['maximum_agreement'],4)

    def test_valuation_pivots_are_injective_for_all_small_slopes(self):
        for n,K,rho in ((1,3,0),(2,3,0),(2,4,0),(2,4,1)):
            modulus=1<<(n*K)
            for a in range(modulus):
                coordinates,weights,values=valuation_pivots(a,n,K,rho)
                sums={sum(w for j,w in enumerate(weights) if subset>>j&1)%modulus
                      for subset in range(1<<len(weights))}
                self.assertEqual(len(sums),1<<len(weights))
                self.assertGreaterEqual(len(coordinates),n)
                self.assertEqual(len(set(values)),len(values))

    def test_affine_path_count_and_fixed_encoding_order(self):
        gates=[(3,1),(5,7),(1,8),(7,2)]
        maps=affine_path_maps(gates,64)
        explicit=set()
        for choice in range(1<<len(gates)):
            a,b=1,0
            for j,(c,d) in enumerate(gates):
                if choice>>j&1:a,b=(c*a)%64,(c*b+d)%64
            explicit.add((a,b))
        self.assertEqual(maps,explicit)
        self.assertLessEqual(len(maps),1<<len(gates))
        for g,K in ((1,3),(2,4),(3,5)):
            size=1<<K
            full=list(range(size))
            short=list(range(size))
            for _ in range(1<<g):
                full=[(y+1)%size for y in full]
                short=[(y&~((1<<g)-1))|((y+1)&((1<<g)-1)) for y in short]
            self.assertEqual(short,list(range(size)))
            self.assertNotEqual(full,list(range(size)))
            self.assertGreater(order_control(g,K)['whole_shift_order'],1<<g)

    def test_ordered_nonlinear_offsets_preserve_fiber_affinity_until_a_swap(self):
        N=8
        def ordered(p,y,z):
            p=(3*p+1)%N
            z=(z+(y&1)*p)%N  # Nonlinear, but targets a later field.
            y=(3*y+(p^3))%N
            p=(p+2)%N
            y=(5*y+p*p)%N
            return p,y,z
        for p,z in itertools.product(range(N),repeat=2):
            values=[ordered(p,y,z)[1] for y in range(N)]
            a,b=(values[1]-values[0])%N,values[0]
            self.assertEqual(values,[(a*y+b)%N for y in range(N)])
        # Swapping the updated later field into y permits backward influence
        # and leaves the theorem's class: y now depends nonlinearly on old y.
        values=[y&1 for y in range(N)]
        self.assertNotEqual(values,list(range(N)))
        self.assertFalse(any(values==[(a*y+b)%N for y in range(N)]
                             for a,b in itertools.product(range(N),repeat=2)))

    def test_assessment_and_scope_stay_explicit(self):
        row=certificate()
        self.assertIn('NO NEW KAPPA',row['status'])
        self.assertIn('Recursive role splitting',row['excluded_scope'])
        self.assertIn('no role-volume contraction',row['exact_code']['recurrence'])
        self.assertIn('Stop this bounded attempt',row['assessment'])


if __name__=='__main__':unittest.main()
