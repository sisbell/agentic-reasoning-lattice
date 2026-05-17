# Review of ASN-0086

## REVISE

### Issue 1: R0a Case 2 invokes an unstated documents-antichain assumption
**ASN-0086, R0a proof, Case 2**: "by S7d (ASN-0036, applied at the document level) every document address d'' ∈ dom(Σ.M) has zeros(d'') = 2, and the document-allocator's T10a discipline (the standard substrate convention; the document-level analog of T10a applied to the document-allocator) makes dom(Σ.M) an antichain"
**Problem**: ASN-0036's S7d (the only document discipline statement in the foundation) gives `zeros(d) = 2` and "distinct documents arise from distinct allocation events" but does not preclude ancestor-descendant relationships between documents. A sub-document at `d.1 = inc(d, 1)` would have `zeros = 2`, arise from a distinct allocation event, and prefix-extend `d`. The "standard substrate convention" is invoked as a fact but is neither axiomatized in this ASN nor derived from the cited foundations. Worse, it is unnecessary: when `home(a) ≠ home(a')`, the conclusion follows directly from zero-count agreement. If `a ≼ a'` with both having `zeros = 3` (L1), then the extension `a' = a · w` has `zeros(w) = 0`, so the third zero of `a'` sits at the same position as the third zero of `a`, forcing `home(a') = home(a)` — a direct contradiction with `d ≠ d'`. No documents-antichain premise is consumed.
**Required**: Either (a) replace Case 2's argument with the direct zero-count argument above, or (b) explicitly axiomatize "documents in `dom(Σ.M)` are mutually prefix-incomparable" as a substrate convention in this ASN.

### Issue 2: The `s_C ≠ s_L` convention is invoked without formal statement
**ASN-0086, R0 Step 4 (L14 and L14a bullets)**: "Since `s_L ≠ s_C` by substrate convention, `subspace_I(a) = s_L ≠ s_C` excludes a from `ran(Σ.M)`"; "By the substrate convention `s_L ≠ s_C` and T3..."
**Problem**: The distinctness `s_C ≠ s_L` is consumed in R0 Step 4's L14a and L14 verifications, underlies R4's appeal to L14, and threads through R5's exhaustive check. The ASN refers to it as a "substrate convention" but never introduces it as an axiom alongside the Setup hypothesis, nor cites a specific clause in ASN-0036/0043 where it is fixed. Without explicit codification, the dom-disjointness chain (L14 → R4) and the L14a-preservation argument rest on an unstated premise.
**Required**: Either explicitly state `s_C ≠ s_L` as an axiom adjacent to the Setup hypothesis, or cite a specific foundation clause that fixes it.

### Issue 3: Emit_K does not commit to the sibling-frontier discipline
**ASN-0086, Definition — Emit_K**: "Given input state Σ and finite endsets `F, G ∈ Endset`, `Emit_K(Σ, F, G)` returns `(Σ', a)` where, by R0, `a ∉ dom(Σ.L)`, `a ∈ dom(Σ'.L)`, and `Σ'.L(a) = (F, G, K)`."
**Problem**: R0's existential is discharged constructively by Step 2 (sibling-frontier addresses), but R0's *statement* and the substrate emission primitive above it permit emission at any L1c-conforming-fresh-address — including, by the ASN's own admission under "Breadth of the primitive vs. the discipline R0a names," addresses of the form `a' = a₁.1` for existing `a₁ ∈ dom(Σ.L)`, which strict-prefix-extend `a₁` and falsify R0a's antichain. The worked sketch explicitly says "We invoke not R0's bare existential ... but R0's *Step 2 Case B construction*" — acknowledging that the bare existential is insufficient — yet the Emit_K definition itself does not bind that choice. Under the current Emit_K definition, a single non-disciplinary emission breaks R0a, and Nullify's single-tuple-scope argument fails because the post-state may contain an `a' ∈ dom(Σ'.L)` with `a ≺ a'`, putting `a'` into the to-set's coverage.
**Required**: Tighten Emit_K's definition to commit to R0 Step 2's construction (equivalently, to the sibling-frontier discipline) so R0a holds unconditionally on Emit_K-induced traces; alternatively, mark Emit_K itself as discipline-conditional and propagate that qualifier to Nullify's well-definedness.

### Issue 4: "Three emissions" in R6b's example, only two described
**ASN-0086, R6b "to see the distinction concretely" paragraph**: "consider three emissions at the same state. (1) Emit `(b, F', G_a, R)` ... (2) Emit `(c, F'', G_b, R)` ..."
**Problem**: The example announces "three emissions" but exhibits only (1) and (2). No third emission appears.
**Required**: Either correct "three" to "two", or add the third emission and its discussion.

## OUT_OF_SCOPE

### Topic 1: Higher-arity link nullification semantics
**Why out of scope**: The ASN explicitly scopes `L_K^Σ` and `A_K^Σ` to standard-triple links and gates Nullify on `|Σ.L(a)| = 3` (P2). The Open Questions section flags multi-arity extension as future work; that placement is correct.

### Topic 2: Invariants linking `L_K` to `Σ.M` (relational–arrangement consistency)
**Why out of scope**: Consistency between endset content in `L_K` and currently-visible content in `Σ.M` is a layered concern over both the relational vocabulary and ASN-0036's arrangement model. The Open Questions section already flags this; it does not belong here.

VERDICT: REVISE
