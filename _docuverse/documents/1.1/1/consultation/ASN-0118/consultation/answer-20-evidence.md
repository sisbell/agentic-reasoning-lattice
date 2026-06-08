## Question 20 [evidence]

> Does COPY require the target open with WRITEBERT and the source open with at least READBERT, and does the source's read-only access guarantee no mutation of its content identity during the copy?

## KB Synthesis

**WRITEBERT on the target:** Yes. `docopy` calls `findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)` on the target document before inserting V→I mappings via `insertpm` and creating DOCISPAN entries via `insertspanf` [PRE-INSERT, Finding 0036]. However, per [PRE-INSERT] Finding 0050, this check fires *after* the success response is sent — violating it causes a silent no-op, not a rejected operation. WRITEBERT is a cooperative protocol obligation, not a hard gate.

**READBERT on the source:** The KB confirms `specset2ispanset` calls `findorgl` for each source document (which checks `checkforopen`), meaning the source must be in the session's open list [PRE-RETRIEVE-CONTENTS, Finding 0027]. The KB does not explicitly state which BERT access level is checked for the source during COPY — only that `findorgl` is invoked and fails silently if the document is not open.

**Source content identity during copy:** The source's content identity is structurally guaranteed not to mutate during COPY, regardless of access level. Three independent invariants establish this:

1. The granfilade is append-only — no operation modifies or frees I-addresses [INV-IADDR-IMMUTABILITY, Finding 0064; FC-GRANF-ON-DELETE, Finding 0061].
2. COPY shares existing I-addresses; it calls `insertpm` on the *target's* POOM only, leaving the source POOM untouched [ST-VCOPY, Finding 0002; FC-DELETE-CROSS-DOC].
3. All document POOM mutations are strictly local to the target document [FC-INSERT-IADDR, Finding 0030].

So READBERT on the source provides coordination semantics (preventing concurrent WRITE access from another session while you read) but the immutability guarantee comes from the architecture, not the access control level.

---

## Code Exploration

I now have complete source verification. Here is the full answer.

---

## COPY: Permission Requirements and Source Mutation Guarantees

### Q1: Does COPY require WRITEBERT on target and READBERT on source?

**Target: Yes, WRITEBERT required.** **Source: No — NOBERTREQUIRED, not READBERT.**

The `docopy` function at `do1.c:45–65` makes this explicit:

```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)  /* do1.c:54 */
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)       /* do1.c:55 */
&& acceptablevsa (vsaptr, docorgl)
&& asserttreeisok(docorgl)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)        /* do1.c:60 */
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)    /* do1.c:62 */
```

- **Line 55** calls `findorgl(..., WRITEBERT)` on the target (`docisaptr`). This enforces that the target document is open for write before any modification proceeds.
- **Line 54** calls `specset2ispanset(..., NOBERTREQUIRED)` for the source. This type constant propagates directly into `specset2ispanset` at `do2.c:35`:

```c
findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)  /* do2.c:35 */
```

That `type` is `NOBERTREQUIRED`. At `bert.c:59–61`, the check immediately short-circuits:

```c
if (type == NOBERTREQUIRED) {
    return 1;    /* bert.c:59-61 — Random > 0, no check performed */
}
```

**No BERT entry is created for the source. No read lock is acquired.** The source does not need to be open at all.

---

### Q2: Does the source's "read-only" access guarantee no mutation of its content identity during the copy?

**No — and more precisely, there is no read-only BERT access on the source at all.** Two distinct claims must be separated:

**Claim A: The copy operation itself does not mutate the source.** This is true. Both `insertpm` (do1.c:60) and `insertspanf` (do1.c:62) receive `docisaptr` (the target) as the document being modified. `logbertmodified` is called on the target, not the source. The source's granfilade and spanfilade are read via the `ispanset` structure but never written.

**Claim B: The source's content identity is protected from concurrent mutation during the copy.** This is false. Because `NOBERTREQUIRED` bypasses `checkforopen` entirely (`bert.c:59–61`), no BERT entry is created for the source document during `docopy`. The truth table at `bert.c:44–50` only governs behavior when a BERT entry exists:

```
Open state -->
type            Not Open    #   Open READ    #  Open WRITE
  |         !owned | owned  #conn==|conn!=   #conn==|conn!=
  v         -------+------  #------+------   #------+------
READ           0   |   0    # READ |   0     # WRITE| -1
WRITE         -1   |   0    #  -1  |  -1     # WRITE| -1
```

With `NOBERTREQUIRED`, the protocol never reaches this table. A second connection holding `WRITEBERT` on the source could modify it concurrently — creating a new version with a different tumbler address — and `docopy` would have no awareness of this. There is no transactional read snapshot of the source.

---

### Notable variant: `docopyinternal`

`do1.c:66–82` defines a separate `docopyinternal` that uses `NOBERTREQUIRED` for **both** source and target:

```c
if (!findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)) return FALSE;  /* do1.c:75 */
```

This is used for internal self-copy operations (e.g., during `doinsert` at do1.c:95). It bypasses WRITEBERT on the target entirely, relying on the caller to guarantee safety.

---

### Summary

| | Source | Target |
|---|---|---|
| Permission required | `NOBERTREQUIRED` — none | `WRITEBERT` — enforced at `do1.c:55` |
| BERT entry created | No | Yes, at time of `doopen` |
| Content mutated during copy | No (read only) | Yes — `insertpm` + `insertspanf` |
| Concurrent write protection | **None** — no lock held | Protected by WRITEBERT open state |

The source's access is not "read-only" in the BERT sense — it is **unlocked**. The copy operation reads the source without creating any BERT entry, which means no protocol-level guarantee prevents another connection from modifying the source concurrently. The source's content identity is safe only by convention, not enforcement.
