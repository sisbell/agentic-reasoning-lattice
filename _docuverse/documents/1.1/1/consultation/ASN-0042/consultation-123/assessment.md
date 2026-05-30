# Channel Assignment — ASN-0042 review-123

**Date:** 2026-05-30 05:27

## Issue 1: O7(c) imagines prospective states the claim's transition excludes
Reason: Purely internal editorial fix — the per-state behavior of conditions (ii)/(iv) is already fixed by their definitions in O15, and the claim's carrier is the single transition `Σ → Σ'`. Trimming the `Σ''` meditation requires no design intent or implementation evidence.

## Issue 2: Freshness of the delegate prefix is asserted/derived four times
Reason: Internal consolidation — condition (v)'s `next` semantics (via ASN-0040's `Bop` postcondition `next(s.B,p,d) ∉ s.B`) already supply freshness once; collapsing the redundant O18/Freshness-(v) re-derivations is a sourcing decision derivable from the ASN's own citation structure.

## Issue 3: O17b's "sharpened" clause duplicates delegation condition (v)
Reason: Internal — deciding which of O17b or condition (v) owns the "principal-introduction baptizes its prefix" fact is a normativity/single-source-of-truth choice fully determined by the ASN's existing axioms; no external channel resolves it.

## Issue 4: T4-discharge convention is use-site management prose
Reason: Internal deletion — O17 already states `a ∈ Σ.B ⟹ T4(a)`; removing the convention paragraph and inlining direct O17 citations is mechanical and self-contained.

## Issue 5: Properties table enumerates downstream consumers in a definition slot
Reason: Internal — dropping the parenthetical that names O17b's downstream consumers is a presentation fix; the dependencies are already recorded in O18's and Freshness-(v)'s own derivations within the ASN.

## Issue 6: Repeated defensive reachability-precondition parentheticals
Reason: Internal — removing defensive re-assertions of already-in-scope preconditions is pure prose cleanup, fully verifiable against the proofs' existing hypotheses without external input.
