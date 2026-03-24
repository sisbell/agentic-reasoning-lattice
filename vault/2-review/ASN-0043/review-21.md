# Rebase Review of ASN-0043

## REVISE

(none)

**Analysis.** The rebase introduced GlobalUniqueness as a bridge property extending S4 (OriginBasedIdentity, ASN-0036) to all allocation events via the same tumbler-algebra derivation (T9, T10, T10a + TA5(d) + T3, ASN-0034). Downstream references were updated accordingly. Checked:

1. **Citations correct.** S4 label and ASN attribution match foundation. The three-case structure (same-allocator via T9, non-nesting cross-allocator via T10, nesting-prefix cross-allocator via T10a + TA5(d) + T3) matches S4's derivation in ASN-0036 exactly. The generalization argument — that these depend only on tumbler algebra, not content-store specifics — is sound: all cited properties are ASN-0034 universals.

2. **Downstream references.** L11a correctly cites GlobalUniqueness. The S7 analog in the home section correctly cites T9, T10, T10a + TA5(d) + T3 with L1a replacing S7a and L1 replacing S7b; T4 is established in the preceding clause. L9 and L11b proofs cite L11a/GlobalUniqueness consistently. The worked example verifies GlobalUniqueness non-vacuously across two state transitions.

3. **Registry.** GlobalUniqueness is listed as LEMMA/introduced with correct dependency summary. All other rebased-adjacent entries (L11a, L11b) have consistent labels and status.

4. **Context.** Prose flows naturally around the bridge property. GlobalUniqueness is introduced where the need first arises (Home and Ownership), consumed where uniqueness is needed (L11a, L9 proof, L11b proof).

VERDICT: CONVERGED
