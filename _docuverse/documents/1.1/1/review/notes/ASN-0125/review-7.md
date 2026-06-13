# Review of ASN-0125

The central architecture is sound. EL0's reading of L12/LP13 as a weakest-precondition impossibility, the four-case closure of EL2, the RQ1–RQ7→EL3 derivation that the carrier must be a typed link-to-link tuple, and the two-allocation `editlink` contract all hold up under scrutiny. The proofs are mostly spelled out (EL4's per-claim single-target via PrefixSpanCoverage + R0a; EL11(a)'s "no content address extends a link address" via C1/L0/SC-NEQ; EL13's commutation via `a_emit` locality), the boundary cases that matter here are covered (value-identical edit, third-party edit, revert-without-successor, `current = ∅` standoff, `current = {y}` unedited), and the worked example exercises the contracts against concrete chain addresses. The issues below are a rigor gap and accumulated meta-prose, not errors in the core reasoning.

## REVISE

### Issue 1: `editlink` and `assert_sup` are treated as reachability-producing without discharging ValidComposite

**ASN-0125, EDITop/ASSERTop and the standing precondition**: The standing precondition reads "`Σ →* Σ'` is a finite (possibly empty) sequence of them drawn from **valid composites**," and EL7 concludes "When invoked at a reachable `Σ` ... `editlink(a, ℓ', d_s, d_a)` yields `Σ₂`" with the output then carried into `→*` reasoning (EL7(v), EL5, EL12).

**Problem**: `editlink` is presented as "a *derived composite*" of two `K.λ` steps and `assert_sup` as one `Emit_{K_sup}` (= `K.λ`). For `Σ₁`/`Σ₂` to be reachable — hence for every lifted invariant (R0a, L12, the per-state invariant package, ASN-0086's `wp` results) to apply to them — these `K.λ`-only sequences must satisfy ASN-0047's ValidComposite coupling clauses J0, J1★, J1'★. The ASN never checks them. They do hold vacuously (no `K.α`, no content-subspace `K.μ⁺`, no `K.ρ`, so `dom(C')\dom(C) = ∅`, no content-subspace range change, no provenance change), but a rigorous spec discharges them rather than assuming reachability. This is the composite analogue of "every invariant conjunct addressed."

**Required**: One sentence establishing that a `K.λ`-only sequence is a valid ASN-0047 composite — J0, J1★, J1'★ vacuous because no content is allocated, no content-subspace arrangement is extended, and no provenance is recorded — so the output states of both operations are reachable.

### Issue 2: the "Layer transfer" exhaustiveness over-claim

**ASN-0125, "The substrate we build on" (Layer transfer)**: "ASN-0086 proves its facts over the substrate vocabulary `{K.σ, K.α, K.λ}`, and **every such fact depends on exactly two properties of state evolution**: the link store changes only by `K.λ`'s fresh appends, and the document set `dom(M)` is monotone."

**Problem**: This is an unverified universal quantification over ASN-0086's theorems — exactly the exhaustiveness-claim pattern the anti-bloat classifier targets. The transfer *is* sound for the facts the note actually uses (R0a, `a_emit`, the `Emit`/`Observe`/`Nullify` contracts, `wp` Case 2, R3, R6a), each of which manifestly references only `dom(L)` and `dom(M)`; but "every such fact" asserts a property of proofs not in evidence. If even one ASN-0086 result leaned on a content-specific property of `K.α`, the universal would be false while the note would be none the wiser.

**Required**: Scope the transfer to the facts invoked (the cited ASN-0086 results reference only the link store and `dom(M)`, both preserved by Vocabulary fact V and M1), rather than asserting a universal property of ASN-0086's proof corpus.

### Issue 3: "Scope" meta-paragraph and stray essay content in structural slots

**ASN-0125, "The substrate we build on" (Scope)**: "**Scope.** This note works directly with the substrate transitions and state functions; it does not specify link creation, discovery, or read operations as user surfaces, citing existing foundation operators ... where a reader capability must be named."

**Problem**: A bolded "Scope" sub-paragraph that restates, in prose, the out-of-scope boundary the note already enforces through its operation set — meta-prose about the note rather than reasoning that advances it, and a flagged anti-bloat pattern. Two secondary instances of essay content in argument slots: EL3's second remark ("The commitment costs nothing in mechanism and something in coordination," closing on "a coordination problem the substrate deliberately declines to solve") and EL13's ASN-0042 digression on per-asserter "latest" under an ownership overlay — both carry a real point but inflate it with design philosophy a reader must wade through to reach the claim. (Vocabulary fact V is *not* in this category — it states what each transition does to `L`, which the guidance protects.)

**Required**: Delete the "Scope" paragraph (the operation set already fixes scope). Compress the EL3 coordination remark to its load-bearing core (the carrier requires no substrate change; conventions need an agreed root) and the EL13 overlay digression to its conclusion (cross-home order, and a fortiori per-asserter order absent single-home homing, is not a state function).

## OUT_OF_SCOPE

### Topic 1: coupling the edit to listing the successor
**Why out of scope**: EL7(ii) leaves the successor "born unlisted" and routes the question of whether a layer should couple `editlink` to a `K.μ⁺_L` listing to Open Question 7. The note's job is to fix what the edit *allocates and asserts*; making the result appear in a current view is a separate, deliberate act, correctly deferred.

### Topic 2: authority and stratification for claims that target claims
**Why out of scope**: EL8(d) observes claims are themselves addressable and editable; the well-foundedness of currency resolution over meta-claims, and the authority governing third-party retraction of a claim, are routed to Open Questions 1 and 3. These are new territory, not gaps in the present derivation.

VERDICT: REVISE
