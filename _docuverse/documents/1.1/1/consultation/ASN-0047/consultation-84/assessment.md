# Channel Assignment — ASN-0047 review-84

**Date:** 2026-05-17 17:27

```
## Issue 1: K.μ~ specified in two places with different content
Reason: Editorial consolidation of two definitional treatments of the same construct into one. Derivable from existing ASN content.
```

```
## Issue 2: "Note on..." subsections are pure meta-prose
Reason: Editorial cleanup — choose one notation per concept and drop the redundant notes. No external evidence needed.
```

```
## Issue 3: "Frame consistency check" in K.μ~ is anti-bloat
Reason: Drop a paragraph that verifies what is true by definition. Internal edit.
```

```
## Issue 4: "Note on K.μ⁺ and P4★" is anti-bloat
Reason: Drop a standalone note duplicating the ExtendedReachableStateInvariants proof. Internal edit.
```

```
## Issue 5: Withdrawal-mechanism gap referenced in 5+ sites
Reason: Consolidation of cross-references into the single discussion at D-CTG★. No new design or implementation evidence needed.
```

```
## Issue 6: Version-management deferral referenced 4+ times
Reason: Consolidate forward pointers to the K.δ definition site. Internal edit.
```

```
## Issue 7: "Per-subspace S8 substitution lemma" + use-site reuse note
Reason: Editorial — inline or drop the lemma framing. Content is already correct.
```

```
## Issue 8: Dispatch tables are use-site inventories
Reason: Editorial restructuring of the existing per-case precondition list. Path classification is a design fact already established in the ASN.
```

```
## Issue 9: ValidComposite★ "two clauses serve different roles" is defensive
Reason: Drop defensive prose; the definition stands on its own. Internal edit.
```

```
## Issue 10: D-SEQ★ derivation Step 1 over-elaborated
Reason: Editorial condensation of an existing proof. No new reasoning needed.
```

```
## Issue 11: Cross-document disjointness chain proof over-elaborated
Reason: Editorial condensation, citing T10a.{2,5} → T10 at the appropriate level. Foundation lemmas already supply the structural content.
```

```
## Issue 12: K.μ⁻ undefined at empty pre-state is implicit
Reason: Mechanical fix — add explicit precondition `dom(M(d)) ≠ ∅`. Derivable from the existing effect clause.
```

```
## Issue 13: Empty endset (F, G) semantics not specified
Reason: Whether (∅, ∅, Θ) is admissible touches design intent (does Nelson's link model admit type-only markers?) and implementation evidence (does udanax-green produce or accept empty F/G endsets?).
Nelson question: Does the Xanadu link design admit links with empty from-endset and to-endset (a "type-only marker"), or must F and G always be non-empty alongside the mandatory Θ?
Gregory question: Does `docreatelink` (or any other link-creation path in udanax-green) ever produce a link with empty from-endset or empty to-endset, and what does the implementation do if asked to?
```

```
## Issue 14: L1c axiom content fuzzy
Reason: Foundation cleanup — L1c is from ASN-0043 and its relationship to T10a + SubAllocatorAxiom can be determined from existing axiom statements. Internal.
```

```
## Issue 15: Worked examples enumerate invariants per step exhaustively
Reason: Editorial reduction — cite the ExtendedReachableStateInvariants theorem for frame-preserved invariants. No new content needed.
```

```
## Issue 16: SubAllocatorAxiom's first-emission content not pinned to a tumbler value
Reason: Whether the first emission is deterministically `[d.0.s_C.1]` and `[d.0.s_L.1]` (versus any address meeting the four namespace conditions) requires the designed allocation discipline (Nelson) and the implementation's actual first-emission behavior (Gregory).
Nelson question: When a document's content (or link) sub-allocator is first activated, is the first allocated address required by design to be the specific tumbler `[d.0.s_C.1]` (resp. `[d.0.s_L.1]`), or is the first emission deliberately non-deterministic within the subspace prefix?
Gregory question: What is the first content address and first link address that udanax-green produces under a freshly created document — does the implementation deterministically emit `[d.0.1.1]` and `[d.0.2.1]`, or can the first emission vary?
```
