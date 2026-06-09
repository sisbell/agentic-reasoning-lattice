# Review of ASN-0116

## REVISE

### Issue 1: Redundant coupling restatement — "Provenance coupling" paragraph duplicates PROV
**ASN-0116, "The document remains one coherent sequence"**: The paragraph *"Provenance coupling — the obligation allocation incurs"* states: "ASN-0047 binds it to the three coupling constraints J0, J1★, J1'★ ... — discharged with the valid composite above (clause 2) — and to the composite-boundary coverage properties P7a and P7..." The PROV claim immediately following says the same: "which discharges the coupling constraints J0, J1★, J1'★ of ASN-0047 between the composite's initial and final states; the composite-boundary properties P7a and P7 then hold at the post-state by ExtendedReachableStateInvariants."

**Problem**: The coupling-discharge content is now stated three times — once with full derivation in the valid-composite clause-2 paragraph (the keeper), once in this prose paragraph, and once in the PROV named claim. The prose paragraph's only non-redundant content is its implementation grounding (4/11, the DOCISPAN record). The reader must skip past a restatement of clause 2 to reach that.

**Required**: Collapse the paragraph to its implementation-evidence sentence and let PROV carry the coupling statement; or fold the implementation note into PROV's body. The coupling discharge belongs in exactly one place (clause 2 derives it; PROV names it).

### Issue 2: Meta-narration of proof strategy in the well-formedness section
**ASN-0116, "The document remains one coherent sequence"**: "We do *not* re-derive these per region. What the valid-composite section discharged ... are the *inputs* that earn this reachability; the theorem returns everything else as a corollary. This is the same appeal we already make for S8★, and the reason the walk-through is unnecessary: K.μ⁺ is INSERT's last arrangement-modifying step — K.ρ does not touch M — so the very state whose preconditions we discharged *is* the final post-state."

**Problem**: The load-bearing content is one clause — *K.μ⁺ is the last M-modifying step, so its discharged preconditions are evaluated at the final post-state, hence ExtendedReachableStateInvariants applies.* The surrounding sentences ("We do not re-derive these per region," "the reason the walk-through is unnecessary," "This is the same appeal we already make for S8★") narrate the proof strategy and defend the absence of a walk-through rather than advancing the argument. The "same appeal ... for S8★" back-pointer is an internal cross-reference that carries no inference.

**Required**: Keep the single load-bearing clause (last M-modifying step ⇒ discharged preconditions hold at the post-state); drop the strategy narration and the S8★ self-reference.

## OUT_OF_SCOPE

(none — the note cites only foundation ASNs and defines no out-of-scope operation.)

VERDICT: REVISE
