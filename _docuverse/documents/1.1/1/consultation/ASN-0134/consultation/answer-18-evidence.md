## Question 18 [evidence]

> Given the shared grim reaper, can a long `find_links` traversal of the spanfilade evict granfilade or POOM nodes that the same query later needs, and if so does the query still see a consistent snapshot of the I-address set it started intersecting?

## KB Synthesis

## Answer

Yes to both questions, with important qualifications.

---

### Part 1 — Can eviction happen during a single `find_links` call?

Yes. The shared grim reaper is the mechanism, and it is type-blind.

From [SS-CACHE-MECHANISM]: all in-memory crums — GRAN, SPAN, and POOM — participate in a single circular doubly-linked list managed by `grimreaper`. When `ealloc` fails to obtain memory, `grimlyreap()` scans the entire list and frees crums where `age >= OLD` and `age != RESERVED`, regardless of which enfilade type they belong to. [EC-CROSS-ENFILADE-EVICTION] states this explicitly:

> Memory pressure from one subsystem (e.g., a large link search loading many spanfilade crums) can evict modified crums from another subsystem (e.g., recently inserted text atoms).

A large `find_links` traversal loads SPAN crums in bulk via `findcbcinarea2d()` (which walks all siblings left-to-right per [SS-CONTEXT-LIST]). Each new SPAN crum allocation via `ealloc` can trigger `grimlyreap()`, which can then evict GRAN or POOM crums loaded earlier in the same operation.

The only protection against eviction is `age == RESERVED` ([FC-RESERVED-CRUM]). Whether the traversal consistently marks in-use SPAN crums as RESERVED is not resolvable from the KB — but [EC-CROSS-ENFILADE-EVICTION] treats cross-enfilade eviction as a real hazard, not a theoretical one.

---

### Part 2 — Does the query still see a consistent snapshot of the I-address set?

**Logically yes**; the I-address intersection result is not corrupted. Three properties converge to guarantee this:

**a) The I-address set is frozen before the spanfilade search begins.**

`find_links` has two sequential phases: (1) convert the search specset to I-spans via the document's POOM (`specset2ispanset` / `vspanset2sporglset`), then (2) search the spanfilade via `findlinksfromtothreesp`. The I-addresses to intersect are fully materialized as `typesporgl` / `typeispan` structs in heap memory before phase 2 starts. Evicting the POOM crums that were read in phase 1 has no effect on phase 2 — the needed data has already been extracted.

**b) The spanfilade is write-only; evicted SPAN crums can be re-read identically.**

[INV-SPANF-WRITE-ONLY] establishes that no deletion function exists for the spanfilade — its on-disk content is strictly append-only. A SPAN crum evicted during the traversal will have been written to disk with exactly the same data (clean reads are `modified = FALSE`). If the traversal must reload it, the data is bit-for-bit identical. No semantic information is lost.

**c) No concurrent modification is possible.**

[INV-ATOMICITY] and [INV-SEQUENTIAL-DISPATCH] guarantee that the entire `find_links` operation executes as a single uninterruptible run-to-completion step. No other frontend can issue a `create_link` (the only operation that writes to the spanfilade) between any two steps of the traversal. The I-address ↔ link mapping the query is intersecting against cannot change mid-query.

---

### The residual risk: pointer safety, not semantic consistency

The KB does identify one genuine hazard from [SS-CACHE-MECHANISM]: when `grimlyreap()` frees a crum, it calls `subtreefree` and releases the memory. The `findcbcinarea2d()` traversal navigates via `getrightbro` pointers (raw `typecorecrum *` pointers). If a SPAN crum that was already loaded and pointed to by the traversal is evicted before the traversal dereferences that pointer, the result is a dangling pointer — undefined behavior at the C level.

Whether this manifests in practice depends on whether freshly-loaded crums can age to `OLD` within a single operation. The KB does not specify the age-increment schedule precisely, but [EC-CROSS-ENFILADE-EVICTION] treats the hazard as real rather than theoretical.

---

### Summary

| Question | Answer | Key Entries |
|----------|--------|-------------|
| Can a large `find_links` evict GRAN/POOM crums? | Yes | [SS-CACHE-MECHANISM], [EC-CROSS-ENFILADE-EVICTION] |
| Can it evict SPAN crums loaded earlier in the same traversal? | Possibly, depending on age accounting | [SS-CACHE-MECHANISM], [FC-RESERVED-CRUM] |
| Is the I-address intersection logically consistent after eviction? | Yes | [INV-SPANF-WRITE-ONLY], [INV-ATOMICITY], [INV-SEQUENTIAL-DISPATCH] |
| Is pointer safety guaranteed? | Not resolvable from KB | [SS-CACHE-MECHANISM] |

The semantic snapshot is consistent — the spanfilade's write-only, append-only nature combined with single-threaded execution ensures that. The implementation risk is a use-after-free if in-use SPAN crums are evicted before their raw pointers are dereferenced, but that is an implementation-level hazard separate from the logical consistency question.

---

## Code Exploration

Now I have all the pieces. Let me compile the full answer.

---

## The Grim Reaper, `find_links`, and Snapshot Consistency

### 1. The Shared Grim Reaper

Every crum allocated in udanax-green — regardless of which enfilade (granfilade, spanfilade, or POOM/orgl) — is linked into a single global doubly-linked circular list. The list head is `grimreaper`.

**`enf.h:37–41`** (same layout appears in `typecorecrumhedr`, `structcuc`, `structcbc`, `struct2dcbc`):
```c
struct structcorecrumhedr *nextcrum,
             *prevcrum;
                /* doubly linked circular list of */
                /*   all corecrums for grim reaping */
/*SINT*/unsigned char age;         /* for deciding to grimly reap */
```

**`reap.h:11–14`**:
```c
#define RESERVED 0xff     /* keeps a crum from being reaped */
#define NEW 0
#define OLD 1
```

**`credel.c:15–19`**:
```c
typecorecrum *grimreaper;
INT ingrimreaper = FALSE;
INT reaplevel = 0;
```

The grim reaper is triggered from inside `ealloc()` (**`credel.c:70–76`**):
```c
if (grimreaper == NULL) {
    xgrabmorecore();
    continue;
}
grimlyreap();
```

`ealloc()` is called by `createcrum()`, which is called by `varunpackloaf()` when reading a loaf from disk — i.e., from inside `findleftson()` during any enfilade traversal.

**Age is reset by `rejuvinateifnotRESERVED`** (**`common.h:126`**):
```c
#define rejuvinateifnotRESERVED(x) (((x)->age==RESERVED)?(int)(x):((x)->age = NEW))
```

Called on every `getrightbro`, `getleftson`, `findfather`, etc. in `genf.c`.

**Age is incremented inside `grimlyreap()`** when a candidate is not yet reapable (**`credel.c:158–159`**):
```c
++reapnumber;
grimreaper->age++;
```

So the story is: touching a node resets its age to NEW (0). A node that has not been touched through several `grimlyreap()` passes ages past OLD (1) and becomes eligible for eviction.

---

### 2. The `find_links` Call Chain

```
fns.c:198          findlinksfromtothree()
do1.c:348          dofindlinksfromtothree()   → findlinksfromtothreesp(spanf, ...)
spanf1.c:56        findlinksfromtothreesp()
```

**`spanf1.c:70–100`** (full function body, condensed):
```c
// PHASE 1: Convert each vspecset to an I-space sporglset
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (tovspecset)
    specset2sporglset(taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);
if (threevspecset)
    specset2sporglset(taskptr, threevspecset, &threesporglset, NOBERTREQUIRED);

// PHASE 2: For each endpoint, traverse the spanfilade
if (fromvspecset)
    sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset,
                      orglrange, LINKFROMSPAN);
if (tovspecset)
    sporglset2linkset(taskptr, (typecuc*)spanfptr, tosporglset, &tolinkset,
                      orglrange, LINKTOSPAN);
if (threevspecset)
    sporglset2linkset(taskptr, (typecuc*)spanfptr, threesporglset, &threelinkset,
                      orglrange, LINKTHREESPAN);

// PHASE 3: Intersect
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

`sporglset2linksetinrange()` (**`sporgl.c:239–269`**) queries the spanfilade via:
```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                              &range, ORGLRANGE, (typeisa*)infoptr);
```

Which goes: `retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` (**`retrie.c:229–268`**), a recursive DFS over the spanfilade.

---

### 3. Where the Grim Reaper Fires During Traversal

Inside `findcbcinarea2d`:
```c
// retrie.c:259
findcbcinarea2d(findleftson((typecuc*)crumptr), &localoffset, ...);
```

`findleftson()` (**`genf.c:206–232`**) is the trigger:
```c
typecuc *findleftson(register typecuc *ptr)
{
    if (ptr->leftson == NULL) {
        if (ptr->sonorigin.diskblocknumber == DISKPTRNULL) return(NULL);
        reserve((typecorecrum*)ptr);             // line 216
        inloaf(ptr);                             // line 225 → varunpackloaf → createcrum × N
        if (oldage != RESERVED)                  // line 227 ("zzz experimental")
            rejuvinate((typecorecrum*)ptr);       // line 228
    }
    rejuvinateifnotRESERVED(ptr->leftson);
    return(ptr->leftson);
}
```

Each `createcrum()` call inside `varunpackloaf()` (**`corediskin.c:117`**) can trigger `ealloc()` → `grimlyreap()`. For a large node with many sons, this fires repeatedly per `findleftson()` call.

---

### 4. Can Granfilade / POOM Nodes Be Evicted?

**Yes.** `grimlyreap()` walks the single shared circular list. It does not distinguish node types. From **`credel.c:127–161`**:
```c
for (ptr = grimreaper; grimreaper; grimreaper = (typecorecrum *)grimreaper->nextcrum) {
    if (grimreaper->age == RESERVED) { continue; }
    if (isreapable(&eh, grimreaper)) {
        reap(grimreaper);
        break;
    }
    grimreaper->age++;
}
```

A POOM apex loaded by `specset2sporglset()` is particularly vulnerable. `inorglinternal()` (**`corediskin.c:171–231`**) loads only the apex crum; it sets `sonorigin` but leaves `leftson = NULL`. The sons remain on disk.

`isreapable()` for an apex (**`credel.c:181–225`**) is:
```c
if (localreaper->isapex) {
    if (localreaper->cenftype != POOM) { return(FALSE); }
    for (p = ((typecuc *)localreaper)->leftson; p; p = p->rightbro) {
        // checks each son...
    }
    return(TRUE);  // TRUE if leftson == NULL — loop body never executes!
}
```

**A POOM apex with `leftson == NULL` (no in-core sons) satisfies `isreapable()` immediately once its age reaches OLD.** During a long spanfilade traversal with heavy disk loading, the POOM apexes loaded by `specset2sporglset()` can age past OLD and be reaped.

When reaped (**`credel.c:302–316`**):
```c
if (localreaper->isapex) {
    temp = (typecuc *)localreaper->leftbroorfather;
    grimreaper = grimreaper->nextcrum;
    if (!temp) { return(0); }
    orglwrite((typecbc*)temp);   // writes apex to disk, marks orglincore=FALSE
    return(0);
}
```

The POOM tree is written out and the owning granfilade crum's `orglincore` is set to FALSE. The POOM apex crum is freed from the shared pool.

---

### 5. Does the Query Still See a Consistent I-Address Set?

**Yes — and this is the key point.** The I-address set (the sporglset) is not in crum memory at all.

`specset2sporglset()` produces sporglset entries via **`taskalloc()`**, which allocates from the per-request task pool (**`sporgl.c:249`**):
```c
sporglset = (typesporgl*) taskalloc(taskptr, sizeof(typesporgl));
```

Task-allocated memory is freed by `tfree(taskptr)` at request end (**`bed.c:168`**). It is never touched by `grimlyreap()`, which only operates on crums allocated via `ealloc()`/`falloc()`.

So:
- **Phase 1** (`specset2sporglset` × 3): accesses granfilade/POOM to convert V-space specs into I-space tumblers. Results — stream + width tumblers — are **copied into task memory** as `typesporgl` structures.
- **Phase 2** (`sporglset2linkset` × up to 3): uses those task-allocated sporglsets as **input span constraints** for the spanfilade query. **Does not access the granfilade or POOM at all.** The ORGLRANGE restriction (`range`) is a precomputed span value, not a traversal of the orgl tree.
- **Phase 3** (`intersectlinksets`): operates entirely on extracted link ISAs in task memory.

Even if every POOM apex loaded in Phase 1 is reaped during Phase 2, the sporglset members in task memory are unaffected. The I-address set the query sees in the intersection is exactly the set that was computed at the end of Phase 1.

---

### 6. Spanfilade Self-Consistency During Traversal

The more subtle half of the question: can the grim reaper evict spanfilade nodes that the ongoing traversal will revisit?

**Three protections are in place, together sufficient:**

#### Protection A: `reserve()` during disk load

When `findleftson()` needs to load from disk (**`genf.c:216`**):
```c
reserve((typecorecrum*)ptr);
inloaf(ptr);
```

`reserve()` sets `ptr->age = RESERVED (0xff)`. Inside `grimlyreap()`:
```c
if (grimreaper->age == RESERVED) { continue; }
```

The node being loaded-into is skipped by the reaper for the duration of `inloaf()`. After loading, `rejuvinate()` sets it back to NEW. The father cannot be evicted while we are filling its sons.

#### Protection B: `leftson != NULL` propagates immunity upward

`isreapable()` for any non-apex, non-leaf node checks all siblings (**`credel.c:269`**):
```c
if (p->height > 0 && ((typecuc *)p)->leftson) {
    return(FALSE);  // can't reap a family if any sibling has in-core sons
}
```

Once `findleftson()` sets a node's `leftson` field (loading from disk or returning in-core pointer), that node's parent's sibling group cannot be reaped — because one of the siblings (the father) has `leftson != NULL`. This protection cascades upward: the father's father's sibling group is similarly blocked if the father has `leftson != NULL`.

The entire DFS ancestor path from the current node up to the root is protected by this invariant, not by RESERVED marks. No ancestor on the active traversal stack can be reaped while we are inside its subtree.

#### Protection C: Sibling rejuvenation prevents whole-family reaping

`isreapable()` requires ALL siblings in a family to be OLD (**`credel.c:250–253`**):
```c
for (p = weakfindleftmostbro(localreaper); p; p = p->rightbro) {
    if (p->age < OLD || p->age == RESERVED) { return(FALSE); }
    ...
}
```

Every sibling visited by `getrightbro()` in the DFS rightbro-walk is rejuvenated to NEW by `routinegetrightbro()` (**`genf.c:36–40`**). A NEW (age=0) sibling makes the whole family non-reapable. So no family whose siblings the traversal has recently visited can be evicted.

---

### 7. No Snapshot, But Consistent Reload

There is no snapshot or copy-on-write mechanism. The traversal reads the live spanfilade. Writes go through the `modified` flag and are flushed by `diskflush()` between requests (**`bed.c:105,134`**). Since the backend processes one request at a time per connection (the `select()`-based event loop in **`bed.c:103–149`** calls `xanadu()` once per connection turn), there is no concurrent mutation of the spanfilade during a single query.

When the grim reaper evicts a node, it first writes it to disk (`subtreewrite` or `orglwrite`), then frees the crum. If the traversal later needs those crums again (unlikely for the POOM case), `findleftson()` reloads them from disk and gets exactly what was written — a consistent image.

---

### Summary

| Question | Answer |
|----------|--------|
| Can a long spanfilade traversal trigger grim reaper eviction of POOM/granfilade nodes? | **Yes.** POOM apex crums with `leftson == NULL` satisfy `isreapable()` immediately once OLD. A long traversal fires `createcrum()` → `ealloc()` → `grimlyreap()` repeatedly. |
| Do evicted POOM/granfilade nodes corrupt the I-address set? | **No.** The sporglsets (I-space spans) are extracted into task-allocated memory before the spanfilade traversal begins. Task memory is immune to the grim reaper. |
| Does the query see a consistent I-address snapshot? | **Yes, vacuously.** The I-address set is fixed in task memory by the time any spanfilade traversal can trigger eviction. There is nothing to become inconsistent. |
| Can the traversal evict spanfilade nodes it still needs? | **No**, for nodes on the active DFS path. Three invariants protect them: `reserve()` during disk load (`genf.c:216`), `leftson != NULL` blocking family reaping (`credel.c:269`), and sibling rejuvenation breaking family-OLD conditions (`credel.c:250–253`). |
| Is there a snapshot or versioning mechanism? | **No.** The system is single-threaded per request; the grim reaper writes before freeing; reloads are consistent. |

The one genuine hazard — a use-after-free on sibling pointers already advanced past in the rightbro walk — is averted by Protection C: any recently-visited sibling (age=NEW) prevents the grim reaper from evicting the whole sibling family, since `isreapable()` requires ALL siblings to be OLD.
