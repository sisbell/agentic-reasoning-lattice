## Question 17 [gregory]

> The type namespace lives at `1.0.2.x` — who owns this range? Is it a system-level or node-level allocation that sits outside any user's tumbler prefix, and how is write authority to the type namespace determined?

## KB Synthesis

The KB has partial but incomplete information on this.

## What the KB says

**The type namespace is in the bootstrap document.** [SS-LINK-ENDPOINT / Finding 0024] establishes that link types are VSpec references into a "type registry in the bootstrap document (doc 1)," with known entries at:

| Type | Address |
|------|---------|
| JUMP | `1.0.2.2` |
| QUOTE | `1.0.2.3` |
| FOOTNOTE | `1.0.2.6` |
| MARGIN | `1.0.2.6.2` |

The hierarchical nesting (`1.0.2.6.2` contained in `1.0.2.6`) uses the same tumbler containment predicate as the document address space — making type subtyping a consequence of address prefix-matching, not a separate mechanism [SS-TUMBLER-CONTAINMENT].

**Address structure.** Per the `.0.` field-divider convention [SS-TUMBLER / Finding 0001], `1.0.2.x` parses as node `1`, separator `0`, entity `2`, sub-addressing at `x`. This places the bootstrap document under node `1` at position `2` — distinct from user account space (which follows the `Node.0.User.0.Doc` pattern).

**Write authority in general.** [SS-BERT / Finding 0014] establishes that any document mutation requires WRITEBERT for that document. [PRE-OPEN-DOC] and [INV-WRITE-EXCLUSIVITY] formalize this: at most one connection holds WRITE access at a time. This applies to the bootstrap document the same as any other.

## What the KB cannot answer

The KB does not contain findings about:

- **Who created the bootstrap document** or under which account it was allocated — the KB has no exploration findings targeting system initialization beyond `createenf()` startup [SS-ENFILADE-TREE / Finding 0058]
- **Whether `1.0.2.x` is node-level (system) or user-level allocation** — the address structure suggests it sits under node `1` rather than under a user account prefix, but this is inference from address anatomy, not from a finding
- **Governance of type namespace extension** — no finding documents whether ordinary sessions can acquire WRITEBERT on the bootstrap document, or whether type registration is restricted to a privileged process

The KB is silent on bootstrap document lifecycle. You'd need an additional discovery session targeting `initenffile()`, the bootstrap document creation code, and the BERT permissions on document `1.0.2` to answer the ownership and write-authority questions definitively.

---

## Code Exploration

I now have everything needed for a complete answer.

---

## The `1.0.2.x` Type Namespace: Full Analysis

### What it is

`1.0.2.x` is **not a global tumbler prefix**. It is a set of **local V-addresses within document `1.1.0.1.0.1`** (the bootstrap document — the first document under the default account). The C backend has zero hardcoded references to `1.0.2` anywhere in the source.

The definition lives entirely in `febe/client.py:597-612`:

```python
# Link type addresses - types are in document 1's link subspace (0.2)
# Full address format: 1.1.0.1.0.1.0.2.X where X is the type number
# Local address within doc: version.0.link_subspace.type = 1.0.2.X
LINK_TYPES_DOC = Address(1, 1, 0, 1, 0, 1)  # Bootstrap doc
JUMP_TYPE      = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 2),     Offset(0, 1))])
QUOTE_TYPE     = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 3),     Offset(0, 1))])
FOOTNOTE_TYPE  = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 6),     Offset(0, 1))])
MARGIN_TYPE    = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 6, 2),  Offset(0, 1))])
```

---

### Address decoding

**Text subspace** in a document runs at V-positions `>= 1.0`, established by `do1.c:394-395`:

```c
tumblerclear(&text_subspace_start);
tumblerincrement(&text_subspace_start, 0, 1, &text_subspace_start);  // = 1
```

**Link subspace** starts at V-position `2`, established by `orglinks.c:36-37`:

```c
tumblerclear (&linkspacevstart);
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);  // = 2
```

So V-positions `1 ≤ V < 2` are text subspace; `V ≥ 2` are link subspace. V-address `1.0.2.X` has first digit `1`, so it falls inside the **text subspace** (not link subspace, despite the comment). These addresses sit in a conventional gap: real text starts at `1.0.1` (from `findvsatoappend` → `orglinks.c:42-43`), while these type-identifier addresses sit at `1.0.2.X` sub-positions that are never populated by normal content.

The comment in `client.py:603` cross-references `2.X` positions as "version.0.link_subspace.type = 1.0.2.X" — meaning `1.0.` is a version-level prefix prepended to the raw link-subspace slot `2.X`. This is a naming convention, not a mechanical derivation from the POOM structure.

---

### Who owns this range

Ownership flows from document ownership. The range has no independent owner in the global tumbler tree — it is entirely contained within document `1.1.0.1.0.1`, which is under account `1.1.0.1`:

```c
// be.c:37
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

At startup `be.c:88` copies `defaultaccount` into `task.account`. Document creation uses `makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)` (`do1.c:239`), so the first document gets allocated under `1.1.0.1` → ISA `1.1.0.1.0.1`.

There is no node at `1.0` in the standard addressing hierarchy. The `1.0` prefix in `1.0.2.x` is artificial — it is not the address of any node, account, or document in the global tumbler tree.

---

### System-level or node-level?

**Neither.** This is a **client-level convention**, and purely so:

- No C source file contains `1.0.2` as a constant or address range.
- `init.c` (the backend initialization) sets up request handlers but creates no bootstrap document and no type registry.
- `rcfile.c` reads runtime config but does nothing with type addresses.
- The C backend never enforces or inspects the type address range. Any VSpec is accepted as the third endset of a `createlink` call.

The convention is analogous to how `1.X.0.Y.0.Z` is interpreted as node.account.document in the global space: a useful semantic model layered onto raw tumbler ordering, but the backend only cares about tumblers as ordered identifiers, not the naming convention they encode.

---

### Write authority

Write authority to the `1.0.2.x` range = write authority to document `1.1.0.1.0.1`. The backend's two-step check:

1. **BERT check** — `findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)` in `do1.c:40, 55` requires an active WRITEBERT entry for the document. `bert.c:63-119` uses a hash table keyed on the document's tumbler.

2. **Account ownership** — `isthisusersdocument` (`be.c:171-176`) calls `tumbleraccounteq(tp, &taskptrx->account)`. However, Finding 0050 ("bert-not-enforced-at-backend") shows BERT enforcement is partial.

In practice, because no initialization code bootstraps the type registry document, the `1.0.2.x` addresses contain no content. When a type VSpec like `VSpec(LINK_TYPES_DOC, [Span(1.0.2.2, Offset(0,1))])` is used as a link's third endset, `docreatelink` calls `specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)` (`do1.c:216`). That function converts V-spans to I-spans via POOM lookup — if no content has been inserted at `1.0.2.2`, the result is empty. Then `insertendsetsinspanf` only stores a type entry when `threesporglset` is non-null (`do2.c:122`):

```c
if (threesporglset) {
    insertspanf(taskptr, spanf, linkisaptr, threesporglset, LINKTHREESPAN);
}
```

So type endsets are silently dropped. This is the root cause of the retrieval failure described in Finding 0024.

---

### Why the type-subtype hierarchy works at all

The hierarchical containment of MARGIN under FOOTNOTE (`1.0.2.6.2` under `1.0.2.6`) is structurally valid because tumbler ordering is lexicographic. Any tumbler query against an interval that contains `1.0.2.6` would also contain `1.0.2.6.2` if the width is large enough, enabling "find all footnote-family links" by a range query. This is the intended semantic — tumbler sub-addressing naturally encodes type inheritance. But realizing it requires actual content at the type addresses and a query that explicitly searches a range rather than exact V-span.

---

### Summary

| Claim | Finding |
|-------|---------|
| `1.0.2.x` is a global tumbler prefix | **False** — it's local to doc `1.1.0.1.0.1` |
| Defined in backend C code | **False** — defined only in `febe/client.py:605-608` |
| System-level allocation | **False** — client convention, no backend enforcement |
| Node-level allocation | **False** — no node at `1.0`; doc is under account `1.1.0.1` |
| Write authority via BERT | **True** — `bert.c` governs writes to doc `1.1.0.1.0.1` |
| Types work for link retrieval | **False** — bootstrap doc has no content at `1.0.2.x`, so `specset2sporglset` returns empty and the endset is never stored (`do2.c:122`) |
