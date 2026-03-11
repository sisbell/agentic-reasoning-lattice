## Question 14 [gregory]

> When `CLOSEDOCUMENT` is called, does it flush dirty POOM nodes for that document to disk, or does it only remove the BERT entry and leave cache eviction to the grim reaper?

## KB Synthesis

The KB does not directly describe the implementation of `CLOSEDOCUMENT`. No finding covers what the close handler does internally.

That said, the KB provides strong contextual evidence for an informed inference:

**Against per-document flush:**

- [SS-DURABILITY-BOUNDARY] (Finding 0059): Durability is session-level. `writeenfilades()` is called only from `bed.c:134` during daemon shutdown. There is no documented per-document or per-operation flush. The section explicitly states: "Within-session consistency comes from the in-memory cache, not from disk state."

- [SS-CACHE-MECHANISM] (Finding 0059): The grim reaper selects eviction victims by age (`age >= OLD`), not by document state or close events. Eviction is triggered by memory pressure, not lifecycle events.

- [SS-UNIFIED-STORAGE] (Finding 0059): All enfilade types share a single cache and allocator. There is no per-document cache partition that could be selectively flushed.

**What close almost certainly does:**

Based on [SS-BERT] and [PRE-OPEN-DOC], `CLOSEDOCUMENT` removes the document from the session's open list and updates the BERT table (decrement reference count or remove the entry). This is consistent with the access control model where `checkforopen` tests open-list membership before allowing content operations.

**Bottom line:** The KB cannot confirm this with a code-level citation, but all documented mechanisms point to the grim reaper handling dirty POOM node eviction independently of document close. `CLOSEDOCUMENT` almost certainly only manages the BERT entry and open-list membership — no flush.

If this matters for a spec precondition, the gap should be filled by direct code inspection of the `CLOSEDOCUMENT` handler in `do2.c` or `do1.c`.

---

## Code Exploration

I have enough information to give a complete answer. Here is the full trace:

---

## `CLOSEDOCUMENT`: BERT entry removal only — no disk flush

### Execution path

**`CLOSEDOCUMENT`** is handled by `myclose()` [`fns.c:404`]:

```c
void myclose(typetask *taskptr)
{
    if(getclose(taskptr, &t) && doclose(taskptr, &t, user))
        putclose(taskptr);
    else
        putrequestfailed(taskptr);
}
```

`doclose()` [`bert.c:325`] does exactly one thing:

```c
bool doclose(typetask *taskptr, tumbler *tp, int connection)
{
    if (!removefromopen(tp, connection))
        fprintf(stderr, "Bert was not open!\n");
    return TRUE;
}
```

`removefromopen()` [`bert.c:154`]:
1. Finds the matching `bertentry` in the hash table.
2. Decrements `bert->count` [`bert.c:169`]. If the count is still > 0 (multiple opens), returns immediately — nothing else happens.
3. When count reaches 0: evaluates `bert->created && !bert->modified` [`bert.c:173`]. If true (doc was created but never written to), calls `deleteversion()`.
4. Calls `efree(p->stuff)` and splices the conscell out of the hash chain [`bert.c:177-188`].

That is the entire operation. **There is no call to `diskflush()`, `writeenfilades()`, `orglwrite()`, `subtreewrite()`, or any other disk-write function.**

### `deleteversion()` is a stub

```c
int deleteversion(tumbler *tp)
{
#ifndef DISTRIBUTION
    fprintf(stderr,"deleteversion: tp = ");
    dumptumbler(tp);
    fprintf(stderr,"\n");
#endif
}
```
[`bert.c:348-353`] — The body is empty. It does nothing. In `DISTRIBUTION` builds it emits zero bytes.

Note also that the condition in `removefromopen` — `bert->created && !bert->modified` — is the *opposite* of what `exitbert()` checks. `exitbert()` [`bert.c:210`] calls `deleteversion` when `modified && created` (to roll back an abandoned session). `removefromopen` calls it when `created && !modified` — a created-but-untouched document. Either way, `deleteversion()` is currently a no-op.

### When does disk I/O actually happen?

**1. The Grim Reaper — memory-pressure eviction (`credel.c:106–329`)**

When `ealloc()` runs out of free memory [`credel.c:70-75`], it calls `grimlyreap()`, which walks the `grimreaper` ring looking for an `isreapable()` node. `reap()` then either:

- Calls `orglwrite((typecbc*)temp)` [`credel.c:309`] for apex POOM nodes
- Calls `subtreewrite(temp)` [`credel.c:329`] for non-apex nodes

Both paths eventually call `writeloaf()` to write blocks to disk. This is the only path that flushes dirty POOM nodes on demand during normal operation — and it is triggered by **memory pressure, not by `CLOSEDOCUMENT`**.

**2. Last user disconnects (`bed.c:105`)**

```c
if (n_players < 1) {
    diskflush();   /* Write out everything when no one around */
    ...
}
```

`diskflush()` [`corediskout.c:58`] calls `writeenfilades()` + `initkluge()`, serializing the entire granfilade and spanfilade to disk.

**3. QUIT or SIGINT (`bed.c:134-135`, `bed.c:183-184`)**

```c
writeenfilades();
closediskfile();
```

Both the `quitafteruser` path and the `flagquitting()` SIGINT handler call this before `exit()`.

**4. Single-user exit via `diskexit()` (`corediskout.c:30-53`)**

Same: `writeenfilades()` + `closediskfile()`.

### Answer

**`CLOSEDOCUMENT` only removes the BERT entry.** It has no effect on POOM nodes or the in-core enfilade. Dirty POOM nodes accumulate in memory and are flushed in one of three ways:

1. **Lazily by the grim reaper** — only when `ealloc()` fails under memory pressure, via `reap()` → `orglwrite()` / `subtreewrite()` [`credel.c:292-329`]
2. **Globally when the last user leaves** — via `diskflush()` [`bed.c:105`]
3. **On process exit** — via `writeenfilades()` in `diskexit()`, `quitxanadu()`, or signal handlers

So the second framing in your question is correct: `CLOSEDOCUMENT` removes the BERT entry and **leaves cache eviction entirely to the grim reaper** (and to the exit path). There is no per-document flush on close.
