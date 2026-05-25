## Question 19 [evidence]

> Is there any per-document audit structure (beyond the POOM, granfilade, and spanfilade) that records the historical sequence of which I-spans were ever mapped into a document's V-space?

## KB Synthesis

No. There is no per-document audit structure beyond the three main layers.

The closest thing is the **DOCISPAN portion of the spanfilade**, which is append-only and never purged. Because DELETE does not remove spanfilade entries [INV-SPANF-WRITE-ONLY], [INT-DELETE-SPANF-DIVERGENCE], the DOCISPAN sub-index retains entries for every I-span ever placed into a document via INSERT or COPY. This is why `FINDDOCSCONTAINING` returns a document even after its content is deleted [INV-IADDRESS-PERMANENT], [EC-STALE-SPANF-REFERENCE].

However, the DOCISPAN has three limitations that prevent it from functioning as a true audit trail:

1. **No ordering.** It is a set of `(ISpan → DocISA)` mappings, not a chronologically ordered sequence [SS-DOCISPAN]. Insertion chronology is encoded in I-address monotonicity [INV-MONOTONIC], but that's global, not per-document.

2. **APPEND is invisible.** Content placed via APPEND creates no DOCISPAN entries [EC-APPEND-NO-DOCISPAN], so the record is incomplete.

3. **Not per-document in structure.** It is indexed by I-address to find documents, not organized as a per-document history.

The POOM records current state only — DELETE mutates it destructively with no undo log [SS-POOM-MUTABILITY], [INV-DELETE-NOT-INVERSE]. The granfilade records content bytes permanently but is global and unordered relative to any particular document [FC-GRANF-ON-DELETE].

There is nothing in the KB describing any additional structure.

---

## Code Exploration

I now have all the evidence needed for a complete answer.

---

## Is There a Per-Document Audit Structure for Historical V↔I Mappings?

**No.** There is no per-document structure in udanax-green that records the historical sequence of which I-spans were ever mapped into a document's V-space. The finding is unambiguous across every relevant file.

---

### What the Structures Actually Store

#### POOM (2D enfilade) — current state only

The POOM bottom crum `type2dcbc` [enf.h:109–131] carries exactly one payload field:

```c
/* type2dcbc */
struct struct2dcbc {
    ...
    type2dbottomcruminfo  c2dinfo;   /* enf.h:129 */
};
```

And `type2dbottomcruminfo` is [wisp.h:107–109]:

```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

`homedoc` is a single tumbler — the I-address of the content source for this V-position. It encodes **current** V→I state. There is no list, no sequence, no previous-value field.

#### Granfilade — content, no history

`typecbc` carries `cinfo` of type `typegranbottomcruminfo` [enf.h:101–106], which is a union of text bytes or an orgl pointer plus an `infotype` tag. No history field.

#### Disk structures — refcount and version-disk-number only

`typediskloafhedr` [coredisk.h:12–21]:

```c
typedef struct structdiskloafhedr {
    INT  sizeofthisloaf;
    SINT isapex;
    SINT height;
    SINT denftype;
    SINT numberofcrums;
    SINT refcount;          /* for subtree sharing / GC — coredisk.h:18 */
    SINT allignmentdummy;
} typediskloafhedr;
```

`refcount` is for garbage collection. `typeuberdiskloaf` adds [coredisk.h:67]:

```c
INT versiondisknumber;
```

This is an integer sequence counter for disk-loaf versions (used for cache consistency), not a record of I-span history.

#### BERT table — session state only

`bertentry` [bert.c:13–19]:

```c
typedef struct {
    int  connection;
    tumbler documentid;
    char created, modified;   /* boolean session flags */
    int  type;
    int  count;
} bertentry;
```

`created` and `modified` are single-bit session flags cleared on close. Nothing accumulates across sessions.

---

### The Only "Historical" Information: ISA Tumbler Hierarchy

The sole mechanism that records version lineage is the **tumbler addressing scheme itself**. When `docreatenewversion` creates a new version [do1.c:260–298], it calls `createorglingranf` with a hint that allocates a new ISA under the source document's account. The child tumbler is numerically subordinate to the parent:

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    ...
    makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);   /* do1.c:271 */
    if (!createorglingranf(taskptr, granf, &hint, newisaptr)) ...
```

And `common.h:53` confirms this is load-bearing:

```c
#define NPLACES 16  /* places in mantissa of tumbler - increased from 11 to support deeper version chains */
```

So you can **infer** ancestry by reading tumbler structure — a child ISA is "under" its parent in the tumbler tree. But this is geometric implication in the address space, not an explicit audit log.

---

### What Is Not There

The grep for `history|audit|trail|ancestor|lineage|previous.*version|version.*chain` across all `.c` files [backend/*.c] returns only those two hits: the `NPLACES` comment and a `credel.c:363` comment about protecting crum **tree** ancestors from the grim reaper (the in-memory cache eviction mechanism) — both unrelated to V↔I mapping history.

There is no:
- Append-only list of past I-span→V-position mappings
- "Previous version" pointer in any document struct  
- Changelog written on `docinsert`, `docdelete`, or `docreatenewversion`
- Separate history enfilade or audit file

---

### Reconstructing History Is Query-Time, Not Stored

If you want the sequence of I-spans that appeared in a document's V-space over its lifetime, you must enumerate all version ISAs (by walking the tumbler subtree), open each one, and call `doretrieve` against each version's POOM. `correspond.c` provides I-span intersection tools for comparing two versions at query time — but that is computation across independently-stored version snapshots, not a persisted record.

**The design is append-only at the version level (each edit creates a new version), but there is no structure that makes the sequence of mappings explicit. The history lives in the totality of all versions, queryable but not summarized.**
