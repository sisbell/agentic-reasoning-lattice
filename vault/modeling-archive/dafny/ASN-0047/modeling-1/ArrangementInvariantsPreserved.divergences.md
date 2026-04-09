# Divergences — Arrangement invariants lemma (ArrangementInvariantsPreserved)

- **Line 23**: S2 (functionality) and S8-fin (finiteness) are structural in Dafny's map model — map<Tumbler, Tumbler> is inherently functional and finite. The invariant below captures S3 (referential integrity) and S8a + S8-depth (V-position well-formedness), abstracted into a single per-V-position predicate VPosValid.
