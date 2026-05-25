## Question 1 [theory]

> What must the system guarantee about the identity of content that appears in one document arrangement but is absent from another?

# Content Identity Across Arrangements

The system must guarantee that **content identity is anchored in Istream, not in any particular arrangement**. When content appears in one document arrangement but is absent from another, its identity—its permanent Istream address—is unaltered, persistent, and entirely independent of which arrangements happen to display it.

This is the fundamental separation I designed into the system. Content lives in Istream forever. Arrangements (Vstream) are views over that substrate. "Absence from an arrangement" describes the *view*, never the *content*.

## What Must Be Guaranteed

### 1. The Content Still Exists in Istream

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The phrase "not currently addressable" qualifies the *arrangement*, not the *content itself*. The bytes are still in Istream—they are merely not visible through this particular Vstream view. This is why I insist on append-only storage: deletion is a change of view, not a destruction of substance.

### 2. The Content Remains Available in Other Arrangements

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Removing content from one arrangement cannot remove it from another. Each arrangement is an independent view over the same Istream substrate. Other versions, transclusions, and historical states retain their access to that content.

### 3. The I-Address Is Permanent

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19]

The Istream address that identifies the content is immutable. The content has the same identity whether it appears in arrangement A, arrangement B, both, or neither. Two arrangements that both contain that I-address share the same content—not copies of identical-looking content, but the actual same content.

### 4. Links to the Content Still Resolve

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

Because links attach to I-addresses (not V-positions), they continue to resolve even when content is absent from a particular arrangement. The link remains attached to the bytes themselves, wherever else they may appear in the docuverse.

### 5. Historical Reconstruction Remains Possible

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

Any previous arrangement containing the content can be reconstructed. The content's absence from a current arrangement does not erase the historical arrangements in which it appeared.

### 6. Origin Remains Traceable

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

The I-address structurally encodes the home document. The content's origin cannot be severed by its absence from any particular arrangement. Wherever the content appears, its provenance is visible.

### 7. Correspondence Across Arrangements Remains Computable

Because identity is anchored in Istream, two arrangements can be compared structurally. The system knows which parts correspond—even when one arrangement contains the content and another does not. This is what makes meaningful version comparison possible. SHOWRELATIONOF2VERSIONS returns the correspondence precisely because identity does not depend on inclusion in any particular arrangement.

## The Underlying Principle

This is what I meant when I wrote that "users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals" [LM 2/45]. The fundamental error of conventional storage—what I called "destructive replacement"—is treating documents as the primary entity, where editing means overwriting. Xanadu inverts this: **content is primary; arrangements are views over it**.

When content is "absent" from an arrangement, nothing has been destroyed. The arrangement has simply chosen not to display it. The content's identity—its permanent place in the docuverse—is undisturbed. The system must never conflate "removed from a view" with "destroyed." That distinction is the foundation of historical backtrack, version comparison, transclusion, link survival, royalty accounting, and the entire fabric of the docuverse as a permanent literary record.

A document is, as I have always said, "an evolving ONGOING BRAID" [LM 2/14]. Strands enter the braid; strands leave the braid; but the strands themselves are not destroyed when they leave the current weave. They remain available, identifiable, and reachable—because their identity was never the braid in the first place.
