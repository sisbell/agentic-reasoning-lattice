# Regional Review — ASN-0034/TA5 (cycle 1)

*2026-04-24 08:38*

Reading ASN-0034 as a system to find new issues not in the previous findings.

### Variable `k` overloaded in T4 Axiom schema
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: T4 Axiom, the per-`k` schema and the strictly-positive clause: "for each `k ∈ ℕ` with `0 ≤ k ≤ 3` at which `zeros(t) = k`, the form is — `k = 0`: ... `k = 3`: `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`. In every case, `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ` at every position present."
**Issue**: The symbol `k` is used both as the case index (`zeros(t) = k`, bound to the values 0..3) and as the running component subscript on the document field (`Dₖ` ranging 1..γ). Every other field uses a distinct running letter (`i`, `j`, `l`). A precise reader pauses to disambiguate the two roles; swapping the document subscript to any unused letter (e.g., `Dₕ`) would remove the overlap without touching content.

### TA5a Case k=0 does not crisply close the T4(iv) step
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: TA5a proof, Case `k = 0`: "By TA5-SigValid, `sig(t) = #t`; by T4(iv), `t_{#t} ≠ 0`; hence `t_{sig(t)} ≠ 0`. By NAT-closure, `t_{sig(t)} + 1 ∈ ℕ`; by NAT-zero and NAT-addcompat, `t_{sig(t)} + 1 > t_{sig(t)} ≥ 0`, so `t_{sig(t)} + 1 ≠ 0`. … No new adjacencies arise. For T4(iii), we split on `sig(t)`: …"
**Issue**: The Case `k = 0` walk states T4(i) (via `zeros(t') = zeros(t)`), T4(ii) ("no new adjacencies arise"), and T4(iii) (via the `sig(t) = 1` / `sig(t) ≠ 1` split), but never explicitly lands T4(iv). The ingredients are present — `t'_{sig(t)} = t_{sig(t)} + 1 ≠ 0` and `sig(t) = #t = #t'` — but the reader must compose them. Cases `k = 1` and `k = 2` do close T4(iv) crisply ("boundary `t'_{#t'} = 1 ≠ 0`"); the Case `k = 0` omission makes the four-clause walk asymmetric.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 678s*
