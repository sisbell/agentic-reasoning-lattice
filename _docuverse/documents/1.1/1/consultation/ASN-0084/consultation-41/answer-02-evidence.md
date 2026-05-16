## Question 2 [evidence]

> When REARRANGE is invoked with arguments violating its preconditions (e.g., cut sequence extending beyond the document's V-positions), does udanax-green refuse the operation, signal an error, or exhibit some other defined failure behavior?

## KB Synthesis

## REARRANGE with Out-of-Bounds Cut Points

The KB distinguishes several failure modes based on which precondition is violated.

### What IS enforced: cut count

The only hard validation is the cut count. Providing exactly 2 cuts causes the backend to abort with "Wrong number of cuts" [PRE-REARRANGE Finding 0006]. Valid counts are `|cuts| ∈ {3, 4}`.

### What is NOT enforced: cut ordering and bounds

Cut ordering is silently normalized — `sortknives()` reorders misordered inputs before any processing occurs. This is explicitly not a precondition [PRE-REARRANGE Finding 0056].

Cut positions exceeding document V-extent are **not validated**. The algorithm in `rearrangend()` proceeds as:

1. Sort cuts
2. Compute offsets purely from cut-point arithmetic (`makeoffsetsfor3or4cuts`) — no reference to document state
3. Iterate over POOM spans, classify each into a region via `rearrangecutsectionnd`
4. Apply the computed offset via `tumbleradd`

When cuts extend beyond the document, step 3 simply finds no POOM entries in the out-of-bounds regions. **Empty regions contribute nothing to move** [EC-REARRANGE-EMPTY-REGION]. The operation proceeds without error; the out-of-bounds portions of the rearrangement are silently skipped.

### The response-before-check pattern

Like INSERT and DELETEVSPAN, the FEBE handler for REARRANGE follows the pattern where success is sent to the client *before* `dorearrange()` executes [PRE-INSERT Finding 0050, EC-RESPONSE-BEFORE-CHECK]. So even if the underlying operation is a partial no-op, the client receives a success response.

### Summary

| Violation | Behavior |
|-----------|----------|
| Wrong cut count (e.g., 2) | Backend abort: "Wrong number of cuts" |
| Misordered cuts | Silently sorted, proceeds |
| Cuts beyond document extent | No error; beyond-bounds regions are no-ops; client receives success |
| Cross-subspace cuts | No error; content moves across subspace boundaries [EC-REARRANGE-CROSS-SUBSPACE] |

The system does not define a "refuse" or "signal error" path for out-of-bounds cuts — the operation degrades silently to a partial rearrangement covering only the content that actually exists within the specified ranges.

---

## Code Exploration

Now I have everything verified. Here is the complete answer.

---

## REARRANGE Precondition Violation: Behavior Analysis

### The Short Answer

When REARRANGE receives cut positions that extend beyond the document's V-space, udanax-green exhibits **three distinct failure modes** depending on which layer catches the problem: a silent success sent to the client before work begins, a process abort via `abort()`, or a corrupt document state. No graceful refusal exists. The client is never correctly informed.

---

### Layer 1: Protocol Parsing — fns.c:159–173

The REARRANGE handler is structurally broken relative to every other request handler in the file:

```c
/* fns.c:143–157 — COMMENTED OUT correct version: */
void rearrange (taskptr)
  typetask *taskptr;
{
  ...
  if (
     getrearrange (taskptr, &docisa, &cutseq)
  && dorearrange (taskptr, &docisa, &cutseq))
      putrearrange (taskptr);
    else
      putrequestfailed (taskptr);
}

/* fns.c:159–173 — ACTIVE version: */
void rearrange(typetask *taskptr)
{
  typeisa docisa;
  typecutseq cutseq;
  bool getrearrange(), dorearrange();
 
  (void) getrearrange (taskptr, &docisa, &cutseq);   /* return ignored */
  putrearrange (taskptr);                            /* SUCCESS sent NOW */
  if (!dorearrange (taskptr, &docisa, &cutseq))
#ifndef DISTRIBUTION
      fprintf(stderr,"rearrange failed \n");
#else
      ;
#endif
}
```

The original correct version (lines 143–157) is commented out. The replacement at line 159:

1. Casts `getrearrange()` return to `void` — **validation result ignored** [fns.c:165]
2. Calls `putrearrange()` **unconditionally and before any work** [fns.c:166]
3. Only then calls `dorearrange()` [fns.c:167]
4. If `dorearrange()` fails: debug builds print to stderr; DISTRIBUTION builds do **nothing** [fns.c:169–172]

**The client always receives a success response, regardless of whether the operation failed or even whether the protocol was parseable.** This is not a design choice — the commented-out correct version sitting immediately above it shows it was a regression.

---

### Layer 2: Protocol Validation — get2fe.c, get1fe.c

`getrearrange()` [get1fe.c:65] calls `getcutseq()` which enforces exactly one constraint:

```c
/* get2fe.c:230–231 */
if (!(
   getnumber (taskptr, &ncuts)
&& (ncuts == 3 || ncuts == 4)))
    return (FALSE);
```

It validates that `ncuts` is 3 or 4. **It performs zero validation that the cut positions are within the document's V-space.** The tumbler values are read verbatim [get2fe.c:236–239].

Since the handler ignores this return value anyway [fns.c:165], even a structurally malformed cut sequence (wrong count) causes no refusal — `dorearrange()` runs with whatever garbage was in `cutseq`.

---

### Layer 3: Document Lookup — do1.c:34–43

```c
bool dorearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr)
{
  typeorgl docorgl;
  bool findorgl(), rearrangepm();;

  return (
     findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && rearrangepm (taskptr, docisaptr, docorgl, cutseqptr)
  /*&& TRUE*/ /* ht stuff */  );
}
```

`findorgl()` can legitimately return FALSE (document not found, not open for writing). When it does, `dorearrange()` returns FALSE — which the handler ignores [fns.c:167]. No error reaches the client.

---

### Layer 4: rearrangepm — orglinks.c:137–142

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
  rearrangend((typecuc*)docorgl, cutseqptr, V);
  logbertmodified(docisaptr, user);
  return (TRUE);
}
```

`rearrangepm()` **always returns TRUE** [orglinks.c:141]. The return value of `rearrangend()` (declared `int`) is discarded. Any failure inside `rearrangend()` that does not call `abort()` is silently swallowed here.

---

### Layer 5: rearrangend — edit.c:78–160

This is where out-of-bounds cuts finally meet document structure. There are **no precondition guards** at the top of the function. The cut positions are copied directly into `knives` without bounds checking:

```c
/* edit.c:102–107 */
knives.dimension = index;
knives.nblades = cutseqptr->numberofcuts;
for (i = 0; i < knives.nblades; i++) {
    movetumbler (&cutseqptr->cutsarray[i], &knives.blades[i]);
}
sortknives (&knives);
makeoffsetsfor3or4cuts (&knives, diff);   /* edit.c:108 */
```

`makeoffsetsfor3or4cuts()` [edit.c:164] performs only one check — that `nblades` is 3 or 4 [edit.c:183: `gerror("Wrong number of cuts.")`] — and does arithmetic on the tumbler values without checking their range against the document.

The critical path is then `makecutsnd()` followed by the crum traversal loop:

```c
/* edit.c:113–135 */
for (ptr = (typecuc*)findleftson(father); ptr; ptr = (typecuc *)findrightbro(...)) {
    i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
    switch (i) {
      case -1:
        gerror ("rearrangend can't classify crum\n");   /* edit.c:118 */
      case 0:  case 4: /* these never move */
        break;
      case 1:  case 2:  case 3:
        tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
        ivemodified((typecorecrum*)ptr);
        break;
      default:
        gerror ("unexpected cutsection\n");             /* edit.c:131 */
    }
}
```

---

### Layer 6: Classification — edit.c:191–204

`rearrangecutsectionnd()` determines which cut-slice each crum belongs to:

```c
INT rearrangecutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
  INT i, cmp;
  for (i = knives->nblades -1; i >= 0 ; --i) {
      cmp = whereoncrum (ptr, offset, &knives->blades[i], knives->dimension);
      if (cmp == THRUME) {
          return (-1);                  /* edit.c:198 */
      } else if (cmp <= ONMYLEFTBORDER) {
          return (i+1);
      }
  }
  return (0);
}
```

`THRUME` means the cut passes *through* a crum — the crum straddles the cut boundary — making classification impossible. This is the condition that triggers with out-of-bounds cuts that partially intersect existing crums.

When any crum returns -1, `rearrangend()` falls into `case -1:` with no `break` and hits `gerror()`.

---

### The Fatal Path: gerror → abort — genf.c:546–551

```c
INT qerror(char *message)
{
    fprintf (stderr, "Error: %s\n",message);
    abort();      /* genf.c:549 */
    return(1);
}
```

`gerror` is `#define gerror(s) qerror(s)` [common.h]. It calls `abort()`. **The backend process terminates.** All open sessions die. No error response reaches the client.

---

### Failure Mode Summary

| Precondition Violated | What Happens | Client Sees |
|---|---|---|
| `ncuts` not 3 or 4 | `getcutseq()` returns FALSE; handler ignores it; `dorearrange()` runs on uninitialized `cutseq` | Success (REARRANGE=3) |
| Cut positions beyond document V-space, no crum straddles cut | All crums classify as case 0 (no movement); operation silently no-ops | Success (REARRANGE=3) |
| Cut positions cause any crum to straddle the cut (THRUME) | `gerror()` called → `abort()` → **process crash** | Connection drops |
| Document not open / not found | `findorgl()` returns FALSE; client already got success at fns.c:166 | Success (REARRANGE=3) |
| `dorearrange()` fails for any reason | Debug build: stderr message. Distribution build: nothing | Success (REARRANGE=3) |

---

### Root Cause

The active `rearrange()` handler [fns.c:159–173] diverges from the pattern used by every other handler in `fns.c`. The commented-out correct version directly above it [fns.c:143–157] shows the intended structure: validate → do work → send success OR failure. The replacement sends success unconditionally before doing any work, making it impossible for the backend to ever signal REARRANGE failure to a client.

The outcome for any cut sequence extending beyond document V-positions: the client receives success, the backend either does nothing (cuts beyond all crums) or crashes (cuts through a crum boundary).
