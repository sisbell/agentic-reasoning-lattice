# Review of ASN-0058

## REVISE

### Issue 1: Nonexistent foundation citation in C0
**ASN-0058, C0 (OrdinalDisplacementNecessity)**: "Since `ℕ` is unbounded (NAT-carrier (NatCarrierSet) combined with NAT-addcompat's strict successor inequality `n < n + 1`)…"
**Problem**: There is no `NAT-carrier`/`NatCarrierSet` axiom in the foundation. The natural-number axioms are NAT-addcompat, NAT-closure, NAT-discrete, NAT-order, NAT-wellorder. The unboundedness of ℕ is supplied by NAT-closure (successor closure, `n + 1 ∈ ℕ`) together with NAT-addcompat (`n < n + 1`).
**Required**: Cite NAT-closure + NAT-addcompat (or T0(b) if a tumbler-length argument is intended). Remove the invented `NatCarrierSet` reference.

### Issue 2: Undefined `subspace_I` and missing foundation `ShiftPreservation`
**ASN-0058, M-sub (SubspaceConfinement), clause (b)**: "every I-address of `β` shares the I-subspace of `a`: `(A k … : subspace_I(a + k) = subspace_I(a))` … ShiftPreservation (iv) gives `subspace_I(shift(a, k)) = subspace_I(a)`."
**Problem**: `subspace_I` is never defined in this ASN, and `SubspaceProjection` in ASN-0036 defines only `subspace(v) = v₁`. `ShiftPreservation` with a clause (iv) does not appear in the ASN-0036 claim statements (ASN-0036 supplies `OrdShiftHom`, which covers only the V-side subspace). The derivation therefore rests on an undefined function and an uncited/unavailable foundation lemma.
**Required**: Define `subspace_I` (or reuse `subspace`), and either cite the actual ASN-0036 claim that establishes I-side shift-subspace invariance or supply the argument inline.

### Issue 3: S7c cited but absent from foundation
**ASN-0058, M-sub (b) and M16a**: "S7c's `#E(a) ≥ 2`", "S7c (ElementFieldDepth, ASN-0036) gives `#E(a) ≥ 2`".
**Problem**: ASN-0036's provided claim set contains S7a, S7b, S7d, S7 — no S7c (ElementFieldDepth). M16a's origin-invariance derivation is load-bearing on `#E(a) ≥ 2` (and the `#a ≥ 8` computation). If S7c is not an established foundation, the derivation has a gap. Note the *core* conclusion `origin(a+k) = origin(a)` needs only that the third separator zero lies below the action point `#a`, i.e. `#E(a) ≥ 1` (already from T4/T4a) — so the `≥ 2` appeals appear stronger than necessary.
**Required**: Correct the citation to an existing ASN-0036 claim, or recast M16a to depend only on `#E(a) ≥ 1` (T4a field non-emptiness), eliminating the S7c dependency.

### Issue 4: Forward-reference deferral prose in M6
**ASN-0058, M6 (SplitPreservation)**: "A fifth property — *origin traceability* … also holds, but its derivation rests on M16a … To keep this section's claims local to the split definition, we state and prove that property as a corollary of M16a (M16b) once M16a is in hand."
**Problem**: This justifies document ordering rather than advancing the claim — exactly the forward-reference accretion pattern flagged for this note. The reader must process a rationale for *where* the property lives instead of reading the property.
**Required**: State M6 as the four properties it proves; let M16b carry origin traceability where it is derived. Delete the deferral paragraph.

### Issue 5: Use-site inventory in M16a
**ASN-0058, M16a (OriginInvarianceUnderShift)**: "Use sites discharge it from local hypotheses (M16: `a + n₁ = a₂ ∈ dom(C)` from the M16 statement; M16b: `a + k ∈ I(β) ⊆ dom(C)` by B3 + S3, when `β` belongs to a decomposition of `M(d)`)."
**Problem**: This enumerates downstream consumers of the lemma rather than advancing its statement or proof — a flagged accretion pattern. Each use site already discharges the precondition where it is used (M16, M16b both do so explicitly).
**Required**: Remove the inventory; the precondition `a + k ∈ dom(C)` stands on its own and is discharged at each call.

### Issue 6: Downstream-dependency and non-circularity justifications in M2
**ASN-0058, M2 (DecompositionExistence)**: "The reverse inclusion uses only M-int's premises — neither B1 nor B2 is invoked — so the V-extent translation is not circular with what it is about to deliver." and "M2 inherits S8's preconditions verbatim; downstream claims that lean on M2 (notably C1a and C2) carry the same dependency."
**Problem**: The first sentence is a non-circularity justification about proof structure; the second is a downstream-consumer inventory. Both are flagged accretion patterns that the reader must skip past to follow the actual inclusion argument.
**Required**: Drop both sentences. The reverse-inclusion derivation already cites only M-int; the precondition inheritance is evident from the claim statement.

### Issue 7: "Why a precondition isn't needed" prose
**ASN-0058, M-sub (b) proof**: "No analogous sharpness note arises on the I-side: S7b's `zeros(a) = 3` and S7c's `#E(a) ≥ 2` together imply `#a ≥ 8` … so the depth pathology that would call for a separate precondition is structurally precluded."
**Problem**: This explains why a precondition is *not* required rather than what the proof establishes — defensive justification anticipating an excluded case. The `#a ≥ 8` figure is not used by any conclusion.
**Required**: Remove. Clause (b)'s proof needs only the `a ∈ dom(C)` hypothesis and the I-side shift-invariance lemma (see Issue 2).

## OUT_OF_SCOPE

(none — the ASN stays within mapping-block algebra and resolution; the Open Questions correctly defer I-space discontinuity structure, the decomposition lattice, and multi-source reordering to future work.)

VERDICT: REVISE
