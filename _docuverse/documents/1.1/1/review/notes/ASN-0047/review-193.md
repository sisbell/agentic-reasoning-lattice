# Review of ASN-0047

## REVISE

### Issue 1: L1b subsequent-link derivation uses a false length/zero-count identity

**ASN-0047, *Extended reachable-state invariants*, L1b discharge (subsequent-link case)**: "Same length and zero count force same element-field length: `#E(ℓ) = #ℓ − zeros(ℓ) − 1 = #E(prev) ≥ 2` inductively."

**Problem**: Both the formula and the inference are wrong in general.
- The formula `#E(ℓ) = #ℓ − zeros(ℓ) − 1` is not a valid identity. For a `zeros = 3` address `N.0.U.0.D.0.E`, `#E = #ℓ − #N − #U − #D − 3`, which depends on the field lengths, not just `#ℓ` and `zeros`. Numerically, take `ℓ = [1,0,1,0,1,0,1,1]` (`#ℓ = 8`, `zeros = 3`, `#E = 2`): the formula yields `8 − 3 − 1 = 4 ≠ 2`.
- "Same length and zero count force same element-field length" is false: `[1,0,1,0,1,0,1,1]` and `[1,1,0,1,0,1,0,1]` both have length 8 and three zeros but `#E = 2` vs `#E = 1`.

The conclusion `#E(ℓ) = #E(prev)` is correct, but only via a different argument: `inc(·,0)` modifies only the *value* at position `sig(prev) = #prev` (TA5(c) + TA5-SigValid), a non-separator element-field position, leaving every separator *position* fixed; hence the field parse is identical and `#E(ℓ) = #E(prev)`.

**Required**: Replace the formula and the "same length + zero count ⟹ same #E" inference with the separator-position-preservation argument for `inc(·,0)`.

### Issue 2: Notation reinvented for foundation-defined predicates

**ASN-0047, *Notation* and *The state model***: uses `IsNode(a)`, `IsAccount(a)`, `IsDocument(a)`, `IsElement(a)`, and `ValidAddress(e)`.

**Problem**: ASN-0045 (foundation) already defines these as `Node(t)`, `Account(t)`, `Document(t)`, `Element(t)`, and `T4-valid(t)`. The ASN coins parallel names (`IsNode`, `ValidAddress`) for concepts the foundation fixes, and even uses both spellings of T4-validity inconsistently — "`ValidAddress(e)` (T4, ASN-0034)" in the entity-set definition vs. "`T4-valid(d)`" elsewhere. Standard 7 requires using the foundation's notation rather than reinventing it.

**Required**: Use ASN-0045's `Node`/`Account`/`Document`/`Element` predicates and `T4-valid` uniformly, or state explicitly and once that `IsNode := Node`, etc., are pure abbreviations.

### Issue 3: K.δ frame "M' = M" appears to contradict its stated subsumption of K.σ

**ASN-0047, K.δ definition and *K.σ subsumption***: Frame is "`M' = M` (uniform across the IsNode, IsAccount, and IsDocument cases). The sole effect of K.δ is `E' = E ∪ {e}`." Yet K.δ "subsum[es] ASN-0093's K.σ (DocumentRegistration)," whose foundation effect is `dom(M') = dom(M) ∪ {d}`.

**Problem**: Read literally, "`M' = M`" with "sole effect `E' = E ∪ {e}`" cannot subsume K.σ, which grows the allocated-document set. The reconciliation depends entirely on the Bridging lemma's redefinition `dom(M) := E_doc` (so growing `E_doc` *is* growing `dom(M)` while the function `M` with `∅`-default is unchanged). A reader comparing against K.σ will see a contradiction. The frame statement hides the document-registration effect that the K.σ-subsumption claim asserts.

**Required**: In the K.δ `IsDocument` case, state explicitly that `dom(M) (= E_doc)` grows and that `M'(e) = ∅` is the registered (allocated-empty) arrangement, distinct from the unallocated default — so the subsumption of K.σ's `dom(M') = dom(M) ∪ {e}` is visible at the operation, not only via the Bridging lemma.

### Issue 4: Meta-prose and repeated forward-reference deferral (anti-bloat)

**ASN-0047, several locations** (carries the `review-mode.anti-bloat` classifier):
- *SubAllocatorBundle introduction*: "This is a *bundling lemma* assembled in this ASN, not an axiom and not a result posited by ASN-0093. It collects under one name the sub-allocator facts the discharge chains below rely on, so a call site can cite one bundle rather than five separate ASN-0093 lemmas." — explains why the bundle exists and enumerates use-site convenience rather than advancing content.
- *The state model, "Provenance of inherited foundation results"*: "...we restate them for reading continuity and do not re-derive them. We do not repeat this provenance per result." — pure provenance rationale.
- *Bridging lemma* / *Notational convention (default value)*: "it is *not* a change of typing," "so the notation has one meaning throughout," "This is a writing convenience..." — defensive justification of a notational choice.
- Multiple sections defer to the same downstream location: "discharged per sub-case in §*K.δ case (ii) discharge and parent-allocator activation*" recurs in the K.δ catalogue, TrackedEmission, and S7d.

**Problem**: These passages are meta-prose the precise reader must skip past; they justify document organization and restatement decisions rather than carrying the argument. They match the flagged patterns (definition enumerating downstream consumers; provenance rationale around inherited results; multiple deferrals to one location).

**Required**: Delete the provenance/use-site rationale and defensive-convention prose; cite the discharging foundation lemma at the point of use and state the convention once without justifying its existence. Consolidate the repeated "§K.δ case (ii) discharge" deferrals so the discharge is stated once and referenced, not re-promised from several sites.

## OUT_OF_SCOPE

### Topic 1: NodeUniqueAllocation as an abstraction boundary
The reliance on an "external node-allocation registry" axiom and whether it is the correct abstraction boundary is already raised in Open Questions; settling it belongs to a future ASN, not this revision.

VERDICT: REVISE
