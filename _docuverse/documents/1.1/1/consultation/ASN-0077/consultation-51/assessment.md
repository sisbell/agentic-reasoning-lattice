# Channel Assignment — ASN-0077 review-51

**Date:** 2026-06-03 22:26

## Issue 1: Defensive "no transition-vocabulary closure" prose restated four times
Reason: Pure editorial deletion — collapse four echoing disclaimers into one citation of L1c + Allocator hierarchy + SubAllocatorBundle. The citation basis is already present in the ASN; nothing about design intent or implementation is at stake.

## Issue 2: Transition-vocabulary inventories enumerated, then disclaimed
Reason: The binary modifies-M(d)/fixes-M(d) partition is already stated and load-bearing; the vocabulary inventories are self-declared non-load-bearing. Deletion is internal to the ASN's own argument structure.

## Issue 3: Downstream-consumer justifications for stating claims separately
Reason: Removing use-site rationale prose is purely editorial; whether a claim is labeled has no bearing on the argument and needs no external input.

## Issue 4: Repeated deferral to the worked example and to LP10/LP11
Reason: Deduplication of internal cross-references — the worked-example deferral and the LP10/LP11 (ASN-0098) correspondence are already stated in the ASN; the fix only collapses repetition to a single instance each.

## Issue 5: O11★ and O11'★ are strict special cases of O11★★
Reason: The subsumption is a logical fact internal to the ASN — O11★★'s mixed-chain induction specializes to pure-K.μ⁺ and pure-K.μ⁺_L chains by restricting the per-step case set. No design or implementation evidence is needed to derive the narrower lemmas as one-line specializations.

## Issue 6: O2 derivation explains a citation choice instead of arguing
Reason: The collapse step follows from O2 directly, already proved in the ASN; deleting the M16a meta-contrast is a self-contained editorial fix.
