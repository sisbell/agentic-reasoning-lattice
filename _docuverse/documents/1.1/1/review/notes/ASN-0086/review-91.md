# Review of ASN-0086

The relational layer's core mathematics is sound. I checked R0a's two-case antichain argument, R0a-Cor2's zero-position-stability induction, R1's disjoint-union well-definedness, the WP Case 2 three-regime analysis, and the Worked Sketch's concrete tumbler arithmetic (e.g. `inc(a₁,0)=1.0.1.0.1.0.2.2`, `coverage({(a₁,δ(1,8))})={t:a₁≼t}` excluding `b₁`) — all hold. My findings are confined to the `review-mode.anti-bloat` mandate: accumulated meta-prose and use-site recaps that the precise reader must skip past.

## REVISE

### Issue 1: R6c Consequence (d) recaps the Worked Sketch mid-consequence
**ASN-0086, R6c Consequences (d)**: "The Worked Sketch exhibits both directions concretely: `A_K^{Σ_0} = {(a₁, F₁, G₁)}` shrinks to `A_K^{Σ_1} = ∅` under Step 1's Nullify, and grows to `A_K^{Σ_2} = {(a₂, F₁, G₁)}` under Step 2's re-emission."
**Problem**: The non-monotonicity claim is already fully established by the two sentences preceding this one (the set-difference witness from R6c plus R0's fresh-address guarantee). The Worked-Sketch recap is downstream worked-example content relocated into a consequence bullet — a use-site inventory that advances no reasoning. It also forward-references the Worked Sketch, which itself already exhibits these states.
**Required**: Delete the recap sentence; the preceding R6c/R0 argument carries the consequence on its own.

### Issue 2: Observe_K "Rationale for the match relation" is why-not-what essay
**ASN-0086, Definition — Observe_K**: "`F̂ ⊆ coverage(F)` is the *minimal* substrate-level match relation, in two senses. First, every substrate computes `coverage(·)` ... Second, the relation answers the canonical substrate-level question ..."
**Problem**: This sub-paragraph justifies *why* the match relation is the right design choice rather than stating *what* Observe computes. The definitional content (the match relation and its decidability) is already given in the signature and the "Pattern domain" paragraph; the "minimal in two senses" essay is the design-rationale form the anti-bloat classifier flags ("new prose ... explains why ... rather than what it says").
**Required**: Cut to one sentence stating that the match relation is `F̂ ⊆ coverage(F)` and is decidable; drop the two-senses justification.

### Issue 3: Boilerplate "unconditional under ASN-0093's K.λ contract" repeated as a per-site reminder
**ASN-0086, R0a / Nullify / WP Case 1 / WP Case 2**: "R0a's antichain on `dom(Σ'.L)` (unconditional under ASN-0093's K.λ contract)" and variants.
**Problem**: R0a's unconditionality is established once at R0a's statement. The parenthetical reappears at each consumer (Nullify single-tuple scope, WP Case 1, WP Case 2 regime (i)). Each restatement re-litigates a settled fact at the point of use — the multiple-deferral-to-the-same-fact pattern.
**Required**: State unconditionality at R0a; cite "by R0a" at consumers without re-attaching the rationale.

### Issue 4: Properties Introduced table — "Status" column is uniformly "introduced"
**ASN-0086, Properties Introduced table**: every row's Status entry is "introduced".
**Problem**: A column whose every cell is identical conveys nothing; it is structural noise the reader scans and discards.
**Required**: Drop the Status column (every property in this note is introduced by definition of the table's purpose), or fold the distinction that matters (DEF vs LEMMA vs OP vs COMMITMENT) into the existing Type column, which already carries it.

## OUT_OF_SCOPE

### Topic 1: Whether L1b should be tightened to `#E = 2` at the substrate
**Why out of scope**: R0a-Cor2 already establishes `#E = 2` within this note; whether ASN-0093/0043's L1b admission should be narrowed at its source is a revision to those ASNs, not to ASN-0086. The Open Question correctly parks it.

### Topic 2: Elevating the unit-depth retraction discipline to a substrate K-operation
**Why out of scope**: Introducing a dedicated retraction primitive with a shape constraint is a change to the K-operation vocabulary (ASN-0093 territory), not a correction to this layering note. The note correctly treats it as a layer convention and flags the tradeoff in Open Questions.

VERDICT: REVISE
