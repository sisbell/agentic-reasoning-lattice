# Review of ASN-0114

The operation is correctly built: F0–F8 stay at the level of system guarantees (an alternative implementation must satisfy them), the substrate is drawn entirely from foundation ASNs, the proofs of F2 and F5 check out, the wp(R = ⟨⟩) analysis is genuinely non-trivial with a load-bearing third conjunct, and the worked instance discharges F2 and F7 against a concrete link — including the disconnectedness witness (p=a₃, q=a₅, r=a₇) and the F ∩ [a₃,a₅) = {a₃,a₄} computation, both of which I verified. Boundaries (empty end, invalid selector, orphaned link, N>3 link, disconnected coverage, type-slot-always-nonempty) are all covered.

The findings below are confined to accreted meta-prose, which this note's anti-bloat classifier directs me to surface.

## REVISE

### Issue 1: F4's accounting-machinery aside defends the frame at a layer the abstraction already excludes
**ASN-0114, F4 (PureRead)**: "We note for completeness that Nelson's accounting machinery (cash-register increment, royalty accrual on delivery) sits outside the abstract state Σ modeled here; F4 is a statement about Σ, and monotone bookkeeping counters, to the extent they exist, lie below this abstraction and never alter the link or the referenced material (Q10)."
**Problem**: This is a defensive justification, not part of the frame claim. F4 already says "no state transition" on Σ; if billing counters are below the abstraction, they have no standing to mention — defending against the objection is the bloat. The hedge "to the extent they exist" advances nothing. A reader following the frame skips past this sentence.
**Required**: Delete it. F4's frame is a statement about `Σ.C`, `Σ.L`, `Σ.M`, and the sibling slots; that is complete.

### Issue 2: F5's material-permanence paragraph essays a reading F5 explicitly does not claim, and duplicates the claims-table gloss
**ASN-0114, F5 (TemporalDeterminism)**: "F5 as stated is a *coverage*-permanence claim, and exactly one fact carries it: *link immutability* (L12) … That the recorded addresses are addresses of permanent content identity rather than mutable positions (Q3, Q7, Q8) … is what upgrades coverage-permanence to *material*-permanence … F5 does not formally claim that stronger reading."
**Problem**: The first clause (F5 is coverage-permanence, carried by L12) is a fair scope clarification. The rest is essay about a non-claim — the material-permanence reading is described, motivated with Q3/Q7/Q8, then withdrawn ("F5 does not formally claim that"). Prose that builds up a reading only to disclaim it does not advance the argument. The identical point recurs in the Claims table F5 row ("content-identity addressing upgrades this to material-permanence but is not needed for the coverage claim") — the same non-claim stated twice in different words.
**Required**: Keep the one-line "F5 is coverage-permanence, carried by L12 (via LP13)"; drop the material-permanence essay. Remove the duplicate gloss from the table row.

### Issue 3: "The recorded end versus its resolution" — justification tail and a redundant deferral
**ASN-0114, §"A boundary we must respect"**: "Keeping this boundary sharp is what lets F1 and F5 state unconditional guarantees: they hold of the recorded end precisely because they do not entangle the operation with the mutable arrangement of any document."
**Problem**: The section's core — confronting the implementation evidence (Q11/Q15/Q20) that describes FOLLOWLINK returning *V-positions*, and naming that as resolution rather than this operation — is useful and should stay. But the closing sentence is meta-commentary restating that F1/F5 are unconditional (already established at F1 and F5), and the section's "explicitly outside the scope of this note" is the third deferral of resolution-to-V-positions (also deferred in Open Questions, and in the harness Scope). Multiple paragraphs deferring to the same downstream/out-of-scope location is exactly the accretion pattern.
**Required**: Keep the evidence-confrontation (resolution shrinks/varies by document — Q11, Q15). Cut the closing justification sentence; let the single scope declaration carry the deferral without restating why the scoping is good.

## OUT_OF_SCOPE

### Topic 1: Resolving the recorded endset into a document's V-positions
**Why out of scope**: The implementation evidence describes a projection-and-filter step that converts recorded addresses through a chosen document's arrangement (Q11/Q15/Q20). The ASN correctly identifies this as a separable concern (resolution) distinct from reading the recorded end, and the harness Scope confirms it belongs elsewhere. I checked that none of F1–F8 smuggle arrangement-dependence in; they do not. Boundary correctly drawn.

META: Not applicable — the ASN specifies guarantees on link-store state (precondition, coverage-exact postcondition, pure-read frame, permanence, confinement) and uses implementation evidence only to ground and test them, so it has not drifted into mechanics.

VERDICT: REVISE
