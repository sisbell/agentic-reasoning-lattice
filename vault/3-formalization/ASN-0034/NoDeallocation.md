**NoDeallocation (NoDeallocation).** The system defines no operation that removes an element from the set of allocated addresses. No "deallocate", "free", or "reclaim" mechanism exists. This is a design constraint, not a derived property.

Nelson: "any address of any document in an ever-growing network may be specified by a permanent tumbler address." The permanence guarantee requires that the allocated set can only grow — no mechanism exists to contract it.

*Formal Contract:*
- *Axiom:* The system's operation vocabulary contains no operation that removes an element from the allocated set.
