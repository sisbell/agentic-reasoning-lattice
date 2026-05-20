## Question 1 [theory]

> Was shape-conformance intended to be enforced at the substrate primitive K.λ directly (rejecting any class-(iii) emission of a registered type with non-conformant F/G), or as a relational-layer commitment that all class-(iii) emissions of registered types route through Emit_K?

The terms "K.λ," "Emit_K," "class-(iii) emission," and "F/G" don't appear anywhere in Literary Machines—these belong to a formalization layer your implementation has built on top of my specification. But the underlying design question I can answer with precision.

**My intent: no substrate-level enforcement of shape-conformance, full stop.**

The link mechanism I specified treats the type endset symmetrically with from-set and to-set—as an arbitrary address pointing anywhere in the docuverse. The substrate does not inspect what's at that address:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

If shape-conformance means "links of registered type T must exhibit structural constraints on from-set/to-set," then enforcing that at the substrate primitive would contradict the open-ended type system I designed:

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." [LM 4/43]

So between your two options, the answer is closer to the second (relational-layer commitment), but I must be honest: **I didn't specify any enforcement mechanism for type conformance at all.** I specified conventions and a tentative listing of standard types, with the explicit understanding that:

> "Standardization of a working set of link types is now a high priority, but has less priority than establishing a robust demonstration rig." [LM 4/52]

The philosophical reason matters. The whole point of "types are arbitrary addresses" was **extensibility without authority**. The moment K.λ (or any substrate primitive) can reject a link as "non-conformant," some entity decides what conformance means—and that entity becomes a committee gatekeeping the type vocabulary. That defeats user-definable types.

A relational-layer routing through Emit_K is more faithful to my design, because:
1. It preserves K.λ as a pure connective primitive (any three endsets, no validation)
2. It makes conformance a *commitment by the relational layer*, not a *guarantee by the substrate*
3. Non-routed emissions remain technically valid—just unblessed by the conformance checker
4. Multiple conformance regimes could coexist (different relational layers, different commitments)

This matches how I designed the system to handle other social-layer concerns. Authorship claims, supersession claims, even copyright—these live as link assertions that the community evaluates, not as system-enforced truths. Shape-conformance should be the same: a commitment users make through which paths they route their emissions, not a fence the substrate erects.

That said: if your implementation needs hard shape-conformance for engineering reasons (debuggability, consistency, query optimization), that's a defensible departure from my specification. Just be clear that it *is* a departure, and that it trades some of the type system's open-endedness for safety guarantees I did not require.

NEED_RAW: None. The question concerns a formalization beyond what Literary Machines specifies; the relevant Nelson material on type-system permissiveness is fully captured in [LM 4/43-4/45] above.
