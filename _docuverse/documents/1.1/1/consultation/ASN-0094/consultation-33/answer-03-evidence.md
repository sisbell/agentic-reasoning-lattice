## Question 3 [evidence]

> Is `citation.depends` currently registered in udanax-green's substrate (and if so, with what shape), or does the patch describe a fresh registration at a new K?

## KB Synthesis

Not answerable from the KB.

The KB covers link type registration in the bootstrap document [SS-LINK-ENDPOINT, Finding 0024] — known types are JUMP (`1.0.2.2`), QUOTE (`1.0.2.3`), FOOTNOTE (`1.0.2.6`), and MARGIN (`1.0.2.6.2`). No finding mentions `citation.depends` or any citation-family type, and there is no finding that inventories the complete type registry or describes a "fresh registration" patch mechanism.

---

## Code Exploration

## Answer

`citation.depends` is **not registered anywhere in udanax-green**. The patch describes a fresh registration at a new K.

---

### What "registered in the substrate" would mean here

The backend has no concept called "substrate." It has two atom types, period:

```c
// xanadu.h:145-146
#define TEXTATOM  1
#define LINKATOM  2
```

Every link — regardless of semantic intent — is stored as a `LINKATOM` with three endsets (from, to, three). The `typehint` structure [`xanadu.h:148-153`] carries `supertype`, `subtype`, and `atomtype`, but `atomtype` only encodes `TEXTATOM` or `LINKATOM`. The backend enforces no named link types whatsoever. `docreatelink` always calls `makehint(DOCUMENT, ATOM, LINKATOM, ...)` [`do1.c:207`] regardless of the link's semantic kind.

The closest thing to a "type registry" is a **client-side convention** defined in `febe/client.py`. Link types are stored as spans in a bootstrap document:

```python
# febe/client.py:597-608
# Link types are in document 1's link subspace (0.2)
LINK_TYPES_DOC = Address(1, 1, 0, 1, 0, 1)   # bootstrap doc

# Type numbers (address 1.0.2.X within that doc):
JUMP_TYPE     = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 2),   Offset(0, 1))])  # 2.2
QUOTE_TYPE    = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 3),   Offset(0, 1))])  # 2.3
FOOTNOTE_TYPE = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 6),   Offset(0, 1))])  # 2.6
MARGIN_TYPE   = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 6, 2), Offset(0, 1))]) # 2.6.2
```

The comment at `client.py:599` references `resources/link-registry/link-types.md` and `link-types-relationship.md` — **neither file exists in this repository.**

---

### Exhaustive search result

The strings `citation` and `depends` (as a semantic concept) appear **nowhere** in:

- All backend C source files (`backend/*.c`, `backend/*.h`) — zero hits
- `febe/client.py` — zero hits
- `findings/` — zero hits (only section headers like "## Citations" in some files)
- `knowledge-base/` — zero hits
- `bugs/` — one hit: a comment about crash threshold *depending on* document count (unrelated)
- `docs/` — zero hits

---

### Conclusion

`citation.depends` has no presence in udanax-green's codebase in any form — not as a C type, not as a client constant, not as a registered address in the link type table. The current type table ends at:

| Type address | Name |
|---|---|
| `2.2` | jump |
| `2.3` | quote |
| `2.6` | footnote |
| `2.6.2` | footnote.margin |

Any patch adding `citation.depends` is registering a **completely new entry at a new K** — the slot does not exist yet, and the backend would be entirely agnostic to it (it would treat it as just another `LINKATOM` with a particular three-endset value pointing into the link type bootstrap document).
