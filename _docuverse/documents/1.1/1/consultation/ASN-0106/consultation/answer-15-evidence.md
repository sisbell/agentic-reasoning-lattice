## Question 15 [evidence]

> Does reading several spans together expose self-transclusion — i.e., reveal that distinct V-positions in the result share the same I-address — in a way single-span reads would not?

## KB Synthesis

No. Multi-span reads via `RETRIEVEV`/`retrieve_contents` do not expose self-transclusion in any way that single-span reads cannot, for a structural reason: the retrieve path operates entirely in the V→I→bytes direction and returns only `seq<byte>` with no I-address metadata.

## Why retrieve cannot expose it

The call chain is: SpecSet → `specset2ispanset` (POOM lookup, V→I) → `ispanset2vstuffset` (permascroll lookup, I→bytes) → byte output [PRE-RETRIEVE-CONTENTS, SS-CONTENT-IDENTITY]. I-addresses are consumed internally as lookup keys and discarded before the result reaches the client. A single-span read and a multi-span read covering the same self-transcluded regions both return identical bytes; neither exposes the I-address plumbing that connects them.

The identity ambiguity is genuine: `retrieve_contents` on two V-spans returning identical bytes cannot distinguish self-transclusion from two independent inserts of the same text, because content identity is by origin (I-address), not by textual value [SS-CONTENT-IDENTITY Finding 0018]. Independent inserts at different times receive different I-addresses even for identical characters [INV-NO-IADDR-REUSE].

## What actually exposes self-transclusion

Three I-space operations reveal shared I-address identity:

1. **`compare_versions`** [SS-COMPARE-VERSIONS, EC-SELF-COMPARISON]: Explicitly intersects I-spans. `compare_versions(doc, doc)` returns the entire document as shared content — every self-transcluded pair shows up as a correspondence. Within the same document, `compare_versions` on overlapping regions will report them as sharing identity.

2. **`find_links`** [INV-LINK-IDENTITY-DISCOVERY, Finding 0039]: Discovery operates in I-space via the spanf index. A link created on V-position A is findable from V-position B if both map to the same I-address. The POOM is a multimap [SS-POOM-MULTIMAP], so `ispan2vspanset` returns ALL V-positions sharing an I-address, and `find_links` discovers links from any of them.

3. **`retrieve_endsets`** [SS-RETRIEVE-ENDSETS]: Also operates in I-space via the spanfilade; returns endsets by I-address intersection, not V-position.

## The structural reason multi-span doesn't add anything

The POOM is queried per-VSpec independently [SS-SPECSET, INV-SPECSET-ORDER]. Multiple VSpecs in a SpecSet produce multiple independent POOM lookups; there is no cross-VSpec I-address comparison within the retrieve operation itself. The subspace convention [INV-SUBSPACE-CONVENTION] and dual-enfilade architecture [SS-DUAL-ENFILADE] keep content retrieval (granf path) entirely separate from the I-address identity machinery (spanf path).

**Summary:** Multi-span reads cannot expose self-transclusion because `retrieve_contents` is a pure V→bytes function with no I-address output. Identity exposure requires `compare_versions`, `find_links`, or `retrieve_endsets` — all of which operate explicitly in I-space and are independent of how many V-spans you read at once.

---

## Code Exploration

I now have everything needed for a complete answer. Let me compile the full trace.

---

## Does Multi-Span Reading Expose Self-Transclusion?

**Short answer: No — `retrieve_v` never returns I-addresses for text content; multi-span reads do not structurally reveal that distinct V-positions share an I-address any more than comparing separate single-span reads would. For link atoms, the I-address is included in the response in both cases.**

---

### The Retrieval Pipeline (traced from source)

**Entry point** — `fns.c:175`:
```c
void retrievev(typetask *taskptr)
{
    getretrievev (taskptr, &specset)
    && doretrievev (taskptr, specset, &vstuffset))
       putretrievev (taskptr, &vstuffset);
```

**Phase 1: V → I** — `do1.c:338`:
```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr)
{
    return
       specset2ispanset (taskptr, specset, &ispanset, READBERT)
    && ispanset2vstuffset (taskptr, granf, ispanset, vstuffsetptr);
}
```

`specset2ispanset` (`do2.c:14`) walks the specset list. For each `VSPECID` item it calls `vspanset2ispanset` → `permute(taskptr, orgl, vspanptr, V, ispansetptr, I)` (`orglinks.c:397–401`). The resulting I-spans are **appended in sequence** to one flat linked list with **no deduplication**:

```c
for (; specset; specset = ...) {
    if (itemid == VSPECID)
        ispansetptr = vspanset2ispanset(..., ispansetptr);  // do2.c:36
}
```

If the caller sends two V-specs that happen to map to the same I-span (self-transclusion), `ispanset` will contain that I-span **twice**, linked end-to-end.

**Phase 2: I → content** — `granf1.c:57`:
```c
for (; ispanset; ispanset = ispanset->next) {
    vstuffsetptr = ispan2vstuffset (taskptr, granfptr, ispanset, vstuffsetptr);
}
```

For each I-span, `ispan2vstuffset` (`granf2.c:286`) calls `retrieveinspan` on the granfilade, then for each crum context calls `context2vstuff`.

**`context2vstuff`** (`context.c:240`) produces one of two item types:

| Crum type | Output item | What's included |
|-----------|-------------|-----------------|
| `GRANTEXT` | `TEXTID` | Raw character bytes only — **no I-address** |
| `GRANORGL` | `ADDRESSID` | The I-address of the link orgl: `context->totaloffset.dsas[WIDTH]` |

For `GRANTEXT`:
```c
case GRANTEXT:
    ((typeitemheader *)vstuffset)->itemid = TEXTID;
    context2vtext (context, ispanptr, vstuffset);  // context.c:259–260
```
`context2vtext` (`context.c:277`) copies only the character bytes — V-addresses are **not included**.

For `GRANORGL`:
```c
case GRANORGL:
    ((typeitemheader *)vstuffset)->itemid = ADDRESSID;
    movetumbler (&context->totaloffset.dsas[WIDTH], &((typelink *)vstuffset)->address);
    // context.c:271
```
The I-address (the WIDTH-dimension offset in the granfilade) is included.

**Wire serialization** — `putfe.c:270–274`:
```c
int putretrievev(typetask *taskptr, typevstuffset *vstuffsetptr) {
    putnumber (taskptr->outp, RETRIEVEV);
    putitemset (taskptr, (typeitemset)*vstuffsetptr);
}
```

In `putitemset` (`putfe.c:124`), consecutive `TEXTID` items are **merged** before being counted and sent:
```c
while (itemid == TEXTID && next && next->itemid == TEXTID)
    temp = next;  // count lots of textitems as one item   putfe.c:130–131
```
Then `puttextset` concatenates their bytes into one `TEXTFLAG | length | bytes` wire item.

For `ADDRESSID`:
```c
case ADDRESSID:
    puttumbler (outfile, &((typeaddress *)itemptr)->address);  // putfe.c:173
```
Only the I-address tumbler is sent — no ADDRESSFLAG prefix, no V-address.

---

### What Happens Under Self-Transclusion

Say document D has "ABC" placed at V-position v₁ and again transcluded to V-position v₂ (both map to I-span [iₓ, iₓ+3]).

**Two separate single-span reads**:
- Read [v₁]: `vspanset2ispanset` → [iₓ, iₓ+3] → granfilade → `TEXTID: "ABC"`
- Read [v₂]: same path → `TEXTID: "ABC"`

The client gets identical text on both reads. Equal text is consistent with self-transclusion, but also consistent with identical text at different I-addresses. **The I-address is not in the response.**

**One multi-span read** (both V-spans in one specset):
- `specset2ispanset` produces `ispanset = [iₓ, iₓ+3] → [iₓ, iₓ+3]` (same span twice)
- `ispanset2vstuffset` processes each I-span independently; `retrieveinspan` traverses the same granfilade crums twice; two `TEXTID: "ABC"` items are produced
- `putitemset` **merges** the consecutive TEXTID items into a single wire item: `TEXTFLAG | 6 | "ABCABC"`

**The merging is critical**: the client receives one 6-byte text chunk. It cannot determine from this response where V-span1's content ends and V-span2's begins — the span boundaries are **erased** in the wire format. If anything, multi-span reads are *less* revealing of the V→I structure than comparing two separate reads, because the merging hides the boundary.

---

### The Link-Atom Case

For `GRANORGL` crums, the I-address is included in the response (`context.c:271`). If two V-positions reference the same link orgl (same I-address in the granfilade), then:

- Two separate reads each return an `ADDRESSID` item with the same tumbler
- One multi-span read also returns two `ADDRESSID` items with the same tumbler (link atoms are not merged — only `TEXTID` items are merged by `putitemset`)

In this case a client can compare the two ADDRESSID tumblers and detect that they're equal — revealing that both V-positions point to the same link. But this equality is equally visible whether you read them separately or together; multi-span doesn't add structural power here.

---

### The Operation That Actually Exposes Self-Transclusion

The operation designed to structurally expose shared I-content is `show_relation_of_2_versions` (`do1.c:428`):

```c
bool doshowrelationof2versions(...)
{
    specset2ispanset(taskptr, version1, &version1ispans, READBERT)
    specset2ispanset(taskptr, version2, &version2ispans, READBERT)
    intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
    ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
}
```

This:
1. Converts both specsets to I-spans
2. Computes their **I-span intersection** (shared I-content)
3. Converts the intersection back to V-span pairs via `ispansetandspecsets2spanpairset` → `makespanpairset` (`do2.c:197`)

The wire response (`putshowrelationof2versions`, `putfe.c:299`) serializes the `typespanpairset` — a list of `(stream1, stream2, widthofspan)` triples (`xanadu.h:41`). Each triple gives the V-position in doc1, the V-position in doc2, and the width of the shared content. **This is the operation that explicitly reveals the V↔V relationship mediated by a shared I-address.**

---

### Conclusion

`retrieve_v` discards all V→I mapping information before forming the response. The response is a flat sequence of text bytes and link I-addresses — no V-addresses appear at any level. For text content specifically:

- Neither single-span nor multi-span reads include I-addresses in the response
- Multi-span reads merge consecutive text chunks, **obscuring** rather than exposing span boundaries
- Detecting self-transclusion from `retrieve_v` results requires an out-of-band inference (equal text), not a structural observation

Multi-span reads through `retrieve_v` do not expose shared I-addresses in a way that single-span reads do not. The designed mechanism for V↔V identity comparison is `show_relation_of_2_versions`, which explicitly intersects I-span sets and returns V-span pairs.
