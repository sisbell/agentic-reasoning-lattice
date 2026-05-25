## Question 8 [theory]

> Must the comparison reflect the full version history of each document, or only their current states?

# Comparison: Pairwise, Not Holistic

A comparison reflects two **specified** states. It does not, in a single operation, traverse the full version history of each document.

The protocol command SHOWRELATIONOF2VERSIONS makes this explicit: it takes two spec-sets and "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. Two spec-sets in, correspondence pairs out. Pairwise.

But this should not be confused with a limitation. The **historical backtrack** guarantee means *either* of those spec-sets may be any past state, not just the current one:

> "The user may scroll through any two versions to see corresponding parts; and much more." [LM 2/21]

The word is *any*. Compare current to current, current to historical, historical to historical — the mechanism is the same. The full history is preserved precisely so that any pair within it remains comparable.

There is also a deeper sense in which version history is **implicit** in every comparison. Correspondence is not metadata; it falls out of shared Istream origin. When two versions share I-addresses for some bytes, those bytes correspond — automatically, structurally. Editing produces new Vstream arrangements over the same Istream content, so the lineage is structurally available without being explicitly traversed.

This is why links span versions without explicit history-walking:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

The link mechanism reaches *through* the history because the addressing structure already encodes the relationships. A comparison operation doesn't need to recapitulate that — it just consults what is already true at the address level.

So: a comparison reflects two states. The full version history need not be present *in the comparison itself*, but it remains continuously accessible *for* comparison — and structurally underlies the very notion of correspondence that comparison reports on.
