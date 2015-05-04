#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import stderr, stdin, stdout
from argparse import ArgumentParser
from omorfi.omorfi import Omorfi

def print_analyses(surf, anals, format):
    if format == 'xerox':
        print_analyses_xerox(surf, anals)
    elif format == 'apertium':
        print_analyses_apertium(surf, anals)
    elif format == 'vislcg':
        print_analyses_vislcg(surf, anals)
    elif format == 'conllx':
        print_analyses_conllx(surf, anals)
    elif format == 'conllu':
        print_analyses_conllu(surf, anals)
    else:
        print("format unknown:", format, file=stderr)
        exit(2)

def print_analyses_xerox(surf, anals):
    for anal in anals:
        print(surf, anal.output, sep='\t')
    print

def print_analyses_apertium(surf, anals):
    print("^", surf, sep='')
    for anal in anals:
        print("/", anal.output, sep='')
    print("$")

def print_analyses_vislcg(surf, anals):
    print('"', surf, '"', sep='')
    for anal in anals:
        pos_matches = re_pos.finditer(anal.output)
        pos = "UNK"
        mrds = []
        lemmas = []
        for pm in pos_matches:
            pos = pm.group(1)
        lemma_matches = re_lemma.finditer(anal.output)
        for lm in lemma_matches:
            lemmas += [lm.group(1)]
        mrd_matches = re_mrd.finditer(anal.output)
        for mm in mrd_matches:
            if mm.group(1) == 'WORD_ID':
                mrds = []
            elif mm.group(1) == 'CASECHANGE' and mm.group(2) != 'NONE':
                mrds = ['<*>'] + mrds
            elif mm.group(1) == 'WEIGHT':
                mrds += ['<W=' + str(int(float(mm.group(2)) * 100)) + '>']
            elif mm.group(1) in ['STYLE']:
                mrds += ['<' + mm.group(2) + '>']
            else:
                mrds += [mm.group(2)]
        print('\t"', ''.join(lemmas).replace('"', '\\"'), '"\t',
                ' '.join(mrds), sep='', file=outfile)
    print

def print_analyses_conllx(surf, anals):
    print(1, surf, surf, anals[0].output[0], anals[0].output[0], anals[0].output,
            "-", "-", "-", "-", sep="\t")

def print_analyses_conllu(surf, anals):
    print(1, surf, surf, anals[0].output[0], anals[0].output[0], anals[0].output,
            "-", "-", "-", "-", sep="\t")

def main():
    """Invoke a simple CLI analyser."""
    a = ArgumentParser()
    a.add_argument('-f', '--fsa', metavar='FSAPATH',
            help="Path to directory of HFST format automata")
    a.add_argument('-i', '--input', metavar="INFILE", type=open,
            dest="infile", help="source of analysis data")
    a.add_argument('-v', '--verbose', action='store_true',
            help="print verbosely while processing")
    a.add_argument('-o', '--output', metavar="OUTFILE", 
            help="print factors into OUTFILE")
    a.add_argument('-f', '--format', metavar='FORMAT',
            help="Output in format compatible with FORMAT",
            choices=['xerox', 'apertium', 'vislcg3', 'conllx', 'conllu'])
    options = a.parse_args()
    omorfi = Omorfi(options.verbose)
    if options.fsa:
        omorfi.load_from_dir(options.fsa)
    else:
        omorfi.load_from_dir()
    if not options.infile:
        options.infile = stdin
    if options.verbose:
        print("reading from", options.infile.name)
    for line in options.infile:
        line = line.strip()
        if not line or line == '':
            continue
        surfs = omorfi.tokenise(line)
        for surf in surfs:
            anals = omorfi.analyse(surf)
            print(surf, end='')
            for anal in anals:
                print("\t", anal.output, sep='', end='')
            print()
    exit(0)

if __name__ == "__main__":
    main()