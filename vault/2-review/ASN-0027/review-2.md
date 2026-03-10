# Review of ASN-0027

## REVISE

### Issue 1: A6 concrete example makes a false claim about COPY restoring identity
**ASN-0027, "The Non-Invertibility of Deletion"**: "COPY from d', span (2, 2), to d at position 2 in a state after the INSERT: the result maps positions 2–3 back to a_2, a_3. Identity restored."

**Problem**: COPY is an insertion operation (A4 post-length: `|Σ'.V(d_t)| = n_{d_t} + k`). After DELETE+INSERT, `Σ_2.V(d) = [a_1, a'_1, a'_2, a_4, a_5]` with length 5. Applying COPY(d', (2,2), d, 2) produces `Σ_3.V(d) = [a_1, a_2, a_3, a'_1, a'_2, a_4, a_5]` with length 7, not the original length 5. Positions 2–3 do map to `a_2, a_3` (by A4 identity), but positions 4–5 retain `a'_1, a'_2` (by A4 right shift), so the document is not restored. "Identity restored" is false for the document as a whole.

The formal proof of A6 (non-invertibility) is correct. The error is confined to the illustrative paragraph that attempts to preview A7's restoration pattern but applies COPY after INSERT rather than after DELETE alone.

**Required**: Either remove the COPY paragraph from the A6 example (it belongs in A7), or correct it by showing the proper restoration sequence: DELETE the spurious `a'_1, a'_2` first, *then* COPY from `d'`. Alternatively, show the A7 pattern directly: DELETE without the intervening INSERT, then COPY.

### Issue 2: A3 precondition specifies no operation parameters
**ASN-0027, A3 (RearrangeIdentity)**: "Precondition: `d ∈ Σ.D ∧ n_d ≥ 0`"

**Problem**: The precondition `n_d ≥ 0` is trivially true for any document. Unlike A2 (which specifies inputs `(d, p, k)` with constraints `1 ≤ p`, `p + k − 1 ≤ n_d`, `k ≥ 1`) and A4 (which specifies `(d_s, p_s, k, d_t, p_t)` with source and target constraints), A3 does not state what REARRANGE takes as input. The permutation `σ` appears only existentially in the postcondition with no connection to any input parameter. This makes A3 unverifiable: we cannot check whether a given invocation satisfies the precondition (beyond document existence), nor can a downstream ASN reason about what rearrangement was requested.

**Required**: Specify REARRANGE's input signature — whether it takes a cut-and-paste specification `(d, p_from, k, p_to)`, a full permutation, or some other form — and constrain the precondition accordingly. The postcondition should tie `σ` to the input rather than asserting its existence unconditionally.

### Issue 3: A7 claims full document restoration without derivation
**ASN-0027, "Restoration Through Shared Identity"**: "After step 3, correspondence between d in Σ_0 and d in Σ_3 is restored — the positions map to the same I-addresses. DELETE+COPY-from-version is the identity-preserving undo."

**Problem**: A7's formal statement proves only the `k` deleted positions: `(A j : 0 ≤ j < k : Σ_2.V(d)(p + j) = a_j)`. The claim that the *full* document is restored (`Σ_2.V(d) = Σ_0.V(d)`) requires three additional steps not shown:

1. *Left frame*: A4 left frame gives `Σ_2.V(d)(j) = Σ_1.V(d)(j)` for `1 ≤ j < p`, and A2 left frame gives `Σ_1.V(d)(j) = Σ_0.V(d)(j)`, so `Σ_2.V(d)(j) = Σ_0.V(d)(j)` for `1 ≤ j < p`.
2. *Right frame*: A4 right shift gives `Σ_2.V(d)(j+k) = Σ_1.V(d)(j)` for `p ≤ j ≤ n_d - k`, and A2 compaction gives `Σ_1.V(d)(j) = Σ_0.V(d)(j+k)`, so `Σ_2.V(d)(m) = Σ_0.V(d)(m)` for `p+k ≤ m ≤ n_d`.
3. *Length*: `|Σ_2.V(d)| = (n_d - k) + k = n_d`.

The derivation is straightforward but required — "correspondence is restored" is a multi-step claim, not a corollary of A7 alone.

**Required**: Add the three-step derivation establishing `Σ_2.V(d) = Σ_0.V(d)`, or at minimum state it as a corollary of A7 with the derivation shown.

## OUT_OF_SCOPE

### Topic 1: MAKELINK as a primitive operation
A1 lists five primitive operations. The shared vocabulary defines MAKELINK. If MAKELINK is a primitive operation, its I-space frame condition (`Σ'.I = Σ.I` or extension with fresh addresses for link storage) must be verified. This belongs in a future ASN on link operations.

**Why out of scope**: ASN-0027 correctly covers the five operations specified by its foundation (ASN-0026). Link operations are new territory.

### Topic 2: Version DAG structure and deletion coordination
A9's proof constructs a deletion sequence across all documents referencing `a`. For published content with many transclusions, this coordination is "difficult by design." The ASN notes this but does not formalize what makes it difficult — the version DAG structure, franchise distribution, or access control. These are future ASN topics.

**Why out of scope**: The architectural barriers to reachability decay are above the I-space/V-space level that this ASN addresses.

### Topic 3: A4/A5 cross-document frame consistency
A2 explicitly states the cross-document frame. A3 references P7. A4 and A5 state only source/original frames without a general cross-document clause for unrelated documents. P7 from the foundation covers this, so there is no correctness gap, but the presentation is inconsistent across operations.

**Why out of scope**: Presentation consistency, not a logical error. The foundation P7 applies.

VERDICT: REVISE
