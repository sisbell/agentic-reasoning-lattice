# Review of ASN-0125

I worked through the central thesis and checked the proofs against the foundation contracts. The mathematics is sound: EL0 (mutation impossible) is a clean instantiation of L12/LP13 read as a wp; EL3's elimination of the carrier alternatives is complete and each step cites a real RQ + foundation lemma; the assert_sup/editlink contracts (EL6, EL7) and the discipline-maintenance induction (EL-DM ← EL6(v)/EL7(vi), no circularity) hold; EL4's accessor-totality (PrefixSpanCoverage + R0a), EL10's position-reuse construction, EL11(a)'s projection biconditional, EL13's commutation, and EL14's sink analysis all check out. The worked example traces addresses, `succ_h`/`succ_o`, `current`, and listing correctly through edit, fork, demotion, standoff, repair, and registry churn. The Open Questions are legitimate deferrals (ownership-layer authority, meta-claim stratification, span-level correspondence, edit↔listing coupling), and the implementation notes are demarcated evidence, not spec mechanics — no drift.

One anti-bloat finding remains.

## REVISE

### Issue 1: EL11(b) closes with a use-site inventory
**ASN-0125, EL11 (TwoRegimeDiscovery), part (b)**: "the antichain R0a collapses `≼` to `=` precisely because `y` (resp. `x`) lies in `dom(Σ.L)` — which every use here supplies (`in(a, ·)`, `in(aᵢ, ·)`, `in(ℓ₀, ·)`)."

**Problem**: The parenthetical `(in(a, ·), in(aᵢ, ·), in(ℓ₀, ·))` enumerates the three downstream call-sites (EL16, EL15, the worked example) to reassure the reader that the qualification `y ∈ dom(Σ.L)` is always met. This is the use-site-inventory accretion pattern the anti-bloat mode targets: the load-bearing content is already stated — the `Observe`-identification needs `y ∈ dom(Σ.L)`, while the bare comprehension does not — and cataloging which later sites supply the condition is forward-pointing noise the reader skips past. It compounds if left at source.

**Required**: Drop the parenthetical list, and with it the "which every use here supplies" clause. The point is fully carried by the immediately following sentence ("It is the `Observe` *identification* that carries this qualification; the direct comprehension does not").

## OUT_OF_SCOPE

None. The note defines EDITLINK and assert_sup (not in the excluded set), and EL11's "discovery" concerns the supersession relation this ASN introduces (via foundation `Observe_{K_sup}`), not the out-of-scope FINDLINKS operation. References to ASN-0042 are to a foundation, correctly framed as an optional overlay.

VERDICT: REVISE
