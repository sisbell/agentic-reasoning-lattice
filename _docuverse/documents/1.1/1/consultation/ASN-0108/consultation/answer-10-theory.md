## Question 10 [theory]

> Must the boundaries between successive windows be a private convenience for the reader, or a stable property of the system that any reader would observe identically?

# Window Boundaries: Stable System Property, Not Reader Convenience

The boundaries between successive windows are a **stable property of the system**—structurally defined, stored, owned, and observable identically by any reader. They are not a private reader convenience. But there is an important distinction between the *boundary itself* (system property) and the *visual presentation of it* (front-end choice), which I'll draw out below.

## A compound document IS its window structure

A window is not something a reader imposes—it is part of how the document is defined. A compound document is, structurally, a sequence of inclusions and native material:

> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material." (2/32)

The quote-links (inclusion links) ARE the document. The point at which one window ends and the next begins is exactly the point at which one quote-link's span ends and the next element begins. Because these inclusion links are stored as part of the document's structure—its out-links, under the owner's control—every reader who retrieves the document retrieves the same arrangement. The mapping from the document's virtual byte stream to its various home Istreams is the document.

## The home document of every character is objectively ascertainable

The decisive guarantee is that the origin of any character is an observable fact, not a reader's guess:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

A window boundary is precisely the location where the ascertainable home document changes. If any reader can determine the home document of each character identically, then the transition points between successive windows are determined identically for all readers. This is reinforced by the native/non-native distinction:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

Where a byte's home location lies is a fixed structural fact (its Istream address), so the boundary between two differently-homed spans is fixed too.

## The boundaries are permanently defined, including across time

Window boundaries persist as a stable definition because derivative/compound documents are permanently defined in terms of originals and changes (see `design-notes` material on the non-destruction guarantee, 2/37). Even the time-binding mode of a window is a property *of the window definition*, not a reader's whim:

> "A quotation—an inclusion window—may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." (2/37)

Whether a window floats in time or is fixed is set by whoever composed the compound document—so two readers opening the same compound document observe the same window structure.

## The one genuinely reader-side aspect: rendering, not boundary

What *is* left to the reader's side is how the boundary is *displayed*—borders, shading, whether you "step through" the glass—not where it falls:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else..." (2/34)

> "Viewing-methods and manipulations are up to the designers of the equipment and viewing program." (2/47)

So the *visual treatment* of a window edge is a front-end matter and can differ between readers. But the edge's *location in the byte stream*—the point where content stops coming from document B and starts coming from document C—is fixed by the inclusion structure.

## Conclusion

The boundary between successive windows is a **stable system property**. It is fixed by the stored quote-links that constitute the compound document, and it is guaranteed observable because "you can at once ascertain the home document of any specific word or character" (2/40). What a reader's front end may freely choose is only how to *render* that boundary—not whether it exists or where it lies. Two readers opening the same compound document will find the windows beginning and ending at exactly the same places.
