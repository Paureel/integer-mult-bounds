# Conditional orthogonal-star improvement

Aurel Prosz (Paureel), October 8, 2026. Developed in “Improve Integer Mult
Bounds” with assistance from OpenAI ChatGPT, then independently reconstructed,
reviewed and integrated with assistance from OpenAI Codex.

The supplied conditional witness is

$$T(n)=O\!\left(n(\log n)^{1-\kappa}\right),\qquad
\kappa=591/10^{12}=5.91\times10^{-10}>2^{-31}.$$

It is approximately **7.12048 times** the inherited compact-control headline
`8.3e-11`, at CrocSwap commit `6e564879f51ae16f23d392e9e196c605f36d90df`.
The millionfold comparison with an older conversational direct-swap witness
does not represent a millionfold original contribution: most of that change
comes from Douglas Colkitt's newer compact-control work. These ratios compare
exponent savings, not measured runtime speedups. No global priority or
unrestricted optimality claim is made.

The new result replaces the complex side network. It retains the bit primitive,
compact-control method, Gaussian setup and assembly interfaces. It does not
depend on the earlier direct-swap proposal or hypothetical resampling algorithm.

## Provenance and deliverables

The research conversation described a package named
`orthogonal-star-kappa-improvement.zip`. That archive was unavailable during
integration. This fork publishes a fresh reconstruction of the described
mathematical construction, with matching counts and independent exact checks;
it does not claim to reproduce or audit that archive's actual files or 48-test suite.

- [Written finite-network proof](../../notes/orthogonal-star-construction.tex).
- [Reconstructed graph, compiler and exact verifier](../../scripts/orthogonal_star.py).
- [Generated certificate](../../certificates/orthogonal-star.json).
- [Independent patch against the original pinned manuscript](../../patches/orthogonal-star-31.patch).
- [Patch generator](../../scripts/make_orthogonal_star_patch.py) and
  [regression tests](../../tests/test_orthogonal_star.py).

The complete original multiplication theorem remains assumed. No proof-assistant
verification or complete multiplication-machine implementation is supplied.
The reconstruction is an additional AI-assisted audit, not independent expert review.

## Fixed-pair grouping and the repaired residual

Partition 25 points into parts of sizes 12 and 13. Assign every triple to its
same-part pair, choosing its two smallest points when it lies entirely in a
part. There are `C(12,2)+C(13,2)=144` groups. Every triple is assigned once.
This number is optimal for pair centers covering all triples: their complement
must be triangle-free, whose 25-vertex edge bound is `floor(25^2/4)=156`.
This establishes only the pair-cover optimum, not the circuit optimum.

For a fixed pair `{i,j}`, source indicators `u_k=e_i+e_j+e_k` satisfy
`u_k · u_l = delta_kl` over the two-element field. Every subset is orthonormal.
For target `S`, its group contributes half the sum of disjoint triples and
minus half the sum of intersection-two triples. Together with the retained
center coefficient `(|S intersection T|-1)/2`, this is exactly the identity.

For a source subset spanning `U` inside `t_S`'s complement, the canonical vector
of its injection residual is `1+t_S+sum(u_k)`. A nonzero residual is alternating
exactly when this vector vanishes; it then has no orthonormal basis. The
unrepaired example with pair `{0,1}`, target `{0,1,2}`, and all 22 outside
third points really fails. Splitting an offending sum into a singleton and
the remaining sum makes both canonical vectors nonzero. All 50 necessary
repairs and their additional output uses are charged.

Build requested sums by recursively bisecting each ordered group, skipping
empty intersections and interning exact supports. Every addition has disjoint
supports. The reversible compiler reuses one incoming pivot for one outgoing
use at each addition and allocates the remaining uses separately. It uses
`additions+outputs` roles and never aliases simultaneous inputs.

| Quantity | Exact value |
| --- | ---: |
| Ground size and triple count | 25; 2300 |
| Fixed-pair groups | 144 |
| Active additions | 160046 |
| Requests before repair | 323940 |
| Repaired partial outputs | 323990 |
| Side roles per invocation | 484036 |
| Scalar coefficients checked | 5290000 |
| Scratch-frame incidences, both orientations | 7738184 |
| Small symbolic input variables, each orientation | 478 |

## Scratch restoration, frames and exact rank budget

With mixer `L`, copy `V`, side injection `J`, center gather `G` and scatter `R`,
the signed transparent schedule cancels the initial contributions `JLz` and
`Rc`, adds `(JLV+RG)x=x`, and restores arbitrary scratch. Exact rational
symbolic maps at `h=7` check all 478 input variables, including arbitrary
scratch, in both directions. The general cancellation identity applies at
every fixed size. The three stages give the original signed exchange `(-Y,X)`.

Forward middle frames use source spans; reverse middle frames use their
orthogonal complements. Early mixers **and early injection** use the common
label `D0=B tensor F`. Cleanup uses `D1=A tensor F`. Assigning a smaller
early target-line frame after a `D0` mixer would create an extra decrease;
the supplied assignment avoids it while preserving data stage boundaries.

Nested source subsets have orthonormal residuals. A node's complement is
nonalternating because no active query or node uses all 23 vectors of a full
star. Output residuals are checked after repair. The original norm-one
witnesses cover data, center, common-component and terminal tensor residuals.
Thus every nonzero edge residual admits the required orthonormal basis.
The phase interface supplies exactly one signed translation kernel per basis
vector, with unchanged endpoint corrections.

No auxiliary bank is shared across stages. Only the `h+1` centers decrease,
each losing `h` dimensions per invocation. With `v=2300`, `N=v^3`, `m=15625`,
and side roles `R_side=484036`,

$$W=2N+3v^2(R_{\rm side}+h+1)=7706397940000,$$
$$L_{\rm loss}=3v^2h(h+1)=10315500000,$$
$$s=Wm-2N+2L_{\rm loss}=120412464109500000.$$

The normalized deficit is `eta=14/455245625`. A 20-term positive exponential
sum proves `log(m)<9.66`, and exact rationals prove
`eta > (3.18e-9)*9.66`. Therefore the complex exponent saving is
`a_c=1-sigma=3.18e-9`. The paired bit saving stays `a_b=2.96e-9`.

## Dependency argument and parameters

The [inherited compact-control review](compact-control-review.md) maps the
general tape claims to their proofs. The replacement supplies the same finite
phase interface, with its own `m,W,s`; none of those general proofs requires
the original unshared complex side graph. Specifically:

1. Compact address rotations only permute complete coefficient encodings.
   Their polynomial offset work is paid by superpolynomial record lengths.
2. Existing-coordinate front/back fields remain complete in every child.
   Whole-row padding and splitting the separate row index give exactly `V/W`
   logical volume, with temporary fields restored before recursive boundaries.
3. Exceptional-address repair is charged at every node. Its `O(p^-3)` density
   is not substituted into the obsolete global `2^-K` estimate.
4. The recurrence's internal exponent is
   `chi=tau+(1-beta)*max(sigma-tau,0)`. The leaf exponent is
   `sigma+beta*(1-sigma)` and reservations cost `d^max(1-c,0)` times logarithms.
5. The actual new scalar-operation count and retained phase wrappers fit the
   fixed node charge `E=64(W+m+1)^3`; `s<m^5`. The generalized guard uses
   `C1=5-4*beta+zeta`, and `epsilon*C1<1` keeps coefficient widths `O(p)`.
6. The seven retained assembly powers consume the completed layer bound.
   All required Gaussian, prime, dimension and spacing conditions stay strict.

Use these exact rational parameters:

    tau = 1-2.96e-9, sigma = 1-3.18e-9,
    epsilon = 0.1999, c = 1,
    beta = 0.001, delta = 1e-6, zeta = 0.0001,
    C1 = 4.9961,
    lambda = 1-2.959e-9, lambda' = 1-2.958e-9,
    kappa = 5.91e-10.

Here `sigma<tau`, so `chi=tau`. All 31 compact-system conditions are positive.
The minimum assembly margin and absorption gap are

$$G=\epsilon(1-\lambda')=5.913042\times10^{-10},$$
$$G-\kappa=3.042\times10^{-13}>0.$$

Keeping the inherited smaller complex saving fails the new layer conditions.
Keeping spacing `c=1/5` fails the final margin. The new headline requires both
the replacement construction and the revised spacing choice.

For fixed declared savings, the scoped strict-inequality supremum is
`min(a_b,a_c)/(5+4*min(a_b,a_c)) = 37/62500000148`.
Indeed `q=1-lambda' < min(a_b,a_c)`, and `g3,g5>kappa` imply
`kappa<q/(5+4q)`. Conversely take `beta,zeta,delta` small, `c=1`,
`q` below that minimum, and approach the balance of `g3` and `g5`; all other
constraints have positive room. The guard approaches `C1=5` and remains
compatible. This proves a supremum within these fixed-saving interfaces,
not optimality for other networks or integer multiplication generally.

## Reproduction and verification boundary

Run `make verify` with Python 3.11 or newer. This regenerates the new certificate
and source patch, rechecks all finite counts and frame incidences, checks the
matrix and symbolic identities, verifies the pinned source hashes, and runs
the full tests and independent patch checks. Certificate generation uses
explicit exceptions rather than assertions, and normal versus `python -O`
generation can be compared byte-for-byte. The manuscript patch incorporates
the written finite proof, retained compact-control arguments and new parameters.

The original `upstream/` files and older certificates/patches remain unchanged.
The inherited compact-control PDF describes its earlier `8.3e-11` result;
the new proof is supplied as source, not as a newly compiled PDF. Exact checks
support finite identities and feasibility. The general tape and analytic
claims remain mathematical proofs and assumptions, not consequences of tests.
