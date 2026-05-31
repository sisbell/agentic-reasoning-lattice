# Review of ASN-0043

The proof apparatus (CPP, FSP, FSE, L1c chain reconstruction, the six-step worked example) is sound. I checked the chain constructions in L1c, FSE, and L9 Cases A/B against TA5/TA5a/T10a zero-count arithmetic, the CPP applications in both `s = home(a)` and FSE, and the coverage arithmetic in worked-example Steps 4–6 — all hold. The remaining issues are residual meta-prose, consistent with the `review-mode.anti-bloat` signal.

## REVISE

### Issue 1: "Summary of the Link Model" is non-advancing recap
**ASN-0043, "Summary of the Link Model"**: "A link is an addressed, owned, typed, bidirectional connection between arbitrary spans of content in the tumbler space. The address *is* the link's identity, and home is determined by that address alone, independent of the endsets ... Classification is likewise decoupled from content: the type endset is matched by address coverage, never by dereferencing the address ..."
**Problem**: This paragraph restates L0/L1 (addressed), L2 (home from address alone), and L8/L9 (type-by-coverage, ghost types) in prose, introducing no claim, derivation, or example. It is essay content the precise reader skips to reach the worked example — exactly the "prose that does not advance reasoning" the anti-bloat classifier targets.
**Required**: Delete the section, or replace with a one-line pointer to the Properties Introduced table.

### Issue 2: L13 opens with scope-demarcation rather than its claim
**ASN-0043, L13 — ReflexiveAddressing**: "That link addresses are admissible endset-span targets is already given by L4(c) (cross-subspace endsets); L13's content is the canonical span for such a reference and the compound structures it composes into."
**Problem**: The sentence explains the boundary between L13 and L4(c) — telling the reader what L13 does *not* re-derive — before stating what L13 *does*. This is the "explaining the relationship to another claim" pattern; the actual content (the canonical span identity) follows in the next sentence and stands on its own.
**Required**: Open L13 directly with the canonical-span identity; if the L4(c) relationship must be noted, compress to a parenthetical citation on the existing "admissible target" sentence.

### Issue 3: `.type` = slot 3 re-justified at each use site
**ASN-0043, Worked Example Step 3 (L8 check)**: "the `.type` accessor resolves to slot 3 unambiguously under the StandardTriple convention extended to arity 4 by L3."
**Problem**: The accessor is *defined* in StandardTriple ("`Σ.L(a).type ≡ Σ.L(a).e₃`"), re-noted in L8 ("denotes slot 3 (the named accessor introduced above)"), then re-justified again here. Three statements of one definitional fact. The arity-4 re-justification adds nothing — L3 already fixes slot 3 uniformly for every `N ≥ 3`, established before the worked example.
**Required**: State the accessor once at definition; drop the L8 and worked-example re-explanations, citing `.type` directly.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace constant (s_C-residence scoping of L14/L14a)
**Why out of scope**: L14's disjointness and L14a's non-transcludability are scoped to the `s_C`-resident slice of content, not all of `dom(Σ.C)`. This is already correctly recorded as the first Open Question; extending disjointness to all content requires a new content-side invariant, which is future-ASN territory, not a defect here.

VERDICT: REVISE
