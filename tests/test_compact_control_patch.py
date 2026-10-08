"""Integration boundaries of the independent compact-control source patch."""
from pathlib import Path
import re
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from make_compact_control_patch import patched_files

ROOT=Path(__file__).resolve().parents[1]


class CompactControlPatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files={name:(old,new) for name,old,new in patched_files()}
        cls.layer=cls.files['build/sections/05-layers.tex'][1]
        cls.assembly=cls.files['build/sections/08-assembly.tex'][1]

    def test_pinned_inputs_and_all_extension_proofs(self):
        for name,(old,new) in self.files.items():
            self.assertEqual(old,(ROOT/'upstream'/name).read_text())
        for name in ('compact-control-movement.tex','compact-control-layout.tex',
                     'compact-control-guard.tex'):
            self.assertIn((ROOT/'notes'/name).read_text(),self.layer)
        self.assertIn((ROOT/'notes/independent-complex.tex').read_text(),
                      self.files['build/sections/03-motifs.tex'][1])

    def test_legacy_rectangle_contract_remains_for_appendix(self):
        self.assertEqual(self.layer.count(r'\label{lem:packed-selected-bit-rectangle}'),1)
        self.assertEqual(self.layer.count(r'\label{prop:compact-selected-addition}'),1)
        self.assertIn('grouped-rectangle',self.layer)
        # Only the new batching section is used by the improved layer.
        batching=self.layer[self.layer.index(r'\subsection{Batching a common layer'):]
        self.assertNotIn(r'(eK)^\tau',batching)
        self.assertNotIn(r'\tau(1+c/\beta)',batching)
        self.assertNotIn('lem:packed-selected-bit-rectangle',batching)
        self.assertIn('prop:compact-selected-addition',batching)

    def test_separate_arities_and_new_guard(self):
        self.assertIn(r'm=m_{\rm c}=15625',self.layer)
        self.assertIn(r'm_{\rm b}=125000',self.layer)
        self.assertNotIn('prop:complex-motif-interface',self.layer)
        self.assertIn('prop:compact-complex-interface',self.layer)
        self.assertIn(r'C_1=5-4\beta+\zeta',self.layer)
        self.assertIn(r'18mB^2(1+1/\zeta)',self.layer)

    def test_assembly_includes_reservations_and_local_repair_sum(self):
        self.assertIn(r"1-c<\lambda'",self.assembly)
        self.assertIn(r'd^{10000}\le b^{1999}',self.assembly)
        self.assertIn(r'\kappa=\frac{83}{10^{12}}',self.assembly)
        self.assertIn(r'G_*-\kappa',self.assembly)
        self.assertIn('volume-weighted recurrence',self.assembly)
        self.assertNotIn(r"=O(Vp^{A'}2^{-K})",self.assembly)
        self.assertNotIn(r'$C_1=2$',self.assembly)

    def test_no_dangling_or_duplicate_internal_labels(self):
        texts=[]
        for path in (ROOT/'upstream/build').rglob('*.tex'):
            name='build/'+str(path.relative_to(ROOT/'upstream/build'))
            texts.append(self.files[name][1] if name in self.files else path.read_text())
        all_text='\n'.join(texts)
        labels=re.findall(r'\\label\{([^}]+)\}',all_text)
        self.assertEqual(len(labels),len(set(labels)))
        refs=re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}',all_text)
        self.assertEqual(set(refs)-set(labels),set())


if __name__=='__main__':unittest.main()
