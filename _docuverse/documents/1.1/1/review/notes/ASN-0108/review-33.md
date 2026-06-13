# Review of ASN-0108

The mathematics here is sound. I checked the weakest-precondition algebra in W2 (the three-way nesting membership-identity ⟹ frozen-prefix ⟹ `j'=j ∨ (j≥m' ∧ j'≥m')`, and the empty-window corner that witnesses the strictness), the rank-block induction in W4, the F-V/F-LAMBDA bridge in W6a, the multiplicity-charge termination argument in W9b, and the count formula in W9a against all four boundary walks (`m=4`, `m=5`, `m=0`, `N>m`). They hold. The treatment of clause-1-as-non-removable-hypothesis (W9c) versus clause-1-as-not-necessary-for-coherence (W5) is correctly distinguished and free of the contradiction it courts. The concrete walks are real proofs, not decoration, and they cover the edge cases that matter (orphaned cursor, empty set, first-window-short, exact multiple, re-ascension).

The problem is not the reasoning — it is the scaffolding accreted around it. This note carries the anti-bloat classifier, and the forward-reference meta-prose it warns of is present and findable. The findings below are about that accretion plus a few precision slips, not about the proofs.

## REVISE

### Issue 1: Use-site inventories in the key-definition section
**ASN-0108, "The Enumeration Order" → "What κ is, concretely"**: "This section defines the three; the guarantees below — W5, W6, W8 — sort them." And in the content-position foil paragraph: "the walks under W5, W8, and W9c use this content-position key to expose why cut-point preservation and computability-through-disappearance are load-bearing."
**Problem**: Both sentences enumerate downstream consumers of the definitions rather than advancing the definitions' meaning — exactly the "definition's introduction enumerates downstream consumers" pattern. The reader learns nothing about what the three keys *are* from being told which later claims will reference them; the cross-references are recoverable at the use sites (W5, W6, W8 already name their relevant key).
**Required**: Delete the consumer inventories. Let each key's definition stand on its own properties (permanent vs mutable, injective vs needs-tiebreaker); the claims downstream already cite the keys they sort.

### Issue 2: The foil framing is stated twice
**ASN-0108, "The Enumeration Order" → "What κ is, concretely"**: "We carry it only as the cautionary foil: keying on *position* rather than *identity* is precisely what the windowing laws below must guard against…" followed a few lines later by "Links are defined to track permanent content identity, not position … the content-position key is the instructive foil, not the implementation."
**Problem**: Two paragraphs in the same passage make the identical point — the content-position key is a foil, not the implementation. The second restates the first in different words.
**Required**: Keep one. The substantive content (links track identity not position; the bare content key fails W0/W1 injectivity and needs the `(boundary, address)` composite tiebreaker) is worth keeping; the duplicate "this is a foil, not the implementation" sentence is not.

### Issue 3: "Ladder of key conditions" glossary carries forward-reference framing
**ASN-0108, "Stability of the Order Across Evolution"**: "Five conditions on the key recur below; we collect their definitions here as a glossary." … "Which candidate key occupies which rung — and how the two families relate — is the verdict of W5 and W8 below."
**Problem**: The glossary's *definitions* (Computability vs Value-totality vs clause 1 / clause 2 / state-stability) do real work — the Computability/Value-totality split is genuinely load-bearing in W8, where the two permanent keys reach W8 by different routes. But the framing sentences are forward-reference scaffolding: "recur below" and "the verdict of W5 and W8 below" announce that later claims will use these terms, which the later claims demonstrate on their own.
**Required**: Keep the five definitions; drop the "recur below" / "verdict of W5 and W8 below" framing. A glossary needs an introduction stating what it defines, not a manifest of where the terms get used.

### Issue 4: W5 double-signposts the W6 deferral
**ASN-0108, "Stability of the Order Across Evolution" (prose)**: "Both identity keys are therefore state-stable, and W5 does not distinguish them; where they differ is W6's concern, treated there." And the Claims table row for W5: "Both identity keys are state-stable; W5 singles out only the content-position key (how the two identity keys differ is W6's)."
**Problem**: The fact "the two identity keys differ only at W6" is signposted in W5 prose, in the W5 table row, in W6's prose ("This is the one place the two *permanent* keys part"), and in the W6 table row. That is four pointers to one downstream fact — the "multiple paragraphs defer to the same downstream location" pattern. The W5-side deferral and its table parenthetical are redundant with W6 stating the fact itself.
**Required**: Let W6 own the claim. W5 can note that it does not distinguish the two identity keys without also pointing to where they are distinguished; the table parenthetical can be dropped.

### Issue 5: "recoverable" (W2) versus "computable" / "value-total" (W5 glossary, W8) — terminology drift for one concept
**ASN-0108, "The Cursor: Identity, Not Offset"**: "wp(resume_id, R) ≡ κ(c) recoverable" … "recoverable unconditionally, with no state lookup". **W8**: "The load-bearing property is **computability** … *not* value-invariance and *not* state-stability".
**Problem**: W2's identity-cursor weakest precondition is exactly W8's *computability* (κ(c) evaluable against the current set, so After(c,Σ') is well-defined), but W2 names it "recoverable" and glosses it as "with no state lookup" — which is the W5 glossary's *value-totality*, the strictly stronger property that only the address key supplies. The reader meets the wp first under a name the glossary never defines, glossed toward the stronger condition, and then must reconcile it with W8's careful computability/value-totality split. Same concept, two lexicons, with the W2 gloss leaning on the wrong rung of the ladder W5 later builds.
**Required**: State W2's identity-cursor wp as "κ(c) **computable**" (the weakest condition, matching W8 and the glossary), then specialize: under the address key, κ(c)=c is value-total, so computability holds unconditionally with no state lookup. One vocabulary across W2, the W5 glossary, and W8.

### Issue 6: W4's proof smuggles in a variable-schedule generalization and forward-references W11 to license it
**ASN-0108, "No Gap, No Duplicate — Under Stability"**: W4's statement says only "Against a fixed `(M, κ)`, the successive windows … are pairwise disjoint, consecutive in ≺, and their union is all of M, each link appearing exactly once" — no mention of N or a variable schedule. The proof then opens: "We allow the reader to choose a possibly *different* window size N_i ≥ 1 on each call — the flexibility W11 grants".
**Problem**: Two slips compounded. (a) The proof proves a strictly more general result (variable `N_i`) than W4 states, and only the closing remark ("holds for a variable size schedule as much as a fixed one") surfaces it — a substantive guarantee hidden in a proof. (b) The forward reference to W11 is gratuitous: the freedom to pass a different `N` per call is intrinsic to `Window(q, c, N, Σ)`'s signature (N is an argument), not something W11 grants — W11 merely *observes* boundary objectivity for a given N. So a proof of W4 cites a later claim for a permission the operation's own definition already supplies.
**Required**: Either lift the variable-schedule result into W4's statement (it is worth stating), or keep the proof to the fixed-`N` claim it asserts. Drop the W11 citation regardless — the per-call N flexibility follows from `Window`'s arity, and a proof should not lean on a claim defined after it.

## OUT_OF_SCOPE

### Topic 1: Multi-document enumeration discipline; non-monotone-key append guarantee; cross-state completeness invariant; cursor-invalidation-vs-exhaustion distinguisher; delivery/progress-count correspondence
**Why out of scope**: These are the five Open Questions the note already names, and each is a genuine future-ASN topic (W6's multi-home-document blind spot, the LP18 resurrection accounting, the cross-state stitching invariant, the W8/W9 ambiguity resolution, and the W10 companion-query correspondence). The note defers them correctly rather than half-specifying them; this is the right boundary, not a gap in ASN-0108.

VERDICT: REVISE
