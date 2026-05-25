## Question 11 [evidence]

> Why does CREATENEWVERSION exclude the link subspace (internally 2.x) from the copy — was this a deliberate decision to keep links anchored to the home document, or a side effect of doretrievedocvspanfoo extracting only the text span?

## KB Synthesis

The KB evidence points strongly to **side effect, not deliberate design**, with the semantic outcome being coherent regardless.

## Mechanism

`docreatenewversion` calls `doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm`, which reads only `cdsp.dsas[V]` and `cwid.dsas[V]` from the root POOM node. [ST-VERSION-CREATE Finding 0043] That displacement pointer starts at the text subspace (position `1`), not the link subspace (position `2.x`). The link subspace occupies V-positions *structurally before* the recorded displacement — it is outside the vspan this function returns, so it is never passed to `docopyinternal`.

There is no explicit `if (link_subspace) skip` guard anywhere. The exclusion is a consequence of [SS-DUAL-ENFILADE Finding 0043]: the document's primary vspan, as stored in the POOM root, covers the text region only.

## The "kluge" signal

[ST-VERSION-CREATE Finding 0046] notes that `retrievedocumentpartofvspanpm` is self-described as "a kluge" in the source (orglinks.c:155-162). This suggests the code path was not carefully designed for link-awareness — it simply reuses a convenience function that happens to return text extent.

## Why the outcome is still coherent

Even though the link subspace exclusion is incidental, the result is semantically sound:
- Links are not lost — `find_links` still discovers them on the version via shared permascroll I-addresses [INT-LINK-VERSION Finding 0046]
- The version correctly inherits link discoverability through content identity, not through POOM link entries [INT-LINK-TRANSCLUSION Finding 0043]
- Link orgls remain anchored to their home document's address space regardless [SS-LINK-HOME-DOCUMENT]

The bottom line: the link subspace is excluded because `retrievedocumentpartofvspanpm` extracts a text-anchored vspan from the POOM root's displacement field, not because a designer decided links should stay with their home document. The semantic benefit (links discoverable via identity, not POOM inheritance) is a consequence of the content-identity architecture, not the intent behind this specific code path.

---

## Code Exploration

I now have everything needed to give a complete, cited answer. Here it is:

---

## Why CREATENEWVERSION Excludes the Link Subspace

The exclusion is **not an explicit filter**. It is a structural side effect of the kluge implementation in `doretrievedocvspanfoo`, made possible by the deliberate V-space geometry that separates text (1.x) and links (2.x) into different major tumbler levels.

---

### Execution Path

`docreatenewversion` [do1.c:260-299] has two steps that determine what gets copied:

```c
// do1.c:281-293
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {
    return FALSE;
}
vspec.next = NULL;
vspec.itemid = VSPECID;
movetumbler(isaptr, &vspec.docisa);
vspec.vspanset = &vspan;
...
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

`doretrievedocvspanfoo` [do1.c:301-309] — labeled **"a kluge not yet kluged"** — delegates directly to:

```c
// orglinks.c:155-162
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

This returns a **single monolithic vspan**: the root crum's cumulative displacement (`cdsp.dsas[V]`) as the stream and cumulative width (`cwid.dsas[V]`) as the width. The comment "kluge" appears on both the caller and this function — these are provisional implementations.

---

### The V-Space Geometry That Makes It Work

The link exclusion is a consequence of how V-positions are assigned.

**Text** is placed starting at V = 1.1 (mantissa[0]=1). From `findvsatoappend` [orglinks.c:29-49]:

```c
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart); // linkspacevstart = 2.0
// if no text yet:
tumblerincrement (vsaptr, 0, 1, vsaptr); /* no text in doc */
tumblerincrement (vsaptr, 1, 1, vsaptr); // → 1.1
```

**Links** are placed starting at V = 2.1 (mantissa[0]=2). From `findnextlinkvsa` [do2.c:151-167]:

```c
tumblerincrement (&firstlink, 0, 2, &firstlink); // mantissa[0] = 2
tumblerincrement (&firstlink, 1, 1, &firstlink); // mantissa[1] = 1 → 2.1
```

So: text lives in **major level 1** (mantissa[0]=1), links in **major level 2** (mantissa[0]=2). This separation into distinct major levels is deliberate.

---

### Why the cwid Never Reaches the Link Subspace

From `insertpm` [orglinks.c:75-134], each crum's V-width is computed as:

```c
shift = tumblerlength (vsaptr) - 1;  // = 1 for vsaptr=1.1 or 2.1
inc = tumblerintdiff (&lwidth, &zero); // number of chars or 1 for link
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```

With zero as input to `tumblerincrement` [tumble.c:599-623]:

```c
if (iszerotumbler (aptr)) {
    cptr->exp = -rightshift;  // exp = -1
    cptr->mantissa[0] = bint; // = inc
    return(0);
}
```

Every crum V-width — whether text (14 chars → exp=-1, mantissa[0]=14) or link (1 link → exp=-1, mantissa[0]=1) — is a **sub-level value** (exp = -1).

When these are accumulated to build the root crum's `cwid.dsas[V]`, `absadd` [tumble.c:444-485] handles the equal-exp case:

```c
if (aptr->exp == bptr->exp) {
    answer.exp = aptr->exp;          // stays at -1
    ansmant[0] = amant[0] + bmant[0]; // add mantissa[0] values
    ...
}
```

So: 14 text chars (exp=-1, m[0]=14) + 1 link (exp=-1, m[0]=1) = exp=-1, m[0]=15.

The root's `cwid.dsas[V]` = **0.15** (sub-level, exp=-1).

---

### Why the Range Cannot Reach 2.x

When `absadd` adds a **1.x stream** (exp=0, mantissa[0]=1, mantissa[1]=1) to a **sub-level width** (exp=-1, mantissa[0]=15), the exp-different branch applies [tumble.c:464-477]:

```c
} else if (aptr->exp > bptr->exp) {
    answer.exp = aptr->exp;         // exp = 0
    temp = aptr->exp - bptr->exp;   // = 0 - (-1) = 1
    while (i < temp) {
        ansmant[j++] = amant[i++];  // copy amant[0] = 1
    }
    ansmant[j++] = amant[i++] + bmant[0]; // amant[1] + bmant[0] = 1 + 15 = 16
    i = 1;
```

Result: exp=0, mantissa=[1, 16, 0, ...] = **1.16**.

The link crum is at V = **2.1** (mantissa[0]=2). `tumblercmp` / `abscmp` [tumble.c:87-111] compares from the highest mantissa position down:

```c
a = aptr->mantissa;  b = bptr->mantissa;
for (i = NPLACES; i--;) {
    cmp = *a - *b;
    if (cmp == 0) continue;
    else if (cmp < 0) return LESS;
    else return GREATER;
}
```

Comparing **2.1** vs **1.16**: mantissa[0] → 2 − 1 = 1 > 0 → **TOMYRIGHT**. The link crum at 2.1 is **outside** the range [1.1, 1.16].

Therefore `crumqualifies2d` [retrie.c:270-305] returns FALSE for the link crum, and `findcbcinarea2d` [retrie.c:229-268] skips it. The link's I-span is never returned by `vspanset2ispanset` and is never inserted into the new version.

---

### Proof from the Golden Test

The behavioral test [golden/versions/version_copies_link_subspace.json] confirms this mechanically:

```
Source vspanset (before version):
  [{start: "0", width: "0.1"},   ← link subspace (2.x, normalized to 0 in display)
   {start: "1", width: "1"}]     ← text subspace (1.x)

Version vspanset (after CREATENEWVERSION):
  [{start: "1.1", width: "0.15"}] ← text only, no link subspace
```

The version has V-content starting at 1.1 (the same stream returned by `retrievedocumentpartofvspanpm`), with width 0.15 = the accumulated sub-level V-width of all the text characters. The link at 2.1 never appears.

---

### Was It Deliberate?

**Both and neither.** Two forces combined:

1. **The deliberate V-space design**: `findnextlinkvsa` [do2.c:151-167] explicitly places links at major level 2 (V = 2.1+). This decision — separating text and links into distinct major levels — is the structural precondition. It ensures no sub-level arithmetic can bridge from 1.x to 2.x.

2. **The kluge implementation**: `retrievedocumentpartofvspanpm` [orglinks.c:155-162] is labeled "this is a kluge" and returns only a single vspan. The properly-structured alternative, `retrievevspansetpm` [orglinks.c:173-221], explicitly handles multi-subspace documents — checking `is1story` [tumble.c:237-247], calling `maxtextwid` to skip link crums, and returning **separate vspans** for text and links. If CREATENEWVERSION had used `retrievevspansetpm` and chosen to include the link vspan, links would be copied.

The function name `doretrievedocvspanfoo` suggests an intent to do something different ("foo" as placeholder), and the "not yet kluged" comment indicates the implementation was acknowledged as unfinished. The link exclusion happens correctly, but as an emergent consequence of V-space geometry rather than an explicit policy filter.

**Links are therefore anchored to the home document by the V-space layout**, not by CREATENEWVERSION actively checking "should I copy links?" The new version gets only the text I-spans; the link orgl entries, spanf endpoints, and 2.x POOM entries all remain on the original document. Link discovery still works via content identity (I-addresses in the permascroll are shared), as documented in finding 0043 — but the version carries no link POOM structure of its own.
