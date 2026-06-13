# Review of ASN-0123

## What I verified

**SA (StoredAddressAntichain).** The `a ≺ b ⟹ zeros(d') ≥ 3` contradiction is correct: `a ≼ b` forces `d₀ ≼ d'`, so `d'` carries `d₀`'s two zeros plus the inherited separator at position `#d₀+1` (distinct, since it lies beyond `#d₀`). Sound.

**VN-B1 (VersionNamespaceContiguity).** The K.δ case split is exhaustive and each case closes: Node excluded by `zeros`; `k=2` excluded by the penultimate-separator argument; `k=1` pins `c₁` with `m=0`; `k=0` forces the operand to `c_{j-1}` and freshness pins `j=m+1`. The proof correctly leans only on K.δ's freshness/operand frames, not on VD or global B1. The deliberate refusal to invoke ASN-0040 B2 (whose stated precondition is *global* B1) and the re-derivation of the frontier from VN-B1 + S0 is exactly right.

**PS coverage / ω totality.** The induction `n₀ ≼ e` holds at every K.δ output: `k>0` appends (TA5(b)), `k=0` touches only `sig(t)=#t`, and the `¬Node` operand has `#t ≥ 3` so position 1 is untouched. Coverage is genuinely derived, not assumed, so O2's totality argument transfers.

**V9 severance (the crux), verified assuming-false-until-proven:** `pfx(π_o) ≼ v` ⟹ (O5(ii)) `#pfx(π_o) ≤ #pfx(π)` ⟹ (comparability + O1b) `pfx(π_o) ≺ pfx(π)` strict ⟹ both `d_src ≼ pfx(π)` (Z-mono vs O1a) and `pfx(π) ≼ d_src` (strict-longest-coverer vs O2) contradict. Airtight, and it correctly identifies the account-tier restriction as what pins `allocated_by(π,v)` directly rather than as an imported stipulation.

**V-WF, V8, V9w, V10, V13** each check out: ValidComposite★'s two clauses are discharged (intermediate K.δ/K.μ⁺/K.ρ preconditions; J0 vacuous; J1★/J1'★ = the `R'` clause); V8's coverer-set equality survives the Z-mono/O1a step; V9w's source-side conjunct correctly turns on P4★ *at the boundary* (P-bdy), with the load-bearing role of the boundary hypothesis explicitly defended; V10 reduces cleanly to LP12 at `d=v` with `ran(Σ'.M(v))=A`.

**Boundary cases** are handled: empty source (`n=0`, identity-allocation alone, couplings vacuous), first-vs-subsequent fork (`m=0` vs `m≥1` collapsing to `c_{hwm+1}`), abandoned versions (P1 keeps the rank taken, preserving contiguity), and the node-tier non-owner exclusion (forced, to keep the mint count at one). Concrete example (the `1.1.0.1.0.1` chain) verifies V4/V5/V6, and the golden tests ground V1/V2/V3/V11.

## REVISE

None.

Two points I examined and cleared rather than flag: (1) the Effect clause's unsubscripted `M'(d) = M(d) for every d ∈ E_doc` is unambiguous given the adjacent `M'(v)` line (it ranges over `Σ.E_doc`); (2) V10's citation of single-step LP2/LP3 for a composite transition is redundant but not wrong — `L'=L` (V1) gives `Σ'.L = Σ.L` for the whole composite directly, so coverage-at-Σ equals coverage-at-Σ' independent of the cited lemmas. Neither is wrong-as-stated, so neither meets the REVISE bar.

The cross-foundation `B = E` (entity-level) identification and the PS hybrid are asserted, not derived — but the ASN is explicit that "reading ASN-0042's ownership vocabulary over ASN-0047's states is a hybrid the two foundations do not assemble for us," states PS as a standing assumption, and discharges from it only what coverage supplies (ω totality). That is the legitimate way to bridge two foundations; it is not a gap to be closed inside this ASN.

## OUT_OF_SCOPE

The ASN defines no claims for out-of-scope topics — it touches account establishment, editing, links, and comparison only through frame conditions and the Open Questions list, never by specifying them. Nothing to flag.

VERDICT: CONVERGED
