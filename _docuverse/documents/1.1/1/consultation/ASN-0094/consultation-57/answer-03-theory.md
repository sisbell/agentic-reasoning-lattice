## Question 3 [theory]

> Did the typed predicate framework envision a mechanical derivation of predicate forms from a relation's structural type, or an open-ended catalog of predicate roles attached to types by layer convention?

The phrase "typed predicate framework" is not Nelson's terminology — it doesn't appear in Literary Machines. The closest analog Nelson addresses is the **link type system** (the "three-set"/type endset). On that closest analog, Nelson clearly chose the **open-ended catalog** model, not mechanical derivation.

## What Nelson Says About Type Specification

The type endset is an *arbitrary address*, not a structurally-derived form:

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

## Open-Ended, Not Mechanical

Nelson is explicit that the *set* of types is not derived from any closed schema:

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." [LM 4/43]

> "Standardization of a working set of link types is now a high priority, but has less priority than establishing a robust demonstration rig." [LM 4/52]

> "A TENTATIVE LISTING OF SOME LINK TYPES. Link types are open-ended, so this is not the original beginning, but a first provisional, to give the flavor of current thinking." [LM 4/52]

His listed types (Connection, Comment, Counterpart, Citation, Mail, Quote, Suggested-Threading, etc.) are conventions catalogued by convention, not forms derived from any structural typing.

## What the Mechanism IS Mechanical About

One thing IS mechanical: the *matching* mechanism. Search resolves a type by **address equality**, not by inspecting structure or content:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

So the engine is mechanical (address match), but the *catalog of meanings* is open-ended convention.

## Verdict

For link types specifically, Nelson's design is unambiguously the **open-ended catalog attached by convention** model. Types are addresses chosen by users; the system never derives predicate forms from any structural typing of relations.

NEED_RAW: If "typed predicate framework" refers to the project's formalization work (e.g., ASN-level predicate typing in `vault/4-modeling/` or `vault/project-model/`), that is project-internal terminology beyond Literary Machines and would need to be answered from those project artifacts, not from Nelson's text.
