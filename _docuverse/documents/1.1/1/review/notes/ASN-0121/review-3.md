# Review of ASN-0121

## REVISE

### Issue 1: The transition relation for `→` / `→*` is never defined, and the permanence claims cite R6a beyond its established domain

**ASN-0121, FL-MON and FL-RET**: "For any reachable `Σ →* Σ'` …" / "for every reachable `Σ →* Σ'` … `a ∉ findlinks(q, Σ')` … the monotonicity of `nullified` (R6a) keeps it out forever."

**Problem**: The ASN quantifies over "reachable `Σ →* Σ'`" in FL-MON and FL-RET (and over `Σ → Σ'` in FL-JUNK and FL-STB) without ever defining what transition relation `→` ranges over. This matters because the supporting lemma R6a (ASN-0086, RetractionStability) is established only over ASN-0086's `→ ≡ K.σ ∪ K.α ∪ K.λ` — the allocation-only relation, which excludes the editing operations (the K.μ family of ASN-0047). Yet FL-STB explicitly reasons about "insertion, deletion, rearrangement" transitions, so the intended `→` clearly spans the full ASN-0047 vocabulary. As written, the ASN is caught either way: if `→` is ASN-0086's relation, it contradicts the editing-stability narrative; if `→` is the full vocabulary, then R6a does not by itself discharge "keeps it out forever," because nothing in the cited lemma covers preservation of `nullified` across K.μ⁺/K.μ⁻/K.μ~. (The claim is in fact true — editing leaves `Σ.L` and hence `L_R^Σ` untouched, so `nullified` is constant across those steps — but that step must be shown, not folded silently into an R6a citation.)

Relatedly, FL-MON's parenthetical proof asserts "`a ∈ addressable(Σ')` since it is un-nullified" but never justifies `a ∈ dom(Σ'.L)`, which requires store monotonicity across `→*` (available as ASN-0098 StoreMonotonicity★, but uncited).

**Required**: Define the transition relation `→` the ASN reasons over (cite ASN-0047's atomic vocabulary), and establish that `nullified` and `dom(Σ.L)` are non-decreasing across *all* of it — explicitly noting that the editing operations preserve `Σ.L` (hence `L_R^Σ` and `nullified`) and citing store monotonicity for the membership step in FL-MON — rather than resting permanence solely on the allocation-scoped R6a.

### Issue 2: Matching of higher-arity links (arity > 3) is left implicit

**ASN-0121, "What is being matched" and FL-DEF**: "A link `a ∈ dom(Σ.L)` carries a value `Σ.L(a) = (e₁, e₂, …)` of at least three endsets (L3). The first three slots are, by convention, the *from-endset* `e₁`, the *to-endset* `e₂`, and the *type-endset* `e₃`."

**Problem**: L3 (foundation) permits arity `N ≥ 3`, and FL-WILD returns *all* addressable links (`findlinks((∗,∗,∗,∗), Σ) = addressable(Σ)`), so higher-arity links are genuinely in the result space. But `sat` constrains only `e₁, e₂, e₃`; for a link with `N > 3`, slots `e₄ … eₙ` are silently unconstrained. The semantics are determinate (higher slots ignored), which is presumably correct for an operation named FINDLINKS*FROMTOTHREE*, but the ASN never states this, leaving a reader to infer the treatment of the n-set case (which Nelson explicitly calls for at 4/79). This is the arity boundary case, and a self-contained spec should pin it down.

**Required**: State explicitly that for a link of arity `N ≥ 3`, `sat` constrains slots 1–3 and leaves slots 4+ unconstrained, and confirm this is the intended semantics for this operation. One sentence, plus ideally a line in FL-WILD or FL-DEF noting the result includes higher-arity links matched on their first three slots.

## OUT_OF_SCOPE

(none — the version-scoped retraction, V-spec/I-address agreement, and federation questions are correctly routed to Open Questions rather than claimed.)

VERDICT: REVISE
