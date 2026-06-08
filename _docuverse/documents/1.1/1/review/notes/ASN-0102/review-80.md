# Review of ASN-0102

## REVISE

### Issue 1: J1'★ discharge conflates COPY's post-state residency (Σ') with the closing-boundary residency (Σ_clo) the coupling requires

**ASN-0102, X14, J1'★ discharge and Boundary dichotomy (BD-New)**: BD-New is defined as the horn for pairs that are *range-new across B →\* Σ_clo*: "If instead `a ∉ ran_{s_C}(B.M(d))` **but `a ∈ ran_{s_C}(Σ_clo.M(d))`**…". The J1'★ paragraph then discharges COPY's contribution with: "if `a ∈ New`, (BD-New) gives it range-residency **at Σ'**." And SL states only that "each such `a` is range-resident **at COPY's post-state Σ'**."

**Problem**: BD-New's defining condition is residency at the *closing boundary* `Σ_clo`. The set `New` is defined relative to the *opening* boundary `B` (`New = A ∖ ran_{s_C}(B.M(d))`) with **no** `Σ_clo` condition. SL establishes residency only at COPY's immediate post-state `Σ'`. When COPY is embedded mid-composite (`Σ' ≠ Σ_clo`), a later step in the same composite (e.g. a K.μ⁻ contraction) may remove the copied address from `d`'s content-subspace range before `Σ_clo`. Then `(a, d) ∈ R_clo ∖ R_B` (R is permanent, P2) but `a ∉ ran_{s_C}(Σ_clo.M(d))` — so the pair does **not** "land in" BD-New, and the asserted chain breaks. The note's conclusion ("COPY's step never grounds a J1'★ violation") is defensible as a *local* soundness statement, but the supporting step — that COPY's New additions are discharged by BD-New on the strength of Σ' residency — is not established, because the Σ' → Σ_clo gap is never closed.

**Required**: Either (a) explicitly scope the discharge to COPY as the closing/standalone step (`B = Σ`, `Σ_clo = Σ'`), making the general-`B` premise (`R_B ⊆ Σ.R ⊆ Σ'.R`, COPY mid-composite) consistent with that scope; or (b) state the dependency that COPY's New additions land in BD-New only insofar as they remain content-subspace-resident through `Σ_clo`, and attribute any later removal as the violating step — i.e. separate COPY's local Σ'-residency contribution from the composite-wide Σ_clo-residency obligation, rather than asserting BD-New (a Σ_clo property) is satisfied by SL's Σ' residency.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
