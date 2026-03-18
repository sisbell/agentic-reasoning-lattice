## Question 17 [gregory]

> If doc1 contains "ABCDE" and doc2 transcludes "BCD" (a partial span), does doc2's POOM entry store a V-width of 3 with an I-displacement pointing to I-address of "B" — and does `compare_versions` correctly identify the 3-character overlap between doc1 and doc2 despite the differing V-address ranges?

## KB Synthesis

Yes to both parts. Here is the synthesis:

---

## doc2's POOM entry after transcluding "BCD"

From [SS-POOM-BOTTOM-CRUM] (Finding 0076), each POOM bottom crum stores dual-space coordinates:

```
BottomCrum = {
  origin: { dsas[I]: I-address of "B",  dsas[V]: V-address of "B" in doc2 }
  width:  { dsas[I]: tumbler for 3 (I-precision),
             dsas[V]: tumbler for 3 (V-precision, different encoding) }
}
```

The I-origin is precisely the I-address of "B" in the permascroll — whatever was allocated when "ABCDE" was first inserted into doc1. From [ST-VCOPY] (Finding 0018), vcopy preserves I-addresses: the transcluded "BCD" in doc2 holds the same I-addresses as "BCD" in doc1. No new I-addresses are allocated.

From [SS-INSERT-VWIDTH-ENCODING] (Finding 0076), the V-width encoding uses `shift = tumblerlength(vsaptr) - 1` and `tumblerincrement(zero, shift, 3)` — so if the V-address is `1.1` (tumblerlength=2), the V-width is encoded as `0.3` (exp=-1, mantissa[0]=3), while the I-width is copied directly at I-space precision. From [INV-WIDTH-VALUE-EQUIVALENCE], both encode the integer 3 but as structurally distinct tumblers.

From [ST-VCOPY-CONTIGUITY] (Finding 0033), because "BCD" in doc1 occupies a contiguous V-span (and thus maps to contiguous I-addresses), the transcluded result in doc2 is a single consolidated I-span — one POOM crum, not three.

---

## compare_versions correctly finds the 3-character overlap

From [SS-COMPARE-VERSIONS] (Finding 0015), compare_versions operates in I-space:

> Each pair `(span_a, span_b)` satisfies: `VSpanToISpan(doc_a, span_a) == VSpanToISpan(doc_b, span_b)`

The algorithm ([INT-SPORGL-VERSION-COMPARE], Finding 0013):
1. Convert both documents' V-spans to sporgls (carrying I-address + document provenance)
2. Intersect on I-address ranges
3. Map intersection back to V-spans in each document

For this scenario:
- doc1's "ABCDE" → I-addresses I.1..I.5
- doc2's "BCD" → I-addresses I.2..I.4 (identical to doc1's "BCD" — preserved by vcopy)
- Intersection: I.2..I.4 (width 3)
- Map back: doc1 at e.g. `1.2 for 0.3`, doc2 at e.g. `1.1 for 0.3`

The differing V-address ranges are irrelevant — comparison is purely I-address-based. The result would be:

```
[(doc1: {start: "1.2", width: "0.3"}, doc2: {start: "1.1", width: "0.3"})]
```

This works because the precondition from [PRE-COMPARE-VERSIONS] (Finding 0015) is satisfied — both spans are in the text subspace (V ≥ 1.0), so I-address intersection is meaningful (permascroll addresses, not link orgl ISAs).

---

## Summary

| Property | Answer | Source |
|----------|--------|--------|
| doc2 POOM I-origin = I-address of "B" | Yes | [ST-VCOPY] F0018, [SS-POOM-BOTTOM-CRUM] F0076 |
| doc2 POOM V-width and I-width both encode 3 | Yes, different encodings | [SS-INSERT-VWIDTH-ENCODING] F0076, [INV-WIDTH-VALUE-EQUIVALENCE] F0076 |
| One consolidated POOM crum for "BCD" | Yes | [ST-VCOPY-CONTIGUITY] F0033 |
| compare_versions finds the overlap | Yes | [SS-COMPARE-VERSIONS] F0015, [INT-SPORGL-VERSION-COMPARE] F0013 |
| V-address difference is irrelevant | Yes — comparison is I-space only | [SS-COMPARE-VERSIONS] F0015 |

---

## Code Exploration

Now I have the full picture. Let me compose the complete answer.

---

## Answer

### Part 1: What Doc2's POOM Entry Stores

**Yes — the leaf crum in doc2's POOM stores an I-displacement pointing to the permascroll address of "B" and a V-width of 3.**

Here is the exact call chain when `docopy` is invoked to transclud "BCD" from doc1 into doc2:

#### Step 1 — V→I Conversion of the Source Span

`docopy` [do1.c:53] first calls `specset2ispanset` [do2.c:14] which drives `vspanset2ispanset` [orglinks.c:397], which calls `permute` [orglinks.c:404], which calls `span2spanset` [orglinks.c:425]:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex, ...);
// orglinks.c:435 — searches doc1's POOM restricted to the V-span of "BCD"
```

`retrieverestricted` [retrie.c:56] passes through to `findcbcinarea2d` [retrie.c:229], which walks doc1's POOM tree, finds the crum covering "ABCDE", and calls `makecontextfromcbc` [context.c:151] to capture that crum's absolute coordinates.

Back in `span2spanset`, `context2span` [context.c:176] clips the found crum to the "BCD" restriction:

```c
// context.c:191-196 — if crum starts before lowerbound, shift the I-start
if (tumblercmp(&grasp.dsas[idx1], &lowerbound) == LESS) {
    tumblerincrement(&grasp.dsas[idx2], 0,
        (INT)tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
        &grasp.dsas[idx2]);
}
// context.c:197-202 — if crum ends after upperbound, trim the I-end
if (tumblercmp(&reach.dsas[idx1], &upperbound) == GREATER) {
    tumblerincrement(&reach.dsas[idx2], 0,
        -tumblerintdiff(&reach.dsas[idx1], &upperbound),
        &reach.dsas[idx2]);
}
movetumbler(&grasp.dsas[idx2], &foundspanptr->stream); // I("B")
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width); // width=3
```

So: doc1's POOM crum covers "ABCDE". The V-start of "BCD" is V("A")+1, so the I-start shifts by 1: I("A")+1 = **I("B")**. The V-end of "BCD" is V("A")+3, so the I-end is also clipped correspondingly. Result: `ispanset` = {stream: I("B"), width: 3}.

#### Step 2 — Insertion into Doc2's POOM

`insertpm` [orglinks.c:75] is called with `vsaptr` = the V-address in doc2 (e.g. 1.1) and `sporglset` carrying the I-span {I("B"), 3}:

```c
// orglinks.c:101
unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
//   lstream = I("B"), lwidth = 3

// orglinks.c:105
movetumbler(&lstream, &crumorigin.dsas[I]);     // I-displacement = I("B")
// orglinks.c:109
movetumbler(&lwidth, &crumwidth.dsas[I]);       // I-width = 3
// orglinks.c:113
movetumbler(vsaptr, &crumorigin.dsas[V]);       // V-address in doc2

// orglinks.c:115-117 — V-width derived from I-width
shift = tumblerlength(vsaptr) - 1;
inc = tumblerintdiff(&lwidth, &zero);            // = 3
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);  // V-width = 3
```

`insertnd` [insertnd.c:15] is then called, and for a fresh doc2 the call reaches `firstinsertionnd` [insertnd.c:199]:

```c
movewisp(origin, &ptr->cdsp);  // cdsp.I = I("B"), cdsp.V = doc2's V-address
movewisp(width, &ptr->cwid);   // cwid.I = 3,       cwid.V = 3
```

**The crum stored in doc2's POOM therefore has:**
- `cdsp.dsas[I]` = I("B") — the permascroll address of "B"
- `cwid.dsas[I]` = 3 — I-width (3 characters)
- `cwid.dsas[V]` = 3 — V-width (computed identically from the integer 3 at `orglinks.c:117`)

---

### Part 2: Does `compare_versions` Correctly Find the 3-Character Overlap?

**Yes — and it works precisely because the comparison occurs entirely in I-space (the permascroll), where both documents agree on the addresses of "B", "C", and "D".**

The entry point is `doshowrelationof2versions` [do1.c:428]:

```c
filter_specset_to_text_subspace(taskptr, version1);  // do1.c:440
filter_specset_to_text_subspace(taskptr, version2);  // do1.c:441
// (removes link subspace spans at V < 1.0; both ABCDE and BCD survive)

specset2ispanset(taskptr, version1, &version1ispans, READBERT)  // → {I("A"), 5}
&& specset2ispanset(taskptr, version2, &version2ispans, READBERT) // → {I("B"), 3}
&& intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
&& ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
```

#### The V→I Conversion

- **Doc1**: `specset2ispanset` walks doc1's POOM (which has a crum for "ABCDE") and maps the full V-range → I-span {stream: I("A"), width: 5}.
- **Doc2**: `specset2ispanset` walks doc2's POOM (the crum just created above) and maps doc2's V-range → I-span {stream: I("B"), width: 3}.

Both use the same `permute`→`span2spanset`→`retrieverestricted`→`context2span` path described above. The V-addresses in the two documents are irrelevant at this point — only the I-addresses survive.

#### The Intersection

`intersectspansets` [correspond.c:145] calls `comparespans` [correspond.c:191] → `spanintersection` [correspond.c:210]:

```c
// correspond.c:247-256 — case where aptr.stream < bptr.stream (I("A") < I("B"))
case LESS:
    movetumbler(&bptr->stream, &cptr->stream);   // result.stream = I("B")
    switch (tumblercmp(&aend, &bend)) {
      case GREATER:   // aend=I("A")+5 > bend=I("B")+3, so:
          movetumbler(&bptr->width, &cptr->width); // result.width = 3
    }
```

Result: `commonispans` = {stream: I("B"), width: 3} — the 3-character overlap in permascroll space.

#### Mapping Back to V-Addresses

`ispansetandspecsets2spanpairset` [do2.c:185] calls `restrictspecsetsaccordingtoispans` [correspond.c:18], which calls `restrictvspecsetovercommonispans` [correspond.c:52]:

```c
// correspond.c:74 — for each document, convert the common I-span back to V-spans
ispan2vspanset(taskptr, versionorgl, ispanset, &docvspanset);
```

`ispan2vspanset` [orglinks.c:389] calls `permute` in the reverse direction (I→V), querying each document's POOM restricted to {I("B"), 3}. Doc1's POOM maps this back to V("B")..V("D") in doc1; doc2's POOM maps it back to V("B_in_doc2")..V("D_in_doc2").

Finally `makespanpairset` [correspond.c:267] → `makespanpairsforispan` [correspond.c:290] zips these two V-span sequences together character-by-character, producing a `spanpair` with:
- `stream1` = V-address of "BCD" in doc1
- `stream2` = V-address of "BCD" in doc2 (the entire V-content of doc2)
- `widthofspan` = 3

---

### Summary

| Question | Answer | Key cite |
|---|---|---|
| Does doc2's POOM crum store I-displacement = I("B")? | **Yes** | `orglinks.c:105`, `context.c:194` |
| Does doc2's POOM crum store V-width = 3? | **Yes** | `orglinks.c:115–117` |
| Is the V-width computed from the I-width? | **Yes** — `tumblerintdiff` on `lwidth` gives integer 3, placed at the correct tumbler level | `orglinks.c:116–117` |
| Does `compare_versions` find the 3-char overlap despite different V-ranges? | **Yes** | `do1.c:428–449`, `correspond.c:210–258` |
| How? | Both docs' V-spans are mapped to the same permascroll I-addresses; the intersection is performed in I-space where doc1's [I("A"),5) ∩ doc2's [I("B"),3) = [I("B"),3) | `retrie.c:56`, `context.c:176`, `correspond.c:210` |

The differing V-address ranges are never compared against each other. The POOM acts as a pure bijection between each document's private V-space and the shared permascroll I-space. `compare_versions` exploits that both POOM enfilades point into the same I-space — the intersection there is authoritative, and the result is then projected back to each document's V-space independently.
