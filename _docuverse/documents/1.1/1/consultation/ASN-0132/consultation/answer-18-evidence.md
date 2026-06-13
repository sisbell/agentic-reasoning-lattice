## Question 18 [evidence]

> Are the four query sets resolved from V-spans to I-spans against the POOM state at the instant of the call, so that an earlier INSERT or DELETE in the querying document changes which I-addresses are searched — and does a REARRANGE, which preserves I-addresses while moving V-positions, leave the count for an I-equivalent query unchanged?

## KB Synthesis

Yes, yes, and yes — with some precision needed on what "I-equivalent" means for REARRANGE. Here is the full synthesis.

---

## V-to-I Resolution Is Against POOM State at Call Time

The conversion from V-spans to I-addresses for all query operations goes through the live POOM. [ST-VSPAN-TO-SPORGL] states explicitly: "This conversion is a pure function over the document's current V→I mapping — it reads the enfilade but does not modify it." [SS-FIND-LINKS] (Finding 0028) confirms: "The search specset is converted to I-addresses" at the moment of the call. [SS-RETRIEVE-ENDSETS] (Finding 0035) shows the same: `retrieveendsetsfromspanf` calls `specset2sporglset` (V-to-I translation) as its first step before searching the spanfilade.

There is no cached or snapshotted I-address set for a specset. Every query resolves V-spans freshly against the current POOM tree.

---

## INSERT Changes Which I-Addresses Are Searched

[ST-INSERT] (Finding 0030) gives the precise postcondition: INSERT at V-position `p` of length `n` produces `D'(v) = D(v)` for `v < p`, `D'(v) = fresh_iaddr(v)` for `p ≤ v < p+n`, and `D'(v-n) = D(v)` for `v ≥ p+n`. The POOM is modified in-place [SS-POOM-MUTABILITY].

Consequences for a subsequent query using the same absolute V-span coordinates:

- **Before insertion point**: same content, same I-addresses resolved — no change.
- **At/after insertion point**: V-positions have shifted by `n`. The same absolute V-span now covers different content (and thus different I-addresses).
- **Spans covering the insertion gap**: now include the fresh I-addresses allocated for the inserted text, which were not in the spanfilade link index prior to the insert (unless the insert itself created discoverable links).

[FC-INSERT-IADDR] frames the frame condition: existing I-addresses in other documents are invariant, but within the querying document, which I-addresses map to which V-positions has changed. Since `find_links` resolves through the POOM at call time, the I-address set that gets searched changes.

---

## DELETE Changes Which I-Addresses Are Searched

[ST-DELETE] (Finding 0057, 0064) confirms DELETE removes V-to-I mappings from the POOM exclusively, without touching the spanfilade. After DELETE, a V-span query that previously resolved to I-addresses covering deleted content will now either:

- Return fewer I-addresses (if the deletion was partial), or
- Return no I-addresses (if the entire queried region was deleted).

The spanfilade entries remain [INV-SPANF-WRITE-ONLY], so the link index itself is unchanged — what changes is that the V-span no longer resolves to those I-addresses, so the intersection in `findlinksfromtothreesp` is empty. This is the mechanism documented in [SS-FIND-LINKS] (Finding 0029): `find_links` after source deletion returns empty not because the link was removed, but because the V-to-I conversion produces no I-addresses to intersect with.

---

## REARRANGE and I-Equivalent Queries

[INV-REARRANGE-IDENTITY] (Findings 0016, 0018, 0056) establishes that REARRANGE modifies only `ptr->cdsp.dsas[V]` — the V-address displacement. I-addresses are never touched. The multiset of I-addresses in the document is identical before and after.

[ST-REARRANGE] (Finding 0056) shows the mechanism: `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], ...)` adjusts V-position; I-position is a separate field untouched.

For a query that is "I-equivalent" — meaning the caller uses the *updated* V-spans that track the moved content to its new V-positions — the resolved I-addresses are the same as before REARRANGE. Since the spanfilade is also unchanged, `find_links` returns the same set of links, and the count is identical.

However, the same *absolute* V-span coordinates will now point to different content (content that was displaced into those positions by the rearrangement). That query is not I-equivalent — it will return different results.

[INT-LINK-INSERT] (Finding 0030) makes this explicit for the link case: "Links attached to content via I-addresses survive insertion because I-addresses are immutable. The V-address interpretation of the link shifts, but the link itself references I-addresses and needs no update." The same logic applies to REARRANGE. [INV-REARRANGE-LINK-SURVIVAL] confirms: "Because links are bound to I-addresses (not V-addresses), moving content to new V-positions does not break link bindings."

---

## Summary

| Operation | POOM change | Spanfilade change | Same absolute V-span query | I-equivalent V-span query |
|-----------|-------------|-------------------|---------------------------|--------------------------|
| INSERT | Yes — new mappings, shifted positions | Append-only (new DOCISPAN) | Different I-addresses resolved | N/A (new content added) |
| DELETE | Yes — mappings removed | None (stale entries persist) | Fewer I-addresses resolved | Query would need to omit deleted range |
| REARRANGE | Yes — V-positions shifted, I-addresses unchanged | None | Different content at same coords | Same I-addresses → same count |

The invariant underlying all three cases is [INV-IADDR-IMMUTABILITY]: once allocated, I-addresses never change. What changes is the V→I mapping (POOM), which determines what a V-span query resolves to at any given instant. The spanfilade link index is append-only [INV-SPANF-WRITE-ONLY], so the link associations by I-address are permanent — only the V-span→I-address gateway varies.

---

## Code Exploration

I now have a complete picture of the full call chain. Let me write the answer.

---

## Answer

### The Four Query Sets and V→I Resolution

The query-facing functions are `findlinksfromtothreesp` (`spanf1.c:56`) and `findnumoflinksfromtothreesp` (`spanf1.c:105`). They receive four specsets: `fromvspecset`, `tovspecset`, `threevspecset` (each typed `typespecset`, i.e. V-spec or I-span), and `orglrange` (typed `typeispan *`, already an I-span). The first three go through V→I conversion; the fourth is already in I-space.

---

### 1. Is V→I Resolution Against POOM State at the Instant of the Call?

**Yes — unconditionally.**

The conversion path for each V-specset is:

```
findlinksfromtothreesp (spanf1.c:71–75)
  → specset2sporglset (sporgl.c:14)
      for VSPECID items → vspanset2sporglset (sporgl.c:35)
          → findorgl(taskptr, granf, docisa, &orgl, type)   [sporgl.c:44]
          → vspanset2ispanset(taskptr, orgl, vspanset, &ispanset)  [sporgl.c:48]
```

The critical line is `sporgl.c:44`:
```c
if (!findorgl (taskptr, granf, docisa, &orgl, type)) {
    return (NULL);
}
```

`findorgl` does a **live lookup** in the granfilade — it fetches the POOM node currently registered for `docisa`. There is no snapshot, no cache, no pre-resolved handle. The `orgl` returned is the POOM as it exists at this moment in memory.

`vspanset2ispanset` (`orglinks.c:397`) then calls `permute(taskptr, orgl, vspanptr, V, ispansetptr, I)` (`orglinks.c:401`), which calls `span2spanset` → `retrieverestricted` (`retrie.c:56`) on the live POOM tree. Every V-span is permuted to I-spans by walking the POOM as it currently stands.

---

### 2. Does an Earlier INSERT or DELETE Change Which I-Addresses Are Searched?

**Yes.**

**INSERT** path (`fns.c:84–98` → `do1.c:87–123`):
```
doinsert → docopy → insertpm → insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V)
```
`insertpm` (`orglinks.c:75–134`) adds new 2D crums to the POOM at the specified V-coordinate, each crum encoding a V↔I mapping. After this call the POOM has new V→I entries.

**DELETE** path (`fns.c:333–347` → `do1.c:158–167`):
```
dodeletevspan → deletevspanpm → deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V)
```
`deletend` (`edit.c:31–76`) removes crums in the named V-range and adjusts remaining crum displacements at `edit.c:63`:
```c
tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```
This shifts all V-coordinates above the deleted span downward, so V-positions of surviving content change.

Because FEBE requests are processed serially (the `select` event loop in `bed.c`), each INSERT or DELETE completes fully before the next request is dispatched. When a subsequent FIND query reaches `vspanset2sporglset`, `findorgl` returns the already-mutated POOM. A V-span that used to map to I-address set A may now map to a completely different I-address set B (or nothing), depending on what was inserted or deleted before the query.

---

### 3. Does a REARRANGE Leave the Count for an I-Equivalent Query Unchanged?

**Yes — the I-equivalent query is invariant.**

`dorearrange` (`do1.c:34–43`) calls `rearrangepm` (`orglinks.c:137–142`) which calls:
```c
rearrangend((typecuc*)docorgl, cutseqptr, V);   /* orglinks.c:139 */
```

Inside `rearrangend` (`edit.c:78–160`), the only mutation to crum data is on line `edit.c:125`:
```c
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```
where `index = V` (passed from `rearrangepm` as `V`). The expression `ptr->cdsp.dsas[V]` is the V-displacement of the crum. The I-displacement, `ptr->cdsp.dsas[I]`, is **never touched**. The I-address fabric of the POOM is intact after a rearrange.

Furthermore, `rearrangend` makes no call to `insertspanf` or any spanfilade mutator — the spanfilade (which indexes link endpoints by I-address) is completely unaffected.

Now trace what happens on a subsequent query expressed as I-spans (ISPANID items in the specset). In `specset2sporglset` (`sporgl.c:14–33`):
```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *sporglsetptr = (typesporglset)specset;          /* sporgl.c:21 */
    sporglsetptr = (typesporglset *)&((typeitemheader *)specset)->next;
}
```
The I-span is passed straight through — no POOM lookup at all. In `sporglset2linksetinrange` (`sporgl.c:239–268`) the I-span is handed directly to `retrieverestricted` against the spanfilade. Since the spanfilade was not modified, and the I-addresses themselves were not modified, `retrieverestricted` returns the same set of link-orgl contexts it would have returned before the rearrange, and the count is unchanged.

**Contrast with the same V-span query after a rearrange.** The same V-span now resolves through the mutated POOM to a different I-span set (content formerly at position 3 may now be at position 7, etc.), so the count for that V-spec query can differ. Only the I-equivalent formulation is stable.

---

### Summary Table

| Operation on doc | Effect on POOM `cdsp.dsas[V]` | Effect on POOM `cdsp.dsas[I]` | Effect on spanfilade | V-spec query count | I-spec query count |
|---|---|---|---|---|---|
| INSERT | new crums added at V-position | new I-addresses mapped in | new entries added | can change | can change (new I-addrs) |
| DELETE | crums removed; remaining V-coords shift | I-addresses of removed content gone | unchanged | can change | can change |
| REARRANGE | V-coords of existing crums shifted | **unchanged** | **unchanged** | can change | **unchanged** |

The V→I resolution always reads the live POOM (`findorgl` + `retrieverestricted` on the current tree at `sporgl.c:44` and `orglinks.c:435`). A rearrange only writes `cdsp.dsas[V]` (`edit.c:125`), leaving both `cdsp.dsas[I]` and the spanfilade untouched, so any query stated directly in I-coordinates returns the same link count before and after the rearrange.
