# Review of ASN-0123

I checked the proofs against the foundation contracts, traced the operation's step decomposition, and exercised the boundary cases. The last revision (P-bdy precondition; V9w/V-WF boundary repairs) targeted review-9's single issue; I verified the fix discharges it and found no residual or new defect.

## REVISE

None. The verifications below are the load-bearing ones.

**Boundary-property machinery (the prior issue), V9w + V-WF.** The new P-bdy precondition is used correctly and is genuinely necessary. V9w's first conjunct `(a, d_src) ∈ R'` derives from `(a, d_src) ∈ Contains_C(Σ) ⊆ R` via P4★ — which holds at Σ *only because* Σ is a composite boundary (P-bdy). The ASN is right that the bare-monotonicity route fails: at an interior start where a K.μ⁺ has extended `d_src`'s range with `a` but the matching K.ρ has not fired, `a ∈ A` while `(a, d_src) ∉ R`. P4★'s status as a composite-boundary property (not a per-state invariant) is exactly what makes P-bdy load-bearing rather than decorative. V-WF's terminal-boundary inference (Σ boundary + valid composite ⟹ Σ' boundary, hence P4★ ∧ P4a ∧ P7a at Σ') is sound. The atomicity remark's separation of P-bdy (predecessor) from interior-unobservability (successor) is coherent — V-WF needs only that VERSION executes as one valid composite, which clauses 1–2 establish.

**V9 severance theorem.** Proof of (a) is airtight. Assuming `d_src ≼ v`: O5(ii) at v's allocation forces `#pfx(π_o) ≤ #pfx(π)`; Covering-chain + O1b give `pfx(π_o) ≺ pfx(π)`, so `#pfx(π_o) < #pfx(π)`; then the `d_src ≼ pfx(π)` branch contradicts O1a (Z-mono pushes `zeros(pfx(π)) ≥ 2`) and the `pfx(π) ≼ d_src` branch contradicts O2's maximal-coverer definition of `ω(d_src) = π_o`. Both close. The reliance on `allocated_by(π, v)` (and hence O5 *with respect to π*) is correctly grounded in the account-tier restriction that makes v a single K.δ in π's own domain.

**VN-B1, SA, PS.** The contiguity induction correctly rules out node/k=2 arrivals (zeros and penultimate-component arguments) and pins k=1 to `c₁` and k=0 to the frontier `c_{m+1}`, independent of VD — the right insight. SA's antichain argument (a proper extension would force `zeros(d') ≥ 3`) is valid given LP-Sub's `#E = 2` form, and it is what converts subtree coverage to singleton identity in G2/V10. PS's coverage derivation is complete: position 1 survives every increment (TA5(b) for k>0; `sig(t) = #t ≥ 3` for the non-node k=0 operand), so `n₀ = [1] ≼ e` propagates and `ω` is total.

**Transcription and carry-through.** V-WF's single K.μ⁺ produces the canonical D-SEQ★ set `{[s_C,1,…,1,k]}`, discharging D-CTG★/D-MIN★/S8a/S8-depth. V10 chains LP12 (at d=v) with `ran(Σ'.M(v)) = A` (V2) and LP3 to give the discoverability biconditional, including the post-fork and orphan cases. V2b's impossibility of carrying link-subspace arrangement (CL-OWN vs K.μ⁺_L's `origin(ℓ)=d`) correctly forces content-anchoring as the sole cross-fork channel.

**Edge cases.** n=0 (empty source) verified across V0/V1/V2/V9w/V10/V13 (vacuities hold). Cross-owner node-tier exclusion is forced (intermediate account would be a second permanent entity, breaking V0/V1) and correctly delegated to out-of-scope account establishment while consuming only `Document(v) ∧ v∉E ∧` O5-wrt-π. Iterated forks (V6) stay at `zeros = 2`, so B6 holds at every depth unconditionally — depth-1 forking never spends the separator budget.

I scrutinized the V7 "from any version … trunc(v) = d_src" disambiguation, which fails for cross-owner forks (V9 severance, `parent(v) =` forker's account). It is defensible as written: the paragraph is built entirely on V4c / K.δ-ID.parent-0/1 (owned-fork citations), and V7's apparatus (`S(d,1)`, the registry query) is the owned version-chain throughout, with the cross-owner case partitioned into V9. Not a defect.

## OUT_OF_SCOPE

Nothing improperly included. The ASN touches document creation, edit ops (K.μ family), and link discoverability only through frame conditions and foundation invariants bearing on the fork's guarantees — it defines none of those operations. Its own Open Questions section appropriately defers concurrency serialization, withdrawal/supersession, location-fixed windowing, and derivation-direction recovery to future ASNs.

VERDICT: CONVERGED
