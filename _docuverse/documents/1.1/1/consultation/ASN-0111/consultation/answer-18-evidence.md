## Question 18 [evidence]

> Does the link orgl as read reveal the link's home document identity (the docISA prefix of its ISA), and is that derivable from the link's own address structure?

## KB Synthesis

Yes, and it's directly readable from the link's ISA without inspecting the orgl contents.

From [SS-ADDRESS-SPACE] (Finding 0024) and [SS-LINK-HOME-DOCUMENT] (Finding 0025), a link's I-address follows the structure:

```
{home_doc}.0.2.{link_number}
```

For example, document `1.1.0.1.0.1` produces link ISA `1.1.0.1.0.1.0.2.1`. The home document ISA is the prefix before the `.0.2.` element-field separator.

[SS-TUMBLER-CONTAINMENT] (Finding 0021) gives the mechanical recovery: `tumblertruncate(link_isa, tumblerlength(home_doc), &truncated)` followed by `tumblereq`. Since the allocation rule ([SS-ADDRESS-ALLOC] Finding 0065) bounds link allocation within `docISA.2.2` to `docISA.2.3`, the home document is the longest prefix satisfying `contains(candidate, link_isa)` at the document depth.

The KB does not describe the orgl's internal field layout in enough detail to say whether the home doc is redundantly stored as a field within the orgl itself — that internal structure is not captured in any finding. But the address alone is sufficient to derive it structurally.

---

## Code Exploration

I now have all the source I need. Let me compile the complete analysis.

---

## Does the Link Orgl Reveal the Link's Home Document Identity?

### 1. The Link Orgl as Returned by `fetchorglgr`

`fetchorglgr` [granf2.c:22-81] returns the raw POOM enfilade root:

```c
ret = context->corecrum->cinfo.granstuff.orglstuff.orglptr;
...
return ((typeorgl)ret);
```

`typeorgl` is defined as `INT *` [xanadu.h:17]:
```c
#define typeorgl  INT *   /* temp -- INT for alignment */
```

The returned value is a pointer to a `typecuc` (the enfilade node). That node carries `cdsp` (displacement) and `cwid` (width) in I/V spaces and child crum pointers. **It carries no explicit docISA field.** The orgl as read does not directly reveal the home document identity.

---

### 2. How a Link ISA Is Constructed

In `docreatelink` [do1.c:207-209]:
```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)
```

`makehint` stores the docISA directly into `hint.hintisa` [do2.c:79-84]:
```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr) {
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

`createorglingranf` calls `findisatoinsertgr` [granf2.c:130-156], which because `hintptr->subtype == ATOM` calls `findisatoinsertmolecule` [granf2.c:158-181], where the LINKATOM branch [granf2.c:170-176]:

```c
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
    if (tumblercmp (&lowerbound, isaptr) == LESS)
        tumblerincrement (isaptr, 1, 1, isaptr);
    else
        tumblerincrement (&lowerbound , 0, 1, isaptr);
}
```

`tumblerincrement(aptr, rightshift, bint, cptr)` [tumble.c:599-623] finds the last nonzero mantissa index `idx` of `aptr`, then sets `cptr->mantissa[idx + rightshift] += bint`. This appends new tumbler digits beyond the last nonzero position.

**Concrete example** — docISA `1.1.0.1` (mantissa `[1,1,0,1,0,...]`, length 4):

- `tumblerincrement(&docISA, 2, 2, isaptr)` → `idx=3`, `mantissa[3+2]=mantissa[5]+=2` → `1.1.0.1.0.2`
- First link (lowerbound is zero, so `LESS`): `tumblerincrement(isaptr, 1, 1, isaptr)` → `idx=5`, `mantissa[5+1]+=1` → **`1.1.0.1.0.2.0.1`**

The second link: lowerbound = `1.1.0.1.0.2.0.1`, `tumblerincrement(&lowerbound, 0, 1, isaptr)` → `1.1.0.1.0.2.0.2`.

The link ISA is always computed by appending `.0.2.0.N` segments **to the docISA**. The docISA is structurally the leading prefix of the link ISA.

---

### 3. Is the docISA Derivable from the Link ISA?

**Yes, by truncation — but only if you know the docISA's tumbler length.**

`tumblertruncate` [tumble.c:625-639]:
```c
int tumblertruncate(tumbler *aptr, INT bint, tumbler *cptr)
{
  ...
  for (; bint < NPLACES; ++bint)
      answer.mantissa[bint] = 0;
  tumblerjustify (&answer);
  movetumbler (&answer, cptr);
}
```

Called as `tumblertruncate(linkISA, tumblerlength(docISA), &docISA)` it recovers the docISA exactly. This exact pattern is used in `findisatoinsertnonmolecule` [granf2.c:239]:
```c
tumblertruncate (&lowerbound, hintlength + depth, isaptr);
```

Document ISAs have a deterministic length in the address hierarchy: account ISAs are at depth 2 from the node, and document ISAs are at depth `depth=2` beyond the account ISA (because `ACCOUNT ≠ DOCUMENT` forces `depth=2` [granf2.c:209]). So document addresses are always at a fixed, computable depth.

The link ISA structure `docISA.0.2.0.N` means the home docISA occupies exactly the first `tumblerlength(docISA)` mantissa positions. The separator pattern `.0.2` is the fixed LINKATOM subspace marker.

---

### 4. What the Sporgl Entries Contain

The orgl's POOM enfilade stores sporgl entries inserted by `insertendsetsinorgl` [do2.c:130-148] via `insertpm` [orglinks.c:75-134]. Each sporgl entry carries [xanadu.h:115-121]:

```c
typedef struct structsporgl{
    struct structsporgl *next;
    typeitemid    itemid;
    tumbler sporglorigin;
    tumbler sporglwidth;
    typeisa sporgladdress;
} typesporgl;
```

The `sporgladdress` is the docISA of the **endpoint document** — the document containing the link's from/to/three endpoints. These are set during `specset2sporglset` conversion of the `fromspecset`/`tospecset`/`threespecset` passed to `docreatelink` [do1.c:214-218].

`dofollowlink` [do1.c:223-231] reads this back:
```c
return (
   link2sporglset (taskptr, linkisaptr, &sporglset, whichend,NOBERTREQUIRED)
&& linksporglset2specset (taskptr,&((typesporgl *)sporglset)->sporgladdress, sporglset, specsetptr,NOBERTREQUIRED));
```

The `sporgladdress` of the first sporgl entry in the returned set becomes the docISA used for endpoint retrieval. **This is the endpoint document's identity, not the link's home document.**

---

### 5. Where the Home Document Identity Is Actually Recorded

The home document identity relative to a link is recorded in the **home document's own orgl**, not the link's orgl. In `docreatelink` [do1.c:210-212]:

```c
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)
```

`docopy` [do1.c:45-65] inserts the link ISA into the home document's permutation matrix (home docISA's orgl) at V-position `linkvsa` (in the `.0.2.x` link subspace). The V-position is determined by `findnextlinkvsa` [do2.c:151-167]:

```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);  // = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // = 2.1
```

The link subspace in V-space starts at `2.1` [do2.c:156-158]. The home document's permutation matrix maps V-positions `2.1`, `2.2`, ... to the link ISAs it owns.

---

### Summary

| Question | Answer | Evidence |
|----------|--------|----------|
| Does the link orgl (as returned by `fetchorglgr`) carry an explicit home docISA field? | **No** | `typeorgl = INT *`; the returned POOM enfilade has no docISA field [granf2.c:62-80, xanadu.h:17] |
| Is the home docISA derivable from the link ISA address? | **Yes, by truncation** | Link ISA = `docISA.0.2.0.N` — docISA is the `tumblerlength(docISA)`-story prefix [granf2.c:170-176, tumble.c:625-639] |
| Does the prefix extraction require external knowledge? | **Yes, the docISA length** | The docISA length is not self-encoded in the link ISA; it's a structural property of the address hierarchy (documents are always at depth 2 beyond their account) [granf2.c:209, 237] |
| Do sporgl entries in the link orgl reveal the home docISA? | **No — wrong docISA** | `sporgladdress` fields store endpoint docISAs (from/to/three), not the creating document [xanadu.h:120, do1.c:214-218] |
| Where is the home document/link relationship authoritative? | **Home document's orgl** | `docreatelink` inserts the link ISA into the home doc's permutation matrix at V-space link subspace `2.N` [do1.c:210-212, do2.c:156-158] |

**Conclusion**: The link orgl as read reveals nothing about the home document — it is simply an enfilade mapping V-positions (`1.1` from, `2.1` to, `3.1` three) to I-space sporgl entries for the endpoint documents. The home docISA *is* derivable from the link's own ISA address by truncation — the link ISA is always `docISA.0.2.0.N`, making the docISA a recoverable prefix — but this requires knowing the expected tumbler depth of document addresses, which is a hierarchical invariant of the system rather than data embedded in the link ISA itself. The authoritative record of "this link belongs to this document" lives in the home document's own permutation matrix, not in anything readable from the link's orgl.
