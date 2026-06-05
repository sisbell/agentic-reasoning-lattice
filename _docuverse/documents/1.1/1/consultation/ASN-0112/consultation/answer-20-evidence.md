## Question 20 [evidence]

> Is the start position the operation returns the grasp (offset + displacement) at the POOM root, and does that grasp necessarily coincide with an actual occupied V-address, or can it point into an unoccupied gap?

## KB Synthesis

Two separate questions are embedded here: (1) what the start value is mechanically, and (2) whether it maps to occupied content.

## What the grasp is mechanically

For 2D enfilades (POOM), the root's `cdsp.dsas[V]` is not a static pointer — `setwispnd` continuously maintains it as the **minimum V-dimension displacement** across all content in the tree [SS-ENFILADE-TREE Finding 0066]:

> `setwispnd` finds `mindsp = min(child.cdsp)`, absorbs it into `root.cdsp`, and adjusts children to relative positions. So `root.cdsp` always equals the minimum absolute V-address stored in the tree.

The grasp at any node during retrieval is `grasp = offset + ptr->cdsp` [SS-WHEREONCRUM Finding 0062], accumulating ancestors. At the root, `offset = 0`, so `grasp(root) = root.cdsp = min_vaddr(tree)`.

## Does the grasp coincide with an actual occupied address?

**Yes, the root's grasp IS the minimum occupied V-address** — by construction, `setwispnd` derives it from actual content displacements, not an arbitrary structural value. For a non-empty POOM, some crum exists at that minimum position.

**However, the implied range [grasp, grasp + cwid] is a bounding box, not a contiguity guarantee.** This is the critical distinction.

RETRIEVEDOCVSPAN (opcode 14) reads `(root.cdsp, root.cwid)` raw — it returns the bounding box directly via `retrievevspanpm()`. For a document with both text (1.x) and links (2.x):

> RETRIEVEDOCVSPAN returns `1.1 for 1.2` — a width spanning both subspaces. The gap between the 1.x text subspace and the 2.x link subspace contains no occupied V-addresses. [EC-VSPAN-MISLEADING-SIZE Findings 0017, 0035]

So the **start** of that bounding span coincides with an occupied address (the leftmost text position), but positions within [grasp, grasp+cwid] that fall in the inter-subspace gap are unoccupied.

RETRIEVEDOCVSPANSET (opcode 1) avoids this by calling `retrievevspansetpm()` which uses `is1story` to detect multi-subspace structure and produces separate per-subspace spans [SS-VSPAN-VS-VSPANSET Finding 0035]. Each sub-span's start and extent cover only actual occupied content — no gaps.

## Edge: empty documents

`isemptyenfilade` for 2D types checks both `cdsp = 0` AND `cwid = 0` [SS-ENFILADE-TREE Finding 0066]. An empty POOM has `root.cdsp = 0, root.cwid = 0` — the grasp points to the zero tumbler, which has no occupied content behind it. This is the degenerate case where the grasp does not correspond to any actual V-address.

## Summary

| Operation | Start value | Occupied? |
|-----------|-------------|-----------|
| RETRIEVEDOCVSPAN on text-only doc | min occupied 1.x address | Yes, and range fully occupied |
| RETRIEVEDOCVSPAN on text+link doc | min occupied 1.x address | Start yes; bounding span has gaps |
| RETRIEVEDOCVSPANSET (per-subspace) | min occupied address per subspace | Yes, each sub-span fully occupied |
| Empty document (either op) | zero tumbler | No content exists |

The root grasp equals the minimum occupied V-address, but the bounding span it anchors (`root.cdsp` to `root.cdsp + root.cwid`) can pass through unoccupied V-address ranges between subspaces. [SS-ENFILADE-TREE], [EC-VSPAN-MISLEADING-SIZE], [SS-VSPAN-VS-VSPANSET], [SS-DUAL-ENFILADE]

---

## Code Exploration

Now I have everything I need. The `wisp.c:setwispnd` implementation is the critical piece.

---

## Answer: Start Position, POOM Root Grasp, and Gap Safety

### Part 1: Is the returned start position the root's grasp?

**Yes.** Two retrieval functions both read `cdsp.dsas[V]` directly from the root POOM node and return it as `vspan.stream`:

`orglinks.c:159`:
```c
movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);  /* retrievedocumentpartofvspanpm */
```
`orglinks.c:169`:
```c
movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);  /* retrievevspanpm */
```

`prologuend` defines grasp as `offset + ptr->cdsp` [retrie.c:336]:
```c
dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
```

The root (fullcrum) is always entered with offset cleared to zero — confirmed in three places: `edit.c:38`, `insertnd.c:138`, `retrie.c:19`:
```c
clear (&offset, sizeof(offset)); /* fullcrum alway has zero offset */
```

Therefore `grasp.dsas[V] = 0 + root->cdsp.dsas[V] = root->cdsp.dsas[V]`, and `vspan.stream` is exactly the grasp at the POOM root.

---

### Part 2: Does that grasp necessarily coincide with an occupied V-address?

**Yes — the grasp is always occupied.** The mechanism is `setwispnd` in `wisp.c:171–228`, which is driven by `setwispupwards` after every insert and delete.

**`setwispnd` computes the root `cdsp` as the component-wise minimum of its children's `cdsp`:**

```c
/* find new upper-left corner */
movewisp (&ptr->cdsp, &mindsp);                                         /* wisp.c:193 */
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro (ptr)) {
    lockmin ((tumbler*)&mindsp, (tumbler*)&ptr->cdsp, (tumbler*)&mindsp, /* wisp.c:195 */
             (unsigned)dspsize(ptr->cenftype));
}
```

Then:
```c
dspadd (&father->cdsp, &mindsp, &newdsp, (INT)father->cenftype);       /* wisp.c:200 */
...
movewisp (&newdsp, &father->cdsp);                                       /* wisp.c:224 */
```

`setwispupwards` [wisp.c:83–111] propagates this bottom-up after every modification:
- After insert: `setwispupwards(fullcrumptr, 0)` [insertnd.c:56] and `setwispupwards(father, 1)` [insertnd.c:171]
- After delete: `setwispupwards(father, 1)` [edit.c:74]

By induction, the root's `cdsp.dsas[V]` converges to the **absolute minimum V-start across all bottom crums**. That minimum is the actual V-address where the leftmost content crum begins — an occupied position by definition.

---

### The Nuance: The *Width* Can Span Gaps

While the **start** is always occupied, the bounding box **can contain internal gaps**. `setwispnd` sets the root's width as:

```c
lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid, (tumbler*)&tempwid, ...);  /* wisp.c:213 */
lockmax((tumbler*)&newwid, (tumbler*)&tempwid, (tumbler*)&newwid, ...);         /* wisp.c:214 */
```

This is `max(child.cdsp + child.cwid)` — the right-most reach — not the sum of occupied intervals. The width covers the range from first to last content, which may have holes.

`makegappm` [insertnd.c:162] deliberately creates internal V-gaps by shifting crums:
```c
tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
```

This only fires when `grasp <= origin < reach` [insertnd.c:141–143], i.e., when inserting inside the current document span. After this, the range `[origin, origin+width)` is an unoccupied gap within the document's bounding box.

---

### Summary

| | Claim | Evidence |
|---|---|---|
| `vspan.stream` = root grasp? | **Yes** | `orglinks.c:159,169`; offset always 0 [edit.c:38, insertnd.c:138, retrie.c:19] |
| Grasp = occupied V-address? | **Yes** | `setwispnd` [wisp.c:193–224] keeps root `cdsp.dsas[V]` = global min V-start of content |
| Total span gap-free? | **No** | `makegappm` [insertnd.c:162] shifts crums to create internal gaps; `cwid` is a bounding box, not packed extent |

The returned `vspan.stream` is the V-address of the first (lowest) content crum — always occupied. The returned `vspan.width` defines a bounding box that covers from first to last content and **routinely contains unoccupied gaps** created by insertions inside existing content.
