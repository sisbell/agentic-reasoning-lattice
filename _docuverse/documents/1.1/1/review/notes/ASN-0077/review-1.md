# Review of ASN-0077

## REVISE

### Issue 1: Citation typo for M16a
**ASN-0077, "Lifting origin to a V-span"**: "By M16a (OrdinalInvarianceUnderShift, ASN-0058), `origin(aⱼ + i) = origin(aⱼ)` for every `i` in this range."

**Problem**: ASN-0058 defines M16a as "OriginInvarianceUnderShift", not "OrdinalInvarianceUnderShift". The cited lemma name does not match the foundation.

**Required**: Correct the citation to "OriginInvarianceUnderShift".

### Issue 2: O1 is essentially tautological
**ASN-0077, "Lifting origin to an I-span"**: "Claim O1 (Subspace homogeneity). For any I-span σ such that every element of `⟦σ⟧ ∩ dom(C)` lies wholly within one document's content subspace, `|origins_I(Σ, σ)| ≤ 1`."

**Problem**: As stated, the precondition "lies wholly within one document's content subspace" already means "all addresses share one origin" (by S7a's prefix structure). The conclusion then unfolds to "the set of origins has cardinality ≤ 1," which is a definitional consequence. There is no substantive proof obligation. The "contrapositive" presented later — "if `|origins_I| > 1`, then σ has positions in two or more distinct content subspaces" — is the same restatement read backwards.

**Required**: Either (a) strengthen O1 to a substantive claim (e.g., that `origins_I` *partitions* `⟦σ⟧ ∩ dom(C)` and the partition reflects the document-allocation hierarchy of S7d), or (b) demote O1 to an immediate consequence of S7a + S7d with the relevant derivation explicit.

### Issue 3: O4 reduces to a corollary of O3
**ASN-0077, "Direct resolution through transclusion"**: "Claim O4 (Direct resolution through transclusion). For any V-position `v ∈ dom(M(dₙ))` with `M(dₙ)(v) = a`, `origin(a)` is determined by `a` alone..."

**Problem**: The substantive content — that origin is determined by `a` alone, with no consultation of intermediate documents — is exactly what O3 (Structural derivation) already asserts. The "depth of transclusion chain" framing is rhetorical; once `M(dₙ)(v) = a` is given, the projection sees only `a`. The proof reduces to applying O3 to a single address. O4 as a separately numbered claim does not add formal content.

**Required**: Either present O4 explicitly as a corollary of O3 (rather than a peer claim), or strengthen O4 with content beyond O3 — for instance, a statement about how each intermediate arrangement `M(d_i)` for `2 ≤ i ≤ n-1` independently records the same `a` (which is what actually makes the example work, and which depends on transclusion semantics not yet fixed in this ASN).

### Issue 4: Two formulations of `origins_V` without equivalence proof
**ASN-0077, "Lifting origin to a V-span" vs "The operation"**: The expansion gives `origins_V(Σ, d, σ) = ⋃_{j=1}^{k} { origin(aⱼ + i) : 0 ≤ i < nⱼ }` and reduces it to `{ origin(aⱼ) : 1 ≤ j ≤ k }`; the operation spec later gives `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }`.

**Problem**: Three different forms are presented as the definition. Their equivalence is asserted but never derived. The equivalence requires M2/M3 of ASN-0058 (resolution covers exactly the V-positions in `⟦σ⟧ ∩ dom(M(d))`) plus M16a (each block contributes one origin). Without an explicit derivation, the reader cannot verify that the operation's postcondition matches the lift defined in the body.

**Required**: Show the equivalence chain. Specifically, that for `f = M(d) ↾ ⟦σ⟧`: `⋃_j { origin(aⱼ + i) : 0 ≤ i < nⱼ } = { origin(f(v)) : v ∈ dom(f) }`, justified by ASN-0058's M2 (decomposition covers dom(f)) and M16a (single origin per block).

### Issue 5: Proofs are one-sentence appeals, not derivations
**ASN-0077, throughout**: Most claims are "established" by single-sentence references — e.g., O5: "This is a direct consequence of foundation ASN-0047's P0..." O6: "By P0, `dom(C) ⊆ dom(C')`, so..." O10: "Idempotence follows."

**Problem**: The standard for proof requires multi-step derivations naming each premise and conclusion. "X is a direct consequence of Y" is a claim, not a proof. For instance, O5's full chain is: (1) Σ → Σ' is reachable; (2) by P0, `dom(C) ⊆ dom(C')` and `(A a ∈ dom(C) :: C'(a) = C(a))`; (3) the address `a` is identical in both states (P0 does not modify addresses); (4) origin reads components of `a` only; (5) therefore `origin'(a) = origin(a)`. The ASN compresses this to one sentence and trusts the reader.

**Required**: Each claim's derivation should at least enumerate the premises drawn from foundation and the inference step that closes the conclusion. The current prose hides the steps.

### Issue 6: Edge cases not covered
**ASN-0077, throughout**:

**Problem**: The following edge cases are not addressed:
- *Empty intersection*: `⟦σ⟧ ∩ dom(C) = ∅` (well-formed I-span containing no allocated addresses). Result is `∅`; does the operation succeed? Is `∅` a legitimate SHOWORIGIN output?
- *Singleton I-span*: σ contains exactly one address. The worked example shows multi-block; the singleton scale (which the prose emphasises as semantically central) is not exhibited.
- *Cross-subspace I-span*: σ intersects both `dom(C)` and `dom(L)`. The lift silently drops link addresses by intersecting only with `dom(C)`. Is this intentional? Is this the spec's choice or an open question? (The Open Questions list raises it, but the lift's silent behaviour on this case should be acknowledged in the definition.)
- *Empty document*: `M(d) = ∅`. V-span operation: is the precondition even satisfiable (a well-formed content reference requires `V_{u₁}(d_s) ≠ ∅`)? Need to state whether SHOWORIGIN is admissible on empty documents.

**Required**: Treat each boundary case explicitly. State the result, verify the postconditions hold, and either include in the worked example or supply a brief case-by-case sketch.

### Issue 7: Concrete example covers only the multi-block case
**ASN-0077, "A worked example"**:

**Problem**: The worked example illustrates the multi-block, multi-origin case (5-position transclusion plus 2-position native content). It does not verify O5 (permanence under a transition), O6 (monotonic growth as new content is allocated), O7 (stability when arrangement is unchanged), O9 (identity vs equivalence — what about two documents with identical text?), or O10 (idempotence). The standard requires verifying *key postconditions* against a concrete scenario.

**Required**: Extend the example, or add a second example, that exercises at least one postcondition from each of the permanence/growth/identity-tracking claims — for instance, show what `origins_V` returns at `d₃` before and after a K.μ⁺ extension in `d₃` adds new content from yet another document.

### Issue 8: O8 framing mismatch
**ASN-0077, "Scale invariance"**: "Claim O8 (Scale invariance). For I-spans `σ₁, σ₂` with `⟦σ₁⟧ ⊆ ⟦σ₂⟧`: `origins_I(Σ, σ₁) ⊆ origins_I(Σ, σ₂)`."

**Problem**: The claim is *monotonicity under span inclusion*, not *scale invariance*. The prose ("the same mechanism that names the home of a million-character chapter must name the home of a single character") describes a uniformity-of-mechanism property; the formal statement gives a set-inclusion property. These are different. Monotonicity holds even for a mechanism that varies with size; uniformity is the structural fact (already covered by O3).

**Required**: Either rename O8 to reflect the actual content ("Span union monotonicity") and remove the scale-invariance framing, or strengthen the claim to a uniformity statement (which is already implicit in O3 — pointwise projection — and may need no new label).

### Issue 9: No weakest precondition analysis
**ASN-0077, "The operation"**: The operation spec gives preconditions, postconditions, and frame, but no wp analysis.

**Problem**: The standards require wp analysis or note that it is "trivial." For SHOWORIGIN, several non-trivial wp computations are possible and would clarify guarantees:
- `wp(SHOWORIGIN_I, |result| = 1)` = `(A a, b : a, b ∈ ⟦σ⟧ ∩ dom(C) : origin(a) = origin(b)) ∧ ⟦σ⟧ ∩ dom(C) ≠ ∅` — exact characterisation of single-origin spans.
- `wp(SHOWORIGIN_V, d ∈ result)` = the V-span resolution decomposition contains a block sourced from `d`.

These are non-trivial and would document what the operation can be used to discover.

**Required**: Add at least one non-trivial wp computation showing what the operation reveals about state.

### Issue 10: Operation precondition for V-span elides ASN-0058 conditions
**ASN-0077, "The operation"**: "Preconditions: `(d, σ)` is a well-formed content reference (ASN-0058)."

**Problem**: The reference to ASN-0058 is correct, but well-formedness there is multi-conjunct (subspace non-emptiness, T12, depth match, and the inclusion `{v : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d_s))`). Naming all conjuncts explicitly is required for self-contained operation specification — the reader must verify each precondition before invocation.

**Required**: Enumerate the well-formedness conditions either inline or by explicit conjunct labels from ASN-0058.

## OUT_OF_SCOPE

### Topic 1: Origin lift for link subspace addresses
**Why out of scope**: The lift `origins_I` restricts to `⟦σ⟧ ∩ dom(C)`, silently dropping link addresses. The Open Questions section correctly identifies this as a future ASN concern. Defining link-origin reporting belongs in a separate operation specification or a unified treatment, not this ASN.

### Topic 2: Historical containment via Σ.R
**Why out of scope**: SHOWORIGIN reports current origin, not provenance. The ASN correctly defers historical-containment reporting (a separate operation reading from `Σ.R`) to future work. The Open Questions section captures this.

### Topic 3: Transclusion-chain surfacing
**Why out of scope**: An operation that walks intermediate arrangements `M(d_2), ..., M(d_{n-1})` is distinct from SHOWORIGIN's direct answer. The Open Questions list raises this as a candidate companion operation.

### Topic 4: Native-vs-transcluded distinction within a document
**Why out of scope**: The Open Questions section correctly identifies this as a separate operation. SHOWORIGIN reports identity of origin, not relationship of origin to the queried document.

VERDICT: REVISE
