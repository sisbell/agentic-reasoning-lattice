## Question 2 [theory]

> Must the search reach every document in the docuverse that holds the queried material through transclusion, regardless of where the material was originally authored or which document the asker started from?

The raw page images aren't present in this checkout (the inventory's `/page-NNN.png` paths don't resolve), but the FINDDOCSCONTAINING quotes I need are in the curated `operations` and `i-space-v-space` extracts and are marked with verified page numbers (4/70, 4/63). That's sufficient to answer precisely.

---

## Answer: Yes — that is exactly the guarantee, with one honest distinction between *semantic intent* and *distributed reality*.

The operation that answers this question is **FINDDOCSCONTAINING**, and its specification is deliberately exhaustive on all three counts you name.

### 1. "Every document that holds the material" — exhaustiveness

The operation is defined to return *all* such documents, not a sample or a local subset:

> "This returns a list of all documents containing any portion of the material included by `<vspec set>`." (4/70)

The word "all," and "any portion," are load-bearing. A document that transcludes even one byte of the queried span is in the result set.

### 2. "Regardless of where the material was originally authored" — native-home independence

This is stated almost verbatim in Nelson's gloss on the same command:

> "This returns a list of all documents containing any of the material specified by the span addresses, **regardless of where the native copies are located**." (4/63)

The reason it *must* be independent of authorship origin is structural. Transclusion is inclusion **by reference to a permanent I-address, not by copy**. The originating (native) document is simply the one that first created those bytes and thereby fixed their Istream address:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

Every document that windows that material — whoever authored it, on whatever server — points at the **same I-address**. So the search resolves the queried span to its Istream origin and finds *every* Vstream that references it: the native home **and** every transcluder alike. The author of the original cannot be privileged or excluded, because the search is keyed on the content's address, not on any document's authorship.

### 3. "Regardless of which document the asker started from" — asker independence

The argument to FINDDOCSCONTAINING is a `vspec-set` — *the material*, not the asker's home document. The search runs over the docuverse, not over the local document the asker happened to be reading. The starting document is merely where the asker *pointed* to identify the span; it places no boundary on the results. So whether you started from the original, from a transclusion of it, or from an unrelated document where you happened to copy the address, the returned set is identical.

This is the inverse direction of ordinary windowing, and Nelson explicitly promises both directions:

> "It is possible for the reader to ask to see the materials which are windowed to by a given document. However, it must also be possible for the reader to ask to see whatever documents window to the current document. **Both are available at any time.**" (windowing, 2/35–2/38)

FINDDOCSCONTAINING is the "what windows *to* this content" direction, made global.

### Why this is a *requirement*, not a convenience

This completeness is what makes Xanadu's economic and attributive guarantees work. Royalty must flow to the owner "every time a fragment is summoned"; attribution must be traceable from any byte ("you can at once ascertain the home document of any specific word or character," 2/40). Neither holds if the system can only see uses inside the asker's own neighborhood. Finding *all* transcluders of given content is the mechanism behind "find all uses," royalty accounting, and version/correspondence discovery.

### The one honest caveat: exhaustive *in principle*, best-effort *in practice*

Nelson's verified guarantee is "all documents... regardless of where the native copies are located" — a statement about the **logical/semantic** reach of the search across the unified address space. The docuverse is one space precisely because the network melds servers:

> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space." (4/70)

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse." (4/72)

But Nelson is candid that physical reach is imperfect at any given instant:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." (4/75)

So the design *intent* is total reach (every document holding the material, anywhere, for any asker), implemented over a redundant, self-organizing distributed store; the *operational* reality is that a temporarily disconnected node may not be reached in that moment. The architecture treats "not currently available" as a fallback to retry against backups, not as a redefinition of the guarantee.

A related design principle — stated by Nelson for *link* search rather than for FINDDOCSCONTAINING specifically — captures the same philosophy that volume and distribution must not defeat completeness:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

### Bottom line

Yes. By design, the search **must** reach every document in the docuverse that holds the queried material through transclusion — independent of who authored the material (because the search is keyed on its permanent Istream address, "regardless of where the native copies are located," 4/63) and independent of which document the asker started from (because the query argument is the *material*, not the asker's container). The exhaustiveness is the semantic guarantee Nelson states ("a list of *all* documents," 4/70); the only qualification is the practical one that a distributed network may have nodes temporarily unreachable at the moment of asking (4/75).

---

*Two small scope notes on sourcing:* The asker-independence point (item 3) is a structural consequence of the operation's argument signature as given in the curated `operations` extract, not a single verbatim Nelson sentence — I've drawn it from the command definition rather than quoting it as Nelson's prose. Everything in quotation marks above is verbatim from the verified curated sources. If you want me to confirm the exact surrounding wording of FINDDOCSCONTAINING on the original page (to check whether Nelson adds anything about cross-server search behavior right there), that would be: NEED_RAW: 4/63, 4/70 (raw pages 230, 237), which aren't in this checkout.
