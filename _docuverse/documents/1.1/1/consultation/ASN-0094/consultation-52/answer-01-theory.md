## Question 1 [theory]

> Did Nelson's design intent treat substrate-level mechanisms like emission-order-aware coverage tracking as universally applicable to any link with the appropriate structural shape, or as semantically scoped to a particular link role such as supersession?

My design intent treated substrate-level mechanisms as **universally applicable** to any link with the appropriate structural shape — never semantically scoped to a particular link role like supersession.

The whole architecture rests on symmetry and generalization. The substrate operates on addresses; it does not interpret roles.

**The type endset is just an address — the substrate cannot read meaning into it:**

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

If the substrate does not inspect what's stored at the type address, it cannot distinguish a supersession link from any other structurally-equivalent link. Substrate mechanisms therefore *cannot* be scoped by link role without violating this layering.

**All three endsets follow one convention — one mechanism, applied uniformly:**

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

**Order-of-arrival applies to every link in a document, uniformly — not selectively to "special" roles:**

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

The system tracks arrival order for *all* links in a document. It does not track ordering selectively for supersession links while ignoring others. The substrate gives every link a position; what users do semantically with that position is their concern.

**Types are open-ended specifically to prevent the substrate from knowing roles:**

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." [LM 4/43]

If the substrate had role-aware mechanisms, it would need a fixed registry of which roles get which treatment. I deliberately rejected that. Anyone can mint new types tomorrow; the substrate cannot have privileged knowledge of which ones deserve coverage tracking.

**The design discipline this enforces:**

If a substrate mechanism exploits emission-order properties to track coverage, that mechanism must apply to *any* link whose structural shape matches its requirements. To gate the mechanism on "is this a supersession link?" requires the substrate to (a) read what's stored at the type address (which I forbade), or (b) maintain a registry of special types (which I rejected when I made types open-ended). Either violates the layering.

The correct posture: the mechanism lives in the substrate and applies universally to any structurally-eligible link. Supersession may be the *motivating* use case — the reason someone designed the mechanism — but the mechanism itself cannot be scoped to that role. If it also happens to apply to a counterpart link, an alternative-version link, or a user-defined link nobody has invented yet, that is the system working as designed.

Generalization at the substrate is not an accident to be tolerated. It is the architecture.

---

**Note on terminology:** The phrase "emission-order-aware coverage tracking" is not language from Literary Machines. I have answered from the broader principles of symmetry, address-based type matching, open-ended types, and the universal applicability of substrate operations. If a specific mechanism in your implementation needs sharper Nelson-text grounding, the most relevant raw passages would be:

NEED_RAW: 4/30-4/31 (link instance numbering and order of arrival in full context), 4/58-4/60 (link search semantics and the "AND of the ORs" model)
