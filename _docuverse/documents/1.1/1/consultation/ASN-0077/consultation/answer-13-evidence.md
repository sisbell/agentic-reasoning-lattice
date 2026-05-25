## Question 13 [evidence]

> Does the spanfilade store a distinguished "origin" flag on DOCISPAN entries, or are all entries (origin document plus transcluding documents) structurally indistinguishable?

## KB Synthesis

All DOCISPAN entries are structurally identical — there is no origin flag.

The `insertspanf` call that creates them has the signature `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` [ST-INSERT, Finding 0036]. The `docisaptr` argument is simply the receiving document — whether that document created the content via INSERT or transcluded it via VCOPY/COPY makes no difference to the entry format. Each entry is a mapping of `ISpan → DocISA`, nothing more [SS-DOCISPAN, Finding 0047].

The consequence is that after transcluding content from doc A into doc B, both docs appear in `FINDDOCSCONTAINING` results against those I-addresses, and their entries are indistinguishable from each other's perspective.

Provenance — knowing *which document originally created* an I-address — is tracked elsewhere: in the POOM crum's `homedoc` field in the granfilade, not in the spanfilade at all [INV-IADDR-PROVENANCE, Finding 0046]. The spanfilade records presence, not origin.

---

## Code Exploration

I now have everything I need. Here is the full answer.

---

## Does the Spanfilade Store an "Origin" Flag on DOCISPAN Entries?

**No. All DOCISPAN entries are structurally indistinguishable.** There is no origin flag, bit, or field anywhere in the spanfilade data structure. The distinction between the document that originally produced content and documents that transclude it does not exist within the spanfilade itself.

---

### Data Structure

`DOCISPAN` is not a struct — it is an integer constant (`backend/xanadu.h:39`):

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

It serves as a *span-type discriminator* within the spanfilade's key space, alongside the three link-endpoint types.

The only per-entry payload is `type2dbottomcruminfo` (`backend/wisp.h:107–109`):

```c
typedef struct struct2dbottomcruminfo {
        tumbler homedoc;
} type2dbottomcruminfo;
```

One field. A tumbler. That is the entire metadata budget for a spanfilade leaf.

---

### How an Entry Is Keyed

`insertspanf` (`backend/spanf1.c:15–54`) builds the two-dimensional key:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // line 22
```

`prefixtumbler` (`backend/tumble.c:641–651`) prepends the integer `spantype` as the most-significant mantissa word of the ISA tumbler. For a DOCISPAN entry the ORGLRANGE key is therefore `4.document_isa` — the integer 4 followed by the document's ISA tumbler. The SPANRANGE key is the I-span's stream and width.

---

### What `homedoc` Actually Stores

Still inside `insertspanf`, the `homedoc` field is set depending on item type:

| Item type | `homedoc` ← | Source line |
|-----------|-------------|-------------|
| `ISPANID` | `isaptr` (the document ISA passed in) | `spanf1.c:29` |
| `TEXTID`  | `isaptr` (same document ISA) | `spanf1.c:42` |
| `SPORGLID` | `sporglset->sporgladdress` (the SPORGL's own address, **not** the document ISA) | `spanf1.c:33` |

For the dominant `ISPANID` and `TEXTID` cases, `homedoc` is redundant with what is already encoded in the ORGLRANGE key. For `SPORGLID`, it differs. In neither case is there a boolean or discriminant marking "origin vs. transclusion."

---

### Every DOCISPAN Insertion Uses the Same Code Path

Both `docopy` and `docopyinternal` in `backend/do1.c` call `insertspanf` identically:

```c
// do1.c:62
insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)

// do1.c:79
insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

There is no variant call, no extra flag argument, no second function for "origin" insertions.

---

### Querying Confirms the Flat Model

`finddocscontainingsp` (`backend/spanf1.c:151–188`) is the canonical lookup: given an I-span, which documents contain it?

```c
// spanf1.c:168–171
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                              ispanset, SPANRANGE, (typeisa*)NULL);
```

It queries the full DOCISPAN band (`4.x` for all `x`) and returns *every* document address it finds. There is no filtering by origin, no priority ordering, no flag check. All matching documents are treated as peers.

---

### Conclusion

The spanfilade is a pure multi-map: content spans → sets of document ISAs. Every document that contains a given span registers one DOCISPAN entry keyed on `4.document_isa` × `content_span`. The entries for the origin document and for any transcluding document are byte-for-byte identical in structure. Origin provenance is not recorded in the spanfilade. Recovering it requires going elsewhere — to the POOM version tree or the granfilade — neither of which is consulted during a `finddocscontainingsp` call.
