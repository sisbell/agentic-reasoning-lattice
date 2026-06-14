# Review of ASN-0133

The logic is sound. I checked Q0's PL-membership for the heterogeneous case (every view-sensitive constituent — the four view-parameterized atoms plus the four UV-rewritten behavior collections — does rebuild to a common term view via the fixed-view bases), Q1's absorption, Q3's idem=⊤ dedup-miss argument, Q5's injection, Q5a's bound, Q6's regime analysis (including the case (1)/(2)/(3) split and the H-SFAIR regime-form closure of case (3)), the SC scoping bodies with Q9's anti-monotonicity, and the worked cmt/res sequence. Each holds. The findings below are duplication and precision — which is what the `review-mode.anti-bloat` classifier is asking for on a note this mature.

## REVISE

### Issue 1: The unconditional-recognizability claim is stated twice with the same triple
**ASN-0133, "Triggers: inline or by reference" and Q1**:
- Triggers para: "Recognizability and absorption (Q0, Q1) are *unconditional* relative to the dynamics hypotheses the termination results below name … holding for undisciplined registries, unfair schedulers, and divergent systems alike."
- Q1: "Recognizability and absorption are *unconditional* — they hold for undisciplined registries, unfair schedulers, and divergent systems alike."

**Problem**: The verbatim triple "undisciplined registries, unfair schedulers, and divergent systems alike" carries the same claim in both places. Q1 is its natural home; the Triggers paragraph (already one of the densest in the note) only needs the *PR-DISC* caveat that distinguishes its context.
**Required**: State the unconditional-relative-to-dynamics claim once (Q1), and in the Triggers paragraph keep only "…but not unconditional relative to PR-DISC," referencing Q1 for the rest.

### Issue 2: Q6's closing sentence restates Q5a's checkability breakdown
**ASN-0133, Q5a and Q6**:
- Q5a: "`|⋃_k [D_ρ]_{Σ_k}| < ∞` quantifies over all reachable states and is as meta-level as H-W — a bound on arguments rather than on trigger-true step-instances, but reachability-quantified all the same."
- Q6: "bounded domain growth is itself reachability-quantified, so the move trades one meta-level assumption for a simpler one — a bound on arguments, not on trigger-true step-instances — rather than eliminating meta-level quantification."

**Problem**: Both passages make the identical point (at-most-once is registration-checkable; bounded growth is reachability-quantified/meta-level), down to the verbatim phrase "a bound on arguments[,] [rather than/not] on trigger-true step-instances." Q6's genuinely new content is only "Extinction discipline is *not* a third independent hypothesis of Q6."
**Required**: Keep Q6's "not a third hypothesis" clarification; drop the duplicated checkability breakdown and cite Q5a for it.

### Issue 3: The H-ATOM single-tuple point is repeated in "What this note doesn't cover"
**ASN-0133, H-ATOM and "What this note doesn't cover"**:
- H-ATOM: "A single-tuple fire — one `→_sh` step — is atomic for free by I4's per-step serialization (ASN-0128); H-ATOM enters with teeth only for multi-tuple contracts…"
- Doesn't-cover: "the serialization of multi-step fires that discharges H-ATOM (single-step marker fires needing none — atomic for free by ASN-0128's I4)…"

**Problem**: The parenthetical in the deferral bullet re-states what H-ATOM already established (single-step fires atomic-for-free by I4, multi-step needs serialization).
**Required**: In the deferral bullet, defer the *scheduler/serialization model* without re-deriving H-ATOM's discharge; drop the parenthetical.

### Issue 4: "settled there" directs the reader to an unresolved open question
**ASN-0133, "Triggers: inline or by reference"**: "the dangling-live-reference case ASN-0130's Open Question 3 owns … but what crossing a revoked endorsement should mean is settled there, not here."
**Problem**: ASN-0130's Open Question 3 is, by name, *open* — the semantics is not "settled" there. A reader building on this note is sent to ASN-0130 for an answer that does not exist. The load-bearing claim ("its evaluation still computes, PR3 reads content not registration") is correct and self-contained; only the "settled there" disposition misleads.
**Required**: Say the question is *scoped/owned by* ASN-0130 and remains open there — not "settled."

### Issue 5: Same set called both "upward" and "downward" closure
**ASN-0133, SC (per-target body)**: "the infinite coverage `⋃{t : y ≼ t, y ∈ addrs_G(x)}` those targets close upward to: that downward closure is non-finite…"
**Problem**: The single set `{t : y ≼ t}` is described as what the targets "close upward to" and then as "that downward closure" in the same sentence — internally inconsistent direction terminology. (The math is unambiguous; the prose contradicts itself.)
**Required**: Pick one direction word for the `≼`-extension/subtree set and use it consistently.

## OUT_OF_SCOPE

The five Open Questions bound future work appropriately. The one place worth confirming as future-ASN territory rather than a gap here: H-SFAIR's satisfiability is shown to require a turn-fairness "this note neither states nor derives" — formalizing turn-fairness and proving when a scheduler realizes the H-SFAIR regime form is correctly left to a future scheduler/environment note (already flagged in "What this note doesn't cover"). No addition needed.

VERDICT: REVISE
