# Review of ASN-0115

I checked every claim's proof. The mathematical content is genuinely rigorous: the Confinement lemma's appeal to T5 is sound (preconditions `p ≼ s`, `p ≼ reach(σ)`, `s ≤ t ≤ reach(σ)`, `#p = m−1 ≥ 1` all discharged); R6's no-interior-hole/terminal-overrun sharpening covers every case (`V_S(d)=∅`; `act≠∅` forcing a canonical start; `act=∅ ∧ V_S(d)≠∅` split into the two disjoint sub-cases, with the third sub-case correctly shown impossible); R7's comparability requirement is honestly identified as necessary (divergent branches can bind one address to differing values); R8's link-vacuity is closed by CL-OWN + CL-UNIQ; R11's single-live-condition wp is a correct decomposition (S3★ supplies membership, S0 supplies permanence). The worked instances all compute correctly. No correctness gap found. The one finding is the residual duplication left by the recent R9 sharpening.

## REVISE

### Issue 1: R9 prose re-asserts the box's kind-asymmetry conclusion rather than confining itself to the derivation
**ASN-0115, "What co-delivery reveals: coherent multi-origin assembly" (R9)**:

Box: "...a **link** item carries the address `a` itself (R10), so its home `home(a)` is recoverable from the delivered output; a **content** item carries only the value `Σ.C(a)` (R1), so its origin `origin(a)` is *not* recoverable from the output — it is determinate only through the resolution mapping `v ↦ a`, an internal artifact of computing `deliver`. Co-assembly thus preserves link home in the stream while collapsing content origin out of it; whether content origin must instead travel inline is deferred (Open Question 1)."

Prose, second half: "...a link item carries the address `a`, so its `home(a)` is recoverable from the delivered stream itself; a content item carries only `Σ.C(a)`, so its `origin(a)` survives only in the resolution mapping `v ↦ a`, an internal artifact of computing `deliver`. Co-assembly preserves link home in the output and collapses content origin out of it, with inline content provenance deferred (Open Question 1)."

**Problem**: These two passages state the same conclusion in nearly the same words — the link-carries-`a`/content-carries-value inference, the "resolution mapping `v ↦ a`, internal artifact" phrasing, the "preserves link home / collapses content origin" summary, and the Open Question 1 deferral all appear verbatim in both. A precise reader reaches the prose and re-reads the box. The prose's *first* half does real work the box does not — "Determinacy, though, is automatic — `origin` and `home` are functions of the resolved address, so no faithful resolution could lose it" justifies the box's "determinate through the resolution mapping" phrase. The second half adds nothing the box has not already stated, including its own one-step inferences. This is the accretion the anti-bloat classifier targets (two passages saying the same thing; the same downstream deferral stated twice), and it reads like the R9 sharpening was pasted into both the box and the prose rather than into one.

**Required**: Keep the box as the normative statement. Confine the prose to the determinacy-derivation it uniquely supplies (the "obligations" framing plus "determinacy is automatic because `origin`/`home` are functions of the resolved address"), and delete the second half's verbatim re-statement of the recoverability asymmetry and the duplicate Open Question 1 deferral.

## OUT_OF_SCOPE

(none — R10 correctly delivers a link *reference* `⟨ref, a⟩` and explicitly defers endset-structure reading to READLINK/FOLLOWLINK; no extent-reporting or link-structure claim is defined here.)

VERDICT: REVISE
