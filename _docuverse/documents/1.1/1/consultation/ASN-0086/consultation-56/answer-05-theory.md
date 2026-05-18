## Question 5 [theory]

> Was L1c (LinkAllocatorConformance) intended as an existential conformance witness — that some T10a-conforming chain to the address exists in abstract tumbler space — or as a requirement that the chain's intermediate spawns be operationally executed (with their addresses thereby allocated)?

# On L1c (LinkAllocatorConformance): Existential, Not Operational

The terms "L1c" and "T10a" are spec-internal artifact names, not from Literary Machines. But the underlying design-intent question — does conformance require operational execution, or just abstract structural existence? — is one Literary Machines answers clearly.

## The Existential Reading Is the Intended One

Three textual pillars establish that tumbler-space conformance is fundamentally **conceptual/existential**, not operational:

### 1. Tumblers are a mapping mechanism, not an operational ledger

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17-4/18]

The conformance question is about whether an address is well-formed within the mapping — not whether anyone has "executed" intermediate operations.

### 2. Ghost elements: addresses exist without stored objects

> "The docuverse is the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage." [LM 4/23]

> "Thus the address population of tumbler-space is also an abstraction, since things may be addressed even though nothing is there to represent them in storage. Consider what we may call 'ghost elements'." [LM 4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [LM 4/23]

This is the decisive passage. If addresses can be **linked-to** despite no operational allocation having occurred, then conformance witnesses are existential, not operational.

### 3. Baptism is about rights, not execution

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17]

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

Baptism establishes the *authority* to allocate. It does not require that intermediate forks have been operationally instantiated. The owner of `2` controls `2.x` regardless of whether `2.1` through `2.754` were ever "executed."

## The One Caveat: Links Are Stored Entities

There is a wrinkle worth flagging:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links." [LM 4/23]

Links themselves are *not* ghost elements — they're real stored objects with sequential creation-order addresses:

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

So one could argue: for **link-to-link** chains, the intermediate links must actually exist (be stored), even though their *addresses* are existentially-witnessed by the tumbler structure.

But this distinction reinforces, rather than undermines, the existential reading of L1c. The conformance witness is about the address's well-formedness in tumbler-space — whether `2.755` is a valid allocation under owner `D.V.0.2` — not about whether 754 prior operational SPAWN events were executed.

## Conclusion

The design intent supports **existential conformance**: L1c should require that some T10a-conforming chain to the address *exists* in abstract tumbler space, derivable from the baptism/ownership structure. The operational execution of intermediate spawns is an implementation concern, not a conformance criterion. Nelson's entire design rests on the principle that the docuverse is "conceptually assigned positions" — and conformance lives at that conceptual layer.

**NEED_RAW: 4/26-4/40** — The tumbler-arithmetic pages may contain more precise formal language about address derivation rules that could refine this answer. The curated sources cover the philosophical intent but not necessarily every formal nuance of how addresses are computed/validated.
