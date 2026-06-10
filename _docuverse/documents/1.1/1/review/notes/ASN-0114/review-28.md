# Review of ASN-0114

I checked each claim against its stated derivation, the foundation contracts, and the worked example's arithmetic. The formal content holds up; the items below record what I verified rather than defects.

## REVISE

None.

The following were checked in detail and are sound:

- **The two collapses** (substrate). `coverage(R) = ∅ ⟺ R = ⟨⟩` and `coverage(e) = ∅ ⟺ e = ∅` are both discharged correctly from ASN-0053 S2 — each `⟸` is immediate, each `⟹` is the contrapositive of "every well-formed span denotes a non-empty set." The reuse of these names in F2, F7, and the worked example is load-bearing, not filler.

- **F0/F2/F5/F6/F7 derivations.** F2's `|R| ≥ 2` argument is complete in both halves: `R ≠ ⟨⟩` via the first collapse + F1, and `|R| ≠ 1` via span convexity (S0) forcing the gap point `q` into `⟦σ⟧`. F5 names LP13 and shows the chain `Σ'.L(a).eᵢ = Σ.L(a).eᵢ`. F7's `wp(R = ⟨⟩) ≡ domain ∧ eᵢ = ∅` correctly composes F1 with both collapses, and the `wp(result = ⊥)` line is not redundant padding — it is the third cell of the outcome partition (⊥ / ⟨⟩ / non-empty) that F7's empty-versus-invalid distinction requires.

- **F6 disclosure bounding.** The home-document disclosure is correctly restricted to the T4-valid, document-bearing slice (`zeros(t) ≥ 2`), with explicit acknowledgement that L4/L9 permit covered addresses at node/user level or non-T4-valid interior tumblers on which the projections are undefined. The "representation may leak `eⱼ`" caveat honestly marks F6 as a coverage-level guarantee only, not a representation-level one — no overclaim.

- **Worked example.** The tumbler arithmetic verifies: `a₃ = [1,0,1,0,5,0,1,3]`, `δ(2,8)` has action point `8 ≤ #a₃`, `a₃ ⊕ δ(2,8) = a₅`; `F ∩ [a₃, a₅) = {a₃, a₄}` by LP-Fin Corollary; the disconnection witness `p=a₃ < q=a₅ < r=a₇` with `a₅ ∉ coverage(e₁)` is correct (half-open exclusion of `a₅` plus `a₅ < a₇`). F2 and F7 are both genuinely discharged against this instance.

- **Self-containment.** Every cross-reference (ASN-0034, 0036, 0043, 0047, 0053, 0093, 0098) is to a foundation ASN. No out-of-scope operation is given a claim — the "boundary" section excludes endset resolution rather than specifying it.

## OUT_OF_SCOPE

The ASN's own Open Questions correctly defer normal-form selection, endset-to-V-position resolution, the serialization encoding of `⟨⟩`/`⊥`, and multi-document coverage reporting. These are appropriately marked as future territory, not gaps in this note.

META: not warranted — the note defines an operation (FOLLOWLINK) with abstract postconditions (F1, F4, F7) and invariants stated so any faithful implementation must satisfy them; the implementation evidence is used to corroborate and to expose F7 as an obligation one real implementation fails, not to specify mechanics.

VERDICT: CONVERGED
