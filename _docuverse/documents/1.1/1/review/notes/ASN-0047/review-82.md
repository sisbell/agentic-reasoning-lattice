# Review of ASN-0047

## REVISE

### Issue 1: Broken forward reference to "Reconciliation with ASN-0043's L1c" paragraph
**ASN-0047, K.λ first-link case (in *Link allocation* section)**: "The L1c chain witness for this first-emit case is exhibited in full at the *Reconciliation with ASN-0043's L1c* paragraph in the *Allocator hierarchy under documents* section above"
**Problem**: The cited paragraph does not exist. The "Allocator hierarchy under documents" section contains paragraphs on b_C(d)/b_L(d) structural producibility, SubAllocatorAxiom, the dispatch table, and the cross-document disjointness lemma — but no paragraph titled or matching "Reconciliation with ASN-0043's L1c". Additionally, the chain witness `d → inc(d, 2) = b_C(d) → inc(b_C(d), 0) = b_L(d) → inc(b_L(d), 1) = ℓ` is exhibited *inline* in the K.λ first-link case itself, making the deferral both broken and redundant. The reference appears twice in this paragraph ("at the Reconciliation paragraph" and "L1c's structural-chain existential ... at the Reconciliation paragraph").
**Required**: Either add the cited paragraph or remove the references and let the inline exhibition stand as the chain witness.

### Issue 2: "Why the axiom is needed" parenthetical in K.λ first-link case
**ASN-0047, K.λ first-link case**: "(T10a cannot supply this guarantee in the first-link case: `b_L(d)` is a virtual anchor with no inc-history, and the document `d` cannot spawn two sibling sub-allocators by a single inc(d, 2) operation under T10a's at-most-once constraint.)"
**Problem**: The parenthetical explains *why SubAllocatorAxiom is needed* rather than *what K.λ does*. This pattern is explicitly flagged in the review prompt's anti-bloat note ("new prose around an axiom explains why the axiom is needed rather than what it says"). The same justification then appears again in the "Allocator hierarchy under documents" section ("T10a's at-most-once spawning constraint prevents deriving the operational existence of two simultaneously-active sub-allocator frontiers from a single spawning event at d"), making it a multi-location justification of the axiom's necessity.
**Required**: Remove the parenthetical from K.λ; the necessity argument belongs in (at most) the SubAllocatorAxiom site itself, not at every consumer.

### Issue 3: Sequential-semantics premise paragraph duplicates open-question content
**ASN-0047, K.δ definition, *Sequential-semantics premise on Path 2 freshness***: "Path 2's `e ∉ E` discharge — TA5 determinism fixes the candidate as `inc(t, k)`, K.δ's precondition then verifies its absence from E by inspection — is sound under the single-event sequential semantics this ASN assumes... Concurrent or multi-protocol scenarios... fall outside this ASN's transition model; their treatment... is deferred to the open question on concurrent allocation below."
**Problem**: This paragraph is defensive justification that the discharge mechanism is sound *under stipulated semantics*, with explicit handoff to the open question. The same concern then appears as an open question ("Under what discipline can K.δ's Path 2 freshness discharge ... remain sound when concurrent or multi-protocol entity allocations may emit candidates..."). Both should not exist; the paragraph imagines cases the ASN's transition model already excludes, then defers them.
**Required**: Remove the paragraph; the open question already captures the concern at the appropriate location.

### Issue 4: L14a amendment subsection is multi-paragraph supersession justification
**ASN-0047, *Amendments to existing transitions*, L14a amendment**: A multi-paragraph treatment of why ASN-0043's L14a is superseded, including historical relationship, vacuous-satisfaction reasoning for the four-component scope, and the explicit non-retroactivity disclaimer.
**Problem**: Supersession of a foundation invariant deserves explicit treatment, but the present prose is essay-shaped: a paragraph of justification, then a paragraph clarifying the four-component scope, then an "appeal in this ASN" closing. The substance — S3★ + CL-OWN replace L14a in the extended state, ASN-0043's L14a is authoritative in its original scope — can be stated in 2–3 sentences.
**Required**: Compress to 2–3 sentences stating the replacement, the joint pair that supersedes it, and the non-retroactivity disclaimer.

### Issue 5: Asymmetry derivation (wp analysis) in Orphan links section
**ASN-0047, *Orphan links and coupling flexibility*, *Asymmetry derivation (wp analysis)***: Multi-paragraph wp essay enumerating invariants (P7, P4★, CL-OWN, L0–L14, L-fin) and showing K.λ holds each in frame, then commentary on Nelson's design "corroborating" the absence of a coupling.
**Problem**: The wp checks are mechanical and could be stated as a single sentence: "K.λ holds C, M, R in frame, so no invariant of the extended state requires every ℓ ∈ dom(L) to inhabit some arrangement, and the wp of K.λ is the identity on every invariant." The detailed enumeration of which invariants K.λ frames is a use-site inventory — the kind of "definition's introduction enumerates downstream consumers" pattern flagged in the anti-bloat note.
**Required**: Reduce to a single statement of the structural fact: no invariant forces coupling; the wp analysis is mechanical.

### Issue 6: Closing rhetoric in *Temporal decomposition*
**ASN-0047, last paragraph of *Temporal decomposition***: "Nelson captures the whole architecture in a sentence: 'The braid only grows more complex. It never unravels.' The existential and historical layers are the braid. The presentational layer is the current view of it."
**Problem**: Rhetorical closing, not formal content. The reader gains nothing once the table and P5 are in hand.
**Required**: Drop the closing.

### Issue 7: "Structural sufficiency and known gaps" enumerates use sites and caveats redundantly
**ASN-0047, *Structural sufficiency and known gaps***: The section is a consolidation of four enumerated gaps with cross-references to the worked example, the open questions, the K.δ definition table, and the *Allocator hierarchy under documents* section.
**Problem**: This consolidation is itself a "deferred-to" cluster — every gap points elsewhere ("deferred to *Allocator hierarchy under documents*", "deferred to the open question on withdrawal invariants", "tombstoning gap... see Step 5 counterfactual"). The pattern matches "multiple paragraphs in different sections defer to the same downstream location."
**Required**: Either inline the gap content here or remove the consolidating section; the four named gaps can be footnotes at their points of origin.

### Issue 8: "S8 discharge lemma" naming is misleading
**ASN-0047, *Class (a): Elementary per-state invariants*, *S8 discharge lemma***: "We therefore discharge S8 at the post-state Σ' by projecting M(d') onto its content-subspace restriction... and invoking ASN-0036's S8 on the projection."
**Problem**: The lemma does not *discharge* ASN-0036's S8 in its original form (which fails at the unprojected V-position set under link-subspace mappings). It substitutes a per-subspace decomposition: S8 over the content-subspace projection + D-SEQ★(s_L). "Discharge" suggests the original survives, which it doesn't — the link subspace falls outside S8's scope by the very obstruction the lemma exhibits.
**Required**: Rename to make the substitution explicit (e.g., "S8 substitution lemma" or "Per-subspace S8 decomposition"); state clearly that the unprojected S8 of ASN-0036 does not apply.

## OUT_OF_SCOPE

### Topic 1: Link withdrawal mechanism (tombstoning)
**Why out of scope**: Listed as an open question; the ASN correctly identifies that D-CTG★ admits only suffix truncations, making Nelson's tombstoning unexpressible. A separate withdrawal-mechanism ASN is the appropriate vehicle.

### Topic 2: Account-level k = 1 entity allocation
**Why out of scope**: Listed as an open question; the K.δ precondition's exclusion is documented as a deliberate scope decision pending account-versioning semantics.

### Topic 3: Concurrent or multi-protocol allocation under Path 2 freshness
**Why out of scope**: Listed as an open question; the ASN stipulates single-event sequential semantics and explicitly defers the concurrent treatment.

### Topic 4: Version lineage and arrangement transition relationship
**Why out of scope**: Listed as an open question; the ghost-base versioning worked example correctly notes that "the richer version contract... is deferred to a subsequent version-management ASN."

VERDICT: REVISE
