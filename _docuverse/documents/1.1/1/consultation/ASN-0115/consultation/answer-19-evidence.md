## Question 19 [evidence]

> If a SpecSet crosses into the link subspace (`2.x` internally), does content delivery return link-orgl I-address bytes, or is delivery restricted to text subspace `1.x`?

## KB Synthesis

## Content Delivery with a Cross-Subspace SpecSet

**Delivery is not restricted to 1.x.** The system will attempt to deliver bytes for link-subspace spans, but what it returns is garbage or NULL — silently.

### The call chain

`retrieve_contents` → `doretrievev` → `specset2ispanset` → `ispanset2vstuffset(granf, ispanset)`.

`ispanset2vstuffset` is typed to the permascroll: it treats every I-address in the ispanset as a permascroll address and looks up raw bytes. It has no type awareness — it receives tumblers, not tagged values [SS-DUAL-ENFILADE, Finding 0011].

### What happens at the 2.x entries

When the SpecSet covers a V-position in the link subspace (internal `2.x`), `specset2ispanset` converts it to the link-orgl ISA stored there (e.g., `1.1.0.1.0.1.0.2.1`). That ISA is a **link orgl structure address**, not a permascroll content address — a fundamentally different I-address sort [SS-CONTENT-IDENTITY, Finding 0009].

`ispanset2vstuffset` then queries the permascroll/granfilade for that ISA. The lookup finds no permascroll atom at that address and returns NULL or garbage bytes. No error is raised; the result is silently corrupt [PRE-RETRIEVE-CONTENTS, Finding 0010]:

```
V 2.x → link ISA 1.1.0.1.0.2
ispanset2vstuffset(granf, {1.1.0.1.0.2}) → NULL/garbage
Result delivered to client: corrupt bytes mixed with any valid text
```

### No runtime guard exists

`acceptablevsa()` in `do2.c:110-113` unconditionally returns TRUE [INV-SUBSPACE-CONVENTION, Finding 0010]. There is no subspace filter in the retrieve path. [EC-RETRIEVE-VSPANSET-BOTH-SUBSPACES] documents this as the root cause of silent corruption when callers use the full `retrieve_vspanset` output as input to `retrieve_contents`.

### Summary

| V-span subspace | I-address type | `ispanset2vstuffset` result |
|-----------------|---------------|----------------------------|
| 1.x (text) | Permascroll address | Correct bytes |
| 2.x (link) | Link-orgl ISA | NULL / garbage, no error |

The spec precondition for `retrieve_contents` must therefore require that all V-positions in the SpecSet fall within the text subspace (`V.mantissa[0] == 1`) [PRE-RETRIEVE-CONTENTS, Finding 0027]. The implementation does not enforce this — it is caller responsibility.

---

## Code Exploration

Now I have everything I need to give a precise, code-grounded answer.

---

## Does Content Delivery Return Link-Orgl I-Address Bytes If a SpecSet Crosses Into 2.x?

**Yes. The general content delivery path is fully subspace-blind.** Link-orgl I-address bytes are returned without restriction when a SpecSet's V-span crosses into 2.x. The only subspace filter in the codebase does not apply to the general retrieve path, and does not even exclude 2.x content when it does apply.

---

### 1. The V-Space Layout

Two functions establish the internal subspace boundaries with no ambiguity:

**`findvsatoappend`** (orglinks.c:29–48):
```c
tumblerclear (&linkspacevstart);
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart); /* level-0 digit = 2 */
```
Link space starts at V = 2. Text content lives at V < 2 (starting at V = 1.1); link-orgl ISA references live at V ≥ 2.

**`findnextlinkvsa`** (do2.c:151–166):
```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink); /* 2   */
tumblerincrement (&firstlink, 1, 1, &firstlink); /* 2.1 */
```
The first link-orgl reference in any document is placed at V = 2.1. Each subsequent link increments from there. Equivalently, `setlinkvsas` (do2.c:169–183) confirms: within a link's own orgl, the from-endpoint lives at V = 1.1 and the to-endpoint at V = 2.1.

So the internal map is:

| V range | Contents |
|---------|----------|
| V < 1.0 | Empty in all normal documents |
| V = 1.x | Text content (starts at 1.1) |
| V = 2.x | Link-orgl ISA bytes (starts at 2.1) |

---

### 2. The Content Delivery Path Is Subspace-Blind

The full call chain for a retrieve request (FEBE → `fns.c` → `do1.c`) is:

```
fns.c:175  retrievev()
  → do1.c:338  doretrievev(taskptr, specset, vstuffsetptr)
    → do2.c:14  specset2ispanset(taskptr, specset, &ispanset, READBERT)
      → do2.c:36  vspanset2ispanset(taskptr, docorgl, vspanset, ispansetptr)   [orglinks.c:397]
        → orglinks.c:401  permute(..., V, ..., I)
          → orglinks.c:415  span2spanset(taskptr, orgl, span, V, target, I)
            → orglinks.c:435  retrieverestricted((typecuc*)orgl, span, V, NULL, I, NULL)  [retrie.c:56]
              → retrie.c:83  retrieveinarea(...)
                → retrie.c:97  findcbcinarea2d(crumptr, offset, span1start, span1end, index1,
                                               span2start, span2end, index2, &context, infoptr)
```

`findcbcinarea2d` (retrie.c:229–268) is the bottom of the retrieval stack. It recurses through the POOM tree calling `crumqualifies2d` (retrie.c:270–305) on each node:

```c
/* retrie.c:282–300 */
endcmp = iszerotumbler (span1end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span1end, index1);
if ( endcmp <=/*=*/ ONMYLEFTBORDER) return(FALSE);
startcmp = whereoncrum (crumptr, offset, span1start, index1);
if( (startcmp > THRUME)) return(FALSE);

endcmp = iszerotumbler (span2end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span2end, index2);
if ( endcmp < ONMYLEFTBORDER) return(FALSE);
startcmp =  whereoncrum (crumptr, offset, span2start, index2);
if( (startcmp > THRUME)) return(FALSE);

return (TRUE);
```

This is pure 2D geometric intersection on `(V, I)` bounds. There is **no subspace predicate, no check of V against any threshold, no discrimination between text crums and link-orgl crums**. Whatever crum geometrically overlaps the query rectangle qualifies.

When a V-span that includes V = 2.x is passed in, crums holding link-orgl ISA bytes at those positions qualify, their I-spans are collected via `makecontextfromcbc`, and the result passes back up through `permute` as I-address spans. The final `ispanset2vstuffset` call in `doretrievev` then retrieves the raw bytes at those I-addresses from the granfilade — which are the tumbler-encoded link ISA bytes.

---

### 3. The Only Subspace Filter Does Not Apply Here

There is exactly one function in the entire codebase that filters by subspace:

**`filter_vspanset_to_text_subspace`** (do1.c:386–411):
```c
/* Bug 009 SEMANTIC FIX: Filter vspanset to text subspace only (V >= 1.0). */
tumblerclear(&text_subspace_start);
tumblerincrement(&text_subspace_start, 0, 1, &text_subspace_start); /* text_subspace_start = 1.0 */

for (; vspanset; vspanset = vspanset->next) {
    if (tumblercmp(&vspanset->stream, &text_subspace_start) >= EQUAL) {
        /* This span is in text subspace - keep it */  /* line 400 */
        ...
    }
    /* Spans with stream < 1.0 are in link subspace - skip them */  /* line 408 */
}
```

**Two problems with this filter relative to the question:**

**Problem 1 — It is only called from `doshowrelationof2versions`** (do1.c:428–449):
```c
filter_specset_to_text_subspace(taskptr, version1);   /* do1.c:440 */
filter_specset_to_text_subspace(taskptr, version2);   /* do1.c:441 */
```
The general `doretrievev` path (do1.c:338–346) calls no such filter. The filter is entirely absent from the retrieve chain traced in §2 above.

**Problem 2 — Even within `doshowrelationof2versions`, the filter does not exclude 2.x content.** The threshold is V ≥ 1.0. Since the link subspace occupies V = 2.x, which satisfies V ≥ 1.0, link-orgl spans in the 2.x region pass through the filter unchanged. The comment at do1.c:377–385 describes filtering "link references at V-position 0.x", but the code confirms via `findnextlinkvsa` and `findvsatoappend` that link-orgl references actually live at V = 2.x, which is above the filter threshold. The filter catches nothing in the 2.x range.

---

### 4. `doretrievedocvspanset` Exposes the Link Subspace Span

When a client calls `retrieve_doc_vspan_set`, it calls `doretrievedocvspanset` (do1.c:322–336) → `retrievevspansetpm` (orglinks.c:173–221). That function explicitly returns **both** the text vspan and the link vspan when a document contains links:

```c
/* orglinks.c:216–217 */
putvspaninlist (taskptr, &vspan,     vspansetptr);  /* text vspan  */
putvspaninlist (taskptr, &linkvspan, vspansetptr);  /* link vspan  */
```

A client that uses the returned vspan directly as a SpecSet for `retrieve_v` will therefore receive I-address bytes for both text content and link-orgl ISA bytes.

---

### Conclusion

Content delivery is not restricted to text subspace 1.x. If a SpecSet's V-span crosses into 2.x, `doretrievev` returns I-address spans covering the link-orgl ISA bytes stored at those V-positions. The retrieval stack (`findcbcinarea2d`, retrie.c:229) is a pure geometric 2D intersection with no subspace discrimination. The only subspace filter in the codebase (`filter_vspanset_to_text_subspace`, do1.c:386) is confined to `doshowrelationof2versions` and — even there — does not exclude the 2.x link subspace, since its threshold is V ≥ 1.0.
