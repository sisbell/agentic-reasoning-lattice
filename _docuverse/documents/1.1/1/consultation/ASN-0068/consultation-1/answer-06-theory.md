## Question 6 [theory]

> Did the design contemplate comparing the link arrangements of two documents as a meaningful operation, given that CL-OWN forces every link in d's arrangement to have origin = d — or was compareversions intended only for s_C in practice?

# Compareversions: Content, Not Link Arrangements

Your intuition is correct. Nelson's `SHOWRELATIONOF2VERSIONS` was conceived for content correspondence (s_C), not for comparing link arrangements between documents. Here's the textual and structural evidence:

## What Nelson Actually Specifies

The operation returns "a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. Every passage I can find describing intercomparison frames it as content-level:

> "a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

> "The user may scroll through any two versions to see corresponding parts" [LM 2/21]

> "Moreover, highlighting the corresponding parts is a vital aspect of intercomparison." [LM 3/13]

"Word for word" and "parts" are the operative phrases — content, not link structure.

## Why Link Comparison Would Be Vacuous

Your CL-OWN observation is exactly the structural problem. Nelson is explicit:

> "A document includes only the links of which it is the home document." [LM 4/31]

So d1's links and d2's links are at disjoint tumbler subspaces (the `0.2.N` regions under each document's address). They have no shared Istream origin to correspond on, because links aren't transcluded — they're owned. A `SHOWRELATIONOF2VERSIONS` applied to two link span-sets would correctly return nothing.

## Nelson's Actual Mechanism for Cross-Version Link Behavior

Rather than compare links, Nelson designed **refractive following** — the link layer crosses versions through content correspondence:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

This is the architectural answer to "how do links relate across versions": they don't get compared, they refract. The single link, owned at its home document, applies to every version of the target through the content correspondence the back end already computes. A separate "compare link arrangements" operation would be redundant.

## For User-Asserted Link Equivalence

Where users *do* want to assert that two distinct links or arrangements are equivalent (across truly unrelated documents — translations, parallel treatments), Nelson provides the **counterpart link** [LM 4/53]:

> "The counterpart link shows that there are correspondences between two equivalent documents, sections or passages."

This is a user-created assertion, not a computed comparison. Telling: Nelson reaches for a *link type* to express link-arrangement equivalence, rather than extending the intercomparison operation.

## Summary

In practice and in design intent, `SHOWRELATIONOF2VERSIONS` is the s_C operation. Nelson never contemplates it as a `s_L` operation because:

1. CL-OWN makes two documents' link sets structurally disjoint
2. Refractive following [LM 2/26] makes cross-version link behavior automatic without comparison
3. Counterpart links [LM 4/53] handle the cross-document equivalence case manually

So your implementation is faithful to design intent if `COMPAREVERSIONS` operates on content spans only. Comparing link arrangements directly is not a coherent operation in Nelson's model — it's either trivially empty (different homes) or already handled (refraction).
