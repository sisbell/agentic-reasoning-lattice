## Question 15 [gregory]

> In a multi-session scenario where session A creates a link L targeting content in document D, and session B simultaneously deletes that content from D before A's operation completes — given run-to-completion atomicity, is there any window where L's spanfilade entries could reference I-addresses that were never actually present in D's POOM, or does the serialized execution guarantee consistency between link creation and POOM state?

## KB Synthesis

## Answer

No window exists where L's spanfilade entries can reference I-addresses that were **never actually present** in D's POOM. The combination of run-to-completion atomicity and the V-to-I filtering invariant forecloses it.

### Why atomicity closes the concurrent window

[INV-ATOMICITY] and [INV-SEQUENTIAL-DISPATCH] establish that the `bed.c` event loop is a total serializer: every FEBE operation runs to full completion (parse → mutate → respond) before the next begins. Two sessions' operations never interleave. So the scenario reduces to exactly two orderings:

---

**Case 1: CREATELINK executes before DELETE**

At CREATELINK time, D's POOM still contains the target I-addresses. [ST-CREATE-LINK] shows the operation converts the target V-span to I-addresses via `vspanset2sporglset` → `vspanset2ispanset`, reads the current POOM, finds the addresses, and writes them to the spanfilade via `insertendsetsinspanf`. The spanfilade entries reference I-addresses that *were* present in D's POOM at creation time.

Session B's DELETE then executes. [ST-DELETE] and [INV-SPANF-WRITE-ONLY] confirm DELETE removes only POOM mappings — the spanfilade is never modified. L's entries now point to I-addresses that are no longer in D's POOM: the standard post-hoc orphan/ghost-link state [EC-GHOST-LINK]. The addresses were genuinely present when written; they were only removed afterward.

---

**Case 2: DELETE executes before CREATELINK**

At CREATELINK time, D's POOM no longer contains the target I-addresses. The conversion chain `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` searches D's POOM for the requested V-positions. [INV-ITOV-FILTERING] establishes this as a universal invariant: when `retrieverestricted` returns NULL for an I-address with no current POOM mapping, `span2spanset` silently drops it. The resulting sporglset contains only I-addresses *currently* present in D's POOM.

[ST-CREATE-LINK] then calls `insertendsetsinspanf` with this filtered sporglset. If the deletion removed all the target content, the sporglset is empty and nothing is written to the spanfilade. If some content survived the deletion (e.g., adjacent content shifted into the query range), only those surviving I-addresses are indexed.

In neither sub-case does the spanfilade acquire entries for I-addresses that were never in D's POOM.

---

### Summary

| Ordering | Spanfilade entries at L's endpoints | Were they ever in D's POOM? |
|---|---|---|
| CREATELINK → DELETE | Valid I-addresses, later orphaned | Yes — present at creation time |
| DELETE → CREATELINK | Only currently-present I-addresses (possibly none) | Yes — present at creation time |

The serialized execution guaranteed by [INV-ATOMICITY] means CREATELINK always observes a consistent POOM snapshot. The V-to-I filtering at [INV-ITOV-FILTERING] acts as a further gate: even if session A passed a V-span spec for content that no longer exists, the POOM lookup would return nothing rather than synthesizing phantom I-address entries.

The only scenario that *would* produce spanfilade entries for I-addresses outside D's POOM is the post-hoc orphan (Case 1), but those addresses were genuinely present at the moment of indexing — which is the expected behavior of an append-only spanfilade in a system with permanent but POOM-mutable content.

---

## Code Exploration

I now have all the source I need. Let me compile the complete answer.

---

## Answer: Serialization, V→I Translation, and the Race Impossibility

### 1. The Event Loop Provides True Run-to-Completion Serialization

`bed.c` implements a single-process, single-threaded `select()`-based event loop. There is no threading, no async, no coroutines.

```c
// bed.c:110-142
for (i = 0; i <= nfds; i++) {
    if ((1<<i) & inputfds2) {
        user = fdtoplayer[i];
        task.inp = player[user].inp;
        task.outp = player[user].outp;
        task.account = player[user].account;
        ...
        xanadu(&task);   // ← complete request before incrementing i
```

Even when both sessions A and B have data ready when `select()` returns, the inner `for (i = 0; ...)` loop processes them one at a time, sequentially. `xanadu()` [bed.c:153] calls `(*requestfns[request])(taskptr)` and only returns after `sendresultoutput` and `tfree` complete. **There is no point at which two handlers execute concurrently or interleave.** The scenario "session B deletes before A's operation completes" cannot occur mid-operation — one fully serializes before the other begins.

The only real question is ordering: does B's `deletevspan` run before or after A's `createlink`?

---

### 2. Deletion Touches Only the POOM, Not the Permascroll

`dodeletevspan` [do1.c:158-167]:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr));
}
```

`deletevspanpm` [orglinks.c:145-152]:

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

`deletend` operates on `docorgl` — D's POOM (permutation matrix enfilade). It removes the V→I mapping nodes for the deleted span. The granfilade (permascroll) is untouched. **I-addresses in the permascroll are permanent and are never deleted.**

---

### 3. The V→I Translation Path in `docreatelink`

`docreatelink` [do1.c:195-221] translates A's V-address specset to I-address sporglsets at lines 214-216:

```c
&& specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset,&threesporglset,NOBERTREQUIRED)
```

`specset2sporglset` [sporgl.c:14-33] calls `vspanset2sporglset` [sporgl.c:35-65] for each `VSPECID` spec:

```c
typesporglset *vspanset2sporglset(typetask *taskptr, typeisa *docisa,
    typevspanset vspanset, typesporglset *sporglsetptr, int type)
{
    ispanset = NULL;
    if (!findorgl (taskptr, granf, docisa, &orgl, type))
        return (NULL);
    for (; vspanset; vspanset = vspanset->next) {
        (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
        for (; ispanset; ispanset = ispanset->next) {
            sporglset = taskalloc(...);
            sporglset->itemid = SPORGLID;
            movetumbler(docisa, &sporglset->sporgladdress);
            movetumbler(&ispanset->stream, &sporglset->sporglorigin);
            movetumbler(&ispanset->width,  &sporglset->sporglwidth);
            *sporglsetptr = sporglset;
            sporglsetptr = &sporglset->next;
        }
    }
    return (sporglsetptr);
}
```

The V→I translation uses `vspanset2ispanset` [orglinks.c:389-394] → `permute` [orglinks.c:404-422] → `span2spanset` [orglinks.c:425-454] → `retrieverestricted` [retrie.c:56-85] → `findcbcinarea2d` [retrie.c:229-268].

This is a **live query against D's current POOM tree**. It finds only those POOM nodes whose V-range intersects the requested V-span. `crumqualifies2d` [retrie.c:270-305] gates every node on actual position.

---

### 4. The Two Serialization Cases

**Case A: A's `createlink` runs first, B's `deletevspan` runs second**

`specset2sporglset` queries D's POOM, finds the nodes covering A's requested V-span, and returns valid I-addresses. These I-addresses were present in D's POOM at the moment of translation, and they are permanently in the granfilade. B later calls `deletend` on D's POOM, removing those V→I mapping nodes — but the I-addresses in L's spanfilade remain permanently valid. They correctly reflect content that *was* in D when the link was created. **No phantom references.**

**Case B: B's `deletevspan` runs first, A's `createlink` runs second**

`deletend` has already removed D's POOM nodes covering the target V-span. When A's `specset2sporglset` calls `retrieverestricted`, it finds **no matching nodes**. `span2spanset` [orglinks.c:446-448]:

```c
if(!context){
    return(targspansetptr);   // ← returns unchanged (empty) if no context
}
```

`vspanset2ispanset` returns an empty ispanset. The inner `for (; ispanset; ...)` loop in `vspanset2sporglset` [sporgl.c:49] never executes. `fromsporglset`/`tosporglset` remain NULL.

`insertendsetsinspanf` [do2.c:116-128] calls `insertspanf` [spanf1.c:15-53] with a NULL sporglset:

```c
for (; sporglset; sporglset = ...) {  // ← never enters loop
    insertnd(...);
}
return (TRUE);
```

Nothing is inserted into the spanfilade. `insertpm` [orglinks.c:100-133] similarly loops over the empty sporglset and inserts nothing into the link's POOM.

**L is created successfully (docreatelink returns TRUE), but with empty endpoint entries — no spanfilade insertions, no POOM entries for its endpoints.** A "ghost link": it has a valid ISA and occupies a V-slot in D's link subspace, but `findlinksfromtothree` will never return it, and `followlink` will fail to produce endpoints.

---

### 5. Could the Spanfilade Ever Contain I-Addresses "Never Present in D's POOM"?

**No.** The proof follows directly from the architecture:

1. **Serialization**: Only one handler executes at a time. B cannot interrupt A mid-execution.

2. **Translation is a live query**: `specset2sporglset` translates V→I against D's **current** POOM state at the instant A's request runs. Any I-address it produces was, by definition, present in D's POOM at that instant.

3. **Deletion doesn't retroactively contaminate**: After A's `insertendsetsinspanf` completes, the spanfilade contains I-addresses that correspond to what was in D's POOM at A's execution time. B's subsequent `deletend` cannot reach back and alter those spanfilade entries — the spanfilade has no back-pointer into the POOM.

4. **Empty result on miss**: If the V-addresses don't map to anything in D's POOM (because B already deleted them), `retrieverestricted` returns NULL, and **zero bytes are written to the spanfilade**. There is no fallback path that constructs a fabricated I-address.

The one pathological outcome is **Case B's ghost link**: a link with a valid ISA but no indexed endpoints. The design trades "link creation always succeeds" against "link endpoints may be empty if the content was concurrently deleted." This is a semantic hazard — the caller receives an `linkisa` back from `putcreatelink` with no indication the endpoints resolved to nothing — but it is categorically not the phantom-I-address scenario the question asks about. The spanfilade's consistency with the POOM is guaranteed by the serialized execution and the live V→I query.
