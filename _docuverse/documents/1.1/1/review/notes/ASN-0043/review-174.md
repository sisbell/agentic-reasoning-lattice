# Review of ASN-0043

I checked every L-claim's proof, the FSP/FSE/CPP lemmas, PrefixSpanCoverage, and traced the six-step worked example arithmetic. The mathematics is sound — the prefix-cone coverage proof, the home-preservation arguments in CPP/FSE, the coverage-equality in Steps 5–6, and the L8 discrimination in Step 4 all check out. My findings are confined to the anti-bloat lens this revision carries.

## REVISE

### Issue 1: Unused guard-explanation paragraph sits between the L1c axiom and its proof
**ASN-0043, L1c — LinkAllocatorConformance**: "On a T4-valid input the `k = 1` guard `zeros(tᵢ₋₁) ≤ 3` holds unconditionally (T4-validity propagates along the chain by T10a.4), so only the `k = 2` guard — failing at `zeros = 3` — can actually constrain a step."
**Problem**: This is exposition about which guard "can actually constrain a step," not a statement the axiom makes and not a step any proof uses. The L1c chain's guards are verified per-step explicitly in every consumer (L9 Case A, the worked-example L1c check); FSE uses `k = 0` only. The paragraph matches the flagged pattern "new prose around an axiom explains [the role of its guards] rather than what it says" — a reader following the L1c claim skips it. The immediately following sentence ("The first step seats the field-separating zero at position `#s + 1`...") is a legitimate what-the-step-does statement and should stay.
**Required**: Delete the guard-commentary sentence; retain the axiom and the field-separator sentence.

### Issue 2: L0a opens with a scope-rationale sentence before defining anything
**ASN-0043, L0a — ContentSubspaceScope**: "This ASN scopes its content-side disjointness guarantee to the `s_C`-resident portion of the content store."
**Problem**: A standalone scope-intent sentence preceding the actual definition (`dom(Σ.C)|_{s_C} = ...` and the `s_C`-resident predicate). It restates, in narrative form, what the open question and the qualifier "`s_C`-resident" already carry throughout. This is the "Scope" sub-paragraph pattern the anti-bloat note flags.
**Required**: Drop the opening sentence and lead with the *Content-side T4-validity* derivation and the definition; the scoping is self-evident from the defined slice.

## OUT_OF_SCOPE

### Topic 1: Extending content-side disjointness from the `s_C`-resident slice to all of `dom(Σ.C)`
**Why out of scope**: L14/L14a's disjointness is deliberately scoped to `s_C`-resident content, and the first Open Question already names the missing global content-subspace invariant as future work — not an error in this ASN.

VERDICT: REVISE
