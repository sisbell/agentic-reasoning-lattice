# Review of ASN-0091

This note carries the `review-mode.anti-bloat` classifier. I verified the substantive derivations and the five worked examples — the tumbler arithmetic, the pivot/swap postcondition applications, the fragmentation/coalescence/equality run counts, and the bijection-non-uniqueness trace all check out, and the abstract/concrete split (Vstream-only class realised by REARRANGE_K) is structurally sound. The findings below are accumulated meta-prose, which is what this cycle is asked to surface.

## REVISE

### Issue 1: Premise-avoidance commentary ("which route we did *not* take")

**ASN-0091, RE-subpres (Stage 1) and clause (iv) discharge**:
- "π's signature `π : dom(Σ.M(d)) → dom(Σ'.M(d))` (RA-π) places `π(v) ∈ dom(Σ'.M(d))` directly from the codomain, **with no appeal to RA-dom**."
- clause (iv): "**Discharged from the cut-sequence construction alone — not via the abstract RE-subpres**, which is a downstream consequence of RA-adm".

**Problem**: These clauses tell the reader which premise was *not* used. That is proof-hygiene commentary, not a step in the argument — `π(v) ∈ dom(Σ'.M(d))` stands on its own regardless of whether RA-dom could also have supplied it, and clause (iv) is established by its own construction whether or not RE-subpres exists. The reader must skip past the contrast to follow the actual claim.

**Required**: State the positive fact and stop. Drop "with no appeal to RA-dom" and "not via the abstract RE-subpres, which is a downstream consequence of RA-adm."

### Issue 2: Collapse-case thread is over-elaborated and repeatedly deferred

**ASN-0091, abstract section + realisation intro + clause table + RA-adm layer**: the net-effect-vs-`π≠id` distinction and the resulting "non-trivial case / collapse case" split is restated at five sites, each deferring to the others:
- "This makes π non-identity *as a permutation of V-positions*, but that is strictly weaker than ASN-0047's K.μ~ admissibility clause (ii)…"
- "the clause-by-clause argument below treats the non-trivial case…; the collapse case needs no clause discharge."
- clause (ii): "the defining condition of the non-trivial case; fails in the collapse case, where K.μ~ is not the realiser"
- "**In the collapse case the transition is the identity (per the case split above)**, so every invariant — including the composite-boundary P4a — holds trivially."

**Problem**: The collapse case is a legitimate logical case (a symmetric shared-address arrangement maps to itself under a non-identity π), and the S5 witness paragraph establishing it is genuine content. But its *payload* is "no realiser needed, `Σ' = Σ`, everything trivial" — a one-line triviality wrapped in repeated "(per the case split above)" deferrals across four sections. This is the cross-section deferral pattern the classifier names.

**Required**: Establish the case split once (the S5 witness paragraph), state the collapse case's triviality once at the point of use, and delete the back-references at the realisation intro, clause table (ii), and RA-adm layer.

### Issue 3: Stage scaffolding and exhaustiveness framing inside RE-subpres

**ASN-0091, RE-subpres derivation**: "The argument proceeds in two stages: first we constrain `subspace(π(v))` to the binary set `{s_C, s_L}`, and only then do we run the cross-direction case analysis…" and later "*Stage 2 — cross-direction exclusion.* **We argue both directions, since each is required to establish that** no V-position may cross from one subspace to another under any admissible π."

**Problem**: The proof is the binary constraint plus the two cross-direction exclusions plus the combination — all of which are present and correct. The "two stages," "first… and only then…," and "we argue both directions, since each is required to establish" sentences narrate the structure of a proof the reader is already reading. The "Combining the two stages" sub-paragraph then re-narrates the case combination a second time before stating the conclusion.

**Required**: Run the binary constraint, then the two exclusions, then conclude. Drop the stage-labelling preamble, the "since each is required" justification, and fold the conclusion into the last exclusion rather than a separate "Combining the two stages" recap.

### Issue 4: Post-definition re-narration of the Vstream-only class

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: immediately after the RA-reg/RA-π/RA-frame/RA-adm definition block, a full paragraph re-walks each clause — "RA-frame's `dom(Σ'.M) = dom(Σ.M)` propagates registration to Σ'… RA-dom pins the two domains equal… The defining equation RA-π then says… RA-frame fixes every state component apart from `Σ.M(d)`… RA-adm requires Σ' to satisfy each per-state foundation invariant…" — ending "The abstract class is genuinely 'Vstream-only on d.'"

**Problem**: This restates the definition just given, clause by clause, in prose. The genuinely new content in the paragraph (the bijection-non-uniqueness observation about shared I-addresses) is buried at the end behind the restatement.

**Required**: Cut the clause-by-clause re-narration; keep the bijection-non-uniqueness sentence, which is the only part that advances beyond the definition box.

## OUT_OF_SCOPE

### Topic 1: Joint reconstitution of a split transcluded span

**Why out of scope**: The transclusion section correctly defers "whether the two fragments *jointly reconstitute* the original source span" to Open Question 1. This is genuinely new territory (it concerns the algebra of fragmented transclusion views, not REARRANGE's per-step invariants) and is appropriately left to a future ASN rather than resolved here.

META: The ASN remains squarely on territory — it defines an operation, its state effect, and its invariants, abstractly enough that an alternative realiser would face the same RA-* obligations; the findings are accreted prose, not drift.

VERDICT: REVISE
