## Question 1 [evidence]

> When a document's entire content subspace is deleted while one or more link positions remain, does the implementation permit that state, and does the reported origin (root V-displacement) then become the link minimum `[s_L,1,…,1]` — and does deleting content in the content-maximal case retreat the reported reach/width by the corresponding ordinal steps?

## KB Synthesis

## Answer

**Yes — this state is fully permitted.**

[SS-ADDRESS-SPACE] Finding 0024 documents it explicitly: after deleting all text from a document that contains links, the vspanset still reports the link span. The document is not considered empty. [ST-DELETE] Finding 0024 states the postcondition directly: "deletion removes content from the V-stream but preserves link objects in the 2.x subspace."

---

**Yes — the root V-displacement retreats to the link minimum.**

[SS-ENFILADE-TREE] Finding 0066 establishes the mechanism: in 2D enfilades (POOM is 2D), `root.cdsp` dynamically tracks the **minimum tumbler address** across all children, maintained by `setwispnd` after every modification. Once all text crums (at 1.x, which are numerically smaller than 2.x in tumbler order) are removed, the minimum remaining address becomes the first link position — 2.1. `setwispnd` absorbs this as the new root displacement.

[SS-DUAL-ENFILADE] Finding 0038 gives the direct empirical confirmation:

```
retrievedocvspanset output (document has links only, no text):
  [{"start": "2.1", "width": "0.1"}]
  Links reported at actual internal position 2.x
```

This contrasts with the mixed case, where links are normalized to `"0"` in output with text at `"1"`. The naked 2.1 appears precisely because it is now the root displacement.

---

**Yes, with a subspace-isolation caveat on the "ordinal retreat."**

In the content-maximal case (text + links both present), [SS-VSPAN-VS-VSPANSET] Finding 0017 and 0035 show RETRIEVEDOCVSPAN reports a bounding box spanning both subspaces (e.g., `1.1 for 1.2`), since the raw root cdsp is the text minimum and cwid covers through the link reach.

As text is progressively deleted, two mechanisms govern the retreat:

1. **Text entries shift and shrink** — [ST-DELETE] Finding 0055: Case 2 in `deletend` subtracts the deletion width from subsequent entries' V-displacements (`tumblersub`), and `setwispnd` recalculates root cdsp/cwid. So text-extent reports retreat proportionally to each deletion.

2. **Link entries are immune** — [FC-SUBSPACE] Findings 0054 and 0055 establish two independent protection mechanisms: INSERT uses a deliberate two-blade knife with second blade at the next subspace boundary; DELETE is protected by the `strongsub` exponent guard, which returns the minuend unchanged when `width.exp < entry.vpos.exp`. Text deletion widths (at exponent −1) cannot subtract from link displacements (at exponent 0). Links stay fixed at 2.x throughout.

The upshot: the reported bounding width retreats step-by-step with each text deletion, but exclusively on the text-subspace contribution. When the last text character is removed, the bounding span transitions discontinuously to the link-only report `{"start": "2.1", "width": "0.1"}` — there is no gradual approach from the text minimum toward 2.1, because links never shift. The "ordinal retreat" is monotonically decreasing in the text dimension only.

---

## Code Exploration

I now have everything needed to answer definitively. Let me write the full response.

---

## Analysis: Content Deletion With Surviving Link Positions

### Subspace Layout (V-space)

Before answering the three sub-questions, the relevant V-space geometry must be established. From `setlinkvsas` [do2.c:169-183]:

```c
tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);  // [1,...]
tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);  // [1,1,...] = link FROM minimum
tumblerincrement(tovsaptr,   0, 2, tovsaptr);    // [2,...]
tumblerincrement(tovsaptr,   1, 1, tovsaptr);    // [2,1,...] = link TO minimum
tumblerincrement(threevsaptr,0, 3, threevsaptr); // [3,...]
tumblerincrement(threevsaptr,1, 1, threevsaptr); // [3,1,...] = link THREE minimum
```

Content (text) crums occupy 1-story tumblers (single non-zero mantissa digit). `is1story` [tumble.c:237] returns TRUE for `[1,...]`, `[2,...]`, etc. Link endpoints occupy 2-story tumblers: `[1,1,...]`, `[2,1,...]`, `[3,1,...]`. These are distinct in V-space — a single POOM stores both interleaved.

The classifiers confirm this:
- `istextcrum` [orglinks.c:246-252]: `mantissa[1] == 0` AND `is1story(cwid)` — single-digit V-displacement, 1D width
- `islinkcrum` [orglinks.c:255-261]: `mantissa[0] == 1 && mantissa[1] != 0` — displaced into the [1,n,...] region

So the "link minimum" `[s_L,1,...,1]` referred to in the question is, in practice, `[1,1,...]` — the V-address floor of the FROM-endpoint link subspace.

---

### Question 1: Does the Implementation Permit an Empty Content Subspace with Surviving Links?

**Yes, unconditionally. There is no guard.**

The deletion entry point is `deletevspanpm` [orglinks.c:145-152]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

The **sole guard** is `iszerotumbler(&vspanptr->width)` — a zero-width deletion is rejected. There is no inspection of whether the deleted span contains all content, whether link endpoints exist inside it, or whether the post-deletion POOM would have a content-free V-subspace. The call to `deletend` proceeds, and the function returns TRUE.

`deletend` [edit.c:31-76] then walks the POOM nodes in the deletion range and applies:
- **Case 1** [edit.c:58-60]: entirely enclosed crum → `disown; subtreefree` (crum is destroyed)
- **Case 2** [edit.c:62-63]: boundary crum → `tumblersub(&ptr->cdsp.dsas[index], width, ...)` (displacement adjusted)
- **Case 0** [edit.c:56-57]: crum precedes deletion → untouched

Link crums whose V-addresses fall outside the deleted content range survive case 0 unchanged. After `deletend`, `setwispupwards` [wisp.c:83-110] propagates bound recomputation upward — but this is a geometric recalculation, not a validity check. No error is raised.

Calling code in `dodeletevspan` [do1.c:158-167] also performs no pre-deletion validation of link presence, nor does the FEBE handler `deletevspan` in `fns.c`.

**The empty-content / surviving-link state is fully reachable and silently accepted.**

---

### Question 2: Does the Reported Origin Become the Link Minimum `[s_L,1,…,1]`?

**Answer: Yes via `retrievevspanpm`, but with two distinct behaviors depending on retrieval path.**

#### Path A — `retrievevspanpm` [orglinks.c:165-171] (the simple retrieval)

```c
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler(&((typecuc *)orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler(&((typecuc *)orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

`stream` is the root POOM node's `cdsp.dsas[V]` — whatever displacement value that crum currently holds. This value is **not static**. After every deletion, `setwispupwards` calls `setwispnd` [wisp.c:171-228] which applies the following normalization:

```c
// wisp.c:193-203
movewisp(&ptr->cdsp, &mindsp);                         // mindsp = leftmost child's cdsp
for (ptr = getrightbro(ptr); ptr; ...)
    lockmin(&mindsp, &ptr->cdsp, &mindsp, ...);        // find minimum across all children

if (!lockiszerop) {
    dspadd(&father->cdsp, &mindsp, &newdsp, ...);      // father->cdsp += mindsp
} else {
    movewisp(&father->cdsp, &newdsp);
}
// wisp.c:208-214
for (ptr = findleftson(father); ptr; ...) {
    if (!lockiszerop)
        dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, ...);  // child->cdsp -= mindsp
    lockadd(&ptr->cdsp, &ptr->cwid, &tempwid, ...);
    lockmax(&newwid, &tempwid, &newwid, ...);
}
```

The normalization **absorbs the minimum child displacement into the father's cdsp** and subtracts it from each child's cdsp, so the leftmost child always ends up at relative cdsp = zero. This propagates upward through `setwispupwards`.

After all text crums are deleted and only link crums at absolute V-addresses like `[1,1,...]` remain:
- `mindsp` = minimum child cdsp = the leftmost link crum's relative displacement
- `newdsp` = root's accumulated cdsp is pushed to absorb that offset
- After full propagation, root's `cdsp.dsas[V]` = the absolute V-address of the leftmost surviving point

**The root's `cdsp.dsas[V]` — and therefore the `stream` returned by `retrievevspanpm` — converges to `[1,1,...]`, the minimum of the link subspace.**

This is not coincidental. The POOM normalization invariant ensures the root's displacement always equals the leftmost occupied address. When the leftmost occupied address is a link endpoint at `[1,1,...]`, that IS the root's reported displacement.

#### Path B — `retrievevspansetpm` [orglinks.c:173-221] (the content-maximal retrieval)

This path is dispatched when `is1story(&ccptr->cwid.dsas[V])` is FALSE — i.e., the document's total width is not 1-story, meaning links are present [orglinks.c:184].

```c
if (is1story(&ccptr->cwid.dsas[V])) {
    // text-only: use root cdsp directly
    movetumbler(&ccptr->cdsp.dsas[V], &vspan.stream);    // line 186
    ...
} else {
    // mixed/links present: text origin is ALWAYS zero
    maxtextwid(taskptr, ccptr, &voffset, &maxwid);
    vspan.itemid = VSPANID;
    tumblerclear(&vspan.stream);                          // line 209 — always [0,...]
    movetumbler(&maxwid, &vspan.width);
    vspan.width.mantissa[0] = 0;
    vspan.next = NULL;

    // link span: stream derived from cwid (not cdsp!)
    movetumbler(&ccptr->cwid.dsas[V], &linkvspan.stream); // line 197
    linkvspan.stream.mantissa[1] = 0;
    tumblerjustify(&linkvspan.stream);
    ...
}
```

In this path:
- The **text span** is always reported with `stream = [0,...]` regardless of the root's cdsp. After full content deletion, `maxtextwid` [orglinks.c:224-245] finds no text crums, so `maxwid` stays at its zeroed initial state — reporting width zero.
- The **link span** is computed by stripping the second mantissa digit from the root's `cwid`, not `cdsp`. The link "origin" here is a width-derived quantity, not a displacement-derived one.

**Via this path: the reported text origin is `[0,...]` (always, by design at line 209) and is NOT the link minimum `[1,1,...]`. The link span origin is extracted from `cwid` with a different extraction method.**

The two retrieval paths give structurally different answers. `retrievevspansetpm` is the higher-level path used when content and link spans must be reported separately. Its text origin is always zeroed; this appears deliberate — the code comment at line 192 says "in both cases we have to remove the first digit of the tumbler."

---

### Question 3: Does Deletion in the Content-Maximal Case Retreat Reach/Width by Corresponding Ordinal Steps?

**Yes — reach is recomputed from surviving crums, not decremented by a fixed rule, but the arithmetic is exact ordinal subtraction.**

After `deletend` [edit.c:31-76] processes a deletion range, `setwispupwards` calls `setwispnd` [wisp.c:171-228]. The new width is computed at lines 207-215:

```c
clear(&newwid, sizeof(newwid));
for (ptr = findleftson(father); ptr; ptr = getrightbro(ptr)) {
    if (!lockiszerop) {
        ptr->modified = TRUE;
        dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, ...);
    }
    lockadd(&ptr->cdsp, &ptr->cwid, &tempwid, ...);    // tempwid = child_cdsp + child_cwid
    lockmax(&newwid, &tempwid, &newwid, ...);           // newwid = max(newwid, tempwid)
}
// line 224-225:
movewisp(&newdsp, &father->cdsp);
movewisp(&newwid, &father->cwid);
```

`newwid` is the maximum of `(child_cdsp + child_cwid)` across all surviving children. Each deleted crum simply ceases to contribute. Boundary crums (case 2 in `deletend`) have their cdsp adjusted by `tumblersub` — exact tumbler subtraction — so the remaining crum's right extent contracts by exactly the deleted ordinal interval.

The link between deletion and reach is direct: `doretrievedocvspan` returns the root's `cdsp + cwid`, which after `setwispnd` is the absolute right edge of the rightmost surviving crum. For the content-maximal case, `findnextlinkvsa` [do2.c:151-167] computes:

```c
doretrievedocvspan(taskptr, docisaptr, &vspan);
tumbleradd(&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp(&vspanreach, &firstlink) == LESS)    // firstlink = [2,1,...]
    movetumbler(&firstlink, vsaptr);
else
    movetumbler(&vspanreach, vsaptr);
```

When content is deleted ordinal step by ordinal step from the right edge:
- Each deletion reduces `vspan.width` by the deleted tumbler extent
- `vspanreach` decreases by the same amount
- As long as `vspanreach ≥ [2,1,...]`, the next-link VSA equals `vspanreach` exactly
- Once `vspanreach < [2,1,...]`, the floor `[2,1,...]` takes over — **the reach cannot be reported below the link minimum**

This floor is the only non-linear behavior. Short of it, reach/width retreats exactly one ordinal step per deleted ordinal step of content, because `tumblersub` is exact arithmetic on tumblers with no rounding.

---

### Summary

| Question | Answer |
|---|---|
| **Permit empty-content / surviving-link state?** | **Yes.** `deletevspanpm` [orglinks.c:145] has only one guard: zero-width deletion rejected. No check for surviving links. |
| **Does reported origin become `[s_L,1,…,1]`?** | **Via `retrievevspanpm`: yes.** `setwispnd` [wisp.c:193-203] propagates minimum child displacement into root's `cdsp`, so root's `cdsp.dsas[V]` = leftmost surviving address = `[1,1,...]` once only link crums remain. **Via `retrievevspansetpm`: no** — text origin is always zeroed [line 209]; link origin is extracted from `cwid`, not `cdsp`. |
| **Does reach/width retreat by ordinal steps?** | **Yes, exactly.** `setwispnd` [wisp.c:207-215] recomputes `cwid` as max of surviving `(child_cdsp + child_cwid)`. Boundary crums are adjusted by exact `tumblersub`. Retreat is one-to-one with deleted ordinal content, except that `findnextlinkvsa` [do2.c:162-163] enforces a floor of `[2,1,...]` — reach cannot drop below the TO-endpoint link minimum. |
