# Review of ASN-0084

## REVISE

### Issue 1: V-extent of a block used without formal definition
**ASN-0084, Block Decomposition Transformation**: "Coverage: every v ∈ dom(M(d)) belongs to exactly one block's V-extent" (B1), "the V-extents of distinct blocks are pairwise disjoint" (B2), "their V-extents partition b's V-extent" (Split)
**Problem**: The term "V-extent" appears in the formal properties B1, B2, and the Split definition but is never defined. The meaning is recoverable from B3 — for block b = (v, a, n), the V-extent must be {v + k : 0 ≤ k < n} — but in a specification where B1 and B2 are load-bearing properties cited by R-PIV, R-SWP, and R-BLK, every term in the formal statement should have an explicit definition.
**Required**: Add a one-line definition before B1: "The *V-extent* of a block (v, a, n) is V(v, a, n) = {v + k : 0 ≤ k < n}." Then B1 and B2 reference the defined term.

### Issue 2: `vpos` defined but never used
**ASN-0084, State and Vocabulary**: "The reconstruction vpos(S, o) = [S, o₁, ..., oₖ] is its inverse."
**Problem**: `vpos` is introduced as the inverse of `ord` but never appears again in the ASN. Dead definitions add notational surface area without contributing to any claim or proof.
**Required**: Either remove the `vpos` definition or cite it somewhere in the body.

## OUT_OF_SCOPE

### Topic 1: Depth-2 to arbitrary-depth generalization
**Why out of scope**: The ASN restricts to depth-2 V-positions and correctly notes that D-CTG-depth reduces the general case to contiguity of the last component alone. Formally establishing that every property in this ASN lifts verbatim to depth m ≥ 3 (with ordinal shifts replacing integer arithmetic) is a genuine extension, not a defect in the current ASN.

### Topic 2: Formal connection between Block Split/Merge and ASN-0053 S4/S3
**Why out of scope**: Block Split and ASN-0053's S4 (SplitPartition) are structurally analogous — both partition a contiguous range at an interior point — but operate on different objects (blocks carry I-address mappings; spans do not). A future ASN could formally show that Block Split induces S4 on the underlying V-extent span, and Block Merge induces S3. This is new territory, not a gap in ASN-0084.

## Commentary

The proofs are explicit and case-by-case throughout — no "by similar reasoning" or checkmark-as-proof. Both worked examples verify every postcondition clause against concrete values, and the 4-cut example exercises the merge path to completion. The invariant preservation argument correctly identifies that all ASN-0036 invariants are maintained: domain-dependent invariants (D-CTG, D-MIN, S8-fin, S8a, S8-depth) hold because dom(M'(d)) = dom(M(d)); content-store invariants (S0, S1, S7a–c) hold because C' = C; functionality (S2) is established by R-PIV/R-SWP; referential integrity (S3) is established by R-RI via ran(M'(d)) = ran(M(d)). The R-BLK commutativity proof — π(vⱼ + k) = π(vⱼ) + k — is verified in all six region cases (exterior, 3-cut α/β, 4-cut α/μ/β) using only TS3 associativity, which is the right algebraic tool.

VERDICT: REVISE
