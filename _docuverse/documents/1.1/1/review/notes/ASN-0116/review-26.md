# Review of ASN-0116

The mathematics here is sound. I checked the central arithmetic (`shift(q_k, n) = q_{k+n}`), the composite construction (`K.α`×n → `K.μ⁻` → `K.μ⁺` → `K.ρ`×n), the step-by-step precondition discharges, the careful distinction between ASN-0082's *gapped* `M'₀(d)` and INSERT's *filled* `M'(d)`, the re-derivation of referential integrity and content-store invariants (correctly noting I3-S3/I3-S7 can't be borrowed because INSERT breaks the content frame), the three coupling constraints, the wp derivation, and the worked example — all hold. Boundary cases (append `J=N+1`, empty subspace, front insertion `J=1`) are handled. No correctness or cross-reference defects found; all citations are to foundation ASNs.

The findings below are confined to the meta-prose accretion the `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: Restatement after the K.μ⁺ step
**ASN-0116, "INSERT as a valid composite," suffix-present case**: "The apparent 'rewrite' of the suffix has been split into a removal at the old slot (K.μ⁻) followed by a fresh insertion at a new slot (K.μ⁺), each individually legal."
**Problem**: The two preceding bullet steps already demonstrate exactly this — K.μ⁻ vacates, K.μ⁺ reinstalls, each precondition discharged. The sentence restates the just-shown decomposition in essay form; a reader skips past it.
**Required**: Delete the sentence.

### Issue 2: Prose recap duplicates the Claims Introduced table
**ASN-0116, "What we have established"**: the paragraph re-narrates the entire operation ("On the content layer, INSERT is the n-fold content allocation K.α... On the arrangement layer, INSERT is the contraction–extension pair...") and closes by echoing the intro's "Two effects, two layers" framing.
**Problem**: This content-layer/arrangement-layer recap restates every clause that the immediately following "Claims Introduced" table already enumerates, and reprises the opening "Two effects hide in that sentence." Two slots (prose conclusion, structural table) carrying the same content.
**Required**: Reduce to a single sentence naming the operation's two-layer split, or drop the prose recap and let the table stand.

### Issue 3: Repeated forward-deferral of the coupling discharge
**ASN-0116, "INSERT as a valid composite," final paragraph**: "the I-addresses range-new to the content subspace of M'(d) are exactly A_new (established below) ... J0, J1★, J1'★ and the boundary coverage property P7a are discharged there."
**Problem**: This forward-points twice to the later "document remains one coherent sequence" section, where RAN and the same coupling discharge then reappear. The deferral pointer plus the downstream restatement is the forward-reference accretion pattern.
**Required**: Either discharge the boundary couplings once at the point of first mention, or cut the forward-pointer prose and let the later section carry it without the advance notice.

## OUT_OF_SCOPE

The four Open Questions (transclusion-shared insertion points, concurrent insertions without a serializing authority, transclusion provenance, post-editing fragmentation) are correctly posed as questions, not claimed — no scope violation.

VERDICT: REVISE
