# Review of ASN-0086

## REVISE

### Issue 1: Ghost prose from the removed Σ_D machinery — comparative "no restriction required" framing
**ASN-0086, R0a / Emit_K (two sites)**: "No external discipline restriction on the reachable trajectory is required." … "so `Emit_K` is a function over the full domain — no auxiliary discipline restriction is required." … "ASN-0093's K.λ contract enforces the sibling-frontier discipline as part of the substrate's primitive emission, so `Emit_K` is a function over the full domain."
**Problem**: The prior cycle removed Σ_D and the SFD predicate (per the declined-findings record). These sentences are its residue: they advance the claim by *contrasting against an absence* — telling the reader what is *not* needed rather than stating what holds. R0a should simply be unconditional; Emit_K should simply be total. The reader does not need to be told the removed hypothesis is gone. This is reviser drift (new prose explaining why something is unnecessary).
**Required**: State R0a as unconditional and Emit_K as a function over `Σ` directly. Delete the "no … restriction required" comparative clauses at all sites.

### Issue 2: Two definitions assert the same "every L_R tuple came from Nullify" property
**ASN-0086, Definition — Unit-depth retraction discipline** vs. **Definition — relational layer**: "every `L_R^Σ` tuple … was produced by a `Nullify(Σ, d_retr, b)` call." and "make 'every `L_R^Σ` tuple was produced by a `Nullify` call' a definitional property of the relational layer."
**Problem**: The same commitment is stated twice in different words across two adjacent definition blocks. The "Nullify-as-sole-`R`-producer discipline" paragraph re-derives what "Unit-depth retraction discipline" already names. Duplicate paragraphs compound across cycles.
**Required**: State the discipline once (the named Definition), and have the relational-layer commitment reference it by name rather than re-articulating the property.

### Issue 3: Forward policy essay embedded in the `nullified(Σ)` definition
**ASN-0086, Definition — Nullified**: "withdrawal of such non-tuple entities is recovered at higher layers via *classifier tuples* — e.g. an `L_retired` tuple targeting a document address, consumed through `Observe`, records the document's withdrawal without disturbing its `A_doc` address (R4) or arrangement (L12b)."
**Problem**: This is higher-layer policy narrative occupying a definition slot. It does not advance the meaning of `nullified(Σ)`; the set-builder is already fully specified by the preceding sentence. The same classifier-tuple point is also made in R4 Consequence (b) and R6 discussion — redundant essay content in a structural slot.
**Required**: The definition needs only the `a ∈ A_rel^Σ` restriction and its rationale. Cut the `L_retired` excursion (or relocate to a single Consequences bullet).

### Issue 4: Use-site catalogs and "load-bearing site" meta-prose around the conformance definition
**ASN-0086, Definition — substrate-conforming layer / R7a**: "The individual lemmas are cited at the proof step that consumes them." … "This is the load-bearing site for clause (b) — the frontier-emission condition — of substrate-conformance."
**Problem**: "Cited at the proof step that consumes them" is a deferral that carries no content — it tells the reader the citations are elsewhere. The "load-bearing site for clause (b)" paragraph narrates *why a clause is needed* rather than proving the step; its genuine content (the `a* = [d.0.s_L.1.1]` counterexample showing clause (b) is non-redundant) is buried inside the meta-framing.
**Required**: Drop the "cited at the proof step" sentence. Keep the `a*` counterexample as a one-line necessity remark; delete the surrounding "this is the load-bearing site / clause (a) alone is insufficient" framing.

### Issue 5: R7a's conclusion is largely definitional given clause (b)
**ASN-0086, R7a + Definition — substrate-conforming layer, clause (b)**: "Every fresh link key is emitted at its home document's sibling frontier — i.e., the layer preserves the ASN-0093 sub-allocator chain-discipline lemmas."
**Problem**: Clause (b) requires the layer to emit exactly as K.λ does. R7a then proves that such a layer's link-store effect decomposes into K.λ-steps. The conclusion ("no `Σ.L`-affecting mechanism outside class (iii)") is therefore close to assumed: a layer that emits only at the sibling frontier is, by construction, replaying K.λ. The substantive kernel — that *no class-(ii) content steps are introduced* and that multi-key composites interleave with exactly the required K.σ prefixes — is real, but it is obscured by the near-tautological framing of the headline claim.
**Required**: Reframe R7a so the headline is the substantive part (link-store change ⇒ a K.σ/K.λ replay introducing no content emission), and state plainly that the "outside class (iii)" exclusion follows directly from clause (b) rather than presenting it as an independently-earned result. Acknowledge that conformance is *defined* to include the chain discipline the conclusion relies on.

## OUT_OF_SCOPE

### Topic 1: Concurrency, atomicity, and observation consistency
**Why out of scope**: The interaction of `Emit` with concurrent `Observe`, atomicity of `A_K` transitions, and the consistency model are genuinely new territory (correctly listed under Open Questions), not gaps in this note's single-authority sequential model (SequentialTransitionAxiom is inherited).

### Topic 2: Cardinality bound of `nullified(Σ)` relative to `dom(Σ.L)`
**Why out of scope**: Whether unbounded retraction is permitted or a structural ratio must hold is a new invariant to be posed in a future ASN; this note's claims (R6a–R6c) are correct without it.

### Topic 3: Tightening L1b (`#E ≥ 2` → `#E = 2`) at the source
**Why out of scope**: R0a-Cor2 establishes `#E = 2` for the standard-triple substrate here; whether the *foundation* L1b should be narrowed is a change to ASN-0043/ASN-0093, not a defect in ASN-0086.

VERDICT: REVISE
