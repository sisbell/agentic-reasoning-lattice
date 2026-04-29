# Rebase Review of ASN-0036

## REVISE

### Issue 1: T4 cited with incorrect foundation label
**ASN-0036, S7 derivation**: "S7 follows from S7a …, S7b …, and T4 (field parsing, ASN-0034)."
**Problem**: The foundation label for T4 is **HierarchicalParsing**, not "field parsing." Every other foundation citation in the document uses the formal label — T5 (ContiguousSubtrees), T9 (ForwardAllocation), T10 (PartitionIndependence), TA7a (SubspaceClosure), T3 (CanonicalRepresentation) — making this the sole inconsistency.
**Required**: Replace "T4 (field parsing, ASN-0034)" with "T4 (HierarchicalParsing, ASN-0034)."

---

All other rebased citations check out:

- **S4** → T9, T10: labels correct, derivation sound, registry consistent.
- **S7** → S7a, S7b, T4, T9, T10: derivation logic correct, registry dependencies match body (aside from the T4 label above).
- **S8** → S8-fin, S8a, S2, S8-depth, T1, T5, T10, TA5(c), TA7a: every foundation property is used in the proof, registry matches, no silent dependencies.
- **D-CTG-depth** → D-CTG, S8-fin, S8-depth, T0(a), T1: proof correct, all cited properties used, T0(a) properly supplies the unbounded-values contradiction.
- **D-SEQ** → D-CTG, D-CTG-depth, D-MIN, S8-fin, S8-depth: derivation traces through correctly, transitive ASN-0034 dependencies enter via D-CTG-depth as expected.

No broken references, no orphaned prose, no silent dependencies.

VERDICT: REVISE
