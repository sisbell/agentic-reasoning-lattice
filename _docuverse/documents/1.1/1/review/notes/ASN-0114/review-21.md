# Review of ASN-0114

## REVISE

### Issue 1: The "each ⟸ / each ⟹" attribution is reversed for the first collapse

**ASN-0114, "The substrate we build on"**: "For a span-set `R` this is the *first collapse*, `R = ⟨⟩ ⟺ coverage(R) = ∅`; for an endset `e` it is the *second collapse*, `coverage(e) = ∅ ⟺ e = ∅`. Each `⟸` is immediate — the empty object covers nothing — and each `⟹` is the contrapositive of S2."

**Problem**: The two collapses are written in **opposite operand orders**, so a single uniform "each ⟸ … each ⟹ …" attribution cannot hold for both. Reading the arrows against the biconditionals as literally written:

- *Second collapse* `coverage(e) = ∅ ⟺ e = ∅` (A = `coverage(e)=∅`, B = `e=∅`):
  - `⟹` (A⟹B): `coverage(e)=∅ ⟹ e=∅` — the S2 contrapositive. ✓ matches the text.
  - `⟸` (B⟹A): `e=∅ ⟹ coverage(e)=∅` — empty covers nothing. ✓ matches the text.
- *First collapse* `R = ⟨⟩ ⟺ coverage(R) = ∅` (A = `R=⟨⟩`, B = `coverage(R)=∅`):
  - `⟹` (A⟹B): `R=⟨⟩ ⟹ coverage(R)=∅` — empty covers nothing, the *immediate* one.
  - `⟸` (B⟹A): `coverage(R)=∅ ⟹ R=⟨⟩` — the S2 *contrapositive*.

So for the first collapse the immediate direction is `⟹` and the S2-contrapositive is `⟸` — exactly the reverse of what the sentence asserts. The word "Each" makes a false uniform claim. (Both underlying implications are true, and the collapses are *applied* correctly later — e.g. F2's "`coverage(R) ≠ ∅` … forces `R ≠ ⟨⟩` by the first collapse" — so this is a defect in the justification prose, not a propagating error.)

**Required**: Write both collapses in the same orientation (e.g. both as "object empty ⟺ coverage empty," giving `R = ⟨⟩ ⟺ coverage(R) = ∅` and `e = ∅ ⟺ coverage(e) = ∅`), after which "each ⟸ is immediate … each ⟹ is the contrapositive of S2" becomes uniformly true; or attribute the two directions per-collapse rather than with "each."

### Issue 2: Mid-document corollary roadmap is forward-reference meta-prose, duplicated by the Synthesis

**ASN-0114, "The selector and its domain"**: "Three independent commitments remain — F1, F4, F7 — which we take in turn; the remaining properties F2, F3, F5, F6, and F8 emerge alongside them as corollaries, each traced to its source as it is derived below."

**Problem**: This sentence advances no reasoning — it is a structural roadmap (a use-site inventory of which claims arrive later) capped by pure meta-prose about the derivations ("each traced to its source as it is derived below," which merely says a proof will cite its premises). The same primary/corollary partition is stated again, *more informatively*, in the Synthesis: "under three primary commitments — F1, F4, F7 — atop the F0 definedness precondition, with F2, F3, F5, F6, and F8 following as corollaries (F2, F3, F6 from F1; F5 from F1 and link immutability; F8 from F0 and F1)." The Synthesis version carries the actual dependency chains; the mid-document roadmap carries only the enumeration. Under the anti-bloat pass this is the kind of forward-reference inventory that compounds across cycles.

**Required**: Delete the mid-document roadmap sentence (the Synthesis already records the corollary structure with its derivations); or, if a one-line signpost is wanted, drop at minimum the "each traced to its source as it is derived below" clause. The companion forward reference in "The substrate we build on" ("Two consequences of ASN-0053's S2 … recur below, so we name them here") can be trimmed to just stating the two consequences.

## OUT_OF_SCOPE

None to add. The note scopes itself cleanly: resolution of the recorded endset against a particular document's arrangement (the shrinkage/per-document variation of Q11/Q15/Q20) is correctly excluded in "A boundary we must respect" and attributed to *resolution* rather than FOLLOWLINK, and no F-claim strays into that territory. The remaining genuinely-future questions (normal form for the returned span-set, serialization-boundary encoding of `⟨⟩`/`⊥`, multi-document coverage reporting) are already logged under Open Questions.

VERDICT: REVISE
