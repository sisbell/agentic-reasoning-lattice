# Review of ASN-0043

## REVISE

### Issue 1: Process narration in the FSP introduction
**ASN-0043, L9 proof (FSP setup)**: "Both this construction and the one for L11b (NonInjectivity, below) append a single fresh sibling link to the store while leaving content and arrangements untouched; the conformance argument is identical in both cases except for the payload. We isolate the shared argument as a lemma and then supply only the L9-specific delta."
**Problem**: This narrates how the document is organized rather than advancing the proof. The reader must skip past it to reach the actual lemma. The factoring is sound; the meta-commentary about factoring is noise of exactly the `review-mode.anti-bloat` kind.
**Required**: Delete the framing sentences. State FSP and apply it; the reuse by L11b is evident at L11b's call site.

### Issue 2: FSP is buried inside L9's proof but is shared infrastructure, forcing forward references
**ASN-0043, L9 statement** and **L11b statement**: L9's precondition reads "Σ satisfies the state-local invariants preserved by FSP (FreshSiblingConformance, enumerated in its statement below)"; L11b repeats "denotes the state-local invariants preserved by FSP (FreshSiblingConformance), enumerated in its statement below."
**Problem**: A lemma consumed by two results (L9, L11b) and by the worked example is defined mid-proof of the first result, so two separate invariant statements forward-point into it ("enumerated in its statement below"). This is the flagged accretion pattern — multiple sections deferring to one buried downstream location for their own preconditions.
**Required**: Promote FSP to a standalone subsection before L9, with the state-local invariant set named once there. L9 and L11b then cite it by name without "below," and neither statement needs to define its precondition by forward reference.

### Issue 3: Undefined notation in L9 Case B
**ASN-0043, L9 proof, Case B**: "by CPP (with t₀ = b, p = #h(b)) home(a) = home(b) = d'"
**Problem**: `#h(b)` is never defined; every other site uses `home(·)`. This is a slip for `#home(b)`. CPP's precondition (steps modify only positions beyond `p`) is being instantiated at `p = #home(b)`, so the symbol matters for checking that `#b > p`.
**Required**: Replace `#h(b)` with `#home(b)`.

### Issue 4: Endset-independence stated three times
**ASN-0043, Home and Ownership / L2 / Summary**: The "Home and Ownership" paragraph asserts home is "computed by field projection on the address alone... not attached as metadata"; L2 then formalizes the same ("`home` is a function of the address, not of the link value"); the Summary table's "Address determines" row restates it again.
**Problem**: Two prose paragraphs say the same thing in different words around the formal claim. The Home/Ownership paragraph's independence content duplicates L2.
**Required**: Let the Home/Ownership prose set up ownership and hand off to L2 for the independence claim; do not pre-state L2's content in narrative form.

## OUT_OF_SCOPE

### Topic 1: How an immutable link ceases to be discoverable
**ASN-0043, L12** correctly defers removal/discoverability to Open Questions. The one-line deferral is acceptable scoping (operations are out of scope), not a finding — noting it only to confirm it should stay a single pointer, not grow into a rationale paragraph.

VERDICT: REVISE
