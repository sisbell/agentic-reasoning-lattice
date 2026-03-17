## Question 18 [gregory]

> A link orgl is stored in the granfilade alongside text content — is a link ontologically a special kind of content on the permascroll (occupying I-space positions just as characters do), or is it a categorically different entity that merely uses the same storage substrate?

## KB Synthesis

A link orgl is a **categorically different entity** from permascroll content — it merely uses the same storage substrate. Several KB threads converge on this.

## Different allocation paths

[SS-ADDRESS-SPACE] Finding 0077 is definitive: the granfilade dispatcher `findisatoinsertgr` routes to two distinct sub-allocators. Text uses `findisatoinsertmolecule` (TEXTATOM hint, depth 3+, content subspace). Link orgls use `findisatoinsertnonmolecule` (LINKATOM hint, the same path used for *document address allocation*). This is the machinery telling you: link orgls are structural entities, not content atoms.

## Different identity semantics

[SS-CONTENT-IDENTITY] Finding 0009 draws the sharpest line: permascroll I-addresses represent **content identity** — two documents can share the same I-address via transclusion, meaning they share the same content. Link orgl ISAs represent **object identity** — each link is a unique, non-shareable instance. [SS-CONTENT-IDENTITY] Finding 0015 reinforces: "two documents cannot 'share' a link ISA via transclusion because each link is a distinct object."

## Different V-space treatment

[SS-SUBSPACE-CONVENTION] (Findings 0009, 0010, 0038) encodes the categorical distinction directly into V-space: text lives at mantissa[0]=1, link orgls at mantissa[0]=2, link type endpoints at mantissa[0]=3. The subspace is a type discriminator. [FC-SUBSPACE] confirms these are kept structurally isolated by the two-blade knife mechanism.

## Observable consequence: the contiguity break

[INT-LINK-INSERT] Finding 0063 makes the categorical difference concrete. CREATELINK consumes I-address space in the granfilade (advancing `findpreviousisagr`'s ceiling), so a subsequent text INSERT allocates I-addresses that are non-contiguous with pre-CREATELINK text. Link orgls and text characters compete for the same monotonic allocation sequence — this is the shared substrate — but they are distinct kinds of occupants. `compare_versions` after `INSERT "ABC" → CREATELINK → INSERT "DEF"` returns **two** shared span pairs, not one, precisely because the link orgl sits between the two text runs in I-space.

## Summary

Link orgls and text share the granfilade as a storage substrate, and link orgls do occupy I-space positions (hence the contiguity effect). But ontologically they are structural objects, not content: allocated via the non-molecule path, representing unique object identity rather than shareable content identity, living in a dedicated V-space subspace, and incapable of being transcluded. The granfilade is a general-purpose enfilade that happens to host both; the categorical distinction is enforced by allocation type, V-address convention, and deref semantics, not by separate physical storage.

---

## Code Exploration

Now I have everything I need from the source code. Here is the full answer:

---

## Are Links and Text Content the Same Kind of Entity in Udanax-Green?

**Short answer: No. They share the same granfilade storage substrate and both receive I-space positions, but they are ontologically distinct. A link is not permascroll content — it is a relational entity whose I-space position names a container, not a sequence of characters.**

---

### 1. The Granfilade Type System

The granfilade has exactly two leaf types, defined at [`wisp.h:69-70`]:

```c
#define GRANTEXT  1
#define GRANORGL  2
```

Both inhabit the same node structure ([`wisp.h:94-104`]):

```c
typedef union uniongranstuff {
    typegrantext textstuff;
    typegranorgl orglstuff;
} typegranstuff;

typedef struct structgranbottomcruminfo {
    typegranstuff granstuff;
    INT infotype;       /* the discriminator: GRANTEXT or GRANORGL */
} typegranbottomcruminfo;
```

The `infotype` field is the categorical boundary. The storage is shared; the meaning is not.

---

### 2. Both Receive I-Space Positions — But For Different Reasons

`inserttextgr` ([`granf2.c:83-109`]):
```c
locinfo.infotype = GRANTEXT;
locinfo.granstuff.textstuff.textlength = textset->length;
movmem(textset->string, locinfo.granstuff.textstuff.textstring, ...);
insertseq((typecuc*)fullcrumptr, &lsa, &locinfo);   // inserts at I-space address lsa
tumblerincrement(&lsa, 0, textset->length, &lsa);   // advances by character count
```

`createorglgr` ([`granf2.c:111-128`]):
```c
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf(POOM);   // allocates a nested enfilade
...
insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);    // inserts at I-space address isaptr
```

Both call `insertseq` with an I-space address. But text stores *bytes* at its I-address. A link orgl stores a *pointer to a nested POOM enfilade* — the I-address is the name of a container, not a character.

---

### 3. The I-Space Addresses Are Structurally Different

`findisatoinsertmolecule` ([`granf2.c:158-181`]) allocates I-addresses differently by atom type:

```c
} else if (hintptr->atomtype == TEXTATOM) {          // line 168
    tumblerincrement(&lowerbound, 0, 1, isaptr);     // increment in mantissa[0]
} else if (hintptr->atomtype == LINKATOM) {          // line 170
    tumblerincrement(&hintptr->hintisa, 2, 2, isaptr); // branch at mantissa[2], offset 2
    ...
}
```

`TEXTATOM` and `LINKATOM` are defined at [`xanadu.h:145-146`]:
```c
#define TEXTATOM  1
#define LINKATOM  2
```

And `doinsert` passes `TEXTATOM` while `docreatelink` passes `LINKATOM` ([`do1.c:117`] and [`do1.c:207`]):
```c
/* text: */    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
/* link: */    makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
```

Link I-addresses branch at a deeper mantissa component than text, placing them in a structurally distinct region of I-space even before V-space segregation enters the picture.

---

### 4. Links Are Segregated in V-Space, Not Just I-Space

After getting an I-address, a link is installed in the document's POOM (permutation matrix enfilade) at a V-space address explicitly reserved for links. `findnextlinkvsa` ([`do2.c:151-167`]):

```c
tumblerclear(&firstlink);
tumblerincrement(&firstlink, 0, 2, &firstlink);   // 2.0
tumblerincrement(&firstlink, 1, 1, &firstlink);   // 2.1  ← "link subspace" starts here

(void) doretrievedocvspan(taskptr, docisaptr, &vspan);
tumbleradd(&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp(&vspanreach, &firstlink) == LESS)
    movetumbler(&firstlink, vsaptr);    // first link: V = 2.1
else
    movetumbler(&vspanreach, vsaptr);   // subsequent links: append after last
```

Text content occupies V-addresses starting at 1.1. Links are kept at V ≥ 2.1. `findvsatoappend` ([`orglinks.c:37`]) names the sentinel `linkspacevstart = 2.0` and actively steers text insertions below it.

The V-address of a link is *not* a content position readable by a user. It is a slot in a metadata subspace.

---

### 5. Runtime Tests Confirm the Categorical Split

`istextcrum` and `islinkcrum` ([`orglinks.c:246-261`]):

```c
bool istextcrum(typecorecrum *crumptr) {
    if (crumptr->cdsp.dsas[V].mantissa[1] == 0 && is1story(&crumptr->cwid.dsas[V]))
        return TRUE;
    return FALSE;
}

bool islinkcrum(typecorecrum *crumptr) {
    /* if the whole crum is displaced into link space it is a link crum
     * this is true if the tumbler is a 1.n tumbler where n != 0 */
    if (crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0)
        return TRUE;
    return FALSE;
}
```

These are runtime predicates used during V-space traversal (e.g., in `maxtextwid` at [`orglinks.c:224`]) to skip link crums when computing text extent. The code does not treat them as the same kind of thing — it explicitly tests for and excludes link crums from text operations.

---

### 6. What a Link Orgl Actually Is

When `createorglgr` stores the link at an I-address, it allocates a fresh nested POOM: `createenf(POOM)` ([`granf2.c:120`]). Then `docreatelink` fills that nested POOM with the endpoints ([`do1.c:208-220`]):

```c
createorglingranf(taskptr, granf, &hint, linkisaptr)           // I-address assigned
&& tumbler2spanset(taskptr, linkisaptr, &ispanset)              // I-address as I-span
&& findnextlinkvsa(taskptr, docisaptr, &linkvsa)                // V-address in link subspace
&& docopy(taskptr, docisaptr, &linkvsa, ispanset)               // install in POOM
&& insertendsetsinorgl(taskptr, linkisaptr, link, ...)          // store from/to in nested POOM
&& insertendsetsinspanf(taskptr, spanf, linkisaptr, ...)        // index in span filade
```

`setlinkvsas` ([`do2.c:169-183`]) reveals where the endpoints live inside the nested POOM: "from" at V=1.1, "to" at V=2.1. The link's nested POOM is a private coordinate system; its V-positions address endpoint roles, not document content positions.

---

### Conclusion

A link is **not** a special kind of permascroll content. The comparison breaks down at the fundamental level:

| | Text | Link |
|---|---|---|
| `infotype` | `GRANTEXT` (1) | `GRANORGL` (2) |
| Granfilade payload | Raw bytes (characters) | Pointer to nested enfilade |
| I-address semantics | **Permascroll identity of the characters** | Name of a container/envelope |
| V-address in POOM | Content position (≥ 1.1, text subspace) | Metadata slot (≥ 2.1, link subspace) |
| `islinkcrum` test | False | True |
| Returned as | `TEXTID` | `ADDRESSID` |

Text's I-address *is* the content — the character sequence is at that position on the permascroll, permanently. A link's I-address *names* a relational entity whose content is a (from, to) pair of V-space endpoint references stored inside a nested POOM. The granfilade is the common storage substrate, and both receive I-space coordinates, but the `GRANTEXT`/`GRANORGL` discriminator encodes a genuine categorical difference that the rest of the system respects consistently.
