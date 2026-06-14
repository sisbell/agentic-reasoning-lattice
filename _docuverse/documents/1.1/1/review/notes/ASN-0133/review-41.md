# Review of ASN-0133

The mathematics here is sound. I checked Q0's view-rebuild for completeness (the view-sensitive atom set is exactly {members, targets_of, is_K, M_K} ∪ {succs, sources_to, chain, stale}, and every member is handled), Q5's index-injection, Q-EXT's SF+extinction composition, the idem=⊤ "audit-reading rules out the dedup hit" argument in Q3, Q-FLIP's BH3 re-arm counterexample, and Q6's (1)/(2)/(3) obstruction analysis. I found no rigor defect, no missing boundary (empty domain, zero real fires, finite-σ tail, born-nullified deposit are all handled), and no non-foundation cross-reference. The worked example exists and verifies the heterogeneous rewrite numerically.

The findings below are all of the kind the active `review-mode.anti-bloat` classifier targets: the argument is correct but carries restatements and hypothesis-commentary the precise reader must work around. They are REVISE because the note invites exactly this pass.

## REVISE

### Issue 1: The heterogeneous-rewrite rationale is stated three times
**ASN-0133, Q0 / "Heterogeneous rewrite, worked" / "Value-preservation, at one state"**: the same justification — *the rewrite changes spelling not value because fixed-view atoms read the active slice at every term view and the filter is UV's own default-view definition* — appears in all three places:
- Q0: "a change of spelling, not of value (carried by PC3's fixed-view rebuild equations and UV's default-view definition)"
- Worked: "Both succs and is_filtered_retired are fixed-view atoms reading the active slice at every term view, so this filter denotes the default-view value at audit view too — value carried, spelling changed."
- Value-preservation: "The two spellings agree — succs reads its active slice at every term view (PC3, fixed-view) and the filter is UV's own default-view definition of the result, so the audit-view rewrite reproduces the default value, as the computation just shown bears out"

**Problem**: Only one of these earns its place. The numeric computation in the value-preservation paragraph *is* the demonstration; the trailing clause "as the computation just shown bears out" is circular, and the worked-setup sentence restates Q0's abstract claim before re-deriving it. The "naive merge is ill-formed" point is likewise asserted in Q0 ("for a heterogeneous-view registry that merge is ill-formed"), in the worked setup ("exactly the ill-formed move PC3 forbids"), and again in the numeric check ("the naive same-view merge … would compute … the wrong value").
**Required**: Keep the abstract rewrite in Q0 and the numeric demonstration in the worked example; drop the prose restatements of "spelling not value" / "fixed-view reads active at every term view" that frame the numeric check, and state "naive merge is ill-formed" once.

### Issue 2: Extended meta-commentary on hypothesis roles ("why/whether used") rather than what they say
**ASN-0133, W/H-W "separation" paragraph and the H-SFAIR treatment**:
- H-W: "Beyond this starvation-fragility, H-W is the termination conclusion in disguise … strictly stronger than Q6's entire conclusion, and so unusable as a hypothesis of it, though it formally implies the weaker H-RF."
- H-SFAIR: defined, given a "regime form," then shown "Satisfiability is environment-conditional," then reprised inside Q6's case-(3) closure, to land on "H-SFAIR is the strong-scheduling form of regime (i), not a disjoint second route."

**Problem**: This is the flagged pattern — prose explaining *why a stated hypothesis is (not) usable / (not) independent* rather than what it asserts. The operative facts are one line each: H-W ⟹ H-RF (that is Q5), and H-SFAIR's regime form excludes case (3) but is satisfiable only under turn-fairness "a condition this note neither states nor derives" — i.e., it closes nothing regime (i) does not. The surrounding argument that H-W is "the termination conclusion in disguise" and that H-SFAIR collapses to regime (i) is approached from several angles across the W, H-SFAIR, and Q6 sections.
**Required**: State each role-fact once. H-W: "H-W ⟹ H-RF (Q5); H-W also implies quiescence directly, hence is too strong to serve as Q6's hypothesis — Q6 uses H-RF." H-SFAIR: "H-SFAIR excludes case (3); its satisfiability requires a turn-fairness equivalent to regime (i), so it is not an independent route." Remove the repeated re-derivations of these two conclusions.

### Issue 3: Q6 conflates its statement with its proof
**ASN-0133, Q6**: "Under H-RF and H-FAIR, the registry's own drive to fire is exhausted after finitely many real fires … The system reaches and holds a quiescent state when the environment eventually stops presenting trigger-true work — regime (i); all-SF (regime (ii)) does not supply this by itself …"
**Problem**: The conclusion is hypothesis-indexed (H-RF+H-FAIR alone; +regime (i); +all-SF/grow-only/bounded-growth/weak-fairness; +H-SFAIR for non-grow-only) but the indexing is woven into a single prose run, and the regimes (i)/(ii) and obstructions (1)/(2)/(3) are *introduced inside the proof*. A reader cannot extract "what holds under exactly which package" without consuming the whole proof — the load-bearing unconditional result (past N the registry is fire-inert; residual non-quiescence is environment-driven) is buried mid-paragraph. Relatedly, the regime-(ii) grow-only conclusion is headlined "under weak H-FAIR alone" while the proof in fact also uses bounded growth ("With bounded growth each of the finitely many arguments …") — an imprecise hypothesis attribution.
**Required**: Lead Q6 with the unconditional registry-side conclusion, then tabulate the reached-and-held conclusion per hypothesis package (correcting "weak H-FAIR alone" to "weak H-FAIR + bounded growth"), then give the proof. The (1)/(2)/(3) obstruction taxonomy can stay in the proof but should be named as the structure of the non-grow-only case rather than discovered mid-stream.

## OUT_OF_SCOPE

### Topic 1: Cross-rule discipline bounding coupling when a non-SF lower rule makes re-arm a live route
**Why out of scope**: The note already flags this in the worked composition ("a non-SF lower rule makes re-arm a live route too — this note does not settle") and routes it to its own OQ4 / a future cascade theory. The all-SF coupling case *is* settled here via the Q5a legality condition. Deferring the non-SF general case is correct, not a gap in this ASN.

META: (none — the note holds its layer: rule bodies, schedulers, and the environment model are explicitly left to the implementation/protocol layer, and what it specifies — recognizability, absorption, conditional termination — are system guarantees an alternative implementation would equally owe.)

VERDICT: REVISE
