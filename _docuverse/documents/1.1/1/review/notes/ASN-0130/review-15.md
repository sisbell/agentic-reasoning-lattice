# Review of ASN-0130

The construction is sound. I checked the boundaries the substrate makes available — empty `A_def` (gated by (0)), `k = 0` closed terms, self-reference (PR2(b)), never- and de-registered referents, born-nullified deposits, and re-registration after de-registration — and the load-bearing proofs: PR2's event-wise acyclicity (robust under re-registration because run content is immutable, so a referent's reference set never changes across deposits), PR3a's substitution induction (WT-α/WT-W with the freshness PR3's renaming arranges), the two wp derivations, and PR5's extension of PD0 to open terms and to bound-ℕ aggregate thresholds (sound — the ground consumes only fixity of bound values across a step). I found no correctness gap.

The findings below are bloat, surfaced under the note's `review-mode.anti-bloat` classifier. Both concern the note's central scoping device — "registration-disciplined derivations" — which is over-elaborated and pinned downstream of its first use.

## REVISE

### Issue 1: Off-discipline counterexamples argue outside the claim's declared scope
**ASN-0130, PR0 (wp analysis)**: "Off-discipline this direction fails: an I0-equal incumbent may carry F' with unit spans at a and at an extension a.x ... so VALID ∧ hit would hold while POST-ref fails." and "Off-discipline this direction fails too: a pre-existing raw tuple with F'' = enc({a}) and an unrelated G'' is no hit ... yet satisfies POST-ref at Σ' while the formula reads false."

**Problem**: The wp equivalence is explicitly scoped "on registration-disciplined derivations," and the proof already flags where the discipline does its work — "first use of the discipline" (canonical shaping forces `a' = a` at a hit) and "second use" (¬C3 leaves POST-ref false at a miss). Those on-discipline steps are what a reader needs to follow the equivalence. The two "Off-discipline this direction fails: [construction]" passages then build the counterexamples the scope excludes — proving more than the scoped claim requires. This is a paragraph imagining a case the claim's precondition already rules out. The same pattern recurs as the PR-SIG parenthetical ("Off-discipline the ground gives way: a raw pdef-class deposit ... can mint an active tuple ... whose sig(r) is undefined") and is gestured at a third time in PR3.

**Required**: Drop the off-discipline counterexample constructions. The inline "first/second use of the discipline" markers already discharge the obligation to show the hypothesis is load-bearing; the explicit demonstration that dropping it breaks each direction is reviser-note material, not ASN content.

### Issue 2: "registration-disciplined derivations" is defined downstream of first use, forcing repeated forward deferrals
**ASN-0130, PR-SIG / sig / PR0(iii) / PR3a / PR5a**: the term is defined only inside PR0's "Discipline and uniqueness" subsection, yet it is consumed from PR-SIG (which precedes PR0) onward — `sig`'s induction opens "scoped to registration-disciplined derivations (PR0, Discipline and uniqueness)"; PR0 (iii) cites "(PR-SIG; Discipline and uniqueness below)"; PR3a re-explains "(PR0, Discipline and uniqueness — the hypothesis consumes PR-SIG's sig, the proof PR0 (iii)'s judgment and PR1, all scoped there)"; PR5a defers there again.

**Problem**: Multiple claims in different sections defer to the same downstream location for the note's central scoping concept, each re-explaining a fragment of it. The concept is used from the first definition (PR-SIG) but pinned at the document's middle (PR0) — textbook forward-reference accretion.

**Required**: Hoist the definition of "registration-disciplined derivation" — together with the one-line fact that the entry-point seal (Standard registrations) keeps every shipped-surface derivation disciplined — to a preliminary before PR-SIG. Each downstream claim then cites it once, with no "below," and the per-claim re-explanations collapse to a citation. This also subsumes the remedy for Issue 1: with the scope stated once up front, the urge to re-justify it per claim disappears.

## OUT_OF_SCOPE

(none — the note's Open Questions 1–4 already enclose naming, cross-substrate portability, dangling live references, and certificate classes beyond ST; the "failed re-registration when a referent has been de-registered" corner is a facet of OQ3.)

VERDICT: REVISE
