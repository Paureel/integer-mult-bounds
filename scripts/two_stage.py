"""Independent, exact reconstruction of Paureel's two-stage proof draft.

The conversation archive was unavailable. In particular its smaller bit
graph is not reproduced: the bundled generator uses R=123157, and a weaker
bit saving. This still supports the same final conditional kappa. Acceptance
checks here use explicit exceptions and remain active under python -O.
"""
from dataclasses import replace
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from math import comb, factorial, log2
from pathlib import Path
import json

from certify import Parameters, constraints, margins, verify_sources
from paired_network import circuit
from orthogonal_star import finite_audit, construct, need, serializable

ROOT = Path(__file__).resolve().parents[1]
BIT_SAVING = Q(47, 10**8)
COMPLEX_SAVING = Q(3147, 10**11)
KAPPA = Q(629, 10**11)


def counts(h, roles, complex_case=False):
    v, m, c0 = comb(h, 3), h*h, h+int(complex_case)
    N = v*v
    W = 2*N+2*v*(roles+c0)
    L = 2*v*h*c0
    edge = W*m-2*N+2*L
    s = edge+N
    need(W*m-s == v*(v-4*h*c0), 'Incorrect charged deficit')
    need(0 < s < W*m, 'No positive saving')
    return dict(h=h,v=v,m=m,N=N,R=roles,c0=c0,W=W,L=L,
                edge_calls=edge,correction_calls=N,s=s,deficit=W*m-s,
                eta=Q(W*m-s,W*m))


def bit_audit(h=32):
    c = circuit(h)
    # Check the actual supports even with assertions disabled in inherited code.
    local = c.local
    for node in sorted(local.active):
        if local.args[node]:
            a,b = local.args[node]
            need(a<node and b<node, 'Pair graph is not acyclic')
            need(not local.support[a]&local.support[b], 'Pair sum overlaps')
            need(local.support[node] == local.support[a]|local.support[b],
                 'Wrong pair sum')
    for (a,b),node in local.outputs.items():
        expected=sum(1<<i for i,p in enumerate(local.inputs) if a not in p and b not in p)
        need(local.support[node]==expected,'Wrong pair exclusion output')
    for node in sorted(c.active):
        if c.args[node]:
            a,b=c.args[node]; common,ln=c.provenance[node]
            A,B=c.support_in(a,common),c.support_in(b,common)
            need(a<node and b<node and not A&B,'Invalid shared sum')
            need(A|B==local.support[ln],'Wrong shared support')
            need(c.core[node]==c.core[a]&c.core[b] and
                 c.union[node]==c.union[a]|c.union[b],'Wrong shared provenance')
        need(c.core[node]!=0,'Source span has no common point')
    for (common,target),node in c.outputs.items():
        excluded=tuple(c.points[common].index(x) for x in target if x!=common)
        need(c.support_in(node,common)==local.support[local.outputs[excluded]],
             'Wrong triple exclusion output')
    code=c.compile()
    need(code['roles']==c.additions+len(c.outputs),'Wrong bit role count')
    state=[0]*code['roles']
    for t,slot in code['sources'].items(): state[slot]=c.variables[t]
    for node,ins,outs in code['gates']:
        need(len(set(ins))==len(ins) and set(ins)&set(outs)=={ins[0]},'Aliased bit gate')
        for slot in set(ins+outs):
            need(not state[slot] or c.contained(state[slot],node),'Bit forward decrease')
            state[slot]=node
    for target,slot in code['outputs'].items():
        need(state[slot]==c.outputs[target],'Wrong bit output frame')
    reverse=[0]*code['roles']
    for target,slot in code['outputs'].items(): reverse[slot]=c.outputs[target]
    for node,ins,outs in reversed(code['gates']):
        for slot in set(ins+outs):
            need(not reverse[slot] or c.contained(node,reverse[slot]),'Bit reverse decrease')
            reverse[slot]=node
    for t,slot in code['sources'].items():
        need(reverse[slot]==c.variables[t],'Wrong reverse endpoint frame')
    result=c.verify()
    result['explicit_checks_survive_optimization']=True
    if h==32:
        need(result['additions']==108277 and result['roles']==123157,
             'Unexpected independently generated bit graph')
    return result


def logarithm_certificate(n, saving, upper):
    total=Q(0)
    for k in range(1000):
        total += upper**k/factorial(k)
        if total>n['m']: break
    need(total>n['m'],'Taylor bound did not certify log(m)')
    slack=n['eta']-saving*upper
    need(slack>0,'Unsupported finite saving')
    return dict(log_upper=upper,taylor_terms=k+1,exp_partial_sum=total,
                deficit_slack=slack,saving=saving)


def parameters():
    return Parameters(tau=1-BIT_SAVING,sigma=1-COMPLEX_SAVING,
        epsilon=Q(199999,10**6),c=Q(1),beta=Q(1,10000),delta=Q(1,10**8),
        lam=1-Q(31465,10**12),lamp=1-Q(31464,10**12),
        kappa=KAPPA,C1=Q(49997,10000))


def parameter_certificate(p=None):
    p=p or parameters()
    need(0<1-p.tau<=BIT_SAVING,'Unsupported reconstructed bit saving')
    need(0<1-p.sigma<=COMPLEX_SAVING,'Unsupported complex saving')
    zeta=Q(1,10000)
    need(p.C1==5-4*p.beta+zeta,'Wrong stopped guard')
    chi=p.tau+(1-p.beta)*max(p.sigma-p.tau,Q(0))
    slacks=constraints(p,layout_model='nonadjacent',assembly_model='tight-gaussian')
    slacks['packed_overhead']=p.lam-chi
    slacks['reserved_axes']=p.lamp-max(Q(0),1-p.c)
    for name,value in slacks.items(): need(value>0,'Failed strict condition: '+name)
    gs=margins(p,layout_model='nonadjacent',assembly_model='tight-gaussian')
    need(min(gs.values())>p.kappa,'No strict absorption gap')
    return dict(parameters=vars(p),zeta=zeta,internal_exponent=chi,
                constraint_slacks=slacks,margins=gs,
                minimum_margin=min(gs.values()),absorption_gap=min(gs.values())-p.kappa)


def guard_certificate(n, additions, outputs):
    m,W,s=n['m'],n['W'],n['s']
    need(m>=3 and 2<=s<m**5,'Complex stopped-depth hypothesis fails')
    per=4*(3*additions+outputs)+2*n['v']+2*outputs+8*n['h']*n['v']
    scalar=2*n['v']*per
    # Copy, add, signs and phases for the N corrections, plus ordinary
    # inverse-child and endpoint wrappers, are included in this allowance.
    total=scalar+32*(s+W+m+n['N']+1)
    E=64*(W+m+1)**3
    need(total<E,'Uncharged coefficient operations')
    B=s+E;zeta=Q(1,10000)
    raw=max(Q(128*m*B*B),18*m*B*B*(1+1/zeta))
    C0=-(-raw.numerator//raw.denominator)
    need(s*(8+E)<=9*B*B,'Single-call depth charge fails')
    need(9*m*B*B*(1+1/zeta)+18<=C0,'Whole-layer depth charge fails')
    return dict(s_below_m_fifth=True,E=E,B=B,C0=C0,C1=parameters().C1,
                scalar_updates_upper=scalar,total_node_updates_upper=total,
                correction_copy_and_wrappers_included=True)


def scalar_audit(h=6, complex_case=False):
    """Full two-stage linear map, including every arbitrary scratch input."""
    if complex_case:
        triples,masks,groups=construct(h)
        programs=[]
        for g in groups:
            programs.append(dict(roles=g.code['roles'],
                gates=[(ins,outs) for _,ins,outs in g.code['gates']],
                sources=list(g.code['sources'].items()),
                outputs=[(g.outputs[q][0],slot,g.outputs[q][1])
                         for q,slot in g.code['outputs'].items()]))
    else:
        c=circuit(h);triples=c.inputs;p=c.program()
        programs=[dict(roles=p['roles'],gates=p['gates'],sources=p['sources'],
                       outputs=[(target,slot,Q(1)) for target,slot in p['outputs']])]
    v=len(triples);N=v*v;c0=h+int(complex_case)
    size=2*N+2*v*(sum(p['roles'] for p in programs)+c0)
    forms=[{i:Q(1)} for i in range(size)]
    def add(t,s,scale=Q(1)):
        value=dict(forms[t])
        for key,coef in forms[s].items():
            x=value.get(key,Q(0))+scale*coef
            if not complex_case: x=Q(x.numerator%2)
            if x: value[key]=x
            else: value.pop(key,None)
        forms[t]=value
    def mixer(p,offset,backwards=False):
        gates=reversed(p['gates']) if backwards else p['gates']
        for ins,outs in gates:
            pivot=offset+ins[0]
            if backwards:
                for slot in reversed(outs[1:]): add(offset+slot,pivot,-1)
                if len(ins)==2: add(pivot,offset+ins[1],-1)
            else:
                if len(ins)==2: add(pivot,offset+ins[1])
                for slot in outs[1:]: add(offset+slot,pivot)
    next_slot=2*N
    for stage in (0,1):
        for fixed in range(v):
            X=[i*v+fixed if stage==0 else fixed*v+i for i in range(v)]
            Y=[N+i for i in X]
            src,dst=(X,Y) if stage==0 else (Y,X)
            centers=next_slot;next_slot+=c0
            placed=[]
            for p in programs:
                placed.append((p,next_slot));next_slot+=p['roles']
            schedule=[('mix',1),('inject',-1),('mix',-1),('scatter',-1),
                      ('copy',1),('gather',1),('scatter',1),('mix',1),
                      ('inject',1),('mix',-1),('gather',-1),('copy',-1)]
            if stage: schedule=[(op,-sign) for op,sign in reversed(schedule)]
            for op,sign in schedule:
                if op=='mix':
                    for p,offset in placed: mixer(p,offset,sign<0)
                elif op=='copy':
                    for p,offset in placed:
                        for i,slot in p['sources']: add(offset+slot,src[i],sign)
                elif op=='inject':
                    for p,offset in placed:
                        for i,slot,coefficient in p['outputs']:
                            add(dst[i],offset+slot,sign*coefficient)
                elif op=='gather':
                    for i,t in enumerate(triples):
                        for j in t: add(centers+j,src[i],sign)
                        if complex_case: add(centers+h,src[i],sign)
                else:
                    for i,t in enumerate(triples):
                        for j in t: add(dst[i],centers+j,Q(sign,2) if complex_case else sign)
                        if complex_case: add(dst[i],centers+h,Q(-sign,2))
    need(next_slot==size,'Missing scalar roles')
    for i,form in enumerate(forms):
        expected={i:Q(1)}
        if i<N: expected={N+i:Q(-1 if complex_case else 1)}
        elif i<2*N: expected={i:Q(1),i-N:Q(1)}
        need(form==expected,f'Two-stage scalar map failure at role {i}')
    return dict(h=h,independent_input_variables=size,all_scratch_restored=True,
                full_two_stage_map_exact=True)


# Gaussian rationals as pairs: every endpoint identity is checked exactly.
def gadd(a,b): return (a[0]+b[0],a[1]+b[1])
def gmul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
ONE=(Q(1),Q(0)); I=(Q(0),Q(1)); ZERO=(Q(0),Q(0))
def scale(v,c): return [gmul(x,c) for x in v]
def c_line(v,mask,inverse=False):
    a=(Q(1,2),Q(-1 if inverse else 1,2))
    b=(Q(1,2),Q(1 if inverse else -1,2))
    return [gadd(gmul(a,x),gmul(b,v[i^mask])) for i,x in enumerate(v)]
def full_phase(v,dimension):
    for i in range(dimension): v=c_line(v,1<<i)
    return v
def diagonal(v,mask):
    return [gmul(x,(Q(-1 if (i&mask).bit_count()%2 else 1),Q(0)))
            for i,x in enumerate(v)]


def complex_endpoint_audit(dimensions=(1,3,5,9)):
    checked=0
    for d in dimensions:
        mask=(1<<d)-1
        phase=ONE
        for _ in range(d): phase=gmul(phase,I)
        for source in range(1<<d):
            x=[ZERO]*(1<<d);x[source]=ONE
            F=full_phase(x,d)
            # y input: A=-F y, B=E y. Adding P^-1 A cancels B.
            E=c_line(F,mask,inverse=True)
            correction=c_line(scale(F,(-Q(1),Q(0))),mask,inverse=True)
            need(all(gadd(a,b)==ZERO for a,b in zip(E,correction)),
                 'Complex cross-term survives')
            # x input: pre-sign Z, B=F X_w Zx, post i^wt(w) Z.
            z=diagonal(x,mask)
            translated=[z[i^mask] for i in range(1<<d)]
            corrected=scale(diagonal(full_phase(translated,d),mask),phase)
            need(corrected==F,'Complex endpoint sign correction fails')
            checked+=2
    return dict(basis_inputs=checked,dimensions=list(dimensions),
                cross_term_cancels=True,diagonal_endpoint_exact=True)


def reflection_audit():
    checked=0
    # One early/later interchange implements the upper reflection block.
    for modulus in (3,5,9,25):
        for t in range(1,modulus):
            if __import__('math').gcd(t,modulus)!=1: continue
            inv=pow(t,-1,modulus)
            for x in range(modulus):
                for y in range(modulus):
                    a,b=x,(x+t*y)%modulus
                    a,b=b,a
                    b=(a-b)*inv%modulus;a=-a%modulus
                    need((a,b)==((-x-t*y)%modulus,y),'One-swap reflection fails')
                    checked+=1
    # Address frames for a non-coordinate rational line v=(1,1), G=I.
    # A one-hot bit at each address checks the array-permutation composition.
    for q in (3,5):
        for h0,h1,d0,d1 in __import__('itertools').product(range(q),repeat=4):
            x=(h0,h1,d0,d1)
            def P(a):
                t=(a[2]+a[3]-a[0]-a[1])*pow(2,-1,q)%q
                return ((a[0]+t)%q,(a[1]+t)%q,(a[2]-t)%q,(a[3]-t)%q)
            def F(a): return (a[2],a[3],a[0],a[1])
            E=F(P(x))
            PF=P(F(x))
            need(PF==E,'Partial-swap cross-term fails')
            PP=P(P(x))
            need(PP==x,'Partial swap is not involutory')
            checked+=1
    return dict(exact_modular_address_cases=checked,prime_powers=[3,5,9,25],
                one_recursive_swap_block_exact=True,partial_swap_endpoints_exact=True)


def certificate():
    bit=bit_audit(); complex_graph=finite_audit(34)
    need(complex_graph['roles']==2379258,'Complex graph does not match latest claim')
    b=counts(32,bit['roles']); c=counts(34,complex_graph['roles'],True)
    p=parameter_certificate()
    proof_files=['scripts/two_stage.py','notes/two-stage-construction.tex',
                 'notes/direct-swap-transfer.tex','notes/two-stage-phase-transfer.tex',
                 'notes/compact-control-movement.tex','notes/compact-control-layout.tex',
                 'notes/compact-control-guard.tex']
    return serializable(dict(status='CONDITIONAL TWO-STAGE RESULT; INDEPENDENT RECONSTRUCTION; NOT FORMAL VERIFICATION',
        upstream_commit=verify_sources(),base_fork_commit='43a5ec5d6718a017e139fcc8ea089c59e58f609d',
        provenance='Aurel Prosz (Paureel), developed with ChatGPT and reconstructed with Codex. Cloud ZIP unavailable. The bundled bit generator has more roles; its weaker certified saving suffices for the same kappa.',
        bit_graph=bit,complex_graph=complex_graph,bit_counts=b,complex_counts=c,
        bit_log=logarithm_certificate(b,BIT_SAVING,Q(6932,1000)),
        complex_log=logarithm_certificate(c,COMPLEX_SAVING,Q(705273,100000)),
        parameters=p,guard=guard_certificate(c,complex_graph['additions'],complex_graph['outputs']),
        bit_scalar=scalar_audit(),complex_scalar=scalar_audit(7,True),
        bit_address=reflection_audit(),complex_endpoint=complex_endpoint_audit(),
        fixed_saving_supremum=COMPLEX_SAVING/(5+4*COMPLEX_SAVING),
        proof_sha256={f:sha256((ROOT/f).read_bytes()).hexdigest() for f in proof_files},
        scope='Exact finite graph, scalar, address and arithmetic audits plus written general frame, reflection, copy, endpoint and tape proofs. Retained upstream theorem and compact-control arguments remain assumptions; no independent expert or proof-assistant review or full multiplication implementation.'))


if __name__=='__main__':
    result=certificate()
    (ROOT/'certificates/two-stage.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS conditional two-stage:',float(KAPPA),'~ 2^(-'+format(-log2(float(KAPPA)),'.6f')+')')
    print('Complex finite audit:',result['complex_graph'])
