#!/usr/bin/env python3
"""Standalone pinned-manuscript derivative for the two-stage construction."""
import difflib
from pathlib import Path
from make_patch import replace_once
from make_orthogonal_star_patch import patched_files as star_files
from two_stage import parameter_certificate

ROOT=Path(__file__).resolve().parents[1]


def note(name): return (ROOT/'notes'/name).read_text()


def patched_files():
    parameter_certificate()
    for name,old,new in star_files():
        if name.endswith(('main.tex','00-introduction.tex')):
            new=new.replace(r'\kappa=591/10^{12}',r'\kappa=629/10^{11}')
            new=new.replace('orthogonal-star: Aurel Prosz','two-stage and orthogonal-star: Aurel Prosz')
            if name.endswith('main.tex'):
                new=replace_once(new,'The revised bound is conditional',
                    'The current two-stage extension replaces one tensor stage with a charged\n'
                    'rank-one correction, using a fresh reconstruction with a conservative\n'
                    'bit graph. The earlier network sections are retained for provenance.\n'
                    'The revised bound is conditional')
        elif name.endswith('03-motifs.tex'):
            marker='The exponents used from now on are'
            pos=new.index(marker)
            new=new[:pos]+note('two-stage-construction.tex')+'\n'+new[pos:]
            pos=new.index(marker)
            new=new[:pos]+new[pos:].replace(r'\tau=1-296/10^{11}',r'\tau=1-47/10^8').replace(
                r'\sigma=1-318/10^{11}',r'\sigma=1-3147/10^{11}')
        elif name.endswith('04-swap.tex'):
            marker=r'\subsection{Removing width and row restrictions}'
            pos=new.index(marker)
            new=new[:pos]+note('direct-swap-transfer.tex')+'\n'+new[pos:]
            pos=new.index(marker)
            new=new[:pos]+new[pos:].replace('prop:power-interchange','prop:two-stage-power-interchange')
        elif name.endswith('05-layers.tex'):
            new=new.replace('prop:orthogonal-star-interface','prop:two-stage-complex-interface')
            for a,b in ((r'm_{\rm c}=15625',r'm_{\rm c}=1156'),
                        (r'W_{\rm c}=7706397940000',r'W_{\rm c}=28546995136'),
                        (r's_{\rm c}=120412464109500000',r's_{\rm c}=33000319052800'),
                        (r'm_{\rm b}=125000',r'm_{\rm b}=1024'),
                        (r'\tau=1-296/10^{11}',r'\tau=1-47/10^8'),
                        (r'\sigma=1-318/10^{11}',r'\sigma=1-3147/10^{11}')):
                new=new.replace(a,b)
            start=new.index(r'\paragraph{The exact recursive contract.}')
            end=new.index(r'\paragraph{Returning to normalized butterflies.}',start)
            new=new[:start]+note('two-stage-phase-transfer.tex')+'\n'+r'''
\paragraph{The completed recursive contract.}
Apply the two-stage network and its charged copy correction to $e=mf$
selected axes. The total is exactly $s_c$ children, including $N$ endpoint
children, each of volume $V/W$ on $f$ axes. The diagonal weight-$9f$
correction and row merge give $C^{\otimes e}$ on every original role.
The fixed-tape parking schedule includes the retained originals while each
copy is processed. No additional logical roles or free address translations
are introduced. The scalar-node allowance below includes these operations.
''' +new[end:]
            new=new.replace(r'The source, sink and bank corrections take at most \(4W+4\) more.',
                r'The ordinary wrappers and charged copy corrections are covered by '
                r'$32(s+W+m+N+1)$ elementary operations per coefficient, in addition '
                r'to the explicitly counted $2v$ invocation schedules. Their sum is '
                r'less than $64(W+m+1)^3$ by the two-stage certificate.')
            new=replace_once(new,r'\label{sec:compact-stopped-guard}',r'''\label{sec:compact-stopped-guard}
For the replacement network, the two-stage copy corrections are covered by
$32(s+W+m+N+1)$ elementary operations per coefficient, in addition to
$2v[4(3A+O)+2v+2O+8hv]$ for its actual invocation schedules. Their sum
is less than $E=64(W+m+1)^3$, as checked exactly. Here $A,O$ denote the
finite graph's additions and outputs, and $s$ includes the $N$ correction
children. Copies and diagonal signs preserve complete coefficient encodings;
all scalar additions and fourth-root phases are paid within this allowance.
''')
        elif name.endswith('08-assembly.tex'):
            replacements={
                r'a=296/10^{11}':r'a=47/10^8',
                r'a_{\rm c}=318/10^{11}':r'a_{\rm c}=3147/10^{11}',
                r'\beta=\frac1{1000}':r'\beta=\frac1{10000}',
                r'\frac{49961}{10000}':r'\frac{49997}{10000}',
                r'49961/10000':r'49997/10000',
                r'\frac{1999}{10000}':r'\frac{199999}{1000000}',
                r'\delta=\frac1{10^6}':r'\delta=\frac1{10^8}',
                r'\frac{2959}{10^{12}}':r'\frac{31465}{10^{12}}',
                r'\frac{2958}{10^{12}}':r'\frac{31464}{10^{12}}',
                r'\frac{591}{10^{12}}>2^{-31}':r'\frac{629}{10^{11}}>2^{-28}',
                r'\max\{\sigma-\tau,0\}=\tau':r'\max\{\sigma-\tau,0\}',
                r'e^{1000}<d':r'e^{10000}<d',
                r'b^{1999/10000}':r'b^{199999/1000000}',
                r'd^{10000}\le b^{1999}':r'd^{1000000}\le b^{199999}',
                r'b^{15997/20000}':r'b^{1599997/2000000}',
                r'\frac{2956521}{5\cdot10^{15}}>\frac{591}{10^{12}}':r'\frac{786596067}{125000000000000000}>\frac{629}{10^{11}}',
                r'd^{49961/10000}':r'd^{49997/10000}',
                r'p^{11999/40000}':r'p^{1199999/4000000}',
                r'p^{15997/20000}':r'p^{1599997/2000000}',
                r'p^{1999/10000}':r'p^{199999/1000000}',
                r'p^{8001/10000}':r'p^{800001/1000000}',
                r'p^{3001/5000}':r'p^{300001/500000}',
            }
            for a,b in replacements.items(): new=new.replace(a,b)
        new=('% Modified by Aurel Prosz (Paureel), October 8, 2026.\n'
             '% Conditional two-stage reconstruction; all correction calls charged.\n'+new)
        yield name,old,new


if __name__=='__main__':
    patch=''.join(''.join(difflib.unified_diff(old.splitlines(keepends=True),
        new.splitlines(keepends=True),fromfile='a/'+name,tofile='b/'+name))
        for name,old,new in patched_files())
    (ROOT/'patches/two-stage-28.patch').write_text(patch)
    print('Wrote conditional two-stage patch: 6.29e-9 > 2^-28.')
