# Review of ASN-0069

## REVISE

### Issue 1: §"Subspace Selectivity" transcribes the quoted CL-OWN formula in prose before applying it
**ASN-0069, §"Subspace Selectivity"**: After quoting CL-OWN's formula `(A d, v : ... subspace(v) = s_L : origin(M(d)(v)) = d)`, the next paragraph says: "For every V-position in d's arrangement that lies in the link subspace, the I-address at that position has origin = d."

**Problem**: This sentence is an exact natural-language transcription of the formula just quoted. The subsequent paragraph ("CL-OWN requires every link-subspace V-position's image to have origin = d_new, so transcluding d_op's links — whose origin is d_op ≠ d_new — would violate it") performs the actual application. The transcription sits between the quote and the application, restating the quote without advancing the argument — the "two statements say the same thing in different words" pattern the anti-bloat pass targets.

**Required**: Delete the transcription sentence; the quoted formula plus the application paragraph carry the derivation. Retain "Links in a document's arrangement are home-document links" only if the interpretive label is used downstream.

### Issue 2: Redundant foundation citation in V12(b)
**ASN-0069, §"Permanence Across Source and Fork", V12(b)**: "`(A a : a ∈ ran(M'(d_new)) : a ∈ dom(C''))` for every subsequent state `Σ''` (P0, S0/S1)"

**Problem**: P0 (ASN-0047) is documented as subsuming "ASN-0036's S0 (ContentImmutability) and S1 (StoreMonotonicity)." Citing `(P0, S0/S1)` names the subsuming property and the two properties it subsumes for the same fact. The triple citation is the "use-site inventory" form of accretion — one citation discharges the claim.

**Required**: Cite P0 alone in V12(b).

### Issue 3: Mutual-isolation-via-V5a is re-instantiated three times
**ASN-0069, §"Frame: Source Isolation"** (bidirectional paragraph), **V10(b)**, and **V12 consequence paragraph**: each states that modifications targeting one document do not propagate to the other, "by V5a instantiated at the other document."

**Problem**: V5a is the *general* lemma — it already establishes per-document independence for any `d*` and any sequence with no step M-targeting `d*`, in both directions. The bidirectional paragraph immediately after V5 re-derives this special case inline, and V10(b)/V12 re-instantiate it again. The §"Frame: Source Isolation" bidirectional paragraph adds nothing beyond a direct reading of V5a.

**Required**: Drop the bidirectional paragraph (or compress to one clause pointing at V5a); let V10(b) and V12 carry the two context-specific instantiations that actually do work.

## OUT_OF_SCOPE

### Topic 1: V6a link-discoverability machinery (coverage / project / discoverable_from)
**ASN-0069, §"Subspace Selectivity", V6a**: introduces three new definitions — `coverage(e)`, `project(a, i, d, Σ)`, `discoverable_from(a, d, Σ)` — none of which is supplied by any foundation (ASN-0047 defines Endset/Link/L0–L14/CL-OWN but not link *resolution* to V-positions).

**Why out of scope**: These are link-resolution semantics, and "link semantics" is an out-of-scope topic for CREATENEWVERSION. The fork's own guarantee over links is already fully discharged by V6 (`V_{s_L}(d_new) = ∅`) plus the `L' = L` frame; the discoverability-inheritance lemma layers link-traversal primitives on top to derive a consequence that belongs in a link-operations ASN. The invented `coverage`/`project`/`discoverable_from` vocabulary should be defined there and consumed, not minted here.

VERDICT: REVISE
