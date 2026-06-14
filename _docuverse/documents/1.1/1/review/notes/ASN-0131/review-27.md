# Review of ASN-0131

The note is, on the whole, careful and deep: the core definition is clean, soundness/completeness fall out of the biconditional, the worked instance genuinely exercises every distinctive claim, the union-distributivity derivation factors correctly through the region-independent `Avail(Σ)`, and the contraction wp (RE-CWP) is a non-trivial, correctly-derived refinement of D-CWP. I checked the worked example arithmetic (`a₄ = shift(a₂, 2)`, the straddling width-2 span, the `e₃` field-agreement disjointness) and it holds. The retraction analysis (R-Scope confinement, the antichain freshness of the emitter `b`, the "drops iff sole bearer" forward/backward split) is sound, and the `coverage(Θ)` hypothesis is honestly flagged to OQ6 rather than waved away.

The defects are concentrated in one place: the user-facing insert/delete portion of the stability section.

## REVISE

### Issue 1: Delete (D-SHIFT) is mislabeled a "domain-growing" displacement

**ASN-0131, Claims table RE-EDIT**: "…the user-facing shift-based insert/delete (domain-growing displacements, I3/D-SHIFT, ASN-0082) can move the answer…"

**ASN-0131, stability section**: "an insertion at `p` of width `n` carries the content at every position `v ≥ p` to `shift(v, n)` (I3), *growing* `d`'s arrangement domain rather than preserving it…"

**Problem**: The parenthetical attaches "domain-growing" to the pair I3/D-SHIFT, but D-SHIFT is ASN-0082's *Contraction* (delete), which **shrinks** the arrangement domain — D-CTG-post fixes `V_1(d') = {[1,k] : 1 ≤ k ≤ N − c}`, i.e. `N → N − c`. Delete is domain-shrinking, not domain-growing. Separately, the prose attributes domain-growth to the I3 displacement itself, but I3 *alone* is cardinality-preserving: I3-CS characterizes the post-shift domain as `{v < p preserved} ∪ {shift(u,n) : u ≥ p}` — same cardinality, with a gap opened at `[p, shift(p,n))`. It is the *insert composite* (shift + fill), not I3, that grows the domain.

More importantly, "domain-growing" is the wrong property to be invoking here. The reason the answer moves is that, for a **fixed** region `W`, content swings *through* `W` — gaining and losing I-addresses — under *either* insert or delete, regardless of net domain cardinality change. (For delete, content in the right region slides down out of `W` and content from higher positions slides in; the image swings just as for insert.) The note's own conclusion ("both gains and loses I-addresses") is correct; the "domain-growing" framing both contradicts the delete case and obscures the actual mechanism.

**Required**: Either describe insert (grows) and delete (shrinks) distinctly and correctly, or — better — drop the domain-cardinality framing and state the salient fact: a content displacement moves content through a fixed region, so the image swings non-monotonically. The load-bearing point (the displacement is not a domain-preserving `K.μ~`, so F-IMG-SWING does not apply) survives either way and should be stated without the false "domain-growing" attribution. Alternatively, defer the mechanism to ASN-0082 and cite I3/D-SHIFT for the swing without re-describing it.

### Issue 2: "content slid in from before p" is incorrect

**ASN-0131, stability section**: "…while those positions fill with inserted content or with content slid in from before `p`; so the fixed region's image *both gains and loses* I-addresses."

**Problem**: Under I3's rightward shift, content at positions `< p` is frame-fixed (I3-L leaves it in place) — nothing slides in from before `p`. A vacated region position `v ≥ p` fills with *inserted* content (when `v ∈ [p, shift(p,n))`) or with content displaced **up** from a lower position `v − n`, where `v − n ≥ p` — never from a position before `p`. The phrase describes a flow that I3-L explicitly forbids.

**Required**: Replace "content slid in from before `p`" with the correct source — inserted content, or content displaced up from positions `≥ p` (specifically `v − n`). The "both gains and loses" conclusion is correct and can stand once the mechanism is fixed.

### Issue 3 (anti-bloat): recurring meta-framing that does not advance the argument

**ASN-0131**: e.g. "Three properties of this definition are worth stating, because each is a claim an alternative implementation would also have to honour"; "Three degenerate inputs are worth reading straight off the definition, because each fixes a corner an alternative implementation must also get right"; "an implementation that returned a strict subset, or admitted a near-miss, would not be realising this operation."

**Problem**: The "an alternative implementation would (have to) honour / would not be realising this operation" motif recurs ~5 times. Stating the abstraction-level test once is useful; the repeated invocation is framing that the substantive claims (the three properties, the degenerate cases, soundness/completeness) carry on their own. A lesser instance: the "retraction = emit a withdrawal link, not a delete" point is set up in the *unit-of-the-answer* section, previewed again at the close of the link-emission paragraph ("Retraction is the complementary sub-case … that side-effect … produces the net removal we take up now"), then stated a third time at the head of the retraction section; the mid-stability preview is the trimmable one.

**Required**: Keep one statement of the abstraction-level test and let the property/case claims stand unframed; drop the link-emission paragraph's retraction preview (the retraction section immediately below states it). This is lower-severity than Issues 1–2.

## OUT_OF_SCOPE

The note's own Open Questions (whole-endset vs touching-spans, multiplicity preservation, V-rendering of surfaced endsets, intersection-distributivity, cross-store completeness, type-slot/content matching, link-subspace regions) are correctly scoped as future territory rather than gaps in this note, and I add nothing to them. The named contrast with FINDLINKSFROMTOTHREE is a legitimate scoping mention (by operation name, no ASN number), not a cross-ASN dependency.

VERDICT: REVISE
