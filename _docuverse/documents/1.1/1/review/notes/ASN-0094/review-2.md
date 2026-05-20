# Review of ASN-0094

## REVISE

### Issue 1: Sh-conf scope ambiguous (Emit_K vs K.λ)
**ASN-0094, The Conformance Axiom**: "The substrate restricts ASN-0086's Emit_K by adding two preconditions: Emit_K(Σ, d, F, G) succeeds iff K ∈ T_cat ∧ conf_K^Σ(F, G)."
**Problem**: In ASN-0086, Emit_K is a relational-layer operation; K.λ is the substrate primitive. The proofs of Sh0–Sh3 say "K.λ, which under Sh-conf succeeded only because conf_K^Σ(F, G) held" — but K.λ can in principle be invoked by any class-(iii) caller without going through Emit_K. If Sh-conf only binds Emit_K, the inductive step fails for any K.λ call that bypasses the relational layer.
**Required**: State explicitly whether Sh-conf binds K.λ directly (a substrate-level axiom on the primitive) or relies on the layer-level commitment that all class-(iii) emissions route through Emit_K. If the latter, the proofs of Sh0–Sh3 must cite that commitment as a precondition.

### Issue 2: Sh4 enforcement strategy not formalized
**ASN-0094, Idempotency (Sh4)**: "Sh4 is a layer-level discipline, not a substrate-enforced axiom. [...] Sh4 is realized by the calling layer: before emitting (F, G) into an idempotent relation, the layer first executes Observe_K(...); if a match exists, the emission is suppressed."
**Problem**: Sh4's formal statement is a universally-quantified property over A_K^Σ. The Observe-then-Emit pattern is suggested but not proven to maintain the property under arbitrary `↦*` transitions. Layer enforcement could fail in several ways (forgetting to check, race with retraction) without violating any substrate axiom. Without a formal preservation argument, downstream templates like `K_sidecar_of` are "conditionally well-defined" with no specification of when the condition fails.
**Required**: Either (a) lift Sh4 into Sh-conf as a substrate-enforced precondition (`reject Emit_K when shape(K).idem = ⊤ ∧ duplicate exists in A_K^Σ`), or (b) state a formal layer-discipline contract whose conformance implies Sh4, with an inductive preservation argument.

### Issue 3: AllocatedAddressAntichain Case 3 dependencies
**ASN-0094, Lemma — AllocatedAddressAntichain**: "By L1 (LinkElementLevel, ASN-0043) and ASN-0093's content-side analog, both x and a are element-level (zeros = 3). [...] L0 (SubspacePartition, ASN-0043) gives E(x).1 = s_L for links and ASN-0093 gives E(a).1 = s_C for content, with s_L ≠ s_C (SC-NEQ)."
**Problem**: The lemma's universal quantification is over `x ∈ A^Σ` without an element-level precondition, then proven by case-analysis that depends on (i) a content-side analog of L1 from ASN-0093, (ii) a content-side subspace identifier from ASN-0093, (iii) `s_L ≠ s_C` from a named axiom (SC-NEQ) in ASN-0093. None of these are in the foundation. The lemma also implicitly assumes `#E(x) ≥ 1` for both kinds, which requires the content-side analog of L1b.
**Required**: Either lift the content-side disciplines into stated preconditions on the lemma (e.g., "Assume every `a ∈ dom(Σ.C)` satisfies `zeros(a) = 3`, has element-field length ≥ 2, and has `E(a).1 = s_C ≠ s_L`"), or use only ASN-0043 + ASN-0086 concepts.

### Issue 4: Cross-ASN references to ASN-0093 throughout
**ASN-0094, multiple sites**: References to ASN-0093 appear in AllocatedAddressAntichain, the Coverage walkthrough's emission_order discussion, SubstrateConformingLayer scaffolding via Sh-conf, and the Open Questions.
**Problem**: ASN-0094 cites ASN-0093 explicitly (e.g., "ASN-0093 — ChainEnumerationInjectivity"). Foundation list is ASN-0034, ASN-0043, ASN-0086. While ASN-0086's vocabulary mentions ASN-0093 invariants for its own scaffolding, ASN-0094 should not reference ASN-0093 directly — it should consume those properties via ASN-0086's interface or state them as preconditions in its own definitions.
**Required**: Replace direct ASN-0093 references with either (i) a one-paragraph "substrate scaffolding assumed" preamble stating the content-side properties used (analogs of L1, L1b, the subspace identifier `s_C`), or (ii) consume them through ASN-0086's `SubstrateConformingLayer` definition without naming ASN-0093.

### Issue 5: Multi-arity scope not declared
**ASN-0094, body**: The ASN never states that the shape framework applies only to arity-3 (standard-triple) links.
**Problem**: ASN-0086 defines `L^Σ` as collecting only arity-3 links and explicitly says "higher-arity links in dom(Σ.L) are outside its scope." The shape framework inherits this — `conf_K^Σ(F, G)` is a binary predicate over `(F, G)`, with no provision for a third or fourth endset. But the body reads as if shapes apply to all of `dom(Σ.L)`, which would include the higher-arity links L3 admits. A reader could reasonably ask "what is the shape of a 5-ary link?" and find no answer.
**Required**: Add a scope statement in the framework's opening section: "This framework restricts the standard-triple slice `L^Σ` only; higher-arity links in `dom(Σ.L)` are outside scope." Optionally, note whether and how the framework could be extended to higher arities.

### Issue 6: Worked example shows only successful emissions
**ASN-0094, Worked Example: K = comment**: Four emissions all succeed; the "edge case" only covers retraction.
**Problem**: The example never exercises Sh-conf rejection. The rejection cases are what give Sh-conf its teeth: non-canonical F (e.g., a span of length > 1), `|slot_addrs(F)| = 2` against `c_F = 1`, slot address outside `A_doc^Σ`, K ∉ T_cat. Without showing these, a reader cannot verify that Sh-conf actually fires when it should, or what the failure mode looks like (silent reject, exception, etc.).
**Required**: Add at least two rejection cases to the worked example. Suggested: (i) attempted Emit with `F = {(d_1, δ(2, #d_1))}` — non-unit-depth span violating canonical form; (ii) attempted Emit with G targeting an unallocated address — violating `X_G ⊆ A_doc^Σ`. Show what state the substrate is in after the rejection (presumably unchanged).

### Issue 7: Sh0/Sh1 verification in worked example is hand-wavy
**ASN-0094, Worked Example, Sh0–Sh3 paragraph**: "Sh0–Sh3 hold at Σ_2 by direct check. L_K^{Σ_2} = {τ_1, τ_2}. Both tuples have F and G canonical-slot, slot-cardinality 1, and slot-addresses in A_doc^{Σ_2} (the allocated-set has not shrunk). Sh0/Sh1 give the canonical-form-and-cardinality property; Sh2/Sh3 give the target-domain inclusion. ✓"
**Problem**: This is a "by direct check ✓" without showing the check per tuple. For an example whose purpose is to verify the framework against a concrete instance, this is precisely the spot where the check should be explicit.
**Required**: Show per-tuple verification — e.g., "τ_1: slot_addrs(F_1) = {d_1}, |{d_1}| = 1 ✓ match(1, c_F = 1); slot_addrs(G_1) = {d_2}, |{d_2}| = 1 ✓ match(1, c_G = 1); {d_1} ⊆ A_doc^{Σ_2} ✓; {d_2} ⊆ A_doc^{Σ_2} ✓. τ_2: ..." Two short cases.

### Issue 8: Coverage shape from-slot semantics under-explained
**ASN-0094, Per-Shape Template Walkthroughs, Coverage**: "Coverage — (1, 1, A_doc, A_doc, ⊥). For K with this shape, multiple emissions targeting the same document d are expected (e.g., evolving review status)."
**Problem**: The walkthrough explains the to-slot (the document being covered) but not the from-slot. Who is the "from" in a coverage tuple? The reviewer? The reporter? The `latest_K_for_addr` template doesn't use the from-slot at all, leaving its purpose unclear. A reader cannot tell what cardinality-and-target constraint on the from-slot is supposed to capture.
**Required**: State the from-slot's semantic role for Coverage relations (e.g., "the from-slot identifies the document whose state caused or witnessed this coverage update"), or explain why a non-trivial from-slot is required if templates don't consume it.

### Issue 9: Comment-Resolution co-registration not formalized
**ASN-0094, Per-Shape Template Walkthroughs, Comment**: "The predicate template depends on a separate Resolution relation K_res of Resolution shape (see below). [...] resolved_by(τ, K_res) ≡ (E ρ ∈ A_{K_res}^Σ :: to₁(ρ) = addr(τ))."
**Problem**: `unresolved_K_comments(d)` takes K_res as an implicit parameter, but the framework has no mechanism for registering "the Resolution relation paired with K". Multiple Resolution relations could exist for the same Comment relation; which one does `unresolved_K_comments` consume? If K_res is left as a free parameter, the predicate signature is `(K, K_res, d) → ℘(...)`, not `(d) → ℘(...)` as written.
**Required**: Either (a) formalize per-K co-registration: extend the shape registry so a Comment-shaped K declares its companion K_res; (b) make K_res explicit in the template signature: `unresolved_K_comments_via(K_res, d)`; or (c) define a default "any active Resolution targeting τ resolves it", with a clear statement of what counts.

### Issue 10: Conformance monotone-discharge argument leans on unstated content-store monotonicity
**ASN-0094, Definition — Conformance**: "These sets grow monotonically along ⊑̂: Σ ⊑̂ Σ' entails A^Σ ⊆ A^{Σ'} and analogous for the partition sets (by L12a, ASN-0043, for dom(Σ.L) and the symmetric content-side claim from ASN-0093 for dom(Σ.C))."
**Problem**: Same dependency issue as Issue 3. ASN-0094's monotonicity argument requires `dom(Σ.C) ⊆ dom(Σ'.C)`. ASN-0043 supplies only L12a for `dom(Σ.L)`. The content-side analog is attributed to ASN-0093 without being stated.
**Required**: State the assumed content-store monotonicity as a precondition (or invariant) of the framework, separate from ASN-0093 reference.

## OUT_OF_SCOPE

### Topic 1: Higher-arity link shapes
**Why out of scope**: The framework's restriction to standard triples (arity 3) is appropriate; extending shapes to higher-arity links is a separate design problem that would need its own n-ary slot-conformance discipline.

### Topic 2: (0, 0) shape admission
**Why out of scope**: Mentioned in Open Questions. Whether a single-tuple existence flag without any from/to attribution belongs in the canonical catalog is a future design decision.

### Topic 3: Concurrency and cross-process registry consistency
**Why out of scope**: Mentioned in Open Questions. The shape framework is presented in a single-state-machine model; distributed coherence of the shape registry is a separate problem.

### Topic 4: Provenance c_G = 0|1 versus split shapes
**Why out of scope**: Mentioned in Open Questions. Whether to keep the optional accessor pattern or split Provenance into two shapes is a design refinement, not a soundness issue.

### Topic 5: Composite shapes
**Why out of scope**: Mentioned in Open Questions. Whether the framework needs a new axis for shapes whose F/G are constrained by other relations is exploratory.

VERDICT: REVISE
