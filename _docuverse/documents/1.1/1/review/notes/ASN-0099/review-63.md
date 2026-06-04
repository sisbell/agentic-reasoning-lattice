# Review of ASN-0099

This ASN defines a genuine system operation (FINDLINKS) with abstract state-level guarantees — completeness, determinism, transclusion transparency, monotonicity. The mathematical core is sound; I found no correctness gap in the definitions or proofs. The problems are accretion: defensive framing, use-site inventories, redundant claim-variants, and admittedly non-load-bearing lemmas carrying heavyweight proofs. Per the `review-mode.anti-bloat` classifier, these are findings.

## REVISE

### Issue 1: F4's layered design-justification framing is meta-prose
**ASN-0099, "The Match Predicate" (F4 and its preamble)**: "F4 below is a *design justification*, not a uniqueness theorem... Two layers of prescription are at work — we surface them as commentary motivating F4"; "*Layer 1 — the user-facing guarantee (LM 2/46).*"; "*Layer 2 — the structural family (LM 4/58).*"; and the closing "The uniqueness asserted is *operational distinguishability* under F2 ∧ F3 wired with F1 — not mathematical uniqueness..."
**Problem**: The concrete witness links (Strengthenings 1–3, Weakenings 1–2) are legitimate content — they exhibit realizable pairs distinguishing F1 from alternatives. But the surrounding apparatus is defensive essay: the Layer-1/Layer-2 decomposition, repeated hedges about what F4 does and does not claim, and the LM 4/60 provenance paragraph ("is convergent with the overlap choice within (a) but is not its direct anchor — LM 4/60 governs the cross-link case... while spans-monotonicity ... is grounded in LM 4/58's per-endset existential structure itself") is pure citation-anchoring commentary that advances no claim. A reader chasing "why overlap, not containment?" must wade past the layering scaffold to reach the witnesses that actually carry the argument.
**Required**: Keep the witnesses and the single sentence stating F1 = per-endset overlap. Cut the Layer-1/Layer-2 framing, the repeated "design justification not uniqueness" hedges, and the LM 4/60 anchoring paragraph.

### Issue 2: Use-site inventory after the comprehension meta-lemmas
**ASN-0099, "Determinism and Comprehension Invariance"**: "F8 is the comprehension-level instance for F1's existential; F15 is the comprehension-level instance for the filtered universal; F17 and F18 invoke ComprehensionInvariantUnderΣL against the substitution... F11, F19, and F19-filt instead invoke the per-link primitive, since their hypotheses supply only per-link value preservation..."
**Problem**: This paragraph enumerates downstream consumers of the two lemmas rather than advancing their meaning — exactly the flagged "definition's introduction enumerates downstream consumers" pattern. Each consumer (F8, F11, F15, F17, F18, F19) already states which lemma it cites at its own site, so this is a redundant index that will rot as claims are renumbered.
**Required**: Delete the inventory paragraph. The per-claim citations are self-locating.

### Issue 3: A1 prose imagines K.σ, an operation the vocabulary already excludes
**ASN-0099, "Arrangement Independence"**: "ASN-0093's substrate operation K.σ is *not* in this vocabulary: it registers a document into `dom(M)` without touching `E`, so applied here it would produce a document in `dom(M)` but not in `E_doc`, violating M1 and P8; it belongs to the un-extended substrate `(C, L, M)` and is unreachable in this model."
**Problem**: A1's scope is fixed as V (ASN-0047's extended vocabulary), which does not contain K.σ. Reasoning about what K.σ "would" violate if "applied here" imagines a case the vocabulary definition already excludes. The surrounding paragraph similarly over-explains why K.μ⁺/K.μ⁻ use amended frames before A1a discharges all six operations uniformly.
**Required**: State the vocabulary V once (it is already restated in A1's "Vocabulary scope" clause). Drop the K.σ counterfactual.

### Issue 4: F9 family proliferation with redundant deferrals to one decomposition route
**ASN-0099, "Arrangement Independence" (F9, F9~, F9-cor, F9★, F9-λ)**: five named survivability variants, plus "(The K.μ-only specialization of F9★ is the one-line corollary... we do not name it separately.)" and repeated pointers to the same fact — "the F9★ composition (below)", "reached only through F9★ over its K.μ⁻ + K.μ⁺ decomposition (equivalently, F9~)", and again in F17/F18 "compose over its K.μ⁻ + K.μ⁺ decomposition (the F9~ route)."
**Problem**: The single load-bearing facts are (a) every V∖{K.λ} step preserves Σ.L and (b) K.λ adds exactly one possibly-matching link. The K.μ~-is-non-atomic-so-compose-its-two-steps observation is restated at F9, F9~, F9-cor, F9★, F17, and F18 — multiple paragraphs deferring to the same downstream location. The "we do not name it separately" parenthetical is meta-prose about a naming choice.
**Required**: Collapse to two claims (single-step invariance across V∖{K.λ}; the K.λ increment), state the K.μ~-decomposition handling once, and delete the "we do not name it separately" aside.

### Issue 5: F10a and ChainIndexEqualsAllocationOrder are admittedly interpretive yet carry foundation-grade proofs
**ASN-0099, "Result Ordering"**: "The two lemmas that follow — ChainIndexEqualsAllocationOrder and F10a — are *interpretive*... and play no role in establishing F10's ordering claim." Yet F10a Case (ii) then unfolds a four-step foundation proof (M0, T4, Prefix, M0+T0) to derive `d₂_{#d₁+1} ≥ 1`.
**Problem**: F10's existence/uniqueness is complete via "T1 is a total order on the finite subset" — the ASN says so explicitly. Two lemmas the ASN itself labels non-load-bearing then arrive with detailed citation chains supporting only the prose "Chronological reading" remark. That remark is an interpretation of presentation order, not a state guarantee an alternative implementation must satisfy. This is accreted machinery: heavyweight proof for an interpretive aside.
**Required**: Either reduce the chronological reading to a one-sentence remark with no formal lemma apparatus, or move the ordering-interpretation question to an OUT_OF_SCOPE/future note. Do not retain a multi-step foundation proof for a claim stated to play no role.

### Issue 6: F11's "Distinction from ASN-0098" duplicates the worked example
**ASN-0099, "Persistent Discoverability (I-Side)"**: the bulleted I-side-vs-V-side contrast ("*I-side (F11): persistent.* ... *V-side (ASN-0098): not persistent.*") and the following two paragraphs restate, in different words, what Query 5's narration already demonstrates ("The I-side query... returns `{ℓ}` at both `Σ` and `Σ_5`... The V-side query... returns `{ℓ}` at `Σ` but `∅` at `Σ_5`").
**Problem**: Two passages in the same document make the same point — the I-side/V-side divergence under K.μ⁻ — once abstractly and once concretely. The concrete Query 5 is the better carrier (it is the flagged-acceptable concrete example); the abstract bullets and the "A link is permanently I-side discoverable..." closing paragraph are the redundant restatement.
**Required**: Keep the one-sentence statement that I-side persistence holds while V-side does not, cite Query 5, and cut the duplicated abstract elaboration.

## OUT_OF_SCOPE

### Topic 1: Semantics of querying I-addresses outside dom(C) ∪ dom(L)
**Why out of scope**: The ASN correctly lists this under "What We Have Not Specified" and "Open Questions." It is new territory (ghost/unallocated query targets), not an error here.

### Topic 2: Combined filtered-and-scoped operation, partition/consistency model, access-control composition
**Why out of scope**: Each is correctly deferred in "What We Have Not Specified" / "Open Questions." These are future operations and protocol layers, not gaps in this ASN's guarantees.

VERDICT: REVISE
