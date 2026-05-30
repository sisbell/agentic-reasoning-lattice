# Review of ASN-0042

## REVISE

### Issue 1: O7(c) misclassifies condition (i) as "automatic" and omits it from the binding obligations

**ASN-0042, Delegation / O7 proof (Postcondition (c)) and Formal Contract (c)**: the proof states "Condition (i) holds by the choice of `p''`" and then concludes "Conditions (i), (ii), and (iv) are thus automatic at `Σ'`. The binding obligations on `p''` are exactly (iii) [structural-tier] and (v) [fresh-valid]." The Formal Contract repeats: "binding obligations (iii) [structural-tier] and (v)."

**Problem**: This is internally contradictory and undercounts the obligations. Condition (i) is `pfx(π') ≺ p''`. The phrase "holds by the choice of `p''`" *is* the statement that `p''` must be chosen to satisfy it — i.e., (i) is a binding constraint on the choice, not an automatic consequence. Conditions (ii) and (iv) are the genuinely automatic ones, and even they are automatic only *given* (i): the derivation of (ii) ("π' is the most-specific covering principal of `p''`") presupposes `pfx(π') ≼ p''`, which is exactly (i). If (i) is dropped from the binding obligations, the contract reads as licensing `π'` to delegate any next-reachable fresh, structurally-valid prefix — including prefixes outside `odom(π')` — which contradicts the section's whole claim that delegation operates within the delegate's domain.

**Required**: List (i) [ancestry, `pfx(π') ≺ p''`] among the binding obligations on `p''` in both the proof and Formal Contract (c), and state that (ii) and (iv) are automatic *given* (i) and the original delegation's condition (iv). The set of free obligations on the choice of `p''` is (i), (iii), (v) — not (iii), (v) alone.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer and provenance/effective-owner divergence
The note repeatedly observes (O3 closing remark, O8 design note) that Nelson's "someone who has bought the document rights" implies transfer but the codebase has none. The invariants a transfer operation would have to preserve — and how inalienable provenance (O6) relates to effective ownership (O2) once they diverge — are correctly deferred to the first Open Question. Not an error here.

### Topic 2: Density of ownership domains (gaps between baptized siblings)
Whether `odom(π)` must be gap-free is raised as an Open Question and not assumed anywhere in the proofs. Future ASN territory.

META: (none — the ASN defines abstract ownership state, a delegation operation, and reachable-state invariants; Gregory references serve as corroboration, not as the specification's content, so it remains a system-guarantee spec.)

VERDICT: REVISE
