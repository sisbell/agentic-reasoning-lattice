# Review of ASN-0074

## REVISE

### Issue 1: Non-foundation cross-reference to ASN-0047
**ASN-0074, preamble**: "We work with system state Σ = (C, E, M, R) per ASN-0047"
**Problem**: ASN-0047 is not a foundation ASN. The entity set `E_doc` and the state component `R` are not defined in any foundation. The ASN uses `E_doc` in the ContentReference definition but never defines it locally.
**Required**: Either add ASN-0047 to the foundation list with extracted formal statements, or restate the needed definitions (at minimum, `E_doc`). Component `R` appears unused — drop it from the state tuple. `C` and `M` are already grounded in ASN-0036.

### Issue 2: V-ordering of resolution output incorrectly attributed to B1
**ASN-0074, Resolution**: "This is a consequence of the block decomposition being V-ordered (B1, ASN-0058)."
**Problem**: B1 is a coverage-and-uniqueness condition: every V-position belongs to exactly one block. It says nothing about ordering. The V-ordering of the output follows from the *definition of resolve*, which specifies "⟨β₁, ..., βₖ⟩ ordered by V-start." B2 (Disjointness) is what makes this ordering well-defined (non-overlapping V-extents can be totally ordered). The cited property does not establish the claimed consequence.
**Required**: Replace the citation with the correct derivation: resolve orders blocks by V-start (by definition), which is well-defined because V-extents are disjoint (B2).

### Issue 3: Implementation reference in abstract specification
**ASN-0074, Resolution**: "Gregory's implementation confirms: `incontextlistnd` (the POOM traversal function) performs insertion-sort by V-address during tree traversal, regardless of the internal sibling order that rebalancing may produce."
**Problem**: An abstract specification derives properties from definitions and invariants, not from implementation behavior. The V-ordering is a definitional choice in resolve — it needs no implementation confirmation.
**Required**: Remove the implementation paragraph. If a design note is desired, put it outside the formal body.

### Issue 4: C1 derivation omits the B3 link
**ASN-0074, C1**: "The resolution extracts exactly these I-addresses from the source arrangement. ∎"
**Problem**: The claim is `aⱼ + i ∈ dom(C)` for each run `(aⱼ, nⱼ)` and `0 ≤ i < nⱼ`. The unstated step: B3 (Consistency) gives `M(d_s)(vⱼ + i) = aⱼ + i` for each `i`, so `aⱼ + i ∈ ran(M(d_s))`. Then S3 gives `M(d_s)(vⱼ + i) ∈ dom(C)`. The derivation skips the B3 step entirely — "extracts exactly these I-addresses" is the claim, not the proof.
**Required**: Show the chain: B3 identifies each `aⱼ + i` as `M(d_s)(vⱼ + i)`, S3 places it in `dom(C)`.

### Issue 5: C1a proof sketch miscites S2 for merge consistency
**ASN-0074, C1a**: "Each merge step requires only B3 (consistency with f's values) — guaranteed by S2."
**Problem**: S2 (functionality) guarantees that f is a function, which is needed for the *initial* singleton-block decomposition. The *merge step* preserving B3 is a separate inductive argument: if β₁ and β₂ each satisfy B3, and the merge condition (M7) holds, then β₁ ⊞ β₂ satisfies B3 by case split on `k < n₁` vs `k ≥ n₁`, using M-aux (ordinal increment associativity). The citation "guaranteed by S2" points to the wrong property for the wrong step.
**Required**: State that the initial decomposition is consistent by S2, and that merge preserves B3 by the standard argument (case split + M-aux, as in ASN-0058).

### Issue 6: ContentReference definition ill-formed for empty subspace
**ASN-0074, ContentReference**: "#ℓ = #u = m, where m is the common V-position depth in subspace u₁ of d_s (S8-depth, ASN-0036)"
**Problem**: S8-depth says all V-positions in a subspace share the same depth — vacuously true when the subspace is empty, but it does not *define* a common depth. When `V_{u₁}(d_s) = ∅`, `m` is undefined, and the definition cannot be evaluated. The well-formedness condition would be unsatisfiable anyway (the span denotes positions not in `dom(M(d_s))`), but the definition is syntactically ill-formed before reaching that check.
**Required**: Add a precondition `V_{u₁}(d_s) ≠ ∅`, or define m as `#u` and require `m` equals the common depth of `V_{u₁}(d_s)` when non-empty. Either way, the empty-subspace case must be addressed at the definitional level.

### Issue 7: Implicit ordinal displacement requirement not derived
**ASN-0074, ContentReference**: well-formedness condition `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d_s))`
**Problem**: For any depth m ≥ 2, if the displacement ℓ has action point k < m (non-ordinal), the span range includes depth-m tumblers with intermediate components ≠ 1 — positions that cannot appear in `dom(M(d_s))` by D-SEQ. At depth m ≥ 3 the range is actually *infinite* (by T0(a), unboundedly many last-component values), immediately contradicting S8-fin. The well-formedness condition is therefore unsatisfiable for any non-ordinal displacement. This is a significant structural consequence: well-formed content references require ordinal displacements `ℓ = δ(n, m)`.
**Required**: Derive this as a lemma or corollary. State that well-formed content references necessarily have ordinal displacements, and show the argument (D-SEQ forces intermediate components to 1; non-ordinal displacements produce ranges violating this).

### Issue 8: No concrete example
**ASN-0074, entire document**
**Problem**: The review standards require verification of key postconditions against at least one specific scenario. The ASN defines ContentReference, resolve, C1a, and C1 without working through any concrete case.
**Required**: Add a worked example. For instance: a document with canonical decomposition ⟨(v₁, a₁, 3), (v₂, a₂, 2)⟩, a content reference spanning positions 2–4, showing the restriction, the re-decomposition, the resolved I-address sequence, and verification of C1 against specific addresses.

## OUT_OF_SCOPE

### Topic 1: Extension of C1 to content reference sequences
**Why out of scope**: C1 is stated for a single content reference. The extension to sequences (each reference resolves independently, C1 applies to each) is trivial but not stated. This is a natural next step, not an error in what's here.

### Topic 2: Well-formedness checking simplification via D-CTG
**Why out of scope**: D-CTG and D-SEQ imply that the well-formedness containment check reduces to a boundary check (span start ≥ min of V-positions, reach ≤ successor of max). Deriving this simplification is useful for implementation but is not required by the definitions in this ASN.

VERDICT: REVISE
