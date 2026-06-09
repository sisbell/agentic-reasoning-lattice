## Question 2 [evidence]

> Does udanax-green provide any link-creation path that accepts direct I-addresses (bypassing V-span resolution), thereby able to record ghost-type or non-content endsets?

## KB Synthesis

No. The KB documents no link-creation path that accepts raw I-addresses or bypasses V-span resolution.

**The only documented creation chain is V-span → sporgl → spanfilade.**

`domakelink` at `do1.c:173-197` is the sole entry point for link creation from the FEBE layer. It receives source, target, and type as V-spansets and converts them to sporglsets via `vspanset2sporglset` before reaching `insertendsetsinspanf` [ST-LINK-CREATE, Finding 0037]. The conversion chain is mandatory:

```
V-span → vspanset2sporglset → vspanset2ispanset → permute → span2spanset → sporgl (with I-address)
```

The internal function `insertendsetsinspanf` does accept sporglsets (which carry I-addresses directly) [SS-SPORGL-TRANSCLUSION], but the KB documents no FEBE opcode or internal pathway that constructs sporglsets from bare I-addresses and passes them directly to `insertendsetsinspanf`, bypassing `domakelink`.

**Ghost-endset creation is theoretically reachable only through subspace convention violation.** If content was placed in the wrong subspace (e.g., text at V:2.x per [PRE-ENF0-PLACEMENT-GAP], or link ISAs at V:1.x), a subsequent `domakelink` call using that span would extract those misplaced I-addresses as endpoint identities — producing an endset whose I-addresses are not permascroll content. But this is an unintended consequence of [INV-SUBSPACE-CONVENTION] being unenforced [PRE-SUBSPACE-CONVENTION], not a designed capability.

**The type endset is not a special case.** Type endsets reference V-spans in the bootstrap document's type registry at `1.0.2.x` [SS-LINK-ENDPOINT, Finding 0024] — still V-span-resolved, not raw I-addresses.

**Bottom line:** The system provides no API, opcode, or clean internal path for direct I-address link-endpoint registration. Any ghost-endset state would arise only from subspace convention violations, not from a designed bypass.

---

## Code Exploration

I now have all the evidence needed. Let me write the complete answer.

---

## Answer: Direct I-Address Link-Creation Path in udanax-green

**Yes.** udanax-green provides a first-class link-creation path that accepts direct I-addresses for all three endsets, bypassing V→I conversion entirely. This path is exposed through both the FEBE network protocol and the interactive interface.

---

### Entry Points

**FEBE protocol (`get2fe.c:147-180`)** — `getspecset` parses each endset spec by reading a single character flag:

```c
c = pullc(taskptr);
if ((c != SPANFLAG) && (c != VSPECFLAG))
    return(FALSE);
if (c == SPANFLAG) {       // 's' = SPANFLAG (line 17)
    specset=(typespecset)taskalloc(taskptr,sizeof(typespan));
    if (!getspan(taskptr,specset,ISPANID))   // line 169 — sets itemid=ISPANID
        return(FALSE);
} else {                   // 'v' = VSPECFLAG
    specset=(typespecset)taskalloc(taskptr,sizeof(typevspec));
    if (!getvspec(taskptr,specset))          // requires doc ISA + V-spans
        return(FALSE);
}
```

A client sends `s~<stream-tumbler><width-tumbler>` to create an ISPANID endset. The `getspan` call at `get2fe.c:213-221` accepts **any tumbler** for stream and width with no validation that the I-address corresponds to real content.

The interactive interface (`get2.c:177-183`) has the same dual path via a "a span?" boolean prompt.

---

### The Bypass in `specset2sporglset` (`sporgl.c:14-33`)

This is the pivot point. All three endsets of `docreatelink` pass through here (`do1.c:214-216`):

```c
bool specset2sporglset(..., typespecset specset, typesporglset *sporglsetptr, int type)
{
    *sporglsetptr = NULL;
    for (; specset; ...) {
        if (((typeitemheader *)specset)->itemid == ISPANID) {
            *sporglsetptr = (typesporglset)specset;       // line 21 — pass through
            sporglsetptr = (typesporglset *)&((typeitemheader *)specset)->next;
        } else if (((typeitemheader *)specset)->itemid == VSPECID) {
            if (!(sporglsetptr = vspanset2sporglset(...)))  // line 25 — V→I conversion
                return (FALSE);
        }
    }
```

**`sporgl.c:20-22`**: When `itemid == ISPANID`, the item is cast directly to `typesporglset` and passed through unchanged. `vspanset2sporglset` (which calls `findorgl` to look up the orgfilade and then `permute` to convert V→I) is **never called**. There is no lookup, no validation, no conversion.

---

### Storage Path

The ISPANID sporglset then travels into two stores:

**1. Spanfilade (`spanf1.c:26-29`):**
```c
if (((typeitemheader *)sporglset)->itemid == ISPANID) {
    movetumbler (&((typeispan *)sporglset)->stream, &lstream);
    movetumbler (&((typeispan *)sporglset)->width, &lwidth);
    movetumbler (isaptr, &linfo.homedoc);   // link ISA, not a document ISA
}
```
The raw I-address stream/width from the client are stored verbatim in `crumorigin.dsas[SPANRANGE]` / `crumwidth.dsas[SPANRANGE]` via `insertnd` at `spanf1.c:51`.

**2. Orglinks permutation matrix (`orglinks.c:100-101`):**
```c
for (; sporglset; ...) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
```
`unpacksporgl` (`sporgl.c:178-203`) handles ISPANID:
```c
if (((typeitemheader *)sporglptr)->itemid == ISPANID) {
    movetumbler (&((typeispan *)sporglptr)->stream, streamptr);
    movetumbler (&((typeispan *)sporglptr)->width, widthptr);
    tumblerclear (&infoptr->homedoc);   // homedoc cleared to zero
}
```
The zero homedoc is stored in `linfo`, then `insertnd` at `orglinks.c:130` inserts the raw I-address into the permutation matrix with a zero document address.

---

### Retrieval Roundtrip

`dofollowlink` (`do1.c:223-231`) → `link2sporglset` → `linksporglset2specset` (`sporgl.c:97-123`):

```c
if (iszerotumbler (&((typesporgl *)sporglset)->sporgladdress)) {
    ((typeitemheader *)specset)->itemid = ISPANID;            // line 112
    movetumbler(&((typesporgl *)sporglset)->sporglorigin, &((typeispan *)specset)->stream);
    movetumbler(&((typesporgl *)sporglset)->sporglwidth,  &((typeispan *)specset)->width);
```

Because `unpacksporgl` stored `homedoc = 0`, the retrieved sporgl has `sporgladdress = 0`, triggering the ISPANID return path. **The original raw I-address is returned to the client as-is**, without any attempt to resolve it to a V-address.

---

### Ghost-Type Endsets Are Structurally Possible

The type definitions (`xanadu.h:65-76`) show:
```c
typedef struct structtypespan {
    struct structtypespan *next;
    typeitemid itemid;
    tumbler stream;
    tumbler width;
} typespan;
typedef typespan typeispan;
```

Since `getspan` (`get2fe.c:213-221`) accepts arbitrary tumblers for stream and width with no validation, a client may supply I-addresses that:
- Fall in unallocated I-space (no content granule exists there)
- Belong to a different document's I-space
- Point to I-ranges that were allocated but then deleted

All of these constitute ghost endsets — the link is stored, its endset I-addresses are preserved, but they don't correspond to accessible content. The backend has no guard against this; `acceptablevsa` (`do2.c:110-113`) is a stub that unconditionally returns `TRUE`.

---

### The `domakelink` vs `docreatelink` Note

`domakelink` (`do1.c:169-193`) is a two-endset variant with the same ISPANID acceptance path. One notable difference: `docreatelink` at `do1.c:213` has the comment `/*WRITEBERT ECH 7-1*/NOBERTREQUIRED` — the `WRITEBERT` requirement for the link's own orgfilade was removed (replaced with `NOBERTREQUIRED`), while `domakelink` at `do1.c:186` still uses `WRITEBERT`. This suggests `docreatelink` may have been deliberately relaxed to allow creating links to content in documents you can read but don't own — another dimension that enables endsets pointing outside the caller's writable space.

---

### Summary

| Layer | File:Line | Behavior |
|-------|-----------|----------|
| FEBE input | `get2fe.c:167-170` | `'s'` flag creates ISPANID spec from raw tumblers |
| Interactive input | `get2.c:177-183` | "a span?" path creates ISPANID spec |
| No validation | `get2fe.c:213-221` | `getspan` accepts arbitrary tumbler values |
| Core bypass | `sporgl.c:20-22` | ISPANID items pass through `specset2sporglset` without V→I conversion |
| Storage (spanf) | `spanf1.c:26-29` | Raw I-address stored in SPANRANGE dimension |
| Storage (orgl) | `orglinks.c:100-101`, `sporgl.c:183-186` | Raw I-address stored with zero homedoc |
| Retrieval | `sporgl.c:105-114` | Zero `sporgladdress` → ISPANID returned to client |
| Stub guard | `do2.c:110-113` | `acceptablevsa` always returns TRUE |

**The ISPANID path is not a side-channel or backdoor — it is a designed, protocol-level feature.** The FEBE wire format explicitly encodes the `'s'` flag for it. The result is that any client can store link endsets with arbitrary I-addresses, including those that point to non-existent content, making ghost-type or unresolvable endsets a structurally native capability of udanax-green.
