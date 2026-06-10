# Review of ASN-0127

This is a strong, carefully-constructed foundation algebra. The two-phase factoring is clean, every lemma carries an explicit derivation (no proof-by-"similarly" — even F-IMG-CONTR, flagged "symmetric," shows the full argument), the boundary cases (empty region, fresh document with empty arrangement, `findlinks(∅)`, full contraction) are handled by the proofs rather than waved through, and D-CWP supplies a genuinely non-trivial weakest precondition. The worked illustration grounds the load-bearing claims concretely, and the injective-`K.μ~` regime correctly resists the fallacy "incomparable image ⟹ incomparable discovery." Cross-references are all to foundation ASNs (0034/0036/0043/0047/0058/0093/0098); `image`/`findlinks`/`matches` are genuinely new primitives, not reinventions of ASN-0098's `project`/`discoverable_from`.

I verified the witnesses arithmetically (F-IMG-SWING injective and non-injective; the lateral and cardinality-changing swings in the worked illustration), the F-INERT bridges in every D-NONMONO clause, the E-CONS exclusion direction, and the D-CWP `A = A ∪ B ⟺ B ⊆ A` algebra. All check out. One precision issue remains.

## REVISE

### Issue 1: An endset is attributed to an address

**ASN-0127, Operational consequences → Anchoring → Discovery anchoring → D-NONMONO, K.μ~ clause (injective regime)**: "dually, a swapped-in address whose endset also covers the swapped-out one (so that link survives) while matching a further link grows the set `{L_1} ↦ {L_1, L_2}`."

**Problem**: The subject "a swapped-in address" is the I-address now in the image (the `a₁ → a₂` motion of an injective reorder); "whose endset" then attributes an endset to that I-address. Endsets belong to links (`Σ.L(a).eᵢ`), never to the content/link I-addresses that projection targets. Under `K.μ~`, `Σ.L` is fixed (F-PRES) — no link is swapped — so there is no address-owned endset in play. The whole point being illustrated is that a *link* `L_1` survives because *its* endset covers both `a₂` (the new image member) and `a₁` (the displaced one). In an ASN this meticulous about writing `coverage(Σ.L(a).eᵢ)` everywhere else, the slip stands out, and it sits in the single most subtle, most-recently-revised passage — exactly where imprecision costs the most.

**Required**: Re-attribute the endset/coverage to the link. The precise phrasing already exists in this ASN's own worked illustration (cardinality-changing variant: "Admit one further link `L_2' = ({a_2}, ∅, Θ)` … both links reaching `a₂` fire"). Mirror it, e.g.: "dually, when a *matched link's* endset covers the swapped-in address as well as the swapped-out one (so that link survives), and the swapped-in address additionally matches a further link, the set grows `{L_1} ↦ {L_1, L_2}`." (The companion clause's "the swapped-in address witnesses no link" is fine — "address witnesses link" is a clear `a ∈ coverage` shorthand; only "address whose endset" needs the fix.)

## OUT_OF_SCOPE

The four Open Questions (content-keyed query through `Σ.C`; filter-set constraints on F-UDIST; the uniform-transition wp of which D-CWP is the `K.μ⁻` instance; composition with ASN-0098's link projection) are correctly deferred — each is new territory, not a gap in this note's stated scope. I have no additional out-of-scope topics to raise. In particular, multi-document content regions are already expressible by unioning per-document images and feeding the result to the global `findlinks` (F-UDIST), so they are not a missing case.

VERDICT: REVISE
