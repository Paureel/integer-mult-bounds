# A complete fused parity-butterfly block and its recursion budget

**Follow-up:** the [short-guard reduction](short-guard-audit.md) isolates a
gathering theorem that would permit cheaper sparse movement. Its compact
arithmetic is costed, but a sufficiently fast gatherer remains unproved.

**The published result remains conditional kappa=2^-59.** This bounded round
constructs and checks an exact basis-change/butterfly/basis-change block with
no explicit outer layout permutation. Its cost is three coordinate-layer
calls, not a new sublinear primitive. A cut-rank argument shows why arbitrary
fusion of coordinate children and pointwise gates alone cannot supply the
required recursive contraction.

This follows [the sparse/fusion audit](sparse-fusion-audit.md). The implementation
is [audit_fused_block.py](../../scripts/audit_fused_block.py); its exact checks
are recorded in [fused-block-audit.json](../../certificates/fused-block-audit.json).
No published witness or source patch is changed.

## 1. Specify the complete operator and physical layout

Take two address slots x and y, each of width fK bits, in a complete
lexicographic array. Their selected positions are rho+jK for 0<=j<f, with
0<=rho<K. Other address coordinates, including all guards and any auxiliary
slots, are spectators. Each address holds a complex coefficient record.

For each j, let v_j flip both selected bits x_j and y_j. The target is

    B = product_j C_(v_j),
    C_v = ((1+i)/2) I + ((1-i)/2) X_v.

It leaves spectator fibers invariant and returns the same physical address
order. It mixes coefficient values only along the stated paired directions.
There is no initialized scratch assumption.

Let M perform y_j <- y_j XOR x_j at every selected position. M is an
involution and maps the coordinate direction e_(x_j) to v_j. Thus this is
exactly the nontrivial sandwich

    B = P_M (product_j C_(e_xj)) P_M^-1.

The usual implementation would physically perform the basis changes. The
construction below replaces those outer changes by additional coordinate
butterflies. It does not presume that their internal implementations are free
of address movement.

## 2. An exact three-call construction

Write H0=(1/2)[[1,1],[1,-1]], and let H0_x and H0_y denote its tensor
products on the f selected x or y positions. Define the address-diagonal phase

    D(x,y) = i^[sum_j (2 y_j-1)x_j].

Then the exact operator identity is

    B = [2(1+i)]^f H0_y D H0_x D H0_y.

Both sides use Gaussian dyadic coefficients. Operators on the right are
applied chronologically from right to left; the sequence is symmetric.

### Derivation for one pair

Let H be the normalized Hadamard matrix and S=diag(1,i). Fourier conjugation
gives C_(x+y)=H_x H_y diag(i^[x XOR y]) H_x H_y. Holding y fixed, the
inner x operation is C_x when y=0 and i C_x^-1 when y=1. The identities

    C = exp(i pi/4) S^-1 H S^-1,
    i C^-1 = exp(i pi/4) S H S

therefore turn the inner operation into exp(i pi/4) D H_x D, where
D=i^[(2y-1)x]. Thus

    C_(x+y)=exp(i pi/4) H_y D H_x D H_y.

Replacing H by sqrt(2) H0 yields the coefficient 2(1+i). Tensoring the
disjoint selected pairs proves the formula for f positions, with all spectator
coordinates unchanged. The normalized-H notation is only a derivation; the
executed formula contains no irrational coefficients.

### What its machine cost actually says

Given an **exact** coordinate-layer subroutine of cost T_H(f,K,V), the block
costs at most three such calls plus O(V) streaming work in the manuscript's
record regime. This is not a claim of O(V f^r K^theta) without a corresponding
bound on T_H. In particular, a previously proved child routine cannot silently
be used with a larger K outside its hypotheses.

The diagonal phase is computed from the address using polynomial-in-p work
per record, absorbed by the retained superpolynomial record length R. It
multiplies each complex coefficient by a fourth root of unity. The scalar
has the form

    [2(1+i)]^f = 2^[f+floor(f/2)] i^[floor(f/2)] (1+i)^[f mod 2].

It therefore needs only a binary shift, a fourth-root phase, and possibly
one Gaussian addition, all at linear record cost with adequate guards.
The local formula contributes O(f) denominator and magnitude guard bits;
guards needed inside the exact child implementations must also be charged.
The three child calls are exact, not three invocations with unaccounted
intermediate truncation.

The implementation checks the sandwich, the direct directional product, and
the fused formula independently on 168 complete basis inputs. Additional
tests use separated positions, nonzero complex payloads and arbitrary
spectator fibers. All arithmetic uses Gaussian integer pairs and explicit
power-of-two denominators.

## 3. The complete recursive budget rules out this shortcut family

Here is a stronger obstruction than observing that this particular formula
uses three calls.

Consider a fixed linear recursive template on W equal-volume role streams,
each with a complete array on e selected binary coordinates. Allow:

* arbitrary address-pointwise linear mixing of roles and diagonal phases;
* children applying a coordinate Hadamard or C layer on at most f selected
  coordinates of one role, with all other coordinates spectators;
* any ordering, legal fusion, signs, and normalization factors.

The intended result is a full coordinate layer on all e coordinates of every
role, possibly followed by a role permutation. The original all-role contract
has exactly this requirement. Free row manipulations in this model must
preserve the selected coordinates; an address permutation cannot be hidden
as a free change of names.

### Cut rank

Fix a selected coordinate t. Partition the coefficient vector according to
whether that bit is zero or one, across all roles and other coordinates.
For an operator A, let r_t(A) be the rank over the complex numbers of its
block from input t=0 to output t=1. For composable square operators,

    (AB)_10 = A_10 B_00 + A_11 B_10,
    r_t(AB) <= r_t(A)+r_t(B).

No invertibility assumption is needed for this inequality.

An address-pointwise gate has r_t=0. A coordinate child not touching t also
has r_t=0. A child touching t on one complete role stream has rank at most
2^(e-1), including when it acts on several selected positions simultaneously.
Extra spectator coordinates multiply every rank by the same factor.

The target full Hadamard layer has

    r_t(target) = W 2^(e-1),

because its off-diagonal t block is a nonzero scalar times an invertible
Hadamard layer on the remaining coordinates and a role permutation. A full
C layer has the same rank, since its off-diagonal coefficient is nonzero and
the remaining tensor factors are invertible.

Normalize ranks by 2^(e-1). Each target coordinate needs W units. Summing
over all e coordinates gives a required budget of We. Each child touches
at most f coordinates and contributes at most f units to that sum. Thus

    S f >= W e, or S >= Wm when e=mf.

This holds for arbitrary choices of the child coordinate subsets, not just
one fixed partition into slots. It allows pointwise mixing between every
pair of calls, so further phase fusion cannot evade the bound.

The rank-saving recursion needs S<Wm. This template class cannot meet that
strict inequality. Supplying an independently faster child oracle would
import the missing ingredient rather than derive it from this recursion.
The argument does not assert that the three-call formula is optimal among
every possible implementation of the two-slot block.

For that block itself, each of its 2f selected coordinates also has full
off-diagonal rank: the corresponding C_(x_j+y_j) term flips that bit and
its partner, while the other factors are invertible. Thus at least two
f-coordinate children are required in this class. Even a two-call improvement
would only reach the noncontracting boundary for a 2f-to-f recursion.

## 4. Scope and consequence for the next search

This is a limitation of the specified recursive linear templates, **not**
a lower bound on general tape algorithms or integer multiplication. In
particular, the original address permutations do cross these coordinate cuts;
they are outside the zero-cost pointwise class. A direct butterfly along a
noncoordinate direction can also cross several cuts in one operation.

Consequently a successful continuation must include a costed operation of
one of those kinds. We should now focus on a stronger packed selected-bit
row addition, or a direct directional butterfly implemented with genuinely
cheaper movement. Replacing movement entirely by coordinate children and
pointwise phases cannot achieve the desired contraction, even with a better
fusion identity than the one constructed here.

The selected-bit row-addition target remains concrete: perform
y_(rho+jK) <- y_(rho+jK) XOR x_(rho+jK) for every j, preserve all other
address bits and arbitrary auxiliary data, return the original layout, and
meet the active-position/spacing budgets in the preparation note. Shorter
guard windows or retained layouts are candidates only if their gathering,
alignment, repair and restoration costs are included. No improved bound for
that primitive is supplied by this pass.

## Verification

Run `python3 scripts/audit_fused_block.py` and
`python3 -m unittest discover -s tests -p test_fused_block.py -v`, or
`make verify`. The finite operator checks and exact cut-rank controls support
the general proofs above; they are not a formal verification of the complete
upstream theorem. The new artifacts leave the published 2^-59 certificate
and all existing source patches unchanged.
