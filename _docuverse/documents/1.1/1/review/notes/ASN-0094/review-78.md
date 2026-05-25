# Review of ASN-0094

## REVISE

### Issue 1: FDD preservation Case A enumeration is incomplete

**ASN-0094, FunctionalDependencyDiscipline preservation theorem, Case A**: "This case covers all K.σ-steps, K.α-steps, K.λ-steps emitting a tuple of any type `K'` with `K' ≁ K` and `K' ≁ R` (so `L_K` and `nullified` are both untouched at K), and all arrangement-modifying steps in `↦ \ →`"

**Problem**: The enumeration omits the sub-case `K.λ at K' ≁ K with K' ~ R when the new R-tuple's G-coverage does not nullify any τ ∈ A_K^Σ`. In this sub-case `A_K^{Σ'} = A_K^Σ` (the nullified set extends but the extension does not intersect `addr(·)` for any τ ∈ A_K^Σ), so it should fall under Case A. The companion Sh4 preservation handles this explicitly as item 3 of its Case A enumeration. FDD's Case C is restricted to Emit_R-steps "nullifying one or more K-tuple addresses", and Case A's enumeration excludes `K' ~ R` entirely, leaving this sub-case unattributed. The conclusion still holds by case-equation, but the enumeration is incomplete relative to Sh4's.

**Required**: Add the missing sub-case to FDD's Case A enumeration, matching the structure of Sh4 item 3 ("K.λ-steps at type K' with K' ≁ K and K' ~ R when no τ ∈ A_K^Σ lies in the new R-tuple's G-coverage"). Alternatively, drop the explicit enumeration and rely solely on the case-equation `A_K^{Σ'} = A_K^Σ` to define Case A.

### Issue 2: d_retr unspecified in worked example edge case

**ASN-0094, Worked Example: K = comment, Edge case: retraction of τ_1**: "From Σ_5, issue `Nullify(Σ_5, d_retr, a_1)` producing Σ_6."

**Problem**: `d_retr` is introduced without specification. The walkthrough has previously named `home_K` (for comment emissions) and `home_R` (for K_res emissions) but never `d_retr`. Per the Nullify precondition (P0 in ASN-0086), d_retr must be in `dom(Σ_5.M)`; the walkthrough doesn't say which document plays this role.

**Required**: Either pre-allocate d_retr in the walkthrough's Σ_0 setup (alongside `home_K`, `home_R`), reuse one of the existing home documents explicitly, or note that any `d_retr ∈ dom(Σ_5.M)` suffices and the active-subset machinery is independent of this choice.

## OUT_OF_SCOPE

### Topic 1: Multi-process consistency for Sh4/FDD/SHCD contracts
**Why out of scope**: Explicitly flagged in Open Questions as a scope boundary. The single-process atomicity assumption is a deliberate framework commitment, not an unresolved internal question.

### Topic 2: Non-empty `L_K^{Σ_init}` retrofit
**Why out of scope**: Acknowledged in Open Questions. Preservation theorems presuppose empty initial link stores; retrofitting onto non-empty initial states is a future extension requiring per-K baseline checks.

### Topic 3: Ghost-targeting slot semantics
**Why out of scope**: Acknowledged in Open Questions. The framework restricts slot addresses to allocated targets; admitting ghost-targeting at the slot level is flagged as an open design question.

### Topic 4: Composite shapes (F or G constrained by another relation)
**Why out of scope**: Acknowledged in Open Questions as a refinement candidate.

### Topic 5: Container-level link targeting (A_M symbol)
**Why out of scope**: Acknowledged in Open Questions. Catalog extension to dom(Σ.M)-targeting would re-enable metalink-style targeting.

### Topic 6: Standalone walkthroughs for Resolution, Retraction, Provenance, Tuple-Classifier, SHCD opt-in
**Why out of scope**: The ASN explicitly acknowledges non-uniform walkthrough depth. The framework's preservation theorems quantify uniformly over `K ∈ T_cat`, so the load-bearing claims hold at every registered shape. Resolution is exercised as `K_res` in the Comment walkthrough; Retraction as `R` in that walkthrough's edge case; Tuple-Classifier is structurally identical to Classifier modulo a `t_G` substitution; Provenance's `to₁⁻` partiality machinery is exhibited at other shapes' partial-accessor tables.

### Topic 7: Idempotency as a derivable vs. independent shape component
**Why out of scope**: Acknowledged in Open Questions as a refinement candidate. The catalog empirically exhibits both `idem = ⊤` and `idem = ⊥` at identical `(c_F, c_G, t_F, t_G)`, suggesting the axis is independent.

### Topic 8: Promoting per-K disciplines (FDD, SHCD) to a sixth shape component
**Why out of scope**: Acknowledged in Open Questions as a design choice. The current opt-in extension structure is intentional.

VERDICT: REVISE
