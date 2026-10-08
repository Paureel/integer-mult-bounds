# Compact dirty controls: a new movement candidate

**Follow-up completed locally:** the wider-control, reservation, repair and
layer proofs are now supplied in the [compact-control note](../../notes/compact-control-note.tex),
with a conditional `kappa=83/10^12 > 2^-34` witness. See
[current status](current-status.md). The text below preserves the initial
address-only audit and its then-open obligations; it is historical.
An independent research agent proposed moving compact control fields instead
of gathering the spaced target windows. This pass checks that proposal with
arbitrary temporary values, including the case where the source slot follows
the target slot. It is now the priority movement candidate, ahead of the
previously proposed central-gate splitting experiment.

The checked code is [audit_compact_controls.py](../../scripts/audit_compact_controls.py)
and its output is [compact-control-audit.json](../../certificates/compact-control-audit.json).
These are address-permutation controls, not a certified fixed-tape runtime
or a replacement manuscript proof.

## 1. Why the dirty temporary cancels

For a control bit x, target segment u, and arbitrary temporary digit t,
perform the integer operations

    u1 = u + 2*x*t,
    t1 = t + (u1 mod 2),
    u2 = u1 + x*(1-2*t1),
    t2 = t1 - ((u2 mod 2) XOR x).

The first operation preserves target parity a=u mod 2. Consequently

    u2 = u + x*(1-2*a),
    t2 = t.

Thus the target parity is XORed with x, its guard quotient is restored, and
the arbitrary temporary digit returns exactly to its original value. The
temporary is not assumed to be zero, and its load is modular addition, not
an overwrite or a free copy.

For f selected bits, use n=f-1 such segments, omitting the highest selected
position as in the original packed-rectangle proof. Each segment begins at
j_i=rho+iK. Pack the n temporary digits into nG consecutive bits, with radix
B=2^G. The four simultaneous integer updates become whole-field modular
rotations. Supply the omitted highest selected bit separately through the
retained elementary two-bit XOR.

## 2. Actual physical field order

When x precedes y, assume complete compact fields t before x and b after y,
each of width nG. The physical layout may be written t,x,y,b, with arbitrary
spectator intervals. The first and third rotations target y and use x,t as
controls. To update t using y, swap t and b, rotate the back field using the
preceding y, then swap back. Apply the same pattern when unloading t.

This uses four width-nG swaps and four rotations. The field b has arbitrary
initial contents, restored by the two swaps around each load or unload.

When x follows y, use layout u,t,y,x,b, with three compact fields u,t,b.
First perform the earlier-source procedure controlled by the digit parities
of u. Load the selected bits of x into u by swapping u with b, rotating the
back field, and swapping back. Perform the earlier-source procedure again,
now controlled by the updated digit parities of u. Finally unload x from u.
Off temporary-digit overflow, the two control parities XOR to x. This uses
twelve compact swaps and ten rotations. One back field can be reused because
each load/unload restores its arbitrary contents.

Every rotation in the checker has an explicit list of controls. It checks
that all controls physically precede that rotation's target.

## 3. A sufficient invariant exceptional set

Exclude any address with a temporary t digit equal to B-1. For each used
K-bit segment of y, write its initial value as 2g+a and require

    2B <= g < 2^(K-1)-2B.

This conservative interval keeps every intermediate target value within its
own segment. The temporary load also stays in its own radix-B digit. Hence
the packed modular operations agree with the independent integer identities
on the good set. They preserve all bits outside the used selected positions.

For a late source, additionally exclude any u digit equal to B-1. The first
parity flip preserves the target guards; loading x into u cannot then carry
between temporary digits. The second flip and unload restore u,t,b.

With complete independent field ranges, union bounds give

    delta_early <= min(1, n*(2^(-G)+8*2^(G-K))),
    delta_late  <= min(1, n*(2*2^(-G)+8*2^(G-K))).

The ideal operation preserves the target guards and every temporary field,
so this bad set is invariant under it. Every actual primitive is a bijection,
and the complete operation agrees with the ideal map off the bad set.
The actual operation therefore preserves the same bad set. As in the
upstream repair argument, T S^-1 is supported on that set. The checker
constructs the inverse by reversing every rotation and swap and verifies
the repaired address map, including bad inputs.

Taking G=4*ceil(log2 p)+6 makes the temporary-overflow term O(p^-3) when
n<=p. For K=d^c with fixed positive c and d=Theta(p^epsilon), the term
p*2^(G-K) is smaller than every inverse fixed power of p. This is the
right density scale for the retained sorting repair, but its complete
descriptor, inverse-computation and tape costs still need a written audit.

## 4. Two substantive proof obligations

**Wider controls.** The original ordered-affine lemma requires controls of
O(b) digits for a b-digit target. Here a y control can have nK bits while
the back target has only nG. A new bound must explicitly charge offset work.
The natural extension is O(V+M*poly(p)) for M records, because every control
and descriptor has O(p) bits and a fixed number of fields is used. Under
the existing superpolynomial record-width assumption, this would be O(V).
The two-piece rotation implementation in the original lemma suggests this
extension, but the old hypothesis cannot simply be omitted when citing it.

**Complete temporary fields in every child.** The current layer contract
does not promise front and back scratch fields. They cannot be appended as
new independent address coordinates: that would multiply the record volume
by their ranges.

A candidate allocation is to process selected axes in reserved leading and
trailing chunks individually, then retain their address bits as spectators.
Keep the front temporary region separate from the row index divided among
roles. Every row and recursive child must retain the complete temporary
ranges; padding and reassembly must preserve this property.

Reserving O(dG) bits at each end needs O(dG/K+1) chunks, and their individual
processing would cost

    O(V*(d^(1-c)*log(p)+1)).

This is a new top-level cost. It must be included in the layer exponent,
with strict slack above 1-c, and in the treatment of small D where the
reserved regions would overlap. It need not automatically fit below the
recursion's stopping exponent beta: what matters for this preprocessing
cost is the final layer bound. This allocation is a proposed route, not a
completed recursive invariant or an integrated proof patch.

If both obligations and the repair are discharged, the candidate row-addition
cost is O(V*((f*log(p))^tau+1)), without the old K^tau factor. The full layer
must then be recomputed, including preprocessing, leaves, guards, complex
recursion and assembly margins. The earlier 2^-39 and 2^-34 targets remain
hypothetical until that work is complete.

## Verification and next priority

The address suite exhausts 2480 elementary integer cases and 24,576 small
packed cases, and checks 7200 deterministic samples with several segments,
extreme selected offsets, arbitrary scratch, inversion, bad-set invariance,
and exact exceptional repair. It also verifies the physical order of every
rotation's controls. These counts do not establish asymptotic tape costs.

Run `python3 scripts/audit_compact_controls.py` and
`python3 -m unittest discover -s tests -p test_compact_controls.py -v`.

The next bounded research goal should audit the wider-control streaming
bound and temporary-field allocation first. If either requires an overhead
that restores the old spacing penalty, record that obstruction promptly.
If they work, finish the repair and full recurrence before promoting any
new exponent. The proposed finite-network goal becomes the fallback.
