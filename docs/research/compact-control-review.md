# Compact-control result: proof dependencies and review guide

This guide accompanies the conditional witness `kappa = 83/10^12 > 2^-34`.
It records the supplied arguments and their verification limits. It is an
author-side publication review, not independent mathematical review.

Start with the [nine-page note](../../artifacts/compact-control-note.pdf), then
the [combined patch](../../patches/compact-control-34.patch). The patch applies
directly to the pinned upstream source; it includes the retained improvements
and all four new construction sections. No earlier patch should be applied first.
The patched title page identifies Douglas Colkitt's modifications and states
their conditional status. Every changed source file has a modification notice;
the resulting manuscript is not presented as an OpenAI release.

## Retained assumptions

The upstream commit is `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Its complete
multiplication theorem is not proved or formally verified by this repository.
The present result retains its stream model, bit-transfer and complex-phase
interfaces, analytic estimates, resampling, prime selection, synthetic
transforms, and final rounding. It also retains the project's paired bit
network, nonadjacent routing and tighter Gaussian setup.

The relevant source contracts are:

- `02-streams.tex`, `lem:elementary-streams` and `lem:ordered-affine-streams`:
  fixed-tape stream operations and ordered controlled rotations.
- `04-swap.tex`, `lem:chunk-swap`: arbitrary-width, nonadjacent binary chunk
  interchange, including arbitrary spectators, padding and cleanup.
- `03-motifs.tex`, `lem:motif-residuals` and the complex phase interface:
  scalar circuit, residual orthonormal bases and signed endpoints.
- `05-layers.tex` and `08-assembly.tex`: the retained layer interface and
  final multiplication assembly, with the replacements identified below.

Section labels refer to the bundled source or to the combined patched source,
as appropriate. The [reproduction instructions](../reproducibility.md) explain
how to materialize the latter without modifying `upstream/`.

## New obligations and supplied arguments

| Obligation | Argument supplied | What to challenge |
| --- | --- | --- |
| Controls wider than a rotation target | `lem:record-paid-rotation` in [movement](../../notes/compact-control-movement.tex): two-piece streaming, polynomial offset work per prefix fiber, at most one fiber per record | Whether every counter, reset and offset computation is paid by `O(V+M A^C)` without a descriptor scan per payload bit |
| Dirty compact controls | Earlier/later-source constructions in the same source; four-update cancellation, modular swaps and loads | Control order, arbitrary initial temporaries, digit overflow and both source orders |
| Deterministic exceptional repair | Ideal map preserves the bad set; actual bijection agrees off it; sort records under `T S^-1` | Bad-set invariance, inverse offsets on current controls, guard boundaries and exact restoration |
| Existing-coordinate temporaries | [Layout proof](../../notes/compact-control-layout.tex): two front ranges and one back range carved from reserved chunks | Full ranges in every child, no hidden extra volume, small-`D` fallback and reserved-axis cost |
| Recursive cost | Same source: `F(e) <= (s/W)F(e/m) + O((e log p)^tau+1)` plus leaf and reservation costs | Exactly `V/W` child volumes, spectator layout, stopping depth and uniform constants |
| Precision | [Generalized guard](../../notes/compact-control-guard.tex): additive node depth charge and actual stopping depth | New operations must only permute whole coefficient encodings; reserved kernels and all base-`m` pieces must be counted |
| Independent complex arity | [Complex interface](../../notes/independent-complex.tex): original motif at `h=25`, unchanged bit motif at `h=50` | Residual nondegeneracy and norm-one witnesses, scalar restoration, endpoints and absence of a hidden equal-arity requirement |
| Final assembly | Note and patched `08-assembly.tex`: seven margins and a strict absorption gap | Every changed cost must enter the completed layer estimate; retained numerical hypotheses must still hold |

The old ordered-affine lemma alone does **not** establish the wider-control
bound: its original control-width hypothesis is narrower. The new proof pays
polynomial offset work using the superpolynomial record length.

Likewise, the old global exceptional-sort estimate based on `2^-K` does **not**
apply. The new bad fraction is at most `5/(128 p^3)` beyond the common cutoff.
Sorting costs `O(V_call/p^2)` and extraction/reinsertion `O(V_call)` at each
node; these enter the volume-weighted recurrence. The patch replaces the
old global argument explicitly.

The complete-field invariant concerns address ranges, not zero scratch values.
Each row contains all front, active and back coordinates. Padding adds whole
rows, and recursive role splitting divides only the separate row index.
Completed calls restore every temporary coordinate and preserve each original
row, so the padded zero rows can be removed.

## Exact witness and scoped ceiling

The [layer certificate](../../certificates/compact-control-layer.json) records
all parameter slacks and the hashes of the four construction sources. It gives

    min(g_1, ..., g_7) = 333833/(4*10^15) = 8.345825e-11,
    kappa = 83/10^12 = 8.3e-11,
    min(g_i) - kappa = 1833/(4*10^15) > 0.

The strongest supplied witness is about 47.85 million times the previous
`2^-59` saving. If comparing the simpler dyadic corollaries alone,
`2^-34 / 2^-59 = 2^25 = 33,554,432`. Neither ratio is a runtime benchmark.

The upper enclosure `8.369598075e-11` applies to the unchanged `h=25` complex
motif and the retained Gaussian/leaf inequalities. It is not an all-network
ceiling, an optimality theorem for integer multiplication, or a barrier to a
different assembly. The witness exceeds 99% of this scoped upper enclosure.

## Reproducible checks and their limits

Run the focused checks with:

```sh
python3 scripts/audit_compact_controls.py
python3 scripts/compact_control_layer.py
python3 scripts/make_compact_control_patch.py
python3 -m unittest discover -s tests -p 'test_compact_control*.py' -v
git apply --check --directory=upstream patches/compact-control-34.patch
```

Run `make verify` for the full suite and `make compact-note` for the note.
The finite checks cover packed modular address maps and inverses, dirty
temporaries, repair, two-piece rotations, row padding/splitting, recurrence
orderings, rejected parameter choices, and source integration. They do not
simulate the complete fixed-tape multiplication machine or mechanically verify
the asymptotic proofs. PDF compilation checks typesetting and references.

Publication preparation found no additional blocker in this author-side pass.
Independent review remains outstanding, especially for the wider-control tape
bound, recursive layout invariant and local repair summation. A substantive
failure in those arguments would revoke the new headline; passing arithmetic
tests alone would not rescue it.
