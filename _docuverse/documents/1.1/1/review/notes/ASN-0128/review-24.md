# Review of ASN-0128

## REVISE

### Issue 1: The defining displays for `members` and `targets_of` use the unmarked form the surface binds to a different view
**ASN-0128, Default predicates (D1, D3) vs. Denotation and views (View selection)**: View selection commits "a call that omits the selector reads `default`," yet D1 displays `members(K) = ⋃ { addrs(F) : (a, F, G) ∈ A_K^Σ }` and D3 displays `targets_of(x) = ⋃ { addrs(G) : … }` — both unmarked forms, both equated to the *active* reading.
**Problem**: The same expression has two meanings depending on which section governs. Under View selection's rule, `members(K)` denotes the default view, where D1's displayed equation is false whenever any Φ-member filters a source. The note knows the unmarked form is unsafe — D2's bridge writes `members(K, active)` explicitly and warns "the selector is load-bearing," and D3 needs a paragraph ("the selectors are part of the recipe, not an artifact of this section's `active`-reading convention") to manage the collision. A section-local preamble disclaimer ("the equations below are their `active` readings") is a trap for an implementer who reads D1's signature line `members(K) → set of addrs` and binds the unmarked call to the displayed equation.
**Required**: Write the selector into the defining displays and signature lines — `members(K, active) = …`, `targets_of(x, active) = …` — reserving the unmarked form note-wide for the default reading per View selection. The D1–D3 preamble's disclaimer sentence then becomes unnecessary.

### Issue 2: I0's single-span identity rests on an ⊕-cancellation step that is asserted, not shown
**ASN-0128, Idem operational semantics (I0)**: "and start and endpoint fix the displacement, the sum agreeing with `s` strictly below the action point and exhibiting the displacement from it on (TumblerAdd) — so coverage-equal F-slots are the *same* endset"
**Problem**: This is the load-bearing step of I0's entire closure argument — it discharges both the F-slot case and the Binary G case, and the conclusion "No query, matching or enumerating, selects between coverage-equal tuples by content" rests on it. What it needs is left-cancellation: equal start `s` and equal sum `s ⊕ ℓ = s ⊕ ℓ'` force `ℓ = ℓ'`. The parenthetical cites TumblerAdd, which is a definition of the sum's shape, not a cancellation result. The missing argument is a genuine case analysis on the two action points `k, k'`: if `k < k'`, the sum with `ℓ` differs from `s` at position `k` (the action-point component is nonzero) while the sum with `ℓ'` still agrees with `s` there — contradiction; so `k = k'`, then `ℓ_k` is read off by subtraction at `k` and the tails are the sums' tails verbatim. None of this is on the page; "the sum agreeing with `s` strictly below the action point" states the shape of one sum, not why two distinct displacements cannot produce the same sum.
**Required**: Either show the action-point case analysis (two or three sentences suffice: action-point component nonzero, hence the action point is the first disagreement position and is shared; subtraction at it and tail equality recover `ℓ`), or cite a foundation lemma that actually states cancellation for T12-well-formed displacements — if no such lemma exists, the inline derivation is mandatory.

### Issue 3: Organizational meta-prose in BH2's Effect
**ASN-0128, BH2 (determinate-walk), Effect**: "the authority evidence for the no-closure line lives where the line is drawn (What this note doesn't cover, Reachability over the denoted graph)."
**Problem**: This sentence advances nothing about the walk's semantics; it tells the reader where *other prose is located*. The reader following the Effect's specification must step around it, and the deferred section already carries the evidence with its own context — a citation at the use site needs no advance announcement. This is the forward-reference accretion pattern the anti-bloat classifier flags: prose justifying document organization rather than the claim.
**Required**: Delete the sentence. The Effect's own commitment ("one-step `succs`, a walk that halts at a branch, no closure or reachability predicate — by design, not omission") stands complete without it.

### Issue 4: Defensive dismissal of a case the registration scheme already excludes
**ASN-0128, BH1 (read-filter), Rewrite scope**: "Φ itself is never empty: every constructible `Σ_init` carries the shipped `retired` with BH1 (S1, mandatory by R-C1), so a no-filter-anywhere case names no conforming substrate."
**Problem**: The displayed rewrite is well-defined for any Φ, empty included (the subtraction is vacuous and default coincides with active); no claim downstream consumes Φ ≠ ∅. The sentence raises a case only to certify it unrealizable — reviser-drift shape: a paragraph imagining a case the framework's own preconditions already exclude. If the intended content is "on every conforming substrate the default view genuinely differs from the active view in general," that is derivable and unused; if it is nothing, the sentence is noise in the middle of the rewrite's mechanics.
**Required**: Delete the sentence, or reduce it to the bare fact where it is actually consumed (the following sentence's "on the shipped-only registry this is exactly `retired`'s own surfaces" already carries the shipped-registry instantiation).

## OUT_OF_SCOPE

### Topic 1: How a caller's K-designation resolves to a registry key
**Why out of scope**: The note says the operation surface exposes the three shipped representatives "under exactly these names," and `Emit_K` is a family indexed by K, but the binding protocol — whether an app-registered type is invoked by name, by representative endset, or by coverage class, and what namespace governs across apps — is genuinely successor territory, adjacent to Open question 8's multi-app composition. Nothing in this note's contracts is wrong for leaving it out.

### Topic 2: Rejection observability at the operation surface
**Why out of scope**: The exposed `Emit_K` and `Nullify_Binary` fix rejection as "no step, no address," uniformly across failure causes (gate, `K ≁ R`, invalid home, P-tgt). Whether callers can distinguish rejection reasons — an error channel, and its interaction with the partial-map signature — is operational machinery a future note can add without disturbing any contract here.

### Topic 3: Concurrency beyond the serializing authority
**Why out of scope**: I4 correctly scopes itself — `→_sh` inherits ASN-0086's sequential interleaved model, and the "serializing authority" that orders racing calls is posited, not specified. A real multi-writer protocol (who serializes, what the caller observes between submission and commit) is new state machinery, not a gap in this note's per-call contracts.

VERDICT: REVISE
