# Review of ASN-0099

I checked the two-phase factoring (image / findlinks), the match predicate and its individuation witnesses (F4 strengthenings/weakenings), the filtered/scoped forms, the union-of-single-slot-filters identity, and the preservation lattice (A1a, F8, F9, F9-λ, F11, F19, F15). I verified the foundation citations (all of ASN-0034/0036/0043/0047/0093/0098 are foundations — no illicit cross-references), and re-derived the worked example's six queries.

Findings:

- **Proofs are explicit, not hand-waved.** F13's existential-over-disjunction lift, F20a's three-step chain, the ⋃-of-single-slot-filters guard-collapse argument, and F9-λ's domain-split + freshness disjointness are all shown step-by-step. No "by similar reasoning," no checkmark-as-proof.

- **Edge cases are covered:** I=∅, empty link store, empty constraint set, empty scope, R disjoint from arrangement, d ∉ dom(M) (undefined), out-of-range slot (guard), empty slot endset, cross-subspace link images (Query 4), self/meta-links (ℓ_meta), and ghost I-addresses (math holds, semantics correctly deferred).

- **Correct restraint on overclaiming.** F11 asserts I-side persistence and explicitly proves the V-side analogue is *not* a theorem (K.μ⁻ can contract a V-position out of the arrangement), with Query 5 exhibiting exactly that divergence. This is the right Dijkstra-style discipline.

- **The two-lemma structure (ComprehensionInvariantUnderΣL / PerLinkInvarianceUnderValuePreservation) is load-bearing, not redundant** — the per-link weakening is genuinely required at K.λ, where the store grows but prior values are preserved, so the whole-store lemma cannot apply.

- **Anti-bloat scan:** I checked for the flagged accretion patterns (imagined excluded cases, relocated findings, axiom-rationale sub-paragraphs, multi-section deferrals, ordering justifications, consumer inventories). F4's individuation witnesses construct excluded cases *deliberately* to discriminate the design (this is requested wp/individuation depth, not reviser drift). The lone forward reference (F11→F19 "below") carries a substantive caveat. No paragraph forced me to skip meta-prose to follow a claim.

No correctness defect, missing case, undischarged conjunct, or unsupported "derived" claim found. The ASN defines a state-querying operation with its algebraic and stability invariants, stated abstractly enough that any implementation must satisfy them — it has not drifted into implementation mechanics.

VERDICT: CONVERGED
