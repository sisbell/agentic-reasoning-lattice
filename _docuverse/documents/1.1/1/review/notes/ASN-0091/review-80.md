# Review of ASN-0091

## REVISE

### Issue 1: L-chain lemma introduction enumerates downstream consumers and justifies its own promotion
**ASN-0091, "Chain Disjoint-Adjacency Lemma"**: "Several of the run-decomposition witnesses and worked examples below turn on the same structural fact... Because the result is invoked from three separate places — the coalescence witness (RE-coal), the equality witness (RE-eq), and the shared-I-address worked example — we state it once as a named lemma rather than inline."
**Problem**: This is the flagged anti-bloat pattern verbatim — a definition's introduction enumerating its downstream consumers and justifying the structural decision to make it a lemma (matching the recent "promote inline lemma" revision). It advances no reasoning about *what L-chain says*; the use-site inventory rots as consumers change.
**Required**: Delete the two-sentence framing. State the lemma directly. Citations at the use sites (RE-coal, RE-eq, WE4) already point back to it; the lemma needs no forward inventory.

### Issue 2: RE-trans conclusion (iii) overclaims a biconditional that is false in the collapse case
**ASN-0091, "Cross-Document Transclusion Preserved"**: "(iii) holds exactly when origin(a) ≠ d (the rearrangement target)... while if origin(a) = d the rearrangement permutes origin(a)'s own arrangement and (iii) fails."
**Problem**: "exactly when" / "(iii) fails" asserts the converse — that origin(a) = d forces (iii) to fail. But the net-effect collapse branch (your own WE5) and the identity case both yield Σ' = Σ, so when origin(a) = d the arrangement is unchanged and (iii) *holds*. Only the sufficient direction (origin(a) ≠ d ⟹ (iii)) is established and is what the claims table records. The biconditional framing is incorrect.
**Required**: Replace "holds exactly when origin(a) ≠ d" / "(iii) fails" with the sufficient-direction statement: origin(a) ≠ d guarantees (iii); when origin(a) = d, (iii) is not guaranteed (though it may still hold, e.g. under collapse).

### Issue 3: "Reachability scope" sub-paragraph describes an argument not taken
**ASN-0091, "Reachability scope of the realisation"**: "(A reachability-independent, invariant-by-invariant preservation argument would lift the realisation to all invariant-satisfying Σ; we do not pursue it, since every state REARRANGE_K is applied to in this development arises along a trace from Σ₀ and is reachable by construction.)"
**Problem**: Defensive justification for a scoping choice plus a sketch of a path deliberately not pursued — essay content in a structural slot. The scoping (RA-adm claimed only for reachable Σ) is already stated in the preceding sentence and in the RA-adm claims-table row; this parenthetical adds only rationale.
**Required**: Drop the parenthetical. The scope restriction stands on the prior sentence alone.

### Issue 4: Worked-example openers justify each example's inclusion rather than orienting to its content
**ASN-0091, "Worked Example — Net-Effect Collapse"**: "Because this branch determines which realiser discharges RA-adm, we exhibit it concretely." (similarly WE3: "The single new fact this trace adds is...")
**Problem**: These sentences justify *why the example exists* (a document-structure rationale) rather than stating what it shows. The examples themselves are legitimate and distinct; the existence-justification framing is the noise.
**Required**: Replace with a direct statement of what the trace exhibits (e.g., "This trace exhibits a non-identity pivot π for which R-P1/R-P2 yield M'(d) = M(d)"), or delete the framing entirely.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: REARRANGE_K fixes the cut subspace to s_C (CS3), so rearranging the link subspace is genuinely new territory, correctly deferred to the Open Questions rather than treated as a gap here.

VERDICT: REVISE
