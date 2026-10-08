"""Controls for a reversible merge tree and scoped interval-schedule bounds."""
from fractions import Fraction as Q
from pathlib import Path
import itertools
import random
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_gather_schedules import (swap_intervals,recursive_gather,lag_changes,
    boundary_lower_bound,potential,potential_constant,dyadic_charge_upper,
    dyadic_tree_charge,reuse_screen,segmented_shear,whole_slot_shear,
    carry_failure_fraction,certificate)
from audit_short_guards import gather,ungather,compact_add
from prepare_layers import BIT_SAVING


def swaps(length):
    for width in range(1,length//2+1):
        for left in range(length-2*width+1):
            for right in range(left+width,length-width+1):
                yield left,right,width


class GatherSchedules(unittest.TestCase):
    def test_recursive_schedule_every_small_offset_and_inverse(self):
        for f,g in itertools.product(range(2,10),range(1,4)):
            for K in (2*g,2*g+3):
                for rho in range(K):
                    labels,ops=recursive_gather(f,K,rho,g)
                    active=[rho+j*K+t for j in range(f-1) for t in range(g)]
                    self.assertEqual(labels[-len(active):],active)
                    self.assertEqual(len(ops),f-1)
                    for op in reversed(ops):labels=swap_intervals(labels,*op)
                    self.assertEqual(labels,list(range(f*K)))

    def test_unstable_guard_order_is_safe_for_complete_addition(self):
        rng=random.Random(109)
        for f,K,rho,g in ((3,5,4,2),(5,12,11,6),(6,18,7,8)):
            order,_=recursive_gather(f,K,rho,g)
            n=f-1
            tail=f*K-n*g
            for _ in range(80):
                x,y,z=(rng.getrandbits(f*K) for _ in range(3))
                packed=[gather(v,order) for v in (x,y,z)]
                changed=compact_add(*(v>>tail for v in packed),n,g)
                out=[ungather((new<<tail)|(old&((1<<tail)-1)),order)
                     for old,new in zip(packed,changed)]
                top=rho+n*K
                out[1]^=((x>>top)&1)<<top
                mask=sum(((x>>(rho+j*K))&1)<<(rho+j*K) for j in range(f))
                self.assertEqual(tuple(out),(x,y^mask,z))

    def test_all_small_swap_boundary_and_lag_bounds(self):
        for length in range(2,9):
            for colors in itertools.product(range(2),repeat=length):
                initial=[lag_changes(colors,t) for t in range(1,length//2+1)]
                for op in swaps(length):
                    changed=swap_intervals(colors,*op)
                    for t,old in enumerate(initial,1):
                        delta=abs(old-lag_changes(changed,t))
                        self.assertLessEqual(delta,4*min(op[2],t))

    def test_boundaries_also_cover_reversals_and_single_coordinate_moves(self):
        for colors in itertools.product(range(2),repeat=6):
            old=lag_changes(colors,1)
            for left in range(6):
                for right in range(left+1,7):
                    changed=colors[:left]+tuple(reversed(colors[left:right]))+colors[right:]
                    self.assertLessEqual(abs(old-lag_changes(changed,1)),2)
                for target in range(6):
                    changed=list(colors)
                    bit=changed.pop(left)
                    changed.insert(target,bit)
                    self.assertLessEqual(abs(old-lag_changes(changed,1)),4)

    def test_exact_multiscale_potential_controls(self):
        rng=random.Random(10959)
        for q in (Q(5,4),Q(3,2),Q(7,4)):
            for n,g in ((2,1),(3,2),(4,4),(7,8)):
                K=2*g+1
                labels,ops=recursive_gather(n+1,K,K-1,g)
                active={K-1+j*K+t for j in range(n) for t in range(g)}
                colors=[int(i in active) for i in range((n+1)*K)]
                expected=2*(n-1)*sum(q**j for j in range(g.bit_length()))
                final=[colors[i] for i in labels]
                self.assertEqual(potential(colors,g,q)-potential(final,g,q),expected)
                # The local potential bound holds on arbitrary intermediate
                # color words, not only on separated or already packed ones.
                rng.shuffle(colors)
                for op in ops:
                    changed=swap_intervals(colors,*op)
                    delta=abs(potential(colors,g,q)-potential(changed,g,q))
                    self.assertLessEqual(delta,potential_constant(q)*dyadic_charge_upper(op[2],q))
                    colors=changed

    def test_dyadic_tree_cost_and_linear_call_lower_bound(self):
        q=Q(3,2)
        for depth in range(8):
            n=1<<depth
            _,ops=recursive_gather(n+1,3,0,1)
            cost=sum(q**(width.bit_length()-1) for _,_,width in ops)
            self.assertTrue(all(width&(width-1)==0 for _,_,width in ops))
            self.assertEqual(cost,dyadic_tree_charge(n,q))
            self.assertLessEqual(cost,n*(1+1/(2*(1-q/2))))
            self.assertLessEqual(boundary_lower_bound(n),len(ops))
            self.assertGreaterEqual(4*boundary_lower_bound(n),2*n-2)

    def test_optimistic_round_reuse_cannot_remove_quadratic_loss(self):
        for a in (Q(1,4),Q(1,1000),BIT_SAVING):
            optimum=reuse_screen(a,a)
            self.assertEqual(optimum['largest_power_saving_in_this_bound'],a*a)
            self.assertEqual(optimum['amortized_gather_exponent'],1-a*a)
            self.assertEqual(optimum['compact_root_exponent'],1-a*a)
            for b in (Q(0),a/2,a,2*a,a/(1-a),Q(1)):
                self.assertLessEqual(reuse_screen(a,b)['largest_power_saving_in_this_bound'],a*a)
        result=certificate()
        self.assertIn('NO NEW KAPPA',result['status'])
        self.assertEqual(result['assembly_ceiling_for_this_reuse_model'],BIT_SAVING**2/5)
        self.assertIn('Coded role streams',result['excluded_scope'])

    def test_naive_affine_shear_has_dense_guard_carries(self):
        for n,g,K in ((1,1,2),(1,2,3),(1,2,5),(2,1,2),(2,2,3),(3,1,2)):
            bad=total=0
            for controls in itertools.product(range(1<<g),repeat=n):
                for y in range(1<<(n*K)):
                    bad+=segmented_shear(y,controls,g,K)!=whole_slot_shear(y,controls,g,K)
                    total+=1
            self.assertEqual(Q(bad,total),carry_failure_fraction(n,g))
        self.assertEqual(carry_failure_fraction(1,6),Q(63,128))
        self.assertGreater(carry_failure_fraction(16,6),Q(9999,10000))


if __name__=='__main__':unittest.main()
