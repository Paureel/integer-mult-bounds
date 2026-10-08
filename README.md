# A sharper exponent for integer multiplication

**Paureel's two-stage research draft, building on Douglas Colkitt's
compact-control construction and OpenAI's original manuscript.**

In the retained finite-alphabet Turing-machine model with a fixed number of
one-dimensional tapes, this fork supplies the conditional witness

$$
T(n)=O\!\left(n(\log n)^{1-\kappa}\right),\qquad
\boxed{\kappa=629/10^{11}=6.29\times10^{-9}\approx2^{-27.244293}>2^{-28}}.
$$

This increases the preceding `5.91e-10 ≈ 2^-30.656123` exponent saving by
about **10.642978 times**. These compare asymptotic exponent savings,
not measured runtime speedups.

**[Read the construction, dependency audit and discrepancy](docs/research/two-stage.md)** ·
[Inspect the exact certificate](certificates/two-stage.json) ·
[Review the complete source patch](patches/two-stage-28.patch)

The latest completed result in “Improve Integer Mult Bounds” replaces three
stages with **two tensor stages plus a charged rank-one endpoint correction**.
The recursive dimension falls from `h^3` to `h^2`. The correction acts on a
copy, includes one child per data pair, and uses diagonal signs for the complex
endpoint. The new direct partial-swap bit transfer is supplied as a written
proof with exact modular controls. Arbitrary auxiliary values are restored.

There is a reproducibility discrepancy: the bundled bit generator gives
**123157 side roles**, versus the conversation's 119584. Its slightly weaker
certified bit saving `1-tau=4.7e-7` still supports the same final kappa.
The reconstructed complex graph matches the claimed counts: **2379258** side
roles at `h=34`, including **11968** repaired alternating residuals.
All **35808256** scalar coefficients and **37793456** scratch-frame incidences
are checked exactly. The bit instance has `h=32`; its recursive dimension
is 1024, independently of the complex instance's 1156.

The complete original multiplication theorem remains an assumption. The
conversation ZIP was unavailable; this fork publishes a fresh reconstruction.
The general frame, reflection, copy, endpoint and tape proofs accompany exact
finite checks. This AI-assisted audit is not independent expert review or
proof-assistant verification. No complete multiplication-machine implementation
or build of the newly revised manuscript is claimed.

All **31 strict side conditions** and **seven assembly margins** pass. The
limiting margin and strict absorption gap are

$$G=6.292768536\times10^{-9},\qquad G-\kappa=2.768536\times10^{-12}>0.$$

The guard charges correction copies and wrappers and verifies `2<=s_c<m_c^5`.
Douglas Colkitt's compact-control reservation, repair, Gaussian setup and
assembly arguments are retained. The requested thousandfold target
`5.91e-7 ≈ 2^-20.690339` is not achieved by this witness.

The [preceding orthogonal-star audit](docs/research/orthogonal-star.md) and
[inherited compact-control review](docs/research/compact-control-review.md)
remain available. The inherited [PDF](artifacts/compact-control-note.pdf)
describes `8.3e-11 ≈ 2^-33.488098`; it is not a PDF of the new result.

## Reproduce

With Python 3.11 or newer, Git and Make, run from the repository root:

```sh
make verify
git diff --exit-code -- certificates patches
```

No third-party Python packages or network access are needed for these checks.
They regenerate the certificates and patches, run the tests, verify upstream
hashes, and check each patch against the pinned manuscript. The second command
checks exact regeneration on a clean checkout.

With Tectonic installed, rebuild the inherited compact-control note using:

```sh
make compact-note
```

The output is `artifacts/compact-control-note.pdf`. The first PDF build may
download TeX resources. See [reproducibility instructions](docs/reproducibility.md)
for applying the combined patch in a disposable copy and building older notes.
[GitHub Actions](.github/workflows/verify.yml) runs the arithmetic and patch checks.
Passing tests does not establish the complete multiplication theorem; this
repository contains no full multiplication-machine implementation.

The earlier Paureel parameter refinement remains available in
[its audit](docs/paired-tuned-parameters.md) and
[certificate](certificates/paired-tuned-parameters.json). It supports
`kappa=1.7523184e-18` within the older paired parameter system.

## Earlier witnesses and independent patches

Each patch applies independently to the **unmodified** pinned source; they are
alternatives, not a sequence to apply together. The
[result history](docs/research/result-history.md) records the earlier mechanisms
and scoped ceilings.

| Patch | Conditional saving | Scope |
| --- | --- | --- |
| [frozen-154](patches/frozen-154.patch) | `4.379058e-47 ≈ 2^-154` | Original network and recurrence exponents |
| [balanced-153](patches/balanced-153.patch) | `8.758115e-47 ≈ 2^-153` | Balanced assembly parameters |
| [same-network-129](patches/same-network-129.patch) | `1.469368e-39 ≈ 2^-129` | Original network, sharper recurrence comparison |
| [h46-111](patches/h46-111.patch) | `3.851860e-34 ≈ 2^-111` | Smaller network, dyadic parameters |
| [h46-109](patches/h46-109.patch) | `1.540744e-33 ≈ 2^-109` | Rational recurrence saving, strict final margin |
| [h46-108](patches/h46-108.patch) | `3.081488e-33 ≈ 2^-108` | Variable stopping exponent |
| [h46-rational](patches/h46-rational.patch) | `5.8e-33 ≈ 2^-107.087574` | Strongest supplied parameter-only witness |
| [nonadjacent-layout](patches/nonadjacent-layout.patch) | Original parameters retained | Routing proof and revised layout cost only |
| [frozen-nonadjacent-107](patches/frozen-nonadjacent-107.patch) | `6.162976e-33 ≈ 2^-107` | Direct routing, original network and recurrence exponents |
| [h46-nonadjacent-78](patches/h46-nonadjacent-78.patch) | `3.308722e-24 ≈ 2^-78` | Direct routing with the h = 46 network |
| [h46-nonadjacent-76](patches/h46-nonadjacent-76.patch) | `1.323489e-23 ≈ 2^-76` | Direct routing with tuned dimension and stopping parameters |
| [h46-shared-side-75](patches/h46-shared-side-75.patch) | `2.646978e-23 ≈ 2^-75` | Stage-1/stage-3 side-role sharing, routing, and parameter tuning |
| [h46-incidence-67](patches/h46-incidence-67.patch) | `6.776264e-21 ≈ 2^-67` | Rectangle incidence circuits, full auxiliary sharing, routing, and parameter tuning |
| [h46-dag-63](patches/h46-dag-63.patch) | `1.084202e-19 ≈ 2^-63` | Shared intermediate sums and reversible role allocation |
| [h46-shared-point](patches/h46-shared-point.patch) | `1.761829e-19 ≈ 13*2^-66 ≈ 2^-62.299560` | Cross-group sharing |
| [h50-paired-59](patches/h50-paired-59.patch) | `1.734723e-18 ≈ 2^-59` | Paired sums, stopped guard and tighter Gaussian setup |
| **[compact-control-34](patches/compact-control-34.patch)** | **`8.3e-11 ≈ 2^-33.488098`** | **Compact controls, complete reservations, local repair and separate complex arity** |
| [h50-paired-tuned](patches/h50-paired-tuned.patch) | `1.7523184e-18 ≈ 2^-58.985441` | Earlier Paureel parameter refinement |
| [orthogonal-star-31](patches/orthogonal-star-31.patch) | `5.91e-10 ≈ 2^-30.656123` | Paureel complex-network replacement with retained compact controls |
| **[two-stage-28](patches/two-stage-28.patch)** | **`6.29e-9 ≈ 2^-27.244293`** | **Two tensor stages, charged copy correction and direct-swap bit transfer** |

## Attribution, citation, and license

The two-stage and orthogonal-star constructions and earlier paired parameter refinement in this fork are by Aurel Prosz (Paureel),
developed with assistance from OpenAI ChatGPT and Codex. The inherited
constructions and compact-control extension are attributed below.

Author: **Douglas Colkitt**. Research, implementation and drafting were performed
with assistance from OpenAI Codex. The compact-control proposal originated
with a separate research agent; the supplied note develops its tape, layout,
repair and assembly arguments. AI assistance is not independent review or
endorsement by OpenAI. No priority or unrestricted optimality claim is made.

The original manuscript is by OpenAI, pinned at commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Source URLs and SHA-256 hashes are in
[upstream/manifest.json](upstream/manifest.json). Files under `upstream/` remain
unchanged; modifications are supplied as separate patches.

Use [CITATION.cff](CITATION.cff) and also cite the
[upstream manuscript](upstream/README.md). Until a release is archived, include
the repository commit used. Licensed under [Apache-2.0](LICENSE); see
[NOTICE](NOTICE) and [CONTRIBUTING.md](CONTRIBUTING.md).
