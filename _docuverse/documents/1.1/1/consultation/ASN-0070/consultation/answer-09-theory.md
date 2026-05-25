## Question 9 [theory]

> What is the guarantee about partial resolution — if some portion of an endset is reachable in the current document but another portion is not, what must the user see?

Looking at the curated sources, Nelson addresses partial resolution most directly in the link search satisfaction model, which is the "AND of the ORs" rule:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

This means a link is returned to the user when **at least one span of each endset** matches. The link is not suppressed merely because other spans in the endset don't match or aren't reachable in the current document — partial satisfaction is sufficient for the link to surface.

Nelson reinforces this with the explicit performance guarantee:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

The complementary guarantee comes from **survivability**, which governs what makes an endset still meaningful:

> "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end**." (4/43)

So the survival threshold is "anything left" — even one byte remaining at each end keeps the link alive. By symmetry with the search rule, a link with partially-reachable endsets is a fully valid link that the user should encounter.

**What the curated sources establish:**
1. The link is returned/found when one span of each endset satisfies (4/58)
2. The link survives as long as any bytes remain at each end (4/43)
3. Discontiguous endsets are a normal case ("one end of a link may be on a broken, discontiguous set of bytes," 4/42)

**What the curated sources don't explicitly state:** the specific *display* obligation — i.e., must the user see indicators for the unreachable portions, must out-of-document spans be marked as such, must "step through" affordances be offered for non-current-document spans, etc. The texts describe windowing semantics (step through to originals) and "step through the window" navigation (2/34), but I don't find an explicit rule mandating *what visual treatment* unresolved endset portions must receive.

NEED_RAW: 4/56-4/60 (link search satisfaction, "AND of the ORs" detail, junk-link filtering, and any explicit display guarantees Nelson states); 4/47-4/49 (one-sided links and the Tumbler Square — may clarify what visual reach means when only part of an endset is in the current document).
