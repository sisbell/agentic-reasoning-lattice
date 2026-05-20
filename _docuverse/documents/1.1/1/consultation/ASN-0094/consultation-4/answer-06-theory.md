## Question 6 [theory]

> Are Attribute (parent → sidecar) and Citation (citing → cited) conceived as distinct relational primitives in the design, or as the same `(1, 1, A_doc, A_doc, ⊤)` pattern under role-specific naming?

# Same Structural Primitive, Different Type Endset

In my design, there is **one link primitive** — the three-endset link — and all such distinctions live in the type endset, not in separate structural kinds.

## The Universal Link Mechanism

The link mechanism I designed is deliberately uniform:

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose. This is done with a mechanism which is powerful and symmetrical." [LM 4/43]

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

The symmetry is the point. The from-set, to-set, and type-set are all endsets of the same kind — span-sets pointing into tumbler-space. There is no privileged "Attribute primitive" distinct from a "Citation primitive" anywhere in the architecture.

## How Distinction Actually Works

What makes a link mean one thing versus another is purely the address its type endset points to:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

So if your formal notation `(1, 1, A_doc, A_doc, ⊤)` captures the structural shape — one span on each side, both pointing at documents, with type position open — then yes, "Attribute (parent → sidecar)" and "Citation (citing → cited)" instantiate the *same* shape. They differ only by binding the type endset to different addresses.

## On the "Attribute" Terminology

NEED_RAW: I should flag that "Attribute" as a named link type does not appear in Literary Machines as such. My standard listing (4/52-4/55) names Title, Author, and Document Supersession as **metalinks** — links applying to whole documents — and Citation appears among the literary links (4/54). What you're calling "Attribute (parent → sidecar)" sounds like a metalink in my taxonomy, but the specific parent-sidecar framing is a later formalization, not language I used.

## Design Consequence

This matters for your specification: do not introduce Attribute and Citation as separate type-theoretic primitives. They are the same primitive — a three-endset link — distinguished by type-address. The categorical work belongs in the link-type registry (or in convention), not in the relational kernel. Standardizing type addresses is a high priority, but those addresses are catalog entries, not new structural kinds:

> "Standardization of a working set of link types is now a high priority, but has less priority than establishing a robust demonstration rig." [LM 4/52]

If you split them into two primitives, you have abandoned the symmetry that lets users define their own link types without system changes. That symmetry is non-negotiable. Restrict it, and all will lose.
