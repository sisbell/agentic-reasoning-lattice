## Question 2 [theory]

> What relationship must transcluded content bear to the identity of its source, such that the system can always say where the content originally came from?

## The Answer: Transcluded Content Must Share the Source's Istream Identity

The relationship is **identity through shared Istream address**, not duplication. Transcluded content does not get a new identity—it *retains the source's permanent Istream (I-address)*. This is what makes origin always traceable.

### Inclusion by Reference, Not Copy

Transclusion is fundamentally "inclusion by reference, not copy" (per the transclusion concept). When you transclude, you do not duplicate the bytes—you include a reference to their permanent home location:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

Because the content must be *fetched from its home*, the connection to origin cannot be severed. The fetching mechanism itself requires the source identity.

### Identity Is Based on Creation, Not Value

The critical principle (from the content-provenance material) is that content identity is based on **creation, not value**:

- Two documents with identical text created independently have **different** I-addresses.
- Transcluded content **shares the same I-address** as its origin.

This is precisely how the system distinguishes "wrote the same words" from "quoted from the original." Identity is the I-address, and transclusion preserves it.

### The I-Address Structurally Encodes Origin

An Istream address is a tumbler of the form:

```
Node.0.User.0.Document.0.Element
```

The **Document field directly encodes which document originally created the byte**. Origin is therefore *structural*, not metadata that can be stripped or falsified:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

> "Non-native bytes are as much a logical part of a document as native bytes." (4/11)

### Why This Matters

Because transcluded content carries its source's identity:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

The shared identity enables automatic attribution, royalty splitting ("the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically" — 2/45), and finding every document containing the material via **FINDDOCSCONTAINING**, which works "regardless of where the native copies are located" (4/63).

### Summary

Transcluded content must bear an **identity-preserving** relationship to its source: it shares the source's permanent Istream address rather than receiving a new one. Because that I-address encodes the home document and the bytes are fetched from their home location, the system can always trace any character back to where it originally came from. This is the difference between transclusion (a live reference that retains identity) and copying (which, in Nelson's words, leaves you with "the inert, non-interactive copy" — 2/48).

*Note: "I-address," "Istream," and "transclusion" are implementation terms; Nelson's corresponding terms are "home location," "native bytes / virtual byte stream," and "inclusion / windowing / quote-link."*
