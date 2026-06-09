# Review of ASN-0121

This is a careful, well-structured specification. The "answer is forced" derivation is genuinely tight, the `nullified`-monotonicity argument over the full ASN-0047 vocabulary is handled structurally rather than by a fragile per-operation enumeration, and the FL-REACH(d) correction of the naive "subsumes `discoverable_from`" claim is exactly the kind of self-scrutiny these proofs need. Most claims check out. Two issues remain.

## REVISE

### Issue 1: The worked example never exercises the residence axis — FL-RES has no concrete witness

**ASN-0121, "A worked instance" (Traces 1–5) vs. FL-RES**: All five traces fix `H = ∗`. The home-set criterion `liftH`/`athome` — the distinctive feature of a *four*-set operation, and the one axis Gregory's back end is documented to ignore (`TRUE||!homeset`, consultation Q12) — is never evaluated concretely for `H ≠ ∗`.

**Problem**: FL-DIR is given a fully explicit witness (concrete `x`, `y`, disjoint subtree coverages, both `q` and `q'` computed, the asymmetric set difference exhibited). FL-RES, an equally substantive named claim asserting residence/endpoint orthogonality, receives no analogous concrete verification. Standard 6 requires key postconditions to be checked against a specific scenario; the residence postcondition is precisely the one left unchecked, and it is the one most likely to be mis-implemented (per the ASN's own divergence note). The claims that `H` may bound at node/account/document granularity via T5, and that residence can exclude a link that satisfies every endpoint criterion, are asserted but never traced.

**Required**: Add a trace constraining the home-set. The store as given suffices: take `q = (H_other, X, Y, ∗)` with `H_other` covering a document other than `d`, and show `a₁` — which Trace 1 returned under `(∗, X, Y, ∗)` — is now excluded purely on `liftH`, while `q = (H_d, X, Y, ∗)` with `H_d` covering `d`'s subtree readmits it. Better still, add a link homed at a second document with endpoints identical to `a₁` to witness orthogonality directly (residence varied while endpoints held fixed). Exercise at least one node/account-granularity `H` to verify the T5 subtree-membership reading of `athome`.

### Issue 2: FL-STB's precondition is redundant by the ASN's own argument

**ASN-0121, FL-STB**: "for a transition `Σ → Σ'` that preserves the link store and the retraction set — `Σ'.L = Σ.L`, `nullified(Σ') = nullified(Σ)`."

**Problem**: The ASN argues earlier, in deriving `nullified`-monotonicity, that "`nullified(Σ)` is a function of `Σ.L` *alone* — it is defined through the retraction relation `L_R^Σ`, which is itself a subset of the link store." Under that very fact, `Σ'.L = Σ.L` *entails* `nullified(Σ') = nullified(Σ)`; the second conjunct of the hypothesis is not an independent assumption but a consequence of the first. Stating it as a separate precondition obscures the actual minimal hypothesis and reads as though the two could come apart.

**Required**: State the hypothesis as `Σ'.L = Σ.L` alone, noting that `nullified(Σ') = nullified(Σ)` follows because `nullified` is a function of `Σ.L` (as established in the monotonicity discussion).

## OUT_OF_SCOPE

None to record beyond the topics already fenced by the Scope note; the ASN correctly defers version/time-qualified inquiry, V-spec/I-address agreement, residence-as-single-prefix reduction, type-hierarchy exactness, and federation to its Open Questions rather than claiming them.

VERDICT: REVISE
