# Channel Assignment — ASN-0086 review-3

**Date:** 2026-05-16 15:59

## Issue 1: R0 Step 3 hand-waves the chain construction
Reason: The proof asserts universal reachability of structurally-valid addresses via T10a chains, but T10a's at-most-once spawning constraint may make some structurally-valid addresses unreachable depending on allocator history. Implementation evidence clarifies whether the allocator realizes universal reachability or whether Step 2 must filter to reachable candidates.
Gregory question: Does the udanax-green allocator support reaching every structurally-valid link address under a document seed (zeros=3, E₁=s_L, T4-valid), regardless of prior allocations in that document's link subtree, or are some structurally-valid addresses permanently unreachable once nearby allocators have committed?

## Issue 2: Citation error — `zeros(d) = 2` cites the wrong ASN-0036 axiom
Reason: Pure citation fix derivable from ASN-0036's own axiom statements (S7a is content-scoping; S7d is the document-tumbler zeros=2 fact). No external input needed.

## Issue 3: Introductory claim "all visible substrate change reduces to Emit" overreaches
Reason: The ASN itself defines `→` with three primitives, making the correct scope ("relational layer") visible from its own content. Rewording is internal.

## Issue 4: R5 Stage 1 mis-attributes the invariant-preservation witness to L11b
Reason: The replacement citation (R0's construction or L1c's chain discipline) is already established within ASN-0086 and ASN-0043 as available. Internal citation correction.

## Issue 5: Worked sketch invokes R0 with placement constraints beyond its stated guarantee
Reason: Both fix options (strengthen R0 or appeal to R0's proof construction) are derivable from the existing R0 proof's Steps 1–2, which already exhibit the relevant freedom. Internal mechanical revision.

## Issue 6: "Σ' extends Σ" is used but never defined
Reason: Adding a one-line definition tying "extends" to the already-defined `→*` is purely internal formalization.

## Issue 7: L_K's endset-identity partition vs. L8's coverage-equality equivalence
Reason: This is a design choice about whether type identity is syntactic or coverage-based, which requires Nelson's design intent and Gregory's evidence on how the implementation compares type endsets in practice.
Nelson question: When the link model identifies a link's "type" with its third endset, was type-equality intended to be coverage-equivalence (so that any two endsets covering the same address set count as the same type) or strict endset-value identity (so that the same coverage realized via different spans counts as different types)?
Gregory question: When udanax-green resolves whether two links share a type — for example, when answering type-membership queries or matching against a designated retraction type — does it compare type endsets by literal value (endset-sequence equality) or by computed coverage (set-equality on address coverages)?

## Issue 8: No fully concrete worked example
Reason: The required example uses only machinery already present in ASN-0034 (tumbler structure, T10a.2 siblings), ASN-0043 (PrefixSpanCoverage, coverage), and this ASN itself. Verifying the example by hand is internal mechanical work.
