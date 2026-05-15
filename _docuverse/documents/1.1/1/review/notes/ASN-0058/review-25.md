# Review of ASN-0058

## REVISE

### Issue 1: M7 necessity proof opens with OrdShiftHom but does not establish #v₁ ≥ 2
**ASN-0058, M7 (MergeCondition)**: "By OrdShiftHom (ASN-0036), `subspace(v₁ + n₁) = subspace(v₁)`."
**Problem**: OrdShiftHom (ASN-0036) requires #v ≥ 2. The proof later remarks "With m ≥ 2 (V-positions in M(d) lie in the element subspace)..." but never explicitly chains β₁ ∈ B → v₁ ∈ dom(M(d)) → S8a → #v₁ ≥ 2. The dependency is load-bearing for the entire necessity argument and the parenthetical "V-positions in M(d) lie in the element subspace" misstates S8a (which just bounds depth, not subspace).
**Required**: Open the proof with an explicit citation: "Since β₁ ∈ B is in a decomposition of M(d), v₁ ∈ dom(M(d)); S8a (ASN-0036) gives #v₁ ≥ 2." Then OrdShiftHom applies cleanly. Replace the misleading "element subspace" parenthetical.

### Issue 2: M12 partition argument relies on the same implicit S8a chain
**ASN-0058, M12 (CanonicalUniqueness)**: "By OrdShiftHom (ASN-0036), ordinal shift preserves subspace, so v shares its subspace with v₁ and with v₂..."
**Problem**: Same gap as Issue 1 — OrdShiftHom requires #v ≥ 2 for v₁, v₂, v ∈ dom(f). The argument also instantiates OrdShiftHom at offsets that may be 0 (when v = v₁), which OrdShiftHom does not directly address (it requires n ≥ 1); the OrdinalShiftBase convention handles k=0, but the proof should say so.
**Required**: At the start of the partition argument and again at the (⟹) direction's j ≥ 1 sub-case, explicitly establish that all relevant V-positions have #v ≥ 2 via S8a (or via C1a's common-depth condition in the restriction setting). Note where OrdinalShiftBase (k=0) versus OrdShiftHom (k ≥ 1) applies.

### Issue 3: M6(d) forward-references M16 instead of the cleaner M16a
**ASN-0058, M6 (SplitPreservation), clause (d)**: "S7b/S7c (ASN-0036) place the document prefix N.0.U.0.D strictly below the action point #a — the argument is carried out in full in M16 below..."
**Problem**: M16a (OriginInvarianceUnderShift) is the named lemma that captures exactly this fact: `origin(a + k) = origin(a)` for a ∈ dom(C). M6(d) is the natural first consumer, yet it forward-references M16 (which itself derives M16a as a sub-step). This inverts the natural dependency order: M16a should be proved first, then both M6(d) and M16 cite it.
**Required**: Reorder so M16a is established before M6, with M16a's proof self-contained. Then M6(d) and M16 each cite M16a in one line.

### Issue 4: C0a's handling of the partial-projection case is scattered and confusing
**ASN-0058, C0a (PrefixConfinement)**: "The membership predicate `tⱼ ≠ uⱼ` requires `tⱼ` to be defined — i.e., `j ≤ #t`; indices `j > #t` are not in J. The case `#t < m` (where some indices `j < m` would lack `tⱼ`) is disposed of separately at the end of the argument; we proceed under the implicit assumption that the indices considered here have `tⱼ` defined."
**Problem**: The "implicit assumption" disclaimer is awkward, and the "disposed of separately at the end" forward reference inside the same proof requires the reader to track three argument threads simultaneously. The structure conflates "J is well-defined" with "J is non-empty" with the #t < m edge case.
**Required**: Split into two explicit cases at the top of the proof: (a) #t ≥ m — J is well-defined on the full range 1..m-1, run the divergence argument; (b) #t < m — show t is a proper prefix of u, contradicting u ≤ t directly via T1(ii), without ever defining J.

### Issue 5: B1's `v₁ ≥ 1` guard is redundant under standing preconditions
**ASN-0058, Definition (Block Decomposition)**: "(B1) *Coverage.* `(A v ∈ dom(M(d)) : v₁ ≥ 1 : (E! j : 1 ≤ j ≤ m : v ∈ V(βⱼ)))`"
**Problem**: The standing preconditions for M2 include S8a, which makes v₁ ≥ 1 hold automatically for every v ∈ dom(M(d)). The accompanying note "The `v₁ ≥ 1` guard in B1 is the universal S8a precondition" acknowledges this. Carrying a redundant guard in a foundational definition invites readers to look for non-trivial restriction where there is none.
**Required**: Remove the guard from B1, or replace it with a brief acknowledgment in the surrounding prose that S8a's positivity is in force throughout.

### Issue 6: M11 termination phrasing "bounded below by 1 for non-empty M(d)" is misleading
**ASN-0058, M11 (CanonicalExistence)**: "The process terminates because `|B|` is finite and bounded below by 1 for non-empty `M(d)`."
**Problem**: |B| can terminate at any value ≥ 1, depending on the canonical size — the lower bound of 1 is not what makes the process terminate. Termination is by well-foundedness of ℕ on |B|, with each merge step strictly decreasing the count.
**Required**: Replace with "Termination is by well-foundedness of ℕ: |B| is a non-negative integer that strictly decreases on each merge step."

### Issue 7: M16's transitive T10a conformance for element-level allocators relies on an implicit system assumption
**ASN-0058, M16 (CrossOriginMergeImpossibility)**: "T10a is recursive: its allocator-tree clause (ASN-0034) generates element-level allocators as descendants of document-level allocators via further `inc(·, k')` operations, and every such descendant is itself a conforming allocator."
**Problem**: This step asserts that the entire allocator tree below document allocators conforms to T10a, but neither S7d (which speaks only to document tumblers) nor T10a's own statement directly establishes this for I-addresses produced inside a document. The argument relies on system-wide T10a conformance that is assumed but not stated as a precondition of the lemma.
**Required**: Either (a) make the system-wide T10a conformance explicit as a precondition of M16/M16a, or (b) cite the specific ASN-0036 axiom that ensures element-level allocations occur via T10a-conforming sub-allocators of document allocators. The current "T10a is recursive" sentence is a structural claim that needs a precise reference.

### Issue 8: Notation `t + k` overloads tumbler-shift with the integer `c + j` inside M-aux
**ASN-0058, OrdinalShiftBase / M-aux**: "(v + c) + j = v + (c + j)"
**Problem**: The convention defines `t + k` as `shift(t, k)` (a tumbler operation), but M-aux's right-hand side `v + (c + j)` requires the reader to first compute `c + j` as integer addition and then apply shift. This is internally consistent but the symbol `+` carries two distinct interpretations (one when the left operand is a tumbler, another when both operands are naturals). For a foundational convention used throughout the ASN, this overload deserves a note.
**Required**: Add one sentence to the OrdinalShiftBase convention: "When both operands are naturals, `+` denotes natural-number addition; when the left operand is a tumbler and the right a natural, `+` denotes ordinal shift." Or alternatively use a distinct symbol (say `t ⊕_o k`) for the shift operation.

### Issue 9: C1a's "extension of M11/M12" reuses M7f, which is stated for M(d) rather than arbitrary partial functions
**ASN-0058, C1a (RestrictionDecomposition)**: "Each merge step preserves all three conditions by M7f (MergeFrame)."
**Problem**: M7f is stated and proved for B = decomposition of M(d). Applying it to a decomposition of f = M(d_s)|⟦σ⟧ requires the implicit observation that M7f's proof depends only on the partial-function structure (B3) and V-extent partition (B1, B2), not on f being a full arrangement. This generalization is natural but should be flagged.
**Required**: Add one sentence to C1a explicitly noting that M7f's proof carries over verbatim to any partial function f satisfying functionality, finite domain, and common depth, since it consults only the abstract decomposition properties B1–B3.

## OUT_OF_SCOPE

(none — the Open Questions section already correctly defers downstream topics like discontinuity structure, lattice of decompositions, and resolution-order semantics.)

VERDICT: REVISE
