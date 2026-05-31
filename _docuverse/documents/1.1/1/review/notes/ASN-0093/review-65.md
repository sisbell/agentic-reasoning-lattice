# Review of ASN-0093

I worked through the invariant discharges, the sub-allocator chain machinery, the freshness lemmas, and the cross-document disjointness argument, and traced the worked example. The substrate is structurally sound: the zero-separator construction keeps documents (`zeros=2`), content, and links (`zeros=3`) provably non-colliding, the freshness lemmas correctly split into within-/cross-document and cross-subspace cases, and the simultaneous induction has no vicious circularity. The findings below are about accumulated redundancy and defensive prose, which this note is explicitly flagged to surface.

## REVISE

### Issue 1: SD is a transition-independent invariant forced into three redundant matrix cells
**ASN-0093, Discharge of stated invariants, the SD row of the per-(invariant, transition) matrix**: K.σ — "Static at Σ': SD follows pointwise from L0 and StoreT4Validity at Σ' via T7"; K.α — "Static at Σ': same pointwise discharge as the K.σ cell …"; K.λ — "Static at Σ': same pointwise discharge as the K.σ cell …".
**Problem**: SD does not depend on which transition fired — by the note's own framing it is a static consequence of L0 + StoreT4Validity at Σ' via T7. Placing it in a per-transition matrix produces three cells stating the identical discharge, two of which only back-reference the first. This is the "two paragraphs say the same thing in different words" pattern, here as triplicated matrix cells; a precise reader reads the same static argument three times and must confirm the back-references add nothing.
**Required**: Lift SD out of the per-transition matrix into a single static-discharge statement ("SD holds at any Σ' satisfying L0 and StoreT4Validity, via T7"), and drop the three matrix cells.

### Issue 2: StoreT4Validity duplicates a T4-validity result that C1c/L1c already certify
**ASN-0093, Corollary (StoreT4Validity)**: "For any `a ∈ dom(C)`, ChainMembershipForOrigin places `a ∈ A_C(origin(a))` … By ChainElementT4Validity, every element of `A_C(origin(a))` is T4-valid; hence `a` is T4-valid."
**Problem**: C1c (and L1c) already assert that every store entry has a T10a-conforming chain from its T4-valid document seed whose steps preserve T4 — which is exactly T4-validity of the terminus by T10a.4. So T4-validity of store entries is established twice through two separate apparatus (C1c/L1c + T10a.4 on one path; ChainMembershipForOrigin + ChainElementT4Validity on the other). The ChainMembership route does no work that C1c/L1c don't already do for the T4 conclusion (ChainMembershipForOrigin is still independently needed for the freshness lemmas, but not for this corollary).
**Required**: Derive StoreT4Validity directly from C1c/L1c + T10a.4 in one line, or state explicitly why the heavier ChainMembership route is preferred over the available C1c/L1c route.

### Issue 3: C1c and L1c carry a duplicated defensive gloss restating T10a admissibility
**ASN-0093, C1c (ContentAllocatorConformance) and L1c (LinkAllocatorConformance)**: both read "each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfies T10a's per-step admissibility constraints (T4-validity preservation, including the `kᵢ = 2 ⟹ zeros(tᵢ₋₁) ≤ 2` zero-count side condition)".
**Problem**: The parenthetical "(T4-validity preservation, including the `kᵢ = 2 ⟹ zeros(tᵢ₋₁) ≤ 2` …)" restates content that "T10a's per-step admissibility constraints" already names — it re-spells TA5a's zero-count bound inline. It is a defensive gloss on a foundation reference, and it appears verbatim in both C1c and L1c. The Discharge section's chain exhibitions re-derive per-step admissibility with explicit TA5a citations, so the inline gloss carries no load.
**Required**: Drop the parenthetical from both C1c and L1c, leaving "satisfies T10a's per-step admissibility constraints"; the side condition lives in TA5a/T10a and is re-cited where actually discharged.

## OUT_OF_SCOPE

### Topic 1: No invariant forbids a future K.σ document from nesting inside another document's element/content subtree
The substrate is in fact safe here (a `zeros=2` tumbler cannot be a proper extension of a `zeros=3` content/link prefix, since extension never decreases the zero count), and the worked example exercises the `d ≺ d'` case. Stating a document-vs-content-subtree non-collision invariant explicitly belongs to a higher-layer allocation-policy ASN, not a correction here.

VERDICT: REVISE
