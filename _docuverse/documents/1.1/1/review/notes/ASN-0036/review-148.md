# Review of ASN-0036

## REVISE

### Issue 1: "Formal consequence" asserted without a formal statement or derivation

**ASN-0036, The document as arrangement**: "This has a formal consequence: document equality is not decidable by content comparison — the same output can arise from different arrangements of different I-addresses that happen to carry identical values."

**Problem**: The phrase "formal consequence" promises a derived guarantee, but the section supplies only a one-sentence informal gesture. There is no property statement, no formal contract, and no construction. By the standard that derived guarantees must name premises and show the chain, this is a claim, not a derivation. It is also the only "consequence" in the ASN with no example or proof, where the rest of the document is meticulous about both. (There is a latent scope tension too: document identity borders on the out-of-scope "document creation and lifecycle" cluster — so the cleanest fix may also be the safest.)

**Required**: Either (a) promote it to a labeled property with an explicit statement (e.g., ∃ `d₁ ≠ d₂` with `(A v : M(d₁)(v) = M(d₂)(v))`) and an S5-style witness construction discharging it from S2/S4; or (b) drop "formal consequence," relabel the passage a remark, and present it as motivation rather than a derived result.

### Issue 2: Trivial observation that does not advance the argument

**ASN-0036, Sharing (after S5 statement)**: "We observe that the sharing relation is a function of `Σ` alone: for any `a ∈ dom(C)`, the set `{d : (E v :: M(d)(v) = a)}` is determined by the state."

**Problem**: Anything written as a set-builder over `Σ` is trivially determined by `Σ`; the sentence states a tautology and is not used by the S5 proof or any later claim. It is precisely the kind of meta-prose the precise reader must skip past. The `review-mode.anti-bloat` classifier directs surfacing this.

**Required**: Delete, or replace with the actual load-bearing point if one is intended (e.g., that the *inverse* — given `a`, recover referencing documents — is what the Open Questions defer to the operations layer).

### Issue 3: Reviser editorializing inside a derivation

**ASN-0036, Valid insertion position (paragraph before the formal contracts)**: "Distinctness of the `N + 1` valid positions is the one step worth spelling out: for `j, j' ∈ {0, ..., N}` with `j ≠ j'`, the last components `1 + j` and `1 + j'` differ..."

**Problem**: "is the one step worth spelling out" is meta-commentary about the proof rather than the proof. State the distinctness argument directly; the editorial framing is noise.

**Required**: Drop the lead-in clause; keep the argument ("For `j ≠ j'`, the last components `1 + j ≠ 1 + j'` (NAT-order), so the tumblers diverge at position `m` and are distinct by T3").

### Issue 4: Overlapping operations-layer open questions

**ASN-0036, Open Questions**: "Does each well-formed editing operation (DELETE, INSERT, COPY, REARRANGE) preserve D-CTG and D-MIN?" and "What invariants must the displacement mechanism satisfy so that insertion at a ValidInsertionPosition preserves D-CTG, D-MIN, and S2?" and "What must an operation guarantee about existing V-to-I mappings when it inserts at a position that coincides with an occupied V-position?"

**Problem**: Three questions defer the same concern — operation-layer preservation of D-CTG/D-MIN/S2 under insertion — to the same future location. Per the anti-bloat guidance on repeated downstream deferrals, consolidate.

**Required**: Merge into a single open question on operation-layer preservation of the contiguity invariants, retaining the one genuinely distinct sub-point (coincidence with an occupied V-position).

## OUT_OF_SCOPE

### Topic 1: Inverse-sharing cost bound and reachability distinction
The Open Questions on the computability/cost of the sharing inverse and on distinguishing reachable from unreachable content are correctly posed as future work; they require a query/operations model this state-level ASN does not introduce. No action needed.

The proofs of S1, S4, S5, S7, S8, S8a, D-CTG-depth, and D-SEQ were checked case-by-case (including the S8 within-subspace incompatibility lemma at `j < m`, `j = m`, and `m = 2`, and the cross-subspace argument via T5/T10) and are rigorous; boundary cases (empty arrangement, depth `m = 2` vs `m ≥ 3`, append position) are handled. The subspace-identifier-vs-separator distinction is stated correctly.

VERDICT: REVISE
