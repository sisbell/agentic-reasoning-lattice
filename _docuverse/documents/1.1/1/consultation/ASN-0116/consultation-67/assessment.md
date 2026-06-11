# Channel Assignment — ASN-0116 review-67

**Date:** 2026-06-11 00:17

## Issue 1: The worked example posits coverage sets that no endset can have
Reason: The fix is internal — the corrected reading is pure foundation arithmetic already cited in the ASN (PrefixSpanCoverage from ASN-0043, ChainMembershipForOrigin from ASN-0093, the `#E = 2` depth of chain/arrangement addresses), and the review spells out the exact span-form restatement and the subtree-intersection discharge needed. No design-intent or implementation question is open; the example just needs to be rewritten against well-formed span-denoted endsets.

## Issue 2: F-SUB cites I3-X/I3-CX without the gapped/filled bridge it applies everywhere else
Reason: Internal fix — the missing half-step (every block position is subspace-`S` by OrdShiftHom, so the cross-subspace slice of the filled arrangement equals the gapped one) is already established in the ASN's own K.μ⁺ discharge; the revision only needs to extend the bridge statement or add one line at F-SUB. Neither design intent nor implementation evidence bears on a citation-chain repair.

## Issue 3: PROV duplicates I-PROV (anti-bloat)
Reason: Internal editorial consolidation — folding the not-deferred timing clause into I-PROV (or the DOCISPAN paragraph) and dropping the redundant named claim requires no new facts from either channel, only restructuring of content already present.
