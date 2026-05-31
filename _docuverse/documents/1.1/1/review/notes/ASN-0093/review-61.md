# Review of ASN-0093

## REVISE

### Issue 1: Base case misclassifies M1 as a domain-quantified invariant

**ASN-0093, Discharge of stated invariants, "Base case verification"**: "Most invariants are vacuously satisfied: M0/M1/M2/C1/C1b/C1c/C2/L0/L1/L1a/L1b/L1c/L3 quantify over `dom(C)`, `dom(L)`, or `dom(M)`, all empty at Σ₀. C0 and L12 quantify over transitions Σ → Σ', vacuous at Σ₀ until the first transition fires."

**Problem**: M1 (ArrangementMonotonicity) is `(A Σ → Σ' :: dom(M) ⊆ dom(M'))` — it quantifies over *transitions*, exactly like C0 and L12, not over members of `dom(M)`. Grouping M1 with the domain-quantified invariants and justifying its base-case vacuity by "quantify over dom(M)... all empty at Σ₀" is wrong on two counts: M1 is not a membership predicate over `dom(M)`, and its base-case status (vacuous until the first transition) is the C0/L12 reason, not the empty-domain reason. The stated justification does not actually discharge M1.

**Required**: Move M1 into the transition-quantified group with C0 and L12 ("vacuous at Σ₀ until the first transition fires"), and remove it from the domain-quantified list.

### Issue 2: Anchor-exclusion paragraph cites C1 for a `#E ≥ 2` claim that C1 does not make

**ASN-0093, Address sub-allocators under documents**: "The anchors themselves are *not* in `dom(C) ∪ dom(L)` — content and link addresses have `#E ≥ 2` (C1; L1b above), and the anchors have `#E = 1`."

**Problem**: C1 (ContentElementLevel) states `zeros(a) = 3`, not `#E(a) ≥ 2`. The content-side `#E ≥ 2` property is C1b (ContentElementFieldDepth). The citation `(C1; L1b above)` therefore misattributes the content half of the claim — C1 establishes element-level-ness, not element-field depth. The link half (L1b) is correct.

**Required**: Replace the content citation with C1b: `(C1b; L1b above)`.

## OUT_OF_SCOPE

None. The deferred topics (arrangement mutation, entity stratification, provenance, coupling, link withdrawal) are correctly routed to higher-layer ASNs in the Scope section, and the Open Questions raise design questions without smuggling in claims.

VERDICT: REVISE
