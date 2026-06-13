## Question 17 [evidence]

> After the original link's POOM entry is removed from the link subspace (reverse-orphaning it), what is required to resolve the original link orgl by its ISA — is resolution purely a granfilade lookup, or does it depend on a surviving POOM entry or a BERT-opened home document?

## KB Synthesis

## Link Orgl Resolution by ISA: Granfilade Lookup Only

Resolution of a link orgl by its ISA is a **pure granfilade B-tree lookup**, independent of any surviving POOM entry and independent of whether the home document is BERT-opened.

### The Two-Phase Architecture

FOLLOWLINK splits into two completely decoupled phases [SS-FOLLOWLINK]:

**Phase 1 — Orgl lookup:**
`link2sporglset()` at `sporgl.c:67-95` calls `retrieverestricted()` on the granfilade with the link ISA as the address range. This is a direct B-tree traversal of I-space with no open-list check and no POOM involvement. The precondition is solely that the link orgl exists in the granfilade at that ISA [PRE-FOLLOWLINK].

**Phase 2 — Endpoint V-address resolution:**
`linksporglset2specset()` converts the endset I-addresses to V-spans by traversing the specified `homedoc`'s POOM. This phase CAN return empty or partial results if the endset I-addresses have no current POOM mapping, but failure here does not affect Phase 1.

### Why Neither POOM Entry Nor BERT Matters for Phase 1

**POOM entry:** The link orgl at ISA `d.0.2.N` lives in I-space (the granfilade), not in the document's POOM [SS-THREE-LAYER-MODEL]. Removing the POOM entry at V-position `2.x` via DELETEVSPAN severs the document-level reference but leaves the link orgl completely intact in I-space. This is exactly the reverse-orphan state [EC-REVERSE-ORPHAN]: `follow_link(link_id, SOURCE)` continues to work after DELETEVSPAN.

**BERT / home document open:** The `findorgl()` call at `sporgl.c:76-78` checks only that the link orgl exists in the granfilade. Link orgls are sub-objects under a document's address, but the retrieval uses the granfilade B-tree directly — the BERT open-list check (which applies to `findorgl(..., READBERT/WRITEBERT)` for document content retrieval) is not triggered here. Internal lookups bypass BERT via NOBERTREQUIRED [SS-BERT]. This is consistent with [SS-DOCUMENT-LIFECYCLE]: operations working through I-address lookup do not require the referenced document to be open.

### Permanence Guarantee

Link orgls are unconditionally permanent in the granfilade [INV-LINK-PERMANENCE]. No DELETELINK operation exists. Once allocated, the ISA maps to the link orgl forever via the append-only granfilade [INV-IADDR-IMMUTABILITY]. This means Phase 1 succeeds for any validly-created link ISA, regardless of what has been done to the home document's POOM or BERT state.

### What Does Depend on Home Document State

The only aspect of link traversal that requires home-document accessibility is Phase 2's `linksporglset2specset()`. If endset I-addresses have no POOM mapping in the queried document (e.g., after content deletion), the I-addresses are silently dropped and the result is empty — the "ghost link" case [EC-GHOST-LINK]. But this silent filtering [INV-ITOV-FILTERING] is a POOM-layer concern in Phase 2, not a granfilade-layer concern in Phase 1.

**Summary:** ISA resolution is Phase 1 only — a granfilade range query, succeeding by permanence, requiring neither POOM nor BERT.

---

## Code Exploration

I now have the complete picture across all relevant subsystems. Here is the full analysis.

---

## Link Orgl Resolution After POOM Entry Removal

### The Two-Gate Architecture of `findorgl`

Every call to resolve a link's orgl by ISA goes through `findorgl` [granf1.c:17–41]:

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
  if (/*backenddaemon &&*/(temp = checkforopen(isaptr, type, user)) <= 0) {
    if (!isxumain) {
      return FALSE;   // or *orglptr = NULL; return FALSE in DISTRIBUTION
    }
  }
  *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
  return (*orglptr ? TRUE : FALSE);
}
```

Two sequential gates:

1. **Gate 1 — BERT** (`checkforopen`, bert.c:52): checks the link's own ISA in the berttable
2. **Gate 2 — Granfilade** (`fetchorglgr`, granf2.c:22): descends the granfilade by ISA

These are independent. The POOM and the home document have no role in either.

---

### Gate 1: The BERT Check Is on the Link's Own ISA

`checkforopen(isaptr, type, user)` [bert.c:52–87] takes the **link's ISA tumbler** and searches the in-memory berttable:

```c
for (p = berttable[hashoftumbler(tp)]; p && p->stuff; p = p->next) {
    bert = p->stuff;
    if (tumblereq(tp, &bert->documentid)) { ... }
}
```

It looks up the **link's own ISA**, not the home document's ISA. The home document's BERT state is irrelevant here. The search is keyed by tumbler hash against `bert->documentid` [bert.c:65].

Return values:
- `> 0` (READBERT or WRITEBERT): sufficient open found for this connection → continue
- `0`: no open found, but user owns it or only READBERT needed → continues if `isxumain`
- `-1`: conflicting open or insufficient ownership → blocked unless `isxumain`

**`isxumain` controls the failure path.** Three binaries compile this:
- `bed.c:35`: `bool isxumain = FALSE;` — network daemon
- `be.c:29`: `bool isxumain = FALSE;` — test backend
- `xumain.c:23`: `bool isxumain = TRUE;` — standalone interpreter

When `isxumain = FALSE` (both production modes), BERT failure (`checkforopen` ≤ 0) returns FALSE before `fetchorglgr` is ever called.

**However**: the `type` parameter gates this entirely. `NOBERTREQUIRED` [bert.c:59–61]:

```c
if (type == NOBERTREQUIRED) {
    return 1;   /* Random > 0 */
}
```

This returns immediately without searching the berttable at all. The operationally significant callers pass `NOBERTREQUIRED`:

- `dofollowlink` → `link2sporglset(taskptr, linkisa, ..., NOBERTREQUIRED)` → `findorgl(..., NOBERTREQUIRED)` [sporgl.c:75, do1.c:229]
- `docreatelink` → `findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)` [do1.c:213]
- `docopyinternal` → `findorgl(taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)` [do1.c:75]

The comment at do1.c:213 makes the intent explicit: `/*WRITEBERT ECH 7-1*/NOBERTREQUIRED` — the original WRITEBERT was replaced by NOBERTREQUIRED. Link creation and link following both bypass the BERT gate entirely.

**The BERT check does NOT require an opened home document.** It requires at most that the link's own ISA appear in the berttable, and even that requirement is bypassed by `NOBERTREQUIRED`.

---

### Gate 2: `fetchorglgr` Is a Pure Granfilade Lookup

`fetchorglgr` [granf2.c:22–77] receives the global `granf` enfilade root and the link's ISA:

```c
typeorgl fetchorglgr(typetask *taskptr, typegranf fullcrumptr, typeisa *address)
{
    // 1. Bounds check
    if (tumblercmp (&((typecuc*)fullcrumptr)->cwid.dsas[WIDTH], address) == LESS)
        return (NULL);

    // 2. Descend the granfilade by WIDTH index
    if ((context = retrievecrums((typecuc*)fullcrumptr, address, WIDTH)) == NULL)
        return NULL;

    // 3. Exact tumbler equality test
    if (!tumblereq((tumbler*)&context->totaloffset, address)) {
        crumcontextfree(context);
        return (NULL);
    }

    // 4. Load from disk if needed
    if (!context->corecrum->cinfo.granstuff.orglstuff.orglincore) {
        inorgl(context->corecrum);
    }

    // 5. Return orglptr
    ret = context->corecrum->cinfo.granstuff.orglstuff.orglptr;
    ...
    return ((typeorgl)ret);
}
```

`retrievecrums` [retrie.c:15–31] calls `findcbcseqcrum` [retrie.c:167–189], which is a recursive descent of the GRAN enfilade by WIDTH address — a pure tree traversal over the granfilade's own structure. No POOM, no home document, no spanfilade.

The granfilade is a **separate global enfilade** from any document's POOM. It stores one GRANORGL crum per document/link ISA, created by `createorglgr` [granf2.c:106–121]:

```c
bool createorglgr(...) {
    ...
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf(POOM);   // creates the link's own POOM
    locinfo.granstuff.orglstuff.orglincore = TRUE;
    locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
    insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);       // inserts into granfilade
    ...
}
```

This `insertseq` into `fullcrumptr` (the granfilade) is **not** `insertnd` into any document POOM. The granfilade crum's existence is entirely independent of POOM contents.

---

### What the POOM Entry Removal Actually Removes

When `docreatelink` [do1.c:193–219] creates a link, two separate writes occur:

1. **Granfilade**: `createorglingranf(taskptr, granf, &hint, linkisaptr)` [do1.c:209] — writes a GRANORGL crum at `linkisaptr` into the global granfilade. This maps the link's ISA to its own POOM.

2. **Home document's POOM**: `docopy(taskptr, docisaptr, &linkvsa, ispanset)` [do1.c:212] — inserts the link's ISA (as an ispan spanning the link-subspace V-address) into the home document's POOM. This is the V→I mapping entry that places the link in the home document's V-space at `linkvsa` (a link-subspace address ≥ 0.2.1).

"Reverse-orphaning" — removing the POOM entry — calls `dodeletevspan` on the home document for the link-subspace span. That traces to:

```c
bool dodeletevspan(...) {                                   // do1.c:141
    findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)   // finds HOME doc's orgl
    && deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)    // deletes from HOME POOM
}
```

`deletevspanpm` [orglinks.c:142–148] calls `deletend((typecuc*)docorgl, ...)` — this modifies the **home document's POOM** by removing crums from it. It does not touch:

- The granfilade (a different enfilade, the global `granf`)
- The link's own POOM (a different enfilade, stored as `orglptr` in the granfilade crum)
- The spanfilade

After the POOM entry is removed, `fetchorglgr` still descends the granfilade to the GRANORGL crum at `linkisaptr` and returns the link's own POOM. The crum was inserted into the granfilade by `createorglgr` and is not removed by document POOM operations.

---

### Conclusion

**Resolution is purely a granfilade lookup** once the BERT gate is passed.

Neither the POOM entry in the home document nor an open BERT state for the home document is required. Specifically:

1. **Surviving POOM entry — not required.** `fetchorglgr` descends the granfilade by ISA address using `retrievecrums` → `findcbcseqcrum` [retrie.c:167]. This traversal is structural over the GRAN enfilade. The home document's POOM (a POOM enfilade) is a distinct data structure. Removing crums from it does not alter the granfilade.

2. **BERT-opened home document — not required.** The BERT check in `findorgl` [granf1.c:22] calls `checkforopen(isaptr, ...)` where `isaptr` is the **link's** ISA, not the home document's. `checkforopen` searches the berttable by tumbler hash for the link ISA [bert.c:63–65]. The home document's berttable entry is never consulted.

3. **BERT on the link's own ISA — conditionally required.** It is required when:
   - `type != NOBERTREQUIRED`, AND
   - `isxumain = FALSE` (both `bed` and `be` compile targets), AND
   - The link ISA is not in the berttable for the current connection
   
   But for `dofollowlink` and `docreatelink`, `NOBERTREQUIRED` is explicitly passed [do1.c:213, 229], bypassing the berttable search entirely.

4. **Granfilade entry — strictly required.** If the GRANORGL crum does not exist in the granfilade at the link's ISA, `fetchorglgr` returns NULL at the exact-equality check [granf2.c:37–40]. However, this crum is created once by `createorglingranf` during link creation and is not removed by any POOM manipulation — it would require a granfilade-level delete to remove it.
