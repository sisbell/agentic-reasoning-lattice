# Review of ASN-0076

## REVISE

### Issue 1: The structural-vs-arrangement discoverability distinction is stated three times with redundant forward deferrals

**ASN-0076, E4 intro / E7 closing / E11 intro**:
- E4 intro: "the spans are present in the endsets and recoverable by inverse link-store lookup; discoverability is arrangement-conditional, settled in E11."
- E7 closing: "Whether `ℓ_sup` is *discoverable* from a document is therefore a separate question: discoverability is arrangement-governed, made precise in E11 below."
- E11 intro: "E7 settles the supersession link's referents as a property of `Σ'.L` alone. The question a reader actually asks — *can I discover `ℓ_sup` from document `d`?* — we make precise by computing the weakest precondition..."

**Problem**: The same distinction (structural referent-presence vs. arrangement-conditional discoverability) is asserted in three different sections, with two forward pointers (E4, E7) both deferring to E11. This is the "multiple paragraphs defer to the same downstream location" + "two paragraphs say the same thing in different words" pattern. The precise reader meets the same observation three times before reaching the claim that actually settles it.

**Required**: Keep the distinction in one place — E11's intro, adjacent to the claim that formalizes it. Delete the forward-deferral clause from E4's intro ("settled in E11") and the closing paragraph of E7's proof. E7's proof should end at its established memberships; the arrangement caveat is E11's content.

### Issue 2: Defensive reassurance sentence after the composite definition

**ASN-0076, The Composite (closing line)**: "The composite is a named pattern of two existing primitive applications, no different in kind from any other sequence of transitions a user might issue."

**Problem**: This sentence advances no reasoning — it is a reassurance that the composite is unremarkable. The substantive content (EDITLINK is two K.λ steps, admissible under K.λ preconditions) is already stated and is discharged in E0. A defensive "no different in kind" claim is meta-prose that the reader must skip.

**Required**: Delete the sentence. The definition block and E0 already establish that EDITLINK is a sequence of two ordinary K.λ applications.

## OUT_OF_SCOPE

None. The Open Questions section correctly defers supersession-chain semantics, cycle detection, retraction, authorization of `d_new`, and link/content-edit interaction to future ASNs without asserting claims about them.

VERDICT: REVISE
