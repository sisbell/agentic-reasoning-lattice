# Review of ASN-0087

## REVISE

### Issue 1: Symmetry claim contradicts the home-only reflexive route

**ASN-0087, *What Is Indexed?* and M-DiscSymmetry**: "the home document has no privileged position" / "the home document has no privileged role in LP12's definition. Any asymmetry of outcome reflects asymmetry of arrangement-reach, not a privileged status."

**Problem**: The ASN itself proves the opposite for one route. In *Weakest Precondition*, Case 2: "Because `ℓ` enters only `d`'s arrangement, this route [reflexive] is available to the home document alone." MAKELINK *itself* creates an arrangement-reach asymmetry by placing `v_ℓ ↦ ℓ` into the home document and no other. So a reflexively-authored link is discoverable from its home regardless of prior arrangement (M-Reflexive), a capability no `d_target ≠ d` can have. A precise reader meeting the unqualified "no privileged position" in *What Is Indexed?* and then Case 2's "available to the home document alone" must reconcile the conflict unaided. The two are technically compatible only under the LP12-definitional reading, which the *What Is Indexed?* sentence does not carry.

**Required**: Qualify the symmetry statement to carve out the reflexive route — state that MAKELINK does privilege the home document with respect to reflexive self-discovery (by adding `ℓ` to its arrangement alone), and that symmetry holds only for the standard content-reach route. Reconcile this with Case 2 explicitly rather than leaving the reader to.

### Issue 2: Duplicated symmetry message across two sections

**ASN-0087, *What Is Indexed?* and M-DiscSymmetry**: both state, in different words, that discoverability is governed by arrangement-reach uniformly and the home document is not privileged.

**Problem**: This is the flagged pattern "two paragraphs in the same document say the same thing in different words." The claims-table entry M-DiscSymmetry restates the prose conclusion of *What Is Indexed?* without adding content.

**Required**: State the symmetry property once (with the Issue 1 qualification) and let the claims table reference it, rather than re-prosing it.

### Issue 3: Accreted protocol-layer meta-prose in *Inputs*

**ASN-0087, *Inputs*, "Reflexive authoring and prediction"**: the paragraph opens with "'Not a parameter' is weaker than 'unknowable'" and closes with "Reflexive authoring is therefore a protocol-layer capability built atop the substrate's deterministic derivation, not a substrate parameter."

**Problem**: The substantive claim — `ℓ` is deterministically derivable from `Σ` but is not an operation parameter, so reflexive authoring requires predicting `ℓ` — is worth stating. The surrounding elaboration ("Establishing this no-intervening-emission condition ... is a protocol-layer obligation; the substrate operation derives `ℓ` from whatever state it runs against and makes no guarantee that an earlier prediction still holds") is justificatory meta-prose explaining substrate/protocol boundaries, and the closing sentence restates the opening. This is the accretion the `anti-bloat` classifier targets around recently-revised reflexive-authoring prose.

**Required**: Compress to the substantive claim (deterministic derivation + prediction soundness condition); drop the boundary-rationale restatement.

### Issue 4: Repeated deferral to "Weakest Precondition, Case 2"

**ASN-0087, *A Worked Example* (Reflexive variant) and M-Reflexive (claims table)**: both defer the reflexive derivation to "*Weakest Precondition for Discoverability*, Case 2."

**Problem**: Matches the flagged pattern "multiple paragraphs in different sections defer to the same downstream location." Minor, since single-source-of-truth pointers are preferable to duplication — but two pointers plus the Reflexive variant's placement-justifying sentence ("the general derivation ... is given once ... here we only check that the hypothesis holds") add navigational overhead.

**Required**: Acceptable to keep one pointer; drop the placement-justification sentence in the Reflexive variant.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching endsets
The first Open Question (constraints on endsets referencing not-yet-allocated addresses) is correctly deferred — L4 (ASN-0043) permits such spans, and tightening that constraint belongs to a future endset-discipline ASN, not here.

VERDICT: REVISE
