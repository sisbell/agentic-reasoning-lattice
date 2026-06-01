# Review of ASN-0086

I checked the major proofs (R0, R0a, L-ContiguousPrefix, R-Scope, R7a, and the wp Case 2 derivation) against the foundations. The mathematical core is sound: R0a's two-case split (cross-home zero-counting vs. same-home chain-contiguity) holds, the antichain feeds R-Scope and the wp correctly, and the worked example's tumbler arithmetic is internally consistent (a₁=1.0.1.0.1.0.2.1 through a₃=...0.2.5 check out). The findings below are accretion/citation issues, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Rationale/status meta-prose in the Unit-depth retraction discipline definition
**ASN-0086, Definition — Unit-depth retraction discipline**: "The P1 qualifier is essential: because P1 does not gate emission... The discipline therefore constrains both shape and target membership... The discipline is a layer commitment, not a substrate guarantee: a direct K.λ caller can emit a crafted-span retraction that is L-invariant-conforming yet violates it — K.λ fixes emission *address* but not endset *shape*."

**Problem**: The definition's actual content is one clause ("every `L_R^Σ` tuple has a to-endset `{(b, δ(1, #b))}` for some `b ∈ A_rel^Σ`"). The surrounding three sentences explain *why the qualifier is needed* and *what status the discipline has* rather than advancing the definition. This is the "new prose around a definition explains why it is needed rather than what it says" pattern. The substantive content (the address-vs-shape gap) is re-asserted again in the wp section's "Substrate-conformance alone is insufficient" paragraph, so it does load-bearing work only there.
**Required**: Reduce to the one defining clause plus the P1-confinement note; move the address-vs-shape rationale to its single load-bearing use site in the wp domain-restriction argument.

### Issue 2: Redundant conformance scaffolding and duplicated witness deferrals
**ASN-0086, Definition — substrate-conforming layer / Lemma — K-Step Conformance Preservation**: the layer definition restates clauses (a)–(c) of *Definition — substrate-conforming state* at the layer level, and K-Step Conformance Preservation's proof is a one-line trajectory-append ("appending the conformance-preserving step ... extends that trajectory").

Additionally, both *Definition — state-local-conforming state* ("its rightmost inclusion is strict, witnessed by the NestedLinkWitness construction above") and *Definition — substrate-conforming state* ("the converse fails, witnessed by the NestedLinkWitness construction above") close by deferring to the same Remark for the same structural fact (strictness of the conformance hierarchy).

**Problem**: Multiple paragraphs deferring to one location, plus a definition-level restatement of clauses already stated. These are the "multiple paragraphs defer to the same downstream location" and "paragraph looks like content relocated rather than removed" patterns.
**Required**: State the conformance clauses once; have the layer definition cite them rather than re-list. Cite the NestedLinkWitness strictness once and reference it from the second site.

### Issue 3: Properties-table derivation notes under-name premises
**ASN-0086, Properties Introduced table**: `R6c ... (= R6a)`; `R5 ... (= L4(c) + L13)`; `R-Scope ... (= R0a antichain + K.λ freshness)`.

**Problem**: The table presents these "=" notes as the derivation index, but they omit load-bearing premises that the actual proofs use. R6c's induction invokes **R3** at every step to carry `(a, F, G) ∈ L_K^{Σ_{k+1}}` forward — "(= R6a)" alone is insufficient (R6a only preserves nullification, not slice membership). R5's proof additionally consumes L1, L1b, OrdinalDisplacement, T12, and PrefixSpanCoverage. R-Scope's proof additionally relies on P1 (`a ∈ dom(Σ.L)`) and L12a. A reader using the table as the citation summary would miss these.
**Required**: Correct the shorthand to name all premises (at minimum add R3 to R6c), or drop the "=" notes and point to the proof bodies.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations `L_K^{(n)}` and multi-arity retraction
The note restricts `L^Σ` to standard triples and notes higher-arity links "admit an analogous construction." The open questions already defer this; it is new territory, not an error here.

### Topic 2: Concurrency / atomicity of Observe relative to Emit
The active/audit consistency model under concurrent observation is correctly deferred to the Open Questions; R0a and the chain lemmas assume the single serialized commit path that frontier-landing encodes.

META: The note is a relational re-presentation of the ASN-0093 link store — Emit_K *is* K.λ, Nullify *is* K.λ with fixed arguments, and the retraction discipline is self-described as a layer convention — so it adds derived views and a layer protocol rather than new substrate state/operations, but its active/audit invariants (R6a–c) are genuine and internally sound, so it is incomplete-and-trimmable, not off-track.

VERDICT: REVISE
