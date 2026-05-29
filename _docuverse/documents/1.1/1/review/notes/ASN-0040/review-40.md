# Review of ASN-0040

## REVISE

### Issue 1: S2 breaks at the singleton zero tumbler
**ASN-0040, S2 (Trailing-Zero Stream Identity)**: "*Preconditions:* p ∈ T, p_{#p} = 0; p′ = [p₁, ..., p_{#p−1}]."
**Problem**: The only tumbler with `p_{#p} = 0` and `#p = 1` is `p = [0]`, which is in T. For it, `p′ = []` has length 0 and is not a tumbler (T0 requires `#p ≥ 1`), so `S(p′, 2)` is undefined and the identity `S(p, 1) = S(p′, 2)` is ill-formed. The proof silently assumes `#p′ = #p − 1 ≥ 1`. Boundary cases are mandatory; this one is unhandled.
**Required**: Add `#p ≥ 2` to S2's preconditions (or explicitly exclude `p = [0]`, noting `p′ ∈ T` is required). The downstream call sites (B1 sub-case C, B6 necessity (b)) already force `#p ≥ 2`, so the standalone property is the only thing that needs fixing.

### Issue 2: The "Relationship to ASN-0034's allocated set" section is a deferral essay
**ASN-0040, *The baptismal registry***: Bridge1 and Bridge2 are each labeled "forward requirement on activation discipline," and the surrounding prose ("The bridge has two parts, both forward requirements on the activation-discipline ASN…", "The activation-discipline ASN must arrange the alignment…", "The reverse inclusion … holds only under enforcement of the parent prerequisite").
**Problem**: Multiple paragraphs in this section defer to the same downstream location (the activation-discipline ASN) and to the parent-prerequisite open question. This is the flagged accretion pattern: prose that does not advance the present ASN's reasoning, handing obligations forward while reproving (Bridge1 uniqueness) inside the deferral. The reader must work around it to reach the substantive registry development.
**Required**: Reduce to the one load-bearing statement (`allocated(Σ) ⊆ Σ.B` is conditional on a future activation discipline) and drop the multi-paragraph rationale and the Bridge1 uniqueness proof, which belongs wherever activation is specified.

### Issue 3: B0 labeling justification is meta-prose
**ASN-0040, B0 (Irrevocability)**: "B0 follows from B0a: the partition forces … We state it as a labelled primitive because it is the registry analogue of T8 (AllocationPermanence)." Compounded by the Properties table: "primitive label (B0a-derivation given as commentary preceding the B0 statement, not as a labelled corollary)."
**Problem**: This justifies a document-structure/labeling decision (primitive vs. corollary) rather than advancing the claim. The "registry analogue of T8" framing is rationale, not content.
**Required**: State B0 (or derive it from B0a once). Remove the meta-commentary about why it carries the label it does, in both the body and the table.

### Issue 4: B4 placement justification is meta-prose
**ASN-0040, Bop / B4**: "Because B4 governs how Op is built rather than what a caller passes in, it is listed as a structural assumption on Op rather than as part of Bop's PRE."
**Problem**: Pure slot-placement justification — it explains where B4 is filed, not what it asserts. Flagged accretion pattern (essay justifying structural placement).
**Required**: List B4 as a structural assumption and delete the sentence explaining why it is not in PRE.

### Issue 5: The "mutually recursive / joint induction" scaffolding in Bop is unnecessary
**ASN-0040, Bop proof**: "The four obligations are mutually recursive: well-definedness appeals to B1 …; B1's preservation in turn appeals to Bop's postcondition; … We present the per-step arguments here as components of one joint induction over Σ_init →* Σ … with the dedicated §B1, §B10, §B_fin, §B_type proofs below carry[ing] the respective single-step preservation arguments."
**Problem**: The dependencies in fact stratify cleanly: B_fin depends only on B0a/B₀ conf.; B10 depends on B_fin and the self-contained §B6 sufficiency; B1 depends on B10; Bop correctness consumes all three. There is no genuine circularity — B1's inductive step uses only B1@Σ plus the *definitional* postcondition `Σ′.B = Σ.B ∪ {next}`, not Bop's full correctness. The "joint induction" framing overstates the entanglement and defers to four downstream sections. This is essay content about proof organization that the reader must skip past.
**Required**: Drop the mutual-recursion paragraph; let each invariant's section carry its own induction in dependency order, citing B_fin/B10/B1 as already-established when used.

### Issue 6: B9 quantifier defends against an out-of-scope concern
**ASN-0040, B9 commentary**: "In particular, B9 does not presuppose p ∈ Σ.B, and should not implicitly answer the parent-prerequisite question by tightening the quantifier." And: "The trace also illustrates that the unbounded-extent claim is structural, not an existence claim about distant or hypothetical states…"
**Problem**: Reviser drift — the first sentence argues about a parent-prerequisite case that B6/Bop already leave open (out of scope), defending the quantifier rather than stating the claim. The second is essay content restating what the constructive proof already shows.
**Required**: Remove both. The quantifier `(A p, d : B6(p, d) : …)` already says exactly what it admits; no defense against the parent-prerequisite reading is needed.

### Issue 7: Bop's frame condition is stated twice
**ASN-0040, Bop**: The FRAME line in the operation block ("This ASN makes no commitment about whether or how other components Σ carries … are modified across the same transition; their specification is left to the ASNs that introduce them") and the *Frame:* line in the Formal Contract repeat the same content in near-identical words.
**Problem**: Two passages saying the same thing — flagged duplication.
**Required**: Keep the Formal Contract *Frame:* line; reduce the in-line FRAME to a one-clause pointer or delete it.

### Issue 8: B6(iii) uniform-form parenthetical is a defense of notation
**ASN-0040, B6 sufficiency proof**: "(Condition (iii)'s uniform form `zeros(p) + (d − 1) ≤ 3` is ASN-0040's own bridging restatement: it collapses TA5a's two d-cases into a single bound that, combined with T4-validity of p, is equivalent to TA5a's case-based bound on d ∈ {1, 2}, but the uniform form is not itself part of TA5a.)"
**Problem**: This parenthetical explains why the ASN restates a foundation condition, rather than advancing the proof. It is rationale for a notation choice. (Substantively the restatement is sound — at `d = 1`, B6(iii) reduces to `zeros(p) ≤ 3`, redundant with T4 — but the defense of it is the noise.)
**Required**: Cite TA5a's bound directly for each `d`-case and drop the parenthetical.

## OUT_OF_SCOPE

### Topic 1: The reverse inclusion `Σ.B ⊆ allocated(Σ)` and the parent-prerequisite chain
**Why out of scope**: This depends on the ownership/activation model explicitly deferred (Tumbler Ownership, activation discipline). The ASN correctly identifies it as conditional; no claim is asserted here, so it is not an error — only the volume of deferral prose around it is (see Issue 2).

### Topic 2: The Occupied predicate and content/ghost distinction (B3)
**Why out of scope**: Content storage is deferred. B3 is correctly stated as a parametric forward requirement, not a current invariant. (The rationale paragraph "B3 separates two questions that might otherwise be conflated" is borderline essay content but light enough to leave.)

VERDICT: REVISE
