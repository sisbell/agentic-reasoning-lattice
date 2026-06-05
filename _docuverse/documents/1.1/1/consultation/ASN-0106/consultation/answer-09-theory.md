## Question 9 [theory]

> If the same content appears in more than one requested region, what must the result reveal about that content being shared within the single document?

## Answer

If the same content appears in more than one requested region of a single document, the result must **reveal the correspondence between those regions** — it must expose, as explicit ordered pairs of spans, that they are the *same* content shared within the document, not coincidentally-identical separate content.

### Why: identity is structural, by Istream origin

The reason this matters is that in Xanadu, content identity is not based on matching values but on shared Istream (I-address) origin. Two regions that look alike are only "the same content" if they trace to the same permanent I-address. From the curated correspondence source:

> "Correspondence is a RELATION - the relationship between Vstream positions that share the same Istream origin. [...] If two V-positions in different documents (or different versions of the same document) map to the same I-address, those positions CORRESPOND."

And from the provenance source, this is explicitly *not* a value match:

> "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address. This is how the system distinguishes 'wrote the same words' from 'quoted from the original.'" (provenance, citing 4/10-4/11)

So when shared content recurs across requested regions of one document, what the result must surface is that these regions map back to a common origin — the structural fact of sharing, traceable to the home document of every character:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

### How the result expresses it: corresponding span pairs

The operation that computes this comparison returns the correspondence as pairs of spans:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." (4/70, on SHOWRELATIONOF2VERSIONS)

That is the form the revelation takes: ordered pairs identifying which span in one requested region corresponds to which span in the other, because both refract from the same underlying material. Nelson frames this as essential to intercomparison:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." (2/20)

> "Moreover, highlighting the corresponding parts is a vital aspect of intercomparison." (3/13)

### Summary

The result must reveal that the recurring content is **one shared piece of material** — expressed as ordered pairs of corresponding spans tied to a common Istream origin — rather than presenting the regions as disconnected, independently-authored matter. The sharing is a structural correspondence (same I-address), and the result's job is to make that correspondence explicit.

---

NEED_RAW: 4/61-4/70 — The curated sources confirm SHOWRELATIONOF2VERSIONS compares "two spec-sets," but whether a single self-comparison (same document/spec-set against its own overlapping regions) is the canonical operation for *intra*-document sharing, versus FINDDOCSCONTAINING, is not explicitly stated above. I'd verify pages 4/63 and 4/67-4/70 to confirm the exact operation semantics for shared content *within* a single requested spec-set.
