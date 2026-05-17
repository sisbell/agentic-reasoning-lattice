# Channel Assignment — ASN-0086 review-9

**Date:** 2026-05-16 18:58

## Issue 1: R0a Case 2 invokes an unstated documents-antichain assumption
Reason: The reviewer's alternative argument (direct zero-count reasoning from L1: if `a ≼ a'` with `zeros(a) = zeros(a') = 3`, the extension adds no zeros, forcing `home(a) = home(a')`) is derivable entirely from invariants already cited in the ASN. No external evidence needed; the fix is rewriting Case 2's argument using L1 + chain-prefix-preservation already in scope.

## Issue 2: The `s_C ≠ s_L` convention is invoked without formal statement
Reason: This is a formalization-hygiene fix — either state `s_C ≠ s_L` as an axiom adjacent to Setup or locate the existing clause in ASN-0036/0043 where it's pinned. Both options are internal to the lattice; no design-intent or implementation-evidence question is at stake, since the distinctness is already operationally assumed throughout the proof chain.

## Issue 3: Emit_K does not commit to the sibling-frontier discipline
Reason: The choice between tightening Emit_K to commit to Step 2's construction vs. propagating the discipline-conditional qualifier is a substrate-design decision that depends on whether the link-emission primitive was intended to be flat (Nelson) and whether the implementation ever deposits links at strict prefix-extensions of existing links (Gregory). The granf2.c:170–175 citation is suggestive but not exhaustive across the codebase.
Nelson question: Was link emission designed so that every link is sited as a sibling within its home document's link allocator, with no link ever placed as a child of another link?
Gregory question: Does any path in udanax-green ever deposit a link at an address that is a strict prefix-extension of an existing link address, or is the `lowerbound + 1` / `docaddr + 2` pattern in `findisatoinsertmolecule` the only link-emission discipline in the substrate?

## Issue 4: "Three emissions" in R6b's example, only two described
Reason: Editorial mismatch between announced count and exhibited steps; the reviser decides whether the illustrative argument needs a third emission or whether "three" should be corrected to "two." Internal to the ASN.
