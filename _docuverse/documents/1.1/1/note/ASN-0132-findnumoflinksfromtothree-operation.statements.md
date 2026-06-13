# ASN-0132 Claim Statements

*Source: ASN-0132-findnumoflinksfromtothree-operation.md (revised 2026-06-13) — Extracted: 2026-06-13*

## Definition — SatisfactionPredicate

`sat(a, q, Σ) ≡ liftH(a, H) ∧ lift(Σ.L(a).e₁, F) ∧ lift(Σ.L(a).e₂, G) ∧ lift(Σ.L(a).e₃, Θ)`

Where `q = (H, F, G, Θ) ∈ (Endset ∪ {∗})⁴`; each constrained slot demands a single-address overlap (`touch`) between the link's endset and the request set, or for the home slot, residence of `home(a)` in the request region (`athome`); a wildcard slot drops out.

- `liftH(a, H) ≡ athome(a, H) ≡ home(a) ∈ coverage(H)`
- `lift(e, S) ≡ touch(e, S) ≡ coverage(e) ∩ coverage(S) ≠ ∅`

## Definition — AddressableLinks

`addressable(Σ) = dom(Σ.L) \ nullified(Σ)`

The link store minus those targeted by a retraction tuple.

---

## CN-DEF — CountLinksFTT (DEF, function)

`countlinks_FTT(q, Σ) ≡ |{ a : a ∈ addressable(Σ) ∧ sat(a, q, Σ) }|`

The operation reads `Σ` and returns a natural number; its frame is `Σ` — it writes nothing, mutating no component of the state. Defined through the shared relation `sat` (ASN-0121), not through the enumeration operation. Well-defined because the counted set is a finite, computable subset of `dom(Σ.L)` (L-fin ASN-0093, FL-DEC ASN-0121).

---

## CN-LOC — LinkStoreLocality (LEMMA, lemma)

For fixed `q`, `countlinks_FTT(q, Σ)` is a function of `Σ.L` alone; `Σ.C`, `Σ.M`, `Σ.E`, `Σ.R` are never consulted.

Because `sat(a, q, Σ)` consults only the stored value `Σ.L(a)` and the address projection `home(a)`, and `addressable(Σ)` is a function of `Σ.L` alone (FL-LOC, ASN-0121), the counted set — and therefore the count — is a function of `Σ.L` and `q` alone.

---

## CN-UNIT — UnitIsLinkIdentity (THM, theorem)

For every request `q` and state `Σ`, each `a ∈ addressable(Σ)` with `sat(a, q, Σ)` contributes exactly `1` to `countlinks_FTT(q, Σ)`, and each `a` with `¬sat(a, q, Σ)` or `a ∉ addressable(Σ)` contributes `0`. The contribution of a link is independent of:

- (a) the number of spans or addresses its endsets reference (absorbed by the existential in `touch`)
- (b) the number of documents through which its endpoint content is reachable (excluded by CN-LOC)
- (c) the number of arrangement positions at which it surfaces (excluded by CN-LOC)
- (d) the number of versions into which the documents it touches refract (forking shares content references via J4's K.μ⁺ step, no K.α — J4 ASN-0047 — so the version DAG adds no link address; a special case of (c), excluded by CN-LOC)

---

## CN-TRANSCL — TransclusionInvariance (THM, theorem)

A link whose endpoint content is reachable through any number of documents by transclusion contributes `1` to the count. The quantity that grows with sharing — *how many documents reach the content* — is a count of documents, not of links, and is measured by an operation over `Σ.M`, not by this one.

Corollary of CN-LOC and CN-UNIT.

---

## CN-SHARED — MatchDescriptionInSat (META, meta)

The four-set matching criterion is `sat` (ASN-0121), a predicate on a link, a request, and a state. The enumeration is the *set* it carves out; the count is the *size* of that set. The specification of each is a query over `sat`; the specification of neither appeals to the behaviour of the other.

---

## CN-ENUM — CountEqualsEnumerationLength (THM, theorem)

`countlinks_FTT(q, Σ) = |findlinks_FTT(q, Σ)|`

Because both sides are the cardinality of the single set `{a ∈ addressable(Σ) : sat(a, q, Σ)}` — the right side by FL-DEF (ASN-0121), the left by CN-DEF. The equality holds whenever both sides are evaluated against the *same* `Σ`. At a distinct state `Σ'`, `countlinks_FTT(q, Σ')` equals `|findlinks_FTT(q, Σ')|`, not necessarily `countlinks_FTT(q, Σ)`.

---

## CN-ZERO — ZeroIsExistentialEmpty (THM, theorem)

`countlinks_FTT(q, Σ) = 0  ⟺  (A a : a ∈ addressable(Σ) : ¬sat(a, q, Σ))`

A zero count asserts that *no* addressable link in the store satisfies the four sets at `Σ` — that the satisfying set is empty. It is a positive statement about the contents of the link store.

Two weaker readings are excluded:
- "*none could be found*" — excluded by non-impedance (FL-JUNK, ASN-0121): `sat` is decided per link; a zero is a verdict over the whole addressable store.
- "*none could be displayed*" — excluded by CN-LOC: surfacing is a `Σ.M`-property the count does not read.

Note: if a constrained component of `q` has empty coverage, its lift is `false` for every link (FL-EMP, ASN-0121), and the count is `0` vacuously — this *empty-request* zero is distinct in meaning from the *empty-store* zero of CN-ZERO, though the returned number is indistinguishable.

---

## CN-SNAP — CountIsSnapshot (THM, theorem)

`countlinks_FTT(q, Σ)` is a function of the state `Σ`. No component of `Σ` records it; there is no stored counter that the operation reads or maintains. After any mutation `Σ → Σ'` the value `countlinks_FTT(q, Σ')` may differ from `countlinks_FTT(q, Σ)`, and the specification imposes no obligation that the earlier value remain valid. Re-establishing the count requires re-evaluating the cardinality at the current state.

---

## CN-STAB — InvarianceUnderArrangementEditing (THM, theorem)

For a fixed request `q`, any transition `Σ → Σ'` that preserves the link store — `dom(Σ'.L) = dom(Σ.L)` and `Σ'.L(a) = Σ.L(a)` for all `a` — satisfies

`countlinks_FTT(q, Σ') = countlinks_FTT(q, Σ)`

Proof is immediate from CN-LOC. Note: `nullified(Σ') = nullified(Σ)` is a *consequence* of `Σ'.L = Σ.L`, not an extra hypothesis, because `nullified(Σ)` is a function of `Σ.L` alone. Transitions covered: content insertion, deletion, and rearrangement (F-PRES, ASN-0127), content allocation (K.α), and provenance recording (K.ρ). Only link creation and retraction — transitions that grow `Σ.L` or `nullified` — can move the count.

---

## CN-RETRACT — RetractionExcludesImmediately (THM, theorem)

If `a ∈ nullified(Σ)`, then `a` contributes `0` to `countlinks_FTT(q, Σ)` for every `q`, and continues to contribute `0` at every reachable successor state (the nullified set never shrinks — R6a, ASN-0086). Yet `a` remains in `dom(Σ.L)` with its value `Σ.L(a)` permanently fixed (L12, ASN-0043). The count ranges over `addressable(Σ) = dom(Σ.L) \ nullified(Σ)`; it counts the *active view*, not the *store*.

---

## CN-MONO — MonotoneAccumulation (THM, theorem)

Across any `Σ →* Σ'` in which no currently-counted link becomes nullified, `countlinks_FTT(q, Σ) ≤ countlinks_FTT(q, Σ')`, and each newly created link that satisfies `q` and is addressable increments the count by exactly `1`.

For a transition `Σ → Σ'` creating a fresh ordinary link `ℓ` (fresh: `ℓ ∉ dom(Σ.L)`; ordinary: `L_R^{Σ'} = L_R^Σ`):

```
countlinks_FTT(q, Σ') = countlinks_FTT(q, Σ) + 1   if sat(ℓ, q, Σ') ∧ ℓ ∉ nullified(Σ')
countlinks_FTT(q, Σ') = countlinks_FTT(q, Σ)        otherwise
```

Weakest precondition for the count to rise:

`wp(create ℓ, countlinks_FTT(q, ·) = countlinks_FTT(q, Σ) + 1) = sat(ℓ, q, Σ') ∧ ¬(E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))`

— the new link must itself satisfy the four sets *and* not be born already-retracted. This is the FL-WP(a) condition of ASN-0121. Under the unit-depth retraction discipline (ASN-0086), R0a forces `t = ℓ` from `t ≼ ℓ` (contradicting freshness), so the second conjunct is automatic and the precondition collapses to `sat(ℓ, q, Σ')`.

---

## CN-ORPHAN — OrphansAreCounted (THM, theorem)

A link `a ∈ addressable(Σ)` with `sat(a, q, Σ)` is counted whether or not any document surfaces its endpoint content — that is, whether or not `discoverable_from(a, d, Σ)` holds for any `d`. The count is an *existence* quantity over the addressable store, not a *discovery* quantity over arrangements.

The counted set is a *superset* of what any document surfaces (FL-REACH, ASN-0121, made a cardinality); the gap is exactly the orphans. A link unsurfaced by any arrangement remains in `dom(Σ.L)` with its value unchanged (LP17, ASN-0098), and if addressable and matching, is counted. Discoverability rising (LP18, ASN-0098) does not change the count; the link was counted all along.

---

## CN-OBT — CountIsExistenceAssertion (THM, theorem)

`countlinks_FTT(q, Σ) = N` asserts that `|{a ∈ addressable(Σ) : sat(a, q, Σ)}| = N`. It does not assert that those `N` links are deliverable on demand. Delivery is a separate concern across a separate boundary (out of scope here), subject to availability the count never speaks to. The count promises *that `N` satisfying links exist in the store*, not *here are `N` handles you may fetch*.
