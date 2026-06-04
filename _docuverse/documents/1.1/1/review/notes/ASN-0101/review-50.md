# Review of ASN-0101

## REVISE

### Issue 1: D3's discoverability discussion duplicates D9
**ASN-0101, D3 ("Link store: the link graph is untouched")**: "We can be sharper about what D3 entails. ... What changes is *discoverability* ... the projection ... depends on `M(d)`. After DELETE, the projection can lose elements: V-positions in `X` ... are removed ... V-positions in `Π` are renamed by `σ_d` ... V-positions in `Λ` are unchanged. ... Its discoverability from `d` may shrink. Its discoverability from other documents `d' ≠ d` is unchanged ..."

**Problem**: This is the substance of D9 (the per-document, per-subspace projection characterisation: `Λ` unchanged, `Π` renamed by `σ_d`, `X` removed, other documents invariant) and of the "Link discoverability: the projection picture" intro, restated in prose. D3's own task is link-store immutability (`dom(L') = dom(L)`, value preservation); the discoverability sketch belongs to D9, where it is formalised. The same coverage-unchanged/discoverability-shrinks-or-renames point is then made a third time in the "Link discoverability" section opener ("link values are unchanged, coverage is unchanged, only the projection ... is altered"). Three passages in three sections say the same thing.

**Required**: Reduce D3 to its actual content — link-store immutability and the single derived fact that `coverage(L'(ℓ).eᵢ) = coverage(L(ℓ).eᵢ)` — and let D9 carry the projection/discoverability characterisation without anticipatory restatement.

### Issue 2: D9 Frame-note sentence is scope-justifying meta-prose
**ASN-0101, D9 "Frame note"**: "The first bullet's appeal to D5 (`M'(d'') = M(d'')`) is itself conditioned on `d'' ∈ dom(M)` in D5's statement, so the membership restriction is the natural scope of the lemma."

**Problem**: The preceding two sentences already establish what the reader needs — that `project` is defined only for `d ∈ dom(Σ.M)` and that D4 supplies `dom(M') = dom(M)`. This trailing sentence justifies *why the lemma is scoped the way it is* rather than advancing the claim; it explains document choices, not transition facts.

**Required**: Delete the sentence. The well-definedness point is fully made by the two sentences before it.

## OUT_OF_SCOPE

None. The ASN defines no claims for INSERT, COPY, REARRANGE, link semantics, version creation, or BEBE; the implementation-limitation section explicitly disclaims rather than specifies those mechanics.

VERDICT: REVISE
