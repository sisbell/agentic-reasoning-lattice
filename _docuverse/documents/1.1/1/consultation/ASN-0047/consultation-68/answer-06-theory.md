## Question 6 [theory]

> Is the choice n₀ = [1] structurally necessary for your design — does the specific digit "1" carry semantic content (e.g., the "refer to the entire docuverse by '1'" usage at LM 4/28) — or would any single-component positive tumbler `[c]` with c ≥ 1 serve equivalently as the bootstrap root?

The choice of `[1]` is **semantically loaded by design**, not arbitrary.

Nelson explicitly assigns the digit `1` two interlocking meanings that any other positive integer would fail to carry:

**1. Ancestral root of the docuverse**

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." (4/28)

The "1" is not an arbitrary label — it is the ancestor from which all other server nodes fork. Substituting `[2]` would break the descent relation Nelson invokes.

**2. "1-positions" as wildcard for "all of this level"**

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server—or the entire docuverse." (4/38)

This is the deeper structural use. The patterns `0.0.0.1`, `1.2.0.0.1`, `1.2.3.4.0.1` rely on `1` (after leading zeros) meaning "all of." A different bootstrap value would either collide with this wildcard convention or force a separate notation for "entire docuverse."

**The unified picture:**

> "So the docuverse is all really one big forking document." (4/18)

The forking-document metaphor requires a singular root. Nelson chose `1` so that root-identity and "select-all" semantics coincide in one digit.

**Conclusion:** Abstractly, the *tree algebra* works for any `[c]`, c ≥ 1 — forking, depth-first ordering, span subtrees, link survivability are all preserved. But the *Nelsonian conventions* (`1` as ancestor, `1` as wildcard) are bound to the specific digit. Choosing `[c]` with c ≠ 1 would preserve the structure but lose the designed semantic overloading at LM 4/28 and 4/38.
