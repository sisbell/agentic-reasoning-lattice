# Review of ASN-0042

## REVISE

### Issue 1: Condition (v) explanatory paragraph is axiom-justification meta-prose

**ASN-0042, State Axioms (O15)**: "Condition (v) is stated as exactly the two facts the ownership theorems consume of a delegate prefix... Earlier drafts asserted this next-reachable form in both (v) and O17b — an over-determination, since no ownership theorem (O1a, O1b, O2, O3, O8, NestingByDelegation) consumes the full `next`/`hwm` form; each routes through Freshness-(v)... We therefore designate O17b as primitive for the baptism-stream form and (v) as primitive for validity and freshness."

**Problem**: This paragraph explains *why the axiom is structured as it is* and references *earlier drafts*, enumerating downstream consumers (O1a, O1b, O2, O3, O8, NestingByDelegation) as a use-site inventory. None of it advances the meaning of condition (v); it is exactly the "new prose around an axiom explains why the axiom is needed rather than what it says" accretion pattern. The reader must skip it to reach the actual conditions.

**Required**: State condition (v) as `T4(pfx(π')) ∧ pfx(π') ∉ Σ.B` and stop. Delete the over-determination/earlier-drafts/use-site commentary.

### Issue 2: Freshness-(v) "derived" block is a naming-handle restatement

**ASN-0042, State Axioms (Freshness-(v))**: "Under the weakened (v) these are immediate (they *are* condition (v)); we retain the name Freshness-(v) as the handle by which downstream proofs cite the pair. The complementary baptism-stream form... is mutually consistent with (v): B6 sufficiency would in any case give... so the two primitives never conflict."

**Problem**: A "derived" entry whose own text concedes its content "*are* condition (v)" carries no derivation — it manufactures a citation handle and then argues consistency between two primitives. The mutual-consistency paragraph is pure rationale, not a claim that any proof consumes. This is reviser drift: prose existing to justify a prior structural decision.

**Required**: Either drop the Freshness-(v) entry and have downstream proofs cite condition (v) directly, or reduce it to a one-line alias with no consistency essay.

### Issue 3: Triangular cross-deferral — (v), O17b, Freshness-(v) state the same content three times

**ASN-0042, O15 condition (v) / O17b closing / Freshness-(v)**: O17b closes with "O17b is the *sole* primitive carrier of this form; delegation condition (v) no longer restates it (see *State Axioms*, condition (v))"; condition (v)'s paragraph defers the form to O17b; Freshness-(v) again says the form "is supplied separately by O17b."

**Problem**: Three locations assert the identical split ("(v) gives validity+freshness, O17b gives the next-reachable form, they don't conflict") with mutual "see X" deferrals. This is the "multiple paragraphs defer to the same downstream location" and "two paragraphs say the same thing in different words" pattern compounding across cycles. The single fact — `pfx(π') = next(Σ.B,p,d)` is fixed by O17b — needs one statement.

**Required**: State the coupling once in O17b's body. Remove the back-references in condition (v) and Freshness-(v).

### Issue 4: O17 proof carries a non-circularity / document-ordering justification

**ASN-0042, O17 proof**: "The licensing step is RegistryReachability, not a bare import of B10: B10 is an invariant over ASN-0040-reachable registries, and RegistryReachability is precisely what certifies `Σ.B` to be one. RegistryReachability's own derivation uses only O14 and O17b, never O17, so there is no circularity."

**Problem**: The proof of O17 is one line (RegistryReachability + B10). The appended sentences justify *why the dependency ordering is acyclic* — meta-commentary on document structure, not the derivation. This is the "prose justifies document ordering / non-circular by Y argument" pattern.

**Required**: Keep the one-line derivation. Delete the non-circularity gloss.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
The note repeatedly notes Nelson permits transfer ("someone who has bought the document rights") while the system has no transfer mechanism, and lists transfer in Open Questions. Correctly deferred — no claim is asserted, so this is future territory, not an error here.

META: not applicable — the ASN defines ownership state, operations, and invariants at the required abstraction; its deficiency is accreted meta-prose around the (v)/O17b coupling, which is fixable, not drift off-track.

VERDICT: REVISE
