# Channel Assignment — ASN-0100 review-15

**Date:** 2026-05-27 16:58

```
## Issue 1: S8a argument's set-membership is imprecise for the append case
Reason: The fix replaces an imprecise set-membership formulation with a direct citation of ValidInsertionPosition postcondition (b) / ValidFirstInsertionPosition postcondition (b) from ASN-0036, which the ASN already cites elsewhere. Purely a wording correction derivable from definitions already in the ASN.
```

```
## Issue 2: Composite-atomicity precondition wording is ambiguous
Reason: The body's own analysis (subspace separation via L0 + SC-NEQ) already establishes that INSERT depends only on A_C(d)'s chain and M(d)'s text subspace. The fix re-scopes the precondition wording to match this internal analysis; no external evidence needed.
```

```
## Issue 3: Exhaustiveness clause's K.μ⁻-fired case relies on a glossed argument
Reason: The fix is to state explicitly that step 3 of INSERT's contract constrains K.μ⁺ to add *exactly* the Insertion + Shifted-right positions. This is a specification authoring choice — the contract is INSERT's own, not a question about K.μ⁺'s vocabulary or design intent.
```

```
## Issue 4: P6 preservation argument elides a subtle case
Reason: The identification E_doc = dom(M) under ValidComposite★ is implicit throughout the ASN's substrate citations (e.g., INS.frame.E specialising to dom(M') = dom(M) for documents). The fix surfaces this existing identification; derivable from ASN-0047's framework as already used.
```

```
## Issue 5: The K.α ordering proof has a subtle circularity
Reason: The fix reframes the forced-ordering argument through K.α's subsequent-emission predicate consulting dom(C) — a mechanism already cited from ASN-0093 in §Effect One. The required reframing uses facts already established in the ASN.
```

```
## Issue 6: Missing concrete trace for the alternative decomposition in case (i.b)
Reason: The reviewer's required fix offers option (b) — explicitly note that the alternative decomposition is admissible only if the substrate retains pre-state link ordering across K.μ⁻. This is a limitation acknowledgment, statable from the ASN's own analysis without external evidence.
```

```
## Issue 7: K.ρ commutativity claim contradicts its own forced-ordering analysis
Reason: The fix is to note that K.ρ-before-K.μ⁺ relies on composite-level atomicity (already in INS.pre). The dependency is internal to the ASN — its own atomicity precondition makes intermediate states unobservable as composite boundaries.
```

```
## Issue 8: Tight endset trace's "tightness precondition" inserted late
Reason: The fix is to construct Σ_{e_1} explicitly in the worked example, grounding the tightness assumption in a concrete substrate state. The reviewer provides the construction template (dom(Σ_{e_1}.C) ⊇ {a₂, a₃, a₄} with canonical span); purely an authoring fix.
```
