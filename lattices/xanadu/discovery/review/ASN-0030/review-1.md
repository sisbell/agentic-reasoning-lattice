# Review of ASN-0030

## REVISE

### Issue 1: A7a contradicts A8
**ASN-0030, Link Integrity / Ghost Domain**: A7a states unconditionally `(A a ∈ endset(L) : a ∈ dom(Σ'.I))`. A8 states "A link may reference an address `a` where `a ∉ dom(Σ.I)`" and defines `ghost(a) ≡ a ∉ dom(Σ.I) ∧ T4(a)`.

**Problem**: These are contradictory. A ghost link has endset addresses not in `dom(Σ.I)`. If no allocation occurs at those addresses in the transition Σ → Σ', they remain outside `dom(Σ'.I)`, violating A7a. The link integrity narrative reinforces the contradiction: "the spanfilade lookup succeeds — the I-address entries were permanently indexed at link creation" assumes all endset addresses were allocated at link creation, which ghost links violate by definition.

**Required**: Either (a) restrict A7a to non-ghost endsets: `(A a ∈ endset(L) : a ∈ dom(Σ.I) ⟹ a ∈ dom(Σ'.I))`, or (b) quantify A7 and A7a over `endset(L) ∩ dom(Σ.I)` and handle the mixed case (some endpoints allocated, some ghost) explicitly. A7's precondition "whose endset addresses are in dom(Σ.I)" partially addresses this for A7 but A7a states no precondition at all.

### Issue 2: A3(c) — transclusion cannot recover truly unreferenced content
**ASN-0030, The Accessibility Partition**: "Transition (c) is the recovery mechanism... transclusion provides a more immediate path: if any operation creates a new V-space mapping to an unreferenced I-address, the content becomes active again."

**Problem**: COPY(d_s, p_s, k, d_t, p_t) requires positions p_s through p_s+k−1 to be in d_s's V-space. If an I-address is in state (ii) — absent from every document's V-space — no COPY can reach it. The conditional "if any operation creates a new V-space mapping" identifies no such operation in the foundations. INSERT allocates fresh addresses (not mappings to existing ones). No defined operation creates a V-space mapping to an arbitrary existing I-address.

The error propagates into the link integrity section: "When unreferenced I-addresses are transcluded into a new document, the link becomes discoverable again." This is self-contradictory — transclusion (COPY) from V-space requires reachability, but the premise is that the addresses are unreferenced.

**Required**: Distinguish: (a) content still reachable in some document or version — COPY recovers it, but the content was never truly unreferenced (it was active, state (i)); (b) content in no V-space anywhere — no defined operation recovers it. Label A3(c) as consistent with invariants but not achievable by any currently defined operation for truly unreferenced addresses. The link integrity recovery claim must be similarly qualified.

### Issue 3: `reachable(a, d)` defined independently of foundation `refs(a)`
**ASN-0030, Identity and Reachability**: `reachable(a, d) ≡ (E p : 1 ≤ p ≤ n_d : Σ.V(d)(p) = a)`

**Problem**: ASN-0026 defines `refs(a) = {(d, p) : d ∈ Σ.D ∧ 1 ≤ p ≤ n_d ∧ Σ.V(d)(p) = a}`. The new definition is exactly `reachable(a, d) ≡ (E p : (d, p) ∈ refs(a))`, and `reachable(a) ≡ refs(a) ≠ ∅`. The equivalences are never stated.

**Required**: Define `reachable` in terms of `refs`, or explicitly state the equivalence, connecting the new concept to the foundation rather than re-deriving it from V-space primitives.

### Issue 4: No concrete example
**ASN-0030, throughout**

**Problem**: The ASN derives all properties abstractly but never verifies them against a specific scenario. A worked example would anchor the identity/reachability distinction and catch any gap in the accessibility transitions.

**Required**: One concrete scenario — e.g., document d with V-space mapping [a₁, a₂, a₃]; DELETE position 2; verify A4 (a₂ ∈ dom(Σ'.I) with content unchanged), the accessibility transition (a₂ moves from active to unreferenced if no other document references it), and the resulting V-space [a₁, a₃]. Then COPY a₂ from a version (if one exists) and trace the reverse transition.

### Issue 5: A4a (REARRANGE) asserted from implementation evidence, not derived
**ASN-0030, REARRANGE section**: `{Σ'.V(d)(p) : 1 ≤ p ≤ n_d} = {Σ.V(d)(p) : 1 ≤ p ≤ n_d}`

**Problem**: REARRANGE has no formal specification in any foundation ASN. Part (c) — set equality of I-addresses before and after — is justified solely by Gregory's implementation: "`rearrangend` operates exclusively on `cdsp.dsas[V]`." Implementation evidence is confirmation, not derivation. A4a is then used in the analysis as though it were established.

**Required**: Mark A4a explicitly as a specification requirement on REARRANGE (what it must satisfy) rather than a derived property (what follows from foundations). The distinction matters: if a future ASN formalizes REARRANGE, A4a becomes a required postcondition to verify, not a known theorem.

### Issue 6: A5 (COPY) introduced without preconditions
**ASN-0030, COPY section**: "COPY(d_s, p_s, k, d_t, p_t) — copy k positions from d_s into d_t"

**Problem**: A5(a) states `Σ'.V(d_t)(p_t + j) = Σ.V(d_s)(p_s + j)` for `0 ≤ j < k`, but the preconditions that make this well-defined are absent. At minimum: d_s ∈ Σ.D, d_t ∈ Σ.D, 1 ≤ p_s, p_s + k − 1 ≤ n_{d_s}, 1 ≤ p_t ≤ n_{d_t} + 1, k ≥ 1. Without these, A5(a) quantifies over potentially invalid positions.

**Required**: State preconditions explicitly, following the pattern of P9 (ValidInsertPos) in ASN-0026.

### Issue 7: A9 and A10 listed alongside formal invariants
**ASN-0030, Properties Table**: A9 ("coordinate-level, independent of physical storage") and A10 ("no client-verifiable mechanism for content authenticity") appear in the same table as formal invariants A0–A8.

**Problem**: A9 is vacuously true — every abstract specification is implementation-independent by definition; stating it as a property adds no formal content. A10 is a meta-remark about what the specification does not provide — a non-property. Listing both alongside invariants that constrain implementations and enable proofs conflates formal claims with commentary.

**Required**: Separate A9 and A10 from the formal properties. Either label them as "Design Remark" in the table or move them to a discussion section outside the properties enumeration.

## OUT_OF_SCOPE

### Topic 1: Formal specifications for DELETE, COPY, and REARRANGE
**Why out of scope**: ASN-0026 specifies INSERT in detail (P9) but provides only classification (+_ext) and cross-document independence (P7) for the other operations. Full formal specifications — preconditions, postconditions, frame conditions — belong in an amendment to ASN-0026 or a dedicated operations ASN, not in an analysis of address permanence.

### Topic 2: Formal link model
**Why out of scope**: The ASN derives link properties from I-space foundations, which is valid. A complete model of link creation (MAKELINK preconditions — can you link to ghost addresses?), storage, indexing, and querying is new territory.

### Topic 3: Recovery mechanism for truly unreferenced content
**Why out of scope**: Nelson's "historical backtrack functions" are acknowledged but undefined. Specifying a mechanism that creates V-space mappings to arbitrary I-addresses is a separate design question, correctly listed in the ASN's open questions.

VERDICT: REVISE
