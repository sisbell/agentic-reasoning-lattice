## Question 4 [evidence]

> In the udanax-green K.δ operation, do the Node and Account creation cases leave every document arrangement M(d) unchanged and add no entry to dom(M), so that ran/dom of every arrangement is untouched?

## KB Synthesis

From the KB, Node and Account creation satisfy both properties.

**No modification to any M(d)**

Node/Account creation calls `createorglingranf` with a non-document hint (NODE→NODE, depth=1; ACCOUNT→DOCUMENT, depth=2) to allocate an orgl address in the granfilade [SS-ADDRESS-ALLOC / ST-ADDRESS-ALLOC, Finding 0021]. This operation writes only to the address-space portion of the granfilade. The POOM enfilade for any document d is a separate tree structure; nothing in the allocation path calls `insertpm`, `deletevspanpm`, or any other POOM-mutating primitive. [SS-POOM-MUTABILITY] confirms that M(d) is the sole locus of destructive mutation and is modified only by INSERT, DELETE, and REARRANGE operating on a specific document's orgl.

The analogous case is explicit in [FC-GRANF-ON-VERSION] (Finding 0077): even VERSION, which *does* allocate a document address, leaves `granf_content` and all POOMs unchanged. Node/Account creation is weaker still — it never creates a document orgl at all.

**No addition to dom(M)**

dom(M) is the set of document ISAs that have associated POOM structures. Node and Account orgls are non-document entities; they are allocated via `findisatoinsertnonmolecule` with a DOCUMENT hint only when creating *documents* [ST-ADDRESS-ALLOC, Finding 0021]. A Node or Account address entry in the granfilade has no POOM, so dom(M) is unaffected.

**Caveat — cache interaction**

The shared grim-reaper cache means Node/Account allocation could, under memory pressure, evict modified POOM crums to disk [EC-CROSS-ENFILADE-EVICTION, SS-CACHE-MECHANISM]. This changes durability state but not the logical value of any M(d); evicted crums are reloaded transparently. It is not an observable mutation of any arrangement.

**Conclusion:** Yes — both properties hold. Node and Account creation are pure granfilade address-space operations; they leave ran/dom of every arrangement untouched.

---

## Code Exploration

Now I have everything I need to give a complete, cited answer.

---

## Answer: Node and Account Creation in K.δ — Effect on M(d) and dom(M)

**Short answer: Yes.** Both Node creation and Account creation leave every existing M(d) unchanged and add no entry to dom(M). Here is the full trace.

---

### Entry Point: `createnode_or_account` (fns.c:375–386)

```c
void createnode_or_account(typetask *taskptr)
{
  tumbler t;
  bool getcreatenode_or_account(), docreatenode_or_account();

    if(  getcreatenode_or_account(taskptr,&t)
         && docreatenode_or_account(taskptr,&t)) {
        putcreatenode_or_account(taskptr,&t);
    } else {
        putrequestfailed(taskptr);
    }
}
```

Both Node and Account creation route through the same function `docreatenode_or_account`. There is no separate code path for Account vs. Node.

---

### Core Operation: `docreatenode_or_account` (do1.c:243–258)

```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr)
{
  typeisa isa;
  typehint hint;
  bool createorglingranf();
  bool result;

    tumblercopy(isaptr, &isa);
    makehint (NODE, NODE, 0, &isa, &hint);                    // do1.c:251
    result = createorglingranf (taskptr, granf, &hint, &isa); // do1.c:252
    if (result) {
        tumblercopy(&isa, isaptr);
    }
    return result;
}
```

**Key line is do1.c:251.** The hint type is `(NODE, NODE)` — supertype and subtype both set to `NODE`. Compare this with the two document-creating operations:

- `docreatenewdocument` (do1.c:239): `makehint (ACCOUNT, DOCUMENT, 0, ...)` — creates a Document under an Account
- `docreatenewversion` (do1.c:271–275): `makehint (DOCUMENT, DOCUMENT, 0, ...)` or `makehint (ACCOUNT, DOCUMENT, 0, ...)` — creates a Document under a Document or Account

The Node/Account hint `(NODE, NODE)` allocates in the Node address stratum, not the Document stratum. This distinction propagates through every layer below.

---

### `createorglingranf` (granf1.c:50–55)

A thin wrapper:

```c
bool createorglingranf(typetask *taskptr, typegranf granfptr, typehint *hintptr, typeisa *isaptr)
{
  bool createorglgr();
     return (createorglgr(taskptr, granfptr, hintptr, isaptr));
}
```

---

### `createorglgr` (granf2.c:111–128) — the only mutation site

```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typegranbottomcruminfo locinfo;
  bool findisatoinsertgr();
  typecuc *createenf();

      if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
          return (FALSE);
      locinfo.infotype = GRANORGL;
      locinfo.granstuff.orglstuff.orglptr = createenf (POOM);     // granf2.c:120
    reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);  // granf2.c:121
      locinfo.granstuff.orglstuff.orglincore = TRUE;               // granf2.c:122
      locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
      insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);         // granf2.c:125
    rejuvinate ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
      return (TRUE);
}
```

This function does exactly two things:

1. **granf2.c:117** — `findisatoinsertgr` computes a fresh address `*isaptr` in the Node stratum (because `hint.supertype == hint.subtype == NODE`, `depth = 1` at granf2.c:209).
2. **granf2.c:120–125** — allocates an empty POOM (`createenf(POOM)`) and inserts it into `granf` at that Node address via `insertseq`.

**That is the entire operation.** There are no calls to:
- `insertpm` / `insertspanf` — the two functions that add content to a document arrangement
- `deletevspanpm` / `rearrangepm` — the two functions that mutate existing arrangements
- `fetchorglgr` / `findorgl` — the functions that open an existing ORGL for writing

---

### Address-stratum argument: why the new ORGL is not in dom(M)

`findisatoinsertgr` dispatches at granf2.c:135 on `hintptr->subtype`:

```c
if (hintptr->subtype == ATOM) {
    findisatoinsertmolecule (...);   // text/link atoms under an existing doc
} else {
    findisatoinsertnonmolecule (...); // DOCUMENT, ACCOUNT, or NODE-level entries
}
```

For hint `(NODE, NODE)`, `subtype == NODE ≠ ATOM`, so `findisatoinsertnonmolecule` runs. Inside (granf2.c:209):

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

`NODE == NODE` → `depth = 1`. The new address is computed as one sub-level below the supplied hint ISA.

For document creation (`ACCOUNT, DOCUMENT`), `depth = 2` — two sub-levels, nesting a Document under an Account. That two-level nesting is what defines the Document address stratum.

A Node/Account ISA has depth 1 and sits above the Document stratum. M is defined over Document ISAs. The new ORGL is at a Node ISA, which is outside dom(M) by definition.

---

### `spanf` is never touched

`spanf` (the spanfilade recording I↔V correspondence) is modified only in:
- `insertspanf` (called from `docopy`, `doinsert`, `domakelink`)
- `insertendsetsinspanf` (called from `docreatelink`)

None of these are reachable from `createnode_or_account`. The spanfilade is completely untouched, so the ran/dom of every arrangement is untouched.

---

### `xaccount` (fns.c:364–373) — Account activation, not creation

For completeness: `xaccount` is a separate FEBE handler that sets the session's active account reference:

```c
void xaccount(typetask *taskptr)
{
  bool getxaccount();
    if (getxaccount(taskptr,&(player[user].account))) {
        putxaccount(taskptr);
    }
}
```

It writes to `player[user].account` — a per-connection variable in the player table — and touches no global document state at all. M(d) and dom(M) are trivially unaffected.

---

### Summary

| Operation | Modifies `granf`? | Modifies `spanf`? | Modifies any existing ORGL? | Adds to dom(M)? |
|---|---|---|---|---|
| `createnode_or_account` | Yes — adds one NODE-stratum ORGL entry | No | No | No — new ORGL is at NODE address, not DOCUMENT address |
| `xaccount` | No | No | No | No |

**Both the Node creation and Account creation cases of K.δ leave every M(d) unchanged and add no entry to dom(M).** The mutations are confined to the Node stratum of `granf`; the Document stratum and `spanf` are unperturbed. The ran/dom of every arrangement is untouched.
