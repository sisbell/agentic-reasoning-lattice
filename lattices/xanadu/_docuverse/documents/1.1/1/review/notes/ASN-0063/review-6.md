# Review of ASN-0063

## REVISE

### Issue 1: K.μ~ fixedness argument has a cardinality gap
**ASN-0063, Extending the Transition Framework (S3★ preservation by K.μ~)**: "Since K.μ⁺ (amended) requires subspace(v) = s_C for new V-positions, K.μ⁺ cannot create link-subspace V-positions. Therefore K.μ⁻ cannot remove any link-subspace V-position without breaking the bijection — the removed position's I-address (in dom(L)) would need placement under a content-subspace V-position, violating S3★."
**Problem**: The argument rules out mapping the removed position's I-address to a *new* content-subspace V-position (cases: K.μ⁺ precondition requires `a ∈ dom(C)`, and surviving content positions already map to dom(C)). But it does not rule out mapping it to a *surviving* link-subspace V-position that already maps to the same link address. The missing step is the cardinality argument: K.μ⁺ cannot create link-subspace V-positions, so `|dom_L(M'(d))| ≤ |dom_L(M(d))|`. The bijection π restricted to link-subspace positions is an injection from `dom_L(M(d))` (size N) into `dom_L(M'(d))` (size N − r, where r positions were removed). For r ≥ 1 the injection cannot exist. Therefore r = 0 — no link-subspace positions can be removed.
**Required**: Add the cardinality step. Show that π must map link-subspace positions to link-subspace positions (the existing S3★ argument covers this), then show the injection from a larger set into a strictly smaller set is impossible.

### Issue 2: CL1 proof claims "exactly one" but ASN later notes overlapping I-spans
**ASN-0063, Endset Resolution (CL1 proof)**: "Every address in `image(d, Ψ)` lies in the denotation of exactly one CL0 I-span, establishing `image(d, Ψ) ⊆ coverage(E)`."
**Problem**: When content is shared (S5, UnrestrictedSharing), multiple blocks can map different V-positions to the same I-address. Each block produces its own CL0 I-span, so the I-address lies in *multiple* CL0 I-span denotations — not exactly one. The ASN itself notes this three paragraphs later: "The CL0 I-span collection is therefore not necessarily normalized — overlapping spans may arise from transcluded content." The containment conclusion (`image ⊆ coverage`) needs only "at least one," which holds regardless.
**Required**: Change "exactly one" to "at least one" in the CL1 proof. The preceding sentence about V-positions falling in exactly one block is correct — the error is in transferring "exactly one" from V-positions to I-addresses.

### Issue 3: Orphan links section claims K.μ⁻ achieves link withdrawal without noting D-CTG constraint
**ASN-0063, Extending the Transition Framework (orphan links)**: "Link withdrawal via K.μ⁻ applied to the link subspace would produce the same state — a link present in L but absent from all current arrangements."
**Problem**: K.μ⁻ removing a link-subspace V-position from the interior of the contiguous range violates D-CTG. The ASN itself proves K.μ~ cannot rearrange link-subspace positions (they are fixed), so gaps cannot be closed by reordering. The only D-CTG-preserving K.μ⁻ removes from the boundary — but even this breaks D-CTG unless it removes the *maximum* V-position (removing the minimum shifts D-MIN). The sentence presents K.μ⁻ withdrawal as straightforward when it is constrained.
**Required**: Qualify the claim. Either note that K.μ⁻ on the link subspace is constrained by D-CTG (and the system currently lacks a mechanism to close interior gaps), or state that the achievability of link withdrawal is deferred to the open question on withdrawal invariants.

### Issue 4: CL4 overclaims "any one of which would suffice" for five principles
**ASN-0063, What Is Preserved (CL4)**: "We arrive at this guarantee from five independent architectural principles, any one of which would suffice"
**Problem**: Only principles #2 (S0, Istream immutability) and #4 (K.λ frame condition) are formal guarantees that individually establish `C' = C`. Principle #1 (separate storage) is a design observation with no independent formal force. Principle #3 (owner-only modification) is explicitly noted as "not yet formalized in the transition framework." Principle #5 (structural separation) is a design philosophy. Three of five cannot individually "suffice" as formal proofs.
**Required**: Restate. The formal proof (already given before the five principles) is correct and sufficient. The five principles can be presented as reinforcing design context, but the claim that any single one suffices should be restricted to the two formal guarantees (#2 and #4).

### Issue 5: CL11 claims "all foundation invariants" but omits P3 and P4a
**ASN-0063, Invariant Preservation (CL11)**: "Theorem CL11 — InvariantPreservation. CREATELINK preserves all foundation invariants."
**Problem**: P3 (ArrangementMutabilityOnly, ASN-0047) and P4a (HistoricalFidelity, ASN-0047) are not listed or verified. P3: M(d) is extended (permitted by P3's extension clause), L is extended (new state component — P3 doesn't address L but the extension is monotonic, consistent with P3's spirit). P4a: R' = R and dom(C') = dom(C), so all existing provenance entries retain their historical witnesses. Both are trivially preserved, but the universal claim "all foundation invariants" requires either listing them or explicitly noting which invariants are vacuously preserved and why.
**Required**: Add one-sentence justifications for P3 and P4a, or add a blanket statement identifying the remaining invariants and why they are trivially preserved (R unchanged, C unchanged, E unchanged).

## OUT_OF_SCOPE

### Topic 1: Link withdrawal operation design
**Why out of scope**: The ASN correctly defers link withdrawal to an open question. The full design — which positions can be removed, how D-CTG is maintained, whether a K.μ~_L is needed — is new territory for a future ASN on link lifecycle operations.

### Topic 2: Link-subspace reordering capability
**Why out of scope**: The ASN proves K.μ~ fixes link-subspace mappings, which means the current framework has no mechanism for link-subspace reordering. Whether such a mechanism is needed (and if so, what transition supports it) is a future design question, not an error in this ASN.

### Topic 3: Discovery implementation and performance guarantees
**Why out of scope**: The ASN defines disc as a derived function on system state. Implementation concerns — enfilade structure, sub-linear query time, range queries vs. point queries — are implementation architecture, not abstract specification. The ASN correctly identifies these as open questions.

VERDICT: REVISE
