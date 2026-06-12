---
create_note: 130
title: "Predicate Definitions as Substrate Content"
source_doc: "_workspace/asn-new-predicate-definitions-draft.md"
depends: [36, 43, 86, 93, 126, 128, 129]
---

# Why I'm importing this doc

ASN-0129 (doubly converged: maiden run plus anti-bloat audit) defines the
predicate language, but its terms are meta-level objects with no existence
inside the system. This note is the operations layer of the protocols
stack — the MAKELINK of predicates: terms become content. A definition is
an immutable K.α run holding an encoded PL term, registered by a validated
classifier emit (PR0, the R-VAL/P-tgt enforce-by-rejection pattern),
referenced by address, versioned by the shipped supersession machinery,
and certified against ASN-0129's spelling-level ST class.

Three foundation facts carry the design: S0/S1 make validation a permanent
fact rather than a cache (PR1); total ordering of registration events makes
the reference graph a DAG by construction, with self-reference and mutual
recursion unconstructible rather than checked-for (PR2), preserving PC6a
under definitional reference; and S4's identity-by-origin dissolves naming.
Two standard registrations ship (pdef, pd_stable) under R-C1-style
collision checks, extending ASN-0128's precedent.

Strategic intent: this completes the third-party extension story — a
builder's protocol logic lives in the docuverse as linkable, citable,
supersedable documents, with the stability lint ("is this termination
predicate certified ST") expressible as a one-atom PL query. The worked
composition demonstrates the certificate refusing an active-view
terminator and accepting its Marker-pattern respelling — the protocol
design lesson enforced structurally.

The draft was authored against ASN-0129's final post-audit text (WT,
ST/SF, FP, the C-reach/C-emit conjecture status) and survived an
operator adversarial review that re-grounded PR2 on registration order
and resolved the content-read boundary precisely.
