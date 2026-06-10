# Review of ASN-0115

The mathematical content is sound. I checked every claim (R0–R11, the Confinement lemma, and the `act`/`depthcompat`/`item` definitions) and found no correctness gap: the override's too‑shallow/too‑deep behavior is consistent (too‑deep is empty by Confinement, override vacuous; too‑shallow is the case it bites), R6's no‑interior‑hole argument is honestly scoped to the bindable slice and correct under D‑SEQ★, R7's active‑set‑agreement handles the override and empty‑restriction sub‑cases, R8's link‑vacuity follows from CL‑OWN + CL‑UNIQ, and the worked instances (R6, R8, R9, R10, R11) check out arithmetically. Boundaries are covered (empty spec‑set, empty `act`, `s₁ ∉ {s_C,s_L}` collapses to `act = ∅`, orphaned content). All cross‑ASN references resolve to foundation ASNs.

The findings below are prose‑level, consistent with this note's `review-mode.anti-bloat` classifier: accreted meta‑prose that the precise reader has to work around.

## REVISE

### Issue 1: R7's proof is padded with non-advancing editorial asides
**ASN-0115, §"Repeatability" (R7 proof)**: the proof of repeatability carries several sentences that characterize the proof or re-state the conclusion rather than advance the argument:
- "The proof is short and exposes which input is the variable one." — the *next* sentence ("`deliver` is a function of two things…") does the actual framing; this one only characterizes the proof.
- "(This is the operative sub-case for the override: … which is non-empty in the too-shallow case `#s < m_S` the override exists to handle, yet `act = ∅` at each via the override.)" — the proof has already concluded `act = ∅` at both states; this re-explains the override's purpose (already given at the `act` definition).
- "The two item kinds now conclude by different routes, and the asymmetry is the point." — "the asymmetry is the point" is emphasis, not argument.
- "The labelling of the two states is immaterial — value-equality is symmetric — so naming the descendant `Σ'` costs no generality." — the WLOG was already declared in R7's statement ("without loss of generality `Σ →* Σ'`"); re-justifying it at the end is duplication.
- "The only mutable input to a content delivery is the arrangement; this is exactly why repeatability is conditioned on 'unchanged arrangements' and on nothing else." — closing editorial restatement of the established result.

**Problem**: This is the densest accumulation of meta-prose in the note. The genuine signposts in this same proof — "non-trivial because `act`'s depth-compatibility branch reads the *whole* subspace state of `dⱼ`" — flag a real subtlety and should stay; the five sentences above do not advance the reasoning and a reader must skip past them.
**Required**: Trim the proof to its advancing steps (active sets agree across the depth-compat / override / empty-restriction split; link items stable by address; content items stable by S0 over `Σ →* Σ'`). Drop the proof-characterizations, the redundant WLOG re-justification, and the closing restatement.

### Issue 2: stability rationale accreted around the `depthcompat` forward reference
**ASN-0115, §"What a spec-set is, and what delivery is" (V-spec definition)**: "Each condition defining a V-spec is *stable*: the structural conditions … make no reference to state at all, and the one state-dependent conjunct, `d ∈ dom(Σ.M)`, is monotone (ASN-0047, M1 ArrangementMonotonicity), so once `d` is allocated it stays allocated and the conjunct, once true, never lapses. We deliberately keep *depth compatibility* … out of well-formedness, precisely because it would *not* be stable … Depth compatibility is therefore a *consulting-state* predicate `depthcompat(ρ, Σ)`, defined below and applied inside `act`, where it is the sole depth check."

**Problem**: This is the forward-reference-accretion pattern the classifier targets: a multi-sentence "why the definition is shaped this way" essay wrapped around the single forward pointer to `depthcompat`/`act`. The stability/monotonicity sub-argument supports the permanent-citation narrative but is cited by no proof (R7 leans on `Σ →* Σ'` and arrangement-restriction equality, not on well-formedness stability), so it reads as rationale rather than load-bearing content. The operative takeaway is one sentence.
**Required**: Compress to the operative fact — depth compatibility is mutable (`m_S(d)` re-pins on insertion, ASN-0047), so it is a consulting-state predicate `depthcompat(ρ, Σ)` checked inside `act`, not a well-formedness condition. Keep "where it is the sole depth check" only if a later proof needs it.

## OUT_OF_SCOPE

I have no additional future-territory topics to add. The note's own Open Questions correctly capture them (straddling spans, dangling references under relaxed S3★, channel faithfulness, inline provenance, outright failure). I confirm the link-position "material" decision — delivering `⟨ref, a⟩` rather than the link's endset structure, with structure-reading deferred to READLINK/FOLLOWLINK — is handled explicitly in R10 and respects the operation boundary; it is correctly scoped, not missing.

VERDICT: REVISE
