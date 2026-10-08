# Packed movement audit: constants improve, the exponent obstruction remains

**Follow-up:** the [preparation pass](research/layer-preparation.md) extends
the recurrence sum below to both orderings of tau and sigma. The historical
calculations here retain their original parameters and scope.
The subsequent [short-guard reduction](research/short-guard-audit.md) shows
that logarithmic working guards suffice after gathering. The gathering and
inverse costs are still missing; it does not certify a new kappa.

October 7, 2026. This is a scoped follow-up to the conditional 2^-76 witness.
It audits the existing packed routine and its recurrence, not all possible
implementations of the same mathematical operator. No stronger headline kappa
is certified by this audit, and no upstream source or existing patch is changed.

## Findings

1. Retaining layouts between the eight packed rotations reduces the worst-case
   count from sixteen to eight full-slot swaps. This is a constant-factor change
   to an already constant count, so it does not improve the time exponent.
2. Summing the recurrence with K kept explicit removes an avoidable dependence
   on the stopping exponent beta. The revised sufficient layer condition is
   `lambda-prime > max(tau*(1+c), sigma + beta*(1-sigma))` when `sigma <= tau`,
   with strict final slack. This is a useful proof refinement, not a new primitive.
3. The root overhead still contains `(d K)^tau`. Its current upper bound can
   certify a sublinear layer only when `c < (1-tau)/tau`. Thus this refinement
   retains the quadratic dependence of the final saving on `a = 1-tau`.
4. A generic binary basis change does not commute through a child butterfly.
   Cancelling changes across children or pointwise gates needs additional
   algebraic compatibility; leaving them as metadata is not sufficient.

This audit itself leaves **kappa = 2^-76** unchanged. A subsequent
[stage-sharing construction](../notes/stage-reuse-note.tex) supports 2^-75
by changing the finite network. The sharper recurrence below has not
been incorporated into a replacement source patch or the main parameter checker.

## Where K enters

In `05-layers.tex`, a network invocation on e selected axes groups them into
m slots, each containing f = e/m complete K-bit chunks. A slot has width
L = f K. Its selected bits are at offsets rho + j K, for 0 <= j < f.

Each elementary binary row addition uses the eight-rotation gadget on three
slots x,y,z. A rotation must place its target after both controls to invoke
`lem:ordered-affine-streams`. The arbitrary-gap swap lemma moves a **complete
L-bit slot**, at cost O(V L^tau). The network dimension m and the number of
row additions are fixed, so the complete node overhead is

    O(V ((e K)^tau + 1)).

Full slot width, rather than the number of swaps, is the remaining source of
K-dependence. The manuscript already uses nonadjacent swaps inside this routine.
There is no growing quadratic swap count analogous to the axis-routing issue.

## Retaining the layout between rotations

The chronological target sequence is

    y, z, y, z, z, y, z, y.

The source restores the initial layout after each rotation. Instead, put the
next target into the rightmost of the three slot positions and retain that
layout until the next target needs to move. Restore the initial layout after
the last rotation and before exceptional-set repair.

All three slots have equal width, so the physical field lengths stay fixed.
Keep their three logical names in finite state. A rotation's two controls then
precede its target, and the same collapsed descriptors and offset formula apply.
The spectator intervals remain in their physical positions. The logical eight
rotations and their composition S0 are unchanged. Once the original layout is
restored, the existing exceptional-set predicate, destination keys, and repair
procedure apply without change. Tape count and payload preservation are unchanged.

There are six changes between successive target names. If y is initially
rightmost, those six swaps suffice. Otherwise one initial and one final swap
suffice in addition. A dynamic program over all six layouts, allowing every
whole-field transposition between rotations, verifies the following counts:

| Initially rightmost slot | Original swap-and-restore count | Retained-layout minimum |
| --- | ---: | ---: |
| x | 16 | 8 |
| y | 8 | 6 |
| z | 8 | 8 |

This finite optimum fixes the original rotation order, requires each target to
be rightmost, and restores the initial layout. It is not a lower bound on other
gadgets or streaming algorithms. Both schedules still cost O(V (f K)^tau).

## A sharper recurrence sum

Write B = s_c/W_c for the normalized branching factor and suppose
B <= m^sigma with sigma <= tau. These conditions hold for our current common
choice tau = sigma = 1-a. Fix K = floor(d^c) throughout the layer. At depth j,
the total normalized overhead of a root problem on e axes is bounded by

    O(B^j ((e K / m^j)^tau + 1)).

At every internal node e/m^j >= 1 and K >= 1. The +1 is absorbed, and the
sum over J = O(log d) levels is at most

    O(K^tau e^tau sum_{j < J} (B / m^tau)^j)
      = O(K^tau e^tau log d).

If B < m^tau, as certified for the present network, the geometric sum is
bounded by a fixed constant and this logarithm is unnecessary. Its possibly
large constant is independent of the input size.

Stopping below d^beta leaves the source's leaf bound unchanged:

    O(e^sigma d^(beta*(1-sigma))).

Summing the O(log d) base-m pieces and row preprocessing consequently gives

    O((log d)^2 [d^(tau*(1+c)) + d^(sigma+beta*(1-sigma)) + 1]).

Any fixed lambda-prime strictly greater than both displayed exponents absorbs
the logarithms. This replaces the stronger sufficient condition based on
`K <= e^(c/beta)`, which charged the maximum overhead exponent of every node
as though it were the root. It changes the analysis, not the executed procedure.
It leaves all row-padding, guard-depth and numerical arguments unchanged.
For sigma > tau, the geometric sum must be analyzed separately; the formula
above is not asserted for that case.

### Why the refinement does not reach the 60s

With tau = 1-a, the revised sufficient condition still needs

    (1-a)(1+c) < 1, hence c < a/(1-a).

The final layout margin remains g2 = epsilon*c*a. With the current C1 = 20
constraint epsilon < 1/20, every certificate using these bounds therefore has

    kappa < a^2 / (20*(1-a)) < 2^-75.

This is the same simple necessary upper bound established in the tuning note.
The refined recurrence can simplify parameter choices or improve constants,
but it cannot remove the second factor of a. This is a limitation of the
available estimates, not a proved lower bound on actual machine work.

## Why basis changes cannot simply be cancelled

An edge's child kernels are conjugated by a binary address permutation P_M.
The source uses the exact identity

    P_M X_v P_M^-1 = X_(Mv),

where X_v translates addresses by v. Therefore, with C_v = alpha I + beta X_v,

    P_M C_v P_M^-1 = C_(Mv).

For example, M(u,v) = (u,v xor u) sends direction (1,0) to (1,1). Thus its
conjugation of a one-coordinate child acts along a two-coordinate direction;
dropping the conjugations changes the operator. A finite Gaussian-integer
example in the checks distinguishes these operators exactly.

This does not exclude merging adjacent basis changes or choosing specially
compatible bases. But saving a fixed number of calls at each node only changes
a constant. To improve the exponent, a new argument must remove the wide-slot
cost or amortize it over growing amounts of work. Also, a pointwise scalar gate
combines matching addresses from its wire roles: independently retaining
different physical layouts on those roles requires alignment or a compatible
reformulation of that gate. The current contract does not supply it for free.

## Other tempting shortcuts and their missing guarantees

- Treating a K-bit chunk as one digit would use a growing radix. The elementary
  digit lemma explicitly fixes its radix; its proof uses radix-dependent stream
  counts. The current lemma cannot be invoked with radix 2^K at constant cost.
- Moving selected bits individually takes O(V f) for a slot with f selected
  positions. That has no sublinear saving in f, so it does not supply the
  required accelerated layer overhead.
- Replacing guard spacing K by O(log p) while otherwise retaining the transform
  layout gives only a polylogarithmic-in-p improvement in p K^(tau-1).
  That term cannot certify any fixed positive power saving p^(-kappa).

## Concrete target for further work

A stronger sparse selected-bit primitive would be consequential. For example,
a uniform bound O(V f^(1-b) K^theta), up to fixed logarithmic factors, would
replace the root condition by `1-b + theta*c < 1`. A substantially smaller
ratio theta/b would permit larger c. This is a desired new bound, not one
established by this audit. Any candidate must restore arbitrary scratch values,
include exceptional repair and descriptor work, and keep a fixed tape count.

The other route is a stronger finite network, improving the existing primitive
exponents. Mere rescheduling of the present constant number of wide swaps has
now been checked and does not provide the desired exponent jump.

## Reproducibility and scope

Run `python3 scripts/audit_packed_movement.py` for the finite layout counts.
`tests/test_packed_audit.py` checks them against an independent finite-state
optimization, checks failure of generic conjugation cancellation, and compares
exact recurrence unrolling with direct recursion on rational test instances.
These tests support the written audit; they do not prove the upstream machine
bounds or establish an impossibility result for alternative implementations.
