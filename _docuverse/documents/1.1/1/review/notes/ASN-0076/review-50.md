# Review of ASN-0076

## REVISE

### Issue 1: E4 lead-in over-claims discoverability

**ASN-0076, "The Supersession Relationship" (lead-in to E4)**: "E4 states precisely what the link model establishes: the spans are present in the endsets and recoverable by any discovery operation."

**Problem**: The clause "and recoverable by any discovery operation" is not what E4 establishes, and it contradicts the ASN's own later results. E4 proves only structural membership of the spans in `Σ'.L(ℓ_sup)` — an inverse link-store fact. Discoverability is a *separate, conditional* property: E11 proves that when neither `ℓ_old` nor `τ_sup` is arranged in a document, `ℓ_sup` is **orphaned** (LP17) and discoverable from no document. The entire E7→E11 development exists to separate structural presence from discoverability; this lead-in collapses the distinction and asserts the false direction.

**Required**: Drop "and recoverable by any discovery operation," or qualify it to structural presence only (e.g., "the spans are present in the endsets and recoverable by inverse link-store lookup; discoverability is arrangement-conditional, settled in E11").

### Issue 2: E4 closing is a pure forward-reference deferral

**ASN-0076, E4 (closing sentence)**: "The coverage these spans induce — and hence the structural relationship the supersession link bears to the entities at `ℓ_old` and `ℓ_new` — is carried by E7 below."

**Problem**: This sentence advances no reasoning within E4; its only content is "coverage is treated in E7." Combined with E7's own closing pointer ("made precise in E11 below"), this is the forward-reference accretion the anti-bloat classifier targets — a chain of deferral sentences a precise reader must skip past. E7 immediately follows E4 and is plainly the coverage claim; the pointer is navigation, not argument.

**Required**: Delete the E4 closing sentence. E7's closing carries enough substantive content (the inverse-lookup-vs-arrangement distinction) to stand without E4 announcing it in advance.

## OUT_OF_SCOPE

### Topic 1: Supersession-chain invariants, cycle detection, and "current successor" computation
The Open Questions enumerate chain formation, retraction semantics, multi-link supersession, and reader-side resolution policy. These are correctly deferred — they require new state or new conventions beyond the EDITLINK composite, and belong to future ASNs.

### Topic 2: Authorization of `d_new` selection
E6's application-layer note defers who may publish a supersession (executor/capability model) to a future authorization ASN. This is genuinely new territory, not a gap in EDITLINK.

VERDICT: REVISE
