# Review of ASN-0070

## REVISE

### Issue 1: No worked example exercises a non-empty link-subspace resolution

**ASN-0070, "A Worked Example"**: All four configurations yield `Σ_V^{s_L} = ⟨⟩`. Configuration 4 contracts the link subspace but never resolves an endset *into* it; β_L always falls out by L14 disjointness.

**Problem**: The distinctive contribution of this ASN over a single-subspace FOLLOWLINK is the two-subspace partition (F0), and in particular the link-subspace branch of the postcondition `⟦Σ_V^{s_L}⟧_V = R(d, e)|_{s_L}`. That branch rests on the non-trivial reverse direction of F-subspace (S3★-aux + L14 ruling out `subspace(v) = s_C` when `M(d)(v) ∈ dom(L)`) and on the s_L canonical component at depth `m_{s_L}(d)`. L4 (ASN-0043) and the prose explicitly admit endset coverage straddling `dom(L)`, yet no concrete scenario ever places a covered link address into a document's link-subspace arrangement and reads back a non-empty `Σ_V^{s_L}`. The standard requires verifying key postconditions against a specific scenario; the s_L = non-empty case — the novel half — is never checked.

**Required**: Add a configuration in which `coverage(L(ℓ).eᵢ)` contains a link I-address `ℓ₀` that `d` arranges at a link-subspace V-position (e.g. `[2,1] → ℓ₀`), so that `Σ_V^{s_L}` is non-empty, and verify F-sound, F-complete, and F-subspace (`subspace(v)=s_L ⟹ subspace_I(M(d)(v))=s_L`) against the result.

### Issue 2: F-canonical is classified DEF but is load-bearing as a uniqueness theorem

**ASN-0070, "Claims Introduced"**: F-canonical is tagged `DEF`, yet its statement includes "a given `R(d, e)` admits exactly one canonical form" and F-det's *Depends* cites "F-canonical (derived above)" as the source of representational uniqueness.

**Problem**: The claim mixes a definition (the canonical-form shape) with a theorem (existence-and-uniqueness, proved over several pages in Steps 1–3). Tagging the whole thing `DEF` mislabels the proof obligation that F-det and F-empty actually lean on. A dependent reading the table cannot tell that a uniqueness theorem is being invoked.

**Required**: Split the definitional content (canonical-form shape) from the uniqueness result, or retag F-canonical as `LEMMA`/`THM` reflecting the derived uniqueness it supplies to F-det and F-empty.

## OUT_OF_SCOPE

### Topic 1: Reporting which covered I-addresses failed to resolve (partial-reach diagnostics)
**Why out of scope**: Raised correctly as an Open Question. The result form deliberately carries only what resolved; surfacing the unreached subset is a future result-form question, not an error here.

### Topic 2: Concurrency semantics during concurrent arrangement mutation
**Why out of scope**: The frame establishes state-purity for a fixed `Σ`; concurrent-transition semantics belong to a transition/scheduling ASN.

VERDICT: REVISE
