# Review of ASN-0102

## REVISE

### Issue 1: P4★ appeal at COPY's pre-state assumes COPY is always a standalone composite

**ASN-0102, X14 (J1'★ Old-branch) and "Amendment to ValidComposite★"**: "by P4★ (`Contains_C(Σ) ⊆ R`, ASN-0047) the pair `(a, d)` is *already* in `R` at the pre-state."

**Problem**: The amendment adds COPY to ValidComposite★'s atomic enumeration. That enumeration admits multi-step composites, so nothing forbids a composite such as `K.μ⁻ → COPY` in which COPY's pre-state `Σ` is an *intermediate* state, not a composite boundary. P4★ is a composite-boundary property (ExtendedReachableStateInvariants), so it is not guaranteed at an intermediate `Σ`. The X14 Old-branch discharge of J1'★ evaluates the coupling *per COPY step* and leans on P4★ at `Σ`; for an embedded COPY this is neither the right obligation (clause 2 evaluates couplings only initial-to-final for the whole composite) nor a licensed hypothesis. The "length-1 composite" framing is asserted but the enumeration does not restrict COPY to length-1.

**Required**: Either restrict COPY to standalone (length-1) composites explicitly in the amendment, or discharge J1★/J1'★ for composites that *contain* COPY as a non-initial step without relying on per-step P4★ at COPY's pre-state.

### Issue 2: X7's "freed positions vs occupied portion" passage is meta-prose the proof disowns

**ASN-0102, X7**: "We must be careful about how much of `[v, v+W)` held content pre-state, and we must keep two distinct notions apart. The *freed* positions ... This is a strictly different set from *the portion of the copy target region* ..." (~200 words), followed by "The no-overwrite conclusion does not depend on how much of `[v, v+W)` was previously populated."

**Problem**: The derivation explicitly states the distinction it spends a paragraph drawing is irrelevant to the conclusion, which rests solely on the copied/displaced range disjointness established in the first two sentences. This is prose that does not advance the proof — exactly the accretion the anti-bloat classifier flags.

**Required**: Delete the freed-vs-occupied disquisition; keep the disjointness argument and the one-line no-overwrite conclusion.

### Issue 3: Defensive justification accretion in the ValidComposite★ amendment

**ASN-0102, "Amendment to ValidComposite★"**: "P4★ is thus available at `Σ` from where `Σ` sits in the trace history, not from COPY's forward effect ... The hypothesis is justified, not merely assumed. The 'length-1 composite' reading invoked in X14 is thus licensed by this amendment, not by an implicit widening of the foundation's fixed list."

**Problem**: This is new prose around an admitted transition explaining *why the amendment is needed* and pre-rebutting an objection ("justified, not merely assumed," "licensed ... not by an implicit widening"), rather than stating what the amendment does. Once Issue 1 is resolved the substantive content collapses to one sentence ("COPY is admitted to the atomic enumeration; a standalone COPY's endpoints are composite boundaries").

**Required**: Reduce to the structural statement of the amendment; remove the defensive rationale.

### Issue 4: P1 precondition carries "load-bearing, not decorative" justification prose

**ASN-0102, Precondition P1**: "The content-subspace conjunct is load-bearing, not decorative: ... Pinning `subspace(u_i) = s_C` is exactly the hypothesis under which ASN-0058 C1 ... concludes ... so that X3 and `wp(COPY, S3★)` below are *established*, not assumed. Design intent agrees ..."

**Problem**: A precondition slot should state the condition and the property it discharges, not argue at length that the condition matters and enumerate downstream consumers (X3, wp, "design intent agrees"). The use-site inventory and "established, not assumed" framing are meta-prose.

**Required**: State the conjunct and cite C1 for resolved-address residency in one line; drop the rationale and consumer list.

### Issue 5: New/Old coupling split is restated redundantly

**ASN-0102, X14 vs. the "self-transclusion" and "empty-subspace" worked examples**: the New/Old partition and the J1★/J1'★ branch analysis are given in full in X14 ("Setup for the J1★/J1'★ discharges") and then re-narrated in prose in two worked examples.

**Problem**: Two passages say the same thing in different words. The worked examples should *instantiate* the split numerically, not re-derive the branch logic.

**Required**: In the examples, show the computed `New`/`Old` sets and which branch fires; delete the re-explanation of why each branch holds (already in X14).

## OUT_OF_SCOPE

### Topic 1: Discoverability of copied content after subsequent displacement
**Why out of scope**: The first Open Question concerns how a later operation's displacement interacts with origin/discoverability — this is downstream operation-interaction territory (and link projection lives in ASN-0098), not a defect in COPY's contract.

VERDICT: REVISE
