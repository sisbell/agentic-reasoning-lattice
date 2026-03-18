## Question 12 [gregory]

> If document B transcludes a span from document A, and then document C transcludes the same span from document B, does C's POOM reference the original I-addresses from A's granfilade entry — making the transclusion chain A→B→C fully transparent to `find_links` — or does the second copy introduce any new identity?

## KB Synthesis

Yes — the chain is fully transparent. C's POOM entries reference A's original I-addresses directly, with no new identity introduced at any hop.

## Mechanism

When B transcludes a span from A, the call chain is:

```
source V-spec → vspanset2sporglset(B_or_A) → insertpm(C's POOM)
```

`vspanset2sporglset` converts B's V-span to sporgls by reading B's POOM — which maps B's V-positions to A's original I-addresses [INT-SPORGL-TRANSCLUSION]. The sporgl carries those I-addresses (the `sporglorigin` field) unchanged into `insertpm`. No allocation step occurs; `docopy` shares existing I-addresses rather than calling `findisatoinsertgr` [ST-COPY, Finding 0064].

So after A→B transclusion:
- `poom(B)[v_b] = I_a` (A's original I-address)

After B→C transclusion, `vspanset2sporglset` runs against B, reads the same `I_a` from B's POOM, and writes it into C:
- `poom(C)[v_c] = I_a` (still A's original I-address)

The chain telescopes to a single flat identity assignment: C holds A's I-addresses without any intermediate layer.

## Consequence for `find_links`

`find_links` operates purely on I-address intersection in the spanf enfilade [SS-FIND-LINKS, Finding 0028]. Since C holds `I_a`, and the spanf was indexed on `I_a` when the link was created on A's content, `find_links` on C returns the link.

This is the mechanism behind [INV-TRANSITIVE-IDENTITY] (confirmed experimentally as Finding 0018, Key Finding 6):

> "If A transcludes from B, and B transcludes from C, then A and C share content identity... `FINDDOCSCONTAINING` and `compare_versions` both respect this transitivity."

And [INT-LINK-TRANSCLUSION] (Finding 0008) confirms the same holds for link discovery across arbitrarily long transclusion and version chains.

## No new identity is ever created

[ST-VCOPY] states the postcondition explicitly: vcopy creates **no new content identities**. [INV-IADDR-IMMUTABILITY] guarantees I-addresses are permanent and immutable — there is nothing to substitute at each hop. The transclusion chain A→B→C is semantically equivalent to A→C directly from the perspective of `find_links`, `compare_versions`, and `find_documents`.

---

## Code Exploration

I now have all the pieces. Let me write the complete answer.

---

## Transclusion Chain Transparency: A→B→C in udanax-green

**Short answer:** C's POOM references A's original I-addresses, without any intermediate identity. The chain A→B→C is fully transparent to `find_links`. No new identity is introduced at the second copy.

---

### 1. How I-addresses originate: text insertion into A

When text is first inserted (`doinsert`, `do1.c:87`):

```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
```

`inserttextingranf` (→ `inserttextgr`, `granf2.c:83`) calls `findisatoinsertgr` to allocate a new tumbler address `lsa` in the global granfilade, stores the bytes there, and returns an `ispanset` whose `stream` is that address:

```c
movetumbler (&spanorigin, &ispanptr->stream);   // granf2.c:105
tumblersub (&lsa, &spanorigin, &ispanptr->width); // granf2.c:106
```

This `ispanset` is the I-address: **a permanent, globally unique permascroll coordinate for the bytes**. Nothing else assigns or reassigns I-addresses. The granfilade entry is never duplicated.

---

### 2. A's POOM is populated: `insertpm`

`docopy` then calls `insertpm` (`orglinks.c:75`):

```c
unpacksporgl (sporglset, &lstream, &lwidth, &linfo);  // orglinks.c:101
movetumbler (&lstream, &crumorigin.dsas[I]);           // orglinks.c:105 — I-axis = I-address
movetumbler (vsaptr,   &crumorigin.dsas[V]);           // orglinks.c:113 — V-axis = V-address in A
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // orglinks.c:130
```

A's POOM now holds a crum mapping: **V-address-in-A ↔ I-address**.

---

### 3. B transcludes from A: `specset2ispanset` traverses A's POOM

`docopy` (`do1.c:45`) begins with:

```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
```

`specset2ispanset` (`do2.c:14`) handles a VSPECID by:

```c
findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)  // do2.c:35
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))  // do2.c:36
```

`vspanset2ispanset` (`orglinks.c:397`):

```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```

`permute` (`orglinks.c:404`) traverses A's POOM restricted to the requested V-span and returns the corresponding I-spans. **The result is A's original permascroll I-address.**

Then `insertpm` writes B's POOM with:
- `crumorigin.dsas[I]` = **A's I-address** (from the permute result)
- `crumorigin.dsas[V]` = B's V-address

**B's POOM contains no new identity. It stores A's original I-address in its I-dimension.**

---

### 4. C transcludes from B: the same path, one level deeper

When C transcludes from B, `specset2ispanset` is again called, this time with B's POOM:

```c
vspanset2ispanset(taskptr, docorgl_B, B_vspanset, ispansetptr)  // do2.c:36
→ permute(taskptr, docorgl_B, B_vspanset, V, ispansetptr, I)     // orglinks.c:404
```

B's POOM maps B's V-address to A's I-address (written in step 3). **`permute` returns A's original I-address directly** — there is no second lookup into the granfilade.

C's `insertpm` then writes:
- `crumorigin.dsas[I]` = **A's I-address** (unchanged from step 3)
- `crumorigin.dsas[V]` = C's V-address

**C's POOM also contains A's original I-address. The second hop introduces no new identity.**

---

### 5. The spanfilade: both B and C indexed by A's I-address

`insertspanf` (`spanf1.c:15`) is called for both B and C with `ispanset` = A's I-address:

```c
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);   // spanf1.c:49 — key = I-address
movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);  // spanf1.c:51
```

The ORGLRANGE dimension carries B's ISA (for the B entry) and C's ISA (for the C entry). Both entries are indexed by A's I-address in the SPANRANGE dimension.

---

### 6. `find_links` is transparent: I-address is the only key

`dofindlinksfromtothree` (`do1.c:348`) → `findlinksfromtothreesp` (`spanf1.c:56`):

```c
specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);  // spanf1.c:71
sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);  // spanf1.c:77
```

`specset2sporglset` (`sporgl.c:14`) → `vspanset2sporglset` (`sporgl.c:35`):

```c
vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);         // sporgl.c:48
movetumbler(docisa,          &sporglset->sporgladdress);        // sporgl.c:53
movetumbler(&ispanset->stream, &sporglset->sporglorigin);       // sporgl.c:54
```

Whether you query from A, B, or C, the `sporglorigin` ends up as A's I-address (after passing through the respective POOM).

`sporglset2linksetinrange` (`sporgl.c:239`) then searches the spanfilade:

```c
if (FALSE/*trying to kluge links followable thru versions */&&...) {
    infoptr = &linfo; ...
} else
    infoptr = NULL;  // sporgl.c:254-255
...
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
// sporgl.c:259
```

The `if (FALSE ...)` permanently disables homedoc filtering. `infoptr = NULL`. The search key is **only the SPANRANGE dimension** — which is A's I-address. The spanfilade returns all ORGLRANGE entries (link ISAs) whose SPANRANGE overlaps the queried I-address, regardless of which document (A, B, or C) holds the content.

**Links attached to content in A, B, or C are all findable from any of the three perspectives**, because all three reference the same I-address.

---

### Summary

The transclusion chain A→B→C is **fully transparent** to `find_links` by design:

| Layer | What's stored |
|-------|--------------|
| Granfilade | Text bytes at I-address (only ever written once, by `inserttextgr`) |
| A's POOM | `V_A ↔ I_A` |
| B's POOM | `V_B ↔ I_A` (A's I-address — from `permute` over A's POOM) |
| C's POOM | `V_C ↔ I_A` (A's I-address — from `permute` over B's POOM) |
| Spanfilade | A's I-address indexed, carrying A's ISA, B's ISA, and C's ISA as ORGLRANGE entries |

The POOM is a permutation matrix (V↔I mapping), not a content store. Each transclusion hop adds a new V-axis entry pointing at the pre-existing I-address. `vspanset2ispanset` (`orglinks.c:397`) collapses the chain in one step — it traverses the POOM of whichever document you name, and falls straight through to the original permascroll I-address.

**No new identity is created at the second copy.** C holds no I-address of its own for the transcluded content — only a V-address within its own document space. The I-address remains A's, permanently.
