# Review of ASN-0100

## REVISE

### Issue 1: Counterfactual reasoning about a case INSERT excludes
**ASN-0100, §Cross-subspace isolation**: "Even if it were applied to a position in V_{s_L}(d), by OrdAddHom (b clause, ASN-0082) the subspace identifier — the first component — would be preserved; the position would not migrate to the text subspace. But INSERT never applies shift to non-text positions in the first place."
**Problem**: This paragraph builds an argument about shift acting on link-subspace positions, then retracts it — INSERT's scoping already excludes the case. Reviser-drift: imagining a case the operation's own carrier excludes. The frame INS.frame.subspace (`V_{s_L}(d') = V_{s_L}(d)`) already establishes isolation directly.
**Required**: Delete the counterfactual sentence and the OrdAddHom digression; cite the frame.

### Issue 2: "Composite atomicity" stated in multiple slots
**ASN-0100, §The Operation: Formal Contract**: "Composite-level atomicity is therefore *definitional* — a consequence of INSERT being a valid composite — not an extra property the substrate must separately supply."
**ASN-0100, INS.atomicity / §Atomicity**: "composite-level atomicity is definitional under ValidComposite★ (ASN-0047) — INSERT's elementaries form a contiguous transition sequence, so Σ' is determined by the contract."
**Problem**: The same definitional-atomicity claim appears in the Formal Contract prose, the INS.atomicity table row, and the INS.pre/INS.def rows — same content, different words, across sections.
**Required**: State it once (the Atomicity section), reference from elsewhere.

### Issue 3: Repeated deferral to §Provenance for the same discharge
**ASN-0100, multiple sites**: "the discharge is given in §Provenance"; (worked example, interior) "is discharged generally in §Provenance"; (worked example, empty) "is the general §Provenance discharge"; (atomicity, step 4) "are discharged in full in §Provenance (R, P4★, P4a, P7a)."
**Problem**: Four-plus paragraphs in different sections defer to the same downstream location for J0/J1★/J1'★. The reader must hold each pointer. The worked-example instantiations are concrete and useful; the surrounding "but the general logic is in §Provenance" pointers are accretion.
**Required**: Let the worked example instantiate the pairs without re-pointing; carry one forward pointer, not four.

### Issue 4: Use-site inventory attached to a precondition
**ASN-0100, §The Operation: Formal Contract, State Preconditions**: "d ∈ dom(M) (so K.α, K.μ⁺, K.ρ all have their d ∈ E_doc precondition met; K.μ⁻ when fired further requires dom(M(d)) ≠ ∅, satisfied in cases that invoke it)"
**Problem**: The parenthetical enumerates which elementary steps consume the precondition rather than advancing the precondition's meaning — a use-site inventory.
**Required**: State the precondition `d ∈ dom(M)`; drop the consumer enumeration (per-step preconditions are discharged in §Atomicity).

## OUT_OF_SCOPE

(none — the ASN's own Open Questions and Bounding the Scope correctly defer link-subspace insertion, COPY, DELETE, version derivation, and replication.)

VERDICT: REVISE
