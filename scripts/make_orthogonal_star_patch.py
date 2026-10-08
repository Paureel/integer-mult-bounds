#!/usr/bin/env python3
"""Pinned-source derivative for Paureel's reconstructed orthogonal-star bound."""
import difflib
from pathlib import Path

from make_compact_control_patch import patched_files as compact_files
from make_patch import replace_once
from orthogonal_star import parameter_certificate

ROOT = Path(__file__).resolve().parents[1]


def patched_files():
    parameter_certificate()
    for name, old, new in compact_files():
        if name.endswith(('main.tex', '00-introduction.tex')):
            new = new.replace(r'\kappa=83/10^{12}', r'\kappa=591/10^{12}')
            if name.endswith('main.tex'):
                new = new.replace('Douglas Colkitt (modifications)',
                                  'Douglas Colkitt and Aurel Prosz (modifications)')
                new = new.replace(r'\small Compact-control modifications: Douglas Colkitt}',
                    r'\small Compact-control: Douglas Colkitt; orthogonal-star: Aurel Prosz}')
                new = new.replace('modified: October 7, 2026', 'modified: October 8, 2026')
                new = replace_once(new, 'The revised bound is conditional',
                    'It also includes Aurel Prosz\'s orthogonal-star complex network, developed\n'
                    'with ChatGPT and independently reconstructed and audited with Codex.\n'
                    'The revised bound is conditional')
        elif name.endswith('03-motifs.tex'):
            marker = 'The exponents used from now on are'
            pos = new.index(marker)
            new = new[:pos] + (ROOT/'notes/orthogonal-star-construction.tex').read_text() + '\n' + new[pos:]
            pos = new.index(marker)
            new = new[:pos] + new[pos:].replace(r'\sigma=1-418/10^{12}', r'\sigma=1-318/10^{11}')
        elif name.endswith('05-layers.tex'):
            new = new.replace('prop:compact-complex-interface', 'prop:orthogonal-star-interface')
            new = replace_once(new, 'W=W_{\\rm c}=58645352620000', 'W=W_{\\rm c}=7706397940000')
            new = replace_once(new, 's=s_{\\rm c}=916333630984500000', 's=s_{\\rm c}=120412464109500000')
            new = replace_once(new, r'$\sigma=1-418/10^{12}$', r'$\sigma=1-318/10^{11}$')
        elif name.endswith('08-assembly.tex'):
            new = replace_once(new, '$a_{\\rm c}=418/10^{12}$', '$a_{\\rm c}=318/10^{11}$')
            new = replace_once(new, r'c=\frac15', 'c=1')
            new = replace_once(new, r'\lambda=1-\frac{1671}{4\cdot10^{12}}', r'\lambda=1-\frac{2959}{10^{12}}')
            new = replace_once(new, r"\lambda'=1-\frac{167}{4\cdot10^{11}}", r"\lambda'=1-\frac{2958}{10^{12}}")
            new = replace_once(new, r'\kappa=\frac{83}{10^{12}}>2^{-34}', r'\kappa=\frac{591}{10^{12}}>2^{-31}')
            new = replace_once(new, r'\chi=\tau+(1-\beta)(\sigma-\tau)',
                r'\chi=\tau+(1-\beta)\max\{\sigma-\tau,0\}=\tau')
            new = replace_once(new, r'\frac{333833}{4\cdot10^{15}}>\frac{83}{10^{12}}',
                r'\frac{2956521}{5\cdot10^{15}}>\frac{591}{10^{12}}')
            new = replace_once(new, r'K=\Theta(p^{1999/50000})', r'K=\Theta(p^{1999/10000})')
        new = ('% Modified by Aurel Prosz (Paureel), October 8, 2026.\n'
               '% Independently reconstructed conditional orthogonal-star result.\n' + new)
        yield name, old, new


if __name__ == '__main__':
    patch = ''.join(''.join(difflib.unified_diff(old.splitlines(keepends=True),
        new.splitlines(keepends=True), fromfile='a/'+name, tofile='b/'+name))
        for name, old, new in patched_files())
    (ROOT/'patches/orthogonal-star-31.patch').write_text(patch)
    print('Wrote independent conditional orthogonal-star patch; kappa=591/10^12 > 2^-31.')
