## Question 7 [theory]

> Does the design specify a canonical structural form for the bootstrap node (e.g., a single-component tumbler), or is any tumbler with `zeros = 0` admissible as n₀?

# The Canonical Bootstrap Form

The design specifies a **single canonical bootstrap node** — the single-digit tumbler `1` — not "any tumbler with zeros = 0."

## Nelson's Specification

Nelson is explicit on this point at LM 4/28:

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position."

This establishes three things:

1. **The first digit must be `1`** — this is a structural requirement, not a convention
2. **All other servers descend from node `1`** through forking — so `1.2`, `1.3`, `1.2.3` are descendants, not alternative bootstraps
3. **The bare digit `1` refers to the entire docuverse** — making it the unique root

## Why Multi-Component Node Tumblers Aren't Bootstraps

Under Nelson's forking model (LM 4/19-4/20):

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism... New items may be continually inserted in tumbler-space while the other addresses remain valid."

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

Server `1.2` exists only because someone who owns `1` allocated it. So `1.2` cannot itself be n₀ — it presupposes n₀ = `1`. The tree has exactly one root.

## On the Implementation Framing

The phrase "zeros = 0" appears to be implementation terminology (referring to the count of major-divider zeros separating Node.0.User.0.Document.0.Element fields per LM 4/26-4/28). Nelson himself doesn't speak in those terms. But mapping it back to his design:

- A pure node tumbler (no zero separators) does satisfy "zeros = 0"
- But only **one** such tumbler — the digit `1` — is the bootstrap
- Other pure-node tumblers (`1.2`, `1.2.3`) are *interior nodes of the forking tree*, baptized by the owner of `1`

## Caveat on What Nelson Doesn't Address

Nelson does not use the term "bootstrap node" and does not formally axiomatize n₀ as a distinguished constant. He describes the tree's recursive structure and the requirement that all addresses begin with `1`. Whether the formal spec should treat n₀ as the constant tumbler `[1]` or as a parameterized root is a specification design choice Nelson didn't directly address.

NEED_RAW: 4/28 (raw 195) — to confirm there is no additional language qualifying "always begins with the digit 1" with allowances for alternative root structures.
