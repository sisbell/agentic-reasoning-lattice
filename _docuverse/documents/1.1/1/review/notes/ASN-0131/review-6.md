# Review of ASN-0131

This is a strong, carefully-argued note. The foundation citations are accurate (all to the verified foundation set), the WP analysis (RE-CWP) is genuine and non-trivial, the union-distributivity proof is fully shown, and the retraction analysis (RE-RET) is admirably honest about the imposed-discipline boundary on the type slot. I verified RE-DEF's `I ⊆ dom(Σ.C)` via S3★, the `Avail`-factoring used in RE-UDIST, the `sel = findlinks_V ∩ addressable` identity (RE-SEL), the contraction WP and its `R = ∅` collapse (RE-CWP), and the field-segment-agreement argument for `coverage(e₃) ∩ dom(Σ.C) = ∅` — all sound. The defects below are confined to the worked instance, which is the one place the ASN's verification of its own postconditions falls short of the claims it makes.

## REVISE

### Issue 1: Worked instance asserts an exact result that depends on two unspecified endsets

**ASN-0131, *A worked instance***: "The second, at a distinct address `ℓ₂ ≠ ℓ₁`, is `L₂ = (e₁, e₂′, e₃′)`" … "The answer is therefore a single role-tagged endset, `RE(W, d, Σ) = { (1, e₁) }`".

**Problem**: The displayed equality is stated as a definite fact, but `e₂′` and `e₃′` are never specified or constrained. With `dom(Σ.L) = {ℓ₁, ℓ₂}`, the answer is
`RE(W, d, Σ) = {(1, e₁)} ∪ ({(2, e₂′)} if touch_W(e₂′)) ∪ ({(3, e₃′)} if touch_W(e₃′))`.
Nothing rules out `a₂ ∈ coverage(e₂′)` or `a₂ ∈ coverage(e₃′)`, so as written the instance establishes only `{(1, e₁)} ⊆ RE(W, d, Σ)`, not the asserted equality. This directly undercuts the subsequent read-off: "**Per-endset surfacing (RE-OVL).** Only slot 1 appears" is justified only for `L₁`'s slots (`e₂`, `e₃` shown to miss); `L₂`'s slots 2 and 3 are never analysed, so "only slot 1 appears" is not actually shown. The instance is meant to *verify* the postconditions against a specific scenario; for the exactness claim it does not.

**Required**: Pin down `e₂′` and `e₃′` enough to make the equality hold — e.g. state `coverage(e₂′) ∩ {a₂} = coverage(e₃′) ∩ {a₂} = ∅` (or give them concrete coverage disjoint from the image, as was done for `e₂` and `e₃`) — and extend the "only slot 1 appears" read-off to cover `L₂`'s two non-from slots.

### Issue 2: The adopted convention RE-WHOLE is never exercised by a concrete scenario

**ASN-0131, RE-WHOLE / *A worked instance***: "(This endset is single-span, so it exercises *no-clipping* (RE-CLIP), not whole-endset surfacing (RE-WHOLE): both the whole-endset and touching-spans-only readings return this same single span unclipped.)"

**Problem**: RE-WHOLE is an introduced (if provisional) postcondition with a distinctive, non-obvious consequence — a *discontiguous* touching endset is surfaced with its non-touching spans intact, i.e. the answer volunteers anchoring that points *outside* the queried region. The ASN explicitly concedes the worked instance does not exercise this: `e₁` is single-span, so whole-endset and touching-spans-only coincide. Every other endset in the instance either misses or is single-span. Consequently the one behavior that distinguishes RE-WHOLE from a touching-spans-only implementation — the very distinction OQ1 turns on — is asserted but never verified against any concrete state. By the standard that key postconditions must be checked against at least one specific scenario, RE-WHOLE is unsupported.

**Required**: Add (or extend `ℓ₁` with) an endset carrying at least two spans, one covering an in-region address and one covering an out-of-region address, and show explicitly that the full endset — including the non-touching span — is returned. This both verifies RE-WHOLE and makes its difference from the touching-spans-only reading concrete, which is exactly what OQ1 is weighing.

## OUT_OF_SCOPE

(none) — The ASN correctly defers its boundary topics (intersection-distributivity, link-subspace regions, rendered/V-order mode, multi-store completeness, type-slot meaningfulness, multiplicity preservation, whole-vs-touching spans) to numbered Open Questions rather than smuggling claims about them into the body. No claim about a scoped-out sibling operation is defined here.

VERDICT: REVISE
