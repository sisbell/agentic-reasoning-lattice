# Review of ASN-0126

The formal core is sound. I verified the projection bridge, the weakest-precondition derivation (gate vs. landing, with the five-conjunct result), P3/P5/P6, and the address arithmetic of the worked illustration — including the born-nullified witness, where `a_R = ...2.3 ∉ coverage(G_rng)` but `g = ...2.4 ∈ coverage(G_rng)` correctly forces the citation out of `A_citation^{Σ₂}`. The wp also correctly absorbs `K ∈ T_admissible` and the L3 non-empty-type-slot clause into "K registered" via C0. No correctness defect found.

This note carries `review-mode.anti-bloat`, and the residual findings are exactly the accretion the classifier targets: forward-reference duplication and defensive prose around an otherwise clean argument.

## REVISE

### Issue 1: `π(Σ_init) = Σ_init^{0086}` stated twice, with mutual cross-reference
**ASN-0126, The shape-gated emit / Registry permanence**:
- The shape-gated emit: "by the Σ_init construction (Registry permanence), π(Σ_init) = Σ_init^{0086} exactly"
- Registry permanence: "forgetting the registry recovers ASN-0086's own initial state exactly, π(Σ_init) = Σ_init^{0086} — the fact the projection bridge above (The shape-gated emit) invokes."

**Problem**: The same equation is asserted in both sections, each deferring to the other — a forward reference from the earlier section paired with a back-reference from the later. This is the flagged pattern "multiple paragraphs in different sections defer to the same downstream location," compounded by verbatim duplication of the equation. A reader following the induction base in The shape-gated emit is sent forward to a section that sends them back.

**Required**: State the construction and the equation once, in Registry permanence (where `Σ_init` is defined), and let The shape-gated emit cite it without restating. Alternatively, lift the one-line `Σ_init` construction ahead of its first use and drop the duplicate assertion.

### Issue 2: R5(c) cited as a redundant second exclusion witness
**ASN-0126, Single-source**: "`Emit_K` is total over `Endset × Endset` and `∅ ∈ Endset`, so `Emit_K(Σ, d, ∅, G)` is a legitimate ASN-0086 invocation with no `→_sh` image, and R5(c) (TupleSelfTargeting, ASN-0086) is a *proven lemma* constructing the empty-from tuple `(∅, G_self, K)`, equally excluded."

**Problem**: "Excludes *every* empty-from emit" is immediate from `|F| = 1` alone — any `F = ∅` has `|F| = 0 ≠ 1`. The witnesses serve only to show the exclusion is non-vacuous (ASN-0086 *admits* such emits). One witness — `Emit_K`'s totality — does that. The R5(c) clause is a second illustration of the same point, an exclusion inventory that does not advance the argument.

**Required**: Drop the R5(c) clause.

### Issue 3: Defensive and redundant prose
**ASN-0126, Registry permanence**: "To show it never drifts we must reconcile it with the transition relation rather than merely assert permanence."
**Problem**: "rather than merely assert permanence" is a defensive flourish justifying that a proof follows; the sentence's work is done by the frame-condition extension immediately after it.

**ASN-0126, The shape-gated emit**: the gate-vs-landing distinction is stated — "the gate ... *enables* the emit ... while the two inherited conjuncts ... govern *landing* — whether the deposited tuple reaches the *active* subset rather than merely the audit slice `L_K^{Σ'}`" — and then restated in the next sentence: "the gate (0)/(i)/(ii) governs only well-formedness and deposits the conforming tuple into the *audit* slice `L_K^{Σ'}`, while the third inherited conjunct ... is independent of the gate."
**Problem**: The mechanics (gate → audit slice; inherited conjuncts → active subset) appear in both sentences; only the narrowing from "two inherited conjuncts" to "the third inherited conjunct" is new content.

**Required**: Cut the defensive clause; collapse the two gate-vs-landing sentences into one that states the mechanics once, then narrows directly to the third conjunct that sets up "born nullified."

## OUT_OF_SCOPE

### Topic 1: A span-length-aware shape for single-tuple-scope retraction
The catalog measures G by span *count* only. Binary therefore admits a single non-unit G-span — the note flags this in Single-source ("a single G-span of non-unit length ... is equally Binary-conformant") and exercises it deliberately in the born-nullified illustration with `G_rng = {(g, δ(3, #g))}`. Consequently the substrate cannot *enforce* R-Scope's `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`; an app must voluntarily route through the unit-depth wrapper. A shape or predicate constraining span *length* (not just count) would let the substrate gate unit-depth retraction directly. This axis appears in neither the catalog nor the Open questions (Q6 covers arity and F-count, not span length).

**Why out of scope**: Span-length gating is a new measure, not an error in the present count-based catalog. The note states the limitation honestly; closing it is successor territory. Worth adding to the Open questions list so the successor inherits it.

VERDICT: REVISE
