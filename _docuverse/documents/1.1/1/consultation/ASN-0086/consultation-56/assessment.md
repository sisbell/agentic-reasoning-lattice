# Channel Assignment — ASN-0086 review-56

**Date:** 2026-05-18 07:10

```
## Issue 1: R0 Step 2 Case B asserts contiguity of prior siblings that the construction does not require
Reason: The fix is internal — replacing the contiguity argument with the simpler T10a.7 + L-fin justification is derivable from cited lemmas already in scope; no external evidence or intent input is needed.
```

```
## Issue 2: R6b is a tautological restatement of the definition, mislabeled as a lemma
Reason: The fix is internal — either demoting to Remark or expanding via a structural contrast with a recursive A_R-quantified alternative is purely a definitional/exposition choice grounded in the existing Definition of nullified.
```

```
## Issue 3: R7a's replay sequence does not explicitly discharge L0/L1/L1b/L1c at each replay step
Reason: The fix is internal — state-invariance of address-structural properties (L0/L1/L1b are projections of the address; L1c is structural over tumbler-space chains) is derivable from ASN-0034/ASN-0043 content already cited.
```

```
## Issue 4: Frame condition (iii) names the class "Emit_K" but Emit_K is later defined as a strict subset
Reason: The fix is internal — pure notation/terminology correction; striking the parenthetical and replacing with a descriptive label is editorial.
```

```
## Issue 5: The "witness-only reading" of L1c is asserted but not formally grounded
Reason: The witness-only reading is a substrate-semantic commitment about L1c that is asserted repeatedly without anchor; Nelson clarifies whether this matches design intent for LinkAllocatorConformance, and Gregory clarifies whether udanax-green's allocator behavior aligns with the witness-only interpretation.
Nelson question: Was L1c (LinkAllocatorConformance) intended as an existential conformance witness — that some T10a-conforming chain to the address exists in abstract tumbler space — or as a requirement that the chain's intermediate spawns be operationally executed (with their addresses thereby allocated)?
Gregory question: When udanax-green emits a link via `findisatoinsertmolecule`, does the implementation require intermediate addresses along the T10a producer chain (from document seed to the emitted link's address) to be physically allocated/resident, or does it only verify reachability in the abstract allocator hierarchy without materializing the chain?
```

```
## Issue 6: Arrangement-modification frame's L12a citation misrepresents what L12a establishes
Reason: The fix is internal — L12a's monotonicity content is in ASN-0043 already; the corrected three-part citation (L12 forbids modification, L12a forbids removal, definitional partition of ↦ forbids extension on arrangement steps) restates known facts.
```

```
## Issue 7: The proof of R0a's Stage 2 inductive step does not address the discipline's enforcement at class-(iii) steps
Reason: The fix is internal — the counterexample (`a' = a₁.1` for existing `a₁`) already appears in the Implementation Notes paragraph defining sibling-frontier discipline; inlining it at Stage 2 just relocates existing content.
```

```
## Issue 8: The Worked Sketch verifies R-claims by inspection without systematic coverage
Reason: The fix is internal — adding explicit R-claim citations to existing computation steps is purely an exposition enhancement; all relevant R-claims are already established and applied tacitly in the sketch.
```

```
## Issue 9: R5's generalization claim has no proof
Reason: The fix is internal — enumerating which R0 Step 4 invariants are endset-content-dependent (only L3) versus address-and-state-dependent (the rest) requires only inspection of R0's existing proof content.
```
