"""Exact certificate for Paureel's orthogonal-star complex network.

Developed with ChatGPT; independently reconstructed and audited with Codex.
The original conversation archive was unavailable during integration. This
implementation builds queries and balanced sums from their mathematical
definitions and reproduces the reported counts. It does not formally verify
the retained multiplication theorem or the general compact-control tape proof.
"""
from array import array
from itertools import combinations
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import comb, factorial
from pathlib import Path
import json

from certify import Parameters, constraints, margins, verify_sources

ROOT = Path(__file__).resolve().parents[1]
BIT_SAVING = Q(296, 10**11)
COMPLEX_SAVING = Q(318, 10**11)
KAPPA = Q(591, 10**12)
BASE_REPOSITORY_COMMIT = '6e564879f51ae16f23d392e9e196c605f36d90df'


def need(ok, message):
    if not ok:
        raise ValueError(message)


class Group:
    def __init__(self, h, pair, indices, triples, masks):
        self.h, self.pair, self.indices = h, pair, indices
        self.triples, self.masks = triples, masks
        self.n = len(indices)
        self.support = [0] + [1 << i for i in range(self.n)]
        self.args = [None] * (self.n + 1)
        self.lookup = {s: i for i, s in enumerate(self.support)}
        self.outputs = []
        self.repairs = 0
        for target, sm in enumerate(masks):
            for size, sign in ((0, Q(1, 2)), (2, Q(-1, 2))):
                selected = sum(1 << j for j, idx in enumerate(indices)
                               if (masks[idx] & sm).bit_count() == size)
                if not selected:
                    continue
                selections = [selected]
                if self.canonical(selected) == ((1 << h) - 1) ^ sm:
                    # A zero-dimensional residual needs no orthonormal basis.
                    if h - 1 - selected.bit_count() > 0:
                        bit = selected & -selected
                        need(selected != bit, 'Cannot repair a singleton')
                        selections = [bit, selected ^ bit]
                        self.repairs += 1
                for subset in selections:
                    residual_dimension = h - 1 - subset.bit_count()
                    residual_canonical = ((1 << h) - 1) ^ sm ^ self.canonical(subset)
                    need(not residual_dimension or residual_canonical,
                         'Alternating output residual')
                    self.outputs.append((target, sign, self.build(subset)))
        self.code = self.compile()

    def canonical(self, subset):
        answer = 0
        while subset:
            bit = subset & -subset
            subset ^= bit
            answer ^= self.masks[self.indices[bit.bit_length() - 1]]
        return answer

    def build(self, subset, lo=0, hi=None):
        if not subset:
            return 0
        if subset in self.lookup:
            return self.lookup[subset]
        hi = self.n if hi is None else hi
        mid = (lo + hi) // 2
        left = subset & (((1 << mid) - 1) ^ ((1 << lo) - 1))
        right = subset ^ left
        if not left:
            return self.build(right, mid, hi)
        if not right:
            return self.build(left, lo, mid)
        a, b = self.build(left, lo, mid), self.build(right, mid, hi)
        need(not self.support[a] & self.support[b], 'Overlapping sum inputs')
        node = len(self.args)
        self.lookup[subset] = node
        self.support.append(subset)
        self.args.append((a, b))
        return node

    def compile(self):
        users = [[] for _ in self.args]
        for node, args in enumerate(self.args):
            if args:
                for pos, parent in enumerate(args):
                    users[parent].append(('gate', node, pos))
        for output, (_, _, node) in enumerate(self.outputs):
            users[node].append(('output', output))
        edge, source, output, gates = {}, {}, {}, []
        roles = 0
        for node in range(1, len(self.args)):
            need(users[node], 'Dead node changes the role count')
            if self.args[node]:
                ins = (edge[node, 0], edge[node, 1])
                pivot = ins[0]
            else:
                pivot = roles
                roles += 1
                ins = (pivot,)
                source[self.indices[node - 1]] = pivot
            outs = (pivot,) + tuple(range(roles, roles + len(users[node]) - 1))
            roles += len(users[node]) - 1
            need(len(set(ins)) == len(ins), 'Aliased inputs')
            need(set(ins) & set(outs) == {pivot}, 'Invalid pivot reuse')
            gates.append((node, ins, outs))
            for use, slot in zip(users[node], outs):
                if use[0] == 'gate':
                    edge[use[1], use[2]] = slot
                else:
                    output[use[1]] = slot
        additions = len(self.args) - self.n - 1
        need(roles == additions + len(self.outputs), 'Wrong reversible role count')
        return dict(roles=roles, sources=source, outputs=output, gates=gates)

    def frames(self):
        # Labels describe the P-tensor summand. The common B-tensor F
        # summand is restored by the separate stage-boundary argument.
        zero = ('zero', 0)
        full = ('full', 0)
        allbits = (1 << self.h) - 1
        metadata = {zero: (0, 0), full: (self.h, allbits)}
        for idx, tm in enumerate(self.masks):
            metadata['line', idx] = (1, tm)
            metadata['line_complement', idx] = (self.h - 1, allbits ^ tm)
        for node in range(1, len(self.args)):
            subset = self.support[node]
            dim, canon = subset.bit_count(), self.canonical(subset)
            metadata['span', node] = (dim, canon)
            metadata['complement', node] = (self.h - dim, allbits ^ canon)

        def contains(a, b):
            if a == b or a == zero or b == full:
                return True
            ak, av = a
            bk, bv = b
            if ak == bk == 'span':
                return not self.support[av] & ~self.support[bv]
            if ak == bk == 'complement':
                return not self.support[bv] & ~self.support[av]
            if ak == 'line' and bk == 'span':
                return self.support[bv] == (1 << self.indices.index(av))
            if ak == 'span' and bk == 'line_complement':
                subset = self.support[av]
                return all(not (self.masks[self.indices[j]] & self.masks[bv]).bit_count() % 2
                           for j in range(self.n) if subset & (1 << j))
            if ak == 'line' and bk == 'complement':
                subset = self.support[bv]
                return all(not (self.masks[av] & self.masks[self.indices[j]]).bit_count() % 2
                           for j in range(self.n) if subset & (1 << j))
            if ak == 'complement' and bk == 'line_complement':
                return self.support[av] == (1 << self.indices.index(bv))
            return False

        counts = dict(forward=0, reverse=0, nonzero_residuals=0)
        for reverse in (False, True):
            state = [zero] * self.code['roles']
            direction = 'reverse' if reverse else 'forward'

            def set_frame(slot, label):
                old = state[slot]
                need(contains(old, label), f'Frame decrease or bad inclusion: {old}, {label}')
                da, ca = metadata[old]
                db, cb = metadata[label]
                need(db >= da, 'Dimension decrease')
                need(db == da or ca ^ cb, 'Alternating nonzero residual')
                if db > da:
                    counts['nonzero_residuals'] += 1
                state[slot] = label
                counts[direction] += 1

            def mixer(label, backwards=False):
                gates = reversed(self.code['gates']) if backwards else self.code['gates']
                for node, ins, outs in gates:
                    target = label(node) if callable(label) else label
                    for slot in set(ins + outs):
                        set_frame(slot, target)

            def copy(label):
                for idx, slot in self.code['sources'].items():
                    set_frame(slot, label(idx) if callable(label) else label)

            def inject(label):
                for query, slot in self.code['outputs'].items():
                    idx = self.outputs[query][0]
                    set_frame(slot, label(idx) if callable(label) else label)

            if not reverse:
                mixer(zero); inject(zero); mixer(zero, True)
                copy(lambda idx: ('line', idx))
                mixer(lambda node: ('span', node))
                inject(lambda idx: ('line_complement', idx))
                mixer(full, True); copy(full)
            else:
                copy(zero); mixer(zero)
                inject(lambda idx: ('line', idx))
                mixer(lambda node: ('complement', node), True)
                copy(lambda idx: ('line_complement', idx))
                mixer(full); inject(full); mixer(full, True)
            need(all(label == full for label in state), 'Incomplete terminal frames')
        return counts


def construct(h):
    triples = list(combinations(range(h), 3))
    masks = [sum(1 << j for j in t) for t in triples]
    partition = defaultdict(list)
    for idx, t in enumerate(triples):
        a = [j for j in t if j < h // 2]
        b = [j for j in t if j >= h // 2]
        partition[tuple((a if len(a) >= 2 else b)[:2])].append(idx)
    groups = [Group(h, p, ids, triples, masks) for p, ids in partition.items()]
    return triples, masks, groups


def verify_matrix(masks, groups):
    """Check all scalar coefficients, including every required zero."""
    v = len(masks)
    side = array('b', [0]) * (v * v)
    for group in groups:
        for target, coefficient, node in group.outputs:
            subset = group.support[node]
            twice_coefficient = int(2 * coefficient)
            while subset:
                bit = subset & -subset
                subset ^= bit
                source = group.indices[bit.bit_length() - 1]
                address = target * v + source
                need(side[address] == 0, 'A side coefficient is charged twice')
                side[address] = twice_coefficient
    for target, tm in enumerate(masks):
        for source, sm in enumerate(masks):
            center = (tm & sm).bit_count() - 1
            expected = 2 if target == source else 0
            need(center + side[target * v + source] == expected,
                 f'Wrong scalar coefficient at ({target},{source})')
    return v * v


def finite_audit(h=25):
    triples, masks, groups = construct(h)
    result = dict(h=h, triples=len(triples), groups=len(groups), additions=0,
                  outputs=0, repairs=0, roles=0, forward=0, reverse=0,
                  nonzero_residuals=0)
    digest = sha256()
    for group in groups:
        for i, source in enumerate(group.indices):
            for j, other in enumerate(group.indices):
                need((masks[source] & masks[other]).bit_count() % 2 == (i == j),
                     'Group indicators are not orthonormal')
        result['additions'] += len(group.args) - group.n - 1
        result['outputs'] += len(group.outputs)
        result['repairs'] += group.repairs
        result['roles'] += group.code['roles']
        for key, value in group.frames().items():
            result[key] += value
        digest.update(json.dumps([group.pair, group.indices, group.args,
            [(target, str(sign), node) for target, sign, node in group.outputs]],
            separators=(',', ':')).encode() + b'\n')
    result['matrix_coefficients'] = verify_matrix(masks, groups)
    result['circuit_sha256'] = digest.hexdigest()
    need(result['forward'] == result['reverse'], 'Orientation count mismatch')
    if h == 25:
        need(result['additions'] == 160046, 'Addition count mismatch')
        need(result['outputs'] == 323990, 'Output count mismatch')
        need(result['repairs'] == 50, 'Repair count mismatch')
        need(result['roles'] == 484036, 'Role count mismatch')
        need(result['forward'] + result['reverse'] == 7738184,
             'Scratch incidence count mismatch')
    return result


def symbolic_audit(h=7):
    triples, masks, groups = construct(h)
    v = len(triples)
    center_start = 2 * v
    offset = center_start + h + 1
    placed = []
    for group in groups:
        placed.append((group, offset))
        offset += group.code['roles']

    def add(forms, target, source, scale=Q(1)):
        value = dict(forms[target])
        for variable, coefficient in forms[source].items():
            value[variable] = value.get(variable, Q(0)) + scale * coefficient
            if not value[variable]:
                del value[variable]
        forms[target] = value

    schedule = [('L', 1), ('J', -1), ('L', -1), ('R', -1),
                ('V', 1), ('G', 1), ('R', 1), ('L', 1),
                ('J', 1), ('L', -1), ('G', -1), ('V', -1)]
    for inverse in (False, True):
        forms = [{i: Q(1)} for i in range(offset)]
        operations = [(op, -sign) for op, sign in reversed(schedule)] if inverse else schedule
        for op, sign in operations:
            if op == 'L':
                for group, base in placed:
                    gates = reversed(group.code['gates']) if sign < 0 else group.code['gates']
                    for node, ins, outs in gates:
                        pivot = base + ins[0]
                        if sign > 0:
                            for role in ins[1:]:
                                add(forms, pivot, base + role)
                            for role in outs[1:]:
                                add(forms, base + role, pivot)
                        else:
                            for role in reversed(outs[1:]):
                                add(forms, base + role, pivot, Q(-1))
                            for role in reversed(ins[1:]):
                                add(forms, pivot, base + role, Q(-1))
            elif op == 'V':
                for group, base in placed:
                    for idx, slot in group.code['sources'].items():
                        add(forms, base + slot, idx, Q(sign))
            elif op == 'J':
                for group, base in placed:
                    for query, slot in group.code['outputs'].items():
                        target, coefficient, _ = group.outputs[query]
                        add(forms, v + target, base + slot, sign * coefficient)
            elif op == 'G':
                for idx, triple in enumerate(triples):
                    for point in triple:
                        add(forms, center_start + point, idx, Q(sign))
                    add(forms, center_start + h, idx, Q(sign))
            elif op == 'R':
                for idx, triple in enumerate(triples):
                    for point in triple:
                        add(forms, v + idx, center_start + point, Q(sign, 2))
                    add(forms, v + idx, center_start + h, Q(-sign, 2))
        for idx, form in enumerate(forms):
            expected = {idx: Q(1)}
            if v <= idx < 2 * v:
                expected[idx - v] = Q(-1 if inverse else 1)
            need(form == expected, f'Symbolic dirty-scratch failure at role {idx}')
    return dict(h=h, independent_input_variables=offset,
                forward_and_inverse_exact=True, arbitrary_scratch_restored=True)


def counts(h=25, additions=160046, outputs=323990):
    v, m = comb(h, 3), h**3
    N, roles = v**3, additions + outputs
    W = 2 * N + 3 * v * v * (roles + h + 1)
    loss = 3 * v * v * h * (h + 1)
    s = W * m - 2 * N + 2 * loss
    return dict(h=h, v=v, m=m, N=N, additions=additions, outputs=outputs,
                side_roles=roles, W=W, L=loss,
                s=s, eta=Q(W*m-s, W*m))


def parameters():
    return Parameters(tau=1-BIT_SAVING, sigma=1-COMPLEX_SAVING,
        epsilon=Q(1999,10000), c=Q(1), lam=1-Q(2959,10**12),
        lamp=1-Q(2958,10**12), kappa=KAPPA, beta=Q(1,1000),
        delta=Q(1,10**6), C1=Q(49961,10000))


def parameter_certificate(p=None):
    p = p or parameters()
    need(0 < 1-p.tau <= BIT_SAVING, 'Unsupported bit saving')
    need(0 < 1-p.sigma <= COMPLEX_SAVING, 'Unsupported complex saving')
    zeta = Q(1,10000)
    need(p.C1 == 5-4*p.beta+zeta, 'Guard exponent mismatch')
    chi = p.tau+(1-p.beta)*max(p.sigma-p.tau,Q(0))
    slacks = constraints(p, layout_model='nonadjacent', assembly_model='tight-gaussian')
    slacks['packed_overhead'] = p.lam-chi
    slacks['reserved_axes'] = p.lamp-max(Q(0),1-p.c)
    for name, slack in slacks.items():
        need(slack > 0, 'Failed strict constraint: '+name)
    gs = margins(p, layout_model='nonadjacent', assembly_model='tight-gaussian')
    need(min(gs.values()) > p.kappa, 'No strict absorption gap')
    return dict(parameters=vars(p), zeta=zeta, internal_exponent=chi,
                constraint_slacks=slacks, margins=gs,
                minimum_margin=min(gs.values()), absorption_gap=min(gs.values())-p.kappa)


def guard_certificate(n):
    m, W, s = n['m'], n['W'], n['s']
    need(m >= 3 and 2 <= s < m**5, 'Depth bound does not apply')
    # One invocation uses 4 mixers, 2 copies, 2 side injections and 4
    # center operations. Counting elementary scalar updates also pays for
    # fanout. Across the three stages their count is < 64(W+m+1)^3.
    per_invocation = 4*(3*n['additions']+n['outputs'])+2*n['v']+2*n['outputs']+8*n['h']*n['v']
    scalar_updates = 3*n['v']**2*per_invocation
    E = 64*(W+m+1)**3
    # Each inverse child has two diagonal signs and a fourth-root phase;
    # endpoint corrections and bank restoration add at most a fixed number
    # per role. Sixteen pays for each such child/role and bookkeeping.
    total_node_updates = scalar_updates+16*(s+W+m+1)
    need(total_node_updates < E, 'New node operations exceed the retained charge')
    B = s+E
    zeta = Q(1,10000)
    raw = max(Q(128*m*B*B),18*m*B*B*(1+1/zeta))
    C0 = -(-raw.numerator//raw.denominator)
    need(s*(8+E) <= 9*B*B, 'One-piece guard constant fails')
    need(9*m*B*B*(1+1/zeta)+18 <= C0, 'Whole-layer guard constant fails')
    return dict(E=E,B=B,C0=C0,C1=5-4*Q(1,1000)+zeta,
                elementary_scalar_updates_upper=scalar_updates,
                total_node_updates_upper=total_node_updates,
                node_charge_scope='Scalar updates plus retained inverse/endpoint wrappers fit E. Permutation operations add no coefficient depth.')


def serializable(value):
    if isinstance(value,Q): return str(value)
    if isinstance(value,dict): return {str(k):serializable(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [serializable(v) for v in value]
    return value


def certificate():
    finite = finite_audit()
    n = counts(additions=finite['additions'], outputs=finite['outputs'])
    bound, total, terms = Q(966,100), Q(0), 0
    while total <= n['m']:
        total += bound**terms / factorial(terms)
        terms += 1
        need(terms < 1000, 'Logarithm comparison failed')
    need(n['eta'] > COMPLEX_SAVING*bound, 'Complex saving is too large')
    small = symbolic_audit()
    proof_files = ['scripts/orthogonal_star.py','notes/orthogonal-star-construction.tex',
                   'notes/compact-control-movement.tex','notes/compact-control-layout.tex',
                   'notes/compact-control-guard.tex']
    return serializable(dict(
        status='CONDITIONAL ORTHOGONAL-STAR RESULT; INDEPENDENTLY RECONSTRUCTED FINITE IMPLEMENTATION; NOT FORMAL VERIFICATION',
        upstream_commit=verify_sources(), base_repository_commit=BASE_REPOSITORY_COMMIT,
        provenance='Aurel Prosz (Paureel), developed with ChatGPT and reconstructed/audited with Codex. The conversation ZIP was unavailable; this is the independently checked reconstruction, not a copy of that archive.',
        finite=finite, symbolic=small, counts=n, bit_saving=BIT_SAVING,
        complex_saving=COMPLEX_SAVING, log_upper=bound,
        log_certificate=dict(exp_positive_partial_sum=total,terms=terms),
        guard=guard_certificate(n), witness=parameter_certificate(),
        fixed_saving_supremum=min(BIT_SAVING,COMPLEX_SAVING)/(5+4*min(BIT_SAVING,COMPLEX_SAVING)),
        improvement_over_base=KAPPA/Q(83,10**12),
        proof_sha256={name:sha256((ROOT/name).read_bytes()).hexdigest() for name in proof_files},
        verification_boundary='Finite graph, scalar matrix, scratch frames and parameter inequalities checked exactly. General tape/layout/precision/assembly arguments are supplied in source. The retained original multiplication theorem is assumed, and no proof-assistant or complete multiplication-machine implementation is supplied.'))


if __name__ == '__main__':
    result = certificate()
    (ROOT/'certificates/orthogonal-star.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS conditional orthogonal-star witness:',KAPPA,'> 2^-31')
    print('Finite additions, outputs and scratch incidences:',result['finite']['additions'],
          result['finite']['outputs'],result['finite']['forward']+result['finite']['reverse'])
