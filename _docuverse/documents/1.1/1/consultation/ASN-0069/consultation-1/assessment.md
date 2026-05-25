# Channel Assignment — ASN-0069 review-1

**Date:** 2026-05-25 02:53

## Issue 1: V8c and V8 prose cite ASN-0068
Reason: The fix is editorial — drop the ASN-0068 citation and restate symmetry as following from set equality of the V-position pair set, which is derivable from V4a and V5 already in this ASN.

## Issue 2: V1 derivation misidentifies the producing allocator
Reason: The reviewer has already identified the correct allocator (`A_v(d_src)`) and the correct foundation (ASN-0047's Allocator hierarchy). The fix is to update the citation; no external evidence needed beyond what foundations supply.

## Issue 3: V1 derivation cites NodeUniqueAllocation for a document
Reason: The reviewer has identified the correct citations (T10a's general allocator discipline and Allocator hierarchy definition) from foundations already in scope. Purely a citation correction.

## Issue 4: V9 derivation uses J1, not J1★
Reason: Pure citation update from J1 to J1★ within the extended-state framework already established by V0's composite verification. Substantive conclusion unchanged.

## Issue 5: V4 strengthens J4 without acknowledging the extension
Reason: The strengthening is real and the ASN's own prose justifies it on semantic grounds, but committing to literal V-position and I-address inheritance as a normative design commitment (rather than one admissible implementation among many) requires confirming Nelson's intent and Gregory's behavior.
Nelson question: Does the design require that a fork preserve V-positions and V→I mappings literally (same tumblers, same images), or does it only require that the inherited content be reachable from `d_new` in some structurally faithful way (admitting rebased V-positions or rearranged correspondences)?
Gregory question: Does `docreatenewversion` install V-positions in `d_new` that are literally equal as tumblers to the source's content-subspace V-positions, with literally equal I-addresses at each position — or does the V-span extraction via `retrievedocumentpartofvspanpm` rebase, renumber, or otherwise transform V-positions in the new version's arrangement?

## Issue 6: V7 admits two distinct behaviors
Reason: Non-determinism in a normative spec needs to be resolved or explicitly parameterized; both Nelson's design intent and Gregory's implementation are needed to choose normatively or to justify parameterization.
Nelson question: When `CREATENEWVERSION` is invoked on a source with no content, does the design intent require rejection, require producing an empty new version, or treat this case as outside the operation's specified domain?
Gregory question: When `docreatenewversion` is invoked on a source whose content subspace is empty, does the operation report failure to the caller, produce a new version entity with an empty arrangement, or behave in some other observable way?

## Issue 7: V11a prefix transitivity derivation is informal
Reason: Derivation of Prefix transitivity from its ASN-0034 definition plus T0's `≤` transitivity is mechanical and can be constructed inline using foundations already cited.

## Issue 8: V8 implicit state for V_{s_C}(d_src)
Reason: Pure clarification — pick pre-fork or post-fork as the reference state and state it explicitly. V5 ensures equality, so the choice is presentational, not substantive.

## Issue 9: V10(a) cites SubAllocatorAxiom for A_v
Reason: Citation correction from SubAllocatorAxiom to the Allocator hierarchy definition in ASN-0047 — same form as Issues 2 and 3, derivable from foundations.
