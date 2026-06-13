## Question 18 [evidence]

> If two sessions each create a successor to the same link `2.N` in the same home document, does the run-to-completion event loop simply allocate them V-positions `2.N+1` and `2.N+2` with no detection that both claim to replace `2.N` — leaving the fork between competing successors unrecorded in any enfilade?

## KB Synthesis

Yes, that is exactly what happens — and the KB gives a precise account of every layer involved.

## Event Loop Serialization

The backend processes requests strictly one at a time [INV-SEQUENTIAL-DISPATCH] [INV-ATOMICITY]. Even if both sessions have requests ready on their file descriptors simultaneously, `select()` returns and the loop processes Session A's CREATELINK to completion before Session B's begins. There is no interleaving.

## V-Position Allocation

When Session A's CREATELINK executes, `findnextlinkvsa` computes the next V-position as `vspanreach` — the current document-end extent of the link subspace — and places the new link orgl there (e.g. `2.N+1`) [SS-LINK-SUBSPACE] [ST-CREATE-LINK]. After that operation completes, `vspanreach` has advanced. When Session B's CREATELINK executes, `findnextlinkvsa` reads the now-updated extent and allocates `2.N+2` [ST-ADDRESS-ALLOC]. 

The allocation uses a stateless `findpreviousisagr` query-and-increment, so Session B sees Session A's link orgl as the new maximum and steps past it [SS-ADDRESS-SPACE] [INV-MONOTONIC].

## No Fork Is Recorded Anywhere

The three-layer link model has no lineage field [SS-THREE-LAYER-MODEL]:

- **I-space (link orgl):** Stores FROM/TO/TYPE endsets and the home document. No predecessor pointer, no version field.
- **Spanfilade (DOCISPAN/link index):** Maps I-addresses to link ISAs for discovery. No lineage.
- **POOM (document V-stream):** Records the V-position (`2.N+1` or `2.N+2`) of each link's orgl ISA. The two entries sit adjacently in the `2.x` subspace with no structural relationship between them and `2.N`.

Both new links are permanent and independently discoverable [INV-LINK-PERMANENCE] [ST-LINK-GLOBAL-VISIBILITY]. Nothing in any enfilade encodes that they were both intended to follow `2.N`. The concept of "successor" or "replacement" is purely application-level; the backend has no such abstraction.

## Access Control Caveat

CREATELINK follows the correct BERT-check-before-response pattern — unlike INSERT/DELETE which send success before checking [EC-RESPONSE-BEFORE-CHECK]. Because WRITEBERT is exclusive [INV-WRITE-EXCLUSIVITY], under normal protocol only one session holds write access to the home document at a time. If Session B lacks WRITEBERT, its CREATELINK returns failure, not a silent discard. But if both sessions somehow reach CREATELINK with valid write access (e.g. on separate home documents sharing content identity, or if BERT compliance is bypassed per [INT-BERT-FEBE]), the sequential allocator simply produces `2.N+1` and `2.N+2` with the fork undetected and unrecorded.

---

## Code Exploration

I now have all the evidence needed. Let me compile the full answer.

---

## Answer: Concurrent Link Successor Creation in the Same Home Document

### 1. The event loop is single-threaded and strictly run-to-completion

`bed.c:103–142` shows a `select()`-based multiplexer that processes one request at a time:

```c
for (;;) {
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... } else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                task.inp = player[user].inp;
                task.outp = player[user].outp;
                task.account = player[user].account;
                xanadu(&task);          // [bed.c:128]
            }
        }
    }
}
```

`xanadu()` at `bed.c:153–172` calls `(*requestfns[request])(taskptr)` and sends the result before returning. Even when multiple file descriptors are simultaneously ready after a single `select()` call, the inner `for i` loop processes them **one at a time in fd-number order**. There is no preemption and no parallelism.

---

### 2. V-position allocation reads live document state

`findnextlinkvsa` in `do2.c:151–167` computes where the next link will be placed:

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);   // firstlink = 2.0
    tumblerincrement (&firstlink, 1, 1, &firstlink);   // firstlink = 2.1

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);   // current extent
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);
    else
        movetumbler (&vspanreach, vsaptr);          // = max(2.1, stream+width)
    return (TRUE);
}
```

The result is `max(2.1, stream + width)` — the immediate end of the current document content. Because the loop serializes requests, each call reads the state left by all previous completed operations.

**Consequence:** With a serialized loop, Session A's `CREATELINK` completes first and updates the document vspan. Session B's `CREATELINK` then reads the already-updated vspan. They cannot both receive the same position `2.N+1`. They receive `2.N+1` and `2.N+2` sequentially — **the exact collision the question describes cannot occur at runtime**.

---

### 3. But the BERT write-lock is bypassed for link creation

`docreatelink` in `do1.c:195–221` has this chain:

```c
  && createorglingranf (taskptr, granf, &hint, linkisaptr)     // [do1.c:209]
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)          // [do1.c:210]
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)            // [do1.c:211]
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)           // [do1.c:212]
  && findorgl (taskptr, granf, linkisaptr, &link,
               /*WRITEBERT ECH 7-1*/ NOBERTREQUIRED)           // [do1.c:213]
```

The comment `/*WRITEBERT ECH 7-1*/` shows the write-permission check on the link organelle itself was deliberately disabled. `NOBERTREQUIRED` short-circuits `checkforopen` at `bert.c:59–61`:

```c
if (type == NOBERTREQUIRED) {
    return 1;    // always succeeds — [bert.c:60–61]
}
```

So while `docopy` still checks BERT on the **home document** (`do1.c:212` → `findorgl(..., WRITEBERT)` in `do1.c:55`), the link organelle itself has no access guard. Both sessions can call `CREATELINK` on the same home document without any BERT-level conflict detection for the link object.

---

### 4. ISA allocation is also purely sequential with no ancestry field

`createorglgr` in `granf2.c:111–128` calls `findisatoinsertgr`, which for `LINKATOM` reaches `findisatoinsertmolecule` at `granf2.c:158–181`:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;
    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement (isaptr, 1, 1, isaptr);
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);
        else
            tumblerincrement (&lowerbound , 0, 1, isaptr);
    }
}
```

`findpreviousisagr` (`granf2.c:255`) scans the in-memory granf tree for the highest ISA below `upperbound`. The result is a pure increment from the current highest-allocated ISA. **No "predecessor" field, no "branched-from" pointer, no ancestry metadata** enters the `locinfo` struct or is written into the enfilade by `insertseq` at `granf2.c:125`. The link organelle's ISA simply encodes its ordinal position under the parent document in the tumbler tree.

---

### 5. The spanf (link endpoint index) has no fork record either

`insertendsetsinspanf` (called at `do1.c:219`) writes from/to/three endpoint sets into the spanfilade. The data stored is endpoints only — no "this link supersedes link X" field exists anywhere in the spanf item structure.

---

### Summary

| Question | Answer |
|---|---|
| Can both sessions receive the same V-position 2.N+1? | **No.** Run-to-completion ensures `findnextlinkvsa` always reads the post-update vspan. |
| Do they receive 2.N+1 and 2.N+2 sequentially? | **Yes.** Whichever session's `CREATELINK` arrives first in the fd-scan order gets 2.N+1; the other gets 2.N+2. |
| Does BERT detect the conflict for the link organelle? | **No.** `docreatelink` [do1.c:213] explicitly passes `NOBERTREQUIRED`, bypassing the write-lock check. |
| Is the fork — that both sessions intended to follow 2.N — recorded in any enfilade? | **No.** Neither the granf crum, the spanf entry, nor the V-position allocation carries any predecessor reference. The two new links appear as consecutive siblings with no structural trace of their shared origin. |

The run-to-completion scheduler prevents the V-position collision from actually occurring, but it provides no substitute for the missing version-lineage record. Once both requests have completed, the historical fact that two sessions each intended to place the next link after 2.N — constituting a fork in the link sequence — is **permanently lost from every enfilade in the system**.
