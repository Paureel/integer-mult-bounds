"""Address identities and physical control order, not tape-runtime claims."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_compact_controls import (program,execute,ideal,exceptional,
    repaired,controls,certificate)


class CompactControls(unittest.TestCase):
    def test_every_rotation_uses_only_preceding_controls(self):
        for late,count in ((False,4),(True,12)):
            order,ops=program(2,8,7,2,late)
            self.assertEqual(sum(op[0]=='swap' for op in ops),count)
            for op in ops:
                if op[0]=='rotate':
                    self.assertTrue(all(order.index(c)<order.index(op[1]) for c in op[2]))

    def test_exhaust_small_single_segment_and_dirty_fields(self):
        n,K,rho,G=1,5,0,1
        good=bad=0
        for late in (False,True):
            for x in (0,1):
                for y in range(1<<(2*K)):
                    for t in (0,1):
                        for b in (0,1):
                            for u in ((0,1) if late else (None,)):
                                state=dict(x=x,y=y,t=t,b=b)
                                if late:state['u']=u
                                result=execute(state,n,K,rho,G,late=late)
                                wanted=dict(state,y=y^x)
                                self.assertEqual(ideal(state,n,K,rho),wanted)
                                is_bad=exceptional(state,n,K,rho,G,late)
                                self.assertEqual(exceptional(result,n,K,rho,G,late),is_bad)
                                self.assertEqual(execute(result,n,K,rho,G,late=late,inverse=True),state)
                                if is_bad:bad+=1
                                else:
                                    good+=1;self.assertEqual(result,wanted)
                                self.assertEqual(repaired(state,n,K,rho,G,late),wanted)
        self.assertGreater(good,0);self.assertGreater(bad,0)

    def test_multiple_segments_extreme_offsets_and_inverse(self):
        result=controls()
        self.assertEqual(result['packed_cases']['early'],3600)
        self.assertEqual(result['packed_cases']['late'],3600)
        self.assertGreater(result['packed_cases']['good'],0)

    def test_saturated_digit_is_excluded_even_with_safe_target_guard(self):
        state=dict(x=1,y=40,t=3,b=2)
        self.assertTrue(exceptional(state,1,7,0,2))
        state['t']=2
        self.assertFalse(exceptional(state,1,7,0,2))

    def test_certificate_does_not_claim_a_tape_bound(self):
        c=certificate()
        self.assertIn('ADDRESS-ONLY',c['status'])
        self.assertIn('NO EXPONENT CLAIM',c['status'])
        self.assertEqual(len(c['outside_this_checker']),4)
        self.assertIn('compact-control-note.tex',c['cost_proof'])


if __name__=='__main__':unittest.main()
