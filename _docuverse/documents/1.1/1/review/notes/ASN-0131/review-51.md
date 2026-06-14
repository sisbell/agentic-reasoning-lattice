# Review of ASN-0131

This is a careful, largely correct note. I verified the core machinery and found no correctness or completeness defect: RE-DEF's biconditional yields RE-SND/RE-CMP by direct unpacking; the worked instance computes correctly and genuinely exercises RE-OVL/RE-CLIP/RE-WHOLE/RE-UNIT; the union proof and the non-injective intersection counterexample (RE-UDIST-∩) are sound; the RE-CWP weakest precondition is derived correctly (including the `R = ∅` boundary collapsing to `RE = ∅`); and the retraction-stability "iff sole bearer" argument (forward via R6a + the net-removal hypothesis, backward via R-Scope) holds, with the `coverage(Θ) ∩ dom(Σ.C) = ∅` hypothesis honestly flagged to Open Question 6. RE-ADDR is sound (its "does not retract its own emitter address" clause is what carries the retraction emitter `b`).

The findings below are accretion, of the kind the anti-bloat classifier targets — both clustered around the ASN-0086 lemma-transfer machinery.

## REVISE

### Issue 1: Vestigial double-justification of the retraction emitter's addressability
**ASN-0131, "The unit of the answer" (RE-ADDR intro), "Under retraction", and Claims table (RE-ADDR)**:

RE-ADDR's own statement already discharges `b`'s addressability through its general "does not retract its own emitter address" clause — `b` targets `ℓ ≠ b`, so RE-ADDR applies directly and arity-independently. Yet the note keeps a parallel `wp` Case 2 proof of the *same* fact in three places:

- RE-ADDR intro: "(For the narrower case of a genuine standard-triple emission, ASN-0086's `wp` Case 2 reaches the same conclusion through its non-self-targeting conjunct `a_emit ∉ coverage(G)`; we draw on that form below for the retraction emitter `b`, a genuine triple.)"
- Use site: "`b` is therefore addressable in `Σ'` ... by RE-ADDR — and, since `b` is a genuine `Emit_R`/`Emit_K` triple, equally by `wp` Case 2's non-self-targeting conjunct `a_emit = b ∉ coverage(G) = {u : ℓ ≼ u}` (ASN-0086) ..."
- Claims table: "the genuine-triple case additionally matches `wp` Case 2's non-self-targeting conjunct (ASN-0086)".

**Problem**: RE-ADDR was generalized (per the most recent revision) precisely so that one tool covers `b`. The `wp` Case 2 path is now subsumed, identical in content (same R0a/discipline argument), and adds no information — it is a leftover of the pre-generalization justification. Two proofs of one load-bearing fact, advertised at the definition and re-executed at the use site, is exactly the redundancy the anti-bloat mode names ("say the same thing in different words"; "definition's introduction enumerates downstream consumers").
**Required**: Keep RE-ADDR as the single justification for `b`. Drop the `wp` Case 2 pre-announcement in the RE-ADDR intro, the "equally by `wp` Case 2 ..." clause at the use site, and the "additionally matches `wp` Case 2" tail in the claims-table entry.

### Issue 2: The lemma-transfer bridge is framed as a use-site inventory with forward/back cross-references
**ASN-0131, "The unit of the answer" (bridge), with use-site parentheticals at R-Scope and `wp` Case 2**: "We invoke this transfer at the use sites below, noting the carried hypotheses there." — then at R-Scope: "(its hypotheses name `d_retr ∈ dom(Σ.M)` and the emitter `a_emit(Σ, d_retr)`, carried to this ASN-0047 state by the bridge above)", and similarly at `wp` Case 2.

**Problem**: The bridge itself does necessary work (transferring ASN-0086's `Σ.L`/`nullified` lemmas to ASN-0047-reachable states is a genuine soundness obligation, and I confirmed it is sound). But the *framing* is the forward-reference accretion the classifier flags: the bridge announces an inventory of downstream use sites ("we invoke this transfer at the use sites below"), and the use sites point back ("by the bridge above"), re-listing carried hypotheses each time. The forward announcement plus the round-trip cross-references are the degrading element.
**Required**: State the bridge's conclusion self-containedly once — that ASN-0086's `Σ.L`/`nullified` lemmas hold at ASN-0047-reachable states, *including* those whose hypotheses name `dom(Σ.M)` or `a_emit(Σ, d)` — and let R-Scope and `wp` Case 2 cite it by name without the "we invoke below" announcement or per-site re-derivation of which hypotheses are carried.

## OUT_OF_SCOPE

The seven Open Questions (whole-endset vs touching-spans, multiplicity, V-position rendering, intersection-equality under injective `Σ.M(d)`, non-co-resident link stores, type-slot/content matches, link-subspace regions) correctly defer their respective extensions. I have nothing to add here — these are future territory, not defects in this note.

VERDICT: REVISE
