# Channel Assignment — ASN-0096 review-2

**Date:** 2026-05-24 08:37

## Issue 1: LP-EXT headline statement is contradicted by the worked example
Reason: The ASN's own prose already supplies the composed form (`π(proj) ∪ new-coverage-positions`) immediately after the headline; the fix is to elevate that statement to the claim and the claims table. Derivable from existing content.

## Issue 2: LP-CONTR breaks under K.μ⁻ with within-subspace shift
Reason: The composed form `π'(proj ∩ R_ret)` already appears in the worked example's prose; the resolution between the ASN-0047 quote (pure restriction) and the example's shift is a presentation choice the author can make consistently. Derivable from existing content.

## Issue 3: Atomic decomposition arity contradicts the displacement story
Reason: The modeling choice — whether K.μ⁺ and K.μ⁻ are defined to include within-subspace shifts or whether the shift requires a composed K.μ~ atom — is a spec-internal decision; once committed, LP-MAP, LP-EXT, and LP-CONTR align. The ASN already has both readings present in prose.

## Issue 4: LP-MAP completeness is asserted without enumeration
Reason: The full list of seventeen FEBE commands is not in the ASN; need Nelson for design intent on the command set and Gregory for which commands udanax-green actually implements and how they decompose into POOM mutations.
Nelson question: What are the seventeen FEBE editing and document commands, and what is each command's intended state-level effect — in particular, which ones beyond INSERT, COPY/VCOPY, DELETEVSPAN, REARRANGE, APPEND, MAKELINK, CREATENEWDOCUMENT, CREATENEWVERSION can affect a document's arrangement?
Gregory question: Which of the seventeen FEBE commands does udanax-green implement, and what is each command's decomposition into POOM mutations (or other arrangement-touching operations) in the C source?

## Issue 5: LP-CON title and statement misalign; coverage-not-yet-allocated case unaddressed
Reason: The title/statement misalignment is internal wording, but the speculative-coverage question (what happens when a later K.α allocates an I-address already inside an existing endset's coverage) is a design-intent question that the ASN's own L4 paraphrase ("future allocations") raises but does not answer.
Nelson question: Does the design intend endset coverage to forward-reference addresses allocated after link creation? When a future K.α allocates an I-address that falls within an existing endset's coverage, is that address considered part of the link's effective referenced set, and what discipline (if any) governs "well-behaved" endset specifications to prevent or admit this?

## Issue 6: Projection type signature treats a dependent product as Cartesian
Reason: Pure type-theoretic restatement; the dependence of `Σ.E_doc` on `Σ` is already implicit in the ASN, and the fix is to present it as a dependent product or add a precondition. Derivable from existing content.

## Issue 7: "Boundary cases test the type signature directly" misclassifies the cases
Reason: Wording fix; the boundary cases as written test structural/semantic edge behaviors of the projection definition, not signature totality, and the rephrasing is straightforward. Derivable from existing content.

## Issue 8: `footprint` is used in LP-NOD without being defined alongside `proj` and `render`
Reason: `footprint(ℓ, i, Σ) := {d ∈ Σ.E_doc : proj(Σ.L(ℓ).eᵢ, d, Σ) ≠ ∅}` is definable in terms of `proj`; the fix is to lift this definition into the projection section before its first use. Derivable from existing content.

## Issue 9: LP-DISC "derivation walk" does not establish the biconditional
Reason: Since `discoverable` is *defined* by the RHS, the biconditional is true by definition; the fix is to reframe the walks as well-definedness arguments and state the definitional nature plainly. Derivable from existing content.
