# Review of ASN-0036

## REVISE

### Issue 1: `#v ≥ 2` / `m ≥ 2` is attributed to S8a in multiple places, but S8a disclaims it

**ASN-0036, S8a Postconditions**: "Downstream consumers needing `#v ≥ 2` cite the domain-restriction axiom directly."

But downstream claims repeatedly source the depth bound from S8a instead:
- **D-CTG-depth, Depends**: "S8a — `m ≥ 2` and componentwise positivity of V-positions"
- **S8-depth, Postconditions**: "there exists a common depth `m_s ≥ 2` (by S8a)"
- **D-SEQ, Preconditions**: "`m ≥ 2` inherited from S8a"
- **ValidInsertionPosition, Preconditions**: "`m ≥ 2` is the common depth of V_1(d) by S8-depth and S8a"
- **S8 within-subspace lemma**: "(a V-position with `v₁ = S`, `#v = m ≥ 2`, satisfying S8a)"

**Problem**: S8a's stated postcondition is componentwise positivity only — it does *not* export `#v ≥ 2`, and its own note instructs readers to cite the domain-restriction axiom for that bound. The five sites above cite S8a for exactly the bound S8a says it does not supply. A reader chasing "by S8a" to find `m ≥ 2` lands on a claim that disclaims the obligation. This is an internal citation contradiction, and the precise-citation convention the ASN otherwise enforces (per-step foundation citations) makes it load-bearing, not cosmetic.

**Required**: Pick one. Either widen S8a's postcondition to export `#v ≥ 2` (and delete the routing note), or correct all five downstream citations to point at the `Σ.M(d)` domain-restriction axiom. The argument is sound either way — only the attribution is wrong.

### Issue 2: S8a's routing note is use-site meta-prose

**ASN-0036, S8a Postconditions**: "Downstream consumers needing `#v ≥ 2` cite the domain-restriction axiom directly."

**Problem**: This is a use-site routing instruction, not content that advances S8a's claim. It tells future authors where to cite rather than stating what S8a guarantees — and Issue 1 shows the downstream authors did not follow it. Under the `review-mode.anti-bloat` classifier this is the pattern to surface at source: a definition annotated with where its consumers should look instead of what it says.

**Required**: Remove the note. If S8a is meant to be the carrier of `#v ≥ 2`, state that in the postcondition; otherwise the bound's source needs no editorial pointer embedded in S8a.

## OUT_OF_SCOPE

None. The Open Questions already route operation-layer obligations (INSERT/DELETE preservation of D-CTG, subspace-alignment enforcement, depth-`m` conventions) to future work without claiming them here.

VERDICT: REVISE
