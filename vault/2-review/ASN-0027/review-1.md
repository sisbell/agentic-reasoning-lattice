# Review of ASN-0027

## REVISE

### Issue 1: A4 (CopySharing) missing preconditions and target frame conditions
**ASN-0027, COPY section**: "A4 (CopySharing). COPY from source document `d_s`, span `(p_s, k)`, to target document `d_t` at position `p_t` creates V-space mappings to the *same* I-addresses."
**Problem**: A4 specifies only the identity clause and source frame. It omits: (a) preconditions — valid ranges for `p_s`, `k`, `p_t`, whether `d_s ∈ Σ.D`, whether `d_t ∈ Σ.D`; (b) target length postcondition — `|Σ'.V(d_t)|`; (c) target left frame and right shift — what happens to positions outside `[p_t, p_t+k)`. DELETE (A2) specifies all of these. COPY does not. This matters because A7 depends on A4: the proof of identity-restoring COPY requires that COPY at position `p` in the post-DELETE document is well-defined and that position `p+j` exists in the result. The precondition *is* satisfied (from A2's precondition, `p ≤ n_d - k + 1`, so `p` is a valid insertion point in the shortened document), but the ASN never verifies this because A4 has no precondition to check against.
**Required**: Add to A4: precondition (`d_s ∈ Σ.D ∧ 1 ≤ p_s ∧ p_s + k - 1 ≤ n_{d_s} ∧ k ≥ 1 ∧ d_t ∈ Σ.D ∧ 1 ≤ p_t ≤ n_{d_t} + 1`), length postcondition (`|Σ'.V(d_t)| = n_{d_t} + k`), left frame (`(A j : 1 ≤ j < p_t : Σ'.V(d_t)(j) = Σ.V(d_t)(j))`), and right shift (`(A j : p_t ≤ j ≤ n_{d_t} : Σ'.V(d_t)(j + k) = Σ.V(d_t)(j))`). Then in A7's proof, verify the COPY precondition is met.

### Issue 2: A9 proof invokes cross-document frame for same-document references
**ASN-0027, ReachabilityDecay proof**: "For each `(d_i, p_i)`, DELETE on `d_i` at position `p_i` removes that reference. By A2 (cross-document frame), each DELETE affects only its target, so the references in other documents are unchanged until their turn."
**Problem**: The proof enumerates `refs(a) = {(d_1, p_1), ..., (d_m, p_m)}` and processes them sequentially, invoking A2's cross-document frame. But when multiple pairs share the same document (`d_i = d_j` for `i ≠ j`), deleting at `p_i` compacts positions within `d_i`, renumbering `p_j`. The cross-document frame does not apply within the same document. After deleting at `p_1` in document `d`, position `p_3` (if `p_3 > p_1` and both reference `a`) becomes `p_3 - 1`. The proof treats all m references as independent, but they are not when they share a document.
**Required**: Fix the proof to process documents one at a time: for each document `d` appearing in `refs(a)`, repeatedly delete the lowest-numbered position mapping to `a` until `d` has no references to `a`, then move to the next document. The cross-document frame justifies independence *between* documents. Within a document, each deletion reduces the count of positions mapping to `a` by exactly one (compaction preserves remaining mappings, just at shifted positions). This establishes `|refs(a)|` decreasing monotonically to zero.

### Issue 3: No concrete example
**ASN-0027, throughout**: The ASN never instantiates a specific state and traces an operation through the postconditions.
**Problem**: The review standard requires at least one concrete scenario. A6 (NonInvertibility) is the natural candidate — it argues abstractly about fresh addresses but never shows a specific document.
**Required**: Add a worked example, e.g.: "Let `Σ₀.V(d) = [a₁, a₂, a₃, a₄, a₅]`. DELETE(d, 2, 2) yields `Σ₁.V(d) = [a₁, a₄, a₅]` (A2: left frame preserves position 1, compaction shifts positions 4–5 to 2–3). INSERT(Σ₁, d, 2, 2, 'XY') yields `Σ₂.V(d) = [a₁, a'₁, a'₂, a₄, a₅]` where `a'₁, a'₂ ∉ dom(Σ₀.I)`. Verify: `a'₁ ≠ a₂` and `a'₂ ≠ a₃` (since `a₂, a₃ ∈ dom(Σ₀.I)` by P2). Identity lost. Now COPY from version: `Σ₃.V(d) = [a₁, a₂, a₃, a₄, a₅]`. Identity restored."

### Issue 4: A6 uses `correspond` in a cross-state sense not defined by ASN-0026
**ASN-0027, Non-Invertibility of Deletion**: "correspond(d_{Σ₀}, p + j, d_{Σ₂}, p + j) = false for all j in the affected range"
**Problem**: ASN-0026 defines `correspond(d_1, p_1, d_2, p_2) ≡ Σ.V(d_1)(p_1) = Σ.V(d_2)(p_2)` — comparing two documents within a single state. The subscripts `Σ₀` and `Σ₂` on `d` indicate a comparison across different states, which the foundation does not define. The formal content is correct (A6 proves `Σ₂.V(d)(p+j) ≠ Σ₀.V(d)(p+j)`), but the `correspond` notation misapplies a foundation definition.
**Required**: Either (a) define a cross-state correspondence explicitly: `correspond_temporal(d, p, Σ, Σ') ≡ Σ.V(d)(p) = Σ'.V(d)(p)`, or (b) express the claim directly without invoking `correspond`: "The I-address at position `p+j` in `Σ₂` differs from the I-address at position `p+j` in `Σ₀`: `Σ₂.V(d)(p+j) ≠ Σ₀.V(d)(p+j)` for all `0 ≤ j < k`."

### Issue 5: A3 (RearrangeIdentity) missing precondition
**ASN-0027, REARRANGE section**: A3 states postconditions and frame conditions but no precondition.
**Problem**: Every other operation specification in this ASN (A2, A4, A5) has preconditions or at minimum states the document membership requirement. A3 has none — not even `d ∈ Σ.D`. Without a precondition, the specification applies to non-existent documents.
**Required**: Add precondition: `d ∈ Σ.D ∧ n_d ≥ 0`. (If additional parameters constrain the permutation — e.g., a source range and target position — state those too, or note that the spec abstracts over permutation selection.)

## OUT_OF_SCOPE

### Topic 1: MAKELINK and other potential primitive operations
**Why out of scope**: A1 covers the five operations classified by ASN-0026's `+_ext`. MAKELINK (mentioned in the vocabulary) is not yet formalized by any foundation ASN. When MAKELINK is specified, its I-space effect must be verified against A1's pattern (likely extends I-space with fresh addresses for link content, preserving the permanence conclusion). This is a future ASN, not an error in this one. However, A1 should note its scope explicitly ("for the five operations defined in ASN-0026") rather than claiming "for each primitive operation" unqualified.

### Topic 2: Publication protocol and franchise obligations
**Why out of scope**: A10 correctly identifies publication obligation as contractual rather than architectural. The mechanisms of enforcement (franchise structure, storage rental, due process for withdrawal) are system-level policy, not state-and-operation specification. Future ASNs.

### Topic 3: Accessibility recovery guarantees
**Why out of scope**: The open questions about bounded version backtracking, mandatory version retention for published content, and the distinction between "never referenced" and "all references deleted" are genuine specification gaps but are above the I-space/V-space layer this ASN formalizes.

VERDICT: REVISE
