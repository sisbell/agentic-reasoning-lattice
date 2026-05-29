# Review of ASN-0040

The proofs here are, on the whole, rigorous: the inductions (B0★, B_fin, B1, B10, B9) are complete with explicit base/step, the case analyses (B7, B8) are exhaustive, and the worked trace verifies postconditions against concrete addresses. I found no gaps in the formal arguments. The remaining problems are the meta-prose accretion this note's `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: B4 carries a downstream-consumer inventory and "why-needed" prose
**ASN-0040, B4 (Atomic Baptism)**: "no second baptism in the same namespace can interleave, which would let two acts read the same hwm and compute the same c_{hwm+1}. Atomicity is what forecloses that interleaving; it is the handle B8 and B9 cite."
**Problem**: Two of the flagged patterns at once. "it is the handle B8 and B9 cite" is a use-site inventory — it names downstream consumers rather than advancing what B4 *says*. The preceding sentences explain *why* atomicity is needed (to prevent a hypothetical double-read) rather than stating the property. The object content of B4 is just: each `baptize(p, d)` is one edge of `→`, on which read/compute/commit collapse.
**Required**: Cut the consumer inventory and the interleaving rationale. State the single-edge collapse and stop. B8/B9 cite B4 in their own *Depends* lines; B4 need not announce them.

### Issue 2: B3 wraps its invariant in forward-reference essay prose
**ASN-0040, B3 (Ghost Validity)**: "We record the relationship between baptism and content as a forward requirement on whichever future ASN introduces content storage… Every future ASN introducing Occupied must arrange its operations so that…"
**Problem**: The object content is the invariant `Occupied(t, s) ⟹ t ∈ s.B` plus the three-way taxonomy (populated / ghost / unbaptized). The framing prose about "whichever future ASN" and what future ASNs "must arrange" is forward-reference accretion — it advances no reasoning in this note. This is the kind of meta-prose the anti-bloat pass exists to remove.
**Required**: State the invariant and the permitted-configuration taxonomy directly. Drop the editorializing about future ASNs; the `Occupied` predicate's introduction-as-parameter already signals it is defined elsewhere.

### Issue 3: Worked-example sprawl restates the proofs it illustrates
**ASN-0040, "B9 unbounded extent exhibited" and "B7 illustrated — equal-length parents"**: The B9 subsection re-runs the constructive argument B9's proof already gives (it *is* a construction), now with M = 5 and Steps 5–7. The "equal-length parents" subsection reproduces B7's equal-length-parents case verbatim on [1,0,1]/[1,0,2].
**Problem**: Concrete examples are welcome, but these two restate their own proofs in different words — the "two paragraphs say the same thing" pattern. B9's proof is already constructive, so a second numeric construction adds no verification the proof lacks. (The "nesting prefixes" illustration *is* a genuinely distinct case and earns its place; the other two do not.)
**Required**: Keep one illustrative trace and the nesting-prefix B7 witness. Fold the equal-length B7 illustration and the M = 5 B9 re-derivation back into a single line each, or cut them, since the proofs already carry the construction.

### Issue 4: s.B-vs-allocated(s) disambiguation defers to an open question
**ASN-0040, §The baptismal registry**: "We must situate s.B against the foundation's `allocated(s)`… s.B is a distinct state component…" — while the relationship `allocated(s) ⊆ s.B` is itself deferred to an Open Question.
**Problem**: The disambiguation paragraph and the open question both address the same s.B/allocated(s) relationship from opposite ends; the paragraph asserts distinctness, the question defers the linkage. The "binary character… Nelson's model has no third status… either conceptually assigned (in B) or not" paragraph likewise just restates that B is a set with membership.
**Required**: Reduce the disambiguation to the one load-bearing sentence (s.B is the committed registry, not the allocator's realized domain) and let the open question own the relationship. Drop the binary-character restatement.

## OUT_OF_SCOPE

### Topic 1: The allocated(s) ⊆ s.B activation discipline
**Why out of scope**: Aligning allocator-extension transitions with baptismal operations depends on the operation layer and genesis seed selection — correctly left as an Open Question, not a defect here.

VERDICT: REVISE
