# Conditional two-stage refinement

Aurel Prosz (Paureel), October 8, 2026. Developed in “Improve Integer Mult
Bounds” with ChatGPT, independently reconstructed and audited with Codex.

The latest completed conversational result is supported by this reconstruction:

$$\kappa=629/10^{11}=6.29\times10^{-9}\approx2^{-27.244293}>2^{-28}.$$

It improves the previous `5.91e-10 ≈ 2^-30.656123` exponent saving by
`6290/591 ≈ 10.642978`. These ratios concern the asymptotic exponent,
not a measured runtime improvement. The result is conditional on the retained
multiplication theorem and the written transfer and compact-control arguments.
This additional AI-assisted audit is not independent expert or formal review.

## What was checked and what was reconstructed

The latest completed answer in “Improve Integer Mult Bounds” described
`two-stage-kappa-research.zip`. Its cloud sandbox link did not expose the
archive to this local task. We therefore publish a fresh implementation and
written proof, not a claim to have inspected that package or its 33-test suite.

There is a material reproducibility difference. The bundled paired-bit
generator at `h=32` gives **123157** side roles, rather than the conversation's
**119584**. The conversation's `a_b=4.885e-7` fails the simple deficit test
for our larger graph. We certify the conservative `a_b=4.7e-7` instead.
The same final kappa is still supported because the complex saving controls
the limiting margin. The complex graph's counts match the latest answer.

The latest research message after that answer contains a request for further
improvement but no completed result. It supplies no additional theorem.

## The structural change and its charged correction

Two stages in a two-factor label space use `m=h^2`, replacing `h^3`.
Their scalar map is `(x,y) -> (-y,x+y)`, with arbitrary auxiliaries restored.
Deleting a stage without completing this map would be invalid.

For bit-array address frames, put `P=S_U`, `E=S_(U-perp)`, `F=S_full`.
The two framed stages give `A=Fy`, `B=Fx+Ey`. Since `PF=E`, XORing `PA`
into `B` cancels the unwanted term. A direct partial-swap line is a rational
rank-one reflection. A lower triangular conjugation and one earlier/later
interchange implement it, with all other updates directed forward on tape.
The [new transfer proof](../../notes/direct-swap-transfer.tex) supplies the
general argument, prime choice, complete ranges and fixed-tape schedule.

For complex frames, `P=C_U`, `E=F P^-1`. The outputs are `A=-Fy`,
`B=F P^-2 x+Ey`. Adding `P^-1 A` removes `y`. Pre/post diagonal signs and
a fourth-root scalar remove the remaining `P^-2`; the proof uses the
two-triple indicator's weight **9**, rather than the old weight 27.
The [endpoint proof](../../notes/two-stage-phase-transfer.tex) derives this
identity. It does not treat address translation as a free tape operation.

Both corrections act on a **copy** of `A`. Copying costs sequential work and
temporary tape storage; it preserves the role's logical shape and `V/W`
recursive volume. The original is parked during the child, using the retained
depth-first schedule. No additional routed role or clean address field is
assumed. Transforming and restoring the original with two children would
destroy the positive deficit; the negative-control test verifies this.

For `v=C(h,3)`, `N=v^2`, and `c0=h` or `h+1`,

$$W=2v^2+2v(R+c_0),\quad L=2vhc_0,$$
$$s_{edge}=Wm-2N+2L,\quad s=s_{edge}+N=Wm-N+2L.$$

All initially zero and final full scratch-frame extensions are charged.
The only decreases are the central returns. The
[two-factor proof](../../notes/two-stage-construction.tex) gives the actual
data boundaries, invocation frames, arbitrary-scratch identity and counts.

| Quantity | Reconstructed bit circuit | Complex circuit |
| --- | ---: | ---: |
| h; v; m | 32; 4960; 1024 | 34; 5984; 1156 |
| Side roles R | 123157 | 2379258 |
| W | 1271238080 | 28546995136 |
| Charged s | 1301743508480 | 33000319052800 |
| Positive deficit Wm-s | 4285440 | 7324416 |
| Normalized deficit | 27/8201536 | 9/40549709 |
| Certified 1-tau or 1-sigma | 4.7e-7 | 3.147e-8 |

Positive exponential Taylor sums certify `log(1024)<6.932` and
`log(1156)<7.05273`. The exact inequalities `eta>a log_upper` imply
`s/W<m^(1-a)` via `exp(-x)>1-x`.

## Exact finite evidence

The complex graph uses 272 groups, 768202 additions, and 1611056 outputs,
including **11968** alternating-residual repairs. Its complete matrix has
**35808256** exactly checked coefficients. Both scratch orientations trace
**37793456** incidences. Every nonzero residual is tested for nonalternation.
The bit audit checks all actual disjoint-sum supports, exclusion outputs,
compiled pivot aliases and both span/complement inclusion schedules explicitly.
These acceptance checks survive Python's optimization flag.

Full small two-stage scalar maps check all **7600 bit** and **31010 complex**
independent input variables, including arbitrary auxiliary initial values.
Exact Gaussian rational endpoint checks cover **1108** basis inputs, including
the actual weight-9 correction. Modular address controls cover **13810** cases,
including non-coordinate partial-swap lines and the one-interchange reflection
block over prime powers. These are finite controls accompanying general proofs.

The parameters are

    epsilon=0.199999, c=1, beta=0.0001, delta=1e-8,
    zeta=0.0001, C1=4.9997,
    lambda=1-3.1465e-8, lambda'=1-3.1464e-8.

All **31 strict side conditions** and **seven assembly margins** pass with
the reconstructed bit saving. The minimum is

$$G=6.292768536\times10^{-9},\qquad
G-\kappa=2.768536\times10^{-12}>0.$$

The complex stopped-depth guard checks `2<=s<m^5` using the complete budget.
Its explicit node allowance includes copies, scalar adds, signs and inverse
wrappers. The Gaussian margin is `1.24e-6>0` with its formula unchanged.
The fixed declared-saving supremum is
`a_c/(5+4a_c) ≈ 6.29399984154226e-9 ≈ 2^-27.243376`, so this is a narrow
strict-margin witness. It is not an unrestricted algorithmic ceiling.

The requested `5.91e-7 ≈ 2^-20.690339` target fails this parameter system.
No hypothetical smaller-role graph, different resampling routine or further
thousandfold improvement is included as an achieved result.

## Reproduce and review

- [Implementation and independent checker](../../scripts/two_stage.py)
- [Exact generated certificate](../../certificates/two-stage.json)
- [Standalone pinned-source patch](../../patches/two-stage-28.patch)
- [Patch generator](../../scripts/make_two_stage_patch.py)
- [Structural and negative-control tests](../../tests/test_two_stage.py)

`make verify` includes the new certificate, source patch, tests and applicability
check. The normal and optimized certificate outputs are compared during this
audit. Pinned upstream files and historical certificates remain unchanged.
No build of the complete revised manuscript, full multiplication machine,
proof-assistant verification or independent expert review is claimed.
