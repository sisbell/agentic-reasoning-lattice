# Review of ASN-0082

This note carries the anti-bloat classifier. The mathematics is sound — I checked the contraction engine (OrdinalExceedsDisplacement → D-BJ/D-SEP/D-DP → D-CTG-post/D-SEQ-post), the insertion consistency argument, and both span-width derivations (I3-S, D-S) against their cited foundation lemmas and the worked examples; all discharge correctly, including the verbose depth-1 ℕ-subtraction identity in D-S(a). The findings below are meta-prose accretion, which is what this cycle is scoped to catch.

## REVISE

### Issue 1: Use-site inventory in OrdinalExceedsDisplacement
**ASN-0082, OrdinalExceedsDisplacement (paragraph after the lemma statement)**: "The `#v = 2` hypothesis stands as a precondition; consumers discharge it at their own sites. For the endpoint instantiation `v = r` — where `r` need not lie in `dom(M(d))` — the result-length identity gives `#r = #w = #p = 2` directly."
**Problem**: The lemma already states `#v = 2` as an explicit precondition. This paragraph narrates *who* discharges it downstream (the "consumers discharge at their own sites" / "endpoint instantiation `v = r`" material is the D-S use-site pre-explained at the definition site). This is exactly the use-site-inventory pattern: prose that points at downstream consumers rather than advancing the lemma's meaning. The git log shows OrdinalExceedsDisplacement was just trimmed for verbosity; this is residue.
**Required**: Delete the paragraph. The `#v = 2` precondition speaks for itself; D-S can establish `#r = 2` via the result-length identity at its own site without a forward note here.

### Issue 2: Duplicate Statement Registry rows for associativity
**ASN-0082, Statement Registry**: two rows — `ℕ assoc | derived | ℕ addition associativity (a + b) + k = a + (b + k) for positive b, k — supplied by TA-assoc specialized to depth-1 tumblers` and `TA-assoc | lemma | (a ⊕ b) ⊕ c = a ⊕ (b ⊕ c) ... | cited (ASN-0034)`.
**Problem**: The `ℕ assoc` row records nothing the `TA-assoc` row does not — it is the same foundation lemma specialized at depth 1, used once in D-S(a). Two registry entries for one cited fact is duplication.
**Required**: Drop the `ℕ assoc` row; the depth-1 specialization is already explained inline in the D-S derivation.

### Issue 3: Method-rationale prose in D-S derivation
**ASN-0082, D-S derivation of (a)**: "Because ASN-0034's NAT-* extraction supplies no ℕ-subtraction law, we discharge this single-component identity through the depth-1 tumbler lemmas."
**Problem**: This sentence explains *why the proof is structured the way it is* rather than performing a step — it pre-empts a "why not just use arithmetic?" objection. Under anti-bloat this is justification-of-structure prose. The ReverseInverse/TA-assoc/TA4 chain that follows is self-evidently the argument; the reader does not need the editorial framing.
**Required**: Remove the sentence and lead directly with "Write `x = s₂ − c`, i.e. `[x] = [s₂] ⊖ [c]`. ReverseInverse at depth 1 gives…".

## OUT_OF_SCOPE

The depth-greater-than-one generalization (gap-closure, dense partition, the TA4 zero-prefix collision with S8a positivity) is correctly deferred to the Open Questions rather than attempted here; no action needed.

VERDICT: REVISE
