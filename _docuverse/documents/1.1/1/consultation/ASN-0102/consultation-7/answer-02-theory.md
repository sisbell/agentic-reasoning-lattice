## Question 2 [theory]

> Is there a primary Literary Machines passage stating that inclusion/virtual-copy creates an additional reference to the same stream content rather than duplicating it, and if so what is its `LM x/y` locus?

Yes. The clearest primary locus is **LM 4/10–4/11**, with supporting statements at **LM 2/36**.

## Primary passage: LM 4/10–4/11

This is where Nelson defines inclusion/virtual-copy explicitly as reference to home-location content, not duplication. From the curated `i-space-v-space` and `sporgl-provenance` sources (verified against the original):

> "The virtual byte stream of a document may include bytes from any other document." (4/10)

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

> "Non-native bytes are as much a logical part of a document as native bytes." (4/11)

Read together, these establish the point directly: the term "inclusions or virtual copies" names spans whose bytes remain stored at their **home locations** and are fetched by request — i.e., an additional reference to the same stream content, not a duplicate. The phrase "obtained by front-end or back-end requests to their home locations" is the operative statement that no second copy is made.

## Supporting passage: LM 2/36

The transclusion/windowing discussion states the no-copy property as a system consequence:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update—especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." (2/36)

## Assessment

For a single best `LM x/y` answer: **4/11** is the precise locus, because it both (a) coins "inclusions or virtual copies" and (b) states their bytes live at "home locations" reached by request. **2/36** corroborates by asserting "no copying operations are required." Both are verified in the curated sources, so no raw-page check is needed.
