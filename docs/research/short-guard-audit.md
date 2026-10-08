# Short working guards reduce sparse addition to a gathering problem

**Later result:** [compact dirty controls](current-status.md) bypass gathering
and supply a local conditional exponent in the 30s. The gathering reduction
and its unproved gatherer below are preserved as historical research.

**Follow-up:** the [gather-schedule audit](gather-schedule-audit.md) constructs
a reversible merge tree, proves a linear call-count obstruction for serial
interval schedules, and checks why ordinary round reuse retains quadratic
accounting. Coded or direct strided operations remain open.

**The published result remains conditional kappa=2^-59.** This pass proves
a reduction, conditional on the existing packed-rectangle and chunk-swap
interfaces. Its working guards can have width O(log p), independently of the
original spacing K. Gathering those guards and restoring the original layout
still need a faster implementation. No such implementation or new kappa is
claimed here.

This follows the [complete-block audit](fused-block-audit.md), which ruled out
one coordinate-child/pointwise-only recursion. The present reduction keeps
physical address movement and specifies the missing movement theorem.
The exact address simulator is [audit_short_guards.py](../../scripts/audit_short_guards.py),
with [controls and conditional targets](../../certificates/short-guard-audit.json).

## 1. Short guards suffice after gathering

Retain the complete rectangle from `lem:packed-selected-bit-rectangle` in
[05-layers.tex](../../upstream/build/sections/05-layers.tex). Each of the three
slots x,y,z has L=fK bits. Selected positions are rho+jK, 0<=j<f,
0<=rho<K, numbered from the least significant bit. Spectator fields between
slots can have arbitrary positive lengths. Records have R bits, total volume
V=MR, A=ceil(log2(2V))=O(p), and R exceeds every fixed polynomial in p.
Assume f<=p and choose

    g = 4 ceil(log2 p) + 6.

For fixed positive c and epsilon, K=floor(d^c), d approximately p^epsilon,
eventually satisfies K>=g. This can require a very large cutoff, but changes
only the cutoff of the asymptotic statement. We do not replace the original K
in the outer transform layout or in its power-saving estimate.

Put n=f-1. In each slot, gather the n disjoint windows

    [rho+jK, rho+jK+g), 0<=j<n,

into a contiguous most significant field of ng bits, preserving their order.
Keep all other coordinates in a spectator field of L-ng bits. These windows
fit even when rho=K-1: the highest original selected bit is omitted, so each
g-bit window ends before the next selected position. All bits in the windows
may be arbitrary; no clean or zero-filled scratch is needed.

The result is again a complete rectangle with three equal compact slots of
width ng. The new spectator intervals absorb the remaining fields. No
record is added or removed, so M,V,R,A are unchanged. The number of field
lengths remains fixed, and their descriptors still have O(A) bits. Constructing
these descriptors takes polynomial-in-p work, absorbed by the record regime.

Apply the original packed-rectangle lemma to the compact slots, with selected
spacing g and offset zero. Then undo the three gathering permutations and
apply one elementary XOR to the original highest selected x,y bits. When f=1,
only this last O(V) operation is needed. The compact lemma itself handles its
highest selected position separately, as in the original proof.

This implements exactly

    y_(rho+jK) <- y_(rho+jK) XOR x_(rho+jK), 0<=j<f.

It preserves all other address bits and every record payload, and restores
the entire arbitrary z slot. The simulator checks the forward address map,
its inverse gathering maps, and the correction of the eight modular rotations.
These are correctness checks, not a simulation of the claimed tape runtime.

### Use the explicit repair bound, not the stronger corollary hypothesis

The manuscript's asymptotic corollary assumes K/log p tends to infinity.
Our compact spacing g does not satisfy that assumption. Instead use the
lemma's preceding explicit estimate, valid for spacing at least six:

    O(V ((ng)^tau+1) + M A^3 + delta M A(R+A)),
    delta <= min(1, 80(n-1) 2^-g).

Since 2^g >= 64 p^4 and n<=f<=p,

    delta <= 80 f 2^-g <= (5/4) p^-3.

Dividing the two repair terms by V gives

    A^3/R = o(1),
    delta A (1+A/R) = O(p^-2).

Constants in A=O(p) are fixed for the family and need not be one. Thus the
entire compact addition costs

    O(V ((f log p)^tau+1)).

Exceptional-set invariance is inherited from the original proof: the eight
rotations S0 agree with the ideal map T0 off the bad set; both are bijections,
and T0 preserves that set. Hence S0 preserves it too, allowing the correction
T0 S0^-1 to sort only exceptional records. The code checks both good and bad
guard values, including wraparound and arbitrary higher bits.

## 2. The missing theorem is a uniform gatherer

Let G and G_inverse be costs of gathering and undoing the windows of one
specified slot, in a complete rectangle with arbitrary spectator fields.
The reduction gives, with a fixed number of calls,

    T_sparse <= O(G + G_inverse + V (f log p)^tau + V).

A usable gatherer must implement the physical record permutation, not just
compute a new address or attach metadata. It must work on a fixed number of
one-dimensional tapes, accept compact binary descriptors, handle arbitrary
payloads, and account for all padding, positioning, rewinds and cleanup.
The bound must be uniform over the permitted spectator lengths and payloads
within the fixed family. The inverse requires the same guarantee. Any
additional record volume must be explicitly bounded and charged.

Suppose, as a **missing hypothesis**, both directions cost

    O(V f^r K^theta polylog(p)),  0<r<1, theta>=0.

With K=d^c, stopping exponent beta, and complex branching exponent sigma,
the unequal-exponent summation in the [preparation note](layer-preparation.md)
then gives the internal exponents

    chi_gather = r + theta*c + (1-beta) max(sigma-r,0),
    chi_compact = tau + (1-beta) max(sigma-tau,0),

and the unchanged leaf exponent

    chi_leaf = sigma + beta(1-sigma).

The sufficient layer exponent is strictly above the maximum of these three.
The polylogarithmic factors are absorbed by fixed strict slack. They may depend
on p; an uncontrolled factor in log V or record width is not silently allowed.
If r<tau, the compact term still has exponent tau: a faster gatherer alone
does not improve that part of the reduction.

Taking r=tau and theta=1-tau is sufficient for the preparation note's exact
hypothetical witnesses:

| Complex network | Conditional target | Status |
| --- | --- | --- |
| Original h=50 family | kappa=2^-39 | Missing gather bound |
| Independently optimized h=25 family | kappa=2^-34 | Missing gather bound; source integration also outstanding |

These are implication checks on rational inequalities, not new multiplication
certificates. Other (r,theta) tradeoffs can be tested in the same formula.

The reason this could remove the quadratic loss is precise. The existing
wide-slot estimate has r=theta=tau, forcing c=O(1-tau). Replacing its spacing
penalty by theta=O(1-tau) can permit constant c. The final margin
epsilon*c*(1-tau) would then be linear in the bit-network saving, subject to
the other layer and assembly margins.

## 3. What easy gathering methods do and do not supply

Moving bits separately, or stable binary sorting on the gathered address
bits, gives an O(V f g) bound in the retained record regime. Even grouping
aligned g-bit windows and moving them individually gives only a linear-in-f
number of moves. Those estimates lack a strict sublinear active exponent.
Applying existing wide-slot primitives to the whole pattern retains the K
cost we are trying to remove. None proves the required new bound.

One must also not treat the varying radix 2^K as fixed. The elementary
fixed-radix digit lemma has radix-dependent stream counts. It cannot be used
unchanged with a growing radix at constant cost.

### A narrow obstruction to one-shot monotone stream gathering

There is a useful diagnostic for proposals that split the input into a fixed
number of globally monotone output streams and then merge them once.
Restrict the input addresses by allowing a guard field of a bits to vary,
followed in lexicographic significance by b active bits; fix every other bit.
Gathering the active bits into an extreme most significant field transposes
these two groups. Such a restriction exists in our window layout when f>=3
and K>g: use one intervening gap and the active windows below it. One may take
a=K-g and b=(f-2)g.

Write A0=2^a and B0=2^b. There are A0 B0 restricted records, ordered guard-major
on input and active-major on output. In any increasing or decreasing output
subsequence of the input stream, at most A0+B0-1 of these records can occur.
Indeed, the input row index is nondecreasing and the output column rank is
monotone; each new record changes at least one, and neither can change more
than its number of values minus one. Reordering the guard or active values
internally does not change this coarse bound. Therefore such a one-shot
split needs at least

    ceil(A0 B0 / (A0+B0-1))

global monotone streams. The stable transpose has longest increasing
subsequence A0+B0-1 and longest decreasing subsequence min(A0,B0), checked
on small exact controls.

**Scope:** this is not a lower bound for all linear-time fixed-tape algorithms.
Nested fiber reversals, multiple rounds, local stacks and coded combinations
are outside this restricted stream model. In particular, it does not exclude
the ordered-affine primitives already used in the manuscript. It prevents
one naive justification of free gathering; it does not rule out fast gathering.

## 4. Next research decision

The arithmetic and exceptional repair do not require the original wide K-bit
guards once the small working windows are together. The next substantive
task is to find a gathering construction with a provable cost in both f and K,
or a direct strided-window operation that avoids gathering entirely.

Begin with a complete small address permutation and its inverse, then derive
the growing-size recurrence before investing in a large search. Promising
directions are recursive gathering with coded intermediate streams, or a
retained layout shared across several operations with all alignment costs
charged. Repeating independent window moves or ordinary binary-key sorting
does not meet the target. The new reduction lets each candidate be assessed
without redoing the packed arithmetic and repair proof.

## Verification

Run `python3 scripts/audit_short_guards.py` and
`python3 -m unittest discover -s tests -p test_short_guards.py -v`, or
`make verify`. The seven tests cover exact gather/inverse permutations,
eight-rotation inversion, exceptional repair, complete row addition with
arbitrary spectators and scratch, logarithmic guard arithmetic, conditional
recurrence targets, and the restricted monotone-stream control. Finite tests
support the written reduction; they do not verify the upstream theorem or
establish the missing gatherer's runtime. Published certificates and patches
remain unchanged.
