## Question 1 [theory]

> Was the tumbler hierarchy designed to require a non-empty seed (e.g., a root node) at genesis, or is bootstrapping from an empty B₀ consistent with the design?

The tumbler hierarchy was designed to require a conceptual root, not bootstrap from a truly empty state. Two structural requirements make this explicit:

**The root digit is mandatory.** Nelson states: "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

**Forking requires an existing owned number.** "The basic principle is that of owned numbers... Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17] You cannot baptize sub-numbers under nothing.

**But "non-empty" is subtle** — the root needn't have stored content. Through ghost elements, "no specific element need be stored in tumbler-space to correspond to them... The docuverse is the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage." [LM 4/23]

So: **the design requires a conceptual seed (digit 1 as root), but not stored content at it.** An empty B₀ is consistent if it means zero stored bytes; inconsistent if it means no addressable root from which to fork.

NEED_RAW: 4/15-4/22 — to verify whether Nelson explicitly addresses genesis state or initial conditions of the tumbler line beyond what's in curated sources.
