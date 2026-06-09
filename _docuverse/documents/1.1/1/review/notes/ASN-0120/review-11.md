# Review of ASN-0120

## REVISE

### Issue 1: Reachability precondition carries a use-site inventory
**ASN-0120, "The substrate we build on" — Standing precondition (reachability)**: "This licenses the per-state invariant citations below — S0/S1 (content permanence), S2/S3 (arrangement functionality and referential integrity), S7 (structural attribution), L0–L14 and L12 (link structure and permanence), each of which the foundation ASNs guarantee only of reachable states."
**Problem**: The standing precondition is correct and necessary, but the sentence then enumerates the downstream invariants the assumption licenses — a use-site inventory. The list of consumers does not advance the precondition's meaning; it is the kind of "what this is needed for" accretion the anti-bloat pass targets.
**Required**: State the precondition (Σ ranges over reachable states) and stop. Drop the enumeration of which invariants it licenses; the citations stand on their own where used.

### Issue 2: ML2 duplicates ML1's load-bearing equation
**ASN-0120, Claims table, ML1 vs ML2**: ML1 states "coverage(e_j) ⊇ ρ(R_j,Σ) with coverage(e_j) ∩ dom(Σ.C) = ρ(R_j,Σ)"; ML2 states "coverage(e_j) ∩ dom(Σ.C) = ρ(R_j,Σ) regardless of I-space fragmentation — every referenced content address recovered, none spurious."
**Problem**: The formal content of ML2 is the identical set equation already asserted in ML1. The set equation holds *by definition* regardless of fragmentation (a set equality is not sensitive to how the spans decompose), so "regardless of I-space fragmentation" adds emphasis, not content. ML2's only genuinely new material is the meta-remark that span-set cardinality is not abstractly observable.
**Required**: Either fold ML2's distinct content (cardinality non-observability) into ML1's discussion, or restate ML2 so it carries a claim ML1 does not — otherwise it is two claims saying the same thing.

### Issue 3: Meta-prose on what is *not* observable, deferring to the implementation note
**ASN-0120, "What the endset arguments name…"**: "(How many spans the endset's representation happens to use to cover those addresses is *not* abstractly observable: the model exposes no span-positional accessor (ASN-0043, L5) and projection depends only on coverage, not decomposition (ASN-0098, LP21). The span-set cardinality is therefore a representation matter, left to the implementation note.)"
**Problem**: This is a paragraph about what the abstraction does *not* fix, ending in a forward defer to the implementation note. The observable guarantee (coverage-level faithfulness) is already stated; the negative-space essay about cardinality is meta-prose the reader must step past.
**Required**: State the positive guarantee once (coverage ∩ store = ρ). If the non-observability point is worth keeping, reduce it to a clause, not a parenthetical paragraph with its own citations.

### Issue 4: Open Question 4 is already answered by ML9 plus a foundation
**ASN-0120, Open Questions**: "What is the precise condition under which a newly created link is discoverable from no document, and what must be true for a later operation to bring it into discoverability without altering the link?"
**Problem**: The discoverable-from-no-document condition is the direct negation of ML9 (∀d', ∀i : ρ(R_i,Σ) ∩ ran(Σ.M(d')) = ∅), and "bringing it into discoverability without altering the link" is exactly ASN-0098 LP17 (GhostProjection / orphaning) and LP18 (Resurrection), a foundation. Posing it as open territory is redundant with the ASN's own ML9 and a verified foundation.
**Required**: Either remove the question or reframe it to ask something ML9 + ASN-0098 do not already settle.

## OUT_OF_SCOPE

### Topic 1: Links with ghost (non-content) type endsets
**Why out of scope**: ML6 requires the type argument to ρ-resolve into `dom(Σ.C)`, so MAKELINK as specified cannot mint the ghost-typed links that ASN-0043 L9 (TypeGhostPermission) permits. This is a consistent restriction (a subset of permitted links), not an error — but an operation that admits a raw-address type endset is new territory for a future ASN, not a gap in this one.

VERDICT: REVISE
