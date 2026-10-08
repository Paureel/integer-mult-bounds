# Bounded audit of sparse movement and phase fusion

The [subsequent complete-block audit](fused-block-audit.md) constructs an
exact three-child parity butterfly and proves a broader cut-rank obstruction
to coordinate-child/pointwise-only recursive fusion.

This follows the [layer preparation](layer-preparation.md). **No new kappa
is established; the published result remains conditional 2^-59.** The pass
rules out several restricted shortcuts, supplies an exact finite phase tool,
and identifies which parts of the current construction must change for a
fusion search to have a chance.

The checker is [audit_sparse_fusion.py](../../scripts/audit_sparse_fusion.py),
with output in [sparse-fusion-audit.json](../../certificates/sparse-fusion-audit.json).
The mathematical statements below concern the stated interfaces and model
classes, not lower bounds on integer multiplication or arbitrary tape routines.

## 1. Batching does not improve the available whole-slot estimate

Let the existing bound for a batch of b active positions be proportional to
V(bK)^tau, where 0<tau<1. Partition f positions into positive batch sizes b_i.
Since b_i<=f and tau-1<0,

    sum b_i^tau = sum b_i b_i^(tau-1) >= sum b_i f^(tau-1) = f^tau.

Thus summing separate calls to this bound cannot improve its exponent over
one whole batch. Restoring layouts less often saves a constant factor when
only the existing constant number of rotations is involved. Moving selected
bits individually instead gives the available O(Vf) bound, which cannot
certify a sublinear simultaneous layer. These are comparisons of the current
certified upper bounds, not lower bounds on actual implementations.

The target budgets are demanding. At the fixed parameters in our hypothetical
2^-39 and 2^-34 rows, keeping the active-position saving a=296/10^11 requires
a spacing exponent theta below approximately 6.1e-9 and 6.4e-9, respectively.
The current theta is nearly one. Alternatively, at theta=1/1000 the necessary
active-position saving is approximately 5e-4 for those same parameters.
These necessary internal-cost conditions do not themselves certify a primitive.
They help reject minor variants before a large search.

## 2. Exact collective identities exist

For a binary direction v, let C_v=a0 I+b0 X_v, where
a0=(1+i)/2, b0=(1-i)/2, and X_v translates addresses by v. In the common
Fourier basis its eigenvalue at x is i^[v dot x]. Hence a product of signed
directional kernels has phase

    q(x)=sum_v epsilon_v [v dot x] mod 4.

Writing x in Boolean coordinates, every such phase has a unique signature

    q(x)=sum_i d_i x_i + 2 sum_{i<j} b_ij x_i x_j mod 4,
    d_i in Z/4, b_ij in F2.

Indeed, Boolean parity expands as sum_i v_i x_i minus twice the pair terms;
higher terms vanish modulo four. This gives an exact, compact equality test.
Our bounded tool exhausts all 512 signatures in dimension three and uses
breadth-first search to minimize the number of C_v or inverse factors.
This scalar count omits the tape costs of implementing the directions.

Two exact examples:

* In dimension three, the product of C_v over all seven nonzero v is the
  identity. At x!=0 exactly four of the seven dot products are one; at x=0
  none is. Consequently the product over the six directions other than u is
  **C_u^-1**. Six directional calls can collapse to one when those operators
  are legally consecutive on the same array.
* In dimension six, M=I+J over F2 is invertible, and its columns have weight
  five and pairwise even overlap. Thus the product of C_v over its six columns
  equals the product over the six coordinate directions. This is a collective
  symmetry, despite M not being a coordinate permutation.

Both are checked as full finite operators, independently of the signature
routine. They demonstrate why a fused primitive can have algebraic room that
an individual-kernel search misses. They do not locate that room in our current
machine algorithm.

## 3. An individual residual already has optimal directional call count

Polarizing q gives the symmetric binary form

    B_q(x,y)=(q(x+y)-q(x)-q(y))/2 mod 2.

A signed C_v factor contributes vv^T to its matrix. Therefore a product of
t such factors has polar rank at most t. A current edge residual of dimension
r has an orthonormal basis V and polar matrix VV^T of rank r. The manuscript
already implements it with r signed directional calls. **No alternative
factorization into these same kernels can use fewer calls on that edge.**
This does not bound a different primitive or fusion across multiple edges.

The same invariant controls a layout shortcut. If conjugating a coordinate
phase on active coordinates S by M preserves that phase, its polar matrix
obeys M P_S M^T=P_S. The image of this matrix is the active subspace, so M
must preserve that subspace. A noncoordinate residual cannot become a
coordinate residual merely by dropping its basis changes. The checker exhausts
GL(3,2) as a finite control; the polar-form argument is dimension-independent.

## 4. Scalar gates constrain legal fusion

Let G be a scalar mixing gate on several roles and D_i their phase operators.
The block operator diag(D_i) commutes with G exactly when

    G_ij != 0 implies D_i=D_j.

This follows by comparing block entries D_i G_ij and G_ij D_j. Thus a common
phase may be moved through a gate; distinct phases on roles that mix generally
may not. A diagonal scalar gate is an exception because it does not mix roles.
The finite checks include both cases.

A common phase can be extracted from all incident roles and moved through a
gate, redistributing its adjacent edge phases. This is a legal way to change
a gate frame. Its score must include both incoming and outgoing edges; the
six-to-one identity is not permission to ignore an intervening mixing gate.

## 5. Even coordinated central-frame changes cannot help in a fixed model

We audited a natural version of this legal redistribution in the original
complex motif at h=25. Keep its side-gate frames and scalar topology fixed,
and change phase frames only on the active h-dimensional tensor factor at
the four central gates. Allow arbitrary quadratic phase frames there, not
only orthogonal projections. Their polar matrices are arbitrary symmetric
binary h by h matrices.

Put v=C(h,3) and c=h+1. At h=25, v=2300 and c=26. Let P_t=t t^T for
the binary indicator t of a triple. In the active factor the four original
central frames, chronologically, have polar matrices

    D=0, A=I, C=0, B=I.

The X path through these gates has boundary matrices P_t and I; its central
path is P_t -> A -> B -> I. The Y path is 0 -> D -> C -> I+P_t.
Each of the c center roles follows 0 -> D -> A -> C -> B -> I.
Every unchanged tensor summand contributes the same rank before and after
the proposed change, so it can be omitted in this comparison.

The current active-factor incident rank is

    S0=2v(h-1)+3ch=112350.

Triangle inequalities eliminate B and D from a lower bound on a replacement:

    S >= sum_t [rank(A+P_t)+rank(A+I)]
       + sum_t [rank(C)+rank(C+I+P_t)]
       + c [rank(A)+rank(A+C)+rank(C+I)].

### Rank density of triple indicators

The binary triple indicators span F2^h: differences of two triples give any
pair of coordinate units, and an odd-weight triple supplies the remaining
dimension. Fix a basis of h triple indicators and average all its coordinate
permutations. Transitivity on triples makes each triple appear with probability
h/v. A subspace of dimension k contains at most k members of every basis.
Consequently at least (v/h)(h-k) triple indicators lie outside that subspace.

For a symmetric matrix Q of rank k, adding t t^T has rank at least k-1;
when t is outside the image of Q, its rank is k+1. Therefore

    sum_t rank(Q+P_t) >= v(k-1)+2(v/h)(h-k).

### Joint lower bound

Write

    x=h-rank(A),                 y=h-rank(I+C),
    u=rank(A)+rank(I+A)-h,       w=rank(C)+rank(I+C)-h.

All four quantities are nonnegative. Also

    rank(A+C) >= h-rank(I+A)-rank(C).

Substituting the density bounds into the preceding incident-rank expression
gives

    S-S0 >= (v-c)(u+w)+2(v/h-c)(x+y).

At h=25, v/h-c=92-26=66>0, so no choice of the two middle central frames can
improve the score. Equality forces A=I and C=0. With those fixed, the X and Y
paths force B=I and D=0 for equality as well. This proves joint optimality of
the original four **polar matrices** in this model. Distinct phases with those
same polar matrices cannot beat the attained rank lower bound either.

The proof applies whenever v/h>c, including the complex-admissible h>=22.
It is stronger than a single-gate coordinate-descent failure. A finite control
checks all 4096 pairs of symmetric 3x3 changes embedded in the active h=25
factor. The least changed score in that restricted screen is 112850, versus
112350 at the original frames. The all-matrix claim comes from the proof,
not from extrapolating that finite search.

This result does **not** cover changing side frames at the same time, mixing
different tensor factors, splitting or regrouping scalar gates, changing the
network topology, or implementing a new tape primitive.

## Decision for the next bounded attempt

Stop separate-call batching, single-residual factor searches, and central-only
frame relabeling. The credible fusion search must change side and central
structure together or change which scalar operations are grouped into gates.
The exact phase tool can score small candidates, but promotion requires a
complete legal gate identity, the all-role endpoints, and a tape implementation
whose dependence on f and K meets the preparation budgets. A scalar identity
or a numerical frame score alone is not enough.

The alternative remains a directly stronger sparse address primitive. The
current audit does not establish that either surviving route will succeed.

## Verification

Run `python3 scripts/audit_sparse_fusion.py` and
`python3 -m unittest discover -s tests -p test_sparse_fusion.py -v`.
Both are included in `make verify`. The phase group, small operator identities,
mixing criterion, finite central-frame screen, and target arithmetic are
machine-checked. General rank and tape-accounting statements depend on the
written proofs and retained upstream interfaces.
