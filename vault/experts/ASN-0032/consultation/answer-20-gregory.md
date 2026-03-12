## Question 20 [gregory]

> Internal links (source and target both reference the same document) — what concrete use cases motivated support for same-document links, and does bidirectional follow-link on an internal link have different semantics than on a cross-document link?

## KB Synthesis

## Internal Links in Udanax-Green

**On motivation — what the code reveals**

The KB doesn't record Nelson's stated rationale, but the type registry tells the story. [SS-LINK-ENDPOINT] Finding 0024 shows four registered types:

| Type | Address | Subtype |
|------|---------|---------|
| JUMP | `1.0.2.2` | — |
| QUOTE | `1.0.2.3` | — |
| FOOTNOTE | `1.0.2.6` | — |
| MARGIN | `1.0.2.6.2` | under FOOTNOTE |

FOOTNOTE, MARGIN, and JUMP are all structurally suited to same-document linking. A footnote reference mark and its footnote text both live in the same document — separating them cross-document would be artificial. The MARGIN subtype (a kind of annotation attached to text in the same document) makes the intent explicit. JUMP could serve within-document navigation (e.g., a table of contents entry to its section heading).

The more fundamental reason is that link endpoints are content identities [SS-LINK-ENDPOINT] Finding 0004, and content identity is indifferent to document boundaries. The constraint `doc(source) != doc(target)` would have had to be added explicitly; it was never imposed.

**On bidirectional follow-link semantics**

The KB is unambiguous: internal and cross-document links are identical in every observable respect [ST-LINK-CREATE] Finding 0020.

```
follow_link(internal_link, SOURCE) → specset referencing this doc
follow_link(internal_link, TARGET) → specset referencing this doc
```

Both succeed. The endset is stored as I-addresses in the link orgl [SS-FOLLOWLINK] Finding 0048. FOLLOWLINK extracts those I-addresses, then resolves them through the `homedoc` parameter's POOM. For an internal link, both endpoints resolve through the same POOM — but the POOM lookup (`span2spanset` → `retrieverestricted`) treats each endset independently with no special-case logic for "same document."

One subtle point from [SS-FOLLOWLINK] Finding 0048: FOLLOWLINK takes a `homedoc` parameter that determines which document's POOM is used for I→V resolution. For a cross-document link, you might call `follow_link(L, TARGET, doc_B)` to get the target expressed in doc_B's V-space. For an internal link, you'd pass the same document for both endpoints. If you passed a *different* document (one that had transcluded the linked content), you'd get the endpoints expressed in that document's V-space instead — this works identically for internal vs. cross-document links, since it's purely content-identity-based [INV-ITOV-FILTERING].

The only thing the KB cannot answer here is whether link discovery (`find_links`) on a document might return an internal link *twice* — once from matching the source content and once from matching the target content within the same V-span. The multi-span duplication edge case [EC-MULTISPAN-LINK-DUPLICATION] was observed with multi-span creation but wasn't specifically tested for same-document source/target overlap. That's a gap in the findings.

---

## Code Exploration

---

## Answer: Internal Links — Use Cases and Bidirectional Follow-Link Semantics

### Why Same-Document Links Are Supported

`docreatelink` (do1.c:195-221) imposes **no check** that source and target belong to different documents:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
                  typespecset fromspecset, typespecset tospecset,
                  typespecset threespecset, typeisa *linkisaptr)
{
    ...
    specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
    specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
    ...
}
```

Each endpoint is independently converted to a sporgl via `specset2sporglset` (sporgl.c:14-33), which resolves the VSpec's `docisa` field for each independently. If both VSpecs carry the same `docisa`, the resulting sporgls simply share `sporgladdress`. There is no "same-document prohibition" anywhere in the call chain — not in `docreatelink`, not in `specset2sporglset`, not in `insertendsetsinorgl` or `insertendsetsinspanf`.

This is by design. The uniform storage model (discussed in Finding 0009, 0011) treats all link endpoints as sporgl sets: the backend doesn't need to know whether the endpoints are in the same document or not. The link's own POOM stores source endset at V=1.1 and target endset at V=2.1 (set by `setlinkvsas`, do2.c:169-183), and those V-positions in the link's internal space are orthogonal to the question of whether the endpoint documents match.

---

### Concrete Use Cases

The four link types defined in the client API (`JUMP_TYPE`, `FOOTNOTE_TYPE`, `MARGIN_TYPE`, `QUOTE_TYPE`) all have natural same-document instantiations:

| Use Case | Canonical Link Type | Concrete Example |
|----------|--------------------|-|
| **Intra-document cross-reference** | JUMP | "See §3" in body → §3 heading, same doc |
| **Footnote** | FOOTNOTE | Footnote marker → footnote text at page bottom, same doc |
| **Margin annotation** | MARGIN | Main paragraph → margin gloss, same doc |
| **Glossary/Index** | JUMP | "glossary" (body) → "Glossary:" definition section, same doc |
| **Self-transcluded content** | JUMP | Original span → vcopy of same content inserted later in same doc |

The golden test `self_referential_link.json` is the glossary pattern: source="glossary", target="Glossary" both in document `1.1.0.1.0.1`. The link is created at `1.1.0.1.0.1.0.2.1` (first link in that document's link subspace, V=0.2.1) and both `follow_link(source)` and `follow_link(target)` succeed.

The design point is architectural, not incidental. Nelson's original Xanadu concept explicitly included footnotes and glossary links — operations that inherently live within a single document. The `FOOTNOTE_TYPE` constant exists in the client API precisely because same-document annotation links are a first-class intended use case.

---

### Does Bidirectional Follow-Link Have Different Semantics for Internal Links?

**No. The code path is identical.** Here is the full trace:

#### `dofollowlink` (do1.c:223-232)

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr,
                  typespecset *specsetptr, INT whichend)
{
    typesporglset sporglset;
    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr,
                              &((typesporgl *)sporglset)->sporgladdress,
                              sporglset, specsetptr, NOBERTREQUIRED));
}
```

#### Step 1: `link2sporglset` (sporgl.c:67-95)

Opens the link's own orgl and searches its V-space at the slot for `whichend`:

```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);  // slot 1/2/3
tumblerincrement (&zero, 0, 1,        &vspan.width);   // width covers that slot
context = retrieverestricted((typecuc*)orgl, &vspan, V, NULL, I, NULL);
```

`setlinkvsas` (do2.c:169-183) placed source at V≈1.1, target at V≈2.1, type at V≈3.1 in the link's own POOM. This is internal to the link orgl and has nothing to do with what document the endpoints belong to.

`contextintosporgl` (sporgl.c:205-220) extracts the stored 2D crum info:

```c
sporglptr->sporgladdress = context->context2dinfo.homedoc;
sporglptr->sporglorigin  = context->totaloffset.dsas[I];
sporglptr->sporglwidth   = context->contextwid.dsas[I];
```

`homedoc` was stored there at link-creation time by `unpacksporgl` (sporgl.c:183-187), which copied it from `sporglset->sporgladdress` — the document that owned that endpoint at creation time.

#### Step 2: `linksporglset2specset` → `linksporglset2vspec` (sporgl.c:97-137)

```c
int linksporglset2vspec(typetask *taskptr, typeisa *homedoc, ...)
{
    specptr->docisa = *homedoc;   // note the kluge: homedoc, not sporglset->sporgladdress
    sporglset2vspanset(taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
}
```

`sporglset2vspanset` calls `ispan2vspanset` → `permute` (orglinks.c:389-454) to convert the stored I-addresses back to current V-positions in `homedoc`'s orgl. Returns a VSpec with `docisa=homedoc` and the current V-spans for that content.

#### The only behavioral difference

For a **cross-document link** (A → B):
- `follow_link(LINK_SOURCE)` → sporgladdress stored = docA → returns VSpec{docA, source-spans}
- `follow_link(LINK_TARGET)` → sporgladdress stored = docB → returns VSpec{docB, target-spans}

For an **internal link** (A → A):
- `follow_link(LINK_SOURCE)` → sporgladdress stored = docA → returns VSpec{docA, source-spans}
- `follow_link(LINK_TARGET)` → sporgladdress stored = docA → returns VSpec{docA, target-spans}

Both endsets return VSpecs with the same `docid`, pointing to different V-spans within that document. Confirmed by `self_referential_link.json`:

```json
{ "op": "follow_link", "end": "target", "result": ["Glossary"] }
{ "op": "follow_link", "end": "source", "result": ["glossary"] }
```

The code path is identical. The only practical consequence for the caller: with a cross-document link you must open a different document handle to dereference the target content; with an internal link the same already-open handle serves both.

---

### The `homedoc` Kluge (sporgl.c:134)

One subtle asymmetry is worth noting. In `linksporglset2vspec`:

```c
movetumbler (homedoc/*&sporglset->sporgladdress*/, &specptr->docisa);
```

The comment reveals the original code used each sporgl's individual `sporgladdress`. It was later changed to use a single `homedoc` — the first sporgl's address, passed from `dofollowlink`. For all real-world endpoints (single-document, whether internal or cross-document), this makes no difference: all sporgls for one endset share the same `sporgladdress`. The kluge would only matter if a single link endpoint spanned content in multiple documents simultaneously, which the architecture does not prevent but which no test exercises.

For internal links specifically, this kluge is completely benign: both the `homedoc` argument and every sporgl's `sporgladdress` are the same document ISA.

---

### Summary Table

| Property | Cross-document link | Internal link |
|----------|---------------------|---------------|
| Restriction in `docreatelink` | None | None (same path) |
| Source sporgl `sporgladdress` | docA | docA |
| Target sporgl `sporgladdress` | docB | docA |
| `follow_link(LINK_SOURCE)` | VSpec{docA, src-spans} | VSpec{docA, src-spans} |
| `follow_link(LINK_TARGET)` | VSpec{docB, tgt-spans} | VSpec{docA, tgt-spans} |
| Code path difference | None | None |
| Caller consequence | Open two docs | One open handle suffices |

Same-document links are supported because the architecture is uniform by design — `docreatelink` has no prohibition, `specset2sporglset` resolves each endpoint independently, and all four link types have natural intra-document use cases (footnote, glossary, margin note, cross-reference). `follow_link` on an internal link executes the same code as on a cross-document link; the only observable difference is that both returned VSpecs name the same document ISA.
