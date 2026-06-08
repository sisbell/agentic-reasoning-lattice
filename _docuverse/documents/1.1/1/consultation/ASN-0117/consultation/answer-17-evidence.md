## Question 17 [evidence]

> When DELETE removes a span from document A, does a separate document B that transcludes those same I-addresses retain its own POOM entries and content completely unchanged, per the F0 cross-document frame axiom?

## KB Synthesis

Yes, completely. [FC-DELETE-CROSS-DOC] states this explicitly: DELETE operates on a single document's POOM tree only. `deletend` is called on the target document's orgl; other documents' trees are separate data structures and are not touched.

The concrete evidence from [ST-DELETE / Finding 0064]:

```
D has "ABCD", T transcluded "BC" from D (sharing I(5.2), I(5.3))

After DELETE "BC" from D:
  POOM(D): V(1.1)→I(5.1)  V(1.2)→I(5.4)   -- "BC" mapping gone
  POOM(T): V(2.1)→I(5.2)  V(2.2)→I(5.3)   -- UNCHANGED
  Granfilade: I(5.2)="B"  I(5.3)="C"       -- content bytes persist
```

Three independent properties guarantee this:

1. **POOM isolation** [SS-POOM-MUTABILITY] — each document has its own POOM tree; DELETE mutates only the target document's tree in-place.

2. **Granfilade immutability** [INV-IADDR-IMMUTABILITY] — the granfilade is append-only. DELETE never calls any granfilade removal function; it only frees POOM bottom crums. The I-addresses and their content bytes are permanent.

3. **Spanfilade unchanged** [INV-SPANF-WRITE-ONLY] — DELETE has no call to any spanf function ([ST-DELETE / Finding 0057]). Document B's DOCISPAN entries remain intact.

The only consequence is that B's spanfilade entries become "stale" references — they still assert B contains those I-addresses even after the bytes are unreachable from A. This is the [EC-STALE-SPANF-REFERENCE] edge case: `actual_docs(i) ⊆ find_documents(i)`, a superset relationship. B can still retrieve the transcluded content normally via its own POOM.

---

## Code Exploration

All citations verified. Here is my full answer.

---

## F0 Cross-Document Frame Axiom: DELETE Isolation Analysis

**Verdict: Yes.** When DELETE removes a span from document A, document B that transcluded the same I-addresses retains its POOM entries and content completely unchanged. The evidence is in the call chain, data structure ownership, and the total absence of any cross-document write path.

---

### The Complete DELETE Call Chain

**Entry point — `fns.c:333`**:
```c
void deletevspan(typetask *taskptr)
{
    (void) getdeletevspan (taskptr, &docisa, &vspan);
    putdeletevspan (taskptr);
    if (!dodeletevspan (taskptr, &docisa, &vspan))
```

**`do1.c:158`** — `dodeletevspan` performs exactly two operations:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

1. `findorgl` — resolves the document ISA to its specific ORGL node in granf
2. `deletevspanpm` — modifies that ORGL node's enfilade

**`orglinks.c:145`** — `deletevspanpm` is the entire write scope:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

Both `deletend` and `logbertmodified` receive only document A's `docorgl` and `docisaptr`. There is no parameter, global pointer, or loop that touches any other document.

---

### How Document Identity Is Scoped

**`bert.c:13`** — Each open document has a `bertentry` keyed by `documentid` (a tumbler):
```c
typedef struct {
    int connection;
    tumbler documentid;
    char created, modified;
    int type;
    int count;
} bertentry;
static conscell *berttable[NUMBEROFBERTTABLE];
```

**`granf1.c:17`** — `findorgl` enforces the scope gate:
```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr,
              typeorgl *orglptr, int type)
{
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        /* error — not open */
        return FALSE;
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

`checkforopen` matches on `tumblereq(tp, &bert->documentid)` — `bert.c:65`. It only returns a positive result for the exact document ISA passed in. `fetchorglgr` then retrieves only that document's ORGL subtree.

**`bert.c:97`** — `logbertmodified` is equally narrow: it walks `berttable` and flips `modified = TRUE` only on the entry whose `documentid` matches `tp` (document A):
```c
int logbertmodified(tumbler *tp, int connection)
{
    for (p = berttable[hashoftumbler(tp)]; p && p->stuff; p = p->next) {
        bert = (bertentry *) p->stuff;
        if (bert->connection == connection && tumblereq(tp, &bert->documentid)) {
            bert->modified = TRUE;
            return(0);
        }
    }
}
```

Document B's `bertentry` never appears in this loop unless B's tumbler hashes to the same bucket *and* `tumblereq` matches — which requires identical document ISAs. Since A ≠ B, B's entry is never touched.

---

### Where the Structural Modification Actually Happens

**`edit.c:31`** — `deletend` receives the root crum of document A's ORGL (`fullcrumptr = (typecuc*)docorgl`) and operates entirely within that subtree:
```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    prologuend((typecorecrum*)fullcrumptr, &offset, &grasp, &reach);
    movetumbler(origin, &knives.blades[0]);
    tumbleradd(origin, width, &knives.blades[1]);
    ...
    makecutsnd(fullcrumptr, &knives);
    newfindintersectionnd(fullcrumptr, &knives, &father, &foffset);
    for (ptr = (typecuc *) findleftson(father); ptr; ptr = next) {
        ...
        switch (deletecutsectionnd((typecorecrum*)ptr, ...)) {
          case 1: disown((typecorecrum*)ptr); subtreefree(...); break;
          case 2: tumblersub(&ptr->cdsp.dsas[index], width, ...); break;
        }
    }
    setwispupwards(father, 1);
    recombine(father);
}
```

`fullcrumptr` is document A's ORGL root — the tree walk (`findleftson`, `findrightbro`) is bounded to its children. `disown`/`subtreefree` frees crums within that subtree. Nothing here references the granf globally by ISA; it operates on the node pointer already in hand. Document B's ORGL is a different node, unreachable from this pointer.

---

### V-Address vs I-Address Separation

**`orglinks.c:397`** — Conversion between V-spans and I-spans is per-ORGL:
```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, ...)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

Each document's ORGL encodes its own private V↔I permutation matrix. Document A's V-addresses map to document A's I-addresses (A's content allocation range in the spanfilade). Document B has a separate ORGL with its own V↔I mapping — its I-addresses are in a different tumbler range entirely.

When document B transcluded content from A, that transclusion was recorded in the spanfilade indexed by **A's I-addresses** with B's V-address range. The `deletend` on A's ORGL removes crum nodes that represent the V→I mapping for A's V-space. It does not modify the spanfilade entries that record B's transclusion relationship, and it does not touch B's ORGL.

---

### Summary

| Claim | Evidence |
|---|---|
| DELETE resolves exactly one ORGL via ISA | `do1.c:164` — `findorgl(granf, docisaptr, &docorgl, WRITEBERT)` |
| `deletend` is scoped to that ORGL's subtree | `orglinks.c:149`, `edit.c:31` — `fullcrumptr = (typecuc*)docorgl` |
| Bert modification is ISA-matched, single document | `bert.c:104` — `tumblereq(tp, &bert->documentid)` |
| V↔I permutation is per-ORGL, not global | `orglinks.c:397-401` — `permute(orgl, ...)` |
| No code path writes to a second document's ORGL | Entire `do1.c`, `orglinks.c`, `edit.c` — no secondary document traversal |

The F0 axiom holds by construction in this codebase. Document isolation is not enforced by a single guard — it is an emergent property of the design: every write-path function receives an already-resolved ORGL pointer, and the only way to resolve an ORGL is through `findorgl` keyed by a single document ISA. There is simply no mechanism by which operating on document A's ORGL could reach or modify document B's ORGL or its POOM entries.
