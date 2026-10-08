# Bounded coded-carry attempt and assessment

**Outcome: exact gap restoration, but no sublinear recurrence and no new
kappa.** Stop this bounded attempt. The construction below works, yet its
best demonstrated cost is linear in the number of windows. A scoped bound
also excludes compressing it into a sublinear number of whole-slot affine
movements in a fixed-bank circuit. This does not exclude recursive coded
networks or general tape algorithms.

The published result remains conditional kappa=2^-59. This follows the
[gather-schedule audit](gather-schedule-audit.md). The implementation is
[audit_coded_carries.py](../../scripts/audit_coded_carries.py), with exact
[controls and assessment](../../certificates/coded-carry-audit.json).

## 1. Concrete target and stopping criterion

An earlier control slot supplies n values x_j in [Q], Q=2^g. A target slot
has n periods of K bits, K>g, each containing a low g-bit value y_j and
arbitrary gap bits. Perform

    y_j <- y_j+x_j modulo Q

without changing any gap bit, control value, spectator coordinate or payload.
This is the strided affine operation that the previous whole-slot substitute
failed to implement: its carries changed a positive-density set of gaps.

For this bounded experiment, require an exact small identity and a cost
that could lead to a sublinear recurrence. A correct identity with a linear
number of full-stream stages is not sufficient to continue a large search.

## 2. Exact code: split by carries, translate, recombine

For one window define c_j=[y_j+x_j>=Q]. On the c_j branch, translate the
whole target slot by

    (x_j-Q c_j) 2^(jK).

The new short-field value lies in [0,Q), so there is no net carry or borrow
into its gap. Let D_(j,c) be the address-dependent diagonal mask selecting
that branch, and P_b the full-slot cyclic translation by b. The exact
operator is

    T_j = P_(x_j 2^(jK)) D_(j,0)
        + P_((x_j-Q) 2^(jK)) D_(j,1).

This identity holds for arbitrary record values. The two masked streams
have disjoint destination support, so their sum, or bitwise XOR for bit
payloads, gives the required permutation. Selecting a branch can be done
by a full-stream scan with address arithmetic polynomial in p, absorbed by
the retained superpolynomial record width. Each translation is a legitimate
ordered-affine call because its offset uses only the earlier controls and
the fixed branch choice. Temporary streams use a fixed number of tapes and
are cleared after use.

The different T_j commute as exact operators, because each updates a
different short field and restores all gaps. Their product implements the
whole target. The code tests the product and a direct address map on complete
arrays, including all arbitrary gap values.

### Two implementations, neither with a saving

Expanding the product gives 2^n masked translation terms, indexed by the
complete carry pattern c. Their offsets are

    sum_j (x_j-Q c_j) 2^(jK).

When every x_j is nonzero, every carry pattern occurs, and the offsets are
distinct modulo 2^(nK). This flat expansion is exponential.

Keeping the product factored uses two translations per window and O(n)
full-stream stages. It costs O(Vn) in the retained record regime. A balanced
description has normalized recurrence

    F(n) = 2F(n/2)+O(1), F(1)=O(1).

Both subcomputations still act on the entire array. Creating two temporary
copies does not give two role streams of volume V/2. There is no analogue of
the original all-role network's s/W contraction. Restoring arbitrary gaps
is solved here; improving the recursive cost is not.

## 3. Why a fixed invertible encoding cannot simply hide the carry

Already for one window, full-slot unit translation on K bits has order 2^K,
whereas incrementing only the low g bits has order 2^g. After 2^g full-slot
increments, a gap bit changes; the desired short-field operator is identity.

Conjugation by an invertible encoding preserves operator order. Thus no
fixed invertible encoding of the entire arbitrary-input state space turns
that full shift into the short-field increment. The statement also holds
for invertible linear encodings of full data banks. It does not exclude
redundant encodings followed by projection or a multi-operation construction
such as the exact code above.

## 4. Flat affine coding still needs linearly many movements

The next question was whether algebraic cancellation between coded streams
could combine the exponential carry branches into only a few movements.
There is a useful obstruction for a precisely specified class.

### Circuit class

Use a fixed number W of banks with the same complete address domain and
unchanging bank volume. Allow arbitrary address-dependent pointwise linear
mixing between banks, including masks, copies and cancellations. Movement
gates apply affine permutations to full equal-width address slots. They may
mix those slots affinely and temporarily change arbitrary auxiliary slots.
Their parameters may depend on read-only controls. Each movement is charged
as a separate complete-bank pass. There is no recursive row splitting,
smaller-volume child, or permutation of a proper subfield hidden in a gate.
Changing radix or padding to a different address domain is also outside this
fixed-domain model.

Fix the read-only controls. For k movement gates, expanding any output/input
bank block into computation paths gives at most 2^k address maps: each path
uses a chronological subset of those gates. Pointwise masks and coding
change coefficients or cancel paths, but introduce no new address graph.
Each path map is affine. For a distinguished slot y, fixing all other input
slot values makes its output coordinate ay+b modulo 2^L, with L=nK.
The coefficient a need not be odd when slots are mixed.

### An affine graph covers only a small part of the target

Consider the required special case of flipping n separated selected bits:

    T(y)=y XOR M, M=sum_j 2^(rho+jK), 0<=rho<=K-3.

At most 2^(L-n) values of y satisfy T(y)=ay+b for any a,b modulo 2^L.
Here is an elementary proof, valid for every n and K in the stated range.
Write y=sum_i 2^i y_i and let s_i be -1 at selected positions and +1
elsewhere. Then

    T(y)-ay = M + sum_i (s_i-a) 2^i y_i modulo 2^L.

If a is even, all s_i-a are odd. The summand weights have distinct
2-adic valuations 0,...,L-1. Their subset sums are distinct modulo 2^L:
in any difference, the least nonzero valuation cannot cancel. Thus every
right-hand side occurs at most once.

If a=1 modulo 4, choose the n selected coordinates. Each coefficient
-1-a has valuation one, giving distinct weight valuations rho+jK+1<L.
If a=3 modulo 4, choose the n unselected coordinates immediately above
the selected ones. Their coefficients 1-a have valuation one, giving
distinct valuations rho+jK+2<L. In either case, fix all other coordinates;
the chosen n coordinates give distinct sums. There are only 2^(L-n)
settings of the other coordinates, proving the agreement bound.

For multiple mutable slots, fix their other input values and apply this
argument to y. The requirement to restore those other slots can only reduce
agreement. Hence each affine path graph covers at most a 2^-n fraction of
the complete target graph. At least 2^n path graphs are needed, and therefore

    2^k >= 2^n, so k>=n.

This permits arbitrary coding coefficients and cancellations. A required
nonzero target entry must lie in the support of at least one path, regardless
of how the path coefficients combine. With fixed W and separate full-bank
passes, k>=n precludes a sublinear-in-n bound in this model.

The one-bit target also occurs in the general short-field interface: choose
x_j=2^(g-1). Addition modulo 2^g then flips only the top short-field bit,
so rho=g-1; K>=g+2 supplies the two gap positions needed by the proof.
Thus this is not merely a small-g artifact. At K=2,rho=0 the clean bound
does have a boundary exception: the corresponding agreement maximum is
2^(L-n+1). The controls explicitly test that exception.

### Fixed-order ordered-affine operations

The same path argument applies, separately, to the manuscript's forward
whole-slot operations while field order stays fixed. These can add nonlinear
functions of earlier fields to a later target. Earlier fields never depend
on the initial value of y. Along each path, the output y is still affine in
its own initial value when the other initial coordinates are fixed.
Consequently the same agreement bound applies.

This extension does **not** allow combining those nonlinear operations with
arbitrary field exchanges: moving a later field back into y can introduce
nonlinear dependence on the original y and escape the argument. Nor does the
argument cover recursion that splits banks into smaller volumes. These are
real escape routes, including mechanisms used in the upstream machinery.
The result is not a general lower bound for coded gathering or multiplication.

## 5. Assessment and decision

The bounded attempt produced an exact operation and a meaningful limitation
of its natural coded implementation. It produced **no candidate with a
sublinear recurrence**. Cheap exact carry cancellation alone is insufficient
when it still takes a full-stream stage per window.

The evidence does not justify expanding this into a broad topology search
now. Return the main effort to stronger finite networks. Keep the short-guard
reduction and conditional linear targets as reusable infrastructure, but
reopen this direction only for a concrete construction that supplies smaller
child volumes or costed backward/nonlinear address movement and demonstrates
the complete all-role contraction. A suggestive identity or a new encoding
without that cost calculation is not enough.

## Verification

Run `python3 scripts/audit_coded_carries.py` and
`python3 -m unittest discover -s tests -p test_coded_carries.py -v`, or
`make verify`. Eight tests check complete small basis inputs, arbitrary gap
values, exact carry codes, translation support, exhaustive small affine
agreement, the distinct-valuation proof controls, encoding order, and the
scope boundary for nonlinear ordered operations. These finite checks support
the written arguments; they do not formally verify the upstream theorem.
Published certificates, source patches and the bundled manuscript are unchanged.
