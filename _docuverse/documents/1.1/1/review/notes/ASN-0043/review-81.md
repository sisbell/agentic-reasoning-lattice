# Review of ASN-0043

## REVISE

### Issue 1: L14a stated unconditionally but derived only under s_C-residence

**ASN-0043, L14a (NonTranscludability) and its derivation**: The invariant is stated unconditionally —
`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∉ dom(Σ.L))` — yet the derivation reads: "S3 together with L0+L0a satisfies L14a **in the s_C-resident regime**: S3 requires `Σ.M(d)(v) ∈ dom(Σ.C)`, and L0+L0a establish `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`."

**Problem**: S3 only gives `Σ.M(d)(v) ∈ dom(Σ.C)`, not membership in the s_C slice. L0a's disjointness covers only `dom(Σ.C)|_{s_C}`. If a content address is non-s_C-resident (which the ASN explicitly admits is possible — see L0a's rationale and the first Open Question), the argument does not exclude it from `dom(Σ.L)`, so the unconditional L14a is unproven for those addresses. This is internally inconsistent with L14 itself, which in the same section carefully scopes disjointness to `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`.

**Required**: Either carry the s_C-residence hypothesis into the L14a statement (matching L14 and L0a), or strengthen the proof to establish full `dom(Σ.C) ∩ dom(Σ.L) = ∅` independently (e.g., via GlobalUniqueness on distinct content vs. link allocation events) rather than via subspace separation alone.

### Issue 2: Triplicated "T4b projections well-defined on link addresses" discharge

**ASN-0043, L1a / LinkHome definition / Home-and-Ownership opening**: The same discharge — "by L1c's T4-validity postcondition together with L1's `zeros(a) = 3`, T4b's projections `N(a), U(a), D(a)` are well-defined" — is written three times in adjacent passages:
- L1a: "By L1c's T4-validity postcondition (below), every link address is T4-valid, so T4b's projections … are well-defined…"
- LinkHome def: "by L1c's T4-validity postcondition link addresses are T4-valid; L1 establishes `zeros(a) = 3` … therefore T4b's projections N, U, D are well-defined"
- Home/Ownership opening: "by L1c's T4-validity postcondition together with L1's `zeros(a) = 3`, T4b's projections … are well-defined on every link address."

**Problem**: Same claim, same premises, three near-identical statements within one page — meta-prose the reader must re-skip. Matches the flagged "two paragraphs say the same thing in different words" pattern.

**Required**: State the well-definedness discharge once (e.g., at LinkHome) and reference it; delete the repetitions.

### Issue 3: Duplicated content-address T4-validity discharge (L0a / L9)

**ASN-0043, L0a and L9 witness**: L0a — "for `b ∈ dom(Σ.C)`, by S7b's postcondition that T4b's projections … are well-defined, combined with T4b's definitional domain (UniqueParse) being precisely the T4-valid subset of T — so any `b ∈ dom(Σ.C)` … is T4-valid." L9 repeats: "T4-validity of `b ∈ dom(Σ.C)` follows from S7b's well-definedness of T4b's projections on `b` together with T4b's domain … being the T4-valid subset of T."

**Problem**: The identical S7b+T4b-domain argument appears verbatim in two sections.

**Required**: Establish content-address T4-validity once and cite it.

### Issue 4: PrefixSpanCoverage axiom wrapped in placement/rationale meta-prose

**ASN-0043, PrefixSpanCoverage axiom**: "This identity is a property of spans and tumblers, with no link-specific content: it speaks only of `coverage`, `δ`, `shift`, and `≼`, all defined in ASN-0034 … It is a span/tumbler-algebra fact, adopted here as an axiom pending a span-algebra ASN." Plus the parenthetical "(note `x ⊕ δ(1, #x) = shift(x, 1)` … — a supporting identity, not an equivalent form)".

**Problem**: This prose explains *why the axiom is placed here* and *why it is an axiom* rather than advancing what it states — matching the flagged patterns "new prose around an axiom explains why the axiom is needed rather than what it says" and document-ordering justification. The "— a supporting identity, not an equivalent form" hedge is defensive noise.

**Required**: Keep the axiom statement and the coverage equation; drop the provenance/placement commentary (the Open Questions already record the pending span-algebra ASN).

## OUT_OF_SCOPE

None — the future-territory items are already correctly parked in Open Questions.

VERDICT: REVISE
