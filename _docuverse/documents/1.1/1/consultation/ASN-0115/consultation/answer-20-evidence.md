## Question 20 [evidence]

> Does RETRIEVECONTENTS always source bytes from the granfilade by I-address (FC-GRANFILADE-PERMANENT), meaning deleted-then-orphaned I-addresses are still deliverable if a SpecSet somehow references them?

## KB Synthesis

Yes — with an important qualification about *how* the SpecSet gets resolved to I-addresses.

## RETRIEVECONTENTS sources bytes from the granfilade unconditionally

The call chain is: SpecSet → `specset2ispanset` → I-spans → `ispanset2vstuffset(granf, ispanset)`. The final lookup goes directly into the granfilade by I-address with no secondary check on whether those addresses are currently referenced in any POOM.

The granfilade is **permanently append-only**. [INV-IADDR-IMMUTABILITY] (Findings 0030, 0064) establishes that DELETE frees POOM bottom crums but never touches the granfilade entries themselves. [FC-GRANF-ON-DELETE] confirms: `∀ op ∈ {DELETE, REARRANGE} : granf_after(op) = granf_before(op)`. The bytes at an I-address remain in the granfilade forever.

## The constraint is in SpecSet resolution, not in the lookup

The chokepoint is `specset2ispanset`, which routes through a document's current POOM via `findorgl`. [PRE-RETRIEVE-CONTENTS] requires the referenced document to be open. If an I-address has been deleted from a document's POOM (V→I mapping removed), that document's POOM will produce no I-span for it — so `ispanset2vstuffset` never gets a chance to look it up.

However, this is a POOM-level exclusion, not a granfilade-level one:

- **A version created before deletion** still has those I-addresses in its POOM. [FC-VERSION-ISOLATION] guarantees that editing the original doesn't affect the version's POOM. A SpecSet over the version delivers the bytes. [ST-COPY] (Finding 0064) makes this explicit: "undo delete in the Xanadu model is not INSERT(deleted_text) but COPY(from_version_with_original_iaddrs). The precondition for identity-preserving restoration is that some accessible document still references the original I-addresses."

- **Any document that transcluded the content** retains its own POOM mapping. [FC-DELETE-CROSS-DOC] states DELETE in one document has zero effect on any other document's POOM mappings.

## Direct answer

Given a SpecSet that *can* resolve to the orphaned I-addresses (via any live POOM reference — a version, a transcluding document), RETRIEVECONTENTS will deliver those bytes from the granfilade. The granfilade lookup is unconditional. [INV-NO-IADDR-REUSE] further guarantees those addresses are never reassigned to different content.

The granfilade is, in effect, a permanent content-addressed store. "Orphaned" means *unreachable via the deleting document's POOM*, not *absent from the store*. [INV-IADDRESS-PERMANENT] (Finding 0023) confirms this asymmetry: `find_documents` still reports a document for deleted content precisely because the spanfilade (like the granfilade) is append-only and the I-addresses never leave.

---

## Code Exploration

Now I have everything needed. Let me compose the full answer.

---

## Does RETRIEVECONTENTS Always Source Bytes by I-Address from the Granfilade?

**Yes — and the term "FC-GRANFILADE-PERMANENT" does not appear in the C source.** The granfilade is simply the global `granf` (`extern typegranf granf` in `xanadu.h:14`, `#define typegranf INT *`). There is no named constant for it in the FEBE command dispatch. Here is the complete traced path.

---

### The Call Chain

```
retrievev()          [fns.c:175]
  └─ doretrievev()   [do1.c:338]
       ├─ specset2ispanset(... READBERT)   [do2.c:14]
       │    ├─ [ISPANID path] → passes I-span through directly, no auth  [do2.c:24-26]
       │    └─ [VSPECID path]
       │         ├─ findorgl(... READBERT)   [granf1.c:17]
       │         │    ├─ checkforopen(isaptr, READBERT, user)   [bert.c:52]
       │         │    └─ fetchorglgr(taskptr, granf, isaptr)   [granf2.c:22]
       │         └─ vspanset2ispanset(orgl, vspanset)   [orglinks.c:397]
       └─ ispanset2vstuffset(taskptr, granf, ispanset)   [granf1.c:58]
            └─ ispan2vstuffset(taskptr, granf, ispan)   [granf2.c:286]
                 └─ retrieveinspan(granf, lowerbound, upperbound, WIDTH)
                      └─ granfilade tree search by I-address (WIDTH index)
```

---

### What Happens at Each Stage

**`doretrievev` [do1.c:338–346]** calls two things in sequence:

```c
return
   specset2ispanset (taskptr, specset, &ispanset, READBERT)
&& ispanset2vstuffset (taskptr, granf, ispanset, vstuffsetptr);
```

The first converts V-addresses (VSpec items) to I-spans while checking authorization. The second takes the resulting I-spanset and fetches bytes directly from `granf` by those I-addresses.

**`specset2ispanset` [do2.c:14–46]** dispatches on `itemid`:

```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *ispansetptr = (typeispanset)specset;          // line 25 — passed through raw
    ispansetptr = (typeispanset *)&((typeitemheader *)specset)->next;
} else if (((typeitemheader *)specset)->itemid == VSPECID) {
    ...
    findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)  // line 35
    && (ispansetptr = vspanset2ispanset (...))                                   // line 36
}
```

**Critical branch [do2.c:24–26]:** When a SpecSet item already carries `ISPANID`, it is **threaded directly into the output I-spanset with zero authorization check and zero V→I translation.** It goes straight to the granfilade read. The `READBERT` authorization only fires on the `VSPECID` branch.

**`findorgl` [granf1.c:17–41]** — for the VSpec path — calls `checkforopen(isaptr, READBERT, user)` [granf1.c:22]. That checks whether `*isaptr` (the document's I-address) appears in the BERT table with a compatible access grant for the caller:

```c
if (/*backenddaemon &&*/(temp = checkforopen(isaptr, type, user)) <= 0) {
    if (!isxumain) {
        ...
        return FALSE;
    }
}
```

If the document is not open (not in the BERT table), `checkforopen` returns ≤ 0 and `findorgl` returns FALSE — **but this is a per-document authorization check, not a per-I-address liveness check.**

**`ispan2vstuffset` [granf2.c:286–318]** takes the final I-span and calls `retrieveinspan((typecuc*)fullcrumptr, &lowerbound, &upperbound, WIDTH)`. This searches the granfilade tree by I-address interval alone:

```c
movetumbler (&ispanptr->stream, &lowerbound);
tumbleradd(&lowerbound, &ispanptr->width, &upperbound);
context = retrieveinspan ((typecuc*)fullcrumptr, &lowerbound, &upperbound, WIDTH);
```

`retrieveinspan` → `retrievecrums` [retrie.c:15–31] → `findcbcseqcrum` walks the tree by I-address. **There is no check anywhere in this path that the I-address corresponds to content still referenced by any live ORGL, version, or V-span.**

---

### The Liveness Gap

**The granfilade is an append-only content store indexed by I-address.** Deletions remove V-address mappings (the ORGL and spanfilade entries) but do not expunge bytes from the granfilade. `fetchorglgr` [granf2.c:22–82] validates:

1. **Bounds check** [granf2.c:31]: Is `address` ≤ granfilade total width? Returns NULL if not.
2. **Exact-match check** [granf2.c:37–40]: `!tumblereq(&context->totaloffset, address)` → returns NULL if the tree node found doesn't start exactly at the requested address.
3. **Type check** [context.c:250]: `context2vstuff` only emits content for `GRANTEXT` or `GRANORGL` info types.

None of these checks ask: *does any live document currently reference this I-address?* The granfilade simply returns whatever bytes were committed at that I-address when text was originally inserted.

---

### Consequence: Orphaned I-Addresses Are Deliverable

If a SpecSet is constructed that carries raw `ISPANID` items (rather than `VSPECID` items), those I-spans bypass `findorgl` and `checkforopen` entirely [do2.c:24–26] and arrive at `ispan2vstuffset` [granf2.c:286] directly. The granfilade will return any bytes stored at those I-addresses — **regardless of whether they are currently mapped by any live document, version, or ORGL.**

Even through the normal `VSPECID` path, the authorization gate is at the document granularity (is this document open by this user?), not at the content granularity. Once you have an open handle to a document whose ORGL covers a given I-address range, `fetchorglgr` returns the ORGL and `vspanset2ispanset` walks it; nothing prevents retrieving I-addresses whose corresponding V-address has been deleted, as long as the I-address was ever within that document's granfilade range and the bytes are still present in the tree.

---

### Summary

| Question | Answer | Citation |
|---|---|---|
| Does RETRIEVECONTENTS source bytes by I-address from the granfilade? | **Yes, always.** V→I conversion happens first (for VSPECID specs), then the granfilade is hit by I-address. | `do1.c:343–345`, `granf2.c:294–297` |
| Is there a liveness check (is this I-address still live in any document)? | **No.** | No such check exists anywhere in `retrie.c`, `granf1.c`, `granf2.c`, `do2.c` |
| Can raw ISPANID specs bypass authorization entirely? | **Yes.** The ISPANID branch in `specset2ispanset` [do2.c:24–26] threads I-spans directly through with no `checkforopen` call. | `do2.c:24–26` |
| What is "FC-GRANFILADE-PERMANENT"? | **Not a C constant.** The granfilade is just the global `granf` (`typegranf`). | `xanadu.h:13–14` |
| Can deleted-then-orphaned I-addresses deliver bytes if a SpecSet references them? | **Yes, if the bytes remain in the granfilade tree and the I-address falls within its known width.** The only checks are bounds, exact-address match, and (for VSPECID specs) document-level BERT authorization — not content liveness. | `granf2.c:31, 37–40`, `granf1.c:22`, `do2.c:24–26` |
