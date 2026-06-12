# Review of ASN-0120

The technical content of this revision holds up under checking. I verified the load-bearing chains in detail: the `wf`/δ-form equivalence (`#ℓ_j = #u_j ∧ actionPoint(ℓ_j) = #u_j` ⟺ ordinal displacement), the T5 prefix-confinement step that feeds S3★ and discharges `ρ(R,Σ) ⊆ dom(Σ.C)`, the expanded ρ/resolve agreement proof (the B1/B3 two-step is now an actual proof — domains coincide by definition of restriction, run-named addresses equal `ran(f)` by Coverage and Consistency), the recovery equation's two directions (the left-to-right F-trace-to-chain-run identification correctly routes through StoreT4Validity → TA5-SigValid before reading the merge identity backward; the TS3 induction handles k = 1 and k = 2 separately and composes only where both amounts are ≥ 1), the K.μ⁺_L precondition discharge at the intermediate state (S3★/S3★-aux evaluated at the pre-state, freshness against the whole store), ML9's Facts (a) and (b) including the `d' = d` boundary and the necessity direction of the wp equivalence, the J0/J1★/J1'★ vacuity claims, the contracted-home mixed-branch analysis in MLop, and the worked example's arithmetic and invariant checks (including K.μ⁻'s strict-contraction precondition and the post-edit trace). The empty-resolution boundary is settled per slot with the unique admissible record `e_j = ∅`, and ML6's necessity-and-sufficiency argument for `ρ(R₃,Σ) ≠ ∅` is exact. No proof gap, missing boundary case, or foundation misuse found.

What remains is residue of the most recent revision cycle, of exactly the kind the anti-bloat classifier flags.

## REVISE

### Issue 1: discharge and notation facts stated at two sites each (revision residue)
**ASN-0120, "The substrate we build on" / MLop / ML10**: Two instances of the same accretion pattern — a fact established once is restated at a second site with a cross-pointer back to the first.

(a) The arrow reservation. The substrate section establishes it: "We reserve `→`, as the foundations do (SequentialTransitionAxiom), for single elementary transitions; the composite ... is written `Σ →* Σ'`." MLop then restates it mid-contract: "the effect is the composite `Σ →* Σ'` — a ValidComposite★ of two named elementary steps, `K.λ` followed by `K.μ⁺_L`, **the arrow `→` remaining reserved for the elementary transitions themselves** — and its net effect is two entries." The bolded clause adds nothing at that point; it interrupts the contract sentence with a notational footnote already settled, and reads as a defensive trace of the elementary-vs-composite revision rather than part of the operation's definition.

(b) The J1'★ discharge. The substrate paragraph performs it in full: "J1'★ quantifies instead over new provenance entries `(a, d) ∈ R' \ R`, and `R' \ R = ∅`: both `K.λ` and `K.μ⁺_L` carry `E' = E ∧ R' = R` in their ASN-0047 frames (ML10)." ML10's body then states the same inheritance and the same connection again: "Σ'.E = Σ.E ∧ Σ'.R = Σ.R, inherited from the frames of K.λ and K.μ⁺_L (ASN-0047) — ... and the R' = R clause is what discharges J1'★ above," and the ML10 claim row carries it a third time ("the `R' = R` clause grounds J1'★'s vacuity"). The frame fact's home is ML10; the discharge belongs at the substrate paragraph where the coupling constraints are evaluated. Stating both facts at both sites, with mutual forward/back pointers, is the forward-reference accretion pattern this note is flagged for.

**Problem**: Two paragraphs in different sections saying the same thing, with cross-pointers in both directions; the pattern compounds across cycles if left in place.

**Required**: State each fact once at its proper site. Cut the arrow-reservation clause from MLop's effect sentence. Keep the J1'★ discharge in the substrate paragraph (which may cite ML10's frame), and reduce ML10's body to the frame fact itself, dropping the "is what discharges J1'★ above" back-pointer; the claim-row parenthetical can shrink correspondingly.

## OUT_OF_SCOPE

### Topic 1: Endset arguments referencing the link subspace (link pointing at link)
**Why out of scope**: The resolution machinery deliberately confines specs to the content subspace (`subspace(u_j) = s_C`); what MAKELINK must guarantee when an endset names another link is a genuinely new question about the record's well-formedness, correctly deferred by the ASN's second Open Question.

### Topic 2: Direct I-address endset arguments (ghost and foreign endsets)
**Why out of scope**: ML1/ML3 restrict this ASN to V-spec arguments, which provably produce only content-backed endsets; reaching L4/L9's full generality (ghost types, addresses outside the store) requires a distinct argument shape and is a separate operation surface, not an error here.

### Topic 3: Semantics of the empty non-type endset
**Why out of scope**: The ASN settles everything operational about the boundary — definedness, the unique admissible record `e_j = ∅`, legality under L3, and inertness in the discoverability test; what the degenerate one-sided link *asserts* is a semantic question properly left to the first Open Question.

VERDICT: REVISE
