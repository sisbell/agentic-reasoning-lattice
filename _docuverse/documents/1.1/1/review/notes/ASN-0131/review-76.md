# Review of ASN-0131

## REVISE

### Issue 1: "First, overlap, not containment" restates the paragraph that motivated it

**ASN-0131, "When does an endset touch the region?"**: The motivating paragraph already argues the point in full — *"Containment — `coverage(e) ⊆ I` — would require the entire endset to lie inside the region. But this is plainly too strong … The relation we want is overlap: the endset touches the region exactly when it covers at least one address the region also covers."* — and then the first numbered property re-states it: *"First, **overlap, not containment**. A single shared address suffices; partial overlap is real contact. The endset need not lie inside the region, and the region need not lie inside the endset."*

**Problem**: This is the two-paragraphs-saying-the-same-thing pattern the anti-bloat classifier targets. "The endset need not lie inside the region" / "a single shared address suffices" are the conclusions the preceding paragraph already reached by rejecting containment. The only content in "First" not already present above is the Nelson "all or any part of" framing. The reader who followed the motivation must skip past "First" to reach genuinely new material ("Second"/"Third"). Note that "Second" (existential *within* an endset) and "Third" (per-endset, not per-link) are *not* redundant — they introduce new aspects; only "First" duplicates.

**Required**: Fold the Nelson "all or any part of" quote into the motivating paragraph and drop the "First" point (renumbering "Second"/"Third"), or trim the motivating paragraph to pose-the-question only and let the three points carry the characterization. Do not keep both.

### Issue 2: Finiteness and computability are argued at length but carry no claim label

**ASN-0131, "The unit of the answer"** (the paragraph beginning *"The answer just defined is **finite unconditionally** …"*) and the **Claims Introduced** table: the note establishes, across a multi-sentence paragraph, that the result is unconditionally finite and (given a finitely-presented `W`) computable by finitely many decidable tests. Every *other* guarantee in the note — eighteen of them — is captured as a labeled `RE-*` claim; this one is not.

**Problem**: The Claims table is the note's citeable interface. A downstream note cannot cite "RE returns a finite set" or "RE is decidable" because neither is labeled. The asymmetry is also internally inconsistent: the recent strengthening of this argument (per the revision history) signals it is treated as non-trivial, yet non-trivial guarantees elsewhere all get labels. Either the result is a guarantee worth the prose — in which case it should be a claim — or it is the trivial observation "a subset of a finite set is finite," in which case the dedicated paragraph is over-built.

**Required**: Promote the result to a labeled claim (e.g. `RE-FIN`: result finite unconditionally; computable under finite presentation of `W`) and add it to the table; or, if it is meant as a trivial remark, reduce the paragraph to one sentence.

## OUT_OF_SCOPE

### Topic 1: Image distributivity over union and intersection

**Why out of scope**: The union-distributivity and intersection-non-distributivity sections re-derive facts about `image` itself — `image(W₁ ∪ W₂, d, Σ) = image(W₁, d, Σ) ∪ image(W₂, d, Σ)` and `image(W₁ ∩ W₂, d, Σ) ⊆ image(W₁, d, Σ) ∩ image(W₂, d, Σ)` (strict under non-injectivity, via M13/M14). These are properties of ASN-0127's `image` primitive, not of `RE`, and the note needs them only because ASN-0127 exposes `F-VDIST` (over `findlinks_V`) but no raw image-distributivity lemma. Deriving them inline here is defensible — there is nothing to cite — so this is not an error in ASN-0131. But the natural home for these lemmas is ASN-0127's image layer; lifting them there would let this note cite rather than rebuild. That is future foundation-maintenance territory, not a revision to this note.

### Topic 2: The deferred Open Questions are correctly scoped

**Why out of scope**: OQ1 (whole-endset vs touching-spans extent), OQ3 (rendered V-order answers), OQ4 (weakest structural sufficient condition for intersection-equality), OQ5 (cross-server completeness), OQ6 (type-slot match against content), and OQ7 (link-subspace regions) each name real future territory and are left as questions rather than half-answered. The note holds RE-WHOLE provisional pending OQ1 and carries the `coverage(Θ) ∩ dom(Σ.C) = ∅` net-removal hypothesis honestly pending OQ6, rather than asserting a guarantee it cannot support. These deferrals are handled correctly — flagged only to confirm no further-ASN coverage is owed here.

VERDICT: REVISE
