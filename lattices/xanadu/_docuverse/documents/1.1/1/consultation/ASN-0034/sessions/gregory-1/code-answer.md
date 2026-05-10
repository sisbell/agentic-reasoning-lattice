I now have everything I need. Here is the complete analysis:

---

## `tumblerincrement` Call Sites: bint Values by Allocation Level

### The Function

`tumblerincrement(aptr, rightshift, bint, cptr)` [tumble.c:599–623]:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    ...
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify(cptr);
}
```

- `rightshift` controls which position in the mantissa is incremented (0 = least-significant active position)
- `bint` is the amount added at that position

---

### Type Hierarchy Constants [xanadu.h:140–146]

```c
#define NODE      1    // server/node level
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4

#define TEXTATOM  1
#define LINKATOM  2
```

---

### Structural ISA Allocation: `findisatoinsertnonmolecule` [granf2.c:203–241]

This function is invoked for all **non-ATOM** subtypes (nodes/servers, accounts, documents, versions). The critical parameter is `depth`:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

All three `tumblerincrement` calls in this function use **bint=1**:

```c
tumblerincrement(&hintptr->hintisa, depth - 1, 1, &upperbound);  // [granf2.c:213] — upper bound
...
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);            // [granf2.c:237] — first child
...
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr); // [granf2.c:240] — next sibling
```

#### Node/Server Level

`docreatenode_or_account` [do1.c:251]:
```c
makehint(NODE, NODE, 0, &isa, &hint);
```
- supertype=NODE(1), subtype=NODE(1) → `depth = (1==1) ? 1 : 2 = **1**`
- All three `tumblerincrement` calls: **rightshift ∈ {0, 1}, bint=1**

#### Account Level

Accounts are created via the same `makehint(NODE, NODE, ...)` call — there is no separate account-level allocation function. `xaccount` [fns.c:364] only reads a pre-existing player account from the player table; it does not allocate in the granfilade. Account addresses ARE node addresses, created by `docreatenode_or_account`.

- **bint=1 universally**

#### Document Level

`docreatenewdocument` [do1.c:239]:
```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
```
- supertype=ACCOUNT(2), subtype=DOCUMENT(3) → `depth = (2==3) ? 1 : 2 = **2**`
- [granf2.c:213]: `tumblerincrement(&hintisa, 1, **1**, &upperbound)` — bint=1
- [granf2.c:237]: `tumblerincrement(&hintisa, 2, **1**, isaptr)` — bint=1
- [granf2.c:240]: `tumblerincrement(isaptr, ..., **1**, isaptr)` — bint=1

#### Version Level

`docreatenewversion` has two branches [do1.c:271, 275]:

- **Same account** (`tumbleraccounteq && isthisusersdocument`):  
  `makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint)` — supertype==subtype → depth=1, **bint=1**

- **Different account**:  
  `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` — same as document creation, depth=2, **bint=1**

---

### Atom ISA Allocation: `findisatoinsertmolecule` [granf2.c:158–180]

Invoked when `hintptr->subtype == ATOM`, for inserting text (`TEXTATOM`) or link (`LINKATOM`) atoms. The bint values here are derived from `hintptr->atomtype`:

#### TEXTATOM (atomtype=1), called from `doinsert`/`domakelink` with `makehint(DOCUMENT, ATOM, TEXTATOM, ...)` [do1.c:117, 180]:

| Line | Call | rightshift | bint |
|------|------|-----------|------|
| [granf2.c:162] | `tumblerincrement(&hintisa, 2, atomtype+1, &upperbound)` | 2 | **2** (=TEXTATOM+1) |
| [granf2.c:166] | `tumblerincrement(&lowerbound, 2, atomtype, isaptr)` | 2 | **1** (=TEXTATOM) |
| [granf2.c:167] | `tumblerincrement(isaptr, 1, 1, isaptr)` | 1 | **1** |
| [granf2.c:169] | `tumblerincrement(&lowerbound, 0, 1, isaptr)` | 0 | **1** |

The bint=2 at line 162 constructs the **upper bound of the search range** (to find where to insert), not the increment applied to the allocated address itself.

#### LINKATOM (atomtype=2), called with `makehint(DOCUMENT, ATOM, LINKATOM, ...)` [do1.c:180, 207]:

| Line | Call | rightshift | bint |
|------|------|-----------|------|
| [granf2.c:162] | `tumblerincrement(&hintisa, 2, atomtype+1, &upperbound)` | 2 | **3** (=LINKATOM+1) |
| [granf2.c:171] | `tumblerincrement(&hintisa, 2, 2, isaptr)` | 2 | **2** |
| [granf2.c:173] | `tumblerincrement(isaptr, 1, 1, isaptr)` | 1 | **1** |
| [granf2.c:175] | `tumblerincrement(&lowerbound, 0, 1, isaptr)` | 0 | **1** |

Again, bint=3 at line 162 and bint=2 at line 171 are for **range-bound computation**, not for advancing past an existing allocation.

---

### Content Element Allocation: `inserttextgr` [granf2.c:83–109]

```c
tumblerincrement(&lsa, 0, textset->length, &lsa);  // [granf2.c:100]
```

- **bint = `textset->length`** — advances the local storage address (LSA) by the number of bytes in the text chunk

This is the **only call where bint>1 is used for actual storage position advancement**: multi-character text is laid out as a contiguous span in the granfilade, and `lsa` is stepped forward by the content length for each text segment in the list.

Also `findlastisaincbcgr` [granf2.c:280–284], which finds the last ISA in a GRANTEXT crum during search:
```c
tumblerincrement(offset, 0, (INT)ptr->cinfo.granstuff.textstuff.textlength - 1, offset);
```
- **bint = textlength−1** — this is a **query traversal** helper, not an allocator

---

### V-Space (VSA) and Utility Calls (not ISA allocation)

These construct V-space addresses (where content lives in a document's virtual address space) and are unrelated to ISA (identity-space address) allocation:

| File:Line | Context | rightshift | bint |
|-----------|---------|-----------|------|
| `do2.c:157–158` | `findnextlinkvsa`: building minimum link VSA (2.1) | 0, 1 | **2**, **1** |
| `do2.c:172–176` | `setlinkvsas`: from-VSA (1.1), to-VSA (2.1) | 0, 1 | **1**, **1**, **2**, **1** |
| `do2.c:179–180` | `setlinkvsas`: three-VSA (3.1) | 0, 1 | **3**, **1** |
| `do2.c:58` | `tumbler2spanset`: ISA→spanset width | tumblerlength-1 | **1** |
| `sporgl.c:81–82` | `link2sporglset`: retrieving link endpoints by whichend | 0 | **whichend** (1/2/3), **1** |
| `orglinks.c:37` | `findvsatoappend`: link-space start (2.0) | 0 | **2** |
| `orglinks.c:42–43` | `findvsatoappend`: fallback VSA (1.1) | 0, 1 | **1**, **1** |
| `orglinks.c:117` | `insertpm`: V-span width from content width | shift | **inc** (computed) |
| `spanf1.c:168–169` | `finddocscontainingsp`: docspace search range | 0 | **DOCISPAN=4**, **1** |
| `do1.c:395` | `filter_vspanset_to_text_subspace`: constant 1.0 | 0 | **1** |
| `context.c:194,200,286` | context window arithmetic | 0 | computed offsets |
| `insert.c:89,94` | crum boundary tracking | 0 | textlength, remainingroom |
| `credel.c:511` | width update | 2 | **1** |
| `insertnd.c:179,181,182` | POOM node second-cut positioning | -1, 0, 1 | **1**, computed, **1** |
| `test.c:877` | test loop counter | 0 | **1** |

---

### Summary: Answer to the Question

**bint=1 is the universal case for all structural ISA-allocation levels** — nodes/servers, accounts, documents, and versions. Every call in `findisatoinsertnonmolecule` [granf2.c:213, 237, 240] uses bint=1 regardless of depth. The `depth` parameter controls the *position* in the tumbler (rightshift), not the *amount* of increment.

**bint>1 appears only in these contexts:**

1. **Content element level** (`inserttextgr` [granf2.c:100]): `bint = textset->length` — advances the granfilade LSA by actual character count.

2. **Atom ISA bound computation** (`findisatoinsertmolecule` [granf2.c:162, 166, 171]): `bint = atomtype+1` (2 or 3) and `bint = atomtype` (1 or 2) — used to compute the **search window bounds** to find where to place the next atom, not to advance the allocated address itself.

3. **V-space (VSA) construction** (do2.c, sporgl.c, orglinks.c, spanf1.c): `bint ∈ {2, 3, 4, DOCISPAN=4, whichend}` — constructing virtual-address-space coordinates and search ranges, not ISA allocation.

There is no structural-level (server/account/document/version) allocation site anywhere in the codebase where bint>1 is passed to `tumblerincrement`. The distinction is clean: **structural levels always use bint=1; only content (text bytes) and V-space coordinate construction use bint>1**.