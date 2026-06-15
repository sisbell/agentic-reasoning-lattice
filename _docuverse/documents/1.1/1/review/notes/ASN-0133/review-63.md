# Review of ASN-0133

I checked the proofs for rigor first — Q5's injection, Q5a's at-most-once bound via Q-EXT, Q6's inert-tail/H-FAIR contradiction and the two counterexamples, the Marker-pattern idem=⊤ dedup-miss argument, Q9's anti-monotonicity, and the heterogeneous-rewrite value computation (Σ\* with `y₀`/`a₀`). They hold. Boundary cases that usually trip operation specs — empty registry, empty `[D_ρ]`, zero real fires, single flagged target, idem=⊤ vs idem=⊥ emission steps — are all covered, and the concrete `Σ₀→Σ₁→Σ₂` sequence exercises the surface emitters end to end. I found no logic gap.

The findings below are confined to the `review-mode.anti-bloat` mandate: residual forward-reference/use-site prose. The underlying reasoning in each cited spot is correct — only the prose needs trimming.

## REVISE

### Issue 1: Structural meta-prose previewing the proof and regime list
**ASN-0133, Q6 (TerminationUnderFairness)**: "So Q1's absorption (a fixed point of firing) is the registry's standing guarantee, holding whatever the environment does and **under every regime hypothesis below**. **(The Proof derives the inert tail; the regime list below turns on what is assumed past it.)**"

**Problem**: The parenthetical advances no reasoning about quiescence — it narrates the document's own structure (what the Proof does, what the list does), and "under every regime hypothesis below" forward-points to material stated in the very next paragraph. This is essay content in a structural slot: the reader skips it to reach the regime list, which then says the same thing, which the Proof then derives. It is exactly the "multiple references deferring to the same downstream location" pattern, compounded into one sentence.

**Required**: Delete the parenthetical. Drop "and under every regime hypothesis below" — the regime split is the immediately following content and needs no forward pointer. The Q6 statement should assert the registry-side guarantee and stop.

### Issue 2: Use-site inventory previewing Q5a's mechanism
**ASN-0133, Q5 (RealFiresAreBounded), closing sentence**: "Extinction discipline is neither used nor needed: **its leverage is elsewhere — Q-EXT and Q5a, where it lets bounded domain growth supply the same finite-real-fire conclusion (H-RF, above) directly, with no W(σ) bound at all.**"

**Problem**: The scoping fact — *Q5 needs no extinction discipline* — is legitimate and worth one clause. The remainder enumerates the downstream consumers (Q-EXT, Q5a) and previews their entire mechanism (bounded domain growth → finite real fires, no `W(σ)`). A reader at Q5 does not need Q5a's route described in advance; Q5a states it in full where it belongs. This is the "definition's introduction enumerates downstream consumers" pattern.

**Required**: Trim to the scoping fact, e.g. "Extinction discipline is neither used nor needed for this bound." Remove the "its leverage is elsewhere — Q-EXT and Q5a, where it lets bounded domain growth supply the same finite-real-fire conclusion directly, with no W(σ) bound at all" preview; Q5a already draws the contrast (it explicitly says it "supplies H-RF by a route disjoint from Q5 — it never mentions W(σ)").

## OUT_OF_SCOPE

None. The note scopes its deferrals cleanly — schedulers, stochastic bodies, activation binding, and the environment/workload model are listed under "What this note doesn't cover," and the five open questions (SF certificate, runtime divergence detector, per-scope work, cross-scope oscillation, contract necessity) are genuine future territory rather than gaps in this ASN.

VERDICT: REVISE
