# Review of ASN-0043

## REVISE

### Issue 1: Exact duplicate sentence inside the FSP lemma statement
**ASN-0043, FSP — FreshSiblingConformance (local lemma)**: The sentence

> "FSP places no constraint on the endset *targets* of `ℓ`; in particular `coverage(ℓ.type)` is unconstrained."

appears **twice** in the lemma statement — once immediately before the parenthetical "(L11a is the one cross-event claim …)" and once immediately after it.

**Problem**: This is a verbatim duplication, an editing artifact from a prior cycle. The precise reader must read the same clause twice and check whether the second instance carries new content (it does not). This is exactly the "two paragraphs say the same thing in different words" pattern — here, the same words.

**Required**: Delete one of the two occurrences. Keep a single statement of the targets-unconstrained clause (placing it after the L11a parenthetical reads more cleanly, since the parenthetical interrupts the invariant list).

### Issue 2: Pre-L3 meta-paragraph defers forward and duplicates L3's own verdict
**ASN-0043, paragraph preceding L3**: "Gregory's implementation admits a relaxation that Nelson's design does not: `docreatelink` short-circuits … The legacy internal entry point `domakelink` also exposes a two-endset path. Per Nelson, every link carries a *non-empty* type endset … **L3 formalizes this requirement and fixes the resulting conformance verdict below.**"

**Problem**: Two accretion patterns compound here. (i) The closing sentence is a pure forward pointer ("L3 formalizes … below") that advances no reasoning — the reader is told the verdict exists elsewhere before being given it. (ii) The conformance verdict on arity-2/untyped links is then stated again inside L3 ("Arity-2 'untyped' links are not part of the design — where Gregory's implementation can store such links via empty-type-specset short-circuit, the resulting state lies outside this ASN's conforming link store"). The implementation relaxation and its out-of-scope verdict are thus delivered in two places.

**Required**: Keep the object-level evidence (what `docreatelink`/`domakelink` do) once, attached to L3 where the verdict lives. Drop the "L3 formalizes this requirement and fixes the resulting conformance verdict below" forward-pointer sentence; let L3 state the requirement and the verdict in one location.

### Issue 3: Redundant forward references to L9 for the ghost-address contrast
**ASN-0043, L1a and the pre-L3 paragraph**: L1a notes "ghost addresses are admitted only for endset targets (notably the type endset, **L9**), not for the home prefix"; the pre-L3 paragraph notes the type "must reference at least one tumbler (possibly a ghost, **by L9 below**)."

**Problem**: Two separate sections each insert a forward pointer to L9 to draw the same content-vs-home ghost contrast before L9 is reached. The contrast that matters locally (home prefix must be real; endset targets may be ghosts) is already carried by L1a's own membership invariant `home(a) ∈ dom(Σ.M)`; the L9 cross-reference adds nothing at either site except a deferral.

**Required**: State the home-must-be-allocated fact once at L1a without the L9 pointer (the invariant itself is the argument), and drop the parenthetical "(possibly a ghost, by L9 below)" from the pre-L3 paragraph, which is not about home addresses at all.

## OUT_OF_SCOPE

### Topic 1: Link-store/arrangement consistency under transclusion and link removal
The Open Questions already (correctly) defer the inter-store invariants under transclusion, compound-link well-formedness, and how an immutable link "ceases to be discoverable." These are operations/version-spanning concerns explicitly listed in this ASN's Scope exclusions.
**Why out of scope**: These require an operations model (MAKELINK/REMOVELINK/CREATENEWVERSION) the ASN deliberately does not define; their absence is not a defect in the state/invariant model presented here.

VERDICT: REVISE
