## Question 9 [theory]

> For a Comment-shaped relation K paired with a Resolution-shaped relation K_res, was the design intent that K declare K_res in the shape registry (per-K co-registration), that K_res be an explicit parameter to templates like `unresolved_K_comments_via(K_res, d)`, or that all active Resolution tuples targeting τ count as resolving it?

The specific comment-resolution pairing pattern you describe isn't in *Literary Machines*. I never specified a "shape registry" or "co-registration" — those are later implementation terms. But the principles I established point unambiguously to your option #3: **all active Resolution-typed tuples targeting τ count as resolving it.**

Here's why, drawing on what I actually wrote:

**1. Types are open-ended, with no registry.** I was explicit: "the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose" [LM 4/43]. Per-K co-registration (option #1) would impose exactly the schema authority I argued against — "no schema changes, no registry, no committee" is the design.

**2. Type matching is by ADDRESS, not by declared relationship.** "The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address" [LM 4/44-4/45]. K_res is discovered by matching the Resolution type's address. Nothing about K declares it; nothing about a template parameter privileges it. The address itself is the discriminator.

**3. Search is universal across the home-set.** A link satisfies a search when "one span of each endset satisfies a corresponding part of the request." If you constrain the request to (type = K_res, to-set ∋ τ), every link in the world matching those constraints is returned. The home-set can be the entire docuverse — anyone's Resolution link counts. This is the same pattern as my **counterpart link** [LM 4/53] and **supersession link** [LM 4/52]: anyone can make a claim of correspondence or supersession; the system surfaces all such claims; users evaluate them.

**Where option #2 fits.** Passing K_res as a parameter to `unresolved_K_comments_via(K_res, d)` is acceptable as a *query convenience* — the front-end can scope its search — but it is not the *semantic basis* of resolution. The semantic basis is universal type-matching plus endset-matching. The template parameter merely names which type address to match.

**The deeper principle.** I designed link types so that social dynamics become visible in the link structure itself, not hidden in system fields. Resolution should work the same way: a Resolution-typed link targeting τ is a public, attributed, disputable claim. If someone disagrees that τ is resolved, they make their own link expressing that disagreement. The system doesn't arbitrate; it surfaces.

So: **K must not declare K_res; K_res must not be a privileged template parameter; any Resolution-typed tuple targeting τ resolves τ, modulo whatever filtering the front-end chooses to apply.** This is consistent with everything I built — tumblers, endsets, open-ended types, universal addressability.

NEED_RAW: [4/56-4/60 for full link-search filter mechanics; 4/50-4/52 for compound-link semantics that might bear on whether a Resolution can itself be link-to-link]
