## Question 16 [evidence]

> Does the granfilade retain enough metadata to reconstruct the original V-position context of a now-deleted I-span, or is V-position information only preserved while a POOM entry exists?

## KB Synthesis

**V-position information is preserved only while a POOM entry exists. The granfilade stores no V-position metadata.**

The state model makes the separation explicit [SS-POOM-MUTABILITY]:

- **granfilade**: `I-addr → byte` — content bytes, append-only, no V-position data
- **spanfilade (DOCISPAN)**: `I-addr → {doc-ISA}` — which document contained the I-address, no V-position
- **POOM**: `V-addr → I-addr` — the sole repository of V-position context, and the only mutable layer

When DELETE removes a POOM entry, three things happen [ST-DELETE / Finding 0064]:
1. The V-to-I mapping is pruned from the POOM (`disown` + `subtreefree`)
2. The I-address and its content bytes persist in the granfilade unchanged
3. The DOCISPAN entry in the spanfilade persists — it records only that document D *once* contained the I-address, not *where*

The granfilade literally has no field to store a V-position. Its bottom crums hold content bytes; its structure encodes an I-address tree. Neither encodes "this content was at V-position 1.7" [SS-GRAN-BOTTOM-SINGLETON], [SS-UNIFIED-STORAGE].

The DOCISPAN superset property [EC-STALE-SPANF-REFERENCE] makes this concrete: after deletion, `FINDDOCSCONTAINING(α)` still returns the document, but `I-to-V(α, D)` returns empty — precisely because the V-position record (POOM entry) is gone while the I-space record (granfilade + DOCISPAN) survives.

**Consequence**: The only mechanisms that preserve V-position context past a DELETE are (a) another document's POOM that maps the same I-address via transclusion [FC-DELETE-CROSS-DOC], or (b) a version created before the deletion [ST-VERSION-CREATE / Finding 0072]. Without one of those, V-position context is permanently unrecoverable [INV-DELETE-NOT-INVERSE].

---

## Code Exploration

The write is pending your approval. Here is the complete answer regardless:

---

## Does the Granfilade Retain V-Position Metadata for Deleted I-Spans?

**No. V-position information exists exclusively in the POOM and is destroyed when a V-span is deleted. The granfilade has no V dimension — architecturally it cannot store V-position context.**

---

### The Structural Argument

#### Granfilade Is 1D

From `wisp.h:22-23`:
```c
#define DSPSIZEGR 1
#define WIDSIZEGR 1
```

A granfilade crum's `typewid cwid` has only `dsas[WIDTH]` — a single I-dimension component. Compare POOM:
```c
#define DSPSIZEPM 2
#define WIDSIZEPM 2
```

POOM crums store both `dsas[I]` (index 0) and `dsas[V]` (index 1) [`wisp.h:19-20`].

The granfilade's bottom crum type is `typegranbottomcruminfo` [`wisp.h:101-104`]:
```c
typedef struct structgranbottomcruminfo {
    typegranstuff granstuff;  // GRANTEXT: text string + length
                               // GRANORGL: orgl pointer + disk ptr
    INT infotype;
} typegranbottomcruminfo;
```

Neither `typegrantext` (just `textstring` + `textlength`) nor `typegranorgl` (just `orglptr` + `diskorglptr` + `orglincore`) contains any V-position field. The granfilade is structurally incapable of recording where in V-space a given I-span lives.

#### POOM Is the Exclusive V↔I Repository

The V↔I mapping is encoded purely in the POOM crum's structural position fields — `cdsp.dsas[V]`/`cdsp.dsas[I]` (displacement) and `cwid.dsas[V]`/`cwid.dsas[I]` (width). These are walked cumulatively during tree traversal via `prologuend` to reconstruct absolute V and I positions. The payload `type2dbottomcruminfo` contains only a `tumbler homedoc` — the owning document ISA. [`wisp.h:107-109`]

No other structure carries V-position data.

---

### The Deletion Path: What Gets Freed

```
dodeletevspan [do1.c:158-167]
  → findorgl(granf, docisaptr, &docorgl, WRITEBERT)
  → deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
       [orglinks.c:59]
     → deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V)
          [edit.c:31-76]
```

`dodeletevspan` [do1.c:158-167] calls exactly two functions: `findorgl` and `deletevspanpm`. There is no call to any granfilade or spanfilade modification function.

`deletend` [edit.c:31-76] operates on the POOM in dimension V. For each POOM crum inside the deleted V-range, `deletecutsectionnd` returns case 1:

```c
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);   // edit.c:59-60
    break;
```

`subtreefree` physically deallocates the crum and its entire subtree. The `cwid.dsas[I]`, `cwid.dsas[V]`, `cdsp.dsas[I]`, `cdsp.dsas[V]` — the encoded V↔I mapping — are gone.

For POOM crums that survive but fall after the deleted range, case 2 applies:

```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;   // edit.c:63
```

Surviving crums have V-displacements shifted downward. The POOM reflects only post-deletion V-positions — there is no record of what the pre-deletion V-positions were.

---

### What Each Structure Retains

| Structure | What survives | V-position retained? |
|-----------|--------------|---------------------|
| Granfilade `GRANTEXT` crums | Text bytes at their I-addresses | **No** — 1D, no V field ever existed |
| Granfilade `GRANORGL` entries | POOM root pointer (current state) | Reflects post-deletion state only |
| POOM crums in deleted V-range | **Physically freed** by `subtreefree` | **No — destroyed** |
| POOM crums after deleted range | V-displacements adjusted downward | No — show post-deletion V-positions |
| Spanfilade DOCISPAN entries | Unmodified — persist permanently | No — store document ISA, not V-position |

The spanfilade is worth noting: `insertspanf(..., DOCISPAN)` is called during `docopy` [do1.c:62] but never removed by `dodeletevspan`. This is why `find_documents` still returns deleted content (Finding 0023). But DOCISPAN entries record only *I-address → document ownership*, not V-positions. The spanfilade's bottom crum also uses `type2dbottomcruminfo` with a single `homedoc` tumbler — no V-position.

---

### The Asymmetry This Creates

After deletion, three things are true simultaneously:

1. **The text bytes survive** — GRANTEXT crums at those I-addresses remain in the granfilade. The content is retrievable *if you already know the I-address*.
2. **Document ownership survives** — DOCISPAN entries in the spanfilade are never removed. `find_documents` still associates those I-spans with the document.
3. **The V↔I mapping is gone** — The POOM crums that encoded "I-span X appeared at V-position Y in document D" have been `subtreefree`d. That knowledge is irrecoverable.

The permanence guarantee in Xanadu applies to content *identity* (I-addresses) and content *ownership* (DOCISPAN), not to V-position *context*. Once a V-span is deleted, the original V-position at which that content appeared in the document is lost. No post-hoc traversal of the granfilade, spanfilade, or surviving POOM can reconstruct it.

**V-position information is only preserved while a POOM entry exists.**
