# Channel Assignment — ASN-0121 review-7

**Date:** 2026-06-09 01:40

## Issue 1: "span denotes a contiguous subtree (T5)" miscites the foundation
Reason: Pure citation correction internal to the foundation already in scope — restrict the claim to prefix spans, cite PrefixSpanCoverage (ASN-0043) for the span-equals-subtree identity and T5 only for convexity. No design intent or implementation evidence is in question; both lemmas and their precise content are foundation facts the ASN already invokes.

## Issue 2: FL-MON's value-preservation step needs the multi-step persistence lemma, not single-step L12
Reason: Pure citation refinement — replace bare "immutability" with LP13 (ASN-0098) for `Σ'.L(a) = Σ.L(a)` across `Σ →* Σ'`, matching the precision the proof already applies to the domain conjunct via StoreMonotonicity★. The needed lemma is named in the foundation the ASN relies on; no channel is required.
