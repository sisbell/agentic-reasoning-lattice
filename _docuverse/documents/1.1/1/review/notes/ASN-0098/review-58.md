# Review of ASN-0098

I checked the projection-displacement claims (LP2–LP21), the F-substrate machinery (LP-Sub, LP-Fin, LP12b), the discoverability/wp derivations, and the worked trace. The core reasoning is sound: boundary cases (empty endset, empty arrangement, `R = ∅` contraction, document registration) are handled up front, the LP-Fin interval count is exhaustively case-split, and the worked trace's two branches compute correctly under the bijection equation. The findings below are all prose/forward-reference accretion of the kind this note's `review-mode.anti-bloat` classifier flags — places where the reader works around restated or defensive text to reach the argument.

## REVISE

### Issue 1: LP8 states the document-registration effect twice
**ASN-0098, LP8**: the hypothesis parenthetical reads "registering a fresh document `d_new` (with `d_new ∉ dom(Σ.M)`, `dom(Σ'.M) = dom(Σ.M) ∪ {d_new}`, `Σ'.M(d_new) = ∅`, and `Σ'.M(d) = Σ.M(d)` for every `d ∈ dom(Σ.M)`)"; the verification paragraph then restates the identical content as "it extends `dom(M)` by one fresh document, initialises the new document's arrangement to `∅`, and preserves every pre-existing arrangement pointwise."
**Problem**: Two paragraphs in the same claim say the same thing in different words. The verification sentence's only job is to assert K.δ-Document matches the hypothesis form; once the hypothesis is stated in symbols, re-narrating it in prose advances no reasoning.
**Required**: Drop the prose restatement; cite K.δ's `Document(e)` effect clause as discharging the hypothesis form and proceed directly to the LP4 application for (a) and the empty-domain comprehension for (b).

### Issue 2: "Discovery Independence of Origin" restates one inspection four times
**ASN-0098, Discovery Independence of Origin**: "The discoverability of a link from `d` depends on none of them — only on the I-address content of `d`'s arrangement. This is visible by inspection of LP12: the right-hand side references `coverage(...)` and `ran(...)` and nothing else. The characterisation contains no reference to `home(a)` or to the origin documents of coverage I-addresses. The home document is a metadata property of the link's address ... Similarly, origin is a metadata property of each coverage I-address ... so discovery is indifferent to provenance."
**Problem**: This is the single observation "LP12's RHS mentions only coverage and range" expanded into four sentences (home-independence, origin-independence, metadata-property, provenance-indifference), none carrying a formal claim. It is essay content occupying the slot before LP16 where a one-line corollary of LP12 would suffice.
**Required**: Collapse to one sentence stating the corollary of LP12 (discoverability references only `coverage(Σ.L(a).eᵢ)` and `ran(Σ.M(d))`, hence is independent of `home(a)` and of each coverage address's origin), then proceed to LP16.

### Issue 3: `tight` definition carries defensive justification rather than stating the predicate
**ASN-0098, tight definition**: "The canonical-span requirement is *definitional*: a non-canonical span is fixed at false before any quantifier evaluation, so no state can render it tight. ... Tightness is a state-relative predicate; in the canonical use case `Σ_e` is the state at which `e` was incorporated into a link, but the predicate is well-defined at any state."
**Problem**: The first sentence defends *why* the definition is shaped this way ("definitional," "fixed at false before any quantifier evaluation"); the last sentence narrates the intended use site. Neither advances the predicate's meaning. The load-bearing content (LP-Sub + LP-Fin confine the universal quantifier to a finite set, so the predicate is decidable) is the only part that belongs.
**Required**: Keep the decidability sentence (the `s ∈ F` / LP-Fin reduction). Remove the "definitional"/"fixed at false" defense and the "state-relative predicate / canonical use case" usage narration.

## OUT_OF_SCOPE

(none — the Open Questions correctly defer reverse-discovery, V-order preservation, cross-document operation equivalence, and link-to-link discovery to future ASNs; none is improperly claimed here.)

VERDICT: REVISE
