## Question 20 [evidence]

> The KB records that compare_versions crashes when either document contains link orgls in its POOM (EC-COMPARE-CRASH) — what specific assumption in correspond.c breaks on link-subspace entries: the I-address structure of link orgls, the V-width/I-width exponent encoding, or the subspace boundary in the traversal cuts?

## KB Synthesis

## What Breaks in `correspond.c` on Link-Subspace Entries

The crash comes from the **I-address structure of link orgls**, not from V-width/I-width exponent encoding or subspace traversal cuts. Here is the precise chain of failure:

### The Two I-Address Sorts are Incomparable

[SS-CONTENT-IDENTITY, Finding 0009] establishes that there are two structurally distinct I-address sorts:

- **Permascroll I-addresses** (e.g., `2.1.0.5.0.123`) — start in the `2.x` node range, dereference to content bytes, shareable across documents via transclusion.
- **Link orgl ISAs** (e.g., `1.1.0.1.0.2`) — start in the `1.x` document address range, dereference to link orgl structures, unique per link, never shareable.

These two sorts live in completely disjoint tumbler ranges. Intersection over link ISAs vs. permascroll addresses will always be empty — not a partial match, but zero matches by construction.

### `permute()` Is Type-Agnostic

[SS-SUBSPACE-CONVENTION, Finding 0009] confirms that `vspanset2ispanset` → `permute()` performs the V-to-I conversion without any type tag or sort discrimination. When `correspond.c` feeds in V-spans covering both subspaces (because `retrievedocvspanset` returns both [EC-RETRIEVE-VSPANSET-BOTH-SUBSPACES]), the link subspace's `2.x` V-positions produce link ISAs alongside the permascroll addresses from `1.x` positions. The permute layer has no mechanism to flag or segregate these.

### The Nested Loop Assumes At Least One Match

[EC-COMPARE-VERSIONS-LINK-CRASH, Finding 0009] identifies the exact structural assumption that breaks:

> "The nested loop structure in `correspond.c` assumes each ispan matches at most one vspec, which the link subspace violates."

More precisely, the loop cannot gracefully handle the **zero-match case** — an ispan derived from a link ISA that intersects with nothing in the other document's I-address set. The algorithm's control flow either dereferences a null pointer or exhausts a list it assumed to be non-empty, triggering the fatal abort via `qerror()` [EC-ERROR-ABORT].

### Why Not the Other Two Candidates

**V-width/I-width exponent encoding** ([SS-POOM-BOTTOM-CRUM], [SS-INSERT-VWIDTH-ENCODING]) is an encoding detail specific to POOM bottom-crum creation during INSERT. `correspond.c` is a read path — it queries existing V-to-I mappings; it never constructs POOM crums. The asymmetric exponent representation is irrelevant here.

**Subspace boundary in traversal cuts** ([SS-TWO-BLADE-KNIFE]) is the knife mechanism used by `makegappm()` during INSERT to restrict which POOM entries get shifted. The two-blade knife is entirely an insertion primitive; `correspond.c` uses no knife cutting at all during version comparison.

### Summary

The assumption `correspond.c` cannot satisfy is: *every I-span produced by V-to-I conversion has at least one counterpart in the other document's I-span set*. For permascroll I-addresses this holds whenever content is shared [ST-COMPARE-VERSIONS]. For link ISAs it can never hold — link ISAs are unique identities ([INV-LINK-PERMANENCE], [SS-CONTENT-IDENTITY, Finding 0015]) living in a different address range, so the intersection is structurally empty. The loop's failure to handle empty intersection is the crash site. This is why [PRE-COMPARE-VERSIONS] requires filtering to the text subspace before entering the comparison algorithm: the subspace filter is not a workaround but the **semantically correct precondition**, since I-span intersection is only defined over commensurable I-address sorts [FC-SUBSPACE].

---

## Code Exploration

Good — I now have the full confirmed code in front of me. Writing the analysis.

---

<analysis>

## Which assumption in `correspond.c` breaks on link-subspace entries

### What `setwispnd` does to the POOM after a link is inserted

After `insertpm` places two crums in the document POOM — a text crum at `vsaptr=1.1` with `cdsp.dsas[V]=1.1, cwid.dsas[V]=0.16`, and a link-reference crum at `vsaptr=2.1` with `cdsp.dsas[V]=2.1, cwid.dsas[V]=0.1` — `setwispnd` runs [wisp.c:171–228]:

```c
/* find mindsp = minimum of all sons' cdsp */
movewisp (&ptr->cdsp, &mindsp);           // mindsp ← 1.1
for (ptr = getrightbro(ptr); ...) {
    lockmin(...mindsp...ptr->cdsp...);    // mindsp = min(1.1, 2.1) = 1.1
}
/* lift father by mindsp, subtract mindsp from every son */
dspadd (&father->cdsp, &mindsp, &newdsp, ...);    // father.cdsp ← 0 + 1.1 = 1.1
...
for (ptr = findleftson(father); ...) {
    dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, ...);  // son.cdsp -= 1.1
    /* father.cwid = MAX(son.cdsp + son.cwid) */
    lockadd(son.cdsp, son.cwid, &tempwid, ...);
    lockmax(&newwid, &tempwid, &newwid, ...);
}
```

After normalization:
- Text son: `cdsp.dsas[V] = 1.1 − 1.1 = 0`, `cwid.dsas[V] = 0.16`; absolute V-range **[1.1, 1.17)**
- Link son: `cdsp.dsas[V] = 2.1 − 1.1 = 1`, `cwid.dsas[V] = 0.1`; absolute V-range **[2.1, 2.2)**
- Root: `cdsp.dsas[V] = 1.1`, `cwid.dsas[V] = max(0+0.16, 1+0.1) = 1.1`

Root cwid = `{mantissa=[1,1,...], exp=0}` — a **two-story tumbler**. `is1story(1.1)` = FALSE.

### What `retrievevspansetpm` produces from the two-story cwid

[orglinks.c:196–220], two-story branch:

```c
linkvspan.stream = ccptr->cwid.dsas[V];
linkvspan.stream.mantissa[1] = 0;    // keep first digit only → 1
tumblerjustify(&linkvspan.stream);
linkvspan.width  = ccptr->cwid.dsas[V];
linkvspan.width.mantissa[1]  = 0;    // → 1
...
maxtextwid(taskptr, ccptr, &voffset, &maxwid);
vspan.stream = 0;
vspan.width  = maxwid;
vspan.width.mantissa[0] = 0;         // keep second digit only → 0.1 (approx)
```

Synthetic vspanset returned to the client: **`{at 0 for 0.1}` and `{at 1 for 1}`**.

### What the traversal cuts find when those spans are queried

`specset2ispanset` → `vspanset2ispanset` → `retrieverestricted` → `findcbcinarea2d` → `crumqualifies2d` [retrie.c:270]:

```
whereoncrum(root, offset=0, address=0.1, V):
  left  = offset.dsas[V] + root.cdsp.dsas[V] = 0 + 1.1 = 1.1
  cmp   = tumblercmp(0.1, 1.1) = LESS → TOMYLEFT
endcmp = TOMYLEFT (-2) ≤ ONMYLEFTBORDER (-1) → return FALSE
```

The root doesn't even qualify for the `{0, 0.1}` query. **No crums are found for the link-subspace synthetic span.** No link-ISA I-spans are added to `version1ispans`.

For `{1, 1}` (V=[1, 2) absolute): root qualifies (its range is [1.1, 2.2)); text son qualifies (absolute V=[1.1, 1.17) ⊂ [1, 2)); link son at absolute V=2.1 **does not** qualify (`crumqualifies2d` computes son's absolute left border = 1.1+1 = 2.1 > 2 = query end → `TOMYLEFT` → FALSE).

So `version1ispans` = text permascroll I-spans only.

### The assumption in `correspond.c` that breaks

The broken assumption is in `restrictvspecsetovercommonispans` [correspond.c:74–79]:

```c
docvspanset = NULL;
if(ispan2vspanset(taskptr,versionorgl,ispanset,&docvspanset)){
    s1=(typevspec *)taskalloc(taskptr,sizeof(typevspec ));
    ...
    s1->vspanset = docvspanset;   /* ← may be NULL */
}
```

**The assumption:** if `ispan2vspanset` returns truthy, then `docvspanset` has been populated with valid V-spans.

**Why it breaks for link-subspace entries:** `ispan2vspanset` [orglinks.c:388–393] calls `permute`, which [orglinks.c:404–421] does:

```c
typevspanset *save;
save = targspansetptr;         /* save = address of docvspanset */
for (; ispanptr; ...) {
    span2spanset(taskptr, ccptr, ispanptr, targspansetptr, fromdim, todim);
    targspansetptr = &(*targspansetptr)->next;
}
return (save);                  /* ALWAYS returns the saved address — never NULL */
```

`permute` returns `save`, which is the address of the local `docvspanset` variable in the caller — a **stack address, permanently non-NULL**. If `retrieverestricted` finds no crums (as happens when the query V=[0, 0.1) is below the POOM's entire V-range), `span2spanset` does not update `*targspansetptr`, leaving `docvspanset = NULL`. The always-truthy return of `ispan2vspanset` then allows the condition at line 74 to succeed, and `s1->vspanset = NULL` is stored.

This propagates to `removespansnotinoriginal` [correspond.c:116]:

```c
if (intersectspansets (taskptr,
    ((typevspec *)new)->vspanset,
    ((typevspec *)old)->vspanset,   /* ← NULL if Bug 2 triggered */
    &newspanset, VSPANID)) {
```

Before the null-guard fix at [correspond.c:163–169], `intersectspansets` calls `gerror("")` → `abort()` when given a NULL input.

### Why the I-address structure is the specific assumption that breaks

The **subspace boundary in the traversal cuts** is working correctly: `crumqualifies2d` accurately identifies that V=[0, 0.1) contains no POOM crums and returns FALSE. The problem is not a failure of the cuts.

The **V-width/I-width exponent encoding** [orglinks.c:115–117] is what determines that link-reference crums land at V=2.1 (absolute) rather than V=0.x — but this encoding is internal to `insertpm` and `setwispnd`; `correspond.c` never reads it directly.

What `correspond.c` does depend on — and gets wrong — is the **I-address structure of link orgls**. The code assumes that for every I-address domain appearing in a document's POOM (permascroll for text, link-orgl ISA for link references), the `ispan2vspanset` call will either:

- (a) correctly return falsy, indicating failure, OR
- (b) correctly return truthy with a non-NULL `docvspanset`

Link orgls use deep hierarchical ISAs (e.g., `1.1.0.1.0.2`) — a completely different address domain from flat permascroll offsets. When the synthetic link-subspace span queries V=[0, 0.1), no crums are found in that range (`crumqualifies2d` correctly rejects them), so `span2spanset` leaves `docvspanset = NULL`. The I-address structure of link orgls is why the backward I→V lookup cannot be completed: the query range in the synthetic vspanset (V=[0, 0.1)) does not correspond to where link-reference crums actually live in the POOM (V=[2.1, 2.2) absolute). The `ispan2vspanset` wrapper does not surface this failure — it returns the always-truthy `save` pointer regardless — and `correspond.c:74` treats that as success.

The "clearly wrong" comment at [correspond.c:222] documents a second pathology — tumbler subtraction is performed in wrong order for cross-subspace span pairs — but this is downstream of the primary assumption failure: bogus results from `spanintersection` would only matter if link-ISA I-spans reached `intersectspansets` as part of `commonispans`, which the I-address domain separation (no shared link-ISA I-spans between a document with a link and a version without one) prevents in the reproduction scenario. The SIGABRT in the reproduction was from Bug 0020's `sons[MAXUCINLOAF]` overflow in `recombinend` during the version-creation step preceding comparison; the correspond.c bugs (nested-loop iterator exhaustion at line 65–66; return-value misuse at line 74) would cause the described NULL-vspanset crash independently under the right input conditions.

</analysis>

<summary>

**The broken assumption is the I-address structure of link orgls.**

`correspond.c:74` assumes `ispan2vspanset`'s truthy return implies a populated `docvspanset`. It breaks because `ispan2vspanset` → `permute` [orglinks.c:421] always returns `save` — the stack address of the output pointer — regardless of whether any V-spans were found. When the synthetic link-subspace span `{0, 0.1}` is processed, `retrieverestricted` queries V=[0, 0.1) in the POOM; `crumqualifies2d` [retrie.c:270] correctly rejects the root (its absolute left border is at V=1.1 > 0.1) and returns nothing. `span2spanset` leaves `docvspanset = NULL`. `ispan2vspanset` returns truthy anyway. `s1->vspanset = NULL` is stored. `removespansnotinoriginal` then passes this NULL to `intersectspansets`, which calls `gerror("")` → `abort()`.

The traversal cuts (option 3) are working correctly — `crumqualifies2d` accurately identifies the empty V=[0, 0.1) range. The V-width/I-width exponent encoding (option 2) is what places link-reference crums at absolute V=2.1, outside the synthetic query range, but that encoding is never directly read by `correspond.c`. What `correspond.c` assumes — and what is wrong — is that `ispan2vspanset` can signal "no V-spans found" via its return value. For link orgls specifically, whose ISAs occupy a different address domain from permascroll text, this backward I→V lookup silently produces a NULL `docvspanset` behind a permanently-truthy return pointer.

</summary>
