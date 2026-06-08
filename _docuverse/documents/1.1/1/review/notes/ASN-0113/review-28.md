# Review of ASN-0113

The technical core is sound: I checked W3 (well-formedness), W4 (exact coverage via T5), W10/W11 (subspace confinement and disjointness), and the three worked instances against specific tumblers, and they hold. The findings below are the anti-bloat patterns the classifier flags, plus one placement issue.

## REVISE

### Issue 1: Meta-prose accreted around the W5 necessity argument over an unreachable state
**ASN-0113, "The extent of a single subspace" (W5)**: The converse of W5 and its concrete counterexample reason entirely about a *non-contiguous* `V_S(d)` (e.g. `{[S,1],[S,3]}` with `[S,2]` inactive) — a configuration D-CTG★ makes unreachable at every reachable state. The necessity result itself is defensible (it shows contiguity is load-bearing), but three layers pile onto it:
- the forward-direction parenthetical ("The strictly stronger claim … is not exercised by the operation … bears only on the D-CTG★-relaxation open question below") — a defensive scope-clarification + forward reference;
- the structural converse *plus* a concrete numeric instance of a state the system never reaches;
- the recap paragraph "The converse just established is the dependency claim: exactness genuinely *rests* on D-CTG★ …", which restates what the converse paragraph already proved.

**Problem**: This is the "imagines a case the invariant already excludes" and "two paragraphs say the same thing" patterns compounding. The recap paragraph adds nothing the converse did not; the parenthetical defends scope rather than advancing the claim.
**Required**: Keep the minimal necessity statement (contiguity ⟹ single exact span exists; non-contiguity ⟹ none does, by order-convexity). Drop the recap paragraph and the forward-reference parenthetical; the concrete unreachable-state instance can go or shrink to a clause.

### Issue 2: Link-counting faithfulness is misplaced under "Permanence of the report"
**ASN-0113, "Permanence of the report" / W18**: The closing paragraph ("The link extent counts links") argues — via CL-OWN, CL-UNIQ, and S2/S3★ — that `n_{s_L} = |V_{s_L}(d)|` faithfully counts home links and `n_{s_C}` counts content positions. This is about *what the count means*, not its permanence.
**Problem**: Essay content in the wrong structural slot. The section is titled and motivated by permanence (W18 = DerivedReport, determinism under fixed `Σ`), but half its body is a faithfulness bridge that belongs with W1/W17 (what the extent measures). The W18 table entry inherits the overload, bundling DerivedReport with two distinct faithfulness claims.
**Required**: Move the count-faithfulness argument next to W1/W17 (or give it its own label). Leave the permanence section to W8→W18 determinism. Trim the W18 table entry to the DerivedReport claim alone.

### Issue 3: Defensive "violation would be corruption" prose in W16
**ASN-0113, "Invariants across the members" (W16)**: "A violation of W16 would be a corruption of the index: orphaned content … or phantom extent …"
**Problem**: Defensive justification imagining a violation to assert significance, rather than advancing the partition claim itself.
**Required**: Cut the sentence, or fold the observable-signature point into one clause; the partition equality and its derivation already stand on their own.

## OUT_OF_SCOPE

The open questions on version-fork permanence, transclusion, single overall extent, and subspace-convention extension are correctly deferred (they map to out-of-scope topics and are framed as questions, not claims) — no action needed.

VERDICT: REVISE
