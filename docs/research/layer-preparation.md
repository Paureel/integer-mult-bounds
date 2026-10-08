# Preparation for a stronger simultaneous-layer primitive

**Current follow-up:** the [compact-control construction](current-status.md)
supplies a different primitive with zero spacing exponent and explicitly paid
temporary reservations. It supports both targets below and a stronger local
conditional witness. This page and its certificate preserve the earlier
preparation pass; their hypothetical labels refer to what was known then.

The subsequent [sparse/fusion audit](sparse-fusion-audit.md) screens batching,
constructs an exact finite phase tool, and proves a scoped obstruction to
changing only the complex motif's central frames.
The [short-guard reduction](short-guard-audit.md) subsequently reduces the
sparse addition target to gathering logarithmic windows, including explicit
repair costs. A fast gatherer remains the missing theorem.

The published result remains **conditional kappa = 2^-59**. This pass supplies
two reusable estimates for the existing recursion and an exact search of the
original complex-network family. Its **hypothetical** 2^-39 and 2^-34 targets
both require a new selected-bit primitive that we have not constructed.

Dependencies are the pinned manuscript's `05-layers.tex`, the
[stopped-depth proof](../../notes/stopped-guard.tex), and the
[packed-movement audit](../packed-movement-audit.md). The new checker is
[prepare_layers.py](../../scripts/prepare_layers.py), with reproducible output
in [layer-preparation.json](../../certificates/layer-preparation.json).
The published checker, certificates, patches, and theorem are unchanged.
These extensions have not been integrated into a full-manuscript patch.

## 1. A guard for every fixed stopping exponent

Retain a complex motif with m>=3 and 2<=s<m^5. Set

    E = 64(W+m+1)^3, B=s+E.

For any fixed rational 0<beta<1 and zeta>0, define

    C1 = 5-4 beta+zeta,
    C0 = ceil(max(128 m B^2, 18 m B^2 (1+1/zeta))).

Then Delta=ceil(C0 d^C1) bounds the depth and shift charge of an entire
simultaneous layer. Coefficient width remains O(p) whenever epsilon C1<1.
This removes the previous beta>=9/10 restriction by allowing the guard
exponent and constant to depend on beta and zeta.

### Proof

The retained coefficient-depth recurrence is

    A(e)<=s A(e/m)+E at an internal node;
    A(e)<=8e when e<d^beta.

For e<=d, the number j of internal levels satisfies
j<=(1-beta)log_m(d)+1. Therefore s^j<=s d^[5(1-beta)], and

    A(e) <= 8 d^beta s^j + E sum_{i<j}s^i
         <= s(8+E) d^(5-4 beta)
         <= 9 B^2 d^(5-4 beta).

For j=0 the same bound holds because 5-4beta>=beta. The last constant
comparison is checked for each motif. E remains additive, not a branch count.
For d>=1, log(d)<=d^zeta/zeta. Since log(m)>1, the number of base-m pieces is

    (m-1)(1+floor(log_m d)) <= m(1+1/zeta)d^zeta.

Their concatenated depth is at most 9mB^2(1+1/zeta)d^C1. Preprocessing and
outer shifts add at most 18d, as in the published proof. Since C1>1 and
9mB^2(1+1/zeta)+18<=C0, the result follows.

The denominator and magnitude induction is unchanged. Bit routines permute
complete coefficient encodings; the complex motif supplies this arithmetic
recurrence. A rational C1 and beta require only integer power comparisons of
fixed degree for guard ceilings and stopping tests, with setup work polynomial
in log(d), covered by the retained setup estimates.

For zeta=1/100 and epsilon=199/1000:

| beta | C1 | epsilon C1 |
| --- | --- | --- |
| 999/1000 | 507/500 | 100893/500000 |
| 1/5 | 421/100 | 83779/100000 |
| 1/100 | 497/100 | 98903/100000 |

All three widths are sublinear in p. The first row improves a nonlimiting
estimate; it does not improve the published headline.

## 2. Packed recurrence with unequal exponents

Let b=s/W<=m^sigma, 0<=sigma<1, 0<tau<1, and keep K=floor(d^c) fixed
throughout the layer. The existing routine gives

    F(e)<=b F(e/m)+O((eK)^tau+1),
    F(e)=O(e) for e<d^beta.

At level j the internal contribution is at most a constant times

    K^tau e^tau (b/m^tau)^j.

The +1 is absorbed since e/m^j>=1 and K>=1. Summing through the actual
stopping depth gives

    internal total = O(log(2d) d^chi),
    chi = tau+tau c+(1-beta)max(sigma-tau,0).

If sigma<=tau, every summand is bounded by the root value. If sigma>tau,
every summand is bounded by that value times the fixed factor m^(sigma-tau)
and d^[(1-beta)(sigma-tau)]. Equality is covered by the logarithm. Replacing
e by d enlarges the estimates, so every base-m piece is covered.

The leaves contribute O(e^sigma d^[beta(1-sigma)]). Summing the pieces and
including row preprocessing gives

    O((log(2d))^2 [d^chi+d^[sigma+beta(1-sigma)]+1]).

Thus lambda-prime greater than both power exponents supplies the layer
interface. To preserve the intermediate notation, the checker still takes
lambda>max(tau,sigma,chi) and
lambda-prime>max(lambda,sigma+beta(1-sigma)); this is sufficient even when
the first two requirements on lambda are unnecessary.

This replaces the old sufficient bound lambda>tau(1+c/beta), covers both
exponent orderings, and does not change the executed routine or tape model.

### The quadratic obstruction persists

Writing a=1-tau and ac=1-sigma, when sigma>tau we have

    1-chi = beta a+(1-beta)ac-tau c.

If ac<=a, sublinearity still forces c<a/tau. Consequently
g2=epsilon c a remains quadratic in a. The sharper recurrence is reusable
accounting, not the missing sparse-movement construction.

## 3. Optimize the complex motif independently

The original complex family has

    v=C(h,3), m=h^3, N=v^3, I=3v^2,
    zc=C(h-3,3)+3(h-3),
    Wc=2N+I(v zc+h+1), Lc=I h(h+1),
    sc=Wc m-2N+2Lc.

Its positive deficit needs **Lc<N**, not 2Lc<N. The stronger joint condition
was sufficient for both interfaces because the rational bit interface pays
an extra N source ranks. The binary phase interface does not. Its exact
condition reduces to h^2-21h-16>0, hence integer h>=22.

### Construction and interface audit

For triples with intersection size j, the center contributes (j-1)/2.
The side correction for distinct even-intersection neighbors is -(j-1)/2.
Their sum is zero for j=0,1,2 and one for j=3. The original eight-step
dirty-scratch restoration and signed three-stage bank exchange therefore
hold at every such h.

Over F2 a triple line has norm one; neighboring lines are orthogonal because
their intersection is even. Their complements are nondegenerate. Every
nonzero residual in the original table has a norm-one vector: choose a
coordinate outside a triple, outside two triples, or outside the earlier
tensor support, and tensor it with the norm-one factors. These coordinates
exist for h>=22>6. The original nonalternating-space argument supplies
orthonormal residual bases. No step requires even h: this unchanged complex
motif has no stage-sharing matching.

The residual table gives Wc m-2N+2Lc independently of its deficit's sign.
The endpoint phase argument and weight-27 corrections are unchanged.
Imposing Lc<N makes the deficit positive. Thus the complex interface alone
extends to this range under the retained upstream lemmas; the rational bit
interface at the same h is not asserted.

Exact logarithm enclosures give the unique maximum at **h=25** among
22<=h<200. For h>=200, zc and m increase and log(m)>1, so

    ac = -log(1-eta_c)/log(m) < 2/(3 zc m-2).

At h=200 this decreasing upper bound is below the h=25 lower enclosure,
certifying the infinite tail. At h=25:

    m=15625, v=2300, N=12167000000,
    Wc=58645352620000, Lc=10315500000,
    sc=916333630984500000, eta_c=14/3464399375.

The optimum is about 4.184799e-10; the convenient strict rational choice
**ac=418/10^12** is certified, 41.8 times the published ac=10^-11.
Also 2<=sc<m^5, so the generalized guard applies.
At fixed h=50, bookkeeping alone supports ac=169/10^13, a factor 1.69.
Neither factor translates into today's bit-limited headline improvement.

The arities can be separated at the interface boundary. `04-swap.tex`
exposes swaps at arbitrary chunk width L, with exponent tau and fixed tape
count. `05-layers.tex` can call that interface at L=(e/m_c)K using its own
m_c for recursion, row splitting and depth. The bit primitive's internal
arity m_b need not equal m_c; assembly uses their time exponents. A future
combined patch must distinguish m_b=125000 from m_c=15625 throughout.
This pass supplies the interface audit, not that integrated source patch.

## 4. Exact targets for the missing sparse primitive

Suppose a replacement primitive has the same complete contract at cost
O(V f^tau K^theta), up to fixed powers of log(p), equivalently log(d) for
fixed epsilon. An uncontrolled log(V) overhead is not allowed: it need not
be logarithmic in p. The recurrence then gives

    chi(theta)=tau+theta c+(1-beta)max(sigma-tau,0).

This is an implication of a missing hypothesis. The cost must include
descriptors, exceptional repair, arbitrary scratch restoration and fixed
tape count; a finite-circuit count by itself is insufficient.

The certificate records two strictly feasible targets assuming **theta=a**,
with a=296/10^11, epsilon=199/1000, delta=1/10000, zeta=1/100:

| Hypothetical target | Complex saving ac | beta | c | 1-lambda-prime |
| --- | --- | --- | --- | --- |
| 2^-39 | 10^-11, published h=50 | 1/100 | 1/200 | 95/10^13 |
| 2^-34 | 418/10^12, complex family at h=25 | 1/5 | 1/10 | 3/10^10 |

In each row lambda is the midpoint between max(tau,sigma,chi(theta)) and
lambda-prime. Every retained assembly constraint and all seven margins have
strict rational slack. The 2^-39 target shows that broadening beta removes
the previously identified complex-leaf obstruction without changing that
motif. The 2^-34 target uses its newly available headroom. Both rows fail
with the existing primitive: substituting theta=tau gives chi>1.

These are **not new established kappa values**. The theta=a hypothesis is
demanding, and neither the guard proof nor the complex-family search supplies
it. The next priority is a bounded sparse/fused-primitive audit using this
exact contract, rather than further tuning of the present graph.

The example cost is sufficient, not necessary. More generally a candidate
cost O(V f^r K^theta), with 0<r<1, has internal exponent
r+theta c+(1-beta)max(sigma-r,0). A stronger saving in the number of active
positions can compensate for a larger spacing penalty. Future screens should
score this tradeoff, rather than reject every candidate whose theta exceeds a.

## Verification

Run `python3 scripts/prepare_layers.py` and
`python3 -m unittest discover -s tests -p test_layer_preparation.py -v`, or
`make verify` for the full repository. Tests unroll actual stopping depths
and piece counts, cover all three geometric-sum regimes, check complex scalar
intersection cases, and reject the hypothetical targets under existing costs.
Exact all-h comparisons certify the arithmetic family optimum. The written
arguments, rather than finite checks alone, supply the general statements.
