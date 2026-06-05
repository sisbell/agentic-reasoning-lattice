## Question 19 [evidence]

> Does the type subspace (`3.x`, reserved per SS-ADDRESS-SPACE) ever appear as a third VSpec in the returned span-set, or does RETRIEVEDOCVSPANSET only ever report text and link subspaces?

## KB Synthesis

## Type Subspace (3.x) in RETRIEVEDOCVSPANSET Output

The KB is not fully answerable on this specific question, but the available evidence points in one direction.

**What the KB confirms about 3.x storage:**

`setlinkvsas()` at `do2.c:169-183` stores all three endpoint references internally: FROM at `2.1`, TO at the next 2.x position, and the type endpoint at `3.1` [SS-DUAL-ENFILADE, Finding 0038]. The three-subspace convention — `1` = text, `2` = link, `3` = link type endpoint — is a stored V-space arrangement, not just a conceptual partition [SS-SUBSPACE-CONVENTION, Finding 0038].

**What the KB shows about RETRIEVEDOCVSPANSET output:**

Every concrete RETRIEVEDOCVSPANSET result in the KB shows at most **two spans**:
- Text + link document: `[{start: "0", width: "0.1"}, {start: "1", width: "1"}]` [SS-DUAL-ENFILADE, Finding 0038]
- Links-only document: `[{start: "2.1", width: "0.1"}]` [ibid]
- Text-only document: `[{start: 1.1, width: 0.5}]` [SS-ADDRESS-SPACE, Finding 0024]

No example shows a third span at `3.x`. The `retrievevspansetpm()` description in the KB only characterizes two normalization paths: zeroing mantissa[1] for the link subspace and using `maxtextwid()` for the text subspace [SS-DUAL-ENFILADE, Finding 0038; SS-VSPAN-VS-VSPANSET, Finding 0035].

**Conclusion:**

The KB does not include any retrieval test or code analysis confirming that `3.x` appears in RETRIEVEDOCVSPANSET output. All documented examples show only text and link subspaces. Whether `retrievevspansetpm()` silently merges the type endpoint span into the link span or simply omits it is not derivable from the KB — **this specific question is not fully answerable from the available findings**.

---

## Code Exploration

I have everything I need. Here is the complete answer.

---

## Does RETRIEVEDOCVSPANSET ever return a type-subspace (3.x) VSpec?

**No. It is architecturally impossible.** The function that builds the returned VSpanSet calls `putvspaninlist` exactly twice (or once for pure-text documents), and neither call ever touches a 3.x address.

---

### Code Path

**`fns.c:129-141`** — dispatch:
```c
void retrievedocvspanset(typetask *taskptr)
{
  ...
  if (getretrievedocvspanset(taskptr, &docisa)
   && doretrievedocvspanset(taskptr, &docisa, &vspanset))
      putretrievedocvspanset(taskptr, &vspanset);
```

**`do1.c:322-336`** — thin wrapper:
```c
bool doretrievedocvspanset(typetask *taskptr, typeisa *docisaptr, typevspanset *vspansetptr)
{
  ...
  if (isemptyorgl(docorgl)) { *vspansetptr = NULL; return TRUE; }
  return retrievevspansetpm(taskptr, docorgl, vspansetptr);
}
```

**`orglinks.c:173-221`** — the sole builder of the output VSpanSet:

```c
bool retrievevspansetpm(typetask *taskptr, typeorgl orgl, typevspanset *vspansetptr)
{
  ...
  if (is1story(&ccptr->cwid.dsas[V])) {          /* pure-text document */
      // builds ONE span from text content
      putvspaninlist(taskptr, &vspan, vspansetptr);   // line 189
      return TRUE;
  } else {                                        /* text + links */
      // LINK SPAN: cwid zeroed at mantissa[1], tumblerjustify'd
      linkvspan.stream.mantissa[1] = 0;           // line 198
      tumblerjustify(&linkvspan.stream);
      linkvspan.width.mantissa[1] = 0;            // line 202
      tumblerjustify(&linkvspan.width);

      // TEXT SPAN: maxtextwid result, mantissa[0] zeroed
      maxtextwid(taskptr, ccptr, &voffset, &maxwid);
      vspan.width.mantissa[0] = 0;               // line 211

      putvspaninlist(taskptr, &vspan, vspansetptr);     // line 216
      putvspaninlist(taskptr, &linkvspan, vspansetptr); // line 217
      return TRUE;
  }
}
```

There are exactly **two `putvspaninlist` calls** in the live code (lines 216-217), and one in the pure-text shortcut (line 189). No third call exists.

---

### What the 3.x subspace actually is

`setlinkvsas` in `do2.c:169-183` **does** produce a 3.x V-address — but only as an internal endpoint slot for 3-ended links created via `CREATELINK`:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);   // 1.x — FROM end
    tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);
    tumblerincrement(tovsaptr,   0, 2, tovsaptr);     // 2.x — TO end
    tumblerincrement(tovsaptr,   1, 1, tovsaptr);
    if (threevsaptr) {
        tumblerincrement(threevsaptr, 0, 3, threevsaptr); // 3.x — TYPE end
        tumblerincrement(threevsaptr, 1, 1, threevsaptr);
    }
    return TRUE;
}
```

These addresses are written into the link's internal orgl by `insertendsetsinorgl` and `insertendsetsinspanf` (`do1.c:218-219`). They are **link endpoint storage addresses**, not document content addresses.

The `islinkcrum` predicate (`orglinks.c:255-261`) identifies link crums as `mantissa[0] == 1 && mantissa[1] != 0` (i.e., the 1.n link slots). The `maxtextwid` traversal at `orglinks.c:240` explicitly skips these: `if(ptr && !islinkcrum(ptr))`. A 3.x crum, even if one existed, would be classified neither as a text crum (fails `mantissa[1] == 0` test at `orglinks.c:248`) nor as a recognized link crum (fails `mantissa[0] == 1` test at `orglinks.c:257`).

---

### Conclusion

RETRIEVEDOCVSPANSET returns **at most two VSpans**:

| Span | Built from | Notes |
|------|-----------|-------|
| Text | `maxtextwid` result, `mantissa[0]` zeroed (`orglinks.c:211`) | Only in `else` branch |
| Link | `cwid.dsas[V]` with `mantissa[1]` zeroed (`orglinks.c:198,202`) | Only in `else` branch |

The type subspace (3.x) is a **link-internal V-address** for the third endpoint of 3-ended links. It is allocated by `setlinkvsas` (`do2.c:179-180`), stored by `docreatelink` (`do1.c:217-219`), and **never surfaced by `retrievevspansetpm`**. No constant `TYPESS` or `SS_ADDRESS_SPACE` exists in the C source — the reservation is a protocol convention, not a code invariant.
