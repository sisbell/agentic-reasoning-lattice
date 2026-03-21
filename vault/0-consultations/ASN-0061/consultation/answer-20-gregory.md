## Question 20 [gregory]

> After DELETE creates unreachable I-addresses (content present in granfilade but referenced by no POOM), is there any operation or query path in the backend that can enumerate these orphaned I-address ranges, or are they permanently invisible unless their addresses are already known from a prior retrieval?

## KB Synthesis

Orphaned I-address ranges are permanently invisible through any described public operation unless their addresses are already known from a prior retrieval.

**Why there is no enumeration path:**

The granfilade is append-only and contains all I-addresses ever allocated [INV-MONOTONIC, FC-GRANF-ON-DELETE]. But there is no described FEBE operation that traverses or enumerates granfilade content by I-address. All retrieval paths require either a starting V-address (which orphaned content lacks) or an I-address you already possess.

The three public query mechanisms all fail to surface orphaned I-addresses:

1. **V-space queries** (`RETRIEVEDOCVSPAN`, `RETRIEVEDOCVSPANSET`, `RETRIEVE_CONTENTS`): These operate through the POOM — they return only content with current V→I mappings. DELETE removes those mappings, so orphaned I-addresses have no V-position and are structurally invisible [ST-DELETE, Finding 0064].

2. **`FINDDOCSCONTAINING`**: Requires a known I-address as input. It searches the spanfilade, which remains stale after DELETE [INV-SPANF-WRITE-ONLY, EC-STALE-SPANF-REFERENCE] — it can confirm that a *known* I-address was once in a document, but provides no mechanism to discover *which* I-addresses are now orphaned.

3. **Link operations** (`FOLLOWLINK`, `RETRIEVEENDSETS`): These perform I→V conversion, which silently drops unreferenced I-addresses without error [INV-ITOV-FILTERING]. Empty endsets signal orphaning but only for I-addresses already known via the link's endset structure [EC-GHOST-LINK].

**The one detection path — not enumeration:**

If you hold a link whose endpoint I-addresses were deleted, `FOLLOWLINK` returning `[]` with `works: true` tells you those specific I-addresses are now orphaned [EC-GHOST-LINK, EC-ORPHANED-LINK]. But this detects orphaning of *known* I-addresses; it does not enumerate unknown ones.

**Why the stale spanfilade doesn't help:**

The post-DELETE spanfilade state satisfies `actual_docs(i) ⊆ find_documents(i)`, not equality [EC-STALE-SPANF-REFERENCE]. Even if you probed `FINDDOCSCONTAINING` for a range, you'd get a superset of current references — and you'd still need to already know which I-address to probe.

**Bottom line:** The architecture has no "scan orphaned I-addresses" operation. The internal `findpreviousisagr` function used by the allocator traverses the granfilade tree to find the maximum I-address, but it is not exposed as a FEBE operation and operates within a bounded document address range, not across all orphaned content. Any orphaned I-address range is recoverable only if its address was captured before deletion — for example, stored in a link endset, recorded by the client, or derivable from the monotonic allocation sequence of a known document.

---

## Code Exploration

Now I have a complete picture. Here is the full analysis:

---

## Answer: Orphaned I-Addresses After DELETE Are Permanently Invisible

### 1. What DELETE Actually Does

The delete path is:

`deletevspan` (`fns.c:333-347`) → `dodeletevspan` (`do1.c:158-167`) → `deletevspanpm` (`orglinks.c:145-152`) → `deletend` (`edit.c:31-76`)

`dodeletevspan` [do1.c:163-166]:
```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
);
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

`deletend` [edit.c:31-76] removes POOM crums in the deleted V-range:
- `case 1:` → `disown` + `subtreefree` — POOM crum is freed
- `case 2:` → `tumblersub` on `cdsp.dsas[index]` — POOM crum is displaced

**Three crucial omissions:**
1. The granfilade (`granf`) is never touched. Content at those I-addresses stays in place.
2. The spanfilade (`spanf`) is never touched. The I→document entries inserted by the original `insertspanf` call remain.
3. `deleteversion` [bert.c:348-353] is a **stub** — the function body contains only a debug `fprintf` and no logic whatsoever.

---

### 2. What the Granfilade Holds

When content is inserted via `doinsert` [do1.c:87-123]:
```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
);
```

`inserttextgr` [granf2.c:83-109] allocates a new I-address (`findisatoinsertgr`), writes bytes via `insertseq`, and returns the resulting ispan. This content is written once and never removed by any operation in the codebase.

`docopy` [do1.c:45-65] then calls both:
```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)    /* POOM */
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN) /* SPANFILADE */
```

After DELETE only modifies the POOM, the granfilade byte content and the spanfilade I→doc association both survive.

---

### 3. The Complete FEBE Query Surface

Every exposed operation in `fns.c` falls into one of two categories:

**V-address-in, content-out** (blocked by missing POOM entry):

| Operation | Path | Blocked? |
|-----------|------|---------|
| `retrievev` | V-specset → `specset2ispanset` → POOM → I-spans → granfilade | **Yes** — POOM entry removed |
| `retrievedocvspan` / `retrievedocvspanset` | Returns POOM root crum `cdsp.dsas[V]` / `cwid.dsas[V]` | Shows only what POOM still holds |
| `copy` | V-specset → I-spans → new POOM entry | **Yes** — can't copy what you can't address |
| `rearrange` | V-address cuts → POOM rearrangement | Operates only on POOM |

**I-address-in or link-in** (not enumeration):

| Operation | Path | Can it find orphans? |
|-----------|------|---------------------|
| `finddocscontaining` [do1.c:15-23] | I-spans (provided by caller) → SPANFILADE → doc ISAs | **No** — caller must already know the I-spans |
| `findlinksfromtothree` [do1.c:348-353] | V-specset → I-spans → SPANFILADE → link ISAs | **No** — still requires V-addresses |
| `followlink` [do1.c:223-232] | Link ISA → link endpoint specsets | **No** — requires knowing the link |
| `retrieveendsets` | Link specset → SPANFILADE endpoint sets | **No** — requires knowing the link |
| `showrelationof2versions` | V-specsets → I-span intersection | **No** — still V-in |

There is no FEBE operation that takes an I-span range as *primary* input for open-ended enumeration, nor any operation that traverses the granfilade or spanfilade from their roots to enumerate all stored ranges.

---

### 4. Internal Functions That Could Enumerate — But Are Not Exposed

The granfilade traversal machinery exists internally:

- `retrieveinspan` [retrie.c:112-136]: scans all leaf crums in a given I-span range via `findcbcinspanseq`. Could, in principle, enumerate all content in the granfilade given `spanstart=0` and `spanend=∞`. **Not exposed via any `do*` function or FEBE handler.**

- `findlastcbcseq` [retrie.c:138-158]: walks the rightmost chain to find the maximum I-address. **Not exposed.**

- `ispan2vstuffset` [granf2.c:286-318]: retrieves content for a specific I-span by calling `retrieveinspan`. Only called from `ispanset2vstuffset` [granf1.c:58-74], which is only called from `doretrievev`, which gets its I-spans from the POOM. The chain is V→POOM→I→granfilade with no external I-span entry point.

- `isaexistsgr` [granf2.c:244-253]: can verify whether a *specific* I-address exists in the granfilade. Only called by `findisatoinsertgr` during new-address allocation. Not called from any query path.

---

### 5. The Spanfilade Is Also a Dead End

Even though `dodeletevspan` does not clean up the spanfilade, the spanfilade provides no enumeration escape hatch:

`finddocscontaining` [spanf1.c:151-188] issues a `retrieverestricted` call against the spanfilade:
```c
context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                               ispanset, SPANRANGE, (typeisa*)NULL);
```
The `ispanset` (SPANRANGE restriction) must be supplied by the caller. It cannot be null — passing `NULL` for `span1ptr` in `retrieverestricted` [retrie.c:56-85] replaces it with a zero-tumbler pair `{0,0}`, which matches nothing.

There is no "scan all SPANRANGE entries" operation exposed to the FEBE client.

---

### 6. Conclusion

After `dodeletevspan` removes the V→I mapping from the POOM:

- The granfilade retains the byte content at those I-addresses permanently. Nothing removes granfilade entries. `deleteversion` [bert.c:348-353] is an empty stub.
- The spanfilade retains the I→document associations from the original `insertspanf` call, but this information is also unreachable — there is no way to enumerate which I-spans are recorded without already knowing the I-spans.
- **Every read path is top-down from V-addresses through the POOM.** The POOM is the only directory of what content is addressable. Once a POOM crum is removed by `deletend`, the I-addresses it mapped become invisible.
- **No FEBE operation enumerates I-addresses bottom-up from the granfilade or spanfilade.**

The orphaned I-address ranges are **permanently invisible unless already known from a prior retrieval**. The content occupies granfilade space indefinitely with no garbage collection path and no client-accessible enumeration mechanism.
