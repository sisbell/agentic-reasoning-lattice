## Question 11 [evidence]

> When SHOWRELATIONOF2VERSIONS finds two POOM entries in the compared documents whose I-spans overlap, what exactly does it return for each correspondence — a pair of VSpecs with document IDs, V-start positions, and widths, or some other structure?

## KB Synthesis

SHOWRELATIONOF2VERSIONS (FEBE opcode 10) returns a sequence of ordered pairs of V-spans. The KB gives the clearest picture from three converging entries:

**Return structure per correspondence:**

Each element of the result is a pair `(span_a, span_b)` where each span is a VSpec — carrying a document ID tumbler, a V-start position tumbler, and a width tumbler. From [SS-SPECSET]: `VSpec = (doc: Tumbler, start: Tumbler, width: Tumbler)`. From [SS-COMPARE-VERSIONS] (Finding 0015):

> "The operation produces a list of ordered pairs of V-spans — one from each document — where the paired spans reference the same permascroll I-address range."

The concrete example:
```
compare_versions(A, B) returns:
  [(A: V 1.1 for 5, B: V 1.1 for 5),    // "Hello" — same P₁..P₅
   (A: V 1.6 for 6, B: V 1.11 for 6)]   // "World" — same P₆..P₁₁
```

And from [ST-COMPARE-VERSIONS] (Finding 0030):
```
[{version_before: 1.1 for 0.2, current: 1.1 for 0.2},
 {version_before: 1.3 for 0.3, current: 1.5 for 0.3}]
```

**The invariant each pair satisfies** [SS-COMPARE-VERSIONS]:

`VSpanToISpan(doc_a, span_a) == VSpanToISpan(doc_b, span_b)`

Both I-spans must be permascroll addresses (not link orgl ISAs) — which is why the operation crashes when link-subspace spans are included [PRE-COMPARE-VERSIONS].

**Underlying mechanism** [INT-SPORGL-VERSION-COMPARE]:

Internally, both documents' content is converted to sporgls (each carrying I-address origin, width, and source document ISA), then intersection is computed on the `sporglorigin` field. The matched I-address ranges are then mapped back to V-positions in each document respectively to produce the output pairs.

**What the KB does not specify:**

The wire-level byte encoding of the FEBE response is not documented in the KB. The KB describes the semantic result as VSpec pairs, but the exact on-wire serialization format (e.g., whether doc IDs are repeated per span or implied by position in the response) is not recorded.

---

## Code Exploration

I have all the information needed. Here is the complete answer.

---

## What `SHOWRELATIONOF2VERSIONS` Returns Per Correspondence

### The Structure: `typespanpair`, not a pair of VSpecs

Each correspondence is a `typespanpair` (defined in `backend/xanadu.h:41-46`):

```c
typedef struct structspanpair {
    struct structspanpair *nextspanpair;
    tumbler stream1;
    tumbler stream2;
    tumbler widthofspan;
} typespanpair;
```

Three tumblers — not four fields (doc1, start1, doc2, start2). The document ID and V-start position are **merged into a single composite tumbler** for each side.

---

### How the Fields Are Populated

`makespanpair` at `backend/correspond.c:351-361`:

```c
typespanpair *makespanpair(typetask *taskptr, tumbler *doc1, tumbler *start1, tumbler *doc2, tumbler *start2, tumbler *width)
{
    spanpair = (typespanpair *) taskalloc (taskptr, sizeof (typespanpair));
    docidandvstream2tumbler (doc1, start1, &spanpair->stream1);
    docidandvstream2tumbler (doc2, start2, &spanpair->stream2);
    movetumbler (width, &spanpair->widthofspan);
    return (spanpair);
}
```

`docidandvstream2tumbler` at `backend/tumble.c:685-699`:

```c
int docidandvstream2tumbler(tumbler *docid, tumbler *vstream, tumbler *tumbleptr)
{
    movetumbler (docid, tumbleptr);
    for (i = NPLACES-1; i >= 0; i--) {
        if (tumbleptr->mantissa[i]) { ++i; break; }
    }
    for (j = 0; i < NPLACES && j < NPLACES;)
        tumbleptr->mantissa[++i] = vstream->mantissa[j++];
}
```

It copies the doc ID tumbler, finds its last occupied mantissa position, then appends the V-start mantissa digits immediately after. The result is a single composite tumbler of the form `docID.Vstart` — the document identifier and V-address concatenated in tumbler notation. There is no separate document ID field in the pair; the doc ID is baked into the leading digits of `stream1`/`stream2`.

---

### The Span-Splitting Logic

The width stored in `widthofspan` is not simply the width of the common I-span. `makespanpairsforispan` at `backend/correspond.c:290-349` walks the V-span lists from both documents in lock-step. When they have different V-span sizes for the same I-content, it splits at the smaller boundary:

- If `span1->width < span2->width` (LESS/EQUAL case, lines 311-321): uses `span1->width`, advances `span1` to its next entry, and slides `span2->stream` forward by `span1->width` with the remainder left on `span2`.
- If `span1->width > span2->width` (GREATER case, lines 323-328): uses `span2->width` and slides `span1` forward similarly.

**This means a single I-span overlap can produce multiple `typespanpair` entries** if the two documents have differently-chunked V-spans pointing into that I-region.

---

### Call Chain Summary

1. **`fns.c:250`** — `showrelationof2versions` calls `getshowrelationof2versions` → `doshowrelationof2versions` → `putshowrelationof2versions`.

2. **`do1.c:428`** — `doshowrelationof2versions` converts each specset to I-spans (`specset2ispanset`), intersects them to find common I-spans (`intersectspansets` with `ISPANID`), then calls `ispansetandspecsets2spanpairset`.

3. **`do2.c:185`** — `ispansetandspecsets2spanpairset` restricts both specsets to just the common I-span range (`restrictspecsetsaccordingtoispans`), then calls `makespanpairset`.

4. **`correspond.c:267`** — `makespanpairset` iterates each common I-span and calls `makespanpairsforispan`.

5. **`correspond.c:290`** — `makespanpairsforispan` produces one or more `typespanpair` nodes by walking the parallel V-span lists and splitting at the min-width boundary.

6. **`correspond.c:351`** — `makespanpair` allocates each node and packs the two `docID.Vstart` composite tumblers plus the shared width.

---

### Wire Format

`putshowrelationof2versions` (`backend/putfe.c:299-303`) serializes:

1. Opcode `SHOWRELATIONOF2VERSIONS` = 10
2. Count N (number of pairs) — `backend/putfe.c:228`
3. For each pair: `stream1` (tumbler), `stream2` (tumbler), `widthofspan` (tumbler) — `backend/putfe.c:233-238`

---

### Summary Answer

Each correspondence record contains **three tumblers**, not a quartet of separate fields:

| Field | Content |
|---|---|
| `stream1` | Composite tumbler: `doc1_ID` mantissa digits followed by V-start-in-doc1 mantissa digits |
| `stream2` | Composite tumbler: `doc2_ID` mantissa digits followed by V-start-in-doc2 mantissa digits |
| `widthofspan` | V-width of this correspondence (the minimum of the two sides' V-span widths at this step) |

Document IDs are **not separate fields** — they are embedded as the leading digits of the `stream` tumblers via `docidandvstream2tumbler` (`tumble.c:685`). The width is shared (one value serves both sides), consistent with the semantic invariant that the paired V-spans map to exactly the same I-address range and therefore have equal V-widths at each pair boundary.
