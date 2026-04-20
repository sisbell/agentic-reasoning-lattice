# Revision Categorization — ASN-0063 review-3

**Date:** 2026-03-21 18:50

## Issue 1: Subspace identifier constraint unestablished; S8a verification built on false premise
Category: INTERNAL
Reason: The derivation s_L > 0 follows from T4 + L1 already cited in the ASN, and verifying link-subspace positions satisfy S8a uses only properties present in the specification. This is a proof-correction task using existing definitions.

## Issue 2: Framework extension permits orphan links without acknowledgment
Category: NELSON
Reason: Whether links may exist in dom(L) without placement in any document's arrangement is a design intent question about link lifecycle — the framework permits it but the ASN neither prevents nor endorses it.
Nelson question: Must every link be placed in its home document's arrangement at creation time, or are orphan links (existing in the link store but not in any document's arrangement) valid system states — for example, after link withdrawal?

## Issue 3: Link-subspace V-position depth m_L undetermined
Category: INTERNAL
Reason: The constraint m_L ≥ 2 is derivable from existing definitions: shift at depth 1 alters the subspace identifier, violating K.μ⁺_L's own precondition `subspace(v_ℓ) = s_L`. No external evidence needed.

## Issue 4: CL0 proof cites wrong property and elides an intermediate step
Category: INTERNAL
Reason: The correct citations (V-extent definition, D-SEQ, S8-depth) are all established in the referenced ASNs. The fix is replacing an incorrect reference and making an implicit step explicit using already-available properties.

## Issue 5: VSpanImage definition missing well-formedness precondition
Category: INTERNAL
Reason: T12 is already defined in ASN-0034 and used elsewhere in this ASN. Adding it as a precondition to VSpanImage is a straightforward gap-fill from existing definitions.

## Issue 6: Unformalized principle cited as established property
Category: INTERNAL
Reason: The fix is editorial: reframe "owner-only modification" as a design principle rather than a proven guarantee, since no foundation invariant establishes it. The ASN already has four other formal principles backing CL4, so the reframing is self-contained.

## Issue 7: Inconsistent notation s_C^V
Category: INTERNAL
Reason: The ASN uniformly uses s_L for both V-position and I-address contexts without superscript distinction. s_C^V appears once and is inconsistent with every other occurrence of s_C. This is a notation typo fixable from the ASN's own conventions.
