# ASN-0114 Claim Statements

*Source: ASN-0114-followlink-operation-read-one-endset-of-a-link-by-selector.md (revised 2026-06-04) — Extracted: 2026-06-08*

## Definition — Coverage

`coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})`

Variables: `e ∈ Endset = 𝒫_fin(Span)`; `s` is a start tumbler address; `ℓ` is a length; `T` is the tumbler space; `⊕` is tumbler addition (OrdinalShift, ASN-0034).

---

## Definition — SelectorValidity

`wp(followlink(a, i), R is a span-set ∧ coverage(R) = coverage(Σ.L(a).eᵢ))`
`≡ a ∈ dom(Σ.L) ∧ 1 ≤ i ≤ |Σ.L(a)|`

---

## F0 — FollowLink (DEF, function)

`followlink(Σ, a, i)` is *defined* (returns a span-set) exactly when `a ∈ dom(Σ.L) ∧ 1 ≤ i ≤ |Σ.L(a)|`; otherwise it returns the distinguished error value `⊥`. When defined, the returned span-set `R` satisfies `coverage(R) = coverage(Σ.L(a).eᵢ)`.

---

## F1 — CoverageExactness (POST, ensures)

For `a ∈ dom(Σ.L)` and `1 ≤ i ≤ |Σ.L(a)|`, with `R = followlink(Σ, a, i)`:

`coverage(R) = coverage(Σ.L(a).eᵢ)`

---

## F2 — DiscontiguityFaithfulness (LEMMA, lemma)

If `coverage(Σ.L(a).eᵢ)` is disconnected, then any `R` satisfying F1 has `|R| ≥ 2`. The discontiguous structure of the recorded end survives into the result; coverage exactness alone enforces it.

*Disconnected* means: there exist `p < q < r` in `T` with `p, r ∈ coverage(eᵢ)` but `q ∉ coverage(eᵢ)`.

Proof sketch: a single span `σ` is order-convex — `⟦σ⟧` contains every position between any two of its members (ASN-0053, S0). So if `R = ⟨σ⟩` with `⟦σ⟧ ⊇ {p, r}`, then `q ∈ ⟦σ⟧ = coverage(R)`, yet `q ∉ coverage(eᵢ)` — contradicting F1.

---

## F3 — RepresentationInvariance (LEMMA, lemma)

Any two span-sets `R, R'` each satisfying F1 for the same `(Σ, a, i)` are denotationally equal: `coverage(R) = coverage(R')`. The operation's guarantee is a property of the position set, not of the span decomposition or the ordering of spans within the result.

---

## F4 — PureRead (INV, predicate)

`followlink` induces no state transition. For the state `Σ` against which it is evaluated, the post-state equals `Σ`: the content store `Σ.C`, the link store `Σ.L`, every arrangement `Σ.M(d)`, and every other endset of the queried link are identical before and after. In particular, requesting end `i` of link `a` changes neither `Σ.L(a)` itself, nor any `Σ.L(a).eⱼ` for `j ≠ i`, nor any document the selected end points into.

---

## F5 — TemporalDeterminism (LEMMA, lemma)

Let `Σ →* Σ'` be any reachable transition sequence with `a ∈ dom(Σ.L)`. Then `a ∈ dom(Σ'.L)` and `coverage(followlink(Σ', a, i)) = coverage(followlink(Σ, a, i))` for every valid selector `i`.

*Derivation dependencies:* L12 (LinkImmutability) fixes a link's value across a single transition; LP13 (UnconditionalLinkPersistence, ASN-0098) extends this to `Σ →*` via its closure schema (★), giving `Σ'.L(a) = Σ.L(a)`, hence `Σ'.L(a).eᵢ = Σ.L(a).eᵢ`. F1 applied at each state then equates the coverages.

---

## F6 — SlotConfinement (LEMMA, lemma)

`followlink(Σ, a, i)` is a function of the single endset `Σ.L(a).eᵢ` (up to coverage). Formally, for links `a, a'` with `coverage(Σ.L(a).eᵢ) = coverage(Σ.L(a').eᵢ)` and arbitrary contents at all slots `j ≠ i`, the results satisfy `coverage(followlink(Σ, a, i)) = coverage(followlink(Σ, a', i))`. The result neither depends on nor returns any `eⱼ` with `j ≠ i`.

---

## F7 — EmptyVersusInvalid (INV, predicate)

The empty span-set `⟨⟩` (a success, denoting `∅`) and the error value `⊥` (a domain violation) are distinct return categories, `⟨⟩ ≠ ⊥`.

- For a valid selector `1 ≤ i ≤ |Σ.L(a)|` over a link `a ∈ dom(Σ.L)` whose end `eᵢ` is empty: `followlink(Σ, a, i) = ⟨⟩`.
- For an invalid selector — `i < 1`, or `i > |Σ.L(a)|`, or `a ∉ dom(Σ.L)` — `followlink(Σ, a, i) = ⊥`.
- An implementation that collapses these two cases is incorrect.

wp form:

`wp(followlink(a, i), result ≠ ⊥) ≡ a ∈ dom(Σ.L) ∧ 1 ≤ i ≤ |Σ.L(a)|`

and the complementary `wp(followlink(a, i), result = ⊥)` is the negation of that condition.

Uniqueness of `⟨⟩`: by ASN-0053 S2, every well-formed span denotes a non-empty set; hence no span-set with one or more spans can have empty coverage, and `⟨⟩` is the *only* span-set whose coverage is `∅`.

---

## F8 — ContentIndependence (LEMMA, lemma)

`followlink(Σ, a, i)` is defined and satisfies F1 whenever `a ∈ dom(Σ.L)` and `1 ≤ i ≤ |Σ.L(a)|`, irrespective of whether any address in `coverage(Σ.L(a).eᵢ)` currently holds content or a link in `Σ`. The result reports the recorded region; the existence of material at that region is a separate question the operation does not ask.
