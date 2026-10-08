"""Structural failure modes and source dependencies of the two-stage proof."""
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
import re
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import two_stage as t
from make_two_stage_patch import patched_files

ROOT=Path(__file__).resolve().parents[1]


class TwoStage(unittest.TestCase):
    def test_budget_charges_one_correction_per_pair(self):
        for h,R,c in ((32,123157,False),(34,2379258,True)):
            n=t.counts(h,R,c)
            self.assertEqual(n['s']-n['edge_calls'],n['N'])
            self.assertGreater(n['deficit'],0)
            self.assertGreater(n['s']+n['N'],n['W']*n['m'])

    def test_smaller_ground_size_has_no_saving(self):
        with self.assertRaisesRegex(ValueError,'positive saving'):
            t.counts(20,1000,True)

    def test_declared_savings_have_exact_exponential_certificates(self):
        for n,a,b in ((t.counts(32,123157),t.BIT_SAVING,Q('6.932')),
                       (t.counts(34,2379258,True),t.COMPLEX_SAVING,Q('7.05273'))):
            cert=t.logarithm_certificate(n,a,b)
            self.assertGreater(cert['deficit_slack'],0)
            self.assertGreater(cert['exp_partial_sum'],n['m'])

    def test_conversation_bit_saving_does_not_fit_actual_graph(self):
        with self.assertRaisesRegex(ValueError,'Unsupported reconstructed bit'):
            t.parameter_certificate(replace(t.parameters(),tau=1-Q('4.885e-7')))
        with self.assertRaisesRegex(ValueError,'Unsupported finite saving'):
            t.logarithm_certificate(t.counts(32,123157),Q('4.885e-7'),Q('6.932'))

    def test_all_assembly_conditions_and_strict_gap(self):
        c=t.parameter_certificate()
        self.assertEqual(len(c['constraint_slacks']),31)
        self.assertEqual(len(c['margins']),7)
        self.assertEqual(c['minimum_margin'],Q('6.292768536e-9'))
        self.assertEqual(c['absorption_gap'],Q('2.768536e-12'))

    def test_requested_thousandfold_target_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'absorption gap'):
            t.parameter_certificate(replace(t.parameters(),kappa=Q('5.91e-7')))

    def test_strict_ceiling_is_rejected(self):
        a=t.COMPLEX_SAVING
        with self.assertRaisesRegex(ValueError,'absorption gap'):
            t.parameter_certificate(replace(t.parameters(),kappa=a/(5+4*a)))

    def test_stopped_guard_includes_copies(self):
        n=t.counts(34,2379258,True)
        c=t.guard_certificate(n,768202,1611056)
        self.assertLess(c['total_node_updates_upper'],c['E'])
        self.assertEqual(c['C1'],Q('4.9997'))
        self.assertTrue(c['correction_copy_and_wrappers_included'])

    def test_dirty_bit_scratch_full_two_stage_map(self):
        self.assertEqual(t.scalar_audit()['independent_input_variables'],7600)

    def test_dirty_complex_scratch_full_two_stage_map(self):
        self.assertEqual(t.scalar_audit(7,True)['independent_input_variables'],31010)

    def test_exact_complex_cancellation_and_diagonal_endpoint(self):
        self.assertTrue(t.complex_endpoint_audit()['diagonal_endpoint_exact'])

    def test_missing_endpoint_signs_leave_wrong_transform(self):
        x=[t.ONE,t.ZERO]
        F=t.full_phase(x,1)
        untranslated=[x[i^1] for i in range(2)]
        self.assertNotEqual(t.full_phase(untranslated,1),F)

    def test_one_interchange_reflection_over_prime_powers(self):
        self.assertTrue(t.reflection_audit()['one_recursive_swap_block_exact'])


class TwoStagePatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.files={n:(o,x) for n,o,x in patched_files()}

    def test_new_bit_transfer_drives_arbitrary_width_operation(self):
        x=self.files['build/sections/04-swap.tex'][1]
        tail=x[x.index(r'\subsection{Removing width and row restrictions}'):]
        self.assertIn('prop:two-stage-power-interchange',tail)
        self.assertNotIn('prop:power-interchange',tail)
        self.assertIn((ROOT/'notes/direct-swap-transfer.tex').read_text(),x)

    def test_new_phase_contract_has_charged_endpoint_children(self):
        x=self.files['build/sections/05-layers.tex'][1]
        self.assertIn('28546995136',x)
        self.assertIn('33000319052800',x)
        self.assertIn((ROOT/'notes/two-stage-phase-transfer.tex').read_text(),x)
        self.assertNotIn('i^{27f}',x)
        self.assertNotIn('none of the corrections',x)
        self.assertIn('copy corrections are covered',x)

    def test_new_assembly_exponents_and_stopping_parameter(self):
        x=self.files['build/sections/08-assembly.tex'][1]
        for item in (r'\frac{629}{10^{11}}',r'e^{10000}<d',
                     r'p^{199999/1000000}',r'p^{1599997/2000000}',
                     r'\frac{786596067}{125000000000000000}',
                     r'\max\{\sigma-\tau,0\}'):
            self.assertIn(item,x)
        self.assertNotIn('=\\tau$',x)
        self.assertNotIn('591',x)

    def test_pinned_inputs_and_all_internal_references(self):
        for n,(o,x) in self.files.items(): self.assertEqual(o,(ROOT/'upstream'/n).read_text())
        alltext='\n'.join(self.files.get('build/'+str(p.relative_to(ROOT/'upstream/build')),
                            ('',p.read_text()))[1] for p in (ROOT/'upstream/build').rglob('*.tex'))
        labels=re.findall(r'\\label\{([^}]+)\}',alltext)
        refs=re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}',alltext)
        self.assertEqual(len(labels),len(set(labels)))
        self.assertEqual(set(refs)-set(labels),set())


if __name__=='__main__': unittest.main()
