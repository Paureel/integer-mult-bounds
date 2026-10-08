# A sharper exponent for integer multiplication

**Paureel's orthogonal-star research draft, building on Douglas Colkitt's
compact-control construction and OpenAI's original manuscript.**

In the retained fixed finite-alphabet Turing-machine model with a fixed number
of one-dimensional tapes, this fork supplies the conditional witness

$$
T(n)=O\!\left(n(\log n)^{1-\kappa}\right),\qquad
\boxed{\kappa=591/10^{12}=5.91\times10^{-10}>2^{-31}}.
$$

This is about **7.12048 times** the inherited `8.3e-11` compact-control result,
at CrocSwap commit `6e564879f51ae16f23d392e9e196c605f36d90df`. Most of the much
larger jump from older conversational witnesses comes from that inherited work.
These compare exponent savings, not practical runtime speedups.

**[Read the new construction, dependency audit and scope](docs/research/orthogonal-star.md)** ·
[Inspect the exact certificate](certificates/orthogonal-star.json) ·
[Review the combined source patch](patches/orthogonal-star-31.patch) ·
[Read the finite-network proof source](notes/orthogonal-star-construction.tex)

The complete original multiplication theorem remains an assumption. This is
an AI-assisted mathematical reconstruction with exact finite verification and
written general proof dependencies; it has not received independent expert
review or proof-assistant verification. The original research conversation's
ZIP was unavailable during integration. The fork publishes the independently
reconstructed implementation, whose counts and identities were checked here.

## What changed

The new complex network partitions source triples on 25 points into **144
fixed-pair groups**. Their indicator vectors are orthonormal over the
two-element field, allowing intermediate sums to be shared while preserving
valid phase-frame residuals. **50 alternating residuals** require explicit
repairs; their costs are included.

The graph has **160046 additions**, **323990 outputs**, and **484036 side roles**
per invocation. Its reversible schedule restores arbitrary initial scratch.
Forward source-span frames and reverse complement frames introduce no extra
side decreases. All **5290000 scalar coefficients** and **7738184 scratch-frame
incidences** are checked exactly. The resulting complex saving is `3.18e-9`;
the paired bit saving stays `2.96e-9`.

Douglas Colkitt's compact-control method is retained. It moves compact fields
at cost `O(V*((f log p)^tau+1))`, reserves complete temporary ranges from
existing coordinates, and charges exceptional repair in every recursion node.
The new finite network supplies the same phase interface with replacement
constants; no earlier direct-swap or hypothetical resampling proposal is used.

Use exact parameters `epsilon=0.1999`, `c=1`, `beta=0.001`, `delta=1e-6`,
`zeta=0.0001`, `C1=4.9961`, `lambda=1-2.959e-9` and `lambda'=1-2.958e-9`.
All **31** compact-system conditions are strict. The limiting margin is

$$G=5.913042\times10^{-10},\qquad G-\kappa=3.042\times10^{-13}>0.$$

For these fixed declared bit/complex savings and the retained inequalities,
the scoped supremum is `37/62500000148`, approximately `5.91999998598e-10`.
This is not a ceiling for other constructions or integer multiplication.

## Evidence and scope

| Component | Evidence |
| --- | --- |
| New graph and full scalar matrix | Exact support and coefficient checks |
| Forward/reverse scratch frames and repaired residuals | Complete finite incidence audit |
| Arbitrary scratch restoration | General cancellation identity and exact rational symbolic maps |
| Parameters, logarithm comparison, guard and margins | Generated rational certificate |
| Compact movement, reservations, repair and recurrence | Inherited written general proofs and dependency review |
| Source integration | Independent patch and internal-reference checks |
| Complete original multiplication theorem | Assumed |
| Original conversation ZIP | Unavailable; a fresh reconstruction is published |
| Independent expert review / formalization | Not supplied |

The [new audit](docs/research/orthogonal-star.md) records the construction and
remaining assumptions. The inherited [compact-control review](docs/research/compact-control-review.md)
records the general movement obligations. Its [PDF](artifacts/compact-control-note.pdf)
describes the preceding `8.3e-11` result; no new PDF build is claimed here.

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
| [frozen-154](patches/frozen-154.patch) | `2^-154` | Original network and recurrence exponents |
| [balanced-153](patches/balanced-153.patch) | `2^-153` | Balanced assembly parameters |
| [same-network-129](patches/same-network-129.patch) | `2^-129` | Original network, sharper recurrence comparison |
| [h46-111](patches/h46-111.patch) | `2^-111` | Smaller network, dyadic parameters |
| [h46-109](patches/h46-109.patch) | `2^-109` | Rational recurrence saving, strict final margin |
| [h46-108](patches/h46-108.patch) | `2^-108` | Variable stopping exponent |
| [h46-rational](patches/h46-rational.patch) | `5.8e-33` | Strongest supplied parameter-only witness |
| [nonadjacent-layout](patches/nonadjacent-layout.patch) | Original parameters retained | Routing proof and revised layout cost only |
| [frozen-nonadjacent-107](patches/frozen-nonadjacent-107.patch) | `2^-107` | Direct routing, original network and recurrence exponents |
| [h46-nonadjacent-78](patches/h46-nonadjacent-78.patch) | `2^-78` | Direct routing with the h = 46 network |
| [h46-nonadjacent-76](patches/h46-nonadjacent-76.patch) | `2^-76` | Direct routing with tuned dimension and stopping parameters |
| [h46-shared-side-75](patches/h46-shared-side-75.patch) | `2^-75` | Stage-1/stage-3 side-role sharing, routing, and parameter tuning |
| [h46-incidence-67](patches/h46-incidence-67.patch) | `2^-67` | Rectangle incidence circuits, full auxiliary sharing, routing, and parameter tuning |
| [h46-dag-63](patches/h46-dag-63.patch) | `2^-63` | Shared intermediate sums and reversible role allocation |
| [h46-shared-point](patches/h46-shared-point.patch) | `13*2^-66` | Cross-group sharing |
| [h50-paired-59](patches/h50-paired-59.patch) | `2^-59` | Paired sums, stopped guard and tighter Gaussian setup |
| **[compact-control-34](patches/compact-control-34.patch)** | **`83/10^12 > 2^-34`** | **Compact controls, complete reservations, local repair and separate complex arity** |
| [h50-paired-tuned](patches/h50-paired-tuned.patch) | `1.7523184e-18` | Earlier Paureel parameter refinement |
| [orthogonal-star-31](patches/orthogonal-star-31.patch) | `591/10^12 > 2^-31` | Paureel complex-network replacement with retained compact controls |

## Attribution, citation, and license

The orthogonal-star construction and earlier paired parameter refinement in this fork are by Aurel Prosz (Paureel),
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
