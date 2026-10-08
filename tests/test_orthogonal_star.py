"""Failure modes and source integration of the conditional star construction."""
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
import re
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from orthogonal_star import (counts, guard_certificate, parameters,
    parameter_certificate, construct, symbolic_audit, BIT_SAVING, COMPLEX_SAVING)
from make_orthogonal_star_patch import patched_files

ROOT = Path(__file__).resolve().parents[1]


class OrthogonalStar(unittest.TestCase):
    def test_uncorrected_twenty_two_source_residual_is_alternating(self):
        target = (1<<0)|(1<<1)|(1<<2)
        sources = [(1<<0)|(1<<1)|(1<<k) for k in range(3,25)]
        total = 0
        for vector in sources: total ^= vector
        self.assertEqual(((1<<25)-1)^target^total,0)
        self.assertEqual(25-1-len(sources),2)
        # Both repaired residuals have a nonzero canonical vector.
        self.assertNotEqual(((1<<25)-1)^target^sources[0],0)
        self.assertNotEqual(((1<<25)-1)^target^total^sources[0],0)

    def test_full_star_complement_would_be_alternating(self):
        total=0
        for k in range(2,25): total^=(1<<0)|(1<<1)|(1<<k)
        self.assertEqual(total,(1<<25)-1)
        # Its two-dimensional complement cannot be charged by unit kernels.
        self.assertEqual(25-23,2)

    def test_orthonormality_is_specific_to_a_fixed_pair(self):
        vectors=[(1<<0)|(1<<1)|(1<<k) for k in range(2,25)]
        for i,x in enumerate(vectors):
            for j,y in enumerate(vectors):
                self.assertEqual((x&y).bit_count()%2,i==j)
        x=(1<<0)|(1<<1)|(1<<2)
        y=(1<<0)|(1<<3)|(1<<4)
        self.assertEqual((x&y).bit_count()%2,1)

    def test_dirty_scratch_identity_over_rationals_in_both_directions(self):
        self.assertEqual(symbolic_audit(),dict(h=7,independent_input_variables=478,
            forward_and_inverse_exact=True,arbitrary_scratch_restored=True))

    def test_guard_and_margins_for_replacement_network(self):
        n=counts();guard=guard_certificate(n);w=parameter_certificate()
        self.assertEqual(n['eta'],Q(14,455245625))
        self.assertLess(guard['total_node_updates_upper'],guard['E'])
        self.assertEqual(w['minimum_margin'],Q('5.913042e-10'))
        self.assertEqual(w['absorption_gap'],Q('3.042e-13'))
        self.assertEqual(len(w['constraint_slacks']),31)

    def test_old_complex_saving_and_spacing_do_not_support_new_witness(self):
        p=parameters()
        with self.assertRaisesRegex(ValueError,'lambda_above_sigma|leaf_cost'):
            parameter_certificate(replace(p,sigma=1-Q(418,10**12)))
        with self.assertRaisesRegex(ValueError,'absorption gap'):
            parameter_certificate(replace(p,c=Q(1,5)))

    def test_fixed_saving_supremum_and_strict_absorption(self):
        a=min(BIT_SAVING,COMPLEX_SAVING)
        ceiling=a/(5+4*a)
        self.assertEqual(ceiling,Q(37,62500000148))
        self.assertLess(parameters().kappa,ceiling)
        with self.assertRaisesRegex(ValueError,'absorption gap'):
            parameter_certificate(replace(parameters(),kappa=ceiling))


class OrthogonalStarPatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.files={name:(old,new) for name,old,new in patched_files()}

    def test_replacement_proof_and_constants_are_used_by_layer(self):
        motifs=self.files['build/sections/03-motifs.tex'][1]
        layer=self.files['build/sections/05-layers.tex'][1]
        self.assertIn((ROOT/'notes/orthogonal-star-construction.tex').read_text(),motifs)
        self.assertIn('prop:orthogonal-star-interface',layer)
        self.assertNotIn('prop:compact-complex-interface',layer)
        self.assertIn('7706397940000',layer)
        self.assertIn('120412464109500000',layer)
        self.assertIn(r'$\sigma=1-318/10^{11}$',layer)

    def test_assembly_uses_maximum_recurrence_and_new_spacing(self):
        text=self.files['build/sections/08-assembly.tex'][1]
        self.assertIn(r'\max\{\sigma-\tau,0\}=\tau',text)
        self.assertIn('c=1',text)
        self.assertIn(r'\kappa=\frac{591}{10^{12}}>2^{-31}',text)
        self.assertIn(r'\frac{2956521}{5\cdot10^{15}}',text)
        self.assertIn(r'K=\Theta(p^{1999/10000})',text)

    def test_pinned_inputs_and_all_internal_references(self):
        for name,(old,new) in self.files.items():
            self.assertEqual(old,(ROOT/'upstream'/name).read_text())
        texts=[]
        for path in (ROOT/'upstream/build').rglob('*.tex'):
            name='build/'+str(path.relative_to(ROOT/'upstream/build'))
            texts.append(self.files[name][1] if name in self.files else path.read_text())
        all_text='\n'.join(texts)
        labels=re.findall(r'\\label\{([^}]+)\}',all_text)
        refs=re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}',all_text)
        self.assertEqual(len(labels),len(set(labels)))
        self.assertEqual(set(refs)-set(labels),set())


if __name__=='__main__':unittest.main()
