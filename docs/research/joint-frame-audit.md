# Joint rational frames with fixed invocation boundaries

**No new kappa.** This pass extends the earlier complex central-frame audit
to the rational bit network and permits joint changes to every internal
active-factor frame, including copy, injection and side gates. For h>=10,
the existing paired invocation already minimizes the full rank sum under
the fixed boundaries and central gate grouping described below.

This is a local optimality theorem, not a lower bound for the general
upstream transfer contract. Changing invocation boundaries, central gate
grouping, role count, or the tensor-stage construction remains outside it.
The published conditional kappa=2^-59 certificate is unchanged.

Exact controls and a complete small physical-edge model are in
[audit_joint_frames.py](../../scripts/audit_joint_frames.py), with output in
[joint-frame-audit.json](../../certificates/joint-frame-audit.json).

## 1. The region and its boundary contract

Let F=Q^h, h>=10, with form H=I-J/9, and v=C(h,3). For each triple T,
let t_T be its indicator and P_T its orthogonal projection for H. These
are rational matrices, generally not symmetric in Euclidean coordinates.
Their explicit entries are

    P_T[i,j] = 1_(i in T) (3*1_(j in T)-1)/6.

The scalar computation is over F2; all ranks below are over Q.

Consider the active h-dimensional factor of a forward invocation with R
side roles and h central roles. Retain these external frames:

| Physical role | Incoming frame | Outgoing frame |
| --- | --- | --- |
| X_T | P_T | I |
| Y_T | 0 | I-P_T |
| Each side role | 0 | I |
| Each central role | 0 | I |

All internal gate matrices may be arbitrary rational h by h matrices.
They need not be projections, self-adjoint, nested, or invertible. The
same matrix must still be used on all incidences of each scalar gate.

Retain the four grouped central gates, in chronological order D,A,C,B:

- D and C act on the physical Y bank and all central roles.
- A and B act on the physical X bank and all central roles.

The original matrices are D=0, A=I, C=0, B=I. Side computation and copy or
injection gates occur between these gates according to the published
schedule. The proof allows their matrices to change jointly too.

These are invocation cuts, not the terminals of the complete bit network.
In particular, the negative initial X frame -P_U is outside this region.
At the first tensor stage the active-factor model applies directly. At later
stages this audit retains the existing common tensor summands and future
line factor; it varies only the active-factor matrices. It does not allow
cross-factor matrices to redistribute costs among those summands.

## 2. Account for whole physical paths

Every side role has a physical path from 0 to I. Rank subadditivity gives
charge at least h on that role, even when its scalar value is mixed with
other roles. Different physical roles have different wire edges. Thus all
side edges together cost at least Rh. The published nested frames attain
this bound exactly. Internal side relabeling cannot finance a central
improvement by reducing that contribution below Rh.

Eliminate the intermediate copy and injection matrices using triangle
inequalities along the data wires. This leaves the lower-bound paths

    X_T: P_T -> A -> B -> I,
    Y_T: 0 -> D -> C -> I-P_T.

Each central role follows

    0 -> D -> A -> C -> B -> I.

Now eliminate B and D from a further lower bound. The data-and-center charge
S satisfies

    S >= sum_T [rank(A-P_T) + rank(I-A)]
       + sum_T [rank(C) + rank(I-P_T-C)]
       + h [rank(A) + rank(A-C) + rank(I-C)].             (1)

No changed edge is free: discarded path segments are bounded through their
endpoints, and the side-role floor is charged separately. With the original
frames, the data-and-center contribution is

    S0 = 2v(h-1) + 3h^2.

The entire original active-factor invocation therefore has rank sum

    Rh + 2v(h-1) + 3h^2.                                (2)

## 3. Rank density for arbitrary rational matrices

For any rational h by h matrix Q of rank k, we claim

    sum_T rank(Q-P_T) >= v(k-1) + 2(v/h)(h-k).           (3)

The rational triple indicators span F: differences of triples give
coordinate differences, and a triple has nonzero coordinate sum. Choose a
basis of h triple indicators and average its coordinate permutations.
Transitivity makes each triple appear with probability h/v. A subspace of
dimension k contains at most k vectors from each basis. Therefore at least
(v/h)(h-k) triple indicators lie outside any k-dimensional subspace.

Write P_T=t_T phi_T, where phi_T=t_T^T H/2. The covectors phi_T form the
invertible image of the triple family because H is nonsingular for h!=9.
They obey the same subspace-density bound in the dual space.

For a rank-k matrix Q and a nonzero rank-one update u phi, put

    alpha = 1_(u outside column(Q)),
    beta  = 1_(phi outside row(Q)).

Then

    rank(Q-u phi) >= k-1+alpha+beta.

The usual rank-one bound proves the case alpha=beta=0. If only one escape
holds, restricting to ker(phi), or applying the transposed argument, gives
rank at least k. If both hold, reduce Q to an invertible k by k block;
the nonzero off-block column and row of the update produce rank k+1.
This distinction matters: a one-sided escape need not increase rank to k+1.

Apply the column and dual-row density estimates separately and sum this
inequality. This proves (3) without any self-adjointness assumption.

## 4. The original central cost is unavoidable in this model

Define nonnegative quantities

    x = h-rank(A),             y = h-rank(I-C),
    u = rank(A)+rank(I-A)-h,
    w = rank(C)+rank(I-C)-h.

Apply (3) to A and I-C in (1). Also,

    rank(A-C) >= h-rank(I-A)-rank(C).

Substitution gives

    S-S0 >= (v-h)(u+w) + 2(v/h-h)(x+y).                 (4)

For every h>=10, both coefficients are strictly positive. Hence S>=S0.
Together with the side floor Rh, this proves that (2) is a minimum over
**all internal rational active-factor frame assignments** satisfying the
retained boundaries and grouped central schedule.

Equality in (4) forces A=I and C=0. The original uncollapsed data paths
then force B=I and D=0 for equality in their contribution. This does not
assert uniqueness of the side, copy, or injection frames.

At h=50, v=19600 and R=509194:

    side contribution        = 25,459,700,
    data contribution        =  1,920,800,
    central contribution     =      7,500,
    total active-factor rank = 27,388,000.

The central path contributes 3h per role, versus the endpoint floor h;
the unavoidable excess in this model is 2h^2 per invocation. This is exactly
twice the existing decreasing-edge loss h^2. Across 3v^2 invocations it
reproduces L=3v^2 h^2=2,881,200,000,000. The global negative-source charge,
unchanged tensor summands and auxiliary-bank joins are not recomputed as
new free parameters here.

## 5. What this closes and what it leaves open

The rejected experiment is broader than changing four central projections:
it includes arbitrary rational changes at adjacent copy/injection gates and
throughout the side circuit, under the specified boundary contract. Merely
enlarging the internal matrix basis or adding low-rank perturbations cannot
improve this invocation's score.

This does not prohibit reducing R with a different side circuit. It says
that, for a fixed R and the stated structure, the current rank accounting
is already tight. It also does not give a general lower bound on the
upstream finite-shear contract.

The next bounded experiment should change a structural premise:

1. Include a boundary between invocations in the optimization region, so
   the intermediate data and auxiliary frames are variables. Charge both
   neighboring invocations and preserve the overall terminal contract.
2. Split or regroup the central gather/scatter operations so their
   incidences no longer all share one matrix. This is a legal scalar
   refinement, but its new intervening data-wire transitions must be paid.
3. Change the tensor-stage or final role-permutation topology more broadly.

The second option is the smaller implementation experiment. Separating the
gather/scatter into point-indexed gates preserves its scalar operation and
enlarges the frame search. It is not a demonstrated saving: data roles
touch several such gates, so reduced center costs can be overwhelmed by
new data-frame transitions. The first option is the direct continuation of
joint boundary-frame optimization. Neither has been solved in this pass.

## Verification

Run `python3 scripts/audit_joint_frames.py` and
`python3 -m unittest discover -s tests -p test_joint_frames.py -v`, or
`make verify`.

The full physical-edge model at h=6 reproduces rank 1292, including all
side, copy, injection, central and cleanup edges. Its scalar invocation is
checked on every input basis vector, including arbitrary dirty scratch,
in both orientations. The general optimality claim starts at h=10, not h=6.

Exact controls at h=10 cover nonsymmetric, nonprojector rational matrices
and joint changes at all four central gates. Additional tests change copy
and injection frames in the physical graph and check the complete path
lower bound. Finite controls support implementation correctness; the
all-matrix result depends on the written proof (1)-(4).
