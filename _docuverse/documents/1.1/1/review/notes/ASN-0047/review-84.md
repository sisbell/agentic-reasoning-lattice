# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ specified in two places with different content
**ASN-0047, Elementary transitions and Decomposition of K.μ~ sections**: K.μ~ is introduced in the elementary-transitions catalogue as a "named composite K.μ⁻ + K.μ⁺," then re-presented with a full bijection-equation contract in the later *Decomposition of K.μ~* section.
**Problem**: Two distinct definitional treatments for the same construct. A reader following the elementary-transitions list must scan forward for the actual contract.
**Required**: One definition. Fold the bijection-equation contract into the first presentation, or state K.μ~ purely as the composition without a separate "contract" framing.

### Issue 2: "Note on..." subsections are pure meta-prose
**ASN-0047, Notation section**: Two subsections "A note on the relationship between subspace(v) and fields(a).E₁" and "A note on dom_C(M(d)) and V_{s_C}(d)" exist solely to note that two notations co-exist and are interchangeable.
**Problem**: Meta-prose explaining redundant notation. The reader learns nothing new from the notes; they exist to forestall confusion about which spelling to use.
**Required**: Choose one notation per concept, drop the other, eliminate the notes. If both must co-exist, define them once at first use without separate metadiscussion.

### Issue 3: "Frame consistency check" in K.μ~ is anti-bloat
**ASN-0047, Decomposition of K.μ~**: A paragraph titled "Frame consistency check" verifies that composing K.μ⁻ and K.μ⁺ frames yields the K.μ~ frame.
**Problem**: This is a sanity check that does not advance reasoning. K.μ~'s frame *is* the composition of its constituents — consistency is by definition, not by verification.
**Required**: Drop the paragraph.

### Issue 4: "Note on K.μ⁺ and P4★" is anti-bloat
**ASN-0047, Content-scoped containment and provenance**: A subsection explains when P4★ is restored at composite boundaries.
**Problem**: Explicit meta-prose. The P4★ preservation argument lives in the ExtendedReachableStateInvariants proof; this standalone note duplicates that argument.
**Required**: Drop the note.

### Issue 5: Withdrawal-mechanism gap referenced in 5+ sites
**ASN-0047**: The link-withdrawal/tombstoning gap is cross-referenced in: D-CTG★ amendment's "Consequence for link withdrawal," *Extended structural sufficiency* tombstoning gap, *Orphan links and coupling flexibility*, worked-example Step 5 counterfactual, and the canonical open question. The open question itself is tagged "canonical reference for the cross-site deferrals," acknowledging the proliferation.
**Problem**: Five cross-references to the same deferral. The "canonical reference" tag is itself meta-prose about the spread.
**Required**: One discussion at the point where D-CTG★ is introduced; drop the cross-references.

### Issue 6: Version-management deferral referenced 4+ times
**ASN-0047**: The "richer version contract... deferred to a subsequent version-management ASN" is referenced at the K.δ definition, the *Ghost-base versioning* paragraph, the S7d preservation note, and the ghost-base worked-example synthesis.
**Problem**: Cross-site deferral pattern. The same forward pointer appears at multiple sites.
**Required**: One deferral note at K.δ. Other sites should reference K.δ, not re-state the deferral.

### Issue 7: "Per-subspace S8 substitution lemma" + use-site reuse note
**ASN-0047, ExtendedReachableStateInvariants proof**: A lemma is named "Per-subspace S8 substitution lemma" with the explicit note "Each per-transition entry below cites this lemma rather than re-deriving the substitution."
**Problem**: The "lemma" content is two sentences: ASN-0036's S8 fails for link-subspace V-positions (they target dom(L), not dom(C)); use D-SEQ★(s_L) instead. The named-lemma framing + use-site reuse note is anti-bloat.
**Required**: Either inline the substitution at each use site or state it once without the lemma framing.

### Issue 8: Dispatch tables are use-site inventories
**ASN-0047, K.δ definition + Allocator hierarchy section**: Two large tables enumerate "Path 1/Path 2/Path 3" dispatch for K.δ freshness, and a separate table dispatches K.α/K.λ freshness obligations across cases.
**Problem**: Use-site inventories. The dispatch logic is a single design decision (T10a-tracked vs. ghost vs. protocol-axiom); enumerating per-case via tables creates redundancy with the per-case precondition list and the discharge prose.
**Required**: State the per-case precondition list and structural identity at K.δ. The Path classification can be stated once as a design fact.

### Issue 9: ValidComposite★ "two clauses serve different roles" is defensive
**ASN-0047, Scoped coupling constraints**: A paragraph after ValidComposite★'s definition explains "The two clauses serve different roles and must not be conflated... Clause (1) is what makes K.α precede K.μ⁺ when both occur... J0 does *not* impose this ordering."
**Problem**: Defensive prose justifying the definition's two-clause structure. If the definition is well-stated, the role distinction is self-evident.
**Required**: Drop the explanation paragraph; let the definition speak for itself.

### Issue 10: D-SEQ★ derivation Step 1 over-elaborated
**ASN-0047, Amendments to existing transitions**: The infinite-cardinality contradiction in Step 1 is broken into three sub-claims (i) pairwise distinctness, (ii) D-CTG★ membership, (iii) infinite subset.
**Problem**: Each sub-claim repeats content from the construction step. (i) follows trivially from u_M differing at position j+1; (ii) is one D-CTG★ application; (iii) is the cardinality of an injective image.
**Required**: One paragraph: "Each u_M ∈ V_S(d) by D-CTG★, the u_M are pairwise distinct by position j+1, so V_S(d) is infinite — contradicting S8-fin." Drop the labeled sub-claims.

### Issue 11: Cross-document disjointness chain proof over-elaborated
**ASN-0047, Allocator hierarchy under documents**: The proof has Case A (prefix-comparable) and Case B (prefix-incomparable), with B further split into (i) same-allocator siblings, (ii) cross-lineage allocators, (iii) mixed version/sibling configurations.
**Problem**: T10a.5 (cross-allocator) → T10 directly handles the cross-document case. The exhaustive sub-case enumeration of "which T10a sub-lemma fires for which allocator-pair configuration" is defensive.
**Required**: Condense to: "By T10a.{2,5} applied at the appropriate allocator-tree level, distinct documents have prefix-incomparable anchor prefixes. T10 then gives cross-document address distinctness."

### Issue 12: K.μ⁻ undefined at empty pre-state is implicit
**ASN-0047, K.μ⁻**: The text says `dom(M(d)) ≠ ∅` is "enforced by the effect clause itself, not a separately-stated precondition."
**Problem**: Implicit preconditions derived by logical observation (no proper subset of ∅) are fragile and easy to miss.
**Required**: State `dom(M(d)) ≠ ∅` explicitly in K.μ⁻'s precondition list.

### Issue 13: Empty endset (F, G) semantics not specified
**ASN-0047, L3 and Endset definition**: `Endset = 𝒫_fin(Span)` admits ∅. L3 requires Θ ≠ ∅ but not F or G. So `Link = (∅, ∅, Θ)` is admissible.
**Problem**: A link with empty from/to endsets has unspecified semantics. The ASN does not address whether such a link is a degenerate "type-only marker," a structural error, or a deliberate construct.
**Required**: Either specify the semantic interpretation of empty F/G, or constrain them to be non-empty.

### Issue 14: L1c axiom content fuzzy
**ASN-0047, L1c**: Stated as "There exists a T4-valid document-level seed s and a T10a-conforming step sequence terminating at a." T4-validity is then discharged via T10a.4.
**Problem**: L1c's existential is what T10a-conformance *means*; restating it as a separate axiom is redundant. The relationship to SubAllocatorAxiom (which establishes the sub-allocator frontier) and to K.λ's first-link namespace discharge is not clearly delineated.
**Required**: Either drop L1c and rely on T10a + SubAllocatorAxiom directly, or state precisely what L1c adds beyond those.

### Issue 15: Worked examples enumerate invariants per step exhaustively
**ASN-0047, worked examples**: Each step's verification enumerates ~15-20 invariants (P0/P1/P2/P3★/P5★/P6/P7/P7a/P8/S2/S3★/S3★-aux/S4/S7a–d/S8a/S8-depth/S8-fin/S8/D-CTG★/D-MIN★/D-SEQ★/L0/L1/L1a/L1b/L3/L12/L14/L-fin/CL-OWN/CL-UNIQ).
**Problem**: ExtendedReachableStateInvariants already establishes uniform preservation. Per-step enumeration repeats the theorem's content.
**Required**: Verify only invariants the specific step plausibly affects (e.g., for K.μ⁻: D-CTG★, D-MIN★, S2, S3★). State that frame-preserved invariants follow by frame, citing the theorem.

### Issue 16: SubAllocatorAxiom's first-emission content not pinned to a tumbler value
**ASN-0047, SubAllocatorAxiom.Namespace**: States "the first address a produced by d's content sub-allocator satisfies a ∉ dom(C) ∪ dom(L) at the state of allocation" with `fields(a).E₁ = s_C`, `#E(a) ≥ 2`, `origin(a) = d`.
**Problem**: The axiom does not say *which* address is the first emission. The ASN's prose treats this as `[d.0.s_C.1]`, but the axiom's statement is consistent with any first-emission address meeting the four conditions. K.α's preconditions then implicitly rely on the [d.0.s_C.1] form without it being axiomatic.
**Required**: Pin the first-emission tumbler form explicitly, or admit non-determinism of the first emission and adjust downstream uniqueness arguments accordingly.

## OUT_OF_SCOPE

### Topic 1: Account-level k=1 versioning
**Why out of scope**: K.δ's precondition excludes this; the canonical open question correctly flags it as future scope.

### Topic 2: Concurrent / multi-protocol allocator soundness
**Why out of scope**: Concurrency is an implementation concern; the open question correctly defers the discipline.

### Topic 3: Tombstone / link withdrawal mechanism
**Why out of scope**: The withdrawal mechanism is a separate design question; the canonical open question correctly defers it.

### Topic 4: Version semantics (lineage acyclicity, version DAG)
**Why out of scope**: Version semantics belong to a deferred version-management ASN.

VERDICT: REVISE
