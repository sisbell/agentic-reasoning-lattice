# Review of ASN-0003

## REVISE

### Issue 1: No distinction between axiom, theorem, and definition
**ASN-0003, Properties Table**: All 14 properties listed with status "introduced"
**Problem**: The ASN presents 14 properties as a flat list, but they have three different logical roles:

- **Definitions** (part of the state model): IV5 repeats IV-Σ2's domain specification. IV6 combines IV-Σ2's functionality with IV0's range condition. IV7 is a non-constraint (states what is *not* required).
- **Redundancies**: IV3 is IV2 restricted to non-initial addresses. IV9 is IV1 + IV2 restated operationally. IV12 is IV0-PRES stated as a property. IV13 follows from IV10 + the definition of DELETE. IV14 follows from IV12.
- **Actual axioms**: IV0, IV1, IV2, IV8, IV10, IV11 (arguably).

The reader cannot tell which properties are load-bearing assumptions and which are derived. A specification that presents six independent axioms as fourteen co-equal properties obscures its own logical structure.

**Required**: Partition the properties into (a) state definitions (part of Σ), (b) axioms (independently assumed), (c) theorems (derived, with proofs). The table should reflect this classification.

### Issue 2: IV4 is a tautology
**ASN-0003, IV4**: "a ∈ dom(Σ'.I) \ dom(Σ.I) ⇒ a ∉ dom(Σ.I)"
**Problem**: This is the definition of set difference. The ASN acknowledges it: "trivially true as stated." The operational content — that the allocation mechanism reliably produces previously-unused addresses — is described in prose but absent from the formalization. As stated, IV4 carries zero information. Any system whatsoever satisfies it.
**Required**: Either formalize the actual guarantee (e.g., "there exists an allocation function that, given Σ, produces addresses outside dom(Σ.I)") or remove IV4 and note that freshness is a mechanism property, not a state invariant.

### Issue 3: IV3 formal statement does not capture "address reuse is impossible"
**ASN-0003, IV3**: "a ∈ dom(Σ.I) ∧ a ∉ dom(Σ₀.I) ⇒ (A Σ' : Σ' is a successor of Σ : Σ'.I(a) = Σ.I(a))"
**Problem**: This says content at allocated addresses doesn't change — which is IV2 (with an unnecessary restriction to non-initial addresses, which are all addresses if Σ₀ is empty). The prose claims IV3 captures "address reuse is impossible," but reuse impossibility requires both persistence (IV1: the address stays allocated, so it can't be freed and reallocated) and immutability (IV2: the content doesn't change). The formal statement captures only the IV2 half.
**Required**: Either derive "address reuse is impossible" as a theorem from IV1 + IV2 (with an explicit proof), or remove IV3 as a separate property and state the consequence in prose under IV1/IV2.

### Issue 4: REARRANGE case in IV0-PRES is one sentence
**ASN-0003, IV0-PRES, Case: REARRANGE**: "REARRANGE permutes V-positions without creating or destroying content. Every V-position in the result maps to some I-address that was mapped before the operation."
**Problem**: REARRANGE is described as "transposition of two regions" and then as "permutes V-positions." These are different things (a transposition of two contiguous regions is a specific permutation). The proof is a single sentence that does not: (a) define what REARRANGE does to the V→I mapping, (b) verify that IV5 (dense contiguity) is maintained, (c) address edge cases (overlapping regions, empty regions, single-element regions), or (d) verify that the resulting V-space is a valid total function on {1, ..., n}.
**Required**: Define REARRANGE's effect on Σ.V(d) precisely — which positions map to which I-addresses after the operation. Then verify IV0 for each category of position (moved, unmoved, boundary).

### Issue 5: COPY case in IV0-PRES does not specify mechanics
**ASN-0003, IV0-PRES, Case: COPY**: "COPY reads I-addresses from a source document's POOM and creates V-space mappings in the target document."
**Problem**: The proof does not specify *where* in the target document the copied content is placed. Does COPY insert at a position (shifting subsequent content, like INSERT)? Does it replace existing content? Does it append? Without knowing how COPY affects Σ.V(d), the proof cannot verify IV0 for the target's non-copied positions. If COPY shifts content (like INSERT), the shifted positions need the same IV1-based argument used in the INSERT case. If it doesn't shift, the domain and contiguity need checking.
**Required**: Define COPY's effect on Σ.V(d) — target position, whether existing content shifts, resulting domain. Then verify IV0 for all position categories (new, shifted, unshifted, other documents).

### Issue 6: IV5 preservation not verified
**ASN-0003, IV0-PRES**: Proves IV0 (referential integrity) is preserved by all operations.
**Problem**: IV0-PRES verifies that V-positions point to valid I-addresses. But dense contiguity (IV5) — that the domain remains {1, ..., n} with no gaps — is equally critical and never verified. INSERT must produce domain {1, ..., n+k}. DELETE must produce domain {1, ..., n-k}. REARRANGE must preserve domain {1, ..., n}. These require showing that the shift/close operations produce the correct contiguous domain. The ASN asserts these effects but does not verify them.
**Required**: For each operation, verify that Σ'.V(d) has domain {1, ..., #Σ'.V(d)} after the operation. This is especially important for INSERT (the k new positions plus k-shifted existing positions must tile {1, ..., n+k} without gaps or overlaps) and DELETE (the closed gap must produce {1, ..., n-k}).

### Issue 7: INSERT boundary cases omitted
**ASN-0003, IV0-PRES, Case: INSERT**: Covers new positions, shifted positions, unshifted positions.
**Problem**: The three-way case split covers the general case but does not verify the boundaries where categories become empty:
- INSERT at position 1 (p=1): no unshifted positions (q < 1 vacuous). Does the proof still hold? Yes trivially, but stating "the unshifted category is empty" would confirm the case was considered.
- INSERT at position #Σ.V(d)+1 (append): no shifted positions. The ASN does not confirm this position is valid — is the precondition 1 ≤ p ≤ #Σ.V(d)+1?
- INSERT into an empty document (#Σ.V(d)=0, p=1): both shifted and unshifted categories are empty. Only new positions exist.
- INSERT of zero bytes (k=0): the "new positions" range p through p+k-1 = p through p-1 is empty. Is this permitted? If so, INSERT is a no-op and IV0 holds trivially. If not, the precondition k ≥ 1 should be stated.

**Required**: State the precondition for INSERT explicitly (valid range of p, valid range of k). Then note which case categories are empty at the boundaries and confirm IV0 holds.

### Issue 8: MAKELINK absent from IV0-PRES
**ASN-0003, IV0-PRES**: "We reason by cases on the operation type" — covers INSERT, DELETE, REARRANGE, COPY, CREATENEWVERSION.
**Problem**: MAKELINK is absent. The ASN's consequences section discusses link survivability at length, and the vocabulary defines links as having three endsets that reference I-space spans. If MAKELINK allocates link content in I-space (LINKATOMs) and/or creates V-space mappings in a link subspace, it is a state-modifying operation that IV0-PRES must cover. If MAKELINK operates on a separate structure not modeled by Σ.V(d), then the ASN's model is incomplete — links are discussed in consequences but absent from the state model.
**Required**: Either (a) include MAKELINK in IV0-PRES with a case analysis showing it preserves IV0, or (b) explicitly scope the ASN to text content and note that link subspace operations are deferred, removing the link survivability consequence (which depends on an unmodeled structure).

### Issue 9: SEP is labeled "theorem" but has no derivation
**ASN-0003, Theorem (SEP)**: "Given IV0 through IV14, the system satisfies: (a) Permanence... (b) Transclusion... (c) Link survivability..."
**Problem**: Each clause of SEP is annotated with the properties it follows from (e.g., "by IV1, IV2, IV8"), but no derivation is shown. (a) is just IV1 + IV2 restated in English. (b) says "by IV7, with COPY preserving I-addresses" — IV7 is a non-constraint (V→I is not injective), which does not *derive* transclusion; it *permits* it. (c) depends on a link model not formalized in this ASN. (d) depends on CREATENEWVERSION sharing I-addresses, which is a specification of that operation, not a consequence of IV0-IV14. Labeling this a "theorem" overstates what has been established.
**Required**: Either provide actual derivations (showing the chain from axioms to each consequence) or relabel SEP as a summary/claim and note which parts depend on operation specifications not formalized in this ASN.

## DEFER

### Topic 1: Formal link model
**Why defer**: The ASN discusses link survivability as a consequence but does not model links in its state definition. A future ASN should formalize link structure (endsets, link index, spanfilade) and verify that MAKELINK preserves the I-space/V-space invariants. This is new territory — ASN-0003 correctly identifies links as a motivation for the two-space architecture, but formalizing them is a separate task.

### Topic 2: Distribution and concurrency
**Why defer**: The open questions ask about multi-node I-space and concurrent allocation. These require a concurrency model not present in this ASN. The single-document, sequential model here is the right foundation to build on.

### Topic 3: Durability ordering (IV14 strengthened to crash survival)
**Why defer**: The open questions correctly identify this as a separate concern. IV14 as an atomicity property is sufficient for the abstract model; crash recovery requires a persistence model.