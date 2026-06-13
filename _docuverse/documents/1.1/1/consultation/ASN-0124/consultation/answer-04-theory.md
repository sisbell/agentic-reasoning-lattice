## Question 4 [theory]

> Must the document in which the queried material natively originates itself appear in the result, or is the operation defined only over documents that share the material from elsewhere?

I was unable to read the raw page images or text files — every Bash, Glob, and file-read call in this session returned empty, so I cannot pull additional surrounding context from the scans. However, the two defining statements of the operation are already present and **verified** (page-cited) in the curated sources, and they are sufficient to answer the question. I'll answer from those and mark the one place I'd want raw confirmation.

---

# Answer: The native (home) document IS included

The operation in question is **FINDDOCSCONTAINING**. The native document — the one in which the queried material originates — **must appear in the result**. The operation is *not* defined only over the documents that share the material from elsewhere (transclusions); it is defined over **all** documents that contain the material, and the home document is the most fundamental container.

## What the specification actually says

Nelson defines the operation inclusively, by *containment*, not by *transclusion*:

> "This returns a list of all documents containing any portion of the material included by `<vspec set>`." — 4/70

> "This returns a list of all documents containing any of the material specified by the span addresses, **regardless of where the native copies are located**." — 4/63

Two things follow directly:

1. **"All documents containing"** is inclusive language. The home document contains its own material by definition — that is precisely what makes it the home document. There is no clause restricting the result to *foreign* documents, so the native document is in scope.

2. **"regardless of where the native copies are located"** confirms the search is over *content identity*, not document boundaries. The query resolves the material to its Istream origin and then finds every document whose arrangement references that origin. The native document's own Vstream references its own Istream content — so it necessarily satisfies the predicate. The phrase explicitly tells you that the document *holding the native copies* is not excluded; the search returns containers whether they hold the native bytes or reference them from elsewhere.

This is reinforced by how the operation maps to the Istream/Vstream model: it "searches Istream origin, returns Vstream locations" (curated [i-space-v-space] mapping). The primary Vstream location of any content is the home document where it was created.

## Why the "transclusion discovery" framing doesn't narrow it

Several of the curated concept notes gloss FINDDOCSCONTAINING as "finds all documents that *transclude* specified content." That is a description of its **novel use case** (the backlink / "who else quotes me" problem), not a restriction in the protocol. Nelson's own words are "all documents *containing*," and a document trivially contains material it natively holds. The home document is not a transclusion of itself, but it is unquestionably a document *containing* the material — so the inclusive definition reaches it.

A useful structural cross-check: the operation is the companion to the windowing guarantee that "it must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time" (curated [windowing], 2/36-domain). The whole point of asking "what contains this material?" is to recover the full set of containers across the docuverse — and the origin is part of that set, not outside it.

## The one practical caveat (front end vs. FEBE)

This guarantee is at the **FEBE / back-end** level: the operation returns the complete set, native document included. A *front end* may, for a given task, choose to suppress the home document as a trivial/expected result (e.g., when a user explicitly wants "who else uses my passage"). That is a presentation choice and does not change what the operation itself returns. Nelson is explicit that such filtering belongs above the storage layer ("scanning belongs in the middle end, not exposed to users" — curated [febe]).

## Summary

| Question | Answer |
|---|---|
| Is FINDDOCSCONTAINING restricted to documents that share the material from elsewhere? | **No.** |
| Does the native/home document appear in the result? | **Yes** — it is the canonical "document containing" the material. |
| On what basis? | "All documents containing... regardless of where the native copies are located" (4/63, 4/70); search is by Istream origin, which the home document's Vstream satisfies. |

---

**NEED_RAW: 4/63, 4/70** (raw pages ~235 and ~237) — The two verified quotes above are decisive on their face, and "regardless of where the native copies are located" points clearly toward inclusion of the native document. I would only want the raw scans to confirm that no adjacent sentence on those pages adds an explicit native/home-document *exclusion* (none is reflected in the curated material, and Nelson nowhere singles the home document out for special treatment — the answer rests on the inclusive wording "all documents containing" rather than on an explicit "the home document is included" statement).
