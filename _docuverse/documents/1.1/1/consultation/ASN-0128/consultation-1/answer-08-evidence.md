## Question 8 [evidence]

> Does udanax-green reserve conventional tumbler addresses for standard link types (e.g., jump links, quote links), and if so, what are they and where are they defined?

## KB Synthesis

Yes. Udanax-green reserves tumbler addresses in the bootstrap document (doc 1) for a type registry. Link types are stored as VSpec references into this registry, not as enums or flags.

## Type Registry Location

The type registry lives at the subspace `1.0.2.x` within the bootstrap document. From [SS-LINK-ENDPOINT] Finding 0024:

| Type | Registry Address | Structure |
|------|-----------------|-----------|
| JUMP | `1.0.2.2` | `version.0.types.2` |
| QUOTE | `1.0.2.3` | `version.0.types.3` |
| FOOTNOTE | `1.0.2.6` | `version.0.types.6` |
| MARGIN | `1.0.2.6.2` | `version.0.types.6.subtype.2` |

## Key Properties

**Types are content references, not metadata.** A link's `type` field is a VSpec where `VSpec.docid = bootstrap_doc` and `VSpec.spans ⊆ addresses(1.0.2.*)`. This means link types participate in the same address/identity system as all other content [SS-LINK-ENDPOINT Finding 0024].

**The hierarchy is encoded in the tumbler structure.** `MARGIN` (`1.0.2.6.2`) is a child address of `FOOTNOTE` (`1.0.2.6`), encoding a subtype relationship via tumbler containment. This enables type queries like "find all footnote-family links" via address-range matching rather than equality comparison [SS-TUMBLER-CONTAINMENT], [SS-LINK-ENDPOINT Finding 0024].

**Definition location.** The `QUOTE_TYPE` and `MARGIN_TYPE` constants are defined in `febe/client.py` as VSpec constructions referencing the bootstrap document addresses. The type address structure uses the `.0.` field separator convention documented in [SS-TUMBLER Finding 0001]: the field at position `1.0.2` means node `1`, account `0`, document `2` within the bootstrap node.

**Type filter is currently non-functional.** As documented in [EC-TYPE-FILTER-NONFUNCTIONAL], passing a type spec to `find_links` returns empty results even when unfiltered search finds links of those types. The type registry addresses are defined, but the type-based search mechanism does not work correctly in the current implementation.

---

## Code Exploration

I now have a complete picture from the source. Here is my full answer.

---

## Answer: Tumbler Addresses for Link Types in udanax-green

**Short answer: No, udanax-green does not reserve tumbler addresses for named semantic link types such as "jump links" or "quote links."** All links share an identical three-ended structure. The only hardcoded tumbler sub-addresses are the **endpoint positions within each link's own V-space**, which are fixed and the same for every link regardless of intent.

---

### What IS reserved: endpoint positions within a link document

`setlinkvsas` in `do2.c:169–183` hardcodes the three endpoint V-addresses inside every link's own POOM orglink:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   // mantissa[0] = 1
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);   // mantissa[1] = 1  → 1.1
    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);       // mantissa[0] = 2
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);       // mantissa[1] = 1  → 2.1
    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr); // mantissa[0] = 3
        tumblerincrement (threevsaptr, 1, 1, threevsaptr); // mantissa[1] = 1  → 3.1
    }
    return (TRUE);
}
```

| Endpoint | V-address in link's own space | mantissa |
|----------|-------------------------------|----------|
| from     | **1.1**                       | [1, 1, 0, …] |
| to       | **2.1**                       | [2, 1, 0, …] |
| three    | **3.1**                       | [3, 1, 0, …] |

These positions are the same for every link. They are not "link types"—they are structural slots.

The corresponding span-type integer constants are defined in `xanadu.h:36–38`:
```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
```

---

### How the lookup works

`link2sporglset` in `sporgl.c:80–83` retrieves an endpoint by searching the link's V-space in the range `[whichend, whichend+1)`:

```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);   // stream = 1, 2, or 3
tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);       // width = 1
context = retrieverestricted((typecuc*)orgl, &vspan, V, …);
```

For `whichend=1`, the range `[1, 2)` captures the from endset at V=1.1. For `whichend=2`, the range `[2, 3)` captures the to endset at V=2.1. This is why `setlinkvsas` uses `N.1` rather than just `N`: the decimal expansion ensures the endpoint falls inside the interval.

---

### No named link types anywhere in the code

A systematic search turns up nothing resembling "jump link," "quote link," or a client-visible link type field:

- The `getcreatelink` protocol handler (`get1.c:46–61`) accepts only: home document ISA, fromset, toset, threeset. **No type parameter.**
- There is no `JUMPLINK`, `QUOTELINK`, `LINKTYPEJUMP`, or any analogous constant anywhere in `*.c` or `*.h`.
- `TEXTATOM=1` and `LINKATOM=2` (`xanadu.h:145–146`) are atom types used internally by `findisatoinsertmolecule` (`granf2.c:158–181`) to compute where to allocate a link's ISA—they are not semantic link types visible to clients.

---

### Link ISA allocation: where link ISAs land in the address hierarchy

`findisatoinsertmolecule` (`granf2.c:158–181`) allocates link ISAs at depth-2 sub-addresses of the host document's ISA, using `LINKATOM=2` as the offset:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
// For LINKATOM (=2): upperbound = docisa.0.3
...
tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
// For LINKATOM (=2): first link ISA = docisa.0.2.1
```

All links go under `docisa.0.2.N` — a single pool per document, with no sub-classification by link type.

---

### Link-space boundary in host documents

`findnextlinkvsa` (`do2.c:151–167`) sets the minimum first-link V-address in a host document to **2.1**:

```c
tumblerincrement (&firstlink, 0, 2, &firstlink);   // → 2
tumblerincrement (&firstlink, 1, 1, &firstlink);   // → 2.1
```

`findvsatoappend` (`orglinks.c:37`) sets `linkspacevstart = 2` as the V-space boundary: text content lives in `[1.1, 2)`, link references live in `[2.1, …)`. The comment at `orglinks.c:257` confirms: a "link crum" in a document is identified by `mantissa[0]==1 && mantissa[1]!=0` (i.e., a 1.N displacement), distinguishing it from plain text crums.

---

### What's NOT there

There is no mechanism—not in the FEBE protocol, not in the ISA allocation logic, not in the tumbler address space—for distinguishing a "jump link" from a "quote link" or any other named link variety. The semantic meaning of the three ends (from/to/three) is entirely determined by convention at the client layer. The backend treats all links identically.
