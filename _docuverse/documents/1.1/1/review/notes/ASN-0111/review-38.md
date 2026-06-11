# Review of ASN-0111

The core specification is sound: the definition is honest, RL0–RL6 are correctly derived from it, the RL4 branched-history witness is constructed carefully and checks out step by step (frontier determinism, branch-independent enabledness, identical allocation of `c`, the `v₁ ≠ v₂` separation), and the worked example's tumbler arithmetic — the interval decomposition `[…1.1, …1.3) = subtree(…1.1) ∪ subtree(…1.2)`, the field projections, the chain addresses — is all verified correct. Two wording-level defects remain, one of which puts a false universal into the claims table.

## REVISE

### Issue 1: Endsets called "span-sets" — a foundation term with different semantics

**ASN-0111, "The link as a readable object"**: "The relationship a link records is therefore not a pair of points but a triple of *span-sets*, each reaching — possibly discontiguously — anywhere in the docuverse. The address-set a span-set denotes is its `coverage` (ASN-0043)."

**Problem**: "Span-set" is a defined foundation term (ASN-0053, SpanSet): a finite *sequence* `⟨σ₁, ..., σₙ⟩` of spans, with positional structure and its own denotation operator `⟦·⟧`. The object being described here is an *endset* (ASN-0043): a finite *set*, `Endset = 𝒫_fin(Span)`, which by L5 has no positional accessor at all. The conflation is not harmless prose: this ASN itself later leans on exactly that distinction — the RL1 corollary cites L5 ("the read exposes membership, not sequence"). A reader directed by this sentence to ASN-0053's span-set machinery (normalization, N1/N2 ordering) would be importing structure that L5 says endsets do not have. Additionally, `coverage` is defined on endsets (ASN-0043), not on ASN-0053 span-sets, so the second sentence attributes a foundation operator to the wrong carrier while citing the foundation.

**Required**: Use the foundation's own term: "a triple of endsets" and "The address-set an endset denotes is its `coverage` (ASN-0043)." If the discontiguity point is wanted, say "each endset a finite set of spans" — no appeal to ASN-0053's term is needed.

### Issue 2: "No address-computable predicate is sufficient" is false without the satisfiability qualifier

**ASN-0111, "Deriving the read", RL0 section, and Claims table**: "no predicate computable from the address alone is sufficient for membership in `dom(Σ.L)`"; "*No address-computable predicate is sufficient* — at the initial state Σ₀ ..."; table entry for RL0: "no address-computable predicate is sufficient (witness: `dom(Σ₀.L) = ∅`)".

**Problem**: As universally quantified statements these are false: an unsatisfiable address-only predicate (e.g. `λa. a ≠ a`) is vacuously sufficient for membership in `dom(Σ.L)`. The proof in the RL0 section is correct precisely because it restricts itself — "any *satisfiable* address-only predicate has a witness `a` with `a ∉ dom(Σ₀.L)`" — but the bolded headline, the earlier derivation-section sentence, and the claims-table entry all drop the qualifier. The claims table is the normative summary that gets extracted and consumed downstream; it must not assert a universal whose repair lives only in body prose.

**Required**: Insert the qualifier at all three sites: "no *satisfiable* address-computable predicate is sufficient" (or equivalent phrasing such as "no address-computable predicate with a witness"). One word; the proof already establishes exactly the qualified claim.

## OUT_OF_SCOPE

None. The note stays inside the direct-read boundary: traversal, search, and counting are distinguished but not specified, and the Open Questions correctly defer the FOLLOWLINK-distinguishability and validity-inference questions to future ASNs rather than answering them here.

VERDICT: REVISE
