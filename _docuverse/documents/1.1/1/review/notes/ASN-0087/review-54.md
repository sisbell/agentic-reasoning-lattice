# Review of ASN-0087

## REVISE

### Issue 1: Preconditions section presents derived emission guarantees as K.λ preconditions

**ASN-0087, Preconditions**: "For K.λ at `Σ`: `d ∈ dom(M)`; `ℓ ∉ dom(C) ∪ dom(L)`; `zeros(ℓ) = 3 ∧ E(ℓ)₁ = s_L ∧ #E(ℓ) ≥ 2 ∧ origin(ℓ) = d`; `ℓ is produced by A_L(d)`; `N ≥ 3 ∧ … e₃ ≠ ∅`"

**Problem**: In ASN-0093, K.λ's binding precondition is `d ∈ dom(M)`, `ℓ produced by A_L(d)` (first/subsequent emission rule), and the well-formed link value. The freshness `ℓ ∉ dom(C) ∪ dom(L)` and the structural shape (`zeros(ℓ)=3`, `E(ℓ)₁=s_L`, `#E(ℓ)≥2`, `origin(ℓ)=d`) are not preconditions there — they are *lemmas* (FirstEmission, FirstEmissionFreshness, SubsequentEmissionFreshness) that hold automatically for any `A_L(d)` emission. This ASN then treats freshness both ways: as a "precondition" here (the K.μ⁺_L derivation says "K.λ's freshness precondition gives `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`") and as a *derived theorem* in "Freshness of the Allocation" ("By FirstEmissionFreshness and SubsequentEmissionFreshness … every emission of `A_L(d)` is fresh"). The same fact cannot be both a caller obligation and a derived guarantee. M-Pre correctly lists only `d ∈ dom(M)`, `N ≥ 3`, `eᵢ ∈ Endset`, `e₃ ≠ ∅`, so the Preconditions list is overstated relative to the claim the ASN actually commits to.

**Required**: Separate the genuine precondition (`ℓ` is the next `A_L(d)` emission) from the facts derived from it (freshness, `zeros=3`, `E₁=s_L`, `#E≥2`, `origin=d`). Cite the emission as the precondition and the structural/freshness facts as its consequences, so the K.μ⁺_L derivation invokes them as derived rather than as "K.λ's freshness precondition."

### Issue 2: D-MIN★ preservation argues only the empty case

**ASN-0087, Invariant Preservation (Per-State Invariants, D-MIN★ row)**: "`D-MIN★: v_ℓ at minimum if empty — K.μ⁺_L positioning rule (depth m_L(d))`"

**Problem**: D-MIN★ requires `min(V_{s_L}^{Σ'}(d)) = [s_L, 1, …, 1]`. The row discharges only the empty case (where `v_ℓ` becomes the minimum). In the non-empty case, `v_ℓ = [s_L, 1, …, 1, n_L+1]` is added *above* the existing positions; D-MIN★ holds because the pre-existing minimum `[s_L, 1, …, 1]` is retained and `v_ℓ` does not undercut it — but this is never stated. This case cannot be deferred to the D-SEQ★ derivation: ASN-0047 derives D-SEQ★ *from* D-MIN★, so using D-SEQ★ to establish D-MIN★ would be circular. D-MIN★ must stand on its own.

**Required**: Add the one-line non-empty case: the existing minimum `[s_L, 1, …, 1]` is preserved because every newly placed `v_ℓ` strictly exceeds it (`n_L + 1 > 1`), so `min(V_{s_L}^{Σ'}(d)) = min(V_{s_L}(d)) = [s_L, 1, …, 1]`.

## OUT_OF_SCOPE

### Topic 1: Well-formedness constraints on forward-reaching endsets
**Why out of scope**: The first Open Question (constraints on endsets whose spans reference not-yet-allocated I-addresses) is genuinely new territory — the StandardAuthoring discipline is defined and its consequences explored, but a full account of forward-reaching endset legality belongs to a future ASN, not this operation definition.

VERDICT: REVISE
