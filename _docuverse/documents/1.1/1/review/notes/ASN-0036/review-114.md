# Review of ASN-0036

## REVISE

### Issue 1: Verbatim T10a.4 gloss repeated across five contracts
**ASN-0036, S7a/S7b/S7c/S7/S7d Depends clauses**: each repeats "T10a.4 ... supplies the *surrounding* T4-validity (no adjacent zeros, positive endpoint components `a₁ ≠ 0 ∧ a_{#a} ≠ 0`)" near-verbatim.
**Problem**: The same sentence, including the same parenthetical enumeration, appears in S7a, S7b, S7c, the S7 proof/preconditions, and S7d. This is the "two paragraphs say the same thing in different words" pattern compounded five-fold — the reader re-parses identical content at each contract.
**Required**: State the T10a.4 → T4-validity dependency once (e.g., at S7b where the element-level restriction is first pinned) and have the later contracts cite S7b rather than re-glossing T10a.4.

### Issue 2: S7c Consequences (b) and (c) are forward-reference / use-site inventory
**ASN-0036, S7c Formal Contract**: Consequence (b) "shift action-point separation" depends on "ShiftPreservation (below)"; Consequence (c) "TA7a operand membership" sets up `o ∈ S` "so that `⊕` and `⊖` are directly applicable."
**Problem**: Neither advances the meaning of the S7c axiom (`#E(a) ≥ 2`). (b) is wholly a property of `shift`, proved later in ShiftPreservation (iv) — parking it in S7c via a downward pointer is forward-reference accretion. (c) is a downstream-applicability note ("so that TA7a applies") rather than a consequence of the axiom itself. Only Consequence (a), subspace-ordinal separation, is a genuine consequence of `#E(a) ≥ 2`.
**Required**: Keep Consequence (a). Move (b) into ShiftPreservation (where it is actually proved) and (c) to the TA7a use-site, removing the forward pointer from S7c's contract.

### Issue 3: Definition contracts carry forward references and downstream-parallel notes
**ASN-0036, `subspace` and `subspace_I` Formal Contracts**: subspace's Depends says "subspace preservation under shift is established by OrdShiftHom (b) below"; both contracts carry "Parallels `subspace_I(a) = E(a)₁` for V-positions" / "Parallels `subspace(v) = v₁`."
**Problem**: A definition's contract should advance the definition's meaning. The "established below" pointer and the reciprocal "parallels X" notes are meta-prose about document structure and downstream consumers, not content of the projection `v ↦ v₁`.
**Required**: Drop the forward pointer and the reciprocal-parallel remarks from both contracts; the projections stand on their own.

### Issue 4: S2 postcondition restates its own axiom
**ASN-0036, S2**: Axiom: "`Σ.M(d)` is a (partial) function — `(A d,v,a₁,a₂ : ... : a₁ = a₂)`." Postconditions: "For each `v ∈ dom(Σ.M(d))`, the image `Σ.M(d)(v)` is uniquely determined."
**Problem**: The postcondition is a verbatim re-expression of the functionality axiom — single-valuedness stated twice in one block with no added content.
**Required**: Delete the redundant postcondition, or replace it with a genuine consequence (e.g., well-definedness of `ran(M(d))` as the image).

### Issue 5: S8-fin justified by operations-layer appeal, not stated at strand level
**ASN-0036, S8-fin**: labeled "Axiom (design requirement)," then "S8-fin follows from the operational reality: each V-position enters `dom(M(d))` through a specific operation ... and the system has performed only finitely many operations."
**Problem**: The prose explains *why the axiom is plausible* by appealing to operations-layer facts (operation counts) that the strand model does not have access to — it does not derive S8-fin within this ASN. This is "new prose explaining why the axiom is needed rather than what it says," with the added defect that the justification reaches outside the strand abstraction.
**Required**: Either keep S8-fin as a bare design requirement (it is one) and drop the operational-derivation prose, or state it as a derived property and supply the strand-level derivation — not both.

### Issue 6: Self-labeled non-dependency essay under S8-depth
**ASN-0036, S8-depth section**: the parenthetical "(Why non-trivial runs arise in practice is a separate question. Allocator discipline — T10a ... But this operational fact is motivation for the definition of correspondence runs, not a dependency of the decomposition proof.)"
**Problem**: The paragraph explicitly declares itself motivation that is "not a dependency of the decomposition proof" — content the precise reader must skip to follow the argument. This is essay content in a structural slot.
**Required**: Remove it, or compress to a one-line remark; the same point recurs more usefully in the `#runs(d)` discussion at the section's end.

## OUT_OF_SCOPE

### Topic 1: Link-subspace contiguity (S = 2)
**Why out of scope**: D-CTG/D-MIN/D-CTG-depth/D-SEQ are correctly bound to the text subspace `S = 1`, with link-subspace sparse/tombstone semantics explicitly deferred to a future ASN. This deferral is handled properly and should not be flagged as missing coverage.

### Topic 2: Operation preservation of D-CTG/D-MIN and subspace alignment
**Why out of scope**: Whether DELETE/INSERT/COPY/REARRANGE preserve the contiguity invariants, and the `subspace(v) = subspace_I(M(d)(v))` alignment obligation, are correctly posed as operations-layer Open Questions rather than asserted here.

VERDICT: REVISE
