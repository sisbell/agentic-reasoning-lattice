# Review of ASN-0103

I checked the allocation argument (Effect One), the frontier definition `D_A = E ∩ S(A,2)`, the freshness/distinctness reasoning, the single-`K.δ` decomposition, the worked example, and the full `ExtendedReachableStateInvariants` + P3 discharge. The mathematics is sound: the length-restriction on `D_A` correctly separates the document chain `S(A,2)` from version chains `S(d_src,1)` (length `≥ #A+3`), both inclusions of `D_A = E ∩ S(A,2)` are proven, freshness collapses cleanly to `d ∈ S(A,2)\E`, and the distinctness/invariant discharges hold. The worked example concretely demonstrates the filter's necessity (the `inc(v1,0)` version-collision). All cross-ASN references are to foundation ASNs. No correctness defect found.

The note carries the `review-mode.anti-bloat` classifier, and a few residual meta-prose instances remain.

## REVISE

### Issue 1: Defensive justification in the input section
**ASN-0103, The Operation's Input**: "There is no content argument. This is not an omission — it is the defining shape of the operation."
**Problem**: "This is not an omission" is defensive meta-prose — it argues against an objection the reader has not raised rather than advancing the claim. The surrounding statements ("Content enters a document only through later operations…"; "Creation deposits nothing") are statements of what the operation does and stand on their own.
**Required**: Drop the defensive clause; keep the substantive "Creation deposits nothing" statement.

### Issue 2: Methodological narration that does not advance the argument
**ASN-0103, Discovering the Effects / Effect One**: "We reason from Nelson's intent backward to the formal post-state."; "Here we must be careful:"; "we need not re-derive these from the increment laws."
**Problem**: These are narration about the proof process, not steps of it. The reader must skip past them to reach the reasoning. The genuine subtlety (versions masquerade as documents under a parent-only filter) is already carried by the formal `D_A` proof and the worked example.
**Required**: Excise the narration; let the `D_A = E ∩ S(A,2)` proof and the worked example carry the point. Trim to the claim and its derivation.

## OUT_OF_SCOPE

### Topic 1: Effective ownership (ω_Σ) and entity-set/registry coupling
**Why out of scope**: The note proves only *structural* ownership `owns(π,d) ≡ pfx(π) ≼ d` (O1) and explicitly defers effective ownership `ω_Σ` and the entity-set/baptismal-registry coupling to Open Question 6. This is correctly scoped — that coupling is future-ASN territory, not a defect here. CND.refer's "no other owner could mint the same address (B8)" is the cross-namespace (unconditional) case of B8, properly grounded via B7 without registry machinery.

VERDICT: REVISE
