## Question 14 [evidence]

> If CREATENEWVERSION is invoked twice in succession on the same source, does each invocation independently derive from the source's current state, or does the second version pick up any structural difference from the first?

## KB Synthesis

Each invocation independently derives from the source's **current state**. The second version sees exactly one structural side-effect of the first: its address allocation.

**Address allocation** [SS-ADDRESS-ALLOC, ST-ADDRESS-ALLOC, Finding 0068]: The algorithm is stateless query-and-increment on the granfilade. First call finds no children under source `S`, allocates `S.1`. Second call finds `S.1` as the highest existing child address, increments to `S.2`. Both sibling addresses fall under the source's namespace.

**Content copying** [ST-VERSION, Finding 0077]: `CREATENEWVERSION` calls `doretrievedocvspanfoo` on the **source document's** current POOM — not on any previously created version. Both invocations read `retrievedocumentpartofvspanpm(source)` to obtain the text vspan, then `docopyinternal` copies those I-addresses into the new version's POOM. If the source is unmodified between calls, `V1` and `V2` receive identical I-address mappings.

**Granfilade effects** [FC-GRANF-ON-VERSION, INV-MONOTONIC]: First VERSION creation adds a document address entry (`S.1`) to the granfilade but does **not** modify the content portion. Critically, unlike CREATELINK, VERSION does not advance the content I-address allocator [Finding 0077] — subsequent text inserts into the source remain contiguous with prior insertions.

**Source isolation** [FC-VERSION-ISOLATION]: The source's POOM is a frame condition for both VERSION calls. Neither version creation modifies the source's V-to-I mapping.

**Concretely:**
```
V1 = CREATENEWVERSION(S)  →  address S.1, ispans(V1) = ispans(S)
V2 = CREATENEWVERSION(S)  →  address S.2, ispans(V2) = ispans(S)
ispans(V1) == ispans(V2)  (assuming no edits to S between calls)
```

The second version differs only in address. Both are independent snapshots of the same source state.

---

## Code Exploration

I have all the evidence needed. Let me compile the complete answer.

---

## CREATENEWVERSION: Two Successive Calls on the Same Source

### Short Answer

**Each invocation independently derives from the source's current (unchanged) state.** The second version does not pick up any structural difference from the first. Both are independent snapshots of the source. They differ only in their assigned tumbler address.

---

### The Call Path

`fns.c:289-300` — FEBE handler for `createnewversion`:

```c
void createnewversion(typetask *taskptr)
{
  typeisa originaldocisa, newdocisa;
  ...
  if (
     getcreatenewversion (taskptr, &originaldocisa)
  && docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa))
       putcreatenewversion (taskptr, &newdocisa);
```

Both the 2nd and 3rd arguments are `&originaldocisa` — both `isaptr` and `wheretoputit` point to the same source address. This matters for ownership branching below.

---

### Inside `docreatenewversion` — `do1.c:260-299`

**Step 1 — Address allocation** (`do1.c:270-278`):

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);  // same-account case
} ...
if (!createorglingranf(taskptr, granf, &hint, newisaptr)) return FALSE;
```

`makehint` records the source's address as the `hintisa`. `createorglingranf` calls `findisatoinsertnonmolecule` (`granf2.c:203-242`) to allocate the next child tumbler under the source.

`findisatoinsertnonmolecule` (`granf2.c:217`):

```c
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

It scans the granfilade for the highest existing child under source, then increments. After the **first** call, `sourceAddr.0.1` exists; the **second** call therefore finds it and produces `sourceAddr.0.2`. The two versions are siblings, not parent-child.

**Critical:** This only affects the new version's *address*, not its content source.

---

**Step 2 — Source vspan read** (`do1.c:281-288`):

```c
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) return FALSE;
vspec.next = NULL;
vspec.itemid = VSPECID;
movetumbler(isaptr, &vspec.docisa);
vspec.vspanset = &vspan;
```

`doretrievedocvspanfoo` (`do1.c:301-309`) → `retrievedocumentpartofvspanpm` (`orglinks.c:155-162`):

```c
movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
```

This reads the source document's V-dimension cumulative displacement and width directly from its orgl node. These are **pure reads** — they do not modify `isaptr`'s orgl at all. `vspec.docisa` is set to `isaptr` (the source), so the copy-source pointer records the source document.

---

**Step 3 — Copy into new version** (`do1.c:292-296`):

```c
addtoopen(newisaptr, user, TRUE, WRITEBERT);
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
logbertmodified(newisaptr, user);
doclose(taskptr, newisaptr, user);
```

`docopyinternal` (`do1.c:66-82`) operates entirely on `newisaptr`:

```c
findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)   // docisaptr = newisaptr
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)       // writes to new doc
&& insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)    // indexes new doc
```

The source document (`isaptr`) is never passed to any write function. The granfilade orgl for the source is opened read-only via `NOBERTREQUIRED` in `doretrievedocvspanfoo`, and the write calls exclusively target `newisaptr`.

---

### What the Second Call Sees

When CREATENEWVERSION is called a second time on the same source:

| Step | What the second call observes |
|------|-------------------------------|
| Address allocation (`granf2.c:217-241`) | `findpreviousisagr` finds the first new version, assigns the *next* child address (`sourceAddr.0.2`). Different tumbler, same logic. |
| Source vspan (`orglinks.c:159-160`) | Reads unchanged `cdsp.dsas[V]` and `cwid.dsas[V]` from the source's orgl — identical values as the first call read. |
| Content copy (`do1.c:293`) | Copies from the same source into the second new version. Identical content to the first new version. |

---

### Conclusion

The two new versions are **independent, content-identical snapshots** of the source. The source document's orgl is not mutated by either call. Each invocation:

1. Allocates the next sequential child tumbler under the source (so they get distinct addresses).
2. Reads the source's V-space displacement/width — which is unchanged between calls.
3. Copies the source's content into the new version.

The second version knows nothing about the first version. It could not pick up structural differences from it even if the first version had subsequently been edited, because the derivation arrow points source → new version, and the source is the invariant reference for both calls. The two versions are siblings (e.g., `sourceAddr.0.1` and `sourceAddr.0.2`) derived from the same parent state.
