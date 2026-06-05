## Question 11 [evidence]

> When RETRIEVECONTENTS resolves a V-address through the POOM to an I-address, does it return the raw bytes from the granfilade leaf, and are those bytes returned verbatim with no encoding interpretation per INV-BYTE-OPAQUE?

## KB Synthesis

Yes. The call chain is: `doretrievev` → `specset2ispanset` (V→I via POOM) → `ispanset2vstuffset(granf, ispanset, ...)` → `movmem` (raw byte copy from the granfilade leaf).

[SS-CONTENT-IDENTITY / Finding 0034] is the definitive source: content is stored as `char textstring[GRANTEXTLENGTH]` (950-byte buffer) with `unsigned textlength` as a byte count. Retrieval at `context.c:308` uses `movmem` — mapped to `memmove` — which is a raw byte copy with no encoding conversion, no character boundary checking, and no validation. The fundamental type is `seq<byte>`, not `seq<char>`.

[INV-SINGLE-CHAR-GRANULARITY / Finding 0034] confirms the invariant: `vspan_width(c) == byte_length(c)` unconditionally. Each byte gets exactly one I-address; V-space positions correspond 1:1 with bytes.

[EC-ENCODING-BOUNDARY-SPLIT] documents the observable consequence: partial retrieval of a multi-byte UTF-8 sequence returns the individual bytes as-is, producing invalid encoded text. The backend performs no character boundary validation on any operation.

The KB doesn't define a tag named `INV-BYTE-OPAQUE`, but the behavior it describes is fully covered by [SS-CONTENT-IDENTITY] and [INV-SINGLE-CHAR-GRANULARITY]. The bytes are returned verbatim from the granfilade leaf — encoding semantics are entirely the caller's responsibility.

---

## Code Exploration

I have all the source evidence. Here is the complete answer.

---

## RETRIEVEV: V-Address Resolution, Granfilade Retrieval, and Byte Opacity

The operation the question calls "RETRIEVECONTENTS" is registered in the code as `RETRIEVEV` [`init.c:49`]: `requestfns[RETRIEVEV] = retrievev`. The full execution path from FEBE entry to wire output confirms that bytes are returned verbatim with no encoding interpretation.

---

### Stage 1 — FEBE Entry Point

**`fns.c:175-186`** — `retrievev(taskptr)`:

```c
void retrievev(typetask *taskptr)
{
  typespecset specset;
  typevstuffset vstuffset;
  ...
  if (getretrievev (taskptr, &specset)
   && doretrievev (taskptr, specset, &vstuffset))
      putretrievev (taskptr, &vstuffset);
```

The caller supplies a `specset` which may contain `VSPECID` items (V-address specs with a document ISA and V-spans).

---

### Stage 2 — V→I Conversion Through the POOM

**`do1.c:338-346`** — `doretrievev`:

```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr)
{
  typeispanset ispanset;
  return
     specset2ispanset (taskptr, specset, &ispanset, READBERT)
  && ispanset2vstuffset (taskptr, granf, ispanset, vstuffsetptr);
}
```

The two-step structure is explicit: first convert V-spans to I-spans, then look up content by I-span.

**`do2.c:14-46`** — `specset2ispanset`: For each `VSPECID` item, it fetches the document's POOM via `findorgl`, then calls `vspanset2ispanset`:

```c
findorgl(taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset(taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))
```

**`orglinks.c:397-402`** — `vspanset2ispanset` delegates immediately to `permute` with direction V→I:

```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```

**`orglinks.c:425-454`** — `span2spanset` calls `retrieverestricted` on the POOM to find POOM leaf nodes (`type2dcbc`) whose V-dimension intersects the requested V-span, then reads their I-dimension off as output spans. The POOM is a two-dimensional enfilade: every leaf maps a contiguous V-interval to a corresponding I-interval. `context2span` (`context.c:176-212`) applies span-clipping arithmetic to produce the exact I-span segment.

This means a V-span does not resolve to a single I-address point. It resolves to one or more I-spans, potentially clipped from multiple POOM leaves. Those I-spans become the lookup keys for the next stage.

---

### Stage 3 — I-Address Lookup in the Granfilade

**`granf1.c:57-74`** — `ispanset2vstuffset`: iterates over each I-span and calls `ispan2vstuffset`.

**`granf2.c:286-318`** — `ispan2vstuffset`:

```c
movetumbler (&ispanptr->stream, &lowerbound);
tumbleradd(&lowerbound, &ispanptr->width, &upperbound);
context = retrieveinspan ((typecuc*)fullcrumptr, &lowerbound, &upperbound, WIDTH);
for (temp = context; temp; temp = temp->nextcontext) {
    if (context2vstuff (taskptr, temp, ispanptr, &vstuffset)) {
        *vstuffsetptr = vstuffset;
        vstuffsetptr = (typevstuffset *)&((typeitemheader *)vstuffset)->next;
    }
}
```

`retrieveinspan` (`retrie.c:112-136`) descends the GRAN enfilade, calling `findcbcinspanseq` to collect all leaf nodes (`typecbc`) whose I-coordinate range intersects `[lowerbound, upperbound]`.

**`context.c:151-174`** — `makecontextfromcbc` copies the leaf node's `cinfo` (which is a `typebottomcruminfo` / `typegranbottomcruminfo`) verbatim into a `typecontext` struct using `moveinfo`, which is `memmove` [`wisp.h:117`]. The leaf's raw `textstring` byte array comes with it.

---

### Stage 4 — Raw Byte Extraction from the Granfilade Leaf

**`context.c:240-275`** — `context2vstuff`: dispatches on the leaf info type:

```c
contextinfotype = context->contextinfo.granbottomcruminfo.infotype;
if (contextinfotype != GRANTEXT && contextinfotype != GRANORGL)
    return (FALSE);
switch (contextinfotype) {
  case GRANTEXT:
    vstuffset = (typevstuffset) taskalloc (taskptr, sizeof (typetext));
    ((typeitemheader *)vstuffset)->itemid = TEXTID;
    context2vtext (context, ispanptr, vstuffset);
    if (((typetext *)vstuffset)->length == 0)
        return (FALSE);
    break;
  case GRANORGL:
    ...  /* returns link address, not bytes */
```

**`context.c:277-309`** — `context2vtext` — **this is the critical function**. It computes the byte-offset `i` and byte-count `vtlength` based on the intersection of the granfilade leaf's I-range with the requested I-span, then:

```c
((typetext *)vstuffset)->length = vtlength > 0 ? vtlength : -vtlength;
movmem (&context->contextinfo.granbottomcruminfo.granstuff.textstuff.textstring[i],
        ((typetext *)vstuffset)->string,
        ((typetext *)vstuffset)->length);
```

`movmem` is defined as `memmove` [`common.h:163`]. This is a raw byte copy from `typegrantext.textstring[GRANTEXTLENGTH]` (the leaf field — see `wisp.h:75-77`). No encoding conversion of any kind.

The only arithmetic performed is span-clipping: computing which byte offset `i` into the leaf's `textstring` aligns with the start of the requested I-span, and how many bytes `vtlength` cover the intersection. The bytes themselves are untouched.

---

### Stage 5 — Write Path to Wire

**`putfe.c:270-275`** — `putretrievev` calls `putitemset` on the vstuffset.

**`putfe.c:189-218`** — `puttextset`/`puttext` — each byte leaves as-is:

```c
for (i = 0; i < textptr->length; ++i)
    xuputc (textptr->string[i], taskptr->outp);
```

A commented-out alternative at `putfe.c:216` shows the original form was even more explicit:

```c
/*        write (fileno(taskptr->outp), textptr->string, textptr->length); */
```

That `write(2)` syscall was replaced with the `xuputc` loop for portability, but the semantics are identical: raw bytes, byte by byte.

---

### Storage Is Also Opaque

For completeness: text is stored into the granfilade leaf at `granf2.c:97-100`:

```c
locinfo.granstuff.textstuff.textlength = textset->length;
movmem(textset->string, locinfo.granstuff.textstuff.textstring,
       locinfo.granstuff.textstuff.textlength);
insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
```

Again `memmove`, no interpretation. The bytes that went in are the bytes that come out.

---

### Answer

**Yes.** RETRIEVEV resolves V-addresses to I-spans by traversing the POOM enfilade (a two-dimensional POOM tree), then uses those I-spans as lookup keys into the GRAN granfilade. When a matching granfilade leaf of type `GRANTEXT` is found, its `textstring` byte array is copied directly into the output `typetext` buffer using `memmove` (`context.c:308`), with only span-intersection arithmetic applied to determine which subset of bytes to copy. Those bytes are then written to the wire byte-by-byte with no transformation (`putfe.c:217-218`). No encoding layer, codec, or character interpretation exists anywhere in the path. **INV-BYTE-OPAQUE holds end-to-end**: the backend stores, retrieves, and retransmits content as raw byte sequences. The only operations performed on byte values are counting them and indexing into them for span-clip arithmetic.
