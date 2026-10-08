# First cancellation circuits: scalar savings defeated by path rank costs

**No new kappa.** The simplest cancellation circuit computes the correct
side map and restores arbitrary scratch. At h=50 it would reduce the side
role count from 509,194 to 137,150. However, with the retained data-copy and
injection frames it cannot have a positive rank deficit. The obstruction
allows arbitrary rational matrices at its internal gates, not just the old
source-span labels.

A second prefix/suffix construction removes explicit self-corrections and
uses 234,900 side roles, but also fails a nonorthogonal-path rank bound.
These are scoped rejections of explicit topologies, not a lower bound on all
cancellation circuits. The published conditional
kappa=2^-59 witness remains unchanged. Code and exact controls are in
[audit_cancellation.py](../../scripts/audit_cancellation.py) and
[cancellation-audit.json](../../certificates/cancellation-audit.json).

## 1. Use the correct scalar field

The bit network's scalar gates operate over F2, although its frame matrices
are rational. These two fields must not be confused.

Index inputs and outputs by triples of [h]. Let A1 be the matrix whose
entries are one exactly when the two triples intersect in one point. If
B1(S,T)=|S intersect T|, then over F2,

    A1 = B1 + I.

For off-diagonal intersections 0,1,2 this has the desired values. On the
diagonal, 3+1=0 in F2. The integer identity involving pair-incidence terms
reduces to this formula; charging a coefficient -2 as a nonzero bit-network
operation would be incorrect.

Define point aggregates and outputs by

    G_i = XOR_(S contains i) x_S,
    z_T = XOR_(i in T) G_i XOR x_T.

Each point aggregate is computed with its own balanced binary reduction
tree. Then each output uses two additions to combine its three point values
and a final addition of its own input. This fixed topology deliberately
retains cancelled paths rather than deleting them from the frame audit.

With v=C(h,3), the point reductions use

    h (C(h-1,2)-1) = 3v-h

additions. The output calculations use 3v, for c=6v-h additions in total.
The existing reversible gather/fanout embedding uses c+v=7v-h side roles.
At h=50:

    v=19600, c=117550, R_side=137150.

This is approximately 3.71 times fewer side roles than the published circuit.
It is only a scalar-circuit comparison, not a multiplication improvement.

## 2. Arbitrary scratch restoration still works

The old reversible circuit compiler can be generalized to additions with
overlapping supports: its scalar invertibility does not require disjoint
supports. The source-span frame proof does require more, and is not reused.

Track each node's actual coefficient support by XOR and its graph-reachable
input set by union. Every output z_T has coefficient zero on x_T, but x_T
is reachable through the final private input edge. This distinction is the
key to the failed frame transfer.

Let L be the reversible mixer, V the input copy, and J the output injection.
The audited schedule

    L, J, inverse L, R, V, G, R, L, J, inverse L, G, V

still produces side contribution JLVx and restores all initial scratch.
Here G,R are the retained central point gather/scatter operations. Since
JLV=A1 and RG=B1, the full invocation is y <- y+x. The three-stage schedule
still exchanges the banks and restores the shared auxiliary banks.

Exact small input-basis checks include every dirty scratch input, in both
forward and reverse invocations. A complete small three-stage check includes
the first/third-stage auxiliary sharing. Thus scalar correctness is not the
reason this candidate fails.

## 3. A rank-excess bound for a private diagonal path

For any rational edge matrices M_tail,M_head,

    rank(M_head-M_tail) >= rank(M_head)-rank(M_tail).

The sum of the quantities on the right telescopes over the network because
all incidences at a scalar gate share one frame matrix. With the original
source and sink matrices, this signed rank sum is Wm-2N: sources contribute
N and sinks Wm-N. Call the difference between an edge's rank charge and its
signed rank change its excess. Every edge has nonnegative excess.

For a nondegenerate triple line t in F=Q^h with form I-J/9, let P_t be its
rational projection. At the first stage, the retained data-copy frame is
P_t and the late target-injection frame is I-P_t, within the active factor.
Their ranks are 1 and h-1, while

    rank((I-P_t)-P_t) = rank(I-2P_t) = h.

The last equality follows because P_t is a projection: I-2P_t acts as -1
on the line and +1 on its complement. On any edge path between these two
frames, rank subadditivity therefore gives total charge at least h. Its
signed rank change is h-2, so its total excess is at least **two**.

No condition on the intermediate rational matrices is used. They may be
nonsymmetric, nonnested, or not projections. The future tensor factor at
stage one is a nondegenerate line, so tensoring with its projection leaves
these ranks unchanged. At later forward stages, the common B component
cancels in the difference and the same excess calculation applies.

## 4. The explicit circuit contains enough disjoint paths to kill its saving

For every T, the middle forward mixer has a path

    copy of x_T -> input fanout -> final private XOR for z_T -> injection into y_T.

The first and last edges are unique to T. The direct x_T input to the final
XOR also has its own physical role. These paths are edge-disjoint, even
though other inputs to the output calculations come from shared point sums.
Changing a pivot role does not remove the graph path: all incidences at its
gate must still have the same matrix.

There are v paths in each invocation and v^2 invocations in the first stage,
so already that stage contains N=v^3 edge-disjoint paths with excess at
least two each. Hence

    s >= (Wm-2N) + 2N = Wm.

Strict contraction requires s<Wm. The candidate fails even if every other
edge is credited only its signed rank change. Charging the retained negative
source edges and central returns makes the result worse. Consequently the
smaller denominator W cannot rescue the construction.

This argument retains the canonical copy/injection frames and the stated
scalar topology. Changing those data-stage frames or routing cancelled
contributions through a different shared topology is outside the rejection.
In particular, graph reachability alone is not enough to sum penalties:
edge-disjointness is essential. A common edge must not be charged repeatedly
for several diagonal paths.

## 5. A second natural formula hits the same problem

For the local pair-exclusion problem, let S be the sum of all pair inputs
and S_c the sum of inputs incident to point c. Over F2 the desired sum
avoiding c,d is

    S + S_c + S_d + x_cd.

The formula is exact, but its final private x_cd term again creates a path
from a triple input to that same triple's output. Using this construction
for all common-point circuits therefore does not avoid the obstruction.
For the stage-one bound, one can select a single such path per physical
target triple; their source-copy edges, local direct edges and output-injection
edges remain distinct. There is no need to count all three common points.

### A budget for partial replacement

Suppose only r targets per invocation use such edge-disjoint private paths,
and retain the original central returns, negative-source convention, and
both forward stages. Those two stages alone add at least 4v^2 r to the rank
charge. The remaining deficit is at most

    D_new <= D_old - 4v^2 r,
    D_old = N-6v^2 h^2.

At h=50, positive deficit requires r<1150, hence at most 1149 targets out of
19600. This is a necessary budget under the stated assumptions, not a proof
that any such partial replacement is beneficial or feasible. Extra losses
from the reversed stage and other transitions have been omitted in its favor.

## 6. Removing self terms: an Euler-ordered leave-one-out circuit

For each point i and each triple T containing it, compute

    H_(i,T) = XOR_(S contains i, S != T) x_S,
    z_T = XOR_(i in T) H_(i,T).

The diagonal is absent in each local sum. Distinct triples intersecting in
one point contribute once, and those intersecting in two contribute twice
and cancel. Thus this is another exact implementation of A1 over F2.

For a fixed common point there are q=C(h-1,2) inputs. Compute all sums
excluding one input with prefixes and suffixes. With inputs x_0,...,x_(q-1),
form prefixes through position q-2 and suffixes back through position 1.
The two end outputs use a suffix or prefix directly; each interior output
adds the prefix ending just before it and the suffix starting just after it.
This requires 3q-6 additions and q outputs, or 4q-6 reversible side roles.
Over all h common points the counts are

    additions = 9v-6h,
    side roles = 12v-6h.

The three contributions to each global target are injected separately. At
h=50 this gives 176,100 additions and 234,900 roles, approximately 2.17 times
fewer roles than the published circuit. This is a scalar count, not a valid
rank-saving witness.

### Nonorthogonal endpoints also cost two excess units

For distinct triple indicators u,t, write c=<u,t>=|U intersect T|-1.
Both have squared norm two. When c is nonzero,

    rank(I-P_t-P_u) = h.

Indeed, any kernel vector must lie in span(u,t). On that span, the operator
sends alpha*u+beta*t to -(c/2)(beta*u+alpha*t), an invertible map. Its
endpoint signed rank change is still (h-1)-1=h-2. Consequently every path
from the retained copy frame for U to the injection frame for T has excess
at least two whenever the labels are nonorthogonal. This includes distinct
triples intersecting in two points, even without a diagonal path.

### An explicit disjoint path packing

Take even h>=6. Within each common-point module, order the pairs of the
remaining h-1 points by an Euler circuit in K_(h-1). Such a circuit exists
because every vertex has even degree. Consecutive pairs, including the last
and first, share one point. After adjoining the common point, consecutive
triples intersect in two points and hence have nonorthogonal labels.

The prefix/suffix circuit contains edge-disjoint paths implementing the
cyclic assignment of source position k to target position k+1 modulo q:

- For k<q-1, use the input edge into prefix k, then the branch to output k+1.
  At the ends, an aliased input or prefix removes the unnecessary gate.
- From the last input to output zero, use the suffix chain.

The prefix paths have distinct input and output branches. The closing
suffix path uses none of their edges. This establishes disjointness within
each module, but global input-copy and output-injection edges can be shared
between the three common-point modules.

To handle that sharing, view the local cyclic assignments as a bipartite
multigraph on global source and target triples. Each source and target has
degree three. It therefore has a perfect matching: for any source set A,
its 3|A| incident edges end in a neighbor set of total degree at most
3|neighbors(A)|, proving Hall's condition. Select only the matched paths.
Now each global copy edge and injection edge is used once, and all local
paths were already edge-disjoint. There are v disjoint nonorthogonal paths
per invocation, and N over the first stage. The same bound follows:

    s >= (Wm-2N)+2N = Wm.

This rejects the explicit Euler-ordered prefix/suffix topology with retained
copy/injection frames, allowing arbitrary internal rational matrices. It
does not reject every ordering or implementation of leave-one-out sums.
Removing explicit self-corrections alone is insufficient.

## 7. Research consequence

Neither explicit circuit is a useful target for internal frame optimization:
the path bounds already permit arbitrary internal matrices and rule them
out under the retained data frames.

The next cancellation attempt should first screen edge-disjoint paths
between **any nonorthogonal source and target labels**, not only diagonal
paths. A viable candidate must reduce that path packing or change the
data-stage frames themselves. Passing the screen is necessary, not
sufficient: scalar correctness, scratch restoration, physical role count,
and the complete edge-rank sum must still be checked.

Shared corrections may help if they actually reduce the edge-disjoint path
packing. Mere sharing of algebraic expressions, or cancellation of final
coefficients, does not establish this. Conversely, reachability alone does
not prove rejection: shared edges cannot be charged repeatedly.

## Verification

Run `python3 scripts/audit_cancellation.py` and
`python3 -m unittest discover -s tests -p test_cancellation.py -v`, or
`make verify`. Ten tests cover small scalar maps, physical private edges,
arbitrary dirty inputs and the shared three-stage network for the first
candidate, exact rational projection ranks, arbitrary intermediate-matrix
controls, the local formula, and the h=50 count and loss budgets. They also
check the leave-one-out map, Euler orders, perfect matching and disjoint
paths at h=6,8,10, and distinct nonorthogonal endpoint ranks. The general
rejections follow from the written rank and matching arguments, not the
finite tests alone. Published certificates and patches are unchanged.
