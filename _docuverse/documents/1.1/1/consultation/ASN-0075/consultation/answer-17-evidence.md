## Question 17 [evidence]

> Can a deleted I-range be transcluded back into a document via COPY using its preserved I-addresses, given that granfilade content persists permanently after DELETE?

## KB Synthesis

## Yes — With a Critical Precondition

**Short answer:** COPY can restore deleted content with its original I-addresses intact, but only if some document still holds a POOM mapping to those I-addresses.

---

### Why DELETE Does Not Destroy the Bytes

[INV-IADDR-IMMUTABILITY] (Finding 0064) establishes the foundation: DELETE operates exclusively on the POOM enfilade, removing V-to-I mappings by pruning bottom crums. The granfilade is append-only — no operation removes I-addresses or their content bytes. [FC-GRANF-ON-DELETE] formalizes this: `∀ op ∈ {DELETE, REARRANGE} : granf_state_after(op) = granf_state_before(op)`.

---

### How COPY Restores Identity

[ST-COPY] (Finding 0064) states this directly:

> COPY is the only mechanism for identity-preserving content restoration after DELETE. The precondition for identity-preserving restoration is that **some accessible document still references the original I-addresses**.

```
Let source still map i to some V-span v_s
After DELETE(doc, v):              iaddr_doc(v) = ∅
After COPY(doc, v, source, v_s):   iaddr_doc(v) = i    -- identity restored
```

Contrast with INSERT: [INV-DELETE-NOT-INVERSE] confirms INSERT always allocates fresh I-addresses, permanently severing transclusion chains, version comparison, and link endpoints. COPY via `insertpm` shares existing I-addresses rather than allocating new ones.

---

### The Critical Precondition

COPY works through a V-spec: it converts V-positions in the source document to I-addresses via that document's POOM, then inserts those I-addresses into the target's POOM ([ST-VCOPY], [PRE-COPY]). There is no mechanism to COPY by direct I-address specification — the interface is purely V-space.

Therefore, the transcluded restoration is possible **if and only if** some document retains a POOM mapping to the desired I-addresses. Candidates include:

- **A version created before deletion** — [ST-VERSION-CREATE] (Finding 0046) confirms CREATENEWVERSION copies text I-addresses, producing an independent snapshot
- **Another document that transcluded the content** — [FC-DELETE-CROSS-DOC] confirms DELETE on document D leaves all other documents' POOMs unchanged
- **The spanfilade** — [INV-SPANF-WRITE-ONLY] confirms DOCISPAN entries persist permanently, so FINDDOCSCONTAINING can locate which documents still hold the I-addresses

If the I-addresses are completely unreferenced in all POOMs (deleted from every document), the bytes persist in the granfilade but are unreachable via any COPY path. This is the "ghost" state described in [EC-GHOST-LINK] — content exists in I-space but cannot be accessed through normal V-space operations.

---

### Summary

| Condition | COPY Restores? | Identity Preserved? |
|-----------|---------------|---------------------|
| Version exists pre-deletion | Yes | Yes |
| Another doc has transclusion | Yes | Yes |
| All POOMs cleared | No (unreachable) | N/A |
| INSERT instead of COPY | Syntactically yes | No — fresh I-addresses |

The Xanadu model's "undo delete" is therefore not `INSERT(deleted_text)` but `COPY(from_surviving_version_or_transclusion)` — a distinction with permanent consequences for content identity, link endpoints, and version comparison.

---

## Code Exploration

All critical code paths are now verified from source. Here is the full answer:

---

## Can a Deleted I-Range Be Transcluded Back via COPY?

**Yes.** DELETE removes V-space visibility only. The granfilade — the permanent I-space store — is untouched. COPY accepts I-addresses unconditionally and re-instantiates them at any V-location. There is no liveness oracle, no reference counting, no guard against transcluding "deleted" content.

---

### What DELETE Actually Does

Entry point: `do1.c:158-167`

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr) {
  typeorgl docorgl;
  return (
     findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
  );
}
```

`deletevspanpm` at `orglinks.c:145-152` does one thing:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr) {
  if (iszerotumbler(&vspanptr->width))
    return (FALSE);
  deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);  // V dimension only
  logbertmodified(docisaptr, user);
  return (TRUE);
}
```

`deletend` at `edit.c:31-76` operates exclusively on the **POOM tree** (the V↔I permutation matrix):

- Case 1 (`edit.c:59-60`): fully-contained crums → `disown` + `subtreefree` — removes POOM nodes
- Case 2 (`edit.c:63`): partially-contained crums → `tumblersub` — adjusts V-displacement offsets

The key constraint: `deletend` is called with the `V` index. It navigates and mutates the **document structure**, not the granfilade enfilade.

---

### `subtreefree` Does Not Touch Granfilade Text

`credel.c:413-432`:

```c
void subtreefree(typecorecrum *ptr) {
  if (ptr->height > 0) {
    for (p = ((typecuc *)ptr)->leftson; p; p = right) {
      disown(p);
      subtreefree(p);               // recurse through POOM nodes
    }
  } else if (ptr->cenftype == GRAN
          && ((typecbc *)ptr)->cinfo.infotype == GRANORGL
          && ((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglincore)
    orglfree(((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglptr);  // line 430
  freecrum(ptr);
}
```

The GRAN branch — `orglfree` at `credel.c:470-489` — only triggers for **GRANORGL** nodes that are in-core. What it does:

```c
// credel.c:487-488
((typecbc *)ptr->leftbroorfather)->cinfo.granstuff.orglstuff.orglincore = FALSE;
((typecbc *)ptr->leftbroorfather)->cinfo.granstuff.orglstuff.orglptr = NULL;
```

It marks the ORGL as out-of-core. The disk block (`diskorglptr.diskblocknumber`) is preserved. The disk content is never freed.

**GRANTEXT nodes are never entered.** There is no code path from `deletend` → `subtreefree` that removes granfilade text atoms. The only thing freed is the in-memory POOM crum struct itself (`freecrum`), which is the *index entry*, not the content.

---

### What COPY Actually Checks

`docopy` at `do1.c:45-65`:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset) {
  return (
     specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)  // line 54
  && findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)       // line 55: validates TARGET doc
  && acceptablevsa(vsaptr, docorgl)                                 // line 56: liveness check?
  && asserttreeisok(docorgl)                                        // line 57: tree integrity only
  && insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)        // line 60: the actual copy
  && insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)     // line 62: spanfilade index
  );
}
```

The supposed liveness check, `acceptablevsa` at `do2.c:110-113`:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr) {
  return (TRUE);
}
```

Unconditional. No measurements taken. No validation of source I-addresses against any document.

---

### I-Span Input Takes No Document Lookup Path

`specset2ispanset` at `do2.c:14-46`:

```c
for (; specset; specset = ...) {
  if (((typeitemheader *)specset)->itemid == ISPANID) {
    *ispansetptr = (typeispanset)specset;   // line 25: I-span passed directly
  } else if (... VSPECID) {
    // ... V-span converted to I-span via current document V↔I mapping
  }
}
```

When the source spec is an I-span (not a V-spec), it bypasses `vspanset2ispanset` entirely. The I-addresses are accepted as-is, with no lookup into any document's current V-structure to verify they are "live."

---

### `insertpm` Writes I-Addresses Into New V-Location Unconditionally

`orglinks.c:100-131`:

```c
for (; sporglset; sporglset = ...) {
  unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
  movetumbler(&lstream, &crumorigin.dsas[I]);    // line 105: source I-address
  movetumbler(&lwidth, &crumwidth.dsas[I]);       // line 109: I-width
  movetumbler(vsaptr, &crumorigin.dsas[V]);       // line 113: destination V-address
  // ... compute V-width from I-width
  insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // line 130
}
```

`insertnd` writes a new POOM crum that maps the I-address range to the new V-address. No check that the I-address is currently referenced anywhere. No check that it was ever in a live document.

---

### The Condition for Successful Re-transclusion

A COPY of a previously-deleted I-range succeeds when:

1. The I-addresses are known (retained from before deletion, or obtained via a prior RETRIEVE that returned them)
2. The granfilade content exists at those I-addresses — which it does, since `deleteseq` in `edit.c:16-28` operates only on GRAN enfilade nodes (used for granfilade editing, *not* called from POOM delete), and POOM deletion never removes granfilade text atoms
3. No disk I/O error when `fetchorglgr` (`granf2.c:22-81`) accesses the content

The system will produce a new POOM entry, a new V-address range, and the content will be retrievable. From the user's perspective, the deleted content reappears at a new location.

---

### What Is NOT Preserved After DELETE

The V-span mapping is gone from the POOM tree. This means:

- A COPY from a **V-spec** of the deleted range will return nothing — `vspanset2ispanset` → `permute` → `retrieverestricted` searches the POOM tree by V-address, finds no crums covering the deleted range, and returns an empty I-span set
- The COPY then inserts nothing; it silently succeeds with zero content

Only COPY from an explicit **I-span** bypasses this. The caller must already know the I-addresses.

---

### Summary Table

| Operation | Granfilade text | POOM V↔I mapping | I-address validity |
|-----------|----------------|------------------|--------------------|
| DELETE | Untouched | Removed | Preserved |
| COPY (I-span) | Read directly | New entry written | Accepted unconditionally |
| COPY (V-spec of deleted range) | Not reached | No match found | N/A — returns empty |

---

### Architectural Interpretation

This is not a bug. The design treats I-addresses as **eternal content identifiers**. The granfilade is a permanent content store indexed by I-address. Deletion from a document means removal from V-space — it is not an assertion that the content has ceased to exist. COPY from I-addresses is the mechanism for bringing content from I-space into V-space, and it works regardless of whether that content has ever appeared in a document, was once deleted, or was directly inserted into granfilade without ever being in a document at all.

The unimplemented `acceptablevsa` stub at `do2.c:110-113` is the architectural marker for where a policy-layer "liveness" check *could* be enforced — but none has been written. In the current implementation, the granfilade is the sole authority on whether content exists, and it says yes permanently.
