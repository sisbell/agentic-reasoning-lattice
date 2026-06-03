# Review of ASN-0075

## REVISE

### Issue 1: D-IDENT argues from a case the definition structurally excludes
**ASN-0075, Identity Preservation (D-IDENT)**: "If SHOWDELETIONS returned new identities — fresh I-addresses with the same byte values — all three guarantees would collapse. The recovered content would be unaddressable by existing links, would not match existing transclusions, and would have spurious new origin. Returning addresses is therefore not a presentation choice; it is a correctness requirement."
**Problem**: The output sets are *defined* as subsets of `dom(C)` (`DeletedFromAWithB = {a ∈ dom(C) : …}`). Returning a fresh I-address is impossible by the definition, not a hazard the proof must guard against. This paragraph imagines a counterfactual the carrier already forecloses — reviser drift. The forward consequences in the three bullets (link survival via L12/P3, transclusion integrity via S2/S3★, origin via S7) are legitimate; the "what would collapse if we did the impossible thing" rhetoric is not.
**Required**: Drop the counterfactual paragraph. The fact that output elements are members of `dom(C)` already discharges the identity claim; keep the three forward bullets and remove the "if … would collapse / not a presentation choice but a correctness requirement" framing.

### Issue 2: The composite-boundary / P4★ dependency is re-justified at four separate sites
**ASN-0075, D-EXH**: "The reachability hypothesis is load-bearing for the proof: it activates `P4★` … The hypothesis is discharged structurally by D-BOUND, where the composite-boundary nature of `P4★` is established."
**ASN-0075, D-BOUND (2nd para)**: "The per-state invariants preserved by every elementary transition … do not entail `P4★` … Restricting invocation to composite boundaries is what makes `P4★` and `P4a` available wherever the proofs in this note invoke them."
**ASN-0075, Supplementary lemma**: "The boundary hypothesis is load-bearing for the same reason as in D-EXH — the argument invokes P4★ — and D-BOUND supplies it."
**ASN-0075, D-RECONS**: "P4a (historical fidelity, ASN-0047; available at this invocation by D-BOUND) ensures …"
**Problem**: Four paragraphs in different sections defer to the same downstream fact (P4★/P4a are composite-boundary properties supplied by D-BOUND). This is forward-reference accretion plus axiom-rationale prose — D-BOUND's second paragraph explains *why the axiom is needed* rather than what it states. The "load-bearing," "discharged structurally," "available at this invocation" phrasing recurs without advancing any argument.
**Required**: State the composite-boundary dependency once, at D-BOUND, including the single substantive fact (intra-composite states may falsify P4★). At each use site, cite D-BOUND tersely (e.g. "P4★, available by D-BOUND") and delete the load-bearing/discharge essay.

### Issue 3: Recurring "not X but Y" rhetorical closings in structural slots
**ASN-0075, D-IDENT**: "Returning addresses is therefore not a presentation choice; it is a correctness requirement."
**ASN-0075, Distinguishing Deletions from Additions**: "The provenance-aware definition above is therefore not optional — it is what makes the operation deliver on its name."
**ASN-0075, D-SUBSP**: "Restricting SHOWDELETIONS to the content subspace is therefore not an implementation simplification but a structural necessity — … not merely asserted."
**Problem**: These are defensive editorializing closings that restate a conclusion already proven, in emphatic prose. They are essay content in claim slots; the precise reader must skip them to reach the next claim.
**Required**: Trim to the derived fact. The derivations preceding each (output ⊆ dom(C); the additions/deletions conflation; the L0/L14/S3★/CL-OWN witness-impossibility chain) stand on their own without the rhetorical coda.

## OUT_OF_SCOPE

### Topic 1: Restoration, multi-document families, concurrency, span-presentation of output
**Why out of scope**: These appear only as Open Questions, correctly deferred — restoration mechanics, >2-document witness structure, and concurrent-snapshot consistency are future ASNs, not gaps in this one. No claim is defined for them, so no flag is needed; noting only that their placement as Open Questions is appropriate.

VERDICT: REVISE
