# Review of ASN-0133

The note is, on the mathematics, in excellent shape. I checked the load-bearing proofs — Q0's view-rebuild closure, Q3's idem=⊤ dedup-miss argument, Q5's injectivity, Q5a's at-most-once bound, and the full Q6 case split including the obstruction cases (1)/(2)/(3) and the H-SFAIR regime form — and they hold. The honest framing (registry-side termination unconditional past N; *reaching* quiescence over non-grow-only domains always needing environment cooperation, with H-SFAIR's satisfiability flagged as turn-fairness this note doesn't supply) is sound and not overclaimed. The two findings below are a genuine but minor gap in one exhaustive enumeration, plus the anti-bloat pass the classifier requests.

## REVISE

### Issue 1: Q0's view-stable classification omits `is_filtered`

**ASN-0133, Q0 (Recognizability)**: "Everything else a Boolean trigger or a QD domain can read — the verdict/optional atoms is_in_chain, tip, target_of, age, targets_keyed (never UV-rewritten, by UV's Verdicts-and-optionals and Booleans clauses) and the fixed-view slices A_K/L_K themselves — is genuinely view-stable"

**Problem**: The closure argument is a partition: every trigger-/domain-readable constituent is either (a) one of the eight view-sensitive atoms rebuilt to fixed-view bases [`is_K, members, targets_of, M_K, succs, sources_to, stale, chain`] or (b) the "genuinely view-stable" remainder enumerated above. The BH1 atom `is_filtered` is a Boolean a trigger can read directly (`T(x) ≡ is_filtered(x)`; the heterogeneous worked example itself reads `is_filtered_retired`) and it appears in **neither** list. It is not view-parameterized (PC3 names only the four) and is never UV-rewritten (UV's Booleans clause lists it explicitly), so it reads its active slice at every term view — view-stable in exactly the sense `is_in_chain` is. The proof in fact *relies* on this fact (it uses "the view-stable Boolean is_filtered_J" as the rebuild filter body), yet the summary partition, presented as a closed exhaustive case analysis ("Everything else ... is genuinely view-stable"), skips it. The one BH1 atom a registry's triggers can read is the one the enumeration leaves unclassified. The conclusion `quiescent_R ∈ PL` survives — `is_filtered` is benignly view-stable — but the case analysis as written does not establish it for `is_filtered`.

**Required**: Add `is_filtered` to the view-stable atoms — the second view-stable Boolean alongside `is_in_chain` — so the partition is exhaustive; or soften "Everything else" so the list is not presented as a closed partition.

### Issue 2: Anti-bloat — consumer-pointer in a hypothesis intro; editorializing restatement in Q5a

**ASN-0133, H-SFAIR**: "This note invokes H-SFAIR in exactly one role: the all-SF, extinction-disciplined regime over a non-grow-only domain (Q6 regime (ii), instantiated by the producer ρ_P)."
**ASN-0133, Q5a**: "this is the quantitative payoff of the SF-plus-extinction design rule" … "The trade buys something exactly when there is an environment to bound."

**Problem**: The parenthetical `(Q6 regime (ii), instantiated by the producer ρ_P)` names the downstream consumer rather than advancing H-SFAIR's meaning — the regime context "all-SF, extinction-disciplined … non-grow-only" already supplies everything the regime-form derivation needs. This is the flagged "definition's introduction enumerates downstream consumers" pattern. In Q5a, "this is the quantitative payoff of the SF-plus-extinction design rule" is editorializing that asserts no claim, and "The trade buys something exactly when there is an environment to bound" restates the closed-case-degeneracy conclusion given two sentences earlier ("the closed special case is degenerate … Q5a says nothing H-RF did not").

**Required**: Delete the consumer parenthetical and the two Q5a sentences; every surrounding claim stands without them.

## OUT_OF_SCOPE

(none) — the "What this note doesn't cover" and "Open questions" sections already place the scheduler, the environment/workload model, and the `pd_extinct` SF certificate at the layers above; none is an error in this note.

VERDICT: REVISE
