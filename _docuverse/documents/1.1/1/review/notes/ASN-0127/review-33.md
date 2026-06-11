# Review of ASN-0127

I checked every derivation independently: the four Phase-1 image lemmas, the Phase-2 algebra, the two-phase composite, the keystone meta-lemma and its per-link form, the operational consequences, both anchoring lanes, and every arithmetic step in the worked illustration. I also ran the anti-bloat scan the classifier requests. I found no defect that requires revision.

## REVISE

No issues. The verifications that support this:

**Phase 1.** F-IMG-MONO and F-IMG-CONTR are each proved by element-chase against the correct frame clauses, in both directions, not "symmetrically" asserted — F-IMG-CONTR shows its own chase. F-IMG-SWING's reindexing `v = π(u)` is sound: K.μ~-FIX makes π a self-bijection of `dom(Σ.M(d))`, the bijection equation substitutes correctly, and the index-set cardinality identity `|π⁻¹(W) ∩ dom| = |W ∩ dom|` follows because π restricts to a bijection between the two index sets. The injective-case transfer of cardinality from index sets to images is valid.

**F-IMG-TAX.** The shape dichotomy is exhaustive and exclusive for distinct sets; finiteness of the image (needed for "equal-size distinct sets cannot nest") is discharged from S8-fin rather than assumed. I re-derived all four witnesses component-by-component: the gain witness yields `{a} ↦ {a, b}`, the loss witness `{a, b} ↦ {b}`, the four-position witness `{a, b} ↦ {a, c}`, the injective witness `{a} ↦ {b}` — each consistent with both the direct post-state reading and the π⁻¹ formula. The admissibility paragraph genuinely discharges K.μ~'s conditions (i)–(v): the pinned domains are D-SEQ★-canonical initial segments at depth 2, value multisets are permutation-preserved (so the K.μ⁻ + K.μ⁺ decomposition is realizable with J0/J1★/J1'★ vacuous), the two-distinct-values precondition holds in every witness, S3★ holds pre- and post-state via allocator-grounded images and LP11 range preservation, and the note correctly derives domain fixity by construction rather than circularly invoking K.μ~-FIX.

**Phase 2 and composite.** F-UDIST's derivation (intersection distributes over union; existential over disjunction) is complete and correctly notes no step consults `I₁ ∩ I₂`. F-FULL's bridge to LP12 is an exact syntactic match of F-MATCH at `I = ran(Σ.M(d))`. F-VDIST correctly identifies why the unrestricted F-UDIST is load-bearing (disjoint regions, overlapping images under content sharing).

**Stability lane.** F-PRES's frame citations check against ASN-0047: every atomic transition except K.λ publishes `L' = L`, so "K.λ is the unique `Σ.L`-modifying transition" is right. F-LAMBDA's disjointness rests correctly on the freshness lemmas, and the prior-key contribution goes through F-CIL-perlink, which is proved concretely (arity equality plus per-slot coverage agreement), so the informal predicate class in F-CIL is never load-bearing on its own. E-CONS — the hardest proof in the note — is sound in both directions: the event/set-difference anchor is proved both ways (freshness pulled back and effect pushed forward through Store Monotonicity★; least-element extraction of the creating step, with K.λ-uniqueness forcing `a = ℓ_new`), the state-indexed match is warranted by E-INV on the suffix, and the exclusion direction correctly isolates the case that needs E-INV.

**Discovery lane.** D-ABSORB proves necessity and witnesses insufficiency with a fully grounded construction (link conformance L0/L1/L1a/L1c discharged via FirstEmission; ghost type unallocated since the store holds one link). D-CWP's bridge correctly reduces the post-image to `(Σ, R)`-quantities — `R ⊆ dom(Σ.M(d_q))` via D-SEQ★ makes the restriction's domain exactly `R` — and the biconditional `A = A ∪ B ⟺ B ⊆ A` is exact, so the "weakest precondition" label is earned. The `R = ∅` full-clearance boundary is handled, including why strict contraction is satisfied.

**Worked illustration.** I recomputed every slot intersection in all eight scenarios; all results match, including the structural premise (sibling prefix-incomparability via T10a.2; `a_θ` separated by T7 plus the Prefix length-gap argument with lengths pinned by FirstEmission and TA5(c)). The composite obligations are not hand-waved: the K.α bullet discharges J0 by embedding in a composite, and the rise bullet discharges J1★ via the standing provenance record (P4★ at the original boundary, carried by P2 across the contraction whose frame is `R' = R`) — a genuinely careful step. The D-CWP satisfied branch separates the wp from the cruder "no in-region drop" condition at both Δ-shapes (link-free and re-witnessed), which is exactly the depth the wp claim needs.

**Anti-bloat scan.** I examined the candidates: the F-IMG-SWING closing pointer to the adjacent F-IMG-TAX, the D-NONMONO reorder clause's injectivity/shape sentences, the D-CWP analog remark, and the E-CONS proof roadmap. On close reading each carries distinct propositional content (the injectivity/shape pair states two different links in the chain injectivity → shape availability → monotonicity behavior; the D-ABSORB parenthetical adds the insufficiency direction, not a repeat of the necessity clause). The deferrals are single instances to distinct, adjacent targets — not the accretion pattern. The worked illustration is concrete-example content, which the review mode explicitly protects. No reviser-drift paragraphs, no defensive axiom prose, no ordering justifications, no consumer inventories.

## OUT_OF_SCOPE

### Topic 1: Slot-indexed conjunctive query algebra (the ASN's Q2)
**Why out of scope**: which of F-UDIST/F-IMONO survive under per-slot filter sets is a different matching semantics; the ASN correctly delimits it rather than gesturing at it.

### Topic 2: Uniform stability wp across the whole K-vocabulary (Q3)
**Why out of scope**: D-CWP deliberately covers only the contraction instance; the uniform characterization is new territory, properly flagged open.

### Topic 3: Content-keyed queries through `Σ.C` and composition with ASN-0098's projection (Q1, Q4)
**Why out of scope**: both name compositions with other state components that this note's two-phase factoring intentionally excludes.

VERDICT: CONVERGED
