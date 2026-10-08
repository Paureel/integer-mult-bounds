# Recursive gathering: a working schedule and a boundary on this approach

**Follow-up:** the [bounded coded-carry attempt](coded-carry-audit.md) constructs
an exact coded operation, but its cost remains linear. A scoped flat-circuit
bound supports pausing this direction and returning to finite networks.

**The published conditional result remains kappa=2^-59.** This round builds
an exact reversible gatherer from existing chunk swaps, then proves why
changing only that kind of schedule cannot meet the short-guard target.
An optimistic screen of sharing the resulting layout across many rounds
still has a quadratic loss. These are scoped results about constructions
and cost estimates, not a lower bound on all tape algorithms.

This follows the [short-guard reduction](short-guard-audit.md). Code and exact
controls are in [audit_gather_schedules.py](../../scripts/audit_gather_schedules.py)
and [gather-schedule-audit.json](../../certificates/gather-schedule-audit.json).

## 1. A complete recursive gatherer

Use the earlier three-slot reduction. In a slot of length fK, take n=f-1
windows of g bits starting at rho+jK, 0<=j<n, and assume K>=2g. This holds
eventually for the proposed logarithmic g and power-growing K. Label every
address coordinate by its original position. A gathering operation must move
those coordinates physically; the labels in the simulator are not a free
runtime representation of a reordered array.

We may allow arbitrary spectator order inside the gathered layout, provided
we know the permutation and undo it exactly. The compact gadget leaves every
spectator bit unchanged, so this relaxation preserves the complete contract.

First gather to the low end of the nK-bit interval starting at rho. Recursively
divide its n periods into left and right groups of sizes ceil(n/2), floor(n/2).
After processing each child, the low-to-high order has the form

    A_left, G_left, A_right, G_right.

The A fields are packed active windows, with their original order preserved.
There is room at the start of G_left for the whole A_right field, since

    ceil(n/2) (K-g) >= floor(n/2) g.

Exchange those two equal contiguous fields with one arbitrary-gap chunk
swap. This produces a packed A_left,A_right prefix; the remaining fields
are spectators whose internal order need not be stable. Repeat up the tree.
Finally exchange the entire ng-bit active block with the slot's most
significant ng-bit field. They are disjoint because

    2ng <= nK <= fK-rho.

There are exactly n swaps: n-1 merges and one final exchange. Reversing them
restores every coordinate, including all arbitrary guards. The simulator
also inserts the compact arithmetic between gathering and restoration and
checks the full selected-bit XOR, with dirty auxiliary data.

### Cost including all levels

For n=2^J, the sum of the existing width charges u^tau is

    g^tau [n^tau + (n/2) sum_(j=0)^(J-1) 2^[j(tau-1)]].

For each fixed 0<tau<1 this is O_tau(n g^tau). General n has the same bound:
at depth j there are at most 2^j nodes, each of size at most ceil(n/2^j);
summing their width charges is a geometric series dominated by its last
levels. This argument bounds the actual uneven tree; it does not pad the
address space to a larger power of two.

Each swap uses the existing arbitrary-width interface with full volume V,
including spectators. Descriptors and the schedule are polynomial in p;
their preparation is absorbed by the retained superpolynomial record width.
The inverse has the same cost. Consequently this construction costs

    O_tau(V n g^tau),

up to the harmless setup costs already covered by that regime. Constants
can be very large as tau approaches one, but remain fixed with input size.
The construction is correct, yet still linear in the number of windows.

## 2. Any serial interval-swap schedule needs linearly many calls

Color the active address coordinates A and all others G. On the cyclic
coordinate list let B be the number of adjacent unequal colors. Initially
there are n separated active windows and B=2n. After gathering all active
coordinates into one field, B=2. These counts do not depend on the order of
individual active or spectator coordinates inside their fields.

Exchanging two contiguous intervals leaves their interiors and the other
pieces intact. Only the four cut boundaries can change, so one exchange
reduces B by at most four. Therefore every such schedule needs at least

    ceil((n-1)/2)

calls. This allows arbitrary interval widths, locations and intermediate
layouts; it is not restricted to the merge tree. Reversing a coordinate
interval changes at most two boundaries. Moving a single coordinate while
preserving the intervening order also changes at most four. Including these
operations in the schedule does not remove the linear call-count bound.

In the serial black-box model, each of these calls performs complete-array
passes costing at least a constant times V. Thus it cannot supply a strictly
sublinear-in-n gather bound, even when g=O(log p). For a family with n a
positive power of p, the gap between n and n^r for fixed r<1 cannot be
absorbed by a fixed polylog(p) factor.

**Scope:** a fixed sequence of physical coordinate permutations on the same
complete array, charged as separate black-box calls. This excludes intermediate
coded streams, modular arithmetic shears, volume splitting across wire roles,
and an implementation that fuses several calls into a different tape
algorithm. It does not assert that every tape step removes only four
boundaries. Nor does it imply that the upstream chunk-swap theorem is false:
that theorem's internal coded computation is outside this model.

## 3. A stronger bound for the width charges of equal-interval swaps

For schedules made solely of equal-interval exchanges, one can also show
that their summed charges u^tau are Omega_tau((n-1)g^tau), matching the
construction's order for n>=2. This is a bound on the stated width-charge
model, not a matching lower bound on the runtime of arbitrary implementations
of the chunk-swap interface.

Let H_t count pairs of different colors at cyclic distance t. For t<=g,
the initial windows and intervening gaps all have length at least t, so

    H_t(initial)=2nt, H_t(final)=2t.

For J=floor(log2 g), define

    P = sum_(j=0)^J 2^[j(tau-1)] H_(2^j),
    q = 2^tau, 1<q<2.

The required decrease is exactly

    2(n-1) sum_(j=0)^J q^j >= 2(n-1)(g/2)^tau.

An exchange of two u-bit intervals changes H_t by at most 4u: only 2u
positions change color, and each participates in two distance-t pairs.
Independently, cutting the cyclic list into its four exchanged/unchanged
pieces preserves all within-piece pair counts. At most 4t pairs cross the
cuts in either layout, and the number of those pairs is the same in both
layouts. This gives a bound of 4t as well. The looser bound

    |change in H_t| <= 8 min(u,t)

suffices. Summing it over the dyadic scales and splitting at floor(log2 u)
yields

    |change in P| <= C_tau u^tau,
    C_tau = 8 [q/(q-1) + 1/(1-q/2)].

Telescoping over any schedule proves

    sum u^tau >= [2^(1-tau)/C_tau] (n-1) g^tau.

This proof allows temporary fragmentation and arbitrary spectator order.
Its constant depends on tau. Exact finite controls use rational q such as
3/2; they support the combinatorial argument without pretending that those
values approximate the present very small saving 1-tau.

The weighted statement does not include every possible single-digit move or
other elementary streaming operation. The simpler boundary-count result
above has the broader stated scope. Neither result excludes coded gathering.

## 4. Sharing this layout across rounds still has quadratic accounting

Could we pay the gathering cost once and keep the layout for many transform
rounds? Give that proposal the most favorable interpretation: gather windows
of width w=d^b, use all w positions in w consecutive rounds, and restore the
layout only once. Ignore incomplete batches and all other overheads. The
recordwise twiddles can use a tracked coordinate permutation; the necessary
physical layout changes are still charged.

The preceding gather estimate is O(V d w^tau), while the existing compact
layer has root overhead O(V (dw)^tau) per round. The amortized normalized
cost estimates are therefore

    movement per round: d w^(tau-1) = d^[1-(1-tau)b],
    compact root per round: (dw)^tau = d^[tau(1+b)].

Put a=1-tau. Ignoring the complex recurrence and all other constraints in
the candidate's favor, the power saving available from these estimates is

    min(a b, a-tau b).

Its maximum over b>=0 is **a^2**, reached at b=a: the first term increases,
the second decreases, and a+tau=1. Thus reusing this ordinary block-swap
gatherer cannot remove the quadratic loss in the certified bound. With the
retained assembly epsilon<1/5, it offers at most kappa<a^2/5 before the
remaining constraints. At the current certified a=296/10^11 this is
1.75232e-18, still in the present regime.

This is an optimistic screen of these available estimates, not an assertion
that every algorithm retaining a layout has this cost. A faster gatherer,
a cheaper joint multi-round operation, or another way to charge movement
could change the conclusion. For logarithmic windows alone, b=0 in power
accounting, so sharing only O(log p) rounds supplies no fixed power saving.

## 5. The first strided-affine shortcut has dense carries

We also checked a concrete candidate beyond interval rearrangements. Let
x_j,y_j be complete g-bit values in separated windows, with at least one gap
bit between windows, and with the entire control slot preceding the target
slot. The desired operation is

    y_j <- y_j+x_j modulo Q, Q=2^g,

preserving every gap bit. A single ordered-affine call can instead add
sum_j x_j 2^(jK) to the full target slot modulo its whole range. Its control
mask is computable from the earlier slot, so the existing interface gives
linear tape cost for that whole-slot operation.

However, it is the wrong permutation whenever a short-field sum overflows:
the carry changes a gap bit that the desired operation preserves. At the
first overflowing window, no lower window has leaked a carry, so at least
one of that window's gap bits definitely changes, even if further carries
continue beyond it. Conversely, if no window overflows, the maps agree.

For one window, exactly Q(Q-1)/2 of the Q^2 pairs satisfy x+y>=Q. With n
independent complete windows, the fraction of addresses where the maps
differ is therefore exactly

    1 - ((Q+1)/(2Q))^n.

This fraction is independent of the positive gap width and of its arbitrary
initial contents. For g=6 it is already 63/128 for one window, and exceeds
0.9999 for sixteen windows. Increasing the distance between windows does not
make this exception rare. The old exceptional-set sorting estimate therefore
does not give a negligible correction for this replacement.

This distinction matters: the eight-rotation gadget moves a guarded integer
by bounded unit steps, whereas a full short-field addition can cross its
g-bit boundary on about half the inputs. Its changed gap bits cannot simply
be assigned the old small bad-set probability. A different correction or
joint cancellation of carries remains possible, but must be constructed.

## 6. What the next construction must change

Ordinary rearrangements of intact windows are now a poor search target.
The next candidate should use coded intermediate role streams or directly
operate on strided windows with arithmetic transformations. It must avoid
performing a separately charged complete-array operation for each window.

There is a useful distinction in the upstream transfer to keep explicit.
Its matrix-shear factorization already extends to interleaved **contiguous**
H and D fields: order each group by physical position, apply the same lower
triangular factors, and implement each pivot addition freely when its control
precedes its target, or with one interchange otherwise. Every spectator
interval is still allowed. This uses at most rank(A) interchanges and O(V)
additional work for fixed dimension m. Merely interleaving a fixed number of
contiguous fields therefore does not require a new matrix factorization.

The missing extension is different: a recursively shrinking coordinate would
contain a growing collection of disjoint windows. A lower triangular update
on those virtual coordinates is not an ordered-affine update on one physical
contiguous target field. Its tape cost must be proved. Calling that update
free would put the unproved gatherer back inside the proposed construction.

The next bounded experiment should consequently allow a strided affine
operation to change gap bits temporarily and ask whether a coded composition
can restore them at completion. The full state of those bits must be included
in every frame identity; the dense carry calculation rules out treating them
as rare exceptions at each step. Test that exact identity before searching a
large network family. Score a full recursive
invocation with its rows, edge implementations and restoration. A finite
identity or a lower edge-rank count alone will not close the movement gap.

## Verification

`python3 scripts/audit_gather_schedules.py` regenerates the scoped certificate.
`python3 -m unittest discover -s tests -p test_gather_schedules.py -v` runs eight
tests: complete gather/inverse schedules, insertion of exact compact arithmetic,
exhaustive small swap/lag bounds, reversals and single-coordinate moves,
multiscale potential controls, exact dyadic tree costs, and rational round-reuse
optimization, and exhaustive small counts of the dense carry failure. They
also run under `make verify`. No published certificate,
upstream source or multiplication patch is changed.
