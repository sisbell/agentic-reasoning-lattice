## Question 3 [evidence]

> What does udanax-green's RETRIEVEENDSETS accept as its region argument — content-subspace spans only, or arbitrary V-positions that (via S3★) could resolve to link addresses?

## KB Synthesis

## RETRIEVEENDSETS: Region Argument Semantics

RETRIEVEENDSETS accepts **arbitrary V-positions** at the protocol level, but only text-subspace spans (1.x) produce meaningful results. Here is why, synthesized from the relevant KB entries.

### What the implementation accepts

The backend imposes no subspace guard on input. `acceptablevsa()` unconditionally returns TRUE [PRE-INSERT, Finding 0049], and the V→I conversion path (`specset2sporglset()` → `vspanset2ispanset()` → `permute()`) is type-agnostic [SS-DUAL-ENFILADE, SS-SUBSPACE-CONVENTION]. The operation will accept 2.x V-positions without error.

### What happens with text-subspace input (1.x)

This is the intended path. The call chain from [SS-RETRIEVE-ENDSETS]:

1. Input specset → `specset2sporglset()` → V→I conversion produces **permascroll I-addresses**
2. Those I-addresses are used as the SPANRANGE query key against the spanfilade
3. The spanfilade is keyed by permascroll I-addresses → set of (link ISA, endpoint type) [INT-SPORGL-LINK-INDEX]
4. Matches return valid link endsets, resolved back to V-spans via the querying document's POOM

### What happens with link-subspace input (2.x)

1. V→I conversion produces **link orgl ISAs** (e.g., `1.1.0.1.0.1.0.2.1`)
2. These ISAs are used as SPANRANGE query keys against the spanfilade
3. The spanfilade is keyed by permascroll I-addresses — link orgl ISAs occupy a structurally different address range (`.0.2.` element field) and are never inserted as spanfilade *keys*, only as *values* [SS-SPANF-OPERATIONS, ST-CREATE-LINK]
4. No entries match → empty endsets returned

This is a **semantically empty result, not a crash**. This contrasts with `compare_versions`, which crashes on link-subspace input because `correspond.c` cannot handle empty I-span intersections gracefully [EC-COMPARE-VERSIONS-LINK-CRASH]. RETRIEVEENDSETS routes through `retrievesporglsetinrange()`, which is designed to return empty results on no-match and does not have the same structural assumption about non-empty intersections.

### The precondition the spec must state

By analogy with [INT-LINK-RETRIEVAL]:

> The spec for `find_links` must state a precondition that the search I-addresses are permascroll addresses (from text subspace), not link orgl ISAs.

The same applies to RETRIEVEENDSETS. The formal precondition is `∀ span ∈ input_specset : span.start.mantissa[0] = 1` (text subspace). This is a **caller obligation**, not a backend enforcement — the convention-over-enforcement principle from [INV-SUBSPACE-CONVENTION] applies. The storage layer does not check it; the spec must require it for the results to be semantically meaningful.

### Summary

| Input subspace | V→I result | Spanfilade match | Output |
|---|---|---|---|
| 1.x (text) | permascroll I-addresses | found (if links exist) | valid endset spans |
| 2.x (links) | link orgl ISAs | not found (wrong key type) | empty endsets, no crash |

RETRIEVEENDSETS does not crash on link-subspace input (unlike `compare_versions`), but returns empty endsets that convey no information. The effective precondition for non-empty results is text-subspace input only. [SS-RETRIEVE-ENDSETS, INT-SPORGL-LINK-INDEX, INV-SUBSPACE-CONVENTION, EC-COMPARE-VERSIONS-LINK-CRASH]

---

## Code Exploration

I now have a complete trace. Let me write the full answer.

---

## What RETRIEVEENDSETS Accepts as Its Region Argument

### Executive Summary

RETRIEVEENDSETS accepts **either I-spans or V-specs** at the protocol level, with no subspace guard at parse time. However, only **content-subspace V-positions (1.x, the text/permascroll region)** produce meaningful results. Link-address V-positions (2.x in the document's V-space) are accepted syntactically but yield empty FROM/TO/THREE sets because the spanfilade lookup architecture makes them unmatchable.

---

### Call Chain (Full Trace)

**1. Parse — `fns.c:350-362` → `get1fe.c:192-196`**

```c
void retrieveendsets(typetask *taskptr)
{
    typespecset specset, fromset, toset, threeset;
    bool getretrieveendsets(), doretrieveendsets();

    if (getretrieveendsets(taskptr, &specset)
     && doretrieveendsets(taskptr, specset, &fromset, &toset, &threeset))
        putretrieveendsets(taskptr, fromset, toset, threeset);
    else
        putrequestfailed(taskptr);
}
```

```c
bool getretrieveendsets(typetask *taskptr, typespecset *specsetptr)
{
    return (getspecset(taskptr, specsetptr));    // get1fe.c:192-196
}
```

**`getspecset` at `get2fe.c:147-180`** accepts either:

- **`SPANFLAG`** → parses as `typespan` (`ISPANID`) — a raw permascroll I-span
- **`VSPECFLAG`** → parses as `typevspec` (`VSPECID`) — a document ISA + vspanset

No subspace check is performed. Any V-position is accepted.

---

**2. Do — `do1.c:369-374`**

```c
bool doretrieveendsets(typetask *taskptr, typespecset specset, typespecset *fromsetptr,
                       typespecset *tosetptr, typespecset *threesetptr)
{
    bool retrieveendsetsfromspanf();
    return retrieveendsetsfromspanf(taskptr, specset, fromsetptr, tosetptr, threesetptr);
}
```

Thin wrapper; no filtering.

---

**3. Core logic — `spanf1.c:190-235`**

```c
bool retrieveendsetsfromspanf(...)
{
    typespan fromspace, tospace, threespace;
    typesporglset sporglset;

    fromspace.stream.mantissa[0] = LINKFROMSPAN;   // = 1  (xanadu.h:36)
    fromspace.width.mantissa[0]  = 1;
    tospace.stream.mantissa[0]   = LINKTOSPAN;     // = 2
    threespace.stream.mantissa[0] = LINKTHREESPAN; // = 3

    if (!(specset2sporglset(taskptr, specset, &sporglset, NOBERTREQUIRED)
       && retrievesporglsetinrange(taskptr, sporglset, &fromspace,  &fromsporglset)
       && linksporglset2specset(taskptr, &((typevspec*)specset)->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
       && retrievesporglsetinrange(taskptr, sporglset, &tospace,   &tosporglset)
       && linksporglset2specset(...tosetptr...))){
        return FALSE;
    }
    // optional THREE endset ...
```

The function converts the input specset → sporglset (I-spans + docisa), then asks the **spanfilade** for entries where **SPANRANGE** matches those I-spans and **ORGLRANGE** falls in the LINKFROMSPAN / LINKTOSPAN / LINKTHREESPAN windows.

---

**4. V→I conversion — `sporgl.c:35-65`**

For a VSPECID input, `specset2sporglset` calls `vspanset2sporglset`:

```c
typesporglset *vspanset2sporglset(typetask *taskptr, typeisa *docisa,
    typevspanset vspanset, typesporglset *sporglsetptr, int type)
{
    if (!findorgl(taskptr, granf, docisa, &orgl, type))   // NOBERTREQUIRED: always succeeds
        return NULL;
    for (; vspanset; vspanset = vspanset->next)
        vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
    // pack ispanset into sporglset ...
}
```

`vspanset2ispanset` at `orglinks.c:397-402` → `permute(V, I)` — walks the **document's granfilade** to map V-positions to I-positions.

There is **no subspace filter here**. All V-positions are passed to `permute`.

---

**5. What the spanfilade stores — `spanf1.c:15-54` and `do1.c:195-221`**

When a link is created by `docreatelink`:

```c
tumbler2spanset(taskptr, linkisaptr, &ispanset)   // link ISA → I-span
findnextlinkvsa(taskptr, docisaptr, &linkvsa)      // linkvsa = 2.1 (first link)
docopy(taskptr, docisaptr, &linkvsa, ispanset)     // store link ISA at V-pos 2.1 in POOM
specset2sporglset(taskptr, fromspecset, &fromsporglset, ...)  // FROM endpoint → content I-spans
insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, ...)
```

`insertspanf` stores in the spanfilade:

| Dimension | Value |
|-----------|-------|
| ORGLRANGE | link ISA prefixed with spantype (1=FROM, 2=TO, 3=THREE) |
| SPANRANGE | permascroll I-span of the content endpoint ("here", etc.) |

SPANRANGE stores **content permascroll I-positions** — not link ISA values.

---

**6. What `findnextlinkvsa` produces — `do2.c:151-167`**

```c
tumblerclear(&firstlink);
tumblerincrement(&firstlink, 0, 2, &firstlink);   // mantissa[0] = 2
tumblerincrement(&firstlink, 1, 1, &firstlink);   // mantissa[1] = 1
// → firstlink = tumbler [2,1] = V-position 2.1
```

Confirmed by golden test `insert_text_check_both_link_positions.json`:

```json
{"op": "link_at_2_1_before", "result": ["1.1.0.1.0.1.0.2.1"]}
```

`retrieve_contents(VSpec(doc, [Span(Address(2,1), Offset(0,1))]))` returns the link ISA — the link's V-position in the document's address space is **2.1**.

---

**7. `acceptablevsa` — `do2.c:110-112`**

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

This is the only potential validation gate in the insertion path — and it is a permanent stub that always returns `TRUE`. It is **not even called** in the RETRIEVEENDSETS path (only in `docopy` and `docopyinternal`).

---

### The S3★ Question Directly

When a link V-position (2.x) is passed to RETRIEVEENDSETS:

1. `getspecset` accepts it (no guard)
2. `vspanset2sporglset` calls `findorgl(granf, docisa)` — succeeds if the document is open
3. `vspanset2ispanset` traverses the document granfilade at V-position 2.x → returns the link ISA I-span (the "permascroll address" of the link reference, inserted by `docopy` via `tumbler2spanset`)
4. `retrievesporglsetinrange` searches the spanfilade where **SPANRANGE overlaps the link ISA I-span** AND ORGLRANGE is in the LINKFROMSPAN range

Step 4 fails to find anything useful because the spanfilade's SPANRANGE dimension contains **content permascroll I-spans** (positions of "here", "Destination content", etc.) — not link ISA values. A link ISA like `1.1.0.1.0.1.0.2.1` is assigned by `createorglingranf`, not drawn from the permascroll; it does not appear in the SPANRANGE of any link-endpoint spanfilade entry.

RETRIEVEENDSETS therefore **returns empty FROM/TO/THREE sets** when given 2.x link-subspace V-positions.

---

### Why the `docs/client-api.md` Pattern Is Misleading

The documentation shows:

```python
link_spans = [s for s in vs.spans if s.start.digits[0] == 0]  # filter to 0.x
specs = SpecSet(VSpec(opened, link_spans))
source_endset, target_endset, type_endset = session.retrieve_endsets(specs)
```

But `retrieve_vspanset` returns two spans for a document with links (from `retrievevspansetpm`, `orglinks.c:173-221`): one representing the text extents (first digit 0 in the internal representation) and one for the link extent. The `digits[0] == 0` filter matches the text-extent span, not the link V-positions at 2.x. Even if it did isolate the 2.x link V-positions, the architecture described above shows that RETRIEVEENDSETS cannot retrieve link endpoints from link V-addresses — that is the job of **FOLLOWLINK** (`dofollowlink`, `do1.c:223-232`), which searches the ORGLRANGE dimension of the spanfilade by link ISA directly.

---

### The Correct Semantics

| Operation | Input | What it finds |
|-----------|-------|---------------|
| `RETRIEVEENDSETS` | Content V-span (1.x) | All links whose FROM/TO/THREE endpoint I-spans overlap the content I-span at that V-position |
| `FOLLOWLINK` | Link ISA (tumbler) | The FROM/TO/THREE endpoint specsets of that specific link |

RETRIEVEENDSETS is a **content → link** lookup: given a region of content, find the links attached to it. Passing link-subspace V-positions yields empty results because those positions map to link ISA values in the granfilade, and link ISAs are not stored as SPANRANGE keys in the spanfilade.

The `filter_specset_to_text_subspace` filter (`do1.c:386-426`) that strips V < 1.0 spans is applied **only** in `doshowrelationof2versions` (`do1.c:437-441`), not in RETRIEVEENDSETS. There is no analogous guard in the RETRIEVEENDSETS path. The operation accepts arbitrary V-positions but is semantically meaningful only for content-subspace (1.x) inputs.
