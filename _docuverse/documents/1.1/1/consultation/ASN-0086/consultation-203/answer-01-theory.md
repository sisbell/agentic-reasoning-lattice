## Question 1 [theory]

> Was the link store designed as a substrate meant to be extended by higher relational layers, such that invariants like retraction-stability are intended to be guaranteed against future layer operations — or is each layer expected to re-establish its own guarantees?

## Short answer

Nelson designed the link store as a **universal substrate meant to be extended by composition**, not as a set of layers each re-proving its own guarantees. Higher relational structures (link-to-link, compound/faceted links, metalinks) are not new mechanisms — they are the *same* link primitive operating in the *same* universal address space, so they inherit the substrate's invariants rather than re-establishing them.

But there's an important caveat about whether Nelson explicitly *guarantees* invariants against future layer operations, which I flag at the end.

## The substrate-and-composition philosophy

The clearest design statement is in the link-to-link material. Higher layers exist precisely *because* nothing new is required:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." (4/49)

> "Complex relational structures, such as the faceted link (discussed in Chapter 2), may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." (4/51)

> "Note that this mechanism can be used for hierarchical link types, subtypes and supertypes. It is searchable for upper- and under-links, and all final data matter below; as well as for many other compound structures." (4/51)

The curated commentary on this draws out the intent directly: the system provides *one* primitive and lets users build on it, "rather than building specific features for 'link hierarchies' or 'link annotations' or 'link-type subtypes'... This follows Nelson's pattern of providing minimal powerful mechanisms rather than feature catalogues" (`prompts/.../link-to-link.md`). And: "This is not a special mechanism requiring new machinery - it falls out naturally from the universality of the addressing system."

This is a substrate-extension design. Relational layers are compositions, not separate subsystems with their own contracts.

## Why the core invariant is inherited, not re-proven

The survivability invariant (what your question calls "retraction-stability") is **structural** — it lives in how links attach to content, not in any layer:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

The symmetry of the design is what makes inheritance work: all three endsets behave identically. "Nelson generalizes the link structure by treating all three parts (from, to, type) identically... This symmetrical design means the system needs only one mechanism for all three" (`endsets.md`). Because a link-to-link uses the ordinary to-set pointing at a link's address —

> "The to-set of the link need simply point to the actual link address in the tumbler line, with a span of 1 to designate that unit only." (4/49)

— a meta-link is just an ordinary link, and the same survivability/addressing guarantees apply by construction. There is no layer boundary at which a guarantee would need re-establishing.

## The caveat — where this goes beyond what Nelson states

Two things to be precise about:

1. **"Retraction-stability" is not Nelson's term**, and Nelson never frames the design as "invariants guaranteed against *future layer operations*." What he establishes is the weaker, structural claim above: the substrate is universal and reusable, so higher structures compose from the same primitive. The *inference* that invariants therefore transfer is sound and matches his "minimal mechanisms" pattern — but it is inference, not an explicit Nelson guarantee.

2. **The survivability invariant is phrased for byte-spans** ("if anything is left at each end"), which assumes *partial* survival is meaningful. A link-to-link endpoint is a single unit (span of 1) pointing at a link, and a link can be deleted into a "not currently addressable" state (see `link-deletion.md`, 4/9, 4/12). Nelson does not explicitly work out whether/how the "if anything is left" rule behaves when the surviving target is an indivisible link rather than a divisible byte-span. So the *philosophy* (substrate inheritance) is clear, but the precise transfer of the survivability invariant to the link-to-link layer is underspecified in the text.

If you want me to verify whether Nelson addresses meta-link deletion semantics directly anywhere in the link chapter, that would be: NEED_RAW: 4/49-4/51 (the link-to-link pages, to confirm no additional invariant discussion beyond the curated extract).
