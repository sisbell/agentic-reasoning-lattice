# Review of ASN-0108

The mathematics is sound. I checked every claim W0–W11: the wp analysis in W2 (the three nested offset preconditions and the past-the-end corner), the rank-block induction of W4 under variable schedules, the cut-point/tail-order split of W5 with all three walks (cut-point skip, harmless tail reorder, cancelling clause-1 failures), the W6a bridge from `findlinks_V` to F-LAMBDA, the charge-injectivity argument of W9b, and the W9a count formula against all four termination walks. All hold, with honest boundary coverage (`m = 0`, exact multiple, `N > m`, orphaned cursor) and a correctly acyclic W5↔W9b dependency (no-re-delivery is unconditional; no-skip and termination compose). The note specifies an operation's abstract contract, not implementation mechanics — no drift.

Two findings, one a precision defect in recurring framing, one anti-bloat.

## REVISE

### Issue 1: "least-covered-I-address key" mislabels what the key actually reads, and omits the tiebreaker it requires
**ASN-0108, The Enumeration Order (Gregory's reading)**: "orders each link by the least I-address that slice covers" and "Requiring the slice to include the type slot discharges the proviso structurally: `e₃ ≠ ∅` (L3) and a non-empty endset has non-empty coverage [...], so a type-including slice covers at least one **I-address** on every link in `dom(Σ.L)`".

**Problem**: The two facts collide. From- and to-endsets may be empty — `Endset = 𝒫_fin(Span)` admits `∅`, and L3 (ASN-0043) constrains only `e₃ ≠ ∅`, leaving `e₁, e₂` unconstrained. So a from- or to-only slice is *not* total on `Match` (a link with empty from-endset has `coverage = ∅`, key undefined). The note's own totality fix — include the type slot — is therefore load-bearing, not optional. But for a link with empty from/to, the designated slice's coverage *is* `coverage(e₃)`, whose addresses are type classifiers, ghost-permitted (L9, ASN-0043) and outside `dom(Σ.C)` — i.e. not I-addresses at all. The totality argument's "covers at least one I-address" is then false; the covered address is a type-classifier tumbler. This propagates into the key's *semantics* everywhere it is described: "their place governed by **which content they point at**" (Enumeration Order), "reads permanent **content identity**, which a `K.μ~` rearrangement does not touch" (W5), "the least covered I-address of its designated endset slice" (W8). For links keyed off their type slot, the key reflects type-classifier identity, not content the link points at.

Separately, the key is named for its primary component alone while the note states it is non-injective and *must* carry a tiebreaker: "the bare content key is not injective on `Match` [...] it must be composed with a permanent tiebreaker — `κ(a) = (endpoint-boundary, a)`". W1 (position-uniqueness) holds only for the composite, yet W5/W6/W8 invoke "the least-covered-I-address key" by that bare name. The blanket "We carry any content key only in this composite form" licenses the math but the name elides the mandatory low-order address component.

**Required**: Rename/restate the key as the least covered *tumbler* (not I-address) of the designated slice — noting it is a type-classifier address precisely when from/to are empty — and either fold the permanent address tiebreaker into the name/definition or state once that "least-covered-X key" abbreviates the composite `(least covered tumbler, link address)`. Correct "covers at least one I-address" to "covers at least one address." (None of the W0–W11 claims depend on the content framing — they need only total + injective + permanent — so this is a precision repair to illustrative prose, not a proof gap.)

### Issue 2: Gregory's-key permanence asserted three ways in one bullet (anti-bloat)
**ASN-0108, The Enumeration Order (Gregory's reading)**: "(a) This key is permanent, by L12 alone: it is the T1-least address in coverage of the designated slice; coverage is a purely combinatorial function [...]; and the slice's endsets are immutable once written (L12). (b) **The key is therefore a pure function of an immutable value — frozen under every transition, with no appeal to where content sits or whether it persists.** (c) A `K.μ~` reorder and a `K.μ⁻` deletion alike leave `Σ.L` [...] untouched; in particular the key value is unmoved by orphaning [...]."

**Problem**: Sentence (a) is the argument; sentence (c) instantiates it to the `K.μ~`/`K.μ⁻`/orphaning case that W8 later consumes. Sentence (b) restates (a)'s conclusion ("permanent" → "pure function of an immutable value, frozen under every transition") without an intervening step. This is the accretion the `review-mode.anti-bloat` classifier targets — the same fact in different words, between the argument and the instance that uses it. (The trailing hook "with no appeal to where content sits or whether it persists" previews the content-position contrast and could be relocated to where that contrast is actually drawn.)

**Required**: Drop (b); the permanence is carried by (a) and reused by name in W5/W8 ("established above").

## OUT_OF_SCOPE

None beyond the ASN's own Open Questions. The multi-home-document enumeration (no global allocation-monotone key), the non-allocation-monotone delivery guarantee, the cross-call matching-set relation, the uncomputable-cursor protocol, and the delivery-vs-sizing correspondence are correctly deferred. The note also properly defers count-only retrieval, full-set retrieval, MAKELINK, FOLLOWLINK, and BEBE.

VERDICT: REVISE
