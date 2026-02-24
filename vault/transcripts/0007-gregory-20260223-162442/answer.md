## KB Synthesis

Looking at this question, I need to trace through how link endset storage and retrieval handle V-space fragmentation caused by INSERT.

## The Scenario

Initial state:
- Link target endset references I-addresses [.0.1.3, .0.1.7] (5 contiguous I-addresses)
- These map to contiguous V-positions, say V:[1.3, 1.7]
- INSERT occurs at V:1.5 with width 0.10

After INSERT:
- I-addresses .0.1.3-.0.1.4 remain at V:[1.3, 1.4] (before insertion)
- I-addresses .0.1.5-.0.1.7 shift to V:[1.15, 1.17] (after insertion)
- Same I-addresses, now non-contiguous in V-space

## How Endsets Are Stored

From `[SS-LINK-ENDPOINT]` Finding 0037:
> "A link endset is not simply a set of V-spans; internally it is a set of I-spans (sporgls). A single user-visible V-span may correspond to multiple I-spans in the endset when the V-span covers content transcluded from multiple sources. Each I-span independently tracks its content identity."

The endset is stored as I-address ranges (sporgls). At creation time, the contiguous I-range [.0.1.3, .0.1.7] was likely stored as a single I-span.

## How RETRIEVEENDSETS Converts I-to-V

From `[SS-RETRIEVE-ENDSETS]` Finding 0035:
> "RETRIEVEENDSETS (opcode 28) takes a specset... converts the input specset to a sporglset (V-to-I translation), defines three search spaces... The use of the querying document's docid for V-address resolution means endsets are always expressed relative to the querying context."

The conversion path from `[INV-ITOV-FILTERING]` Finding 0048:
> "`linksporglset2specset()` calls `sporglset2vspanset()` which calls `ispan2vspanset()` → `permute()` → `span2spanset()`. At `span2spanset()`, `retrieverestricted()` searches the target document's POOM for the I-address."

## The Critical Finding

From `[SS-LINK-ENDPOINT]` Finding 0037:
> "When retrieving endsets, `retrieve_endsets` reports multiple V-spans corresponding to the stored I-spans, **one per contiguous I-region**."

But more importantly, from the I-to-V conversion process, the system walks through the I-address range and discovers which V-positions they currently map to. When the POOM lookup finds:
- I:.0.1.3-.0.1.4 → V:[1.3, 1.4] (contiguous)  
- I:.0.1.5-.0.1.7 → V:[1.15, 1.17] (contiguous but separated by gap)

These form **two non-contiguous V-ranges**.

## Confirming Evidence

From `[EC-PIVOT-LINK-FRAGMENTATION]` Finding 0019:
> "When linked content is rearranged via pivot, the link's endsets become fragmented into multiple spans... Before: 'ABCDEFGH' — link on 'CD' at V 1.3 width 0.2. Pivot: swap BC and DE. After: 'ADEBCFGH' — endsets report FOUR spans"

This demonstrates that when linked content becomes non-contiguous in V-space (whether by pivot or by INSERT creating a gap), the endset retrieval fragments into multiple spans.

## Answer

**RETRIEVEENDSETS returns TWO VSpecs** for that endset.

The reasoning chain:
1. The endset stores I-addresses [.0.1.3, .0.1.7] as a contiguous I-span (`[ST-INSERT]`, `[INV-IADDR-IMMUTABILITY]`)
2. INSERT shifts V-positions but not I-addresses, creating a V-space gap (`[ST-INSERT]` Finding 0030)
3. I-to-V conversion discovers two non-contiguous V-ranges: [1.3, 1.4] and [1.15, 1.17] (`[INV-ITOV-FILTERING]`)
4. RETRIEVEENDSETS reports one VSpec per contiguous V-range (`[SS-LINK-ENDPOINT]` Finding 0037)
5. Result: Two VSpecs in the endset, even though the I-addresses remain contiguous (`[EC-PIVOT-LINK-FRAGMENTATION]` confirms this fragmentation behavior)

## Code Exploration

Based on my code analysis and the golden test evidence, I can provide a definitive answer:

## Answer: ONE VSpec with MULTIPLE VSpans

When INSERT splits a contiguous I-address range that a link's target endset references, **RETRIEVEENDSETS returns ONE VSpec containing MULTIPLE VSpans** (not multiple VSpecs).

## Code Evidence

### Storage at Link Creation [spanf1.c:15-54]

When the link is created with target endset I:[.0.1.3,.0.1.7], `insertspanf` stores it as **one contiguous entry** in the spanfilade:

```c
bool insertspanf(...) {
    for (; sporglset; sporglset = ...) {
        // Extract I-span data
        movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);
        movetumbler(&lwidth, &crumwidth.dsas[SPANRANGE]);
        insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, ...);
    }
}
```

**One I-span → One insertion → One CBC in the spanfilade**

### Retrieval After INSERT Split

The key conversion happens in `span2spanset` [orglinks.c:425-454]:

```c
typespanset *span2spanset(...) {
    // Query organfilade to convert I-span to V-spans
    context = retrieverestricted((typecuc*)orgl, restrictionspanptr, 
                                 restrictionindex, ..., targindex, ...);
    
    // For EACH context (one per contiguous V-region), create a V-span
    for (c = context; c; c = c->nextcontext) {
        context2span(c, ..., &foundspan, targindex);
        nextptr = (typespan*)onitemlist(taskptr, (typeitem*)&foundspan, ...);
    }
}
```

When the organfilade lookup finds the I-addresses now map to **non-contiguous V-positions**, `retrieverestricted` returns **multiple contexts** [retrie.c:262-263]:

```c
for (; crumptr; crumptr = getrightbro(crumptr)) {
    if (crumptr->height != 0) {
        findcbcinarea2d(findleftson((typecuc*)crumptr), ...);
    } else {
        context = makecontextfromcbc((typecbc*)crumptr, ...);
        incontextlistnd(headptr, context, index1);  // Adds to list
    }
}
```

**Each CBC covering part of the query → One context → One V-span in output**

### Final Assembly [sporgl.c:103-120]

```c
bool linksporglset2specset(...) {
    for (; sporglset; sporglset = ...) {  // ONE iteration for our single I-span
        specset = (typespecset)taskalloc(taskptr, sizeof(typevspec));
        linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
        // ^^ This converts the I-span to MULTIPLE V-spans within ONE vspec
        *specsetptr = specset;  // ONE vspec added to result
    }
}
```

And `sporglset2vspanset` [sporgl.c:157] calls `ispan2vspanset`, which populates `vspec->vspanset` with all the V-spans.

## Golden Test Confirmation

Test `golden/endsets/endsets_after_pivot.json` demonstrates this:

```json
{
  "op": "retrieve_endsets",
  "label": "after",
  "source": [
    {
      "docid": "1.1.0.1.0.1",       // ONE VSpec
      "spans": [                      // FOUR VSpans
        {"start": "1.2", "width": "0.1"},
        {"start": "1.2", "width": "0.1"},
        {"start": "1.5", "width": "0.1"},
        {"start": "1.5", "width": "0.1"}
      ]
    }
  ]
}
```

After a PIVOT operation split the originally contiguous I-addresses into non-contiguous V-positions, the result is **one docid entry (one VSpec) with multiple spans (multiple VSpans)**.

## The Critical Distinction

- **Input to spanfilade**: ONE I-span (stored as one entry)
- **Spanfilade retrieval**: ONE sporgl (one context from the spanfilade)
- **VSpec creation**: ONE VSpec (one per sporgl)
- **I→V conversion**: MULTIPLE contexts from organfilade lookup
- **Final result**: ONE VSpec containing MULTIPLE VSpans

The split happens **during I→V address translation**, not during spanfilade retrieval. The endset data is still stored as one I-span, but when converted to V-space, it produces multiple V-spans within a single VSpec container.
