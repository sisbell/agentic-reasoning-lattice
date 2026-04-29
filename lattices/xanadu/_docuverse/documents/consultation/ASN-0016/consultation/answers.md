# Consultation Answers — Content Provenance

**Inquiry:** What must the system guarantee about tracing the origin and path of content? Given content at a location, what can be determined about where it came from, how it arrived, and its relationship to the same content appearing elsewhere?
**Date:** 2026-02-25 20:26
**Questions:** 23 (13 nelson, 10 gregory)

---

## Question 1 [nelson]

> **Inquiry** — Pose focused questions about specific design guarantees

### Nelson's Answer

I'm ready to answer questions about Xanadu's design intent, user-facing guarantees, and the philosophical principles behind the system as described in Literary Machines.

What would you like to know?

---

## Question 2 [nelson]

> **Discovery** — Extract requirements (R), judgments (J), and frame conditions (F) from source documents

### Nelson's Answer

I need to understand what ASN-0016 is about and review the transcripts before performing discovery. Let me start by checking the project structure and existing conventions.

**Tool Use: Read**
`path = "/Users/shane/.claude/projects/-Users-shane-Documents-github-claude-xanadu-spec/memory/MEMORY.md"`

**Tool Use: Glob**
`pattern = "vault/consultations/ASN-0016/**"`

**Tool Use: Glob**
`pattern = "vault/transcripts/ASN-0016-nelson-*/**"`

**Tool Use: Glob**
`pattern = "vault/consultations/ASN-002*/*.md"`

---

## Question 3 [nelson]

> **Specification** — Formalize into definitions and provable properties

### Nelson's Answer

Let me finish reading the files that were cut off.

<tool_call>
{"name": "Read", "arguments": {"file_path": "spec/14-allocation-order.md", "offset": 3000}}
</tool_call>

<tool_call>
{"name": "Read", "arguments": {"file_path": "spec/15-frame-conditions.md"}}
</tool_call>

<tool_result>
<result>
nt `D.k` is derived from document `D`.

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

**D-1207: Link allocation.** Links are allocated sequentially in the `0.2.x` subspace of the element field, in permanent order of arrival.

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

---

## Invariants

### Core Allocation Integrity

**J-0 (Monotonic Sibling Allocation):**
```
∀ parent tumbler p, ∀ siblings p.i and p.j:
  if p.i was allocated before p.j, then i < j
```
New siblings always get strictly increasing digit values.

**J-1 (Allocation Authority):**
```
∀ allocation of address p.k:
  the allocator must be owner(p) or an authorized delegate
```

**J-2 (No Retroactive Insertion):**
```
∀ parent p, ∀ existing siblings p.i, p.j where i < j:
  no new sibling p.k with i < k < j may be allocated after p.j exists
```
You cannot insert between existing siblings. New items go at the frontier.

**J-3 (Cross-Field Independence):**
```
∀ fields F₁ ≠ F₂ ∈ {Node, User, Document, Element}:
  allocation in F₁ does not affect allocation state in F₂
```

**J-4 (Allocation Permanence):**
```
∀ address a, ∀ time t₁ < t₂:
  if allocated(a, t₁) then allocated(a, t₂)
```
Once an address is allocated, it remains allocated forever.

**J-5 (Frontier Monotonicity):**
```
∀ parent p, ∀ time t₁ < t₂:
  frontier(p, t₁) ≤ frontier(p, t₂)
```
The allocation frontier only advances.

**J-6 (Ordering Consistency):**
```
∀ siblings p.i, p.j under same parent:
  allocation_time(p.i) < allocation_time(p.j) ⟺ i < j
```
Allocation order matches tumbler ordering for siblings.

### Version Allocation

**J-7 (Version Ancestry Encoding):**
```
∀ version v created by CREATENEWVERSION(source):
  v.address is a sub-tumbler of source.address in the Document field
```
The version's address structurally encodes its derivation.

### Link Allocation

**J-8 (Link Sequential Allocation):**
```
∀ document d, ∀ links l₁, l₂ in d:
  if l₁ created before l₂, then link_number(l₁) < link_number(l₂)
```
Links get sequential creation-order addresses in the `0.2.x` subspace.

**J-9 (Link Address Permanence):**
```
∀ link l in document d:
  l.address does not change after creation
  (deletion of other links does not renumber l)
```

### FEBE Operation Allocation Rules

**J-10 (Byte Allocation on INSERT):**
```
After INSERT(doc, pos, text):
  ∀ byte b in text:
    b receives a fresh I-address native to doc
    b.I-address was not in I-space before this operation
```

**J-11 (Byte Allocation on APPEND):**
```
After APPEND(doc, text):
  ∀ byte b in text:
    b receives a fresh I-address native to doc
    b.I-address extends doc's I-space contiguously
```

**J-12 (No Byte Reallocation on DELETE):**
```
After DELETEVSPAN(doc, span):
  ∀ byte b that was in span:
    b.I-address is unchanged
    b.I-address remains in I-space
    only the V-space mapping is removed
```

**J-13 (No Byte Reallocation on REARRANGE):**
```
After REARRANGE(doc, cuts):
  ∀ byte b in doc:
    b.I-address is unchanged
    only V-space position changes
```

**J-14 (COPY Preserves I-Addresses):**
```
After COPY(source_spec, dest_doc, dest_pos):
  ∀ byte b in source_spec:
    the V-position created in dest_doc maps to b's original I-address
    no new I-space content is allocated
```

### Cross-Boundary Independence

**J-15 (Cross-Document Allocation Independence):**
```
∀ documents d₁ ≠ d₂:
  allocation events in d₁ do not affect allocation state in d₂
  (each document has its own allocation frontier for bytes and links)
```

**J-16 (Cross-Server Allocation Independence):**
```
∀ servers s₁ ≠ s₂:
  allocation events on s₁ do not affect allocation state on s₂
  (each server has its own allocation frontier for accounts and documents)
```

### Uniqueness and Completeness

**J-17 (Allocation Uniqueness):**
```
∀ addresses a₁, a₂:
  if a₁ ≠ a₂ then the items at a₁ and a₂ are distinct
  (no two distinct items share an address; no address is allocated twice)
```

**J-18 (Allocation Density):**
```
∀ parent p with allocated siblings p.1 through p.k:
  all intermediate values p.1, p.2, ..., p.k are allocated
  (no gaps in sibling allocation within a single parent)
```

Note: This applies within a single allocation authority. Different parents may have different frontier values.

**J-19 (Forking Preserves Parent):**
```
∀ parent p, ∀ allocation of child p.k:
  the content and address of p are unchanged
  (creating children never modifies the parent)
```

**J-20 (Allocation is the Only Entry Point):**
```
∀ address a in the docuverse:
  a entered the docuverse through exactly one allocation event
  (no address appears spontaneously; every address has a creation record)
```

---

## Relationships Between Invariants

### Core Group
J-0, J-4, J-5, J-17 form the foundation:
- J-0: new items get increasing addresses
- J-4: addresses are permanent
- J-5: frontiers don't retreat
- J-17: addresses are unique

Together they guarantee that the tumbler tree grows monotonically with unique, permanent addresses.

### FEBE Interaction Group
J-10 through J-14 formalize how operations interact with allocation:
- J-10, J-11: INSERT/APPEND create new I-addresses
- J-12, J-13: DELETE/REARRANGE don't affect I-addresses
- J-14: COPY reuses existing I-addresses

### Distribution Group
J-15, J-16 ensure allocation works without coordination:
- Different documents allocate independently
- Different servers allocate independently

### Closure
J-20 closes the system: no address appears without an allocation event. Combined with J-17 (uniqueness), this means the set of addresses is exactly the set of items that have been allocated.

---

## Connection to Guarantees

| Allocation Invariant | Supports Guarantee |
|---------------------|-------------------|
| J-0, J-4, J-5 (monotonic, permanent, advancing) | G-1 (Permanence) |
| J-10, J-11 (fresh I-addresses on INSERT/APPEND) | G-2 (Attribution) |
| J-12, J-13, J-14 (no reallocation) | G-8 (Non-Destruction) |
| J-15, J-16 (cross-boundary independence) | PP-3 (Non-Interference) |
| J-17 (uniqueness) | G-2 (Attribution), PP-2 (Attribution Completeness) |
| J-8, J-9 (link sequential, permanent) | G-4 (Link Survival) |
</result>
</tool_result>

<tool_result>
<result>
# 15 — Frame Conditions

## Overview

A **frame condition** specifies what does NOT change when an operation executes. Frame conditions are essential for reasoning about system correctness: they guarantee that operations have bounded effects and don't silently corrupt unrelated state.

> "Without damaging the originals." [LM 2/45]

This principle — that operations on one thing don't damage another — requires formal specification of exactly what each operation leaves untouched.

---

## Definitions

**D-1300: Frame condition.** For an operation `op`, the frame condition `frame(op)` is the set of state components guaranteed to be unchanged after `op` executes.

**D-1301: Affected scope.** For an operation `op`, the affected scope `scope(op)` is the set of state components that `op` may modify. Everything outside `scope(op)` is in `frame(op)`.

```
frame(op) = SystemState \ scope(op)
```

**D-1302: Protected state.** State components that are in the frame condition of EVERY operation — they never change regardless of what operation runs.

```
ProtectedState = ∩{frame(op) | op ∈ AllOperations}
```

**D-1303: Cross-document isolation.** Operations on document `A` do not modify any state belonging to document `B` (where `A ≠ B`).

**D-1304: Cross-version isolation.** Operations on version `V` of document `D` do not modify state belonging to version `W` of `D` (where `V ≠ W`).

**D-1305: I-space monotonicity.** I-space content is in the protected state — it only grows, never shrinks or changes.

---

## System State Components

For frame condition analysis, the system state consists of:

| Component | Symbol | Description |
|-----------|--------|-------------|
| I-space content | `I` | All stored bytes (append-only) |
| V-space mappings | `V(d,v)` | V-to-I mapping for document `d`, version `v` |
| Link set | `L(d)` | Links whose home is document `d` |
| Link endsets | `E(l)` | The three endsets of link `l` |
| Document set | `D` | Set of all documents in the docuverse |
| Allocation state | `A(p)` | Allocation frontier for parent `p` |
| Journal | `J` | The operation journal (append-only) |

---

## Frame Conditions by Operation

### F-0: INSERT Frame

**Operation:** `INSERT(doc, pos, text)`

**Affected scope:**
- `V(doc, current)` — V-space of target document's current version (positions shift)
- `I` — grows (new bytes added)
- `A(doc)` — allocation frontier advances for new byte addresses
- `J` — new journal entry appended

**Frame (unchanged):**
- `V(doc', v)` for all `doc' ≠ doc` — other documents' V-spaces
- `V(doc, v)` for all `v ≠ current` — other versions of same document
- `L(d)` for all `d` — all link sets (no links created or destroyed)
- `E(l)` for all `l` — all link endsets (links attach to I-space, unaffected)
- All existing I-space content (new content added, none changed)
- `D` — document set unchanged (no documents created or destroyed)

```
F-0: After INSERT(doc, pos, text):
  ∀ doc' ≠ doc: V(doc', v) unchanged
  ∀ v ≠ current_version(doc): V(doc, v) unchanged
  ∀ link l: E(l) unchanged
  ∀ I-address a existing before INSERT: content(a) unchanged
  D unchanged
```

### F-1: DELETEVSPAN Frame

**Operation:** `DELETEVSPAN(doc, span)`

**Affected scope:**
- `V(doc, current)` — V-space mapping changes (span removed, positions shift)
- `J` — new journal entry

**Frame (unchanged):**
- `I` — ALL I-space content unchanged (deletion is V-space only)
- `V(doc', v)` for all `doc' ≠ doc`
- `V(doc, v)` for all `v ≠ current`
- `L(d)` for all `d`
- `E(l)` for all `l`
- `D`
- `A(p)` for all `p` — no allocation changes

```
F-1: After DELETEVSPAN(doc, span):
  I unchanged (no I-space content destroyed)
  ∀ doc' ≠ doc: V(doc', v) unchanged
  ∀ v ≠ current_version(doc): V(doc, v) unchanged
  ∀ link l: E(l) unchanged
  D unchanged
```

### F-2: COPY Frame

**Operation:** `COPY(source_spec, dest_doc, dest_pos)`

**Affected scope:**
- `V(dest_doc, current)` — V-space of destination grows (new mappings added)
- `J` — new journal entry

**Frame (unchanged):**
- `I` — no new I-space content (COPY reuses existing I-addresses)
- `V(source_doc, v)` for all versions — source document completely unchanged
- `V(doc', v)` for all `doc' ≠ dest_doc`
- `V(dest_doc, v)` for all `v ≠ current`
- `L(d)` for all `d`
- `E(l)` for all `l`
- `D`
- `A(p)` for all `p` — no allocation changes (no new I-addresses)

```
F-2: After COPY(source, dest_doc, dest_pos):
  I unchanged (no new content created)
  Source document completely unchanged
  ∀ doc' ≠ dest_doc: V(doc', v) unchanged
  ∀ v ≠ current_version(dest_doc): V(dest_doc, v) unchanged
  ∀ link l: E(l) unchanged
  D unchanged
```

### F-3: REARRANGE Frame

**Operation:** `REARRANGE(doc, cuts)`

**Affected scope:**
- `V(doc, current)` — V-space ordering changes (regions transposed)
- `J` — new journal entry

**Frame (unchanged):**
- `I` — completely unchanged
- `V(doc', v)` for all `doc' ≠ doc`
- `V(doc, v)` for all `v ≠ current`
- `L(d)` for all `d`
- `E(l)` for all `l`
- `D`
- `A(p)` for all `p`

```
F-3: After REARRANGE(doc, cuts):
  I unchanged
  ∀ doc' ≠ doc: V(doc', v) unchanged
  ∀ v ≠ current_version(doc): V(doc, v) unchanged
  ∀ link l: E(l) unchanged
  D unchanged
  The SET of V-to-I mappings is unchanged; only their ORDERING changes
```

Note: REARRANGE is a pure permutation. The V-to-I mapping as a set of (position, I-address) pairs doesn't change — only which position maps to which I-address changes.

### F-4: APPEND Frame

**Operation:** `APPEND(doc, text)`

**Affected scope:**
- `V(doc, current)` — V-space extends at the end
- `I` — grows (new bytes added)
- `A(doc)` — allocation frontier advances
- `J` — new journal entry

**Frame (unchanged):**
- All EXISTING V-space positions in doc (no shifting — append is at end)
- `V(doc', v)` for all `doc' ≠ doc`
- `V(doc, v)` for all `v ≠ current`
- `L(d)` for all `d`
- `E(l)` for all `l`
- All existing I-space content
- `D`

```
F-4: After APPEND(doc, text):
  All existing V-positions in doc unchanged (no shift)
  ∀ doc' ≠ doc: V(doc', v) unchanged
  ∀ v ≠ current_version(doc): V(doc, v) unchanged
  ∀ link l: E(l) unchanged
  ∀ I-address a existing before APPEND: content(a) unchanged
  D unchanged
```

APPEND is strictly less disruptive than INSERT: it doesn't shift any existing V-positions.

### F-5: MAKELINK Frame

**Operation:** `MAKELINK(doc, from_set, to_set, three_set)`

**Affected scope:**
- `L(doc)` — link set of home document grows (new link added)
- `A(doc)` — link allocation frontier advances
- `J` — new journal entry

**Frame (unchanged):**
- `I` — no content changes
- `V(d, v)` for all documents `d` and versions `v` — no V-space changes
- `L(doc')` for `doc' ≠ doc` — other documents' link sets
- `E(l)` for all existing links `l` — existing links' endsets
- `D`

```
F-5: After MAKELINK(doc, from, to, type):
  I unchanged
  ∀ d, v: V(d, v) unchanged
  ∀ doc' ≠ doc: L(doc') unchanged
  ∀ existing link l: E(l) unchanged
  D unchanged
```

MAKELINK is purely additive: it adds one link and changes nothing else.

### F-6: CREATENEWDOCUMENT Frame

**Operation:** `CREATENEWDOCUMENT()`

**Affected scope:**
- `D` — document set grows (new document added)
- `A(parent)` — allocation frontier for the parent (user/account) advances
- `J` — new journal entry

**Frame (unchanged):**
- `I` — no content changes
- `V(d, v)` for all existing documents — no V-space changes
- `L(d)` for all existing documents — no link changes
- `E(l)` for all links — no endset changes

```
F-6: After CREATENEWDOCUMENT():
  I unchanged
  ∀ existing doc d: V(d, v) unchanged, L(d) unchanged
  ∀ link l: E(l) unchanged
  Only D grows by one empty document
```

### F-7: CREATENEWVERSION Frame

**Operation:** `CREATENEWVERSION(source_doc)`

**Affected scope:**
- `D` — document set grows (new version-document added)
- `V(new_doc, initial)` — new document gets V-space (copy of source's current V-space)
- `A(source_doc)` — version allocation frontier advances
- `J` — new journal entry

**Frame (unchanged):**
- `I` — no content changes (new version shares I-space with source)
- `V(source_doc, v)` for all versions — source document completely unchanged
- `V(doc', v)` for all `doc' ≠ source_doc` and `doc' ≠ new_doc`
- `L(d)` for all existing documents — no link changes
- `E(l)` for all links — no endset changes

```
F-7: After CREATENEWVERSION(source):
  I unchanged (V-space references existing I-addresses)
  V(source, v) unchanged for all versions
  ∀ doc' ∉ {source, new_doc}: V(doc', v) unchanged
  ∀ d: L(d) unchanged
  ∀ l: E(l) unchanged
```

### F-8: Read Operations Frame

**Operations:** `RETRIEVEV`, `RETRIEVEDOCVSPAN`, `RETRIEVEDOCVSPANSET`, `FINDLINKSFROMTOTHREE`, `FINDNUMOFLINKSFROMTOTHREE`, `FINDNEXTNLINKSFROMTOTHREE`, `RETRIEVEENDSETS`, `SHOWRELATIONOF2VERSIONS`, `FINDDOCSCONTAINING`

**Affected scope:** Nothing (read-only).

**Frame:** ALL state components unchanged.

```
F-8: After any read operation:
  I unchanged
  ∀ d, v: V(d, v) unchanged
  ∀ d: L(d) unchanged
  ∀ l: E(l) unchanged
  D unchanged
  A(p) unchanged for all p
  J unchanged (read operations are not journaled)
```

---

## Protected State

**D-1306: Protected state** — state that NO operation can change:

From the intersection of all frame conditions:

```
ProtectedState = {
  existing I-space content    (only INSERT/APPEND add; nothing removes or modifies)
  existing link endsets       (no operation modifies an existing link's endsets)
  existing document addresses (no operation changes a document's address)
  existing allocation history (past allocations are permanent)
}
```

Note: This is distinct from "state that grows." I-space, the link set, and the document set all grow but never shrink. The protected state includes their pre-existing contents.

---

## Cross-Document Isolation Theorem

**R-0 (Frame Condition Completeness):** Every FEBE operation has an explicit frame condition, and the union of all affected scopes is bounded.

From the frame conditions F-0 through F-8:

**Theorem (Cross-Document Isolation):**
```
∀ operation op on document A, ∀ document B ≠ A:
  V(B, v) unchanged for all v
  L(B) unchanged
```

**Proof:** By inspection of F-0 through F-7, every write operation's affected scope includes only the target document's V-space, link set, and potentially I-space (growth only). No operation includes another document's V-space or link set in its affected scope. ∎

This is the formal basis for PP-3 (Non-Interference).

---

## Composition of Frame Conditions

When multiple operations execute sequentially, the overall frame condition is the intersection of individual frame conditions:

```
frame(op₁ ; op₂) = frame(op₁) ∩ frame(op₂)
```

For operations on different documents:
```
If op₁ targets doc₁ and op₂ targets doc₂ where doc₁ ≠ doc₂:
  frame(op₁ ; op₂) includes V(doc₃, v) for all doc₃ ∉ {doc₁, doc₂}
  and I-space content existing before both operations
```

For operations on the same document:
```
If op₁ and op₂ both target doc:
  frame(op₁ ; op₂) includes V(doc', v) for all doc' ≠ doc
  and I-space content existing before both operations
  but V(doc, current) may be modified by both
```

---

## Connection to Guarantees

| Frame Condition | Supports |
|----------------|----------|
| F-0, F-1, F-2, F-3, F-4 (I-space in frame) | G-8 (Non-Destruction) |
| F-0..F-7 (other docs in frame) | PP-3 (Non-Interference) |
| F-0..F-5 (link endsets in frame) | G-4 (Link Survival) |
| F-1, F-2, F-3 (I unchanged) | G-1 (Permanence) |
| F-8 (reads change nothing) | G-9 (Privacy compatible) |
| All (existing I-space protected) | G-3 (Historical Backtrack) |
</result>
</tool_result>

Good. Now I have a complete picture of the existing specification. The spec already has 16 files (00-15) covering primitives through frame conditions. The question is: what formalization work remains?

Let me check what the Nelson persona identified and what gaps exist.

<tool_call>
{"name": "Read", "arguments": {"file_path": "vault/transcripts/ASN-0016-nelson-1/transcript.md", "offset": 0, "limit": 3000}}
</tool_call>

<tool_call>
{"name": "Grep", "arguments": {"pattern": "NEED_RAW|TODO|FIXME|unspecified|gap|missing", "path": "spec", "include": "*.md"}}
</tool_call>

<tool_result>
<result>
# ASN-0016 Session 1: Tumbler Arithmetic Edge Cases

## Date: 2025-07-05

## Participants
- Shane (interviewer)
- Ted Nelson (persona)

## Transcript

### Shane
Ted, the specification formalizes tumbler ordering as lexicographic with the shorter-prefix rule. But there are edge cases we'd like your perspective on. First: what happens when you compare tumblers across major dividers? For example, is `1.0.2` less than `1.0.3`?

### Ted Nelson
Of course `1.0.2` is less than `1.0.3`. The zeros are just punctuation — they separate the fields, but the ordering still works digit by digit. The tumbler `1.0.2` has digits `(1, 0, 2)` and `1.0.3` has digits `(1, 0, 3)`. Compare position by position: first digits equal (1=1), second digits equal (0=0), third digits 2 < 3. Therefore `1.0.2 < 1.0.3`.

The zeros don't break the ordering. They are PART of the tumbler, not special in terms of comparison. They're special only in terms of INTERPRETATION — they tell you which field you're in.

### Shane
So the ordering treats zeros as ordinary digits for comparison purposes, even though they have semantic significance as field separators?

### Ted Nelson
Precisely. The ordering is PURELY lexicographic on the digit sequence. The semantic interpretation of those digits — which ones are field separators, which field you're in — is a layer on top of the ordering. The ordering itself knows nothing about fields.

This is important because spans must work correctly across field boundaries. A span from `1.0.1` to `1.0.5` covers everything on node 1 for accounts 1 through 5. The ordering makes this natural — you don't need special logic for cross-field spans.

### Shane
What about tumblers of different lengths where one is a prefix of the other? The spec says `(1, 2)` comes before `(1, 2, 3)`. Is this correct?

### Ted Nelson
Yes. Think of the tumbler tree. Node `(1, 2)` is the PARENT of node `(1, 2, 3)`. In depth-first traversal — which is what the tumbler line represents — you visit the parent before its children. So `(1, 2)` comes before `(1, 2, 1)`, which comes before `(1, 2, 2)`, and so on.

This is essential for spans. A span starting at `(1, 2)` includes the parent AND all its descendants. If the parent came after its children, spans wouldn't capture subtrees correctly.

### Shane
One more edge case: what about the empty tumbler? The spec defines it as the root of the tree.

### Ted Nelson
The empty tumbler is a theoretical concept — the root from which everything descends. In practice, the smallest meaningful tumbler is `(1)`, which is the root server. But mathematically, yes, the empty tuple is the root.

For the specification, I'd say: define it formally but note that it has no physical realization in the system. No one addresses the empty tumbler. It's the mathematical starting point, like zero in the natural numbers — real but not a counting number you'd use for addressing.

### Shane
Let's move to tumbler arithmetic. The spec defines addition and subtraction. What about multiplication or division?

### Ted Nelson
There is no tumbler multiplication or division. Tumblers are not traditional numbers. They are tree addresses. You can:

1. COMPARE them (ordering)
2. ADD a difference to an address (move forward on the line)
3. SUBTRACT to get a difference (measure a span)

That's it. Multiplication makes no sense — what would "three times the address of a server" mean? Nothing. These are addresses, not quantities.

The arithmetic is minimal by design. We need just enough to manipulate spans efficiently. Anything beyond comparison, addition, and subtraction would imply that tumblers are numbers, which they are not. They are structured addresses with a convenient arithmetic.
</result>
</tool_result>

<tool_result>
<result>
spec/11-economics.md: The following are NOT specified by Nelson:
spec/11-economics.md: - What happens when storage rental lapses
spec/11-economics.md: - Grace periods for unpaid storage
spec/11-economics.md: - Minimum storage period requirements
spec/11-economics.md: - Disposition of anonymous publisher royalties
spec/11-economics.md: - How inflation affects fixed nib rates
spec/11-economics.md: - Whether storage costs decrease with technology
</result>
</tool_result>

Now I have the full picture. The specification is well-developed across 16 files. Let me now fulfill the user's request: formalize into definitions and provable properties, speaking as Ted Nelson.

Given the extensive existing spec, I should focus on what's missing or could be strengthened. Let me identify the key areas.

<tool_call>
{"name": "Grep", "arguments": {"pattern": "^## |^### |^#", "path": "spec/09-guarantees.md"}}
</tool_call>

<tool_result>
<result>
# 09 — Guarantees
## System Guarantees
## G-1: Permanence
## G-2: Attribution
## G-3: Historical Backtrack
## G-4: Link Survival
## G-5: Ownership
## G-6: Quotation Freedom
## G-7: Link Freedom
## G-8: Non-Destruction
## G-9: Privacy
## G-10: Automatic Royalty
## G-11: Correspondence
## G-12: Publication Permanence
## Guarantee Dependencies
</result>
</tool_result>

The specification is comprehensive. Now let me respond as Ted Nelson to the formalization request, identifying what's been done, what's correct, and what needs refinement or addition.

---

Here is my assessment and formalization contribution, speaking as the designer of the system.

## Assessment of the Current Specification

Your specification across `spec/01-primitives.md` through `spec/15-frame-conditions.md` captures the mechanical structure well. The 12 guarantees, 5 provable properties, journaling model, allocation invariants, and frame conditions form a rigorous foundation. I want to address what the formalization gets right, what it subtly misses, and what remains to be formalized.

## What the Formalization Gets Right

**The I-space/V-space separation is correctly foundational.** You've captured the central insight: content is permanent (I-space), arrangement is flexible (V-space), and the mapping between them is what constitutes a document. This is not just a data structure decision — it is the architectural expression of the principle that literature evolves without losing its past.

**Non-interference is correctly proved from frame conditions.** The Cross-Document Isolation Theorem in `spec/15-frame-conditions.md` is precisely what I meant by "without damaging the originals" [LM 2/45]. The proof by inspection of F-0 through F-7 is sound.

**Royalty correctness follows from attribution completeness.** The chain PP-1 → PP-2 → PP-5 in `spec/12-provable-properties.md` captures why the economic model works: every byte has exactly one home, every home has exactly one owner, therefore royalties partition without loss.

## What Needs Strengthening

### 1. Transclusion Depth Termination

The spec notes that transclusion depth is unlimited (P-0604) but does not prove that resolution terminates. This matters because a compound document can transclude from other compound documents indefinitely [LM 2/36]:

> "A document may have a window to another document, and that one to yet another, indefinitely."

The resolution DOES terminate because every transclusion chain ultimately reaches native bytes — content stored at its home I-address. The V-to-I mapping of any document resolves to I-addresses, and I-addresses are content, not further references.

**Property (Transclusion Termination):**
```
∀ V-position p in any document d:
  μ(p) resolves to an I-address containing data
  in at most 1 step (V-to-I mapping is direct, not chained)
```

The key insight is that COPY does not create a reference to a reference. It creates a V-space mapping directly to the I-address of the source bytes. Even if the source bytes are themselves transcluded in the source document, the COPY operation resolves through the source's V-to-I mapping and records the final I-address. There is no chain of indirection in I-space.

This is already implicit in the COPY frame condition (F-2) and the definition of transclusion (D-0601), but should be stated as an explicit property.

### 2. Refractive Link Following — Formal Specification

The spec defines refractive link following (D-0505) but does not formalize the algorithm. From [LM 2/26]:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version."

**Definition (Refractive Resolution):**
```
Given link l with from-set F pointing to I-addresses {i₁, ..., iₖ},
and target version v with V-to-I mapping μ_v:

refract(l, v) = {p ∈ dom(μ_v) | μ_v(p) ∈ {i₁, ..., iₖ}}
```

This is computable because:
1. The link's from-set resolves to I-addresses (via the version it was created against)
2. The target version's V-to-I mapping is available (PP-1, Referential Integrity)
3. The inverse mapping (I-address → V-positions in target) is enumerable

**Property (Refractive Completeness):**
```
∀ link l, ∀ version v:
  refract(l, v) contains every V-position in v that maps to
  an I-address referenced by any endset of l
```

**Property (Refractive Correctness):**
```
∀ position p ∈ refract(l, v):
  the content at p in version v is identical to the content
  originally referenced by l (same I-address, therefore same bytes)
```

### 3. Link Search Satisfaction — Formal Model

The spec quotes Nelson's satisfaction criterion (D-0406) but doesn't formalize the full search model. From [LM 4/58]:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request."

**Definition (Search Request):**
```
A search request R = (H, F, T, Θ) where:
  H = home constraint (span-set)
  F = from-set constraint (span-set)  
  T = to-set constraint (span-set)
  Θ = type constraint (span-set)
```

**Definition (Link Satisfaction):**
```
Link l satisfies request R = (H, F, T, Θ) iff:
  home(l) ∈ H
  ∧ fromSet(l) ∩ F ≠ ∅
  ∧ toSet(l) ∩ T ≠ ∅
  ∧ typeSet(l) ∩ Θ ≠ ∅
```

Where `∩` means "at least one span of the endset overlaps with the constraint." A "wildcard" constraint (the entire docuverse) trivially satisfies.

**Property (Search Independence):**
```
∀ request R, ∀ links l₁, l₂:
  whether l₁ satisfies R is independent of whether l₂ satisfies R
```

This is what Nelson means by "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS" [LM 4/60]. The search is a filter, not a scan that degrades with noise.

### 4. Ghost Element Interaction with Search

Ghost elements (D-0105) need clearer interaction with link search. From [LM 4/23]:

> "A link to or search of an account or node will find any of the documents under it."

**Property (Ghost Element Subsumption):**
```
∀ ghost element g at address a,
∀ link l with endset e containing span s:
  if s ⊆ subtree(a) then l satisfies a search constraint targeting a
```

A search targeting a ghost element (account, server) matches any link whose relevant endset falls within the subtree rooted at that ghost's address. This is why spans work hierarchically — a constraint on an account address matches links to any document in that account.

### 5. Window Mode Formalization

The spec defines two window modes (D-0604, D-0605) but notes that the FEBE COPY command doesn't explicitly have a mode parameter. This gap should be formalized.

**Definition (Window Reference):**
```
A transclusion reference r = (source_doc, source_span, mode) where:
  mode ∈ {FIXED, FLOATING}
  
FIXED: r resolves to μ_v(source_span) at the version v current
       at creation time of r. Resolution is stable.
       
FLOATING: r resolves to μ_current(source_span) using the source
          document's current version. Resolution evolves.
```

**Property (Fixed Window Stability):**
```
∀ fixed reference r created at time t:
∀ time t' > t:
  resolve(r, t') = resolve(r, t)
```

**Property (Floating Window Currency):**
```
∀ floating reference r to source document s:
∀ time t:
  resolve(r, t) = μ_current(s,t)(source_span)
```

From [LM 2/37]:

> "at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically."

## Summary of What Exists vs. What's Needed

| Area | Status | File |
|------|--------|------|
| Primitives (humbers, tumblers) | Complete | `spec/01-primitives.md` |
| Address spaces (I/V, ghost) | Complete | `spec/02-addresses.md` |
| Content (bytes, spans, span-sets) | Complete | `spec/03-content.md` |
| Documents (ownership, states) | Complete | `spec/04-documents.md` |
| Links (3-endset, types, survival) | Complete | `spec/05-links.md` |
| Versions (correspondence, prismatic) | Complete | `spec/06-versions.md` |
| Transclusion (windowing, compound) | Mostly complete; needs termination proof | `spec/07-transclusion.md` |
| FEBE protocol | Complete | `spec/08-protocol.md` |
| Guarantees (G-1 through G-12) | Complete | `spec/09-guarantees.md` |
| Network (BEBE, distribution) | Complete | `spec/10-network.md` |
| Economics (royalties, franchise) | Complete with noted gaps | `spec/11-economics.md` |
| Provable properties (PP-1 through PP-5) | Complete | `spec/12-provable-properties.md` |
| Operation journaling | Complete | `spec/13-operation-journaling.md` |
| Allocation order | Complete | `spec/14-allocation-order.md` |
| Frame conditions | Complete | `spec/15-frame-conditions.md` |
| **Refractive link following** | **Needs formalization** | — |
| **Link search model** | **Needs formalization** | — |
| **Ghost element search semantics** | **Needs formalization** | — |
| **Window mode formalization** | **Needs formalization** | — |
| **Transclusion termination proof** | **Needs explicit statement** | — |

The specification's structural integrity is sound. The guarantee dependency graph in `spec/09-guarantees.md` correctly identifies G-8 (Non-Destruction) as foundational, with G-1, G-3, and G-4 depending on it. The provable properties in `spec/12-provable-properties.md` correctly show PP-1 (Referential Integrity) as the most fundamental, with PP-4 and PP-5 depending on it.

The five items I've identified above would close the remaining formal gaps between Nelson's design intent and the specification's provable properties. Shall I draft them as a new spec file?

---

## Question 4 [nelson]

> Must the system guarantee that every unit of content can be traced back to a single, identifiable origin — the user who stored it, the moment of storage, and the document in which it first appeared?

### Nelson's Answer

# Origin Traceability: What Xanadu Guarantees

The answer is **partially yes** — two of the three components are structurally guaranteed, one is not, and there is a significant caveat about verification.

## 1. The Document in Which Content First Appeared — YES (Structural)

This is the strongest guarantee. Every byte's permanent I-space address encodes its origin document:

```
Node.0.User.0.Document.0.Element
```

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

This is not metadata that can be stripped — it is the address itself. To fetch content, the system must request it from its home location. Transclusion maintains this connection by referencing the original I-address rather than copying bytes. The connection is unforgeable within the system because the fetching mechanism requires it.

Content identity is also based on *creation*, not *value*. Two users independently typing the same text produce different I-addresses. Transcluded content shares the original I-address. This is how the system distinguishes "wrote the same words" from "quoted from the original."

## 2. The User Who Stored It — YES (Structural), But May Be Anonymous

The User field is part of the tumbler address, so every byte structurally traces to an account:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

However, Nelson explicitly permits anonymous publication:

> "Normally publication will be by accountable individuals and companies with known residence or place of business. Still, there is no reason that anonymous publication by walk-in and transient users of this system should not be allowed. We may call this 'John Doe publication.'" [LM 2/60]

So the system traces to an *account*, but that account may belong to a "John Doe" — a walk-in transient who never identified themselves. The structural traceability is to an address in tumbler-space, not necessarily to a real-world person.

## 3. The Moment of Storage — NO (Not Structural)

This is where the guarantee breaks down. Nelson explicitly excludes time from the address:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

Time is metadata, not structure. It can be used for filtering (e.g., "What links came in from last week?"), and links "will be dated" [LM 4/55], but the timestamp is not part of the permanent address that identifies content. The I-address tells you *where* content lives, not *when* it arrived.

The append-only storage model does impose a chronological ordering — content is "filed, as it were, chronologically" [LM 2/14] — so creation order is implicit in I-address sequence. But this is ordering, not timestamping. You can determine that byte A was stored before byte B (lower I-address), but not the absolute time of either.

## The Verification Caveat

Even for the two guarantees that hold structurally, Nelson provides **no cryptographic verification**:

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." [LM 5/17]

> "Storage Vendor makes no guarantee as to the correctness or authenticity of any material received from other Users." [LM 5/18]

The system's trustworthiness depends entirely on trusting the Storage Vendor franchise. If the vendor is honest, the I-address faithfully encodes origin. If compromised, there is no technical backstop. Nelson's architecture is pre-cryptographic — his solution to trust is social and contractual, not mathematical.

## Summary

| Component | Guaranteed? | Mechanism |
|-----------|------------|-----------|
| Document of first appearance | **Yes** — structural | I-address encodes home document |
| User who stored it | **Yes** — structural, but may be anonymous | I-address encodes owning account |
| Moment of storage | **No** — metadata only | "Time is kept track of separately" |
| Verification of all above | **No** — trust-based | Relies on Storage Vendor honesty |

The system guarantees that every byte can be traced to its origin *document* and *account* — this is structural, encoded in the address, and cannot be severed by any operation within the system. But the *moment* of storage is not part of that structural guarantee, and *verification* of the entire chain depends on contractual trust rather than technical proof.

---

## Question 5 [nelson]

> When the same content appears in multiple documents through sharing, must the system be able to produce, on demand, the complete list of all documents currently containing that content?

### Nelson's Answer

# Yes — FINDDOCSCONTAINING Is an Explicit System Requirement

Nelson specifies this capability as one of the 17 core FEBE operations in XU.87.1. It is not optional or aspirational — it is part of the protocol definition.

## The Operation

**FINDDOCSCONTAINING** is defined on pages 4/63 and 4/70:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

Two things to note about the wording:

1. **"All documents"** — not "some," not "up to N," not "best effort." The complete list.
2. **"Regardless of where the native copies are located"** — this works across the entire docuverse, not just the local server.

## Why This Must Exist

The operation is structurally necessary because of how transclusion works. When content is transcluded (COPY operation), the new document's V-space maps to the *same* I-space addresses as the original. The system tracks these shared I-addresses, which is what makes FINDDOCSCONTAINING possible — it searches for all V-space mappings that reference a given I-space region.

Nelson makes the user-facing expectation explicit in his discussion of windowing:

> "it must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/37 area, from the `windowing` concept]

And from the transclusion design intent, the user guarantee includes:

> "You can find all documents that contain it (via transclusion)"

## How It Works Architecturally

The I-space/V-space separation makes this feasible. Content identity is based on I-addresses, not on textual similarity. Two documents that independently type the same words have *different* I-addresses. Two documents where one transcludes from the other share the *same* I-addresses. So FINDDOCSCONTAINING is a structural query on shared I-space origin — not a text-matching search.

From the concept-operation mapping in `i-space-v-space`:

> **FINDDOCSCONTAINING** — "Searches I-space origin, returns V-space locations"

## Summary

The system **must** produce the complete list of all documents currently containing shared content. This is specified as a core protocol operation (FINDDOCSCONTAINING), follows necessarily from the I-space/V-space architecture, and is part of the user-facing guarantee that attribution and provenance are always discoverable.

---

## Question 6 [nelson]

> Given content found in a document, must the system be able to determine whether that content originated in that document or arrived through transclusion from another document — and if so, identify the source?

### Nelson's Answer

## Yes — absolutely, and it is structural, not optional

The system **must** be able to distinguish content that originated in a document ("native bytes") from content that arrived through transclusion ("inclusions" or "virtual copies"), and it **must** be able to identify the source. This is not a feature bolted on top — it is how the addressing and retrieval mechanism works.

---

### The Native/Non-Native Distinction

Nelson explicitly defines two categories of bytes in any document's virtual byte stream:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The system knows which bytes are native and which are inclusions because this distinction is inherent in the I-space addressing structure. Native bytes have I-addresses under the document's own address subtree. Transcluded bytes have I-addresses under some *other* document's subtree. The I-address itself encodes the home document:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

The **Document field** of every I-address tells you which document created that byte. This is not metadata attached to the byte — it is the byte's permanent identity.

---

### The User-Facing Guarantee

Nelson states this as an unconditional guarantee:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This appears in his description of windowed (compound) documents, where content from multiple sources is assembled into a single view. Even in a deeply nested compound document — layers of glass with windows through windows — the system can always trace any character back to its origin.

---

### How It Works Mechanically

The COPY operation (which implements transclusion) does not duplicate content. It creates a V-space mapping that points to existing I-space content:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

When the system resolves a V-address, it maps through to an I-address. If that I-address falls under the current document's address subtree, the byte is native. If it falls under a different document's subtree, it is an inclusion — and the document field of that I-address identifies the source.

This means:

| Content type | I-address location | How retrieved |
|---|---|---|
| **Native bytes** | Under this document's address | "found directly in storage under its control" |
| **Inclusions** | Under another document's address | "obtained by front-end or back-end requests to their home locations" |

The retrieval mechanism itself requires knowing the source — you cannot fetch transcluded content without knowing where it lives.

---

### The Reverse Lookup

The FEBE protocol includes a dedicated operation for the reverse question — given some content, find all documents that contain it:

> "FINDDOCSCONTAINING: This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

This enables discovering every document that transcludes a given piece of content, regardless of where those documents are in the docuverse.

---

### Why This Matters

Origin traceability is not incidental — it is the foundation for several of Nelson's core guarantees:

1. **Attribution**: Authors get credit because the I-address proves origin
2. **Royalties**: The system knows whom to pay because the I-address identifies the owner
3. **Correspondence**: Version comparison works because shared I-addresses reveal which parts are the same across versions
4. **Non-destruction**: "Modifications never damage originals" because transclusion references the original rather than copying it

As stated in the origin-traceability design intent: "In Xanadu, the origin IS the address. To fetch the content, the system must request it from its home location. The connection cannot be severed because the fetching mechanism requires it."

---

### Content Identity vs. Content Value

One important nuance: the system distinguishes origin structurally, not by content comparison.

Two documents containing identical text created independently have **different** I-addresses. Transcluded content **shares** the same I-address as the original. This is how the system distinguishes "wrote the same words independently" from "quoted from the original" — it is identity by provenance, not by value.

> "Non-native bytes are as much a logical part of a document as native bytes." [LM 4/11]

They appear identically in the V-stream. The distinction is invisible to the casual reader but always discoverable through the I-address.

---

## Question 7 [nelson]

> Must the derivation history of a document's versions preserve enough detail to trace exactly which content was added, removed, or rearranged at each step in the version chain?

### Nelson's Answer

# Derivation History in Xanadu's Version Model

## Short Answer

Nelson requires that every previous version state be **reconstructable** and that **correspondence between versions be computable**. But he does not explicitly require that the *sequence of edit operations* (insert, delete, rearrange) be stored as a replayable log. The architecture achieves traceability through a different mechanism: append-only I-space content plus versioned V-space mappings, from which "what changed" can be *derived* rather than *recorded*.

## What Nelson Explicitly Requires

### 1. Every Previous State Must Be Recoverable

Nelson is unequivocal that every version state must be reconstructable on demand:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

> "The user of such a system may scroll through an individual document, at successive instants of time, alive in the space-time vortex." [LM 2/15]

The guarantee is temporal completeness: you can ask for "a certain part of a certain version at a certain point in time" and get it.

### 2. Correspondence Between Versions Must Be Computable

The SHOWRELATIONOF2VERSIONS operation is specified to return exactly what matches:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

And Nelson frames this capability as essential, not optional:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

### 3. Changes Are Stored Individually and Chronologically

Nelson's storage model is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." [LM 2/15]

## What Nelson Does NOT Explicitly Require

### The Operation Log Distinction

There is a critical distinction between:

1. **State reconstruction** — Given version N, reconstruct its complete V-space arrangement
2. **Operation replay** — Know that "at step 3, the user inserted 'hello' at position 7, then at step 4 deleted positions 12-15, then at step 5 rearranged..."

Nelson's architecture guarantees (1) but does not explicitly require (2).

The mechanism is structural rather than journaled:

- **I-space** is append-only: new content gets permanent addresses; nothing is overwritten [LM 4/11]
- **V-space** is the current arrangement: each version defines a mapping from V-positions to I-addresses [LM 4/10-4/11]
- **Correspondence** is computed from shared I-space origin, not from a stored edit log [LM 4/70]

When SHOWRELATIONOF2VERSIONS compares two versions, it identifies matching spans by their shared I-addresses. It does not replay a sequence of edits. The system knows *what* corresponds — but it derives this from the structure, not from a recorded history of operations.

### The "Ongoing Braid" Metaphor

Nelson's metaphor is revealing:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." [LM 2/15]

A braid preserves the *strands* (I-space content) and their *arrangement at any cross-section* (V-space at a version). You can examine any cross-section and see what's there. You can compare two cross-sections and see what differs. But the braid does not necessarily label each twist with its operation type.

## How This Works in Practice

Consider a document evolving through three versions:

| Version | V-Space Arrangement | I-Space Content |
|---------|---------------------|-----------------|
| V1 | [A, B, C] | A="hello", B=" world", C="!" |
| V2 | [A, C] | (B removed from V-space; still in I-space) |
| V3 | [A, D, C] | D=" there" (new content appended to I-space) |

**What the system preserves:**
- All three V-space arrangements (reconstructable)
- All I-space content (A, B, C, D — permanent, never deleted)
- Shared I-space origin (A and C appear in all versions; B only in V1)

**What the system can compute:**
- V1↔V2 correspondence: A↔A, C↔C; B was removed
- V2↔V3 correspondence: A↔A, C↔C; D was added
- V1↔V3 correspondence: A↔A, C↔C; B removed, D added

**What the system does NOT necessarily store:**
- "V1→V2 was a DELETE operation on span B"
- "V2→V3 was an INSERT of 'there' at position 2"
- The temporal ordering of V1→V2 before V2→V3

The *effect* of each edit is fully recoverable from comparing adjacent version states. But the *type of operation* (insert vs. delete vs. rearrange) is not explicitly stored — it's inferrable from the structural differences.

## The Historical Trace Enfilade

Nelson does mention a specific data structure for history:

> "we redesigned Barus's linking enfilade system, designed the historical trace enfilade, and formulated the general theory of enfilades" [LM 1/36]

The "historical trace enfilade" suggests a dedicated mechanism for tracking version history. However, the curated sources do not provide detail on what this structure stores internally — whether it records operations or only version states.

NEED_RAW: [1/34-1/38] for more detail on the historical trace enfilade's internal structure.

## Conclusion

Nelson's design guarantees that you can:
1. **Reconstruct** any previous version state
2. **Compare** any two versions to see what corresponds
3. **Trace** every byte to its original document of creation

But the design achieves this through **structural preservation** (append-only I-space, versioned V-space mappings, shared-origin correspondence) rather than through an **explicit operation journal**. The derivation history is *implicit in the structure* — computable on demand from comparing adjacent version states — rather than *explicitly recorded* as a sequence of named operations.

The practical effect is the same: you can determine what was added, removed, or rearranged between any two versions. The difference is *how*: by structural comparison of I-space mappings, not by replaying a stored sequence of edit commands.

---

## Question 8 [nelson]

> Must the system permanently record every operation that caused content to arrive at its current location — including the sequence of transclusions, edits, and version-creation acts along the way?

### Nelson's Answer

# No — Nelson Does Not Require Recording the Full Operation Chain

The system must record **where content originated** and **what each version looked like**, but not **the sequence of operations** that produced the current arrangement.

## What Nelson DOES Require

### 1. Origin Traceability (Structural, via I-Addresses)

Every byte has a permanent I-address encoding its home document. This gives you one hop of provenance — "this byte was born in document X" — without recording how it traveled.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The I-address IS the provenance record. It is not metadata that could be stripped — it is the address itself.

### 2. Historical Backtrack (State Reconstruction, Not Operation Replay)

Nelson requires that any previous version can be reconstructed:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

But the mechanism is **state reconstruction**, not operation journaling. The system stores "each change and fragment individually" [LM 2/15] and uses an "indexing method that allows any previous instant to be reconstructed" [LM 2/15]. The goal is to reconstruct **what things looked like**, not to replay **what commands were issued**.

### 3. Version Ancestry (Encoded in Tumbler Address)

CREATENEWVERSION records parent-child relationships between versions:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

But this records **which document was versioned from which**, not the chain of transclusions within a document.

### 4. Content Co-occurrence (Computed, Not Recorded)

FINDDOCSCONTAINING finds all documents sharing content:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

This is **computed from I-addresses**, not from a recorded operation history. If documents A, B, and C all contain bytes with I-addresses from document X, the system can discover that by scanning I-addresses — without ever having recorded the COPY operations that created those transclusions.

## What Nelson Does NOT Require

### The Operation Chain Is Not Recorded

Consider this scenario: Alice creates content in document A. Bob transcludes it into document B. Carol transcludes the same passage from Bob's document into document C.

**What the system knows:**
- Carol's document C contains bytes with I-addresses from A (origin traceability)
- Bob's document B also contains bytes with the same I-addresses from A
- All three documents can be discovered via FINDDOCSCONTAINING

**What the system does NOT need to know:**
- That Carol's transclusion came via Bob's document rather than directly from Alice's
- The specific COPY command that created each transclusion
- The timestamp or sequence of operations

The I-address tells you the **origin**. The V→I mapping tells you the **current arrangement**. Neither requires recording the intermediate steps.

### No Operation Journal Is Specified

Nelson's 17 FEBE commands [LM 4/61] define what the system **does**, not what it **records about doing**. There is no GETHISTORY or GETOPERATIONLOG command. The closest operation is SHOWRELATIONOF2VERSIONS, which:

> "returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

This computes correspondence from **shared I-addresses** — a structural property — not from recorded operations.

## The Append-Only Principle

Nelson's description of append-only storage could be misread as requiring operation logging:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

But "changes" here means **new content** (bytes added to I-space) and **new arrangements** (V-space mappings), not a journal of FEBE commands. The chronological filing serves reconstruction ("any previous instant"), not auditability.

## Summary

| What must be recorded | Required? | Mechanism |
|---|---|---|
| Where content originated | **Yes** | I-address encodes home document |
| What each version looks like | **Yes** | V→I mappings per version |
| Which documents share content | **Computable** | I-address matching (not recorded separately) |
| Version ancestry | **Yes** | Tumbler address encodes parent |
| Which COPY/INSERT/DELETE created each mapping | **No** | Not specified |
| The chain of transclusions across documents | **No** | Not specified |
| A journal of all operations | **No** | Not specified |

Nelson designed a system where **the addresses themselves carry provenance**. The I-address of a byte IS its origin record. The V→I mapping IS the document's structure. There is no need for a separate operation log because the structural properties of the address space already answer the questions Nelson cares about: *Where did this come from?* (I-address), *What does this version look like?* (V-space), and *Who else uses this content?* (FINDDOCSCONTAINING).

---

**NEED_RAW: 1/36** — The "historical trace enfilade" is mentioned but not described in the curated sources. Its internal design might shed light on whether Nelson envisioned operation-level tracking for the version reconstruction mechanism, though nothing in the curated specification suggests this.

---

## Question 9 [nelson]

> If the same content appears in two documents independently — not through sharing but through separate acts of storage — must the system distinguish these as unrelated, even if the content is byte-identical?

### Nelson's Answer

# Yes — Absolutely and By Design

Xanadu **must** distinguish independently stored byte-identical content as unrelated. This is not a quirk of implementation but a foundational architectural principle.

## Content Identity Is Based on Creation, Not Value

The curated source on content provenance states this directly:

> "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address. This is how the system distinguishes 'wrote the same words' from 'quoted from the original.'"

This distinction is the entire point of I-space addressing.

## Why: The I-Address Encodes Origin

Every byte's permanent I-address has the form:

```
Node.0.User.0.Document.0.Element
```

The **Document field** encodes which document created the byte [LM 4/26]. When Alice types "hello world" into document A, those bytes get I-addresses under document A. When Bob independently types "hello world" into document B, those bytes get I-addresses under document B. Different documents, different addresses — regardless of byte values.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

Each INSERT creates **new** native bytes with **new** I-addresses. The permascroll is append-only — new content is "filed, as it were, chronologically" [LM 2/14]. Two independent insertions of the same string produce two distinct sequences of I-addresses.

## The COPY Operation Is How Identity IS Shared

The critical contrast is between INSERT and COPY in the FEBE protocol:

- **INSERT** creates new content in I-space — fresh bytes, fresh addresses
- **COPY** creates a V-space mapping to **existing** I-space content — this is transclusion

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

COPY is Nelson's transclusion operation. After a COPY, the destination document's V-stream includes bytes whose I-addresses point back to the **original** document. This shared I-space origin is what makes the system recognize the content as "the same."

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

## What This Distinction Enables

### 1. Correspondence

Correspondence — the ability to match parts across versions — relies entirely on shared I-space origin:

> "Correspondence is a RELATION — the relationship between V-space positions that share the same I-space origin."

Two documents with byte-identical content created independently have **no** correspondence relationship. Two documents that share content through transclusion **do**. This is how SHOWRELATIONOF2VERSIONS works — it returns "ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70], and correspondence is determined by shared I-addresses.

### 2. FINDDOCSCONTAINING

This operation "returns a list of all documents containing any portion of the material included by \<vspec set\>" [LM 4/70]. It searches by I-address origin, not by byte value. If Bob independently typed the same text as Alice, FINDDOCSCONTAINING on Alice's content will **not** find Bob's document. If Bob transcluded Alice's content, it **will**.

### 3. Origin Traceability

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This guarantee is structural — it comes from the I-address itself. If the system conflated byte-identical content from different sources, this guarantee would be destroyed.

### 4. Royalty Attribution

Royalties flow based on I-space origin. When Bob transcludes Alice's content and a reader accesses it, Alice gets paid because the bytes trace back to her document. If Bob typed the same words independently, Alice gets nothing — correctly, because she didn't write those particular bytes.

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

"Who wrote what" is determined by I-addresses, not by string matching.

## The Deeper Principle

This design reflects Nelson's understanding that **literature is about provenance, not content**. A quotation is not just "the same words" — it is a specific act of inclusion from a specific source. The distinction between "wrote the same words independently" and "quoted from the original" is semantically fundamental to scholarship, attribution, and intellectual honesty.

The system makes this distinction structural and unforgeable. Within the system, you cannot claim to have independently written something you actually transcluded, nor can you be falsely attributed as a source you never were. The I-address is the proof.

---

## Question 10 [nelson]

> Must the system be able to answer temporal provenance queries — for example, "which documents contained this content at a specific past moment" — not just current-state queries?

### Nelson's Answer

# Temporal Provenance Queries in Xanadu

## Short Answer

**Yes, the system should support temporal provenance queries.** Nelson's design principles demand it, and the data required to answer them is structurally preserved. However, the FEBE protocol as specified does not include a temporal parameter on FINDDOCSCONTAINING — creating a gap between Nelson's general guarantees and the specific operations defined.

---

## The General Principle: Full Historical Access

Nelson's foundational guarantee is explicitly temporal:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version **at a given time**, it comes to your screen." [LM 2/15]

> "The user of such a system may scroll through an individual document, **at successive instants of time**, alive in the space-time vortex." [LM 2/15]

This establishes that the system preserves all historical state and that temporal queries are a first-class capability. Nelson doesn't limit this to "show me my document as it was" — the principle is general: any historical state is reconstructable.

---

## The Data Is There

Three structural properties guarantee that temporal provenance data exists:

### 1. All Versions Are Preserved
Every version of every document persists permanently. When a document is edited, the old arrangement remains accessible:

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

### 2. Time Is Tracked
Though not encoded in tumbler addresses, time is explicitly tracked as metadata:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

Links are dated ("Since links will be dated, the time of mailing is shown" [LM 4/55]), and changes are stored chronologically ("filed, as it were, chronologically" [LM 2/14]). The system knows WHEN each version was created.

### 3. I-Space Sharing Is Permanent
When FINDDOCSCONTAINING finds documents sharing content, it works through I-space addresses. Since I-addresses are permanent and all versions are preserved, the historical record of which documents contained which I-space content at which time is fully recoverable.

---

## The FEBE Gap

The specific operation for content provenance, FINDDOCSCONTAINING, is defined without a temporal parameter:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

This appears to operate on current state — it finds documents that currently contain the specified material. It does not include a "as of time T" parameter.

However, Nelson explicitly supports time-based filtering for link discovery:

> "This filtering by different attributes we call 'sieving', and it can only be set up for a comparatively small number of traits — say, location and author and **time**." [LM 2/47]

If link discovery supports temporal sieving, the same capability should extend to content provenance queries. The mechanism is consistent; it simply wasn't specified as an explicit FEBE operation.

---

## What Temporal Provenance Requires

To answer "which documents contained content X at time T," the system needs:

1. **Which versions of which documents ever included X** — derivable from I-space sharing across all preserved versions
2. **When each version was active** — determinable from version creation timestamps (tracked separately per [LM 4/18])
3. **Intersection** — which versions were current at time T and included X

All three are available in Nelson's architecture. The append-only storage model means nothing is lost. The question is only whether the system exposes this as a single query or requires composition of existing operations.

---

## My Design Intent

The system SHOULD answer temporal provenance queries. The entire architecture exists to preserve the historical structure of literature. A system that can tell you "what did this document look like at time T" but cannot tell you "what other documents contained this content at time T" would be arbitrarily limiting a capability that the stored data fully supports.

The absence of a temporal parameter on FINDDOCSCONTAINING in the XU.87.1 protocol is a specification gap, not a design decision. The 17 commands of FEBE were acknowledged as a starting set — Nelson notes that "FEBE commands are presently in verbose ASCII. They will be shortened as needed" [LM 4/61], implying the protocol was expected to evolve.

The principle is clear: if historical state is preserved (it is), and temporal queries are supported for content retrieval (they are), then temporal queries for content provenance are a natural and necessary extension.

---

## Summary

| Aspect | Status |
|--------|--------|
| Design intent supports temporal provenance | **Yes** — "a given part of a given version at a given time" |
| Data required is preserved | **Yes** — all versions, time tracked separately |
| FEBE operation explicitly includes time parameter | **No** — FINDDOCSCONTAINING has no temporal parameter |
| Time-based filtering exists for other queries | **Yes** — sieving by time for link discovery |
| Architectural barrier to implementation | **None** — append-only storage preserves everything needed |

The system must be able to answer temporal provenance queries. The data is there by design. The protocol simply needs to expose it.

---

## Question 11 [nelson]

> Does the ownership record permanently attached to content provide an unbroken chain of attribution, such that any viewer of shared content can always discover the original author regardless of how many documents it has passed through?

### Nelson's Answer

# Yes — Attribution Is Structural and Direct, Not a Chain

The short answer is yes, but the mechanism is more elegant than an "unbroken chain." Xanadu does not trace attribution through a chain of intermediary documents. Instead, every transclusion points **directly** to the original I-space address, making attribution immediate regardless of how many documents the content has passed through.

## The I-Address IS the Attribution

Every byte ever created in Xanadu receives a permanent I-space address with the form:

```
Node.0.User.0.Document.0.Element
```

The **User** and **Document** fields permanently encode who created the content and which document it was born in. This address never changes.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When Document B transcludes content from Document A, B's V-space creates a mapping to A's I-space addresses. B does not receive new I-addresses for that content — it references A's existing ones. The COPY operation is explicitly described as transclusion that "shares I-addresses with the source" [LM 4/67].

## Why Multi-Level Transclusion Doesn't Degrade Attribution

Consider the scenario:

1. **Alice** creates Document A containing "hello world" → bytes get I-addresses under Alice's account
2. **Bob** creates Document B, transcludes "hello" from A → Bob's V-space maps to Alice's I-addresses
3. **Carol** creates Document C, transcludes "hello" from B → Carol copies from Bob's V-stream

When Carol transcludes from Bob's document, she is copying his V-space mapping. But Bob's V-space for those bytes already points to Alice's I-addresses. So Carol's V-space also maps directly to Alice's I-addresses. There is no intermediary pointer — it's not A→B→C but rather:

```
Alice's I-space: "hello"  (permanent, at Alice's address)
     ↑              ↑              ↑
Bob's V-space   Carol's V-space   (any future document)
```

Nelson captures this with the glass pane metaphor:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

And then the guarantee:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

The phrase "any specific word or character" is key — this operates at the byte level, not the document level. And "regardless of" how many layers of glass exist.

## Why This Cannot Be Severed Within the System

Attribution is not metadata attached to content — it is the **address itself**. To fetch the content, the system must request it from its home location. The fetching mechanism requires knowing the origin.

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The system distinguishes "native" from "non-native" bytes structurally. Non-native bytes are fetched from their home. You cannot display transcluded content without resolving its I-address, which encodes its origin.

This is why Nelson can also guarantee reverse discovery:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

The FINDDOCSCONTAINING operation finds every document that transcludes specific content — across any number of levels — because all transclusions share the same I-addresses.

## What the I-Address Actually Tells You

The I-address provides:

| Field | What It Reveals |
|-------|----------------|
| **Node** | Which server stores the original |
| **User** | Which account created the content |
| **Document** | Which specific document the bytes were born in |
| **Element** | The byte's position within that document |

This means any viewer can determine:
- The **home document** (immediately, from the address)
- The **account** that owns that document (from the User field)
- The **server** where it resides (from the Node field)

## Two Important Caveats

**1. Attribution identifies accounts, not necessarily people.** The User field identifies an account in the tumbler hierarchy. The mapping from account to human identity is a contractual/social matter, handled through the Storage Vendor agreement. Nelson supports "John Doe publication" [LM 2/60] where the account holder's real identity may be unknown. So the system guarantees you can trace content to its *account of origin* — tracing to a specific person depends on whether that person published under their real identity.

**2. No cryptographic verification.** Nelson's system provides no technical proof that content at an I-address is unchanged from its original creation:

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." [LM 5/17]

The guarantee is structural (the address encodes origin) and contractual (the Storage Vendor is obligated to preserve content faithfully), but not cryptographic.

## Summary

The ownership record attached to content provides something **stronger** than an unbroken chain — it provides **direct, structural identification of the original creator** at the byte level. There is no chain to break because transclusion does not create intermediary ownership records. Every transclusion, at every level, points directly back to the same permanent I-space address where the content was born. The attribution is the address, and the address is required to fetch the content, so attribution cannot be stripped without breaking the content itself.

---

## Question 12 [nelson]

> Must the system record the historical fact that a transclusion relationship once existed, even after the receiving document removes the transclusion — preserving the complete path content has traveled?

### Nelson's Answer

# Must the System Preserve Historical Transclusion Relationships?

## Short Answer

Nelson does not specify a separate "transclusion provenance log." But his architecture **inherently preserves this history** through the version mechanism — no additional mechanism is needed, because no previous state is ever destroyed.

## The Version History IS the Provenance Record

When Document B transcludes content from Document A, and then the owner of Document B edits to remove that transclusion, here is what happens:

1. **The removal is a V-space operation only.** The current version's V-stream no longer maps to Document A's I-space content. But the I-space content itself is untouched.

2. **The previous version still exists** and still contains the V-space mapping to Document A's I-space. This is not optional — it is the fundamental nature of Xanadu storage.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

3. **Historical backtrack can reconstruct the transclusion relationship at any time.** The system "automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

The "path content has traveled" is not metadata that needs to be separately maintained — it is structural, embedded in the version history itself.

## Why No Separate Mechanism Is Needed

Nelson's append-only storage model means that the V-space arrangement of every version persists:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

The "braid" metaphor is crucial here. A document is not its current state — it is its entire trajectory through time. The transclusion that existed in version 1 is part of the braid even after version 2 removes it. You can always go back to that strand.

Furthermore, the SHOWRELATIONOF2VERSIONS operation can compare any two versions and return "a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. This means you can compare the version-with-transclusion to the version-without and see exactly what was removed.

## What About Discoverability?

There is a subtlety here. The FINDDOCSCONTAINING operation "returns a list of all documents containing any portion of the material included by \<vspec set\>" [LM 4/70]. If Document B's *current* version no longer transcludes from Document A, does this operation still find Document B?

Nelson does not explicitly address whether FINDDOCSCONTAINING searches all versions or only current versions. The phrasing "documents containing" is ambiguous — does it mean "documents that currently contain" or "documents that have ever contained"?

Given Nelson's emphasis on prismatic storage — where "there is thus no 'basic' version of a document set apart from other versions" [LM 2/19] — the old versions are not lesser or hidden. They are equally valid arrangements. But whether the system actively indexes historical transclusion relationships for search purposes versus merely preserving them for reconstruction is an implementation decision Nelson leaves open.

## The Principle

The governing principle is non-destruction:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

And:

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

The system does not need to *separately record* that a transclusion once existed, because it never destroys the version in which that transclusion was present. The historical fact is preserved not as an annotation or log entry, but as a living, queryable, reconstructable version of the document.

## Summary

| Question | Answer |
|----------|--------|
| Must the system record historical transclusions separately? | No — version history preserves them structurally |
| Can past transclusions be discovered? | Yes — through historical backtrack to old versions |
| Can past transclusions be compared to current state? | Yes — via SHOWRELATIONOF2VERSIONS |
| Is there an explicit "provenance chain" mechanism? | Not specified — the version braid itself is the chain |
| Does FINDDOCSCONTAINING find historical transclusions? | Not explicitly specified — NEED_RAW: [4/63, 4/70] for deeper examination of the search semantics |

The system preserves the complete path content has traveled — not through a separate provenance mechanism, but because **it never destroys any state through which content has passed.**

---

## Question 13 [nelson]

> When content from one document is transcluded into a second document, and that second document is then the source of a further transclusion into a third, must the system trace the chain all the way back to the original document of first storage?

### Nelson's Answer

## Yes — But Not by Following a Chain

The answer is yes, the system always resolves content back to its original document of first storage. But the architecture makes this trivially direct rather than requiring chain-following. Here's why.

### I-Space Addresses ARE the Trace

Every byte in Xanadu has a permanent I-space address that encodes its originating document:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When document A creates content, those bytes get permanent I-space addresses under A. When document B transcludes that content, B's V-stream maps to A's I-space addresses. The bytes are non-native to B:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Now when document C transcludes that same content from B's V-stream, C is not creating a reference *to B's reference to A*. C's V-stream maps directly to A's I-space addresses — because that is what B's V-stream resolves to. The COPY operation takes the I-addresses that B's V-stream points to and maps them into C's V-stream.

**There is no chain to trace.** C's mapping points to A's I-space directly. The intermediary (B) is structurally irrelevant at retrieval time.

### The Glass Pane Metaphor Describes Experience, Not Mechanism

Nelson does describe multi-level windowing as a conceptual experience:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

> "A document may have a window to another document, and that one to yet another, indefinitely. Thus A contains part of B, and so on. One document can be built upon another, and yet another document can be built upon that one, indefinitely: each having links to what was already in place." [LM 2/38]

But this layering describes the *user's compositional experience* — how documents are built. At the structural level, every window resolves to I-space addresses that permanently encode origin:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

### Why This Must Be So

Three guarantees require direct resolution to origin:

**1. Attribution.** The system must always identify the original author. If C's reference went through B, and B were withdrawn or corrupted, C would lose its connection to A. Direct I-space addressing prevents this.

**2. Royalties.** When C's reader receives A's bytes, A must be paid:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

The I-address tells the system exactly whom to pay — no chain-following needed.

**3. Content discovery.** The FINDDOCSCONTAINING operation must find *all* documents containing A's content:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

Because both B and C map to A's I-addresses, both are discoverable through the same I-space query. If C pointed to B rather than to A, this operation would require recursive chain-following — violating Nelson's performance guarantees.

### The Architecture Collapses the Chain

The I-space/V-space separation is precisely what makes multi-level transclusion work without chain-following:

| Document | V-Space | I-Space |
|----------|---------|---------|
| A | positions 1-100 → A's native I-addresses | Bytes live here permanently |
| B | positions 1-50 → A's I-addresses (transcluded) | No new I-content for transcluded portion |
| C | positions 1-30 → A's I-addresses (transcluded from B's view) | No new I-content |

All three V-streams resolve to the same I-space addresses. The "chain" A→B→C exists in the history of who-transcluded-from-whom, but not in the address structure. At retrieval time, C fetches directly from A's home location.

### Summary

The system does trace back to the original document — but the I-space addressing makes this a direct lookup, not a chain traversal. Nelson's architecture ensures that transclusion at any depth always resolves to the permanent I-space address of first storage, where the bytes were "actually stored under its control" [LM 4/11]. The intermediary documents provide compositional structure (which passages appear where) but never interpose themselves between the reader and the original content.

---

## Question 14 [gregory]

> Given content at V-address `v` in document `d`, does walking the POOM to retrieve the I-address unambiguously distinguish whether that content was originally INSERT-ed into `d` versus COPY-ed from another document, based solely on whether the I-address falls within `d`'s own I-address range (`docISA.0.1.*`)?

### Gregory's Answer

# Gregory Consultation

**Question:** Given content at V-address `v` in document `d`, does walking the POOM to retrieve the I-address unambiguously distinguish whether that content was originally INSERT-ed into `d` versus COPY-ed from another document, based solely on whether the I-address falls within `d`'s own I-address range (`docISA.0.1.*`)?


## KB Synthesis

## Short Answer

No — the I-address range test is not unambiguous. The I-address encodes the **native document** (where content was first allocated via INSERT), not the most recent copy source. Content originally INSERT-ed into `d` can travel through other documents and return to `d` via COPY while still carrying `d`'s I-address prefix, making it look identical to a direct insert.

---

## What the I-Address Prefix Actually Encodes

The allocation mechanism establishes this firmly. Content I-addresses for document `d` are allocated within `d`'s own tumbler subspace — for a document like `2.1.0.1.0.1`, text content lands at `2.1.0.1.0.1.3.1`, `.3.2`, and so on. [SS-ADDRESS-SPACE, Finding 0033, Finding 0065, Finding 0077]

When a different document `d'` INSERTs content, those I-addresses land in `d'`'s own subspace. So far the test looks viable: I-address in `d`'s range → native to `d`; I-address outside → native to someone else.

But the system design makes a sharper claim:

> Every I-address has exactly one native document — the document where INSERT first allocated it. COPY does not allocate new I-addresses; it creates V→I mappings that reference existing ones. The `homedoc` field in each POOM crum records the I-address origin document, **not the document from which content was most recently copied.** [INV-IADDR-PROVENANCE]

The I-address prefix (and the explicit `homedoc` field used by `isanextensionnd`) records the point of original creation — a fact that is preserved unconditionally through any number of subsequent COPY operations.

---

## The Counterexample: Content That Travels and Returns

Consider this operational sequence:

1. **INSERT "ABC" into `d`** → allocates I-addresses in `d`'s namespace, e.g., `d.3.1`, `d.3.2`, `d.3.3`
2. **CREATENEWVERSION of `d` → `d'`** → `d'`'s POOM maps V-positions to the same I-addresses `d.3.1` through `d.3.3` [ST-VERSION-CREATE, Finding 0046]
3. **COPY from `d'` into some new document `e`** → `e`'s POOM contains entries pointing to `d.3.1`–`d.3.3` (still `d`'s namespace, not `d'`'s or `e`'s) [PRE-COPY, INV-IADDR-PROVENANCE]
4. **COPY from `e` back into `d`** → `d`'s POOM gains new V-position entries pointing to `d.3.1`–`d.3.3`

Now `d` has content at a new V-position that was placed there by a COPY operation from `e ≠ d`, but the I-address is indistinguishable from content that was directly INSERT-ed into `d`. The I-address prefix test returns the wrong answer.

This is not a pathological scenario — it is the normal consequence of transitive transclusion and versioning, which are the system's core operations. [INV-TRANSITIVE-IDENTITY]

---

## Self-Transclusion: The Same Problem Closer to Home

Even without the multi-hop scenario, a single COPY within `d` causes the same problem. When content at V-position `v1` in `d` is VCOPY-ed to position `v2` within the same document:

> A document can transclude content from itself. [...] the document's POOM contains multiple `(V-position, I-address)` entries with the same I-address but different V-positions. [EC-SELF-TRANSCLUSION, SS-POOM-MULTIMAP]

The COPY produces a new POOM entry at `v2` pointing to an I-address already within `d`'s namespace. Although the question explicitly targets COPY from "another document," this case is structurally identical and demonstrates the general principle.

---

## What the `homedoc` Field Gives You

The POOM bottom crum stores an explicit `homedoc` field that `isanextensionnd()` consults during crum extension decisions. [SS-POOM-BOTTOM-CRUM, INV-IADDR-PROVENANCE] This field records the I-address origin document — but it suffers the same limitation as the prefix test. In step 4 of the counterexample above, `homedoc` for the new POOM entries would record `d`, not `e`. You still cannot distinguish "directly inserted into `d`" from "copied from `e`, which itself had this content from `d`'s lineage."

---

## Why This Limitation Exists

The system guarantees I-address immutability and permanence — I-addresses allocated for `d` stay in `d`'s namespace forever [INV-NO-IADDR-REUSE, INV-IADDR-IMMUTABILITY]. COPY is identity-preserving by design [ST-VCOPY]. These two properties together mean that provenance-by-creation-site is the only information the I-address carries, and the chain of subsequent COPY operations is not recorded anywhere in the data model. The granfilade is append-only; there is no operation history, no copy log. [SS-POOM-MUTABILITY, INV-DELETE-NOT-INVERSE]

---

## Summary

| Scenario | I-address in `d`'s range? | Was it INSERTed into `d`? | Test result |
|---|---|---|---|
| Direct INSERT into `d` | Yes | Yes | Correct |
| COPY from unrelated `d'` | No | No | Correct |
| COPY from `d'` whose content traces to `d` | Yes | No | **Wrong** |
| Self-transclusion within `d` | Yes | No (COPY used) | **Wrong** |

The test is reliable only when the copy source is a document with no genealogical or content-identity relationship to `d`. In a system where versioning and transclusion are fundamental operations, that assumption cannot be safely made. The I-address prefix encodes **content origin at creation time**, not the most recent COPY operation, and these are not the same thing. [INV-IADDR-PROVENANCE, ST-VCOPY, INT-VERSION-TRANSCLUSION]

---

## Code Exploration

I now have everything needed to give a rigorous answer. Here it is.

---

## Answer

**Yes — with a precise caveat.** Walking the POOM to retrieve the I-address **does** unambiguously distinguish INSERT-into-`d` from COPY-from-another-document-into-`d`, based on whether the I-address falls within `d`'s own ISA sub-tree. But the mechanism is more subtle than it appears: the correctness of the test depends on a structural fact inside `doinsert` that is easy to miss.

---

### 1. What INSERT Does to the Granfilade

`doinsert` in `do1.c:87-123`:

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);   // hint.hintisa = docisaptr
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset) );
    return(ret);
}
```

Step 1: `inserttextingranf` (wrapper at `granf1.c:44-47`) calls `inserttextgr` (`granf2.c:83-109`), which calls `findisatoinsertgr` (`granf2.c:130-156`). Because `hint.subtype == ATOM`, this dispatches to `findisatoinsertmolecule` (`granf2.c:158-181`):

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    typeisa upperbound, lowerbound;
    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    // upperbound = docISA incremented 2 levels deeper at value (TEXTATOM+1)=2
    // i.e., the ceiling of the text-atom sub-range under docISA

    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    // lowerbound = last existing item below upperbound in the global granfilade tree

    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        // Previous item is at the SAME depth as docISA (e.g., the doc itself)
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement (isaptr, 1, 1, isaptr);
        // First text atom: docISA.{+2 levels, TEXTATOM}.{+1 level, 1}
    } else if (hintptr->atomtype == TEXTATOM) {
        tumblerincrement (&lowerbound, 0, 1, isaptr);
        // Next text atom: lowerbound + 1 at same depth
    }
    ...
}
```

**Result**: Every text atom allocated by INSERT receives an I-address that is a descendant of `docISA` in the granfilade tree — specifically in the range `[docISA.*.{TEXTATOM}, docISA.*.{TEXTATOM+1})`. The question's notation `docISA.0.1.*` names this sub-range.

The text is then stored in the granfilade at this address (`granf2.c:99: insertseq((typecuc*)fullcrumptr, &lsa, &locinfo)`), and the returned `ispanset` carries `itemid = ISPANID` with `stream = lsa` (`granf2.c:102-107`).

---

### 2. How `doinsert` Gets the POOM Updated — and Why the ISPANID Matters

After `inserttextingranf` returns, `doinsert` calls:

```c
docopy (taskptr, docisaptr, vsaptr, ispanset)
```

passing the newly-allocated I-spans as `typespecset specset`. Inside `docopy` (`do1.c:45-65`), the first thing is:

```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
```

In `specset2ispanset` (`do2.c:14-46`), the itemid governs what happens:

```c
for (; specset; specset = ...) {
    if (((typeitemheader *)specset)->itemid == ISPANID) {
        *ispansetptr = (typeispanset)specset;           // pass through DIRECTLY
        ispansetptr = ...;
    } else if (((typeitemheader *)specset)->itemid == VSPECID) {
        findorgl(..., &docorgl, type)                   // open SOURCE doc's POOM
        && vspanset2ispanset(taskptr, docorgl, vspanset, ispansetptr)  // V → I
    }
}
```

The items from `inserttextingranf` are `ISPANID` — **they pass through unchanged**. No V→I conversion. The POOM (`insertpm`, `orglinks.c:75-134`) then records the mapping:

```
V-address vsaptr  ←→  I-address lsa  (lsa is under docISA)
```

---

### 3. What COPY Does

When `docopy` is called directly from the FEBE `copy` handler (`fns.c:35-47` → `do1.c:45-65`), the `specset` contains **`VSPECID` items** — each with a `docisa` (source document's ISA) and a `vspanset` (virtual positions in that source):

```c
// do2.c:27-39
} else if (((typeitemheader *)specset)->itemid == VSPECID) {
    findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
    && (ispansetptr = vspanset2ispanset (
            taskptr, docorgl,
            ((typevspec *)specset)->vspanset,   // V-span in SOURCE doc
            ispansetptr))
```

`vspanset2ispanset` (`orglinks.c:397-402`) calls `permute(taskptr, orgl, vspanptr, V, ispansetptr, I)` which walks the **source document's** POOM, finding the I-addresses that correspond to those V-positions **in the source**. Those I-addresses are sub-addresses of `srcDocISA`, not `docISA`.

`insertpm` then records the mapping in `d`'s POOM:

```
V-address vsaptr  ←→  I-address from srcDoc's POOM  (under srcDocISA)
```

---

### 4. Walking the POOM: What V→I Retrieval Sees

Both INSERT and COPY use `insertpm` (`orglinks.c:75-134`) to record a 2D crum in `d`'s POOM: one axis is the V-address, the other is the I-address (`movetumbler(vsaptr, &crumorigin.dsas[V])` at line 113, `movetumbler(&lstream, &crumorigin.dsas[I])` at line 105).

Retrieving V→I (`vspanset2ispanset` called on `d`'s own POOM via `permute`) traverses `d`'s enfilade and returns the `I` coordinates from the crums matching the given V-span. Those I-addresses are:

- **For INSERTed content**: under `docISA.0.1.*` (allocated by `findisatoinsertmolecule`)
- **For COPYed-from-elsewhere content**: under `srcDocISA.0.1.*` where `srcDocISA ≠ docISA`

---

### 5. The Test Is Unambiguous — With One Important Qualification

**It IS unambiguous** for the case the question describes: INSERT-into-`d` versus COPY-from-a-different-document-into-`d`. The I-address prefix cleanly separates them because:

- `findisatoinsertmolecule` always allocates within `d`'s own ISA sub-tree (bounded above by `tumblerincrement(docISA, 2, TEXTATOM+1)`)
- `vspanset2ispanset` on a foreign POOM returns I-addresses rooted at the source document's ISA sub-tree

**But there is a case that breaks the "original INSERT" interpretation:**

In `docreatenewversion` (`do1.c:260-299`):

```c
movetumbler(isaptr, &vspec.docisa);   // OLD doc's ISA  (do1.c:287)
vspec.vspanset = &vspan;
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // copies into d'
```

When `d'` is created as a new version of `d`, all content from `d` is COPYed into `d'` using the old doc's `VSPECID`. The I-addresses in `d'`'s POOM therefore point into `d`'s sub-tree, **not `d'`'s sub-tree**. For `d'`, the prefix test correctly identifies all this content as "from another document" — which it is (`d`). Any text subsequently INSERTed directly into `d'` gets fresh I-addresses under `d'`'s ISA.

There is also a theoretically degenerate case: **self-COPY** (copying a V-span of `d` back into `d`). The V→I conversion on `d`'s own POOM produces I-addresses already under `docISA`, making them indistinguishable from original INSERTs. But this content *was* originally authored in `d`'s ISA space — the self-COPY doesn't create new I-addresses, it just re-uses existing ones. The question asks about "COPY from another document", so self-copy is excluded.

---

### Summary Table

| Operation | I-address of content at V=`v` in doc `d` | Under `docISA.0.1.*`? |
|---|---|---|
| `INSERT` text into `d` | `findisatoinsertmolecule(hint=docISA)` → `docISA.0.1.N` | **YES** |
| `COPY` from doc `s` (`s ≠ d`) into `d` | `vspanset2ispanset` on `s`'s POOM → `srcISA.0.1.M` | **NO** |
| `COPY` from `d` itself back into `d` | same `d`'s POOM → `docISA.0.1.M` (already there) | **YES** (same space as INSERT) |
| New version `d'` from `d`, inherited content | from `d`'s POOM → `docISA.0.1.N` (not `d'`'s ISA) | **NO** (relative to `d'`) |

**Bottom line**: Walking `d`'s POOM to retrieve the I-address for V-position `v`, and checking whether it falls within `d`'s own ISA sub-tree (`docISA.0.1.*`), **does unambiguously identify whether the content was physically authored (INSERT-allocated) in `d`'s granfilade sub-tree versus transcluded from a different document's ISA space.** The mechanism rests on two structural facts:

1. `doinsert` allocates text in the granfilade under `docISA` via `findisatoinsertmolecule` (`granf2.c:158-181`), and passes those I-addresses to `insertpm` as `ISPANID` items that bypass V→I conversion in `specset2ispanset` (`do2.c:24-26`).
2. Direct user-level `COPY` from a foreign document passes `VSPECID` items through `specset2ispanset` (`do2.c:27-39`), which walks the *source* document's POOM and returns I-addresses rooted at `srcDocISA`, leaving `d`'s own ISA sub-tree untouched.

---

## Question 15 [gregory]

> When `find_documents_containing` returns a set of documents sharing I-addresses with a query span, does the spanfilade preserve enough information to reconstruct the temporal ordering of which document first received those I-addresses — i.e., can the original creator be distinguished from subsequent transcluders?

### Gregory's Answer

# Gregory Consultation

**Question:** When `find_documents_containing` returns a set of documents sharing I-addresses with a query span, does the spanfilade preserve enough information to reconstruct the temporal ordering of which document first received those I-addresses — i.e., can the original creator be distinguished from subsequent transcluders?


## KB Synthesis

No. The spanfilade cannot distinguish the original creator from subsequent transcluders. The information is partially recoverable, but through a different mechanism — the I-address structure itself, not the DOCISPAN index.

---

## What the DOCISPAN Stores

The DOCISPAN sub-index has the structure `Map<ISpan, DocISA>` [SS-DOCISPAN]. When INSERT allocates fresh I-addresses for document A, it calls `insertspanf(..., DOCISPAN)`, creating entries mapping those I-addresses → A. When document B later transcludes that content via COPY, it also calls `insertspanf(..., DOCISPAN)` [ST-INSERT], creating entries mapping the same I-addresses → B.

Both entries land in the same append-only index with no timestamps, no ordering metadata, and no "original" versus "copy" flag. The index records only: *this document contains these I-addresses*. `FINDDOCSCONTAINING` returns a flat set `{A, B, C, ...}` with no provenance ordering [INV-IADDRESS-PERMANENT].

Critically, the spanfilade is strictly write-only — no deletion function exists anywhere in `spanf1.c` or `spanf2.c` [INV-SPANF-WRITE-ONLY]. So even stale references from documents that have since deleted the content persist in the index, making temporal inference from result set membership impossible [EC-STALE-SPANF-REFERENCE].

---

## The I-Address Structure Does Encode the Original Creator

What the spanfilade cannot tell you, the I-address tumbler itself can. Content I-addresses are allocated within a document-scoped namespace:

```
account.0.document.0.element_field.element_number
```

where `element_field = 3` identifies text content [SS-ADDRESS-SPACE, Finding 0065]. The allocation uses `findisatoinsertmolecule` which bounds its search to `docISA` and allocates monotonically within that scope [ST-INSERT, Finding 0033]. So an I-address like `1.1.0.1.0.1.3.0.1.5` encodes that document `1.1.0.1.0.1` is the original allocator.

This is formalized in [INV-IADDR-PROVENANCE]: "Every I-address has exactly one native document — the document where INSERT first allocated it." The `homedoc` field in POOM crums records this origin, and it is unaffected by subsequent COPY operations.

I-address allocation is also monotonically increasing and never reuses addresses [INV-MONOTONIC, INV-NO-IADDR-REUSE], and the granfilade is append-only [FC-GRANF-ON-DELETE], so the I-address space is a permanent record of when and where each byte was first created.

---

## The Two Sources of Evidence Are Separate

| Mechanism | Can identify original creator? | Source |
|-----------|-------------------------------|--------|
| DOCISPAN spanfilade query | No — flat set, no ordering | [SS-DOCISPAN] |
| I-address tumbler prefix | Yes — encodes allocating document | [INV-IADDR-PROVENANCE] |
| POOM `homedoc` field | Yes — per-document internal state | [ST-VCOPY, Finding 0046] |

The correct way to identify the original creator given an I-address set is to inspect the I-address tumbler prefix, not to query the spanfilade. The spanfilade tells you *who currently (or ever) contained the content*; the I-address tells you *who created it*.

Note one additional complication: CREATELINK allocates link orgls in the granfilade's content range, which can create gaps in the text I-address sequence [INT-LINK-INSERT, Finding 0063]. This doesn't break the prefix-encoding of creator identity, but it means the I-address sequence for a single document's text may not be perfectly contiguous if links were interleaved.

---

## Code Exploration

I have all the source evidence needed. Here is the full answer.

---

## Can the Spanfilade Distinguish Original Creator from Transcluder?

**No.** The spanfilade does not preserve sufficient information to reconstruct the temporal ordering of I-address assignment. The original creator cannot be distinguished from subsequent transcluders using data in the spanfilade alone. Here is the complete technical basis for that conclusion.

---

### 1. The Spanfilade Crum Info Structure Has One Field

The metadata stored at each spanfilade bottom crum is defined in `backend/wisp.h:106-109`:

```c
/* type2dbottomcruminfo */
typedef struct struct2dbottomcruminfo {
        tumbler homedoc;
} type2dbottomcruminfo;
```

That is the entire payload beyond the two-dimensional coordinate (`SPANRANGE` × `ORGLRANGE`). There is **no timestamp, no sequence number, no creation-order field, and no "original owner" pointer.** The only metadata associated with a spanfilade crum is a single tumbler identifying the document that caused this crum to be written.

---

### 2. Both Original Insert and Transclusion Write Identical Crum Payloads

The spanfilade entry is written by `insertspanf` in `backend/spanf1.c:15-54`. For an I-span item:

```c
// spanf1.c:27-29
movetumbler (&((typeispan *)sporglset)->stream, &lstream);
movetumbler (&((typeispan *)sporglset)->width, &lwidth);
movetumbler (isaptr, &linfo.homedoc);   // <-- homedoc = the doc doing this operation
```

`isaptr` is always the document currently performing the insert. Two cases:

**Original insertion** — `appendpm` in `backend/orglinks.c:17-27` calls `doinsert` then `insertspanf` with the creating document's ISA. So `homedoc` = creator.

**Transclusion** — `docopy` in `backend/do1.c:45-64`:

```c
// do1.c:60-62
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&& insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

Here `docisaptr` is the **transcluding** document. `insertspanf` is called identically, and `homedoc` is set to the transcluder's ISA.

The crum written by the original creator and the crum written by the transcluder are structurally identical. They differ only in the `homedoc` tumbler value — each records which document wrote it, not which document wrote it first.

---

### 3. `finddocscontainingsp` Returns an Unordered Flat Set

The query path starts at `backend/fns.c:20-32` (`finddocscontaining`) → `do1.c:15-23` (`dofinddocscontaining`) → `spanf1.c:151-188` (`finddocscontainingsp`).

The core of `finddocscontainingsp` [spanf1.c:165-182]:

```c
headptr = addresssetptr;
*addresssetptr = NULL;
clear (&docspace, sizeof(typespan));
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);  // restrict to doc content
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
        if (isinlinklist(*headptr, &document.address))
            continue;
        document.itemid = LINKID;
        document.next = NULL;
        addresssetptr = (typelinkset *) onitemlist(taskptr, (typeitem*)&document, (typeitemset*)addresssetptr);
    }
    contextfree (context);
}
```

The `retrieverestricted` call at `retrie.c:56-85` does a 2D area query: find all spanfilade crums whose `ORGLRANGE` is in the `DOCISPAN` slice (i.e., it is a document content entry) and whose `SPANRANGE` overlaps the query I-span. Results come back from `findcbcinarea2d` [retrie.c:229-268], which traverses the enfilade recursively by coordinate position — ordered by I-address, **not by insertion time**.

The function then calls `beheadtumbler` to strip the `DOCISPAN` prefix and recover the document ISA, deduplicates with `isinlinklist`, and appends to the result list via `onitemlist`. The returned `typelinkset` is ordered by the spanfilade's traversal order (I-address geometry), not by when those documents acquired the I-addresses.

**No timestamp is extracted because no timestamp exists to extract.**

---

### 4. Could Tumbler Ordering Serve as a Proxy?

Document ISAs are tumblers. Tumblers are allocated monotonically — earlier documents get lexicographically smaller tumblers within a user's namespace. So `tumblercmp` on two document ISAs does reveal which document was **created** first.

But this is the wrong question. What matters for the transclusion-creator distinction is which document first **inserted content at** those I-addresses, not which document was created first. A document can be created (`docreatenewversion`) and remain empty for some time before content is copied into it. A later-created document could have been the one that originally typed the text. Document-creation order and content-insertion order are independent.

Furthermore, the `beheadtumbler` call at `spanf1.c:174` strips the high-order component from the ORGLRANGE tumbler. The value stored in `ORGLRANGE` is the document ISA prefixed with `DOCISPAN` — after stripping, you get the document ISA. Comparing these tumblers gives only creation-time ordering, not insertion-time ordering.

---

### 5. The `homedoc` Field's Actual Purpose

The `homedoc` field in `type2dbottomcruminfo` serves a different purpose entirely: **preventing accidental span merging across document boundaries**. In `insertnd.c:301-309`:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    // ...
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Two adjacent crums can only be merged (extended) if they share the same `homedoc`. This keeps each document's spanfilade entries separate, which is structurally correct — but it is a consistency mechanism, not a provenance mechanism. It answers "does this crum belong to document X" but says nothing about "did document X receive these I-addresses before document Y."

---

### Summary

| Question | What the code shows |
|---|---|
| Is creation timestamp stored in spanfilade crums? | No. `type2dbottomcruminfo` [wisp.h:107-109] has one field: `homedoc`. |
| Is insertion order tracked anywhere? | No. Neither `insertspanf` [spanf1.c:15] nor `insertnd` [insertnd.c:15] records when the crum was written. |
| Does `finddocscontainingsp` return ordered results? | No. Returns a deduplicated set ordered by I-address geometry [spanf1.c:151-188]. |
| Does `homedoc` identify the original creator? | No. It identifies the document that performed each particular `insertspanf` call — both creator and transcluder set it to themselves [spanf1.c:29, do1.c:62]. |
| Can tumbler comparison recover insertion order? | No. Tumbler ordering gives document-creation order, not content-insertion order [xanadu.h:39, tumble.c]. |

The spanfilade records **membership** — which documents contain which I-spans — not **authorship lineage**. Transclusion is represented as a symmetric relationship: both the original document and the transcluding document have entries in the spanfilade for the same I-span, and those entries are structurally identical. The system has no mechanism to mark one as primary and the other as derived, because that distinction is not stored.

---

## Question 16 [gregory]

> If document A inserts "Hello", document B copies it from A, and document C copies the same span from B, does `find_documents_containing` called from C return both A and B, or only the documents with DOCISPAN entries — and does the DOCISPAN for B's copy point to the same I-address range as A's original?

### Gregory's Answer

# Gregory Consultation

**Question:** If document A inserts "Hello", document B copies it from A, and document C copies the same span from B, does `find_documents_containing` called from C return both A and B, or only the documents with DOCISPAN entries — and does the DOCISPAN for B's copy point to the same I-address range as A's original?


## KB Synthesis

## Answer

**Yes, `find_documents_containing` returns all three documents (A, B, and C), and B's DOCISPAN entry points to the exact same I-address range as A's original.**

Here is the full chain of reasoning:

---

### I-address allocation: only A gets new addresses

When A inserts "Hello", `inserttextingranf` allocates fresh I-addresses α₁..α₅ in the granfilade [SS-ADDRESS-ALLOC, ST-INSERT]. These are permanently allocated and never reused [INV-NO-IADDR-REUSE].

When B copies from A, and C copies from B, no new I-addresses are allocated. `docopy` shares the existing I-addresses rather than creating new ones [ST-VCOPY]. B's POOM maps its V-positions to α₁..α₅. C's POOM maps its V-positions to the same α₁..α₅ [INV-IADDR-IMMUTABILITY, INV-TRANSITIVE-IDENTITY].

---

### DOCISPAN creation: every copy registers the same I-addresses

Every call to `docopy` (whether from INSERT or COPY) ends with `insertspanf(..., DOCISPAN)` [SS-DOCISPAN, Finding 0036]. This registers the I-addresses against the destination document in the spanfilade:

| Operation | I-addresses registered | Document registered |
|-----------|----------------------|---------------------|
| A INSERT "Hello" | α₁..α₅ | A |
| B COPY from A | α₁..α₅ | B |
| C COPY from B | α₁..α₅ | C |

B's DOCISPAN entry uses the same α₁..α₅ range as A's — because those are the actual I-addresses B's POOM now maps, converted back to I-spans by `specset2ispanset` before being passed to `insertspanf` [SS-DOCISPAN, Finding 0047].

---

### find_documents_containing returns all three

The spanfilade is write-only and monotonically growing [INV-SPANF-WRITE-ONLY]. No operation removes DOCISPAN entries. After all three operations, the spanfilade contains:

```
α₁..α₅ → {A, B, C}
```

`FINDDOCSCONTAINING("Hello")` searches the DOCISPAN sub-index by I-address and returns the full set: **A, B, and C** [SS-DOCISPAN, Finding 0023, INV-IADDRESS-PERMANENT].

This is the same mechanism documented for the general transclusion case: "find_documents_transitive" — because vcopy preserves I-addresses at every hop, all documents in the chain are permanently indexed under the same I-address range [INV-TRANSITIVE-IDENTITY, Finding 0018].

---

### Key distinction: DOCISPAN vs POOM

It is worth noting what `find_documents_containing` does **not** track: document deletions. Even if B later deletes "Hello" from its V-stream, B's DOCISPAN entry persists. The spanfilade is a historical journal, not a current-state index. After deletion, `find_documents_containing` would still return {A, B, C}, but the I-to-V conversion in B would yield empty (the POOM mapping is gone) [EC-STALE-SPANF-REFERENCE, INV-SPANF-WRITE-ONLY, INT-DELETE-SPANF-DIVERGENCE].

---

## Code Exploration

I couldn't write the finding file (no permission granted), but I have traced the full execution path. Here is the complete answer:

---

## Answer: DOCISPAN Transclusion Chains and `find_documents_containing`

### Question 1: What documents does `find_documents_containing` return?

**All three — A, B, and C — are returned.** It is not limited to documents with "original" DOCISPAN entries; it returns every document that has a DOCISPAN entry for the queried I-address range.

### Question 2: Does B's DOCISPAN point to the same I-address range as A's?

**Yes, exactly the same.** B's DOCISPAN is a direct I-address pointer into the permascroll — it is not a pointer through A.

---

## Full Code Trace

### Step 1 — A inserts "Hello"

`doinsert` [do1.c:87] calls `inserttextingranf`, which allocates text in the permascroll (granfilade) and returns an `ispanset` of I-addresses — call it `[Ia, Ia+5)`. Then:

```c
// do1.c:118–119
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy(taskptr, docisaptr, vsaptr, ispanset)
```

Inside `docopy` [do1.c:45–65], `specset2ispanset` is called [do2.c:14–46]. The input already carries `ISPANID`, so it passes through immediately:

```c
// do2.c:24–26
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *ispansetptr = (typeispanset)specset;
```

The resulting `ispanset = [Ia, Ia+5)` is then stored by:

```c
// do1.c:62
insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

Inside `insertspanf` [spanf1.c:15–54]:

```c
// spanf1.c:22 — ORGL-axis key: docA's ISA with DOCISPAN prepended
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);

// spanf1.c:27–28 — SPAN-axis key: the raw I-address
movetumbler(&((typeispan*)sporglset)->stream, &lstream);  // = Ia
movetumbler(&((typeispan*)sporglset)->width, &lwidth);    // = 5
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);

// spanf1.c:51
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

`DOCISPAN = 4` [xanadu.h:39]. `prefixtumbler` [tumble.c:641–651] prepends `4` as the leading tumbler component. So A's spanfilade entry is:
- **ORGL axis**: `4.docA` 
- **SPAN axis**: `[Ia, Ia+5)`

---

### Step 2 — B copies from A

`docopy(taskptr, docB, vsaB, specset_of_A_vspan)` [do1.c:45]. The specset is a `VSPECID` — a virtual-space spec naming document A and a V-position within it.

`specset2ispanset` [do2.c:27–38] recognizes `VSPECID` and calls:

```c
// do2.c:34–36
findorgl(taskptr, granf, &((typevspec*)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset(taskptr, docorgl, ((typevspec*)specset)->vspanset, ispansetptr))
```

`vspanset2ispanset` [orglinks.c:397–402] calls `permute(taskptr, orgl, vspanptr, V, ispansetptr, I)`, which resolves A's POOM (permutation matrix enfilade): it maps A's V-positions to the underlying permascroll I-addresses by calling `retrieverestricted` on A's POOM tree.

Since A's POOM records that V-position `vsaA` → I-span `[Ia, Ia+5)`, the return value is `[Ia, Ia+5)` — **the same raw permascroll address, stored flat, with no pointer through A**.

`insertspanf` is then called with `docB` and `[Ia, Ia+5)`. B's spanfilade entry:
- **ORGL axis**: `4.docB`
- **SPAN axis**: `[Ia, Ia+5)` — **identical I-range to A**

---

### Step 3 — C copies from B

Same mechanism. B's POOM maps B's V-span → `[Ia, Ia+5)`. C's spanfilade entry:
- **ORGL axis**: `4.docC`
- **SPAN axis**: `[Ia, Ia+5)` — **same I-range again**

---

### Step 4 — `find_documents_containing` called from C

`dofinddocscontaining` [do1.c:15–23]:

```c
// do1.c:20–22
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)
&& finddocscontainingsp(taskptr, ispanset, addresssetptr)
```

`specset2ispanset` resolves C's V-span → `[Ia, Ia+5)` via C's POOM. Then `finddocscontainingsp` [spanf1.c:151–188]:

```c
// spanf1.c:167–169 — query region in ORGL axis: the DOCISPAN type band
clear(&docspace, sizeof(typespan));
tumblerincrement(&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement(&docspace.width, 0, 1, &docspace.width);

// spanf1.c:171 — 2D query: ORGL in DOCISPAN band × SPAN overlapping [Ia, Ia+5)
context = retrieverestricted(
    (typecuc*)spanf,
    &docspace, ORGLRANGE,
    ispanset, SPANRANGE,
    (typeisa*)NULL);
```

`retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` [retrie.c:87–110] walks the spanfilade's 2D enfilade, collecting all leaf crums satisfying both axis constraints via `crumqualifies2d` [retrie.c:270–305].

This finds three crums: A's entry, B's entry, C's entry.

For each, the document ISA is recovered by stripping the DOCISPAN prefix:

```c
// spanf1.c:173–174
movetumbler(&c->totaloffset.dsas[ORGLRANGE], &docid);
beheadtumbler(&docid, &document.address);
```

`beheadtumbler` [tumble.c:673–683] shifts off the leading `4` component, yielding the raw document ISA. Duplicates are filtered by `isinlinklist` [spanf2.c:16–23].

**Returned set: {docA, docB, docC}**.

---

## The Key Invariant

The spanfilade stores **(document ISA × permascroll I-address)** pairs directly. B's DOCISPAN is not "B contains A's content at V-position X" — it is "B contains the bytes at permascroll addresses `[Ia, Ia+5)`." The transclusion chain A→B→C is **not stored anywhere in the spanfilade**. It is entirely implicit in the fact that all three documents happen to have DOCISPAN entries for the same I-address range.

`find_documents_containing` is therefore a **flat set union**: given an I-span, return every document ISA that has a DOCISPAN entry touching that span, with no regard for how deep the transclusion chain goes.

---

## Question 17 [gregory]

> The I-address hierarchy encodes document origin (`node.0.user.0.doc.0.element`) — when resolving an I-address retrieved from a POOM entry, can `findpreviousisagr` or similar granfilade traversal determine the originating document address by truncating the I-address at the document level, or is there a dedicated operation for extracting document origin from an I-address?

### Gregory's Answer

# Gregory Consultation

**Question:** The I-address hierarchy encodes document origin (`node.0.user.0.doc.0.element`) — when resolving an I-address retrieved from a POOM entry, can `findpreviousisagr` or similar granfilade traversal determine the originating document address by truncating the I-address at the document level, or is there a dedicated operation for extracting document origin from an I-address?


## KB Synthesis

Good question about I-address structure and document origin recovery. Here's what the KB tells us:

## I-Addresses Do Encode Document Origin as a Prefix

The docuverse convention makes document origin structurally extractable. From [SS-ADDRESS-SPACE] Finding 0077, the granfilade layout makes this explicit:

```
1.1.0.1.0.1              (document d1)
1.1.0.1.0.1.3.0.1.1      (content I-address for text in d1)
1.1.0.1.0.1.3.0.1.2      (next content I-address)
```

The document ISA is literally a prefix of the content I-address — separated by additional `.0.` components encoding element field (3 for text, 2 for links) and element number [SS-ADDRESS-SPACE] Finding 0065.

So yes: `tumblertruncate` at the document address length, followed by `tumblereq` for verification, would recover the originating document. The containment predicate is precisely defined [SS-TUMBLER-CONTAINMENT]:

```
tumblertruncate(&I_addr, tumblerlength(&doc_addr), &truncated);
tumblereq(&truncated, &doc_addr);  // TRUE iff I_addr is under doc_addr
```

## No Dedicated Extraction Function Is Documented

The KB does not describe a function specifically named "extract document ISA from I-address." The documented mechanisms are:

1. **SPORGL provenance** — the primary runtime mechanism. `vspanset2sporglset` produces sporgls where `sporgladdress` IS the originating document ISA [SS-SPORGL]. This is how document provenance is carried through operations (transclusion, link creation, version comparison).

2. **DOCISPAN reverse lookup** — `finddocscontainingsp` queries the spanfilade to find which documents contain given I-addresses [SS-DOCISPAN]. However, this returns a **superset** due to the append-only spanfilade: deleted content still appears in the index [EC-STALE-SPANF-REFERENCE], [INV-SPANF-WRITE-ONLY].

3. **Allocation bounds as implicit encoding** — `findisatoinsertmolecule` sets `upperbound = tumblerincrement(&hintptr->hintisa, 2, ...)`, creating a document-scoped bound for searching [SS-ADDRESS-SPACE] Finding 0065. This implies the system knows the depth at which a document ISA terminates.

## The Allocation Depth Is Known at Each Site

From [SS-ADDRESS-SPACE] Finding 0021, `makehint` encodes hierarchy levels:

| supertype | subtype | depth |
|-----------|---------|-------|
| ACCOUNT | DOCUMENT | 2 |
| DOCUMENT | DOCUMENT | 1 |
| DOCUMENT | ATOM | (element depth) |

So `findisatoinsertnonmolecule` with depth=2 allocates a document under an account, and depth=1 allocates a version under a document [SS-ADDRESS-ALLOC]. This same depth knowledge — that a document address crosses 2 `.0.` boundaries from the node prefix — is what you'd use to truncate an I-address back to its document prefix.

## Summary

**Structural truncation works** — the address hierarchy encodes document origin recoverable via `tumblertruncate` + `tumblereq` [SS-TUMBLER-CONTAINMENT] — but the KB documents no dedicated `iaddr_to_doc` extraction function.

**The SPORGL is the operational answer** [SS-SPORGL]: wherever the code actually needs to know "which document does this I-address come from," it packages I-addresses into sporgls via `vspanset2sporglset`, carrying `sporgladdress` explicitly. The POOM bottom crum itself stores only `(V-origin, V-width, I-origin, I-width)` [SS-POOM-BOTTOM-CRUM] — no document ISA. Document origin is recovered by the sporgl layer above the POOM, not by traversing the granfilade.

`findpreviousisagr` is not a document-origin resolver — it finds the highest existing I-address within a bounded range, used for allocation, not for extracting provenance from existing I-addresses [SS-ADDRESS-SPACE] Finding 0061.

---

## Code Exploration

Now I have everything needed. Let me compile the full answer.

---

## Answer: I-Address Document Origin Extraction

### The I-Address Hierarchy in Memory

`typeisa` is simply `tumbler` [xanadu.h:23]:
```c
typedef tumbler typeisa;
```

A `tumbler` is a fixed-point number with a 16-element mantissa [common.h:53-65]:
```c
#define NPLACES 16
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;
    short exp;
    tdigit mantissa[NPLACES];
} tumbler;
```

The hierarchy `node.0.user.0.doc.0.element` is encoded in the mantissa digits as a sequence with zeros as level separators — each `.0.` pair is a two-digit separator in the mantissa. There is no explicit "level tag" in the struct; hierarchy is implicit in the digit pattern and known depth.

---

### `tumblertruncate` — The Core Mechanism

`tumblertruncate` [tumble.c:625] is the fundamental tool for extracting a prefix:

```c
int tumblertruncate(tumbler *aptr, INT bint, tumbler *cptr)
{
    tumbler answer;
    INT i;
    movetumbler(aptr, &answer);
    for (i = answer.exp; i < 0 && bint > 0; ++i, --bint);
    if (bint <= 0)
        tumblerclear(&answer);
    else
        for (; bint < NPLACES; ++bint)
            answer.mantissa[bint] = 0;
    tumblerjustify(&answer);
    movetumbler(&answer, cptr);
}
```

It keeps the first `bint` significant digits and zeros the rest. This is the explicit mechanism for "truncating at the document level."

---

### `findpreviousisagr` Cannot Determine Document Origin Directly

`findpreviousisagr` [granf2.c:255-278]:
```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
    if (crumptr->height == 0) {
        findlastisaincbcgr((typecbc*)crumptr, offset);
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if ((tmp = whereoncrum(ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
            || tmp == ONMYRIGHTBORDER
            || !ptr->rightbro) {
            findpreviousisagr(ptr, upperbound, offset);
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);
        }
    }
}
```

This function traverses the granfilade tree accumulating absolute WIDTH offsets to find the largest ISA that is `< upperbound`. It returns a **full I-address** (potentially an element-level address) in `offset`. **It has no knowledge of document boundaries** — it just finds the numerically previous entry. Document-level extraction is entirely the responsibility of the caller.

---

### Where Document Origin IS Extracted: the `findisatoinsertnonmolecule` Pattern

This is where the answer lives. In `findisatoinsertnonmolecule` [granf2.c:203-241]:

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    INT depth, hintlength;

    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;  // depth: 1 or 2 levels
    hintlength = tumblerlength(&hintptr->hintisa);            // length of parent ISA

    tumblerincrement(&hintptr->hintisa, depth - 1, 1, &upperbound);

    clear(&lowerbound, sizeof(lowerbound));
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

    // BUG FIX: Check if lowerbound is actually under hintisa by TRUNCATING and COMPARING
    if (!iszerotumbler(&lowerbound)) {
        tumblertruncate(&lowerbound, hintlength, &truncated);      // <-- TRUNCATE to parent level
        lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
    }

    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
    } else {
        tumblertruncate(&lowerbound, hintlength + depth, isaptr);  // <-- TRUNCATE to child level
        tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
    }
}
```

The caller supplies `hintptr->hintisa` — the **known parent document address** — and `tumblerlength(&hintptr->hintisa)` is used as the truncation depth. The pattern at line 231 is:
```c
tumblertruncate(&lowerbound, hintlength, &truncated);
```
to isolate whether the found address is under the expected document. This is not discovery — it is **verification via truncation given known depth**.

The same truncation pattern at line 239:
```c
tumblertruncate(&lowerbound, hintlength + depth, isaptr);
```
extracts the child address up to `depth` levels below the hint.

---

### `findisatoinsertmolecule` for ATOM types [granf2.c:158-181]

For inserting text/link atoms under a document:
```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear(&lowerbound, sizeof(lowerbound));
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

    if (tumblerlength(&hintptr->hintisa) == tumblerlength(&lowerbound)) {  // line 165
        tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement(isaptr, 1, 1, isaptr);
    } else if ...
}
```

At line 165: the comparison `tumblerlength(&hintptr->hintisa) == tumblerlength(&lowerbound)` distinguishes whether `findpreviousisagr` found the document-level entry itself vs. a sub-entry. The document address length is **already known** from `hintptr->hintisa`; it's not derived from the found address.

---

### `finddocscontainingsp` — Closest to Document-Level Extraction from Retrieved Data [spanf1.c:151-188]

This is the one place that does something like "extract document identity from an index entry":

```c
movetumbler(&c->totaloffset.dsas[ORGLRANGE], &docid);  // line 173
beheadtumbler(&docid, &document.address);               // line 174
```

Here `c->totaloffset.dsas[ORGLRANGE]` is the spanfilade's ORGLRANGE index offset — a document address prefixed by `DOCISPAN` (value 4) [spanf1.c:168]. `beheadtumbler` [tumble.c:673] strips the first digit:

```c
int beheadtumbler(tumbler *aptr, tumbler *bptr)
{
    movetumbler(aptr, &temp);
    ++temp.exp;
    if (aptr->exp == 0)
        temp.mantissa[0] = 0;
    tumblerjustify(&temp);
    movetumbler(&temp, bptr);
}
```

This is domain-specific (spanfilade ORGLRANGE index, not general I-addresses from POOM), and it strips a single leading digit, not a multi-level prefix.

---

### For Ownership: `tumbleraccounteq` [tumble.c:38]

`isthisusersdocument` [be.c:171-176] uses:
```c
int isthisusersdocument(tumbler *tp)
{
    bool result = tumbleraccounteq(tp, &taskptrx->account);
    return result;
}
```

`tumbleraccounteq` compares by stopping at the double-zero boundary of the account tumbler — it checks that the document ISA is _under_ a given account, but does not extract or return the document-level prefix. The account tumbler serves as a known boundary, not a computed one.

---

## Conclusion

**There is no dedicated operation for extracting document origin from an I-address.**

The system has two mechanisms, and both require the document address to be **already known externally**:

1. **`tumblertruncate(iaddr, tumblerlength(known_doc_addr), &result)`** — used explicitly in `findisatoinsertnonmolecule` [granf2.c:231, 239] to truncate a found I-address back to the document level. The document level length is supplied by `tumblerlength(&hintptr->hintisa)`, where `hintptr` carries the document address the caller already has.

2. **`tumbleraccounteq`** [tumble.c:38] — for ownership testing. It checks containment within an account boundary using the double-zero termination of the account tumbler, but does not extract a document address.

`findpreviousisagr` [granf2.c:255] is purely a tree-traversal accumulator; it emits full I-addresses and has no awareness of document boundaries. The document-level truncation is always applied by the caller with `tumblertruncate`, and the required truncation depth is always conveyed through the `typehint.hintisa` parameter — specifically `tumblerlength(&hintptr->hintisa)`. The granfilade design assumes the document address is always a given input (the `hint`), never something to be discovered by traversal.

---

## Question 18 [gregory]

> After CREATENEWVERSION, both the original and version share identical I-addresses — does `compare_versions` (SHOWRELATIONOF2VERSIONS) return the shared spans as paired V-address ranges, and is this the ONLY mechanism for determining that two documents are related by versioning rather than independent transclusion?

### Gregory's Answer

# Gregory Consultation

**Question:** After CREATENEWVERSION, both the original and version share identical I-addresses — does `compare_versions` (SHOWRELATIONOF2VERSIONS) return the shared spans as paired V-address ranges, and is this the ONLY mechanism for determining that two documents are related by versioning rather than independent transclusion?


## KB Synthesis

## After CREATENEWVERSION: compare_versions and Relationship Detection

### Part 1: Does compare_versions return shared spans?

**Yes, and it returns all text content as paired V-address ranges.**

CREATENEWVERSION's postcondition is `references(version) = references(source)` at creation time — all text subspace I-addresses are shared [ST-VERSION-CREATE, Finding 0032]. Since `compare_versions` is defined as: return paired V-spans where both documents map to the same permascroll I-address range [SS-COMPARE-VERSIONS], the result immediately after versioning is the complete text content paired with itself:

```
compare_versions(original, version) →
  [(original: V 1.1 for 0.N, version: V 1.1 for 0.N)]
```

One pair covering the entire text, because the I-addresses are identical and V-positions start at the same text-subspace origin [ST-VERSION-CREATE, Finding 0007].

**Critical constraint**: `compare_versions` only covers the text subspace (1.x). CREATENEWVERSION does not copy the link subspace [ST-VERSION-CREATE, Finding 0043], so link content is excluded regardless. If either document contains links and their V-spans are inadvertently included in the comparison input, the operation crashes [EC-COMPARE-VERSIONS-LINK-CRASH].

---

### Part 2: Is compare_versions the ONLY mechanism?

**No.** There is a second mechanism: the **address hierarchy**.

For owned-document versions, the version address is a direct child of the source address [SS-VERSION-ADDRESS, Finding 0032]:

```
Source:   1.1.0.1.0.1
Version:  1.1.0.1.0.1.1    (child, depth=1)
Copy:     1.1.0.1.0.2       (sibling, depth=2, a different document)
```

This is the *only structural difference* between a version and an independent transcluded copy — both share the same I-addresses and both would produce identical `compare_versions` results immediately after creation [SS-VERSION-ADDRESS, Finding 0032]:

> "Both produce documents with shared I-addresses. The address hierarchy is the structural signal that distinguishes a 'version' relationship from an independent copy."

The address containment predicate [SS-TUMBLER-CONTAINMENT] — truncate the version's address to the source's length and compare — tells you whether the relationship is versioning (prefix match) or sibling creation (no match).

**However, this mechanism has a gap.** When a user versions a document they do not own, the ownership-sensitive allocation places the version under the versioning user's own account, not under the source document [SS-VERSION-ADDRESS, Finding 0068]:

```
User B versions User A's doc 1.1.0.1.0.1 →
  version at 1.1.0.2.0.1 (under User B's account)
```

In this cross-user case, the address hierarchy does NOT encode the version relationship. The version is structurally indistinguishable from any other document under User B's account. `compare_versions` would still reveal shared content, but so would any full transclusion — you cannot determine from address or content alone that this is a "version" rather than a copy.

**Summary:**

| Mechanism | Distinguishes version from transclusion? | Limitation |
|---|---|---|
| Address hierarchy | Yes (owned versions) | Fails for cross-user versions |
| `compare_versions` | No — identical results for both | Cannot distinguish why content is shared |
| `find_documents` | No | Returns both, no relationship type |

`compare_versions` answers *what* is shared. The address hierarchy answers *why* (versioning vs. independent copy) — but only for same-user versioning. Neither mechanism alone is sufficient; the combination provides the full picture, with the cross-user versioning case as an architectural gap in structural relationship encoding.

---

## Code Exploration

Now I have everything needed for a complete, code-grounded answer.

---

## Answer

### 1. What `docreatenewversion` Actually Does to I-Addresses

`docreatenewversion` [do1.c:260-299] works as follows:

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    typevspan vspan;
    typevspec vspec;

    if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
        makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);  // [do1.c:271]
    } else {
        makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);  // [do1.c:275]
    }
    if (!createorglingranf(taskptr, granf, &hint, newisaptr)) return FALSE;  // [do1.c:277]

    if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) return FALSE;  // [do1.c:281]

    vspec.next = NULL;
    vspec.itemid = VSPECID;
    movetumbler(isaptr, &vspec.docisa);       // [do1.c:287] vspec references original doc
    vspec.vspanset = &vspan;

    addtoopen(newisaptr, user, TRUE, WRITEBERT);
    docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // [do1.c:293]
    ...
}
```

`doretrievedocvspanfoo` [do1.c:301-309] calls `retrievedocumentpartofvspanpm` [orglinks.c:155-162], which reads the POOM's V-dimension displacement and width:

```c
bool retrievedocumentpartofvspanpm(...)
{
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);  // [orglinks.c:159]
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);   // [orglinks.c:160]
}
```

This returns the text subspace vspan (starting at V=1.x). Then `docopyinternal` [do1.c:66-82] calls `insertpm` [orglinks.c:75-134] which creates new POOM crums in the new document that map the same V-positions to the **same I-addresses** as the original. The I-addresses (permascroll positions) are copied verbatim through `vspanset2ispanset` → `permute` [orglinks.c:397-422], then re-inserted into the new POOM via `insertnd` [orglinks.c:130].

**Result:** After `CREATENEWVERSION`, the original and version have separate V-address namespaces but their text V-addresses map to *identical* I-addresses in the granfilade/permascroll.

---

### 2. How `compare_versions` Returns Paired V-Address Ranges

The call chain from `fns.c:250-261`:

```c
void showrelationof2versions(typetask *taskptr)
{
    typespecset version1, version2;
    typespanpairset relation;

    if (getshowrelationof2versions (taskptr, &version1, &version2)
     && doshowrelationof2versions (taskptr, version1, version2, &relation))
        putshowrelationof2versions (taskptr, relation);
    else
        putrequestfailed (taskptr);
}
```

`doshowrelationof2versions` [do2.c:428-449]:

```c
bool doshowrelationof2versions(typetask *taskptr, typespecset version1, typespecset version2, typespanpairset *relation)
{
    typeispanset version1ispans = NULL;
    typeispanset version2ispans = NULL;
    typeispanset commonispans = NULL;

    filter_specset_to_text_subspace(taskptr, version1);   // [do2.c:440]
    filter_specset_to_text_subspace(taskptr, version2);   // [do2.c:441]

    return
        specset2ispanset(taskptr, version1, &version1ispans, READBERT)  // V→I
      &&    specset2ispanset(taskptr, version2, &version2ispans, READBERT)
      &&    intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)  // I∩I
      &&    ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation);  // I→(V,V)
}
```

**Step A – V→I conversion** (`specset2ispanset` [do2.c:14-46]): Each document's V-spans are converted to I-spans by calling `vspanset2ispanset` → `permute` [orglinks.c:397-422], which walks the POOM to map V-positions to their stored I-addresses.

**Step B – I-address intersection** (`intersectspansets` [correspond.c:145-189]): The two I-span sets are intersected by `comparespans` [correspond.c:191-208] → `spanintersection` [correspond.c:210-265], which computes the overlap of tumbler ranges arithmetically.

**Step C – I→(V₁, V₂) mapping** (`ispansetandspecsets2spanpairset` [do2.c:185-207]):

```c
bool ispansetandspecsets2spanpairset(...)
{
    if (ispanset == NULL) {
        *pairsetptr = NULL;
    } else {
        restrictspecsetsaccordingtoispans(taskptr, ispanset, &specset1, &specset2);  // [do2.c:196]
        makespanpairset (taskptr, ispanset, specset1, specset2, pairsetptr);         // [do2.c:197]
    }
    return (TRUE);
}
```

`restrictspecsetsaccordingtoispans` [correspond.c:18-50] calls `ispan2vspanset` [orglinks.c:389-394] for each document, which calls `permute` in the reverse direction (I→V) to find what V-position each common I-address lives at in each document.

`makespanpairset` [correspond.c:267-288] then iterates over each common ispan, calling `makespanpairsforispan` [correspond.c:290-348] to pair up the corresponding V-spans, and `makespanpair` [correspond.c:351-361]:

```c
typespanpair *makespanpair(typetask *taskptr, tumbler *doc1, tumbler *start1,
                           tumbler *doc2, tumbler *start2, tumbler *width)
{
    spanpair = (typespanpair *) taskalloc (taskptr, sizeof (typespanpair));
    docidandvstream2tumbler (doc1, start1, &spanpair->stream1);  // [correspond.c:357]
    docidandvstream2tumbler (doc2, start2, &spanpair->stream2);  // [correspond.c:358]
    movetumbler (width, &spanpair->widthofspan);                 // [correspond.c:359]
    return (spanpair);
}
```

**Yes: `compare_versions` returns shared spans as paired V-address ranges.** Each `spanpair` encodes (doc₁-address + V-stream-offset, doc₂-address + V-stream-offset, width). These are full V-addresses within each respective document, not raw I-addresses.

---

### 3. Is This the ONLY Mechanism for Detecting Versioning vs. Independent Transclusion?

**No — and it cannot distinguish them.**

`compare_versions` is purely an I-address overlap test. It does not know *why* two documents share I-addresses. Both `CREATENEWVERSION` and `COPY`/`vcopy` cause V-addresses in one document to map to the same I-addresses as another document. The output of `compare_versions` is identical in both cases for the shared portion.

There IS a second, structural piece of information encoded in addresses, but it is **not exposed by any FEBE operation**:

When a user creates a version of their own document, `docreatenewversion` [do1.c:271] uses:
```c
makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
```
This places the version as a **child** of the original in the granfilade tree (Finding 0068, confirmed by `findisatoinsertnonmolecule` [granf2.c:203-242]):

```
Original:  1.1.0.1.0.1
Version:   1.1.0.1.0.1.1    ← child address (prefix relationship)
```

A `vcopy` target, by contrast, is allocated by `docreatenewdocument` [do1.c:234-241] using:
```c
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
```
This places the copy as a sibling under the account:
```
Original:  1.1.0.1.0.1
VCopy:     1.1.0.1.0.2      ← sibling address (no prefix relationship)
```

A client that knows both addresses could infer the relationship by checking whether one address is a tumbler-prefix of the other. But:

1. **No FEBE API operation exposes this.** There is no "get parent document" or "list version children" command in the protocol table (`docs/client-api.md` lists all 20 commands; none query structural lineage).

2. **Cross-user versioning breaks even this heuristic.** When User B versions User A's document, `docreatenewversion` [do1.c:272-275] falls through to the ACCOUNT branch:
   ```c
   makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
   ```
   The cross-user version gets an address under User B's account — e.g. `1.1.0.2.0.1` — which has no prefix relationship to User A's `1.1.0.1.0.1`. The only detectable relationship is I-address overlap, exactly the same as transclusion.

3. **No metadata is stored in the new document.** `docreatenewversion` does not write any "parent pointer" or "origin document" field into the newly created POOM. The granfilade knows the structural position (via the allocated ISA), but that information is only implicitly encoded in the address digits, not in any document-level field queryable through the protocol.

---

### Summary

| Aspect | Code Citation | Conclusion |
|--------|--------------|------------|
| `compare_versions` output type | `correspond.c:351-361` | Returns paired V-address ranges `(stream1, stream2, width)` where each stream encodes a full `docid + V-offset` tumbler |
| Mechanism used | `do2.c:428-449` | V→I conversion per document, I-set intersection, I→V back-projection for each document, pair assembly |
| I-addresses shared after CREATENEWVERSION | `do1.c:285-293`, `orglinks.c:75-134` | Yes, `docopyinternal` maps the same permascroll I-addresses into the new document's POOM |
| I-addresses shared after COPY/vcopy | `do1.c:45-65`, same path | Yes, identical mechanism — both create POOM entries pointing to same I-addresses |
| Can `compare_versions` distinguish versioning from transclusion? | `do2.c:428-449` — no version-specific logic | **No.** The function tests only I-address overlap; the overlap is semantically identical for both operations |
| Is there a second mechanism? | `do1.c:271` + `granf2.c:203-242` | Address prefix relationship (version = child address) encodes lineage for same-user versioning — but this is not exposed by any FEBE API call and fails for cross-user versioning |
| Only FEBE API mechanism? | `docs/client-api.md` command table | Yes: `compare_versions` (opcode 10) is the only protocol-level operation for detecting shared content |

**Bottom line:** `compare_versions` (SHOWRELATIONOF2VERSIONS) returns shared text content as paired V-address ranges using I-address intersection. It IS the only FEBE mechanism for discovering content relationship, but it **cannot discriminate** versioning from independent transclusion — both produce identical I-address overlap. The granfilade address tree does encode version lineage structurally (parent-child addresses) for same-user versioning, but this is implicit in the allocated address digits with no corresponding query API, and it is not reliable for cross-user versioning.

---

## Question 19 [gregory]

> When a single I-address span appears at multiple V-positions within the same document (via self-transclusion), does `incontextlistnd` return ALL V-positions for that I-address, and can the system distinguish which V-position was the original insertion versus which was the copy?

### Gregory's Answer

# Gregory Consultation

**Question:** When a single I-address span appears at multiple V-positions within the same document (via self-transclusion), does `incontextlistnd` return ALL V-positions for that I-address, and can the system distinguish which V-position was the original insertion versus which was the copy?


## KB Synthesis

## Self-Transclusion: All V-Positions Returned, No Origin/Copy Distinction

### Question 1: Does `incontextlistnd` return ALL V-positions?

Yes, unconditionally.

The POOM is explicitly modeled as a multimap [SS-POOM-MULTIMAP]: a single I-address can appear at N distinct V-positions within the same document, and `findcbcinarea2d()` traverses all siblings at each B-tree level, recursively descending into every qualifying subtree and accumulating every matching leaf. The accumulation function `incontextlistnd()` inserts each found context into a sorted linked list, **never replacing existing entries** [SS-CONTEXT-LIST]. So for an I-address referenced at V-positions 1.2, 1.4, and 1.5:

```
ispan2vspanset(poom, i_B) = {
  VSpan(1.2, width=0.1),
  VSpan(1.4, width=0.1),
  VSpan(1.5, width=0.1)
}
```

All three are returned [SS-POOM-MULTIMAP]. The result is V-sorted via insertion-sort regardless of tree traversal order, making the output independent of B-tree structure [INV-RETRIEVAL-V-SORTED], [INV-RETRIEVAL-TREE-INDEPENDENCE].

This has been experimentally confirmed for N=2 and N=3 copies via self-transclusion, with all pairwise `compare_versions` calls correctly reporting shared content [EC-SELF-TRANSCLUSION].

---

### Question 2: Can the system distinguish original insertion from copy?

No. The system has **no mechanism** to mark one V-position as "original" and another as "copy." Three data fields could theoretically encode this distinction; none do:

**I-address:** The I-address is identical for the original and all copies — that is the operational definition of transclusion [ST-VCOPY]. INSERT allocates a fresh I-address; VCOPY places the *same* I-address at a new V-position without allocating anything new [INV-IADDR-PROVENANCE]. So I-address ordering reflects *when content was created*, not *which occurrence is canonical*.

**`homedoc` field:** Each POOM crum stores a `homedoc` identifying the document where the I-address was originally allocated [INV-IADDR-PROVENANCE]. For self-transclusion within document D, both the original crum (from INSERT) and the copy crum (from VCOPY) carry `homedoc = D`. No distinction.

**V-position:** V-positions reflect *current document structure*, not insertion history. They shift with subsequent edits [ST-INSERT] and are not stable temporal markers. The V-position of the "original" and the "copy" are both just locations in the document at query time.

The formal consequence: the system treats all V-positions referencing the same I-address as **semantically interchangeable**. This is made explicit by [INV-LINK-IDENTITY-DISCOVERY]:

> `iaddrs(doc, v1) = iaddrs(doc, v2) ==> findlinks(doc, v1) = findlinks(doc, v2)`

Link discovery, endset retrieval, and `compare_versions` all behave identically for each occurrence. There is no "primary" V-position in the data model.

This is a deliberate design property, not an omission. The Xanadu content identity model is defined by I-address (provenance by origin), not by V-address (provenance by position). Once content is created, all references to it are equal [INV-CONTENT-IMMUTABILITY], [SS-CONTENT-IDENTITY].

---

## Code Exploration

I now have everything needed to give a complete, source-cited answer. The findings 0039, 0078, and 0046 have already documented the key behaviors through code analysis and golden tests. Here is the full answer:

---

## Answer: `incontextlistnd` and Self-Transclusion

### Part 1: Does `incontextlistnd` return ALL V-positions for a given I-address?

**Yes — unconditionally, by design.**

The call chain that converts an I-address to its V-positions is:

```
ispan2vspanset     [orglinks.c:389]
  → permute        [orglinks.c:404]
  → span2spanset   [orglinks.c:425]
  → retrieverestricted [retrie.c:56]
  → retrieveinarea     [retrie.c:87]
  → findcbcinarea2d    [retrie.c:229]
  → incontextlistnd    [context.c:75]
```

#### The retrieval engine: `findcbcinarea2d` [retrie.c:229]

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1,
                          span2start, span2end, index2, (type2dbottomcruminfo*)infoptr)){
        continue;
    }
    if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);   // ← accumulates, never replaces
    }
}
```

Three properties guarantee exhaustive collection:
1. **`getrightbro` iteration** visits every sibling at each tree level
2. **Recursive descent** into every qualifying subtree
3. **`crumqualifies2d`** with `span2ptr = NULL` (the V-restriction): when `iszerotumbler(span2end)` is true (i.e., no V-restriction), `endcmp` returns `TOMYRIGHT` [retrie.c:282], which always passes the check `if (endcmp <= ONMYLEFTBORDER) return FALSE` — so ALL POOM crums whose I-dimension overlaps the query span qualify, regardless of their V-position

Self-transclusion via `docopy` [do1.c:45] calls `insertpm` [orglinks.c:75], which for each source I-span creates a **new POOM leaf crum** with:
- `crumorigin.dsas[I] = lstream` (the shared I-address)
- `crumorigin.dsas[V] = vsaptr` (the NEW destination V-address) [orglinks.c:105–113]

The original insert also created a crum with the same I-range but a different V-address. After one self-transclusion of span X, the POOM has two independent leaf crums:

| crum | I-range | V-range |
|------|---------|---------|
| original | [i, i+w] | [v₁, v₁+w] |
| copy     | [i, i+w] | [v₂, v₂+w] |

`findcbcinarea2d` will visit both leaf crums when restricted to I-range [i, i+w], call `incontextlistnd` for each, and build a context list containing both.

#### The accumulator: `incontextlistnd` [context.c:75]

```c
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
    prologuecontextnd (c, &grasp, (typedsp*)NULL);
    c->nextcontext = NULL;
    clist = *clistptr;
    if (!clist) { *clistptr = c; return(0); }           // first: set
    if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
        c->nextcontext = clist; *clistptr = c; return(0); // beginning: prepend
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {
            if ((whereoncontext(clist,...) > ONMYLEFTBORDER)    // middle:
                && (whereoncontext(nextc,...) < ONMYLEFTBORDER)) {
                c->nextcontext = nextc; clist->nextcontext = c; return(0);
            }
        }
    }
    clist->nextcontext = c;                              // end: append
}
```

This is **insertion-sort by the query dimension** (`index1 = I` when called from `ispan2vspanset`). It **never replaces** an existing entry. Every call adds a new node. After the traversal, the context list contains one entry per qualifying leaf crum — i.e., one per V-position that references the queried I-address. (Finding 0078 documents this in detail.)

#### Empirical proof

Three golden tests confirm the behavior:

**`internal/internal_transclusion_identity`**: Transclude "text" from V=1.10 to V=1.19 in the same document. `compare_versions` returns:
```json
"shared": [{"first": {"start":"1.10","width":"0.4"}, "second": {"start":"1.19","width":"0.4"}}]
```
Both V-positions share the same I-addresses — the V→I→V round-trip works and returns both.

**`internal/internal_transclusion_with_link`**: Link created on first occurrence (V=1.10), then searched from second occurrence (V=1.19):
```json
{"op": "find_links", "from": "second occurrence of 'text' (1.19-1.22)",
 "result": ["1.1.0.1.0.1.0.2.1"]}
```
The link IS found. This is the definitive proof: the backend converted the second occurrence's V-span to its I-span, then traversed the spanfilade using those I-addresses, which led to the link anchored on the first occurrence. That traversal required `ispan2vspanset` returning BOTH V-positions.

**`internal/internal_transclusion_multiple_copies`**: Three copies of "B" at V=1.2, 1.4, 1.5:
```json
{"results": {"1_2": true, "1_3": true, "2_3": true}}
```
All three V-positions share content identity — the I→V mapping scales correctly to N copies.

---

### Part 2: Can the system distinguish original insertion from copy?

**No — not via any built-in field or metadata.**

#### What the POOM crum stores

A POOM leaf crum (`type2dcbc`) contains [via `insertnd` called from `insertpm`, orglinks.c:130]:
- `cdsp.dsas[I]` — I-address (start of the mapped I-range)
- `cdsp.dsas[V]` — V-address (start of the mapped V-range)
- `cwid.dsas[I]` — I-width
- `cwid.dsas[V]` — V-width
- `c2dinfo.homedoc` — the I-address's **native document** (the document whose granfilade allocated this I-space)

The `homedoc` field tells you which document **created** the I-space (i.e., which document first called `inserttextingranf` via `doinsert`). It does NOT record when or why a particular V→I mapping was established.

For self-transclusion within document D:
- Both crums have `homedoc = D` (the same document created the I-space)
- Crum 1: V=v₁, I=x (original insert V-address)
- Crum 2: V=v₂, I=x (copy V-address)

The crums are **structurally identical** except for their V-address.

#### The V-address as implicit ordering

The only observable difference is V-address magnitude. V-addresses are allocated monotonically forward via `findvsatoappend` [orglinks.c:29], which finds the current "end" of document content. The original insert's V-address will be lower (allocated first), and subsequent copies will have higher V-addresses.

However, this is an **emergent property** of sequential V-address allocation, not a formal protocol concept:
- The FEBE protocol does not expose any notion of "original" vs. "copy"
- `insertpm` [orglinks.c:75] treats all insertions identically
- Nothing in `incontextlistnd` marks provenance or creation order
- Finding 0046 explicitly confirms: "NOT from vspanset alone. The ONLY difference is the I-address range [for cross-document copies] ... provenance tracking REQUIRES access to I-addresses, not just V-addresses."

For intra-document self-transclusion, even the I-address is shared, so the only discriminator is V-address ordering — which encodes creation order but not semantic role.

#### What `homedoc` does and does not tell you

`homedoc` in the POOM crum records the **I-space owner**, not the V-mapping history. For a self-transclusion within document D:
- Both crums have `homedoc = D`
- You CAN infer that the I-space was created by D (not transcluded from elsewhere)
- You CANNOT infer which V-position was the "original" mapping

For cross-document transclusion (copy from document A into document B):
- Both crums in B's POOM have `homedoc = A`
- You CAN infer that the I-space originated in A
- You still CANNOT distinguish the order of multiple copies into B from the crum structure alone

---

### Summary

| Question | Answer | Key evidence |
|----------|--------|--------------|
| Does `incontextlistnd` return ALL V-positions for a self-transcluded I-address? | **Yes** | `findcbcinarea2d` [retrie.c:229] visits all siblings via `getrightbro`; `incontextlistnd` [context.c:75] always adds, never replaces; V-restriction is disabled when `span2ptr=NULL` [retrie.c:282] |
| Can the system distinguish original insertion V-position from copy V-position? | **No** | POOM crums store only `(I-addr, V-addr, width, homedoc)` [type2dcbc via insertpm, orglinks.c:75]; no provenance metadata; `homedoc` identifies I-space owner, not V-mapping history |
| What does encode ordering? | V-address magnitude (lower = earlier) | `findvsatoappend` [orglinks.c:29] allocates monotonically; but this is an emergent property, not a protocol concept |

The V-sorted context list returned by `incontextlistnd` will present the original insertion's V-position before the copy's (since lower V-address comes first), but this is a consequence of tumbler ordering — the system has no semantic notion of "original" vs. "copy."

---

## Question 20 [gregory]

> If content is deleted from document A and then the same I-addresses are transcluded back into A from document B (which had previously copied them), does the resulting POOM entry in A become indistinguishable from the original state — i.e., is the round-trip invisible at the POOM level?

### Gregory's Answer

# Gregory Consultation

**Question:** If content is deleted from document A and then the same I-addresses are transcluded back into A from document B (which had previously copied them), does the resulting POOM entry in A become indistinguishable from the original state — i.e., is the round-trip invisible at the POOM level?


## KB Synthesis

## Round-Trip Visibility at the POOM Level

The round-trip is **not invisible at the POOM level**. Several structural distinctions survive, though most observable operations produce identical results.

---

### What remains identical

The I-addresses α₁..αₙ are the same in both the original state and after the round-trip [INV-IADDR-IMMUTABILITY]. The content bytes are identical, and the V→I mapping — if re-inserted at the same V-position — produces the same logical retrieval results. `compare_versions` between original and post-round-trip states would report α₁..αₙ as shared content across both [SS-COMPARE-VERSIONS, INV-TRANSITIVE-IDENTITY]. Link discoverability via `find_links` is also unchanged, since the same I-addresses appear in the spanfilade [INT-LINK-TRANSCLUSION].

---

### What differs internally

**1. The `homedoc` field in POOM crums**

This is the primary structural difference. `isanextensionnd` checks two conditions for coalescing: (1) the new mapping has the same `homedoc` as an existing crum, and (2) the new content is contiguous [ST-INSERT Finding 0062; Finding 0046 in ST-VCOPY]. 

Original INSERT into A produces crums with `homedoc = A`. When B copied from A, B's crums also got `homedoc = A` — because `homedoc` records the I-address origin document, not the most recent copy chain [INV-IADDR-PROVENANCE].

However, when A copies back from B, the sporgl flowing into `docopy` carries `sporgladdress = B` [SS-VSPAN-TO-SPORGL] — B is the document providing the V-span. The POOM crum created for A's re-acquired content thus has `homedoc = B`, not `homedoc = A`.

**Consequence**: If A later inserts text adjacent to the re-acquired content, `isanextensionnd` will fail to coalesce with neighboring native-A crums (different `homedoc`), forcing extra crum creation — equivalent to the CREATELINK coalescing-break penalty described in [EC-GRAN-BOTTOM-SINGLETON via ST-CRUM-BOUND Finding 0063].

**2. A duplicate DOCISPAN entry in the spanfilade**

The original INSERT created a DOCISPAN entry (α₁..αₙ → A) [ST-INSERT Finding 0036]. The DELETE did not remove it [INV-SPANF-WRITE-ONLY]. The re-COPY from B creates a second DOCISPAN entry for the same I-address range also pointing to A [ST-COPY Finding 0047]. The spanfilade now has two entries where the original state had one. `FINDDOCSCONTAINING` still returns A (same logical result), but the spanfilade is measurably larger [INV-SPANF-GROWTH].

**3. Potentially different crum tree topology**

DELETE removes bottom crums and runs `recombinend` [ST-DELETE Finding 0058], possibly leaving a taller tree with empty intermediate nodes (since `levelpull` is disabled [SS-ENFILADE-TREE Finding 0058]). The subsequent INSERT rebuilds the tree from scratch via the normal split path. The final tree topology need not match the original. The two "empty-ish" intermediate states are non-equivalent, as noted for the delete-everything case [EC-EMPTY-DOC Finding 0058].

---

### Summary

| Dimension | Original | After Round-Trip |
|-----------|----------|-----------------|
| I-addresses | α₁..αₙ | α₁..αₙ (identical) |
| V→I mapping | same | same (if same V-position) |
| `homedoc` in crum | A | B |
| DOCISPAN count | 1 | 2 |
| POOM tree shape | T₁ | T₂ (potentially different height/structure) |
| Content retrieval | "X..." | "X..." (identical) |
| `compare_versions` | shared content found | shared content found (identical) |

The round-trip preserves full content identity and observable retrieval behavior. It is not invisible at the implementation level: the `homedoc` distinction alters future coalescing behavior [INV-IADDR-PROVENANCE], the spanfilade accumulates a redundant entry [INV-SPANF-WRITE-ONLY], and the POOM tree structure may differ [SS-ENFILADE-TREE]. These are internal state differences that would only become observable through unusual access patterns — specifically, subsequent adjacent-insertion coalescing and spanfilade growth bounds.

---

## Code Exploration

Here is my full answer, based on direct reading of the source.

---

## The Round-Trip Question: Is It Invisible at the POOM Level?

**Short answer: logically yes, structurally no. The `homedoc` field is identical in both cases (always zero). The V→I mapping is preserved. The internal crum tree will differ.**

---

### What a POOM Bottom Crum Actually Stores

From `enf.h:109-131` and `wisp.h:107-110`, a `type2dcbc` (2-D POOM bottom crum) contains exactly five values:

| Field | Meaning |
|-------|---------|
| `cwid.dsas[I]` | I-space width |
| `cwid.dsas[V]` | V-space width |
| `cdsp.dsas[I]` | I-displacement (relative to parent in tree) |
| `cdsp.dsas[V]` | V-displacement (relative to parent in tree) |
| `c2dinfo.homedoc` | A tumbler: the "home document" identifier |

```c
/* wisp.h:107-110 */
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

There is no timestamp, source-doc trail, or insertion-count in the crum. The only non-coordinate metadata is `homedoc`.

---

### The `homedoc` Field Is Always ZERO on the Normal Copy Path

`docopy` [do1.c:53-64] always calls `specset2ispanset` **before** `insertpm`:

```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)
```

`specset2ispanset` [do2.c:14-46] converts any VSPECID items into ISPANID items by looking up the source document's POOM via `vspanset2ispanset` → `permute` → `retrieverestricted`. The output is always ISPANID-tagged spans.

Inside `insertpm` [orglinks.c:100-101], `unpacksporgl` [sporgl.c:178-203] reads those ISPANID items:

```c
/* sporgl.c:180-183 */
if (itemid == ISPANID) {
    movetumbler(&ispanset->stream, streamptr);
    movetumbler(&ispanset->width, widthptr);
    tumblerclear(&infoptr->homedoc);   /* ← homedoc = ZERO */
}
```

**`homedoc` is cleared to zero for every path that goes through ISPANID sporgls.** That includes:

- **Original insertion** via `doinsert` → `inserttextingranf` → ISPANID → `homedoc = ZERO`
- **Copy from B** → `specset2ispanset` converts VSPEC to ISPANID → `homedoc = ZERO`
- **Re-transclusion back into A** → same path → `homedoc = ZERO`

The POOM provenance chain is severed at insertion. The POOM does not record which document "donated" the I-addresses. (Note: the SPAN enfilade does set `homedoc = isaptr` for ISPANID items in `insertspanf` [spanf1.c:29] — but we're talking about the POOM, where it's always zero on this path.)

---

### Deletion: What `dodeletevspan` Does to the Tree

`dodeletevspan` [do1.c:158-167] → `deletevspanpm` [orglinks.c:145-152] → `deletend` [edit.c:31-76]:

```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

`deletend` cuts the tree at the delete boundaries, then for each child crum:

- **Case 1** — fully inside deletion range: `disown` + `subtreefree` [edit.c:59-60] — crum is **freed and gone**
- **Case 2** — to the right of the deletion: [edit.c:63]
  ```c
  tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
  ```
  The V-displacement shrinks by `width`, closing the V-gap.

Then `setwispupwards` [edit.c:74] + `recombine` [edit.c:75] restructure the tree. The original crums that held the deleted V-span are **permanently freed** — they do not survive.

---

### Re-transclusion: What `docopy` from B Creates

When A calls `docopy(taskptr, A_isa, vsaptr, B_vspec)`:

1. `specset2ispanset` looks up B's POOM → returns the same I-addresses (I1..I2) as ISPANID items. B's POOM holds them because B previously copied from A.

2. `insertpm` [orglinks.c:113-117] computes V-width for each new crum:
   ```c
   shift = tumblerlength(vsaptr) - 1;
   inc   = tumblerintdiff(&lwidth, &zero);
   tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);
   ```
   V-width = `inc × 10^(−shift)`. If `vsaptr` is the same V-position as the original insertion (same tumbler length, same `shift`), and the I-width is the same content, the computed V-width is **identical** to the original.

3. `makegappm` [insertnd.c:124-172] opens V-space by shifting crums at V ≥ vsaptr rightward:
   ```c
   /* insertnd.c:162 */
   tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
   ```
   This is the exact inverse of what `deletend` case-2 did. The surrounding crums' absolute V-positions are restored to their pre-deletion values.

4. `insertcbcnd` [insertnd.c:242-275] tries to extend a neighboring crum via `isanextensionnd` [insertnd.c:301-309]:
   ```c
   if (!tumblereq(&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
       return (FALSE);
   prologuend((typecorecrum*)ptr, offsetptr, &grasp, &reach);
   return (lockeq(reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
   ```
   Extension requires (a) `homedoc` matches (both ZERO — so always passes ✓) and (b) the reach of the existing crum equals the origin of the new content **in both V and I simultaneously**. If this fails, a fresh crum is created via `createcrum(0, POOM)` [insertnd.c:260].

5. `recombine` [insertnd.c:76] restructures the tree after insertion.

---

### What Is Preserved vs. What Differs After the Round-Trip

**Preserved (logically identical):**

| Property | Reason |
|----------|--------|
| I-addresses in A's POOM | `specset2ispanset` on B returns the same I-spans A originally held |
| V-positions of re-inserted content | Same vsaptr → same `shift` → same V-width |
| V-positions of surrounding content | `deletend` case-2 shifted them −width; `makegappm` shifts them +width; net = zero |
| `homedoc` field | ZERO in both cases [sporgl.c:183] |

**Not preserved (structurally different):**

| Property | Why |
|----------|-----|
| Number of crums | Old crums freed via `subtreefree` [edit.c:59]; new ones allocated fresh by `createcrum` [insertnd.c:260] |
| Crum boundaries | B's POOM may split [I1..I2) differently; `specset2ispanset` returns one I-span per crum in B's tree |
| Tree height | `recombine` [recombine.c:22-34] makes locally optimal choices based on current tree state |
| Relative `cdsp` values | Computed relative to tree parent, which changes after restructuring |
| Adjacency merging | Whether `isanextensionnd` fires at all depends on the specific post-deletion crum layout |

---

### The Key Design Implication

**The POOM has no provenance memory.** It cannot distinguish content that was:

- Originally typed into a document
- Copied from another document  
- Deleted and re-transcluded from a third document

All three cases yield `homedoc = ZERO`. The only thing that survives is the V→I mapping. This is by design: in Xanadu's model, content *is* its I-addresses. How it arrived is not the POOM's concern — that provenance lives in the granfilade (which holds the actual bytes at permanent I-addresses) and in whatever link structure was built above it.

**The round-trip is invisible at the observable behavior level** (queries, retrieval, link following all return the same results), but **the internal tree structure will differ** — different number of crums, different crum boundaries, different tree height, different node-relative displacement values — because the original crums were freed and new ones built from scratch.

---

*Finding written to `findings/0079-poom-round-trip-structural-vs-logical-identity.md`.*

---

## Question 21 [gregory]

> Does `vspanset2sporglset` preserve the I-address contiguity structure when converting V-spans to sporgls — specifically, if a V-span maps to three non-contiguous I-address ranges (due to interleaved edits), does the resulting sporgl set contain exactly three entries that individually trace back to three distinct insertion operations?

### Gregory's Answer

# Gregory Consultation

**Question:** Does `vspanset2sporglset` preserve the I-address contiguity structure when converting V-spans to sporgls — specifically, if a V-span maps to three non-contiguous I-address ranges (due to interleaved edits), does the resulting sporgl set contain exactly three entries that individually trace back to three distinct insertion operations?


## KB Synthesis

## Answer: `vspanset2sporglset` and I-address Contiguity Preservation

**Yes, exactly three sporgl entries result from three non-contiguous I-address ranges, and they do individually correspond to distinct I-address ranges from separate allocation events.** Here is the complete picture.

---

### The Conversion Mechanism

The function `vspanset2sporglset` converts V-spans to sporgls through this chain:

> V-span → `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` → one I-span per contiguous I-address region → one sporgl per I-span

`[ST-LINK-CREATE]` (Finding 0037) documents the critical inner loop at `sporgl.c:49-58`: it iterates over **every** I-span returned by `vspanset2ispanset` and creates a **separate sporgl for each**. The granularity of the output is one sporgl per contiguous I-address region — no merging, no consolidation across gaps.

`[SS-VSPAN-TO-SPORGL]` (Finding 0013) confirms the two-step process: (1) convert V-addresses to I-addresses via `vspanset2ispanset`, then (2) attach the source document ISA to each resulting I-span as the `sporgladdress` field. Each sporgl carries:

- `sporglorigin` — I-address start of the contiguous range  
- `sporglwidth` — width of that range  
- `sporgladdress` — the document ISA (provenance)

For a V-span mapping to **N** non-contiguous I-address regions, `|sporgl_set| = N`. Three non-contiguous regions yield exactly three sporgls.

---

### Why Three Non-Contiguous Ranges Arise from Interleaved Edits

`[INV-MONOTONIC]` (Findings 0033, 0061) establishes that I-address allocation is strictly monotonically increasing and append-only. Contiguous V-content from a **single uninterrupted INSERT** gets contiguous I-addresses. Non-contiguity arises specifically when other allocation-consuming operations intervene.

`[INT-LINK-INSERT]` (Finding 0063) provides the clearest example: INSERT "ABC" allocates I.1–I.3; CREATELINK allocates a link orgl in the same address space; INSERT "DEF" then gets I-addresses starting well above I.3. The resulting two text regions are non-contiguous in I-space, even though they appear contiguous in V-space. The same pattern extends to three insertions with two interleaved operations, or to transclusion from multiple sources.

`[SS-DOCISPAN]` (Finding 0047) notes that DOCISPAN entry granularity is per-I-span: inserting 10 contiguous bytes creates 1 entry (1 contiguous I-span), while copying 3 non-contiguous regions creates 3 entries (3 I-spans). This confirms the same granularity model applies throughout the system.

---

### Do the Three Sporgls Trace to Three Distinct Allocation Events?

**Yes**, given the premise that the non-contiguity arose from interleaved edits, each non-contiguous I-address range necessarily reflects a distinct allocation epoch. `[INV-MONOTONIC]` guarantees:

- I-address allocation is strictly monotonic and stateless (a pure function of granfilade state)  
- Gaps between I-address ranges only arise when other allocations (text INSERT, CREATELINK, etc.) consumed addresses in between  
- `[INV-NO-IADDR-REUSE]` ensures no I-address is ever reused, so each range is permanently identifiable with its allocation event

However, a qualifier: the sporgl structure itself carries **document provenance** (`sporgladdress`), not operation-level metadata. All three sporgls in this case would share the same `sporgladdress` (the same document ISA) if the ranges were all inserted into the same document. What differentiates them is the `sporglorigin` + `sporglwidth` pair identifying the distinct I-address range. To trace each sporgl to a *specific* INSERT operation, external knowledge of the insertion sequence (or comparison of I-address ranges against the allocation timeline) would be required — the sporgl alone does not carry an operation timestamp or operation identifier.

---

### Concrete Example

```
INSERT "AAA" → I-addresses I.1, I.2, I.3
CREATELINK   → link orgl allocated at I.2.x (advances allocator)
INSERT "BBB" → I-addresses I.2.1, I.2.2, I.2.3 (gap from I.3)
CREATELINK   → link orgl allocated at I.3.x
INSERT "CCC" → I-addresses I.3.1, I.3.2, I.3.3 (second gap)
```

V-stream now: "AAABBBCCC" — a single contiguous V-span, but mapping to **three** non-contiguous I-address ranges.

`vspanset2sporglset` on this V-span:
1. `vspanset2ispanset` → `permute` → `span2spanset` walks the POOM, discovers three contiguous I-spans
2. Inner loop creates three sporgls:
   - Sporgl₁: origin=I.1, width=3, doc=D
   - Sporgl₂: origin=I.2.1, width=3, doc=D  
   - Sporgl₃: origin=I.3.1, width=3, doc=D

Result: exactly three sporgl entries, one per non-contiguous I-address range, each tracing to a distinct allocation epoch. `[ST-LINK-CREATE]`, `[INT-LINK-INSERT]`, `[INV-MONOTONIC]`

---

### Frame Conditions

`[SS-VSPAN-TO-SPORGL]` notes the conversion is a **pure read**: it reads the document's V→I mapping but does not modify any state. The sporgl set is fully determined by the current POOM state at conversion time. If further interleaved edits occur between conversion calls, the sporgl count for the same V-span may change.

`[SS-POOM-MULTIMAP]` (Finding 0039) confirms the POOM is a multimap accumulating all matching contexts during traversal — the retrieval never drops contexts, so no contiguous region is missed.

---

## Code Exploration

I have a complete trace. Here is the full answer.

---

## Does `vspanset2sporglset` Preserve I-Address Contiguity Structure?

**Short answer: Yes.** The function is structurally transparent to non-contiguous I-address ranges. If a V-span maps to three non-contiguous I-address regions, the resulting sporgl set contains exactly three entries, each corresponding to a distinct POOM leaf crum (i.e., a distinct insertion operation), provided each I-region comes from exactly one leaf crum.

---

## Full Execution Trace

### 1. Entry point — `vspanset2sporglset` [sporgl.c:35–65]

```c
typesporglset *vspanset2sporglset(typetask *taskptr, typeisa *docisa,
    typevspanset vspanset, typesporglset *sporglsetptr, int type)
{
    typeorgl orgl;
    typesporgl *sporglset;
    typeispanset ispanset, *vspanset2ispanset();

    ispanset = NULL;
    if (!findorgl (taskptr, granf, docisa, &orgl, type))   // [sporgl.c:44]
        return (NULL);
    for (; vspanset; vspanset = vspanset->next) {          // [sporgl.c:47]
        (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset); // [sporgl.c:48]
        for (; ispanset; ispanset = ispanset->next) {       // [sporgl.c:49]
            sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
            sporglset->itemid = SPORGLID;
            sporglset->next = NULL;
            movetumbler (docisa, &sporglset->sporgladdress); // [sporgl.c:53]
            movetumbler(&ispanset->stream, &sporglset->sporglorigin); // [sporgl.c:54]
            movetumbler (&ispanset->width, &sporglset->sporglwidth);  // [sporgl.c:55]
            *sporglsetptr = (typesporglset)sporglset;
            sporglsetptr = (typesporglset *)&sporglset->next;
        }
    }
```

Key structural facts:
- `ispanset` is initialized to `NULL` once [sporgl.c:43], then consumed entirely by the inner `for` loop. After the inner loop completes, `ispanset` is `NULL` again (it advanced to the end of the list). Each subsequent call to `vspanset2ispanset` starts with a fresh `NULL` ispanset.
- The inner loop produces **one sporgl per ispan** — no merging, no deduplication.
- Each sporgl records `sporgladdress = docisa`, `sporglorigin = ispanset->stream`, `sporglwidth = ispanset->width`.

### 2. V→I translation — `vspanset2ispanset` [orglinks.c:397–402]

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl,
    typevspanset vspanptr, typeispanset *ispansetptr)
{
    typespanset *permute();
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I); // [orglinks.c:401]
}
```

Delegates entirely to `permute` with the restriction index = `V` and target index = `I`.

### 3. `permute` [orglinks.c:404–422]

```c
typespanset *permute(typetask *taskptr, typeorgl orgl, typespanset restrictionspanset,
    INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
    typespanset *save;
    save = targspansetptr;
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) // [orglinks.c:414]
        targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                      restrictionindex, targspansetptr, targindex);
    return (save);  // [orglinks.c:421]
}
```

Returns `save` — the original pointer `&ispanset` — not the advanced tail pointer. For a single V-span, calls `span2spanset` exactly once.

### 4. `span2spanset` [orglinks.c:425–454]

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, typespanset restrictionspanptr,
    INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
    typecontext *context, *c, *retrieverestricted();
    typespan foundspan;
    typespan *nextptr;
    typeitem *onitemlist();

    context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                                 (typespan*)NULL, targindex, (typeisa*)NULL); // [orglinks.c:435]
    for (c = context; c; c = c->nextcontext) {               // [orglinks.c:439]
        context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex); // [orglinks.c:443]
        nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan,
                                          (typeitemset*)targspansetptr); // [orglinks.c:444]
    }
    if (!context) return(targspansetptr);
    contextfree (context);
    return (&nextptr->next);
}
```

This is the heart of the mechanism. `retrieverestricted` is called with `span2ptr = NULL` and `docisaptr = NULL`, meaning **the I-axis is unconstrained** — only the V-span restriction applies. Every POOM leaf crum that overlaps the V-span is returned as a separate context entry.

### 5. `retrieverestricted` → `findcbcinarea2d` [retrie.c:56–85, 229–268]

```c
typecontext *retrieverestricted(typecuc *fullcrumptr, typespan *span1ptr, INT index1,
    typespan *span2ptr, INT index2, typeisa *docisaptr)
{
    // span2ptr is NULL → span2start=0, span2end=0
    // docisaptr is NULL → infoptr=NULL
    temp = retrieveinarea(fullcrumptr, &span1start, &span1end, index1,
                          &span2start, &span2end, index2, (typebottomcruminfo*)infoptr);
    return(temp);
}
```

→ `retrieveinarea` → `findcbcinarea2d`:

```c
int findcbcinarea2d(typecorecrum *crumptr, typedsp *offsetptr, ...)
{
    for (; crumptr; crumptr = getrightbro (crumptr)) {         // [retrie.c:252]
        if (!crumqualifies2d (...)) continue;
        if (crumptr->height != 0) {
            dspadd (offsetptr, &crumptr->cdsp, &localoffset, ...);
            findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...); // recurse
        } else {
            context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
            incontextlistnd (headptr, context, index1);        // [retrie.c:263]
        }
    }
}
```

This recursively walks the **entire** POOM tree, not just the first match. Every leaf crum that qualifies via `crumqualifies2d` becomes a separate context node. `incontextlistnd` [context.c:75–111] inserts each context into a sorted linked list **without merging**.

`crumqualifies2d` [retrie.c:270–305] tests the I-axis unconstrained when `span2end` is zero [retrie.c:292]: `endcmp = iszerotumbler(span2end) ? TOMYRIGHT : ...`, so any I-address range passes.

**Result: if the V-span overlaps three distinct POOM leaf crums, three separate `typecontext` nodes are returned.**

### 6. `context2span` [context.c:176–212]

For each context (POOM leaf crum), this function clips the I-span to match the portion of the V-span that the crum covers:

```c
int context2span(typecontext *context, typespan *restrictionspanptr,
    INT idx1, typespan *foundspanptr, INT idx2)
{
    movetumbler (&restrictionspanptr->stream, &lowerbound);
    tumbleradd (&lowerbound, &restrictionspanptr->width, &upperbound);
    prologuecontextnd (context, &grasp, &reach);

    if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS)  // [context.c:191]
        tumblerincrement (&grasp.dsas[idx2], 0,
            (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]), &grasp.dsas[idx2]);
    if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER) // [context.c:197]
        tumblerincrement (&reach.dsas[idx2], 0,
            - tumblerintdiff (&reach.dsas[idx1], &upperbound), &reach.dsas[idx2]);

    movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);  // [context.c:206]
    tumblersub(&reach.dsas[idx2],&grasp.dsas[idx2],&foundspanptr->width); // [context.c:207]
}
```

The proportional adjustment is **V-axis linear**: it trims the I-address range in exact proportion to how much of the V-span is clipped at each end. This works correctly because each POOM crum records a linear V↔I mapping (contiguous V-range → contiguous I-range, same width in both axes at the same tumbler depth).

### 7. `onitemlist` [orglinks.c:464–537]

Appends each `foundspan` to the target spanset. The function walks to the end of the linked list and appends [orglinks.c:534]:

```c
((typeitemheader *)temp)->next = (typeitemheader *)newitem;
```

**No merging.** Even if two adjacent I-spans happened to be adjacent in the address space, `onitemlist` would not merge them — it only appends. (The merge logic `putvspaninlist` [orglinks.c:329–387] is a different function, used in a different path.)

---

## The Three-Non-Contiguous-Ranges Case

When a V-span maps to three non-contiguous I-address ranges due to interleaved edits, the situation in the POOM is:

```
POOM leaf crums overlapping the V-span:
  crum A:  V=[v1, v1+w1)  →  I=[i1, i1+w1)     (insertion 1)
  crum B:  V=[v2, v2+w2)  →  I=[i2, i2+w2)     (insertion 2, different I-region)
  crum C:  V=[v3, v3+w3)  →  I=[i3, i3+w3)     (insertion 3, different I-region)
  where i1, i2, i3 are non-contiguous
```

`findcbcinarea2d` finds all three crums (one context per crum). `span2spanset` calls `context2span` three times → three ispans. `onitemlist` appends all three without merging. Back in `vspanset2sporglset`, the inner loop allocates three sporgls.

Each sporgl records:
- `sporgladdress` = the document ISA (same for all three, from `docisa`) [sporgl.c:53]
- `sporglorigin` = the I-start of that crum's I-range, clipped if needed [sporgl.c:54]
- `sporglwidth` = the I-width of that crum's I-range [sporgl.c:55]

Since `i1`, `i2`, `i3` are non-contiguous by assumption, the three `sporglorigin` values are distinct and non-adjacent, and they individually identify the three insertion operations.

---

## Verdict

**`vspanset2sporglset` preserves the I-address contiguity structure exactly.** The function is structurally 1-to-1: each POOM leaf crum that overlaps the input V-span contributes exactly one sporgl to the output, carrying that crum's I-address range (clipped to the V-span boundary). There is no merging at any stage — not in `incontextlistnd` [context.c:75], not in `onitemlist` [orglinks.c:464], not in the inner loop of `vspanset2sporglset` [sporgl.c:49].

If a V-span maps to three non-contiguous I-address ranges due to interleaved edits, the sporgl set will contain **exactly three entries** corresponding to **three distinct POOM leaf crums** corresponding to **three distinct insertion operations**, under the normal assumption that each insertion creates a single contiguous I-span in the granfilade (one leaf crum per insert).

The only case where the count could differ is if a single non-contiguous I-region is itself split across multiple POOM crums (which would be a POOM structural anomaly, not a normal case), or if two crums happen to have adjacent I-ranges that a hypothetical merge step would collapse — but `onitemlist` does not perform that merge.

---

## Question 22 [gregory]

> For DOCISPAN entries created by COPY versus INSERT, is there any structural difference in the spanfilade entry that would allow distinguishing "this document contains original content" from "this document contains transcluded content," or are both recorded identically as `(document, i-address, width)` tuples?

### Gregory's Answer

# Gregory Consultation

**Question:** For DOCISPAN entries created by COPY versus INSERT, is there any structural difference in the spanfilade entry that would allow distinguishing "this document contains original content" from "this document contains transcluded content," or are both recorded identically as `(document, i-address, width)` tuples?


## KB Synthesis

Both INSERT and COPY record **structurally identical** DOCISPAN entries. There is no provenance field distinguishing "original" from "transcluded" content.

## The DOCISPAN Entry Structure

From [SS-DOCISPAN] (Finding 0047), `insertspanf` creates entries by iterating over an `ispanset` linked list and making one `insertnd` call per `typeispan` struct. The `typeispan` struct (per [SS-SPAN]) contains only:

- `stream` — start I-address
- `width` — byte count

No origin-document field. The resulting DOCISPAN entry is a `(document_ISA, i-start, i-width)` triple, period.

## Both Operations Flow Through the Same Call

Both INSERT and COPY terminate at the same `docopy()` function, which makes the identical call:

```c
insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

- **INSERT path:** `doinsert` → `inserttextingranf` (allocates fresh I-addresses) → `docopy` → `insertspanf(..., DOCISPAN)` [ST-INSERT, Finding 0036]
- **COPY path:** `docopy` directly → `insertspanf(..., DOCISPAN)` [ST-COPY, Finding 0047]

The `docisaptr` is the **target** document in both cases. The `ispanset` carries the I-addresses being placed — fresh ones for INSERT, existing ones for COPY. The entry records only "this document now contains these I-addresses," with no tag for how they arrived.

## Provenance Is Implicit, Not Recorded

[INV-IADDR-PROVENANCE] (Finding 0046) confirms: "Provenance tracking requires I-address inspection — from V-addresses alone, INSERT and COPY produce indistinguishable POOM structures."

The I-address value itself encodes provenance implicitly — because I-addresses are allocated within a document-scoped namespace ([SS-ADDRESS-SPACE], Finding 0065), an I-address like `1.1.0.1.0.1.3.0.1.5` identifies its native document by prefix. But that's reading the address value, not consulting any field in the DOCISPAN entry.

## Sporgls Carry Provenance, But Not for DOCISPAN

The sporgl structure does include a `sporgladdress` field (the origin document ISA) per [SS-SPORGL]. However, sporgls are used exclusively for **link endpoint indexing** via `insertendsetsinspanf()` [INT-SPORGL-LINK-INDEX]. DOCISPAN entries use plain `typeispan` structs through `insertspanf` — a completely separate insertion path that discards provenance.

## Summary

The spanfilade DOCISPAN sub-index cannot distinguish original from transcluded content by entry structure alone. Both record `(document, i-address-start, i-width)` identically. To determine whether content is "native" to a document vs transcluded, a caller must inspect the I-address value itself and compare it against the document's allocation namespace — which is an out-of-band inference, not a stored field.

---

## Code Exploration

I now have all the information needed to give a definitive answer. Let me trace both code paths completely.

---

## Answer

**Both INSERT and COPY produce structurally identical DOCISPAN entries in the spanfilade. There is no flag, tag, or field that distinguishes "original" from "transcluded" content at the storage level.**

Here is the full proof by source tracing.

---

### 1. The INSERT code path

`doinsert` in `do1.c:87-123`:

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset));
    return(ret);
}
```

`inserttextingranf` → `inserttextgr` (`granf2.c:83-109`) allocates **new, previously unused** permascroll addresses and writes the text bytes into the granfilade. It returns an `ispanset` containing `(new_permascroll_addr, width)`. Then `doinsert` immediately calls `docopy` with that `ispanset`.

---

### 2. The COPY code path

`docopy` in `do1.c:45-65`:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && asserttreeisok(docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
    && asserttreeisok(docorgl)
    );
}
```

`specset2ispanset` converts the source vspec (a virtual address in some document) to a set of **pre-existing** permascroll i-addresses. Those i-addresses already exist in the granfilade because some prior INSERT wrote them there.

---

### 3. Both paths converge on the same call

The INSERT path calls `docopy` after generating new i-addresses. The COPY path calls `docopy` directly. Both ultimately execute:

```c
insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

with exactly the same argument types and meaning.

---

### 4. What `insertspanf` stores

`insertspanf` in `spanf1.c:15-54`:

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr,
                 typesporglset sporglset, INT spantype)
{
    prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);   // line 22
    tumblerclear (&crumwidth.dsas[ORGLRANGE]);                        // line 23
    clear (&linfo, sizeof(linfo));                                    // line 24
    for (; sporglset; ...) {
        if (itemid == ISPANID) {
            movetumbler (&ispan->stream, &lstream);                  // line 27
            movetumbler (&ispan->width, &lwidth);                    // line 28
            movetumbler (isaptr, &linfo.homedoc);                    // line 29
        }
        movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);         // line 49
        movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);           // line 50
        insertnd(taskptr, (typecuc*)spanfptr, &crumorigin,
                 &crumwidth, &linfo, SPANRANGE);                     // line 51
    }
}
```

`DOCISPAN` is defined in `xanadu.h:39` as the integer constant `4`:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

`prefixtumbler` (`tumble.c:641-651`) prepends the integer `4` to the document ISA tumbler to form the ORGL-dimension key.

---

### 5. The bottom crum data structure

The leaf node stored by `insertnd` is a `type2dcbc` (2-D core bottom crum). Its crum-info field is `type2dbottomcruminfo`, defined in `wisp.h:107-109`:

```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

**One field only: `homedoc`.** This is set to `*isaptr` — the document ISA — in both the INSERT and COPY paths (line 29 of `spanf1.c`).

The complete spanfilade bottom crum for a DOCISPAN entry therefore contains exactly these components:

| Component | Value | Source |
|-----------|-------|--------|
| `cdsp.dsas[ORGLRANGE]` | `prefixtumbler(docISA, 4)` | `spanf1.c:22` |
| `cdsp.dsas[SPANRANGE]` | i-address (permascroll address) | `spanf1.c:49` |
| `cwid.dsas[ORGLRANGE]` | 0 (point in ORGL dimension) | `spanf1.c:23` |
| `cwid.dsas[SPANRANGE]` | width of content | `spanf1.c:50` |
| `c2dinfo.homedoc` | document ISA | `spanf1.c:29` |

---

### 6. Conclusion

**There is no structural difference.** For COPY, the `ispanset` contains i-addresses that were previously written to the permascroll by some other document's INSERT. For INSERT, the `ispanset` contains freshly allocated i-addresses that have just been written. In both cases `insertspanf` is called with `DOCISPAN` and the same document ISA, storing the same `(doc-prefix, i-address, width, homedoc)` tuple.

The only observable difference lies in the **value** of the i-address stored in `cdsp.dsas[SPANRANGE]`:
- **Original content** (inserted by this document): the i-address was newly allocated by `inserttextgr` (`granf2.c:84-109`) for this document.
- **Transcluded content** (copied from another document): the i-address already existed in the granfilade because it belongs to the source document's permascroll slot.

To distinguish them you would have to cross-reference the i-address against other documents' spanfilade DOCISPAN entries — if the same i-address range appears in more than one document's DOCISPAN entries, it is transcluded content. That relationship is implicit in the data rather than stored as a flag. The spanfilade entry itself is recorded identically as `(document, i-address, width)` in both cases.

---

## Question 23 [gregory]

> When APPEND adds content without creating a DOCISPAN entry (the commented-out `insertspanf` call), is the appended content's I-address still discoverable through any other mechanism — for example, by querying the granfilade directly via `findpreviousisagr` — or is there truly no path from an external document to discover that content exists?

### Gregory's Answer

# Gregory Consultation

**Question:** When APPEND adds content without creating a DOCISPAN entry (the commented-out `insertspanf` call), is the appended content's I-address still discoverable through any other mechanism — for example, by querying the granfilade directly via `findpreviousisagr` — or is there truly no path from an external document to discover that content exists?


## KB Synthesis

## APPEND Content: Discovery Analysis

The appended content's I-address is **truly undiscoverable** from an external document via any mechanism. Here is why each potential path is blocked.

### What APPEND Does Create

APPEND does store content in the granfilade — the I-address is permanently allocated and the bytes are accessible via direct V-address query on the owning document. [EC-APPEND-NO-DOCISPAN] confirms the content exists in the granf but the `insertspanf(..., DOCISPAN)` call is commented out.

### Blocked Discovery Paths

**DOCISPAN (spanfilade) — BLOCKED**

This is the canonical reverse-index mechanism. [SS-DOCISPAN] defines it as the only mapping from I-addresses to containing documents. [INV-SPANF-WRITE-ONLY] confirms the spanfilade is write-only and [ST-APPEND-NO-DOCISPAN] explicitly states APPEND omits this step. No DOCISPAN entry means `FINDDOCSCONTAINING` returns nothing for the appended I-addresses.

**`findpreviousisagr` — NOT A DISCOVERY MECHANISM**

This function ([SS-ADDRESS-ALLOC]) finds the *highest existing I-address below a bound* for the purpose of allocation. It tells you an I-address slot exists in the granfilade tree — it does not tell you which document contains it. The mapping from I-address to document is entirely the spanfilade's job. Even if you enumerated every I-address in the granfilade via repeated `findpreviousisagr` calls (itself not a FEBE operation), you would have a list of addresses with no way to associate them with documents without DOCISPAN entries.

**`compare_versions` — BLOCKED**

This uses I-address intersection between two documents ([SS-COMPARE-VERSIONS]). An external document can only share I-addresses with the appended content if it previously received those I-addresses via COPY/vcopy. But COPY requires knowing the content exists and where to find it — which requires DOCISPAN registration in the first place. You cannot bootstrap discovery this way.

**`find_links` — BLOCKED**

Link discovery searches the spanfilade by I-address intersection [SS-FIND-LINKS]. Same dependency on DOCISPAN.

**Direct document access — Not identity-based discovery**

If you already know the owning document's address, open it, and query its V-span extent, you can retrieve the appended content. But this is positional access to a known document — not discovery of content from identity. This path requires prior knowledge of the document, not discovery from the content itself.

### The Structural Reason

[INT-DELETE-SPANF-DIVERGENCE] captures the core architectural fact: the spanfilade and POOM (granf) are two independent layers with no automatic synchronization. DOCISPAN registration is the **only** mechanism that creates the I-address → document association. Since APPEND deliberately skips `insertspanf`, the registration simply never happens.

From [INV-IADDRESS-PERMANENT]: the I-address is allocated permanently and the content bytes persist forever. But permanence in the granfilade is not the same as discoverability via the spanfilade. The appended content occupies a permanent address in the content store while remaining completely opaque to the identity-discovery subsystem.

**Summary:** There is no path. APPEND creates content in a permanent but invisible state — accessible only by positional query on the owning document by a caller who already knows to look there.

---

## Code Exploration

I now have all the source evidence needed. Here is the full analysis:

---

## The Commented-Out `insertspanf` in `doappend` — Full Trace

### The Premise Is Partially Incorrect: DOCISPAN Entries *Are* Created

The question assumes APPEND omits the spanfilade registration. This is not what the code does. Let me trace the entire execution path.

---

### Step 1: `doappend` — the commented-out call

```c
bool doappend(typetask *taskptr, typeisa *docptr, typetextset textset)
{
  bool appendpm(),insertspanf(); /*zzz dies this put in granf?*/

    return (appendpm (taskptr, docptr, textset)/*&&
   appendpm includes insertspanf!   insertspanf(taskptr,spanf,docptr,textset,DOCISPAN)*/
    );
}
```
[`do1.c:25-32`]

The active call is `appendpm`. The `insertspanf(taskptr,spanf,docptr,textset,DOCISPAN)` line is commented out. Critically, the developer left a note: **"appendpm includes insertspanf!"** — which is correct, as the trace below proves.

`doappend` is invoked internally only — from `sourceunixcommand` in `xumain.c:144` when loading a Unix command's output into a new document line-by-line. It is not a FEBE protocol request (no `APPEND` request code exists in `requests.h`).

---

### Step 2: `appendpm` — finds the next append V-address, then calls `doinsert`

```c
bool appendpm(typetask *taskptr, typeisa *docisaptr, typetextset textset)
{
  typeorgl orglptr;
  tumbler vsa;
  bool findorgl(), doinsert();

    if (!findorgl(taskptr, granf, docisaptr, &orglptr, WRITEBERT))
        return(FALSE);
    findvsatoappend((typecorecrum*)orglptr, &vsa);
    return (doinsert(taskptr, docisaptr, &vsa, textset));
}
```
[`orglinks.c:17-27`]

`appendpm` computes the next V-space address via `findvsatoappend` and delegates directly to `doinsert`. It does not itself call `insertspanf`.

---

### Step 3: `doinsert` — allocates I-space, then calls `docopy`

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
  typehint hint;
  typespanset ispanset;
  ...
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset)
    /* no ht stuff here, 'cause it's taken care of in */
    /*   docopy */ );
    return(ret);
}
```
[`do1.c:87-123`]

1. `inserttextingranf` → `inserttextgr` in `granf2.c:83-109` allocates a sequential I-address in the granfilade and returns an `ISPANID`-typed `ispanset` carrying the I-span (stream + width).
2. `docopy` is called with that `ispanset`.

---

### Step 4: `docopy` — this is where `insertspanf(DOCISPAN)` IS called

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
  typeispanset ispanset;
  typeorgl docorgl;
  ...
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && asserttreeisok(docorgl)
    /* the meat of docopy: */
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
    &&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
    && asserttreeisok(docorgl)
    );
}
```
[`do1.c:45-65`]

**`insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` is executed** — `do1.c:62`. The DOCISPAN entry is written to the spanfilade.

---

### What the Two `insertspanf` Paths Would Have Done Differently

The commented-out call in `doappend` was:
```c
insertspanf(taskptr, spanf, docptr, textset, DOCISPAN)
                                    ^^^^^^^
                                    typetextset — TEXTID items
```

The actual call (through `docopy`) is:
```c
insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
                                       ^^^^^^^^^
                                       typeispan * — ISPANID items
```

`insertspanf` in `spanf1.c:15-54` handles both types differently:

- **ISPANID path** (actual): `lstream = ispanptr->stream`, `lwidth = ispanptr->width`, `linfo.homedoc = docisa`. The SPANRANGE dimension of the spanfilade crum records the true I-span (granfilade address + width).
- **TEXTID path** (commented out): `lstream = docisa`, `lwidth = {0, text_length}`, `linfo.homedoc = docisa`. The SPANRANGE records the document ISA itself as the span origin — a degenerate form that conflates I-space with the document's own ISA. This would not encode the real permascroll location.

The TEXTID path was architecturally wrong for DOCISPAN (the purpose of DOCISPAN is to map `docisa → I-span` so that `finddocscontainingsp` can invert it). The developer correctly left that path commented out. The ISPANID path through `docopy` is the correct one.

---

### Can `findpreviousisagr` Serve as an Alternative Discovery Path?

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{ RECURSIVE    /* findpreviousisagr*/
  ...
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if (
         (tmp= whereoncrum (ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
        || tmp == ONMYRIGHTBORDER
        || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);
        }
    }
}
```
[`granf2.c:255-278`]

`findpreviousisagr` walks the granfilade tree and returns the highest I-address that exists below a given `upperbound`. It is **purely an internal allocation oracle**, used by `findisatoinsertmolecule` and `findisatoinsertnonmolecule` to find where to allocate the next I-address. It is not a general-purpose "does this content exist" query.

For `findpreviousisagr` to tell you that specific content exists:
1. You must already know the approximate I-address neighborhood (e.g., the TEXTATOM subtumbler range for `docisa`).
2. It tells you the last I-address below the upper bound — existence of bytes, not their document membership.
3. The granfilade contains text from ALL documents. `findpreviousisagr` cannot tell you which document owns which I-span.
4. This function has no external API exposure. It's a private recursive helper.

In summary: **`findpreviousisagr` cannot substitute for the spanfilade's DOCISPAN index** as an external discovery mechanism. It cannot answer "is this content reachable from any document?" — it only confirms "does the granfilade have an entry at approximately this I-address?"

---

### The Two Independent Discovery Paths

| Path | Mechanism | Requires DOCISPAN? | Direction |
|---|---|---|---|
| POOM orgl walk | `findorgl` → `permute`/`vspanset2ispanset` | No | Document → I-spans |
| Spanfilade DOCISPAN | `finddocscontainingsp` → `retrieverestricted(spanf, DOCISPAN range)` | Yes | I-span → Documents |

The POOM (`insertpm` at `orglinks.c:75-134`) records the V→I mapping inside the document's own orgl — this is the authoritative "what does this document contain" structure. The spanfilade DOCISPAN entries (`insertspanf` at `spanf1.c:15-54`) are the inverse index — the "what documents contain this I-span" structure.

For APPENDed content:
- `docopy` calls **both** `insertpm` (writes to POOM) and `insertspanf(DOCISPAN)` (writes to spanfilade).
- Content is discoverable via both paths.

---

### Final Answer

**The appended content's I-address is fully registered in the spanfilade via DOCISPAN.** The commented-out `insertspanf` in `doappend` [`do1.c:29-31`] was a *redundant direct call* (with the wrong argument type, `textset` instead of `ispanset`) that was correctly removed. The actual registration happens through `appendpm` → `doinsert` → `docopy` → `insertspanf(DOCISPAN)` at `do1.c:62`.

`findpreviousisagr` provides no external discovery path — it is a private granfilade-tree walker used only to find next-allocation addresses [`granf2.c:255-278`], and it operates with no knowledge of document membership.

If hypothetically the DOCISPAN entry *were* missing: the content would still be accessible through the document's POOM orgl (forward direction, knowing the document ISA), but would be invisible to any reverse-index query such as `finddocscontainingsp` [`spanf1.c:151-188`], which relies entirely on the DOCISPAN entries stored in the spanfilade.
