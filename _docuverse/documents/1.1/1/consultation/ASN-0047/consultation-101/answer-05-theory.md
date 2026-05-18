## Question 5 [theory]

> Does the hierarchical baptism design intend that placing an entity into E simultaneously activates its child sub-allocators (account-of-node, document-of-account), or are child sub-allocators activated by a separate event at the first descent?

# Answer

Neither, strictly speaking — the question presupposes a stored-object model that the design rejects.

Sub-allocators are not entities that get "activated." They are **inherent rights of ownership** over a region of tumbler-space. When you own address E, you implicitly own the entire subtree beneath it, and you may baptize sub-addresses at any time without any prior act.

The decisive evidence is the ghost-elements design (4/23):

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it." [LM 4/23]

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

If there's no stored object for the parent, there's nothing to carry an "activation flag" for the children. The address space below any owned address is conceptually populated whether anything sits there or not.

The baptism principle confirms this:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Allocation rights flow from ownership of the parent address — not from a separate enabling event. The "first descent" simply *is* the baptism (a single act that both names the child and asserts the owner's prerogative); it doesn't depend on a precursor activation of the sub-allocator.

**What this means practically:**
- Create account 1.2 → you can immediately baptize 1.2.1, 1.2.7, 1.2.999 with no further ceremony
- The capacity exists the moment ownership exists
- Sub-allocators don't have lifecycles; ownership rights do

**Caveat on intent vs. implementation:** I never explicitly addressed the activation-timing question in *Literary Machines* because, in my conceptual frame, the question doesn't arise — the address space is an abstraction, not a tree of allocator objects. An implementation that materializes sub-allocators as concrete objects is making a choice the spec doesn't constrain, so long as the user-visible guarantee holds: **whoever owns E can fork under E at any moment, without prior arrangement.**

NEED_RAW: 4/21 (the page between the "baptism" passage at 4/17 and the ghost-elements passage at 4/23) may contain additional discussion of allocation mechanics that would sharpen this further.
