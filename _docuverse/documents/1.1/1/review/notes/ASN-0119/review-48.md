# Review of ASN-0119

I checked every imported fact against ASN-0084's contracts, re-derived the worked examples numerically, traced each conjunct of ASN-0047's ExtendedReachableStateInvariants and ExtendedTransitionInvariants through the discharge arguments, and verified the new lemmas (RA2a, RA7a–c, RA8a/b) line by line. The note holds up.

**Verification performed:**

- **Worked pivot** (cuts ord 2,3,6 on ABCDE): R-P1/R-P2/R-EXT yield `A C D E B`; the π table (1↦1, 2↦5, 3↦2, 4↦3, 5↦4) matches the destination equations; destinations {2,3,4}∪{5}∪{1} tile {1..5} disjointly; range and extent invariance check. **Worked swap** (cuts ord 2,3,5,7 on ABCDEF): R-S1/R-S2/R-S3 yield `A E F C D B`; middle displacement `ord(c₀)+w_β − ord(c₁) = 4−3 = +1 = w_β − w_α`. The cut `c₂ = [s_C,6]` (resp. `c₃ = [s_C,7]`) one past the active run is legitimate: R-PRE(iv) constrains only positions strictly below the last cut, consistent with ASN-0084's R-BLK remark that only `c_{n−1}` may fall outside the arrangement.
- **RA2a** is a correct and complete argument: non-S positions fixed pointwise, a text position escaping the subspace would collide with its fixed image under injectivity, and finiteness (S8-fin) closes surjectivity. The S3★ derivation correctly inverts the bijection equation (`M'(d)(u) = M(d)(π⁻¹(u))`) and applies RA2a to keep `π⁻¹(v)` in the text subspace.
- **R-COMM displacement constants** all check: pivot `−w_α` (β), `+w_β` (α), `0` (exterior); swap `−(w_α+w_μ)`, `w_β−w_α`, `w_β+w_μ`, `0`. The four footprint configurations are arithmetically correct under the worked π table, and they genuinely exercise both sides of RA7c's boundary — including the case (α∪β re-abutting) showing confinement is sufficient but not necessary, which the claim correctly does not overstate.
- **RA8a/RA8b**: the composed table π₂∘π₁ (1↦1, 2↦5, 3↦2, 4↦3, 5↦4) equals the atomic π; the uniqueness step `M'(d)(u) = M(d)(π⁻¹(u))` is sound; the divergence witness `M_mid([s_C,4]) = a₂ ≠ a₄, a₅` correctly leans on the stipulated pairwise-distinct I-addresses, and the note is honest that a shared-content pre-state (S5) would not supply that distinctness.
- **Invariant coverage** is exhaustive. The set-invariance rule (RA2 freezes every key set, so key-set-only invariants — S8a, S8-fin, S8-depth, S3★-aux, D-CTG★, D-MIN★, D-SEQ★ — transfer verbatim) is applied only where valid; the three value-dependent invariants are each given positive arguments: S2 and S3★ explicitly, S8★ via R-BLK + R-CANON on the content subspace and the R-NS pointwise freeze on `s_L` (which also carries CL-OWN/CL-UNIQ, whose quantifiers range over a key-and-value-identical slice). J0/J1'★ vacuous by the correct frames; J1★ correctly recognized as *not* settled by full-range invariance (RA1) and closed instead by content-subspace range invariance via RA2a. P4★ via `Contains_C` invariance plus the cross-document closure remark; P4a's induction-extension argument is right — the new final-composite case has an empty new-entry branch, and the original step case is generic in the final composite. P3 at equality; the vocabulary-quantified obligations (M1, NoDeallocation's closed-Σ frame) are discharged rather than overlooked.
- **The K.μ~ coincidence** is handled with the necessary care: the value-degenerate instance (π ≠ id, M'(d) = M(d)) correctly bounds the claim, the "correctness property, not definition" caveat on the bijection equation prevents a real misreading when M(d) is non-injective, and all five admissibility clauses are discharged with the key-level/value-level distinction (π(v) = v vs. M'(d)(v) = M(d)(v)) kept straight. Non-triviality implies K.μ~'s two-distinct-values precondition via ASN-0047's own ValidComposite★ remark, so the coincidence claim is consistent.
- **Boundary cases**: empty text subspace, single-position document, whole-run affected interval, cut at the minimum position — all addressed, with the empty-exterior case correctly classified as a degenerate branch rather than a degenerate input. Partiality is stated cleanly (`wp = R-PRE` for everything except footprint contiguity, which RA7c covers with an explicitly sufficient-not-weakest condition).
- **Anti-bloat scan**: the single forward deferral (K.μ~ discharge) is paired with exactly one discharge site; the lifted-frame explanation (RA4/RA6) is constructive, not defensive; the value-degenerate instance appears twice but with distinct purposes (bounding the coincidence claim; warning about π's definition). No declined-finding shapes, no relocated-finding residue, no downstream-consumer inventories.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Run-structure guarantees for footprints spanning three or more regions
**Why out of scope**: RA7c is explicitly a sufficient condition; characterizing exactly when cross-region footprints retain contiguity (the re-abutting case shows the condition is not necessary) is new territory the ASN already flags as an open question.

### Topic 2: Concurrent or commuting rearrangements without a serializing authority
**Why out of scope**: The atomicity section establishes path-independence of the final state for a *given* composed bijection (RA8a); conditions for order-independence of two independently chosen rearrangements is a coordination question for a future ASN.

### Topic 3: Generalization beyond depth-2 text positions
**Why out of scope**: ASN-0084's closed-form permutations exist only at `S = 1`, depth 2 (CS3/CS4), and the ASN scopes itself accordingly; depth-m rearrangement requires extending the underlying primitive first, not revising this lift.

### Topic 4: Recoverability of prior arrangements from the Istream
**Why out of scope**: REARRANGE records only the new V→I mapping; whether and how the old order is reconstructible is a versioning/history concern, correctly listed among the open questions.

VERDICT: CONVERGED
