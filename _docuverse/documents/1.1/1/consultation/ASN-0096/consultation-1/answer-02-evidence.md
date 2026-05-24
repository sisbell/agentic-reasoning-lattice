## Question 2 [evidence]

> Which udanax-green operations modify existing I-address coverage in a way that would change projection output (vs. operations that only create fresh addresses or new links)?

## KB Synthesis

Three operations modify existing V→I mappings in the POOM and therefore change projection output. The contrast class — operations that only add new coverage — includes VCOPY, CREATELINK, and CREATENEWVERSION.

---

## Operations that modify existing I-address coverage

### 1. DELETE

DELETE removes V→I mappings from the POOM entirely [ST-DELETE, FC-POOM-MUTABILITY]. The I-addresses remain in the granfilade (immutable) and the spanfilade retains stale DOCISPAN entries [INV-SPANF-WRITE-ONLY], but the document's current V→I projection no longer includes the removed addresses.

Effect on projection output:
- `compare_versions` no longer pairs the deleted I-address ranges — the V-spans simply disappear from the result [ST-DELETE, Finding 0064]
- `retrieve_endsets` / `follow_link` return empty spans for endpoints whose I-addresses were freed from the POOM [EC-GHOST-LINK, Finding 0048]
- `find_documents` still returns the document (stale spanfilade), but I-to-V conversion silently drops the addresses [INV-ITOV-FILTERING, EC-STALE-SPANF-REFERENCE]

### 2. INSERT

INSERT shifts all existing V-positions within the insertion subspace forward by the insertion width [ST-INSERT, FC-SUBSPACE, SS-TWO-BLADE-KNIFE]. The I-addresses are unchanged; the mapping `vpos → iaddr` is replaced by `(vpos + width) → iaddr` for every entry in `[insertion_point, next_subspace_boundary)`.

Effect on projection output:
- `compare_versions` reports different V-span pairings: content after the insertion point appears at higher V-positions in one document versus the other [ST-INSERT, Finding 0030]
- `retrieve_endsets` reports shifted V-positions for any link endpoints that were downstream of the insertion [INV-LINK-CONTENT-TRACKING, Finding 0019]
- The fresh I-addresses inserted are additive (new coverage); the *shifting* of existing entries is the modification

Cross-subspace entries are **not** shifted — the two-blade knife bounds the shift to the insertion subspace [FC-SUBSPACE, SS-TWO-BLADE-KNIFE].

### 3. REARRANGE (pivot / swap)

REARRANGE computes displacement vectors from the cut geometry and applies `tumbleradd` to the V-dimension of each affected POOM entry [ST-REARRANGE, Finding 0056]. I-addresses are completely untouched; only `cdsp.dsas[V]` changes.

Effect on projection output:
- `compare_versions` reports the same I-address matches but with rearranged V-span pairings — content that was at `1.2` may now appear at `1.6` [INV-REARRANGE-IDENTITY, Finding 0018]
- `retrieve_endsets` reports new V-positions for any link endpoints whose content was rearranged [EC-PIVOT-LINK-FRAGMENTATION, Finding 0019]
- Cross-subspace rearrangement (a missing precondition violation) can move text into the link subspace, corrupting further projections [PRE-REARRANGE, EC-REARRANGE-CROSS-SUBSPACE]

---

## The contrast class: operations that only add new coverage

| Operation | What it does | Existing coverage |
|-----------|-------------|-------------------|
| VCOPY / docopy | Adds V→I mappings referencing existing I-addresses at new V-positions | Unchanged [ST-VCOPY, PRE-COPY] |
| CREATELINK | Appends link orgl ISA at `vspanreach` (document end) | Unchanged — no prior entries are shifted [ST-CREATE-LINK, SS-LINK-SUBSPACE] |
| CREATENEWVERSION | Copies source text subspace into a new document's POOM | Source POOM unchanged [FC-VERSION-ISOLATION, ST-VERSION-CREATE] |
| INSERT (fresh I-addresses only) | Allocates new I-addresses in the granfilade | The *new* addresses are additive; the *shift* of existing entries is the modification [FC-GRANF-ON-DELETE, INV-MONOTONIC] |

The fundamental reason VCOPY and CREATELINK leave existing coverage untouched: both append to the POOM without invoking the knife-cut shifting path (`makegappm` exits early for boundary cases, and `findnextlinkvsa` always selects the document end) [SS-WHEREONCRUM, PRE-INSERT Finding 0062].

---

## Code Exploration

Now I have everything I need. Let me write the complete analysis.

---

## Which Operations Modify Existing I-Address Coverage in a Way That Changes Projection Output

### Background: What "projection" means in the code

Projection is the V↔I conversion performed by `permute()` in `orglinks.c:404`, called either as `vspanset2ispanset()` (`orglinks.c:397`) or `ispan2vspanset()` (`orglinks.c:389`). Both call `span2spanset()` → `retrieverestricted()` → `findcbcinarea2d()` in `retrie.c:56-265`, which walks the POOM enfilade looking for crums whose 2D `(I, V)` rectangles intersect the query span.

Each POOM crum stores its origin as `cdsp.dsas[V]` and `cdsp.dsas[I]`, and its extent as `cwid.dsas[V]` and `cwid.dsas[I]`. **Anything that moves, removes, or adds to those crum fields changes projection output.**

---

## Operations That Modify Existing I-Address Coverage

### 1. `dodeletevspan` — removes V→I coverage and shifts subsequent crums

Call path: `fns.c:333-347` → `do1.c:158-167` → `orglinks.c:145-152` → `edit.c:31-76`

```c
// orglinks.c:149
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

`deletend` (`edit.c:31`) calls `makecutsnd` to slice the POOM at the deletion boundaries, then iterates over child crums:

- **Case 1** (`edit.c:59`): crums entirely within the deleted V-range are `disown`ed and freed — their V→I mappings are erased entirely.
- **Case 2** (`edit.c:62-64`): crums to the **right** of (after) the deleted range have their V-displacement decremented:

```c
// edit.c:63
tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

This moves all surviving post-deletion I-address mappings to lower V-addresses. Any caller of `vspanset2ispanset()` using the old V-addresses will now get different (or no) results.

---

### 2. `dorearrange` — displaces V-coordinates of existing crums

Call path: `fns.c:159-173` → `do1.c:34-43` → `orglinks.c:137-142` → `edit.c:78-160`

```c
// orglinks.c:139
rearrangend((typecuc*)docorgl, cutseqptr, V);
```

`rearrangend` (`edit.c:78`) cuts the POOM at 3 or 4 positions and applies per-section offsets computed by `makeoffsetsfor3or4cuts` (`edit.c:163`):

```c
// edit.c:125-127
case 1: case 2: case 3: /* 3 only moves in 4 cuts */
    tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
    ivemodified((typecorecrum*)ptr);
```

Each affected crum gets a new `cdsp.dsas[V]` value. The I-coordinates are unchanged — the same permascroll content now appears at different V-positions. `vspanset2ispanset()` called with the pre-rearrange V-addresses returns wrong (or empty) results; called with the post-rearrange V-addresses, returns content that was previously at a different position.

---

### 3. `doinsert` and `docopy` — shift existing crums via `makegappm` during insertion

Call path for insert:
`fns.c:84-98` → `do1.c:87-123` → `docopy` at `do1.c:45` → `insertpm` at `orglinks.c:75` → `insertnd` at `insertnd.c:15` → `makegappm` at `insertnd.c:124`

Call path for copy:
`fns.c:35-47` → `do1.c:45-65` → same `insertpm` → `insertnd` → `makegappm`

`makegappm` (`insertnd.c:124`) is called only for POOM-type enfilades (line 54: `case POOM: makegappm(...)`) and only when the insertion point falls *within* existing content:

```c
// insertnd.c:140-143
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

When it does run, it cuts the POOM and shifts the V-displacement of all crums with `cdsp.dsas[V] >= insertion point`:

```c
// insertnd.c:162-163
tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
ivemodified (ptr);
```

This is the **same mechanism** as the rearrange shift, but in the positive direction. Existing I-addresses (pre-existing permascroll content already mapped in this document's POOM) now appear at higher V-addresses than before the insertion.

For `doinsert` specifically: `inserttextingranf` allocates brand-new I-addresses in the granfilade (those are fresh), but then `docopy` → `makegappm` shifts the V-mappings of all *pre-existing* I-addresses that come after the insertion point. So `doinsert` is both a fresh-address creator **and** an existing-coverage modifier.

For `docopy`: the I-addresses being inserted are from another document (not fresh). The insertion similarly shifts existing coverage in the target document when the VSA is mid-document.

---

## Operations That Only Create Fresh Addresses or New Links

### `docreatenewdocument` / `docreatenode_or_account`

`do1.c:234-258`. Both call only `createorglingranf` to allocate a new empty POOM entry in the granfilade. No existing POOM is read or written. No coverage exists to modify.

---

### `docreatenewversion`

`do1.c:260-299`. Creates a new granfilade entry, reads the source document's V-span via `doretrievedocvspanfoo` (`do1.c:301-308`), and calls `docopyinternal` to populate the **new** document's POOM:

```c
// do1.c:293
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

`docopyinternal` (`do1.c:66-82`) calls `insertpm` on `newisaptr` (the new document), not on `isaptr` (the original). The source document's POOM crums are read by `specset2ispanset` but never mutated. The original document's I-address coverage is completely untouched.

---

### `docreatelink`

`do1.c:195-221`. This is the subtlest case. It calls `docopy` on the container document to embed the link's ISA:

```c
// do1.c:212
&& docopy (taskptr, docisaptr, &linkvsa, ispanset)
```

The `linkvsa` is computed by `findnextlinkvsa` (`do2.c:151-167`), which places links starting at V = 2.1:

```c
// do2.c:157-158
tumblerincrement (&firstlink, 0, 2, &firstlink);  // V component 0 = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // V component 1 = 1
```

Inside `makegappm` (`insertnd.c:140-143`), the guard condition checks whether the insertion point falls within existing content. Text content lives at V ≥ 1.0; links are inserted at V ≥ 2.1, which is always ≥ the reach of text content. The `tumblercmp(...) != LESS` condition evaluates true, `makegappm` returns `0` immediately, and **no existing text-content crums are displaced**.

The container document's POOM is extended in the link subspace with a fresh mapping (link ISA → 2.x V-address). Existing text I-address coverage — the projection that `doretrievev` uses — is unchanged. (The `filter_vspanset_to_text_subspace` filter at `do1.c:386-427` explicitly excludes the link subspace from version-comparison operations, confirming that link-subspace additions are not considered part of text projection.)

---

## Summary Table

| Operation | Modifies existing V→I crums? | Mechanism | Projection effect |
|---|---|---|---|
| `dodeletevspan` | **Yes** | `deletend` removes crums (case 1) and decrements `cdsp.dsas[V]` (case 2) in `edit.c:59,63` | Deleted range maps to nothing; subsequent content shifts to lower V |
| `dorearrange` | **Yes** | `rearrangend` adds `diff[i]` to `cdsp.dsas[V]` in `edit.c:125` | Same I-addresses appear at new V-positions |
| `doinsert` | **Yes** (for pre-existing crums) | `makegappm` increments `cdsp.dsas[V]` for crums past insertion point in `insertnd.c:162` | Existing post-insertion content shifts to higher V |
| `docopy` (direct) | **Yes** (for pre-existing crums) | Same `makegappm` path | Same shift effect |
| `docreatenewdocument` | No | Only `createorglingranf`, no POOM | No existing POOM touched |
| `docreatenode_or_account` | No | Only `createorglingranf` | No existing POOM touched |
| `docreatenewversion` | No | `docopyinternal` writes only the **new** POOM; source read-only | Source document unchanged |
| `docreatelink` | No (text subspace) | `docopy` at link V-address; `makegappm` exits early because link VSA ≥ text reach | Text projection unchanged; only link subspace extended |

### The shared mutation site

The common thread for all three modifying operations is direct mutation of `ptr->cdsp.dsas[V]` on existing POOM crums:

- **Delete**: `edit.c:63` — `tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index])`
- **Rearrange**: `edit.c:125` — `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])`
- **Insert (gap creation)**: `insertnd.c:162` — `tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V])`

These are the only three places in the codebase that write to `cdsp.dsas[V]` on existing (non-new) crums, and they are what separate the projection-modifying operations from the fresh-address and link-creation operations.
