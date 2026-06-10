# Review of ASN-0114

The rigor is sound. F1–F8 are logically complete: F1 is a posited contract with a genuine satisfiability witness (the endset is its own witness); F2's `|R| ≥ 2` is proved in two steps (≠⟨⟩, ≠ singleton-via-convexity); F5 composes L12 correctly through LP13; F7's two S2 collapses and the L3 slot-3 discharge are correct; the worked instance verifies F1/F2/F7 against a concrete link (coverage(e₁) = [a₃,a₅) ∪ [a₇,a₉), the disconnection witness q = a₅, and the ⟨⟩-vs-⊥ split all check out). The note also stays at the coverage abstraction throughout, honestly disclaiming representation-level guarantees (F3, F6) — no drift.

The findings below are anti-bloat: forward-reference accretion and a micro-fact derived four times. This note carries `review-mode.anti-bloat`, and these are exactly the patterns it asks me to surface at source.

## REVISE

### Issue 1: The "Status of the result" paragraph carries notational meta-prose and a use-site inventory

**ASN-0114, "The selector and its domain" → "Status of the result — a relation, determinate up to coverage"**:
> "These are exactly the two cases in which the later sections write `followlink` as a bare equality — the `⊥` of an invalid selector and the `⟨⟩` of an empty end, in F7 and in the worked instance — and there the notation is licensed by this single-valuedness."

and

> "Outside these uses the result is determinate only up to coverage, and we keep it inside `coverage(·)`."

**Problem**: The load-bearing content of this paragraph is three facts — (a) F1 is satisfiable (the endset is its own witness), (b) the result is determinate up to coverage, so `coverage(followlink(…))` is well-defined as a single term, and (c) in the `⊥` and `⟨⟩` cases the result is single-valued. Wrapped around that core is meta-prose about the document's own notational hygiene: a use-site inventory enumerating downstream consumers ("in F7 and in the worked instance," "(used at F7)"), and convention-bookkeeping ("we keep it inside `coverage(·)`"). This is the "definition's introduction enumerates downstream consumers" and "multiple paragraphs defer to the same downstream location" pattern — a reader chasing the actual claim has to skip past it.

**Required**: Trim to the three load-bearing facts. State that `followlink` is determinate up to coverage (so `coverage(followlink(…))` is well-typed), and that it is single-valued at `⊥` and at `⟨⟩`. Drop the enumeration of which later sections use bare equality and the "we keep it inside `coverage(·)`" convention-prose — the bare-equality uses in F7 and the worked instance are self-evidently licensed where they occur and do not need pre-announcing.

### Issue 2: The S2 fact "empty coverage ⟺ ⟨⟩" is derived/cited four times

**ASN-0114** — the same one-line consequence of ASN-0053 S2 (every well-formed span denotes a non-empty set ⟹ `⟨⟩` is the only span-set with empty coverage) appears in four places:

1. "Status of the result," case (ii): "the only span-set with empty coverage is `⟨⟩`; hence `R = ⟨⟩` uniquely."
2. "Status of the result," more-generally sentence: "the equivalence `R = ⟨⟩ ⟺ coverage(R) = ∅` that S2 supplies."
3. F2 proof, first step: "`⟨⟩` is the only span-set with empty coverage (ASN-0053, S2)."
4. F7, "First collapse": "the empty span-set `⟨⟩` is the *only* span-set whose coverage is `∅` — equivalently `R = ⟨⟩ ⟺ coverage(R) = ∅`."

**Problem**: "Two paragraphs in the same document say the same thing in different words" — here, four. F7 names it the "first collapse" and derives it properly, but F2's proof and the Status paragraph each re-invoke it (with slightly different phrasings, and F2 attributes it directly to S2 though it is a one-step consequence of S2, not S2 verbatim). The fact is load-bearing in three claims (F2, F7, the empty-end case), so it deserves a single statement, not three re-derivations.

**Required**: State the equivalence `R = ⟨⟩ ⟺ coverage(R) = ∅` once — naming it as F7's "first collapse" or stating it where `coverage(R)` is first extended to span-sets — and reference that single statement from F2 and the empty-end case. The endset-side companion (`coverage(eᵢ) = ∅ ⟺ eᵢ = ∅`, the "second collapse") can sit beside it.

## OUT_OF_SCOPE

(none) — the note draws its own boundaries well. The "boundary we must respect" section correctly separates FOLLOWLINK (the recorded end) from resolution against a document's arrangement (V-position projection, shrinkage, per-document divergence), and disclaims the latter rather than specifying it; the Open Questions defer normal-form, resolution-shrinkage, and serialization-encoding concerns appropriately.

VERDICT: REVISE
