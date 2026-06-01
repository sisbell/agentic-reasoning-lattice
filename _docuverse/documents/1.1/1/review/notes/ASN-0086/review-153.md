# Review of ASN-0086

I checked the proofs line by line. The mathematics is unusually solid: R0a's two-case decomposition (cross-home via zero-counting, same-home via L-ContiguousPrefix + uniform length), the L-ContiguousPrefix induction over conformance clauses (b)/(c), R7a's K.σ/K.λ replay with its four-part emission-selection discharge, and the worked sketch's tumbler arithmetic all verify. The L-invariant preservation in R0 is comprehensive — every `StateLocalInvariants` conjunct is accounted for, with S/M/C/D invariants frame-fixed and the L-conjuncts discharged individually. I found no missing edge case in the operation branches (first/subsequent emission, off-P1 Nullify, ghost/content targets all covered).

The remaining issues are the accretion patterns the `review-mode.anti-bloat` classifier asks me to surface, plus one structural redundancy.

## REVISE

### Issue 1: Lemma-proof embedded in a definition slot
**ASN-0086, Definition — Nullify**: the paragraph "*Single-tuple scope under R0a*" runs a full multi-step proof — establishing `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` via R0a applied to `dom(Σ'.L) = dom(Σ.L) ∪ {b}`, with sub-arguments that `b ≠ a` and `a ⊀ b`.
**Problem**: This is a lemma (it is then *cited* as a result by wp Case 1: "exactly the single-tuple scope result established in the Definition of Nullify"). Essay/proof content sitting in a structural definition slot is exactly the placement defect the anti-bloat pass flags — a reader must parse a proof to extract the operation's definition.
**Required**: Promote "single-tuple scope" to a named, labeled lemma (e.g., `R-Scope`) with its own contract; reduce the Definition of Nullify to the composition and its postcondition, citing the lemma.

### Issue 2: Meta-prose justifying what is novel vs. inherited
**ASN-0086, L-ContiguousPrefix proof**: "We record the →*-reachable case as a foundation fact, then extend it; the extension is L-ContiguousPrefix's sole added content over the foundation." and "*The genuine added content is that the same contiguity holds at every substrate-conforming state*..."
**Problem**: These sentences advance no reasoning — they narrate the proof's relationship to its foundation rather than proving anything. This is the "prose justifying document ordering / what is novel" pattern. The proof body (reachable case = ChainMembershipForOrigin; extension by induction on clauses (b)/(c)) stands on its own without the editorializing.
**Required**: Delete the two meta-sentences; the case split into "reachable case" and "extension to substrate-conforming states" already signals the structure.

### Issue 3: Unit-depth retraction discipline restated across three locations
**ASN-0086**: the discipline is fully specified in **Definition — Unit-depth retraction discipline**, then re-committed in **Definition — relational layer** ("Together these two commitments make the layer satisfy the *unit-depth retraction discipline*"), then re-justified again in the wp **Domain restriction** and **Substrate-conformance alone is insufficient** paragraphs.
**Problem**: The same layer-commitment-vs-substrate-guarantee distinction is explained three times in different words — the "two paragraphs in different sections say the same thing" pattern. The two wp *insufficiency witnesses* are load-bearing (each proves a restriction necessary) and should stay; the surrounding re-explanation of what the discipline *is* should not.
**Required**: State the discipline once; in later sites cite it by name and retain only the witnesses, not the re-exposition.

### Issue 4: R7a invoked where its conclusion is definitional
**ASN-0086, Relational layer corollary**: "Hence each relational-layer-issued transition `Σ ↝ Σ'` departs from a substrate-conforming Σ, satisfying R7a's added hypothesis... each relational-layer state-affecting operation is itself a single-step K.λ `→`-step."
**Problem**: For the relational layer, `Emit_K` is *defined* as K.λ specialized to `(F, G, K)`, so "each op is a single K.λ step" follows immediately from the Definition of Emit_K — R7a's decomposition machinery (K.σ interleaving, four-part emission-selection discharge) contributes nothing here. R7a's real value is for *arbitrary* substrate-conforming higher layers; its appearance in this corollary reads as heavyweight machinery applied to a trivial instance.
**Required**: Either state the corollary directly from Emit_K's definition and relocate R7a's motivation to the (genuine) general-layer use case, or add one sentence making explicit that R7a is exercised here only as the degenerate `m = 1` instance and is stated for the general case.

## OUT_OF_SCOPE

### Topic 1: Full-domain weakest precondition for Emit_K
The wp Case 2 result is explicitly scoped "over substrate-conforming Σ satisfying the unit-depth retraction discipline" — strictly narrower than Emit_K's declared state-local-conforming domain. The note honestly demonstrates (via two witnesses) that the formula *fails* on the broader domain, but does not derive the true wp there (which would have to quantify over arbitrary crafted-span coverage of the fresh address).
**Why out of scope**: Characterizing self-nullification under non-unit-depth retractions and nested-link pre-states is genuinely a separate analysis; the present note's restricted-domain wp is correctly labeled as such, so this is future territory, not an error here.

### Topic 2: L_K–arrangement interaction and Observe consistency model
The first and last Open Questions (relational predicates depending on document-visibility of from/to content; atomicity of Emit vs. concurrent Observe) concern coupling between `Σ.L` and `Σ.M`/concurrency that this note deliberately holds fixed (M2, empty arrangements).
**Why out of scope**: These require arrangement-modifying operations and a concurrency model neither this note nor ASN-0093 introduces.

VERDICT: REVISE
