# Xanadu Operations

Source: Literary Machines, 4/61-4/70

## What Nelson Says

> "What the Xanadu storage and hypertext system does--and thus is--is defined by the commands to which it responds." (4/61)

> "None of these commands are to be seen by the user. The user's concerns are to be seen on the screen; the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things." (4/61)

> "FEBE includes instructions for insertion in a document, deletion from a document, and rearrangements of unlimited size. These are comparatively simple." (4/61)

> "However, the commands for links and commonality (material shared between documents and versions) are more esoteric, particularly since they have been generalized for the interconnection of broken lists of data." (4/61)

> "Of the 17 current commands in XU.87.1, only one command (RETRIEVEV) is concerned with delivery of the actual content fragments." (4/61)

## Editing Operations

**INSERT**: "This inserts <text set> in document <doc id> at <doc vsa>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

**DELETEVSPAN**: "This removes the given span from the given document." (4/66)

**COPY**: "The material determined by <spec set> is copied to the document determined by <doc id> at the address determined by <doc vsa>." (4/67). This is transclusion — the copy shares I-addresses with the source.

**REARRANGE**: "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." (4/67)

**APPEND**: "This appends <text set> onto the end of the text space of the document <doc id>." (4/67)

## Link Operations

**MAKELINK**: "This creates a link in document <doc id> from <from set> to <to set> connected to <three set>. It returns the id of the link made." (4/68). "The document must be specified because that determines the actual residence of the link--since a document may contain a link between two other documents." (4/63)

**FINDLINKSFROMTOTHREE**: "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69). "If the home-set is the whole docuverse, all links between these two elements are returned." (4/63)

**Link search guarantee**: "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58). "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

**FINDNEXTNLINKSFROMTOTHREE**: Paginated link retrieval — "no more than <nlinks> items past that link on that list." (4/69). Handles "avalanches of material" from link searches.

**RETRIEVEENDSETS**: "This returns a list of all link end-sets that are in <spec set>." (4/70)

## Version Operations

**CREATENEWDOCUMENT**: "This creates an empty document. It returns the id of the new document." (4/65)

**CREATENEWVERSION**: "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." (4/66)

**SHOWRELATIONOF2VERSIONS**: "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." (4/70). "A facility that holds multiple versions is not terribly useful unless it can help you intercompare them in detail." (2/20)

## Retrieval Operations

**RETRIEVEV**: "This returns the material (text and links) determined by <spec set>." (4/67)

**RETRIEVEDOCVSPAN**: "This returns a span determining the origin and extent of the V-stream of document <doc id>." (4/68)

**RETRIEVEDOCVSPANSET**: "This returns a span-set indicating both the number of characters of text and the number of links in document <doc id>." (4/68)

**FINDDOCSCONTAINING**: "This returns a list of all documents containing any portion of the material included by <vspec set>." (4/70). "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." (4/63)
