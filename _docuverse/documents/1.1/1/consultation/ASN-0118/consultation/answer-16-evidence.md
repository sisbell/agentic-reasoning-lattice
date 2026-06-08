## Question 16 [evidence]

> Does COPY read only the source document's POOM and write exclusively to the target's fullcrumptr, leaving the source POOM and every other transcluding document's POOM unchanged?

## KB Synthesis

Yes, with one important qualification on the write side.

**Reads:** COPY converts source V-specs to I-spans by reading the source document's POOM through `specset2ispanset` → `permute` → `retrieverestricted`. This is a read-only traversal — `retrieverestricted` returns contexts without modifying any tree node [SS-VSPAN-TO-SPORGL], [ST-VCOPY].

**Writes to target POOM:** `docopy` calls `insertpm` on the target document's orgl, which modifies only that document's enfilade tree via `insertnd` → `makegappm` (shifting existing entries) and `isanextensionnd`/new-crum creation [ST-VCOPY, PRE-COPY]. No other document's POOM is touched.

**Source POOM unchanged:** The source document's POOM is strictly read during V-to-I conversion. Nothing in the `docopy` → `insertpm` path writes back to the source [FC-DELETE-CROSS-DOC, INV-IADDR-IMMUTABILITY].

**Other transcluding documents unchanged:** Since each document has its own independent POOM tree [SS-DUAL-ENFILADE], and `insertpm` receives a specific target orgl pointer, no other document's POOM can be affected.

**The qualification:** COPY also writes to the **spanfilade** — specifically DOCISPAN entries via `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)`. So the write side is: target POOM plus spanfilade, not target POOM alone [SS-DOCISPAN, FC-CONTENT-SPANF-ISOLATION, ST-COPY].

---

## Code Exploration

I now have all the data needed to answer comprehensively.

---

## Does COPY Read Only the Source POOM and Write Exclusively to the Target's fullcrumptr?

**Short answer:** No — not exclusively. COPY reads the source POOM and writes to the target's POOM (`fullcrumptr`), but it also writes to the global spanfilade (`spanf`). The source POOM and all other documents' POOMs are left untouched.

---

### Call Chain

```
fns.c:copy()
  → do1.c:docopy()
      1. specset2ispanset()     — reads SOURCE POOM
      2. findorgl(…, WRITEBERT) — acquires TARGET POOM for writing
      3. acceptablevsa()        — always TRUE, no-op [do2.c:111-113]
      4. asserttreeisok()       — read-only sanity check on TARGET
      5. insertpm()             — writes to TARGET POOM (fullcrumptr)
      6. insertspanf()          — writes to GLOBAL spanfilade (spanf)
      7. asserttreeisok()       — read-only post-check on TARGET
```

---

### Step 1 — Reading the Source POOM

`specset2ispanset` at `do2.c:14-46` iterates the input specset. When it encounters a `VSPECID` item:

```c
// do2.c:34-38
if (!(
  findorgl(taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
  && (ispansetptr = vspanset2ispanset(taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))))
    return FALSE;
```

- `specset->docisa` is the **source** document's ISA.
- `type` = `NOBERTREQUIRED` (no write lock).
- `vspanset2ispanset` calls `permute(…, V, ispansetptr, I)` at `orglinks.c:397-402`, which traverses the source document's POOM via `retrieverestricted` to convert V-coordinates (virtual space addresses) into I-coordinates (permascroll addresses).
- **This is a read-only traversal of the source POOM. The source POOM is not written.**

---

### Step 2 — Acquiring the Target POOM for Writing

```c
// do1.c:55
findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
```

- `docisaptr` is the **target** document's ISA.
- `WRITEBERT` acquires write access via `bert.c` access control.
- `docorgl` is the returned root pointer for the target's POOM — this is the `fullcrumptr` that `insertnd` later operates on.

---

### Step 5 — Writing to the Target POOM via insertpm

```c
// orglinks.c:99-131
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, tumbler *vsaptr, typesporglset sporglset)
{
    logbertmodified(orglisa, user);    // marks TARGET as modified
    for (; sporglset; sporglset = ...) {
        unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
        movetumbler(&lstream, &crumorigin.dsas[I]);
        movetumbler(vsaptr,   &crumorigin.dsas[V]);
        ...
        insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // ← writes TARGET POOM
        tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);
    }
}
```

`insertnd` receives `(typecuc*)orgl` — the target's POOM root — as its `fullcrumptr` parameter (`insertnd.c:15`). Only this POOM is written here. Each sporgl entry from the source's ispanset becomes a new 2D crum mapping (I-address, V-address) inserted into the target's enfilade.

---

### Step 6 — Also Writing to the Global Spanfilade

```c
// do1.c:62
insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

```c
// spanf1.c:15-53
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr, typesporglset sporglset, INT spantype)
{
    prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // prefix = DOCISPAN + target ISA
    ...
    for (; sporglset; ...) {
        movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);
        movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);
        insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);  // ← writes spanf
    }
}
```

`spanfptr` = the global `spanf` (not the target document's POOM). This writes entries that record: **permascroll I-address → (DOCISPAN, target document ISA)**. This is the global reverse index enabling `FINDDOCSCONTAINING` queries. It is a distinct structure from the target document's `fullcrumptr`.

---

### What Happens to Other Documents' POOMs?

Only the target document's orgl is opened with `WRITEBERT` at `do1.c:55`. No other document's `findorgl` is called for writing. The source is opened `NOBERTREQUIRED` (read-only) at `do2.c:35`. Every other transcluding document's POOM is untouched.

---

### Summary Table

| Structure | Access | Written? |
|---|---|---|
| Source document's POOM | Read (`NOBERTREQUIRED`, via `specset2ispanset`) | **No** |
| Target document's POOM (`fullcrumptr`) | Write (`WRITEBERT`, via `insertpm → insertnd`) | **Yes** |
| Global spanfilade (`spanf`) | Write (via `insertspanf → insertnd`) | **Yes** |
| Other transcluding documents' POOMs | Not accessed | **No** |

---

### Verdict

COPY reads the source POOM (V→I translation only) and writes to the target's `fullcrumptr` — but it does **not** write exclusively there. It also writes to the global spanfilade `spanf` to update the reverse I→document index. The source POOM and every other document's POOM are left completely unchanged.
