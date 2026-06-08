## Question 1 [evidence]

> Does `docopy` perform the displacement and the fill as a single indivisible step, or does it pass through an intermediate state in which the displaced content-subspace positions are dropped/relocated before the copied addresses are bound?

## KB Synthesis

## `docopy` Displacement and Fill Sequencing

`docopy` passes through a logically two-phase internal sequence, but the intermediate state is never externally observable.

### Internal sequencing: two distinct phases

`docopy` routes through `insertpm` → `insertnd` → `makegappm` — the same path as INSERT and CREATELINK [ST-INSERT, Finding 0052].

Within `insertnd`, the phases are ordered:

1. **Displacement phase** — `makegappm` constructs the two-blade knife (`blade[0]` = insertion point, `blade[1]` = next subspace boundary). `insertcutsectionnd` then walks all existing POOM crums and applies `tumbleradd` to the V-displacement of every crum classified as case 1 (within `[blade[0], blade[1])`). After this step, the shifted crums have new V-positions, but no new V→I mapping exists yet for the incoming content [SS-TWO-BLADE-KNIFE, ST-INSERT Finding 0054].

2. **Fill phase** — `isanextensionnd` tests for rightward extension (same `homedoc`, `reach == origin`). If it fires, the existing crum's width is incremented in place. Otherwise, a new bottom crum is allocated and adopted as a right sibling [ST-INSERT, Finding 0062]. Only at this point does the new V→I binding exist.

So yes, there is a transient internal state in which displaced entries have moved but the incoming addresses are not yet bound.

### Why it is not observable

The entire FEBE operation — including all steps of `docopy` — runs to completion inside a single `xanadu(&task)` invocation before the event loop returns to `select()`. The backend is single-threaded with no preemption and no signal handlers that modify state [INV-ATOMICITY, Finding 0042; INV-SEQUENTIAL-DISPATCH, Finding 0042]. No other session or operation can observe the tree between the displacement and fill steps.

### Caveats specific to `docopy`

Unlike raw INSERT (which allocates fresh I-addresses via `inserttextingranf`), `docopy` supplies pre-existing I-spans directly to `insertpm`. The fill phase therefore places existing I-addresses, not freshly allocated ones — but the displacement-then-fill ordering is identical [ST-COPY, Finding 0046; PRE-COPY, Finding 0046].

**Summary:** Displacement and fill are sequential within `insertnd`, not a single indivisible step at the instruction level, but the intermediate state is invisible because the containing FEBE operation is run-to-completion atomic.

---

## Code Exploration

I have all the information needed. Let me write the complete answer.

---

## Does `docopy` perform displacement and fill as a single indivisible step?

**No.** `docopy` executes them as two sequential, non-atomic function calls with a well-defined intermediate state between them.

---

### The call sequence in `docopy` [`do1.c:53–64`]

```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa (vsaptr, docorgl)
&& asserttreeisok(docorgl)

/* the meat of docopy: */
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   // step 1

&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // step 2
&& asserttreeisok(docorgl)
);
```

**Step 1** (`insertpm`) and **Step 2** (`insertspanf`) operate on entirely different data structures and are evaluated independently by C's `&&` short-circuit operator. There is no transaction, no lock, no rollback. The only thing connecting them is the shared `ispanset` value.

---

### Step 1: `insertpm` — POOM displacement + POOM fill [`orglinks.c:75–134`]

`insertpm` iterates over the `sporglset` (the `ispanset`, i.e. the content-space / I-space addresses of what is being copied). For each ispan, it calls:

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
// [orglinks.c:130]
```

Inside `insertnd`, when the enfilade type is `POOM` [`insertnd.c:51–61`]:

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);      // displacement
    checkspecandstringbefore();
    setwispupwards(fullcrumptr,0);
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index); // POOM fill
    setwispupwards(fullcrumptr,1);
    break;
```

**The displacement** happens inside `makegappm` [`insertnd.c:124–172`]. It makes two cuts in V-space at `origin` and just after (`findaddressofsecondcutforinsert`), then walks the child crums and shifts every crum to the right of the insertion point forward:

```c
case 1:
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
    // [insertnd.c:162]
    ivemodified (ptr);
    break;
```

This sliding of existing V-addresses forward is the displacement. It happens entirely within `makegappm`, before `doinsertnd` is called.

**The POOM fill** (binding the new I-space addresses at the newly-opened V-addresses) then happens inside `doinsertnd` → `insertmorend` → `insertcbcnd` [`insertnd.c:185–275`], which creates and adopts new bottom crums recording the V→I mapping.

So within the POOM update itself, there is a stack-level intermediate state between `makegappm` completing and `doinsertnd` inserting the new crum. But because no I/O or coroutine switch occurs between them — it is a straight C call chain — this sub-intermediate state is not externally observable at the protocol level.

---

### Step 2: `insertspanf` — spanfilade fill [`spanf1.c:15–54`]

`insertspanf` is called **after** `insertpm` returns. It operates on the global `spanf` (the spanfilade), not on the POOM. It records, for each I-space address range in the `ispanset`, that this document (`docisaptr`) now references that content:

```c
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
// [spanf1.c:51]
```

The spanfilade is a 2D enfilade indexed by `[ORGLRANGE × SPANRANGE]`. The `ORGLRANGE` axis encodes which document/orgl owns the reference; `SPANRANGE` encodes the I-space (content-space) address. This is the structure queried by `finddocscontainingsp` and link-following operations.

`insertspanf` always returns `TRUE` [`spanf1.c:53`] — it cannot fail short of a fatal `gerror`. But structurally it is a separate function call and it runs entirely after the POOM is already updated.

---

### The observable intermediate state

After `insertpm` returns and before `insertspanf` begins, the system is in this state:

| Structure | State |
|-----------|-------|
| **POOM (`orgl`)** | **Updated.** Existing content displaced to new V-addresses. New V→I mapping crum(s) inserted. |
| **Spanfilade (`spanf`)** | **Stale.** Does not yet record that the new I-space addresses belong to this document. |

Concretely:
- A `doretrieve` by V-address would succeed and return correct content (POOM is live).
- A `dofinddocscontaining` by I-address would **not** yet find this document for the newly-copied content (spanfilade not yet updated).
- A `dofollow` traversing links whose endpoints are in the newly-copied I-space would also be incomplete.

This is the intermediate state: the content-subspace positions are already bound in the POOM, but the spanfilade entry that makes those I-space positions discoverable from the inverse direction has not yet been written.

---

### Summary

`docopy` passes through a real intermediate state. The displacement (V-address gap opened in the POOM via `makegappm`) and the POOM fill (new V→I crum inserted via `doinsertnd`) are sub-steps within a single `insertpm` call and are not externally separable. But the POOM update as a whole (`insertpm`) completes as a fully committed unit **before** the spanfilade update (`insertspanf`) begins. There is no rollback, no transaction, no atomicity across the two structures. The two writes are sequential, with the POOM always leading the spanfilade.
