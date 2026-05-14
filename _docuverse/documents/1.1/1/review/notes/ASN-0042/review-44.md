# Review of ASN-0042

## REVISE

### Issue 1: Field-opening boundary case identifies Σ_pre^0 with Σ_1 contradictorily

**ASN-0042, Worked Example, "Field-opening boundary case"**: "Consider the alternative pre-fork state `Σ_pre^0 = Σ_1` (the state immediately after `π_A`'s delegation, before any document-level baptism under `[1, 0, 2]`). Then `hwm(Σ_1.B, [1, 0, 2], 2) = 0`..."

**Problem**: The example's running Σ_1 contains `a₁ = [1, 0, 2, 0, 3, 0, 1]` (placed in Σ_0.B in the "State Σ₁" paragraph, hence in Σ_1.B by T8). For `a₁ ∈ Σ_1.B`, ASN-0040's B1 (ContiguousPrefix) forces `[1, 0, 2, 0, 1]`, `[1, 0, 2, 0, 2]`, `[1, 0, 2, 0, 3] ∈ Σ_1.B`, so `hwm(Σ_1.B, [1, 0, 2], 2) ≥ 3`, not 0. The equation `Σ_pre^0 = Σ_1` is incompatible with the `hwm = 0` claim.

**Required**: Either rename to a distinct alternative state (e.g., `Σ_alt`) and drop the identification, or explicitly say "consider an alternative scenario where `a₁` was not pre-allocated at delegation time". The field-opening branch is a legitimate case to illustrate; only the identification with the running Σ_1 is wrong.

### Issue 2: Form B length-2 analysis silently elides the longer-Form-B implication for hwm

**ASN-0042, O10 proof, "Non-coverage analysis"**: The Form B argument restricts attention to length-(#pfx(π) + 2) sub-delegates and dismisses longer Form B sub-delegates "by length alone". The parenthetical at the end notes that "we make no claim about the first user-field components U^{(i)}_1 of longer Form B sub-delegates".

**Problem**: This is correct for excluding coverage of `a'` directly, but the reasoning leaves a reader uncertain whether `hwm_0` already accounts for slots claimed indirectly by longer Form B sub-delegates. The argument that `pfx(π).0.U_1 ∈ Σ.B` (from PrefixBaptismCoupling on a length-2 sub-delegate) is the load-bearing fact; for a longer sub-delegate `pfx(π).0.U_1.X`, PrefixBaptismCoupling places `pfx(π).0.U_1.X ∈ Σ.B`, not `pfx(π).0.U_1`. The proof should state that `hwm_0` need not reflect every U_1 across longer chains, but that this is harmless because the length argument already excludes longer sub-delegates from covering `a'` — making the length-2 analysis self-sufficient.

**Required**: One sentence clarifying that the length-2 case alone discharges the non-coverage obligation, and the longer-Form-B U_1 values are irrelevant to `a'`.

## OUT_OF_SCOPE

None — the ASN respects its declared scope. Authentication, ownership transfer, custodial protocols, and per-operation effects are all properly deferred.

META: The ASN is squarely in specification territory — it defines state (Π, pfx), operations (delegation, allocation authorization), and invariants (exclusivity, refinement, irrevocability), abstracted from any implementation. No drift.

VERDICT: REVISE
