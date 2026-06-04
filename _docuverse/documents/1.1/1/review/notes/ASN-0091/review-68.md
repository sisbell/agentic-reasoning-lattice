# Review of ASN-0091

## REVISE

### Issue 1: RA-adm status paragraph is rationale, not reasoning
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "For the abstract Vstream-only class, RA-adm is a *definitional admissibility constraint* — a membership condition that restricts which bijections π are admitted, not a property derived from the other clauses. A transition is Vstream-only only if it satisfies RA-adm; nothing is owed by way of proof at the abstract level. A concrete realiser, by contrast, must *prove* that its transition satisfies RA-adm … and that proof obligation is discharged for REARRANGE_K below."
**Problem**: This is meta-prose about the *epistemic status* of a clause and an announcement of a forward proof obligation — it advances no reasoning. The clause RA-adm is already stated in the frame block. The "nothing is owed / a concrete realiser must prove" framing is the kind of defensive justification the anti-bloat classifier targets, and it ends in a forward pointer ("discharged … below").
**Required**: Delete the paragraph. RA-adm stands as a clause; the REARRANGE_K discharge section already does the work without this preamble.

### Issue 2: Repeated deferral to the same downstream RA-adm discharge
**ASN-0091, multiple sites**: the table row "the per-state foundation invariants then follow at Σ', discharged in the RA-adm paragraph below"; the prose "The binary transition invariants … are discharged in 'State-Component-Only Invariants' below"; the body paragraph "RA-adm requires that every per-state foundation invariant holding at Σ hold at Σ' … ExtendedReachableStateInvariants is the explicit form of this implication"; and again the worked-example bullet "the per-state predicates ride on RA-adm (this state is reachable, so ExtendedReachableStateInvariants applies)."
**Problem**: Four separate locations defer to or restate the same single mechanism (reachable ⟹ per-state invariants, via ExtendedReachableStateInvariants). This is the "multiple paragraphs defer to the same downstream location" / "two paragraphs say the same thing in different words" pattern that compounds across cycles.
**Required**: State the reachability⟹invariants discharge once, at its home (the RA-adm discharge), and replace the other three with a bare citation.

### Issue 3: "Standing premise" paragraph carries justificatory aside
**ASN-0091, "REARRANGE_K Realises the Abstract Class"**: "*Standing premise of the REARRANGE_K realisation.* Σ is reachable from Σ₀ … This is the operative regime — REARRANGE_K is a system operation, only ever invoked at a state already reached from Σ₀ — and it is precisely the hypothesis ExtendedReachableStateInvariants requires."
**Problem**: The premise itself (Σ reachable) is the only load-bearing content; the em-dash clause is rationale explaining *why the premise is reasonable*, not what it states or how it is used.
**Required**: Keep the premise sentence; drop the "This is the operative regime — … — and it is precisely the hypothesis … requires" elaboration.

### Issue 4: ChainDisjointAdjacency parenthetical defends an unused case
**ASN-0091, "Run Decomposition Is Not Invariant" (inline lemma)**: "Domain disjointness is established without appeal to any prefix-positional disagreement, so the conclusion holds uniformly across all length cases — including those where one document tumbler is a proper prefix of the other (e.g., `d_X = [1, 0, 1, 0, 1]` and `d_Y = [1, 0, 1, 0, 1, 1, 1]` …)."
**Problem**: None of the four witnesses or worked examples exercises a proper-prefix document pair — every witness uses `d = [1,0,1,0,1]` and `d' = [1,0,1,0,2]`, which are *not* prefix-related. The clause and its worked example defend robustness against a case no consumer reaches; this is accreted defensive content (reviser drift), not a step the lemma's users need.
**Required**: Remove the "including those where one document tumbler is a proper prefix … (e.g., …)" elaboration. The general domain-disjointness argument already covers all cases; the example adds nothing the proof or its consumers use.

### Issue 5: Clause-correspondence inventory is partly redundant scaffolding
**ASN-0091, "Clause Correspondences and Per-Invariant Discharges"**: the "Abstract class clause ← REARRANGE_K source" table plus the surrounding prose ("With RA-reg discharged above, the abstract class's defining clauses map to their REARRANGE_K sources, and K.μ~'s own admissibility clauses (i)–(v) … map to their discharge").
**Problem**: The first table is a use-site inventory mapping each abstract clause to an ASN-0084 source name; combined with the "Claims Introduced" Provenance column at the end of the note, the same source-attribution is recorded twice. The connective prose ("map to their sources … map to their discharge") restates the table's purpose without adding content.
**Required**: Keep the (i)–(v) *discharge* table (object-level — it does real work). Fold the source-mapping table's content into the Provenance column it duplicates, and drop the connective sentence.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: REARRANGE_K's CS3 fixes the cut subspace to content (S = 1), and the note correctly defers link-subspace rearrangement to an Open Question. This is new territory, not a defect.

### Topic 2: Joint reconstitution of a fragmented same-source span
**Why out of scope**: RE-trans establishes per-fragment origin but explicitly does not claim the fragments jointly reconstitute the source span; this is correctly listed as an Open Question and belongs to a future ASN.

META: (not applicable — the ASN defines a transition class, its operation realiser, and state invariants abstractly; it has not drifted into implementation mechanics.)

VERDICT: REVISE
