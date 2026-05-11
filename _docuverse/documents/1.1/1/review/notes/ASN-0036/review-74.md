# Review of ASN-36

## REVISE

### Issue 1: S7c's load-bearing role is misattributed

**ASN-36, parenthetical remark introducing S7**: "(S7c, stated here for architectural completeness, is load-bearing for S8-depth's ordinal shift analysis below, not for S7 itself.)"

**Problem**: S8-depth (Fixed-depth V-positions) is a single statement about V-positions sharing a common depth within a subspace; it neither references the element-field projection `E(a)` of I-addresses nor invokes S7c. The actual site that consumes S7c is the discussion of `shift(a, k)` on full I-addresses in S8's correspondence run definition — specifically: "For I-addresses, `shift(a, 0) = a` and `shift(a, k) = a ⊕ δ(k, #a)` for `k ≥ 1`. This is well-defined: ... — S7c guarantees element-field depth δ ≥ 2..." The action point at position `#a` falls strictly after the subspace identifier (at position `#a − #E(a) + 1`) iff `#E(a) ≥ 2`, which is what S7c supplies. S8-depth itself does no such analysis.

**Required**: Replace "S8-depth's ordinal shift analysis below" with a precise reference, e.g., "S8's correspondence run definition for I-address shifts" or "the subspace-preservation argument for I-address shifts in S8 below."

### Issue 2: S3's claimed dependency on NoDeallocation is unsubstantiated

**ASN-36, Properties Introduced table, S3 row**: "S3 | Referential integrity… | design; uses NoDeallocation (ASN-0034)"

**Problem**: The body of "The arrangement and referential integrity" does not invoke NoDeallocation. The maintenance analysis cites S1 — the closing sentence reads "What matters for persistence is that S1 guarantees once `a` enters `dom(C)`, it remains." NoDeallocation never appears in S3's discussion. The table entry's "uses NoDeallocation" lacks textual support.

**Required**: Either invoke NoDeallocation explicitly in S3's discussion (showing how the address-space-level no-deallocation guarantee underwrites referential integrity at the content-store level — at present S1 is what's actually cited) or replace the table's "uses NoDeallocation (ASN-0034)" with "uses S1."

### Issue 3: S7's cross-document uniqueness invokes GlobalUniqueness without an explicit allocation-event premise

**ASN-36, S7 Proof, "Uniqueness across documents"**: "Document tumblers are themselves products of the tumbler allocation scheme: a document is created by allocating a document-level address under the owning user's prefix. For documents `d₁ ≠ d₂` created by distinct allocation events, GlobalUniqueness (ASN-0034) guarantees their document-level tumblers are distinct."

**Problem**: The application of GlobalUniqueness requires document creation to be an allocation event within T10a's allocator tree. This commitment — distinct documents correspond to distinct allocation events — is introduced for the first time *inside* the proof. It is not a precondition of S7, not declared as a sibling axiom alongside S7a/S7b/S7c, and not derivable from any prior property in the ASN. S7a says only that *I-addresses* are allocated under their originating document's prefix; it does not say document-level tumblers themselves are allocated via T10a. Without this premise, GlobalUniqueness cannot be instantiated, and the uniqueness step has a formal gap.

**Required**: Add the missing commitment as an explicit precondition or sibling axiom — e.g., "documents are addressed by document-level tumblers (`zeros = 2`) allocated via T10a's discipline under the owning user's prefix" — and cite it where GlobalUniqueness is invoked.

### Issue 4: D-CTG's parametric statement and text-only restriction don't line up

**ASN-36, D-CTG, D-MIN statements**: D-CTG is written as a parametric quantifier over `V_S(d)` for any subspace S, then qualified in prose as "*Required only for `S = 1`.*" Likewise for D-MIN.

**Problem**: The formal statement `(A d, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : …)` quantifies over S implicitly through the predicate, but the design constraint applies only at `S = 1`. A reader who applies D-CTG to the link subspace (S = 2) would get a wrong conclusion — and nothing in the formal statement signals the restriction. The derived statements D-CTG-depth and D-SEQ inherit the same ambiguity, and the proofs of both invoke D-CTG without re-checking that the subspace under consideration is `S = 1`.

**Required**: Either bind `S = 1` directly into the formal statements (e.g., write the quantification over `V₁(d)` specifically), or add an explicit precondition `S = 1` to each statement (D-CTG, D-MIN, D-CTG-depth, D-SEQ) and to ValidInsertionPosition, which implicitly inherits the same restriction.

### Issue 5: Issue with j = m case argument in S8 uniqueness proof

**ASN-36, S8 Proof, "Uniqueness within a subspace", Case j = m**: "From `t < shift(v, 1)` with first divergence at `m`: `t_m < shift(v, 1)_m = v_m + 1` (NAT) by T1(i)."

**Problem**: The proof asserts that t and shift(v, 1) first diverge at m, but does not justify why m is the *first* divergence position between t and shift(v, 1) — it has only been established that m is the first divergence between t and v. The bridging argument is: tᵢ = vᵢ for i < m (by hypothesis on j), and shift(v, 1)ᵢ = vᵢ for i < m (by TumblerAdd's prefix rule, since the action point of δ(1, m) is m); therefore tᵢ = shift(v, 1)ᵢ for i < m, and (since t ≠ shift(v, 1) by the assumption t < shift(v, 1)) the divergence falls at m. This bridging step is left implicit.

**Required**: Insert one sentence between "Then `tᵢ = vᵢ` for `i < m`" and the T1(i) application: "Since `shift(v, 1)ᵢ = vᵢ` for `i < m` by TumblerAdd's prefix rule, we get `tᵢ = shift(v, 1)ᵢ` for `i < m`, so the first divergence between `t` and `shift(v, 1)` is at position `m`."

## OUT_OF_SCOPE

(No items. The Open Questions section appropriately defers operation-level behaviour, link-subspace semantics, version semantics, and implementation concerns to future ASNs, and the Scope section excludes them explicitly.)

VERDICT: REVISE
