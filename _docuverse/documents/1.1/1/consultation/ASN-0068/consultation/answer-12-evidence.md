## Question 12 [evidence]

> Does the correspondence result returned by `compare_versions` take the form of a SpecSet pairing — i.e., a list of `(VSpec_in_doc1, VSpec_in_doc2)` tuples where each pair shares the same I-address span — or does it return I-address spans directly without V-mapping?

## KB Synthesis

`compare_versions` returns **V-span pairs**, not I-address spans directly.

[SS-COMPARE-VERSIONS] is explicit: the operation "produces a list of ordered pairs of V-spans — one from each document — where the paired spans reference the same permascroll I-address range." Each pair `(span_a, span_b)` satisfies `VSpanToISpan(doc_a, span_a) == VSpanToISpan(doc_b, span_b)`.

The concrete example from [ST-INSERT] (Finding 0030) confirms the shape:
```
[(version_before: 1.1 for 0.2, current: 1.1 for 0.2),
 (version_before: 1.3 for 0.3, current: 1.5 for 0.3)]
```

I-address arithmetic is strictly internal. [INT-SPORGL-VERSION-COMPARE] describes the mechanism: both documents' content is converted to sporgls (carrying I-addresses), intersection is computed in I-space, then results are **mapped back to V-spans** in each document. The sporgl provides provenance to perform that final mapping.

The postcondition is: for each pair `(s_a, s_b)` in the result, `s_a` is a V-span in doc_a and `s_b` is a V-span in doc_b, and they are joined by shared I-address identity. No I-addresses appear in the returned structure.

---

## Code Exploration

I now have everything I need to give a complete, code-cited answer.

---

## Answer

`compare_versions` returns **a list of `(VSpan, VSpan)` pairs** — V-address pairs, not I-addresses. The I-address computation is purely internal.

---

### The full pipeline

#### 1. Backend dispatch — `requests.h:27`
Command 10 maps to `SHOWRELATIONOF2VERSIONS`. The handler is `showrelationof2versions` at `fns.c:250`.

#### 2. Top-level handler — `fns.c:250–261`
```c
void showrelationof2versions(typetask *taskptr) {
  typespecset version1, version2;
  typespanpairset relation;
  ...
  if (getshowrelationof2versions(taskptr, &version1, &version2)
   && doshowrelationof2versions(taskptr, version1, version2, &relation))
      putshowrelationof2versions(taskptr, relation);
```
Inputs are two `typespecset` values (i.e., two VSpec-sets, one per document). Output is a `typespanpairset`.

#### 3. Core computation — `doshowrelationof2versions`, `do1.c:428–449`
```c
specset2ispanset(taskptr, version1, &version1ispans, READBERT)  // V→I for doc1
&& specset2ispanset(taskptr, version2, &version2ispans, READBERT)  // V→I for doc2
&& intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)  // shared I-spans
&& ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
```

I-addresses are the intermediate representation used to detect **common origin** (same permascroll bytes). But they are never put on the wire.

#### 4. Span pair construction — `makespanpair`, `correspond.c:351–361`
```c
docidandvstream2tumbler(doc1, start1, &spanpair->stream1);
docidandvstream2tumbler(doc2, start2, &spanpair->stream2);
movetumbler(width, &spanpair->widthofspan);
```
Each `typespanpair` stores two **global V-addresses** (`stream1`, `stream2`) plus a shared `widthofspan`. The struct is defined at `xanadu.h:41–46`:
```c
typedef struct structspanpair {
    struct structspanpair *nextspanpair;
    tumbler stream1;    // global V-address in doc1
    tumbler stream2;    // global V-address in doc2
    tumbler widthofspan;
} typespanpair;
```

#### 5. Wire format — `putspanpair`, `putfe.c:233–238`
```c
puttumbler(taskptr->outp, &spanpair->stream1);
puttumbler(taskptr->outp, &spanpair->stream2);
puttumbler(taskptr->outp, &spanpair->widthofspan);
```
Format over the wire: `N` (count), then for each entry: `stream1`, `stream2`, `widthofspan` — all V-addresses.

#### 6. Client decoding — `client.py:768–778`
```python
def compare_versions(self, specseta, specsetb):
    self.xc.command(10, specseta, specsetb)
    sharedspans = []
    for i in range(self.xc.Number()):
        starta, startb = self.xc.Address(), self.xc.Address()
        width = self.xc.Offset()
        doca, locala = starta.split()
        docb, localb = startb.split()
        sharedspans.append((VSpan(doca, Span(locala, width)),
                           VSpan(docb, Span(localb, width))))
    return collapse_sharedspans(sharedspans)
```
The client reads each global address, splits it into `(docid, local-start)`, and constructs a `VSpan(docid, Span(local_start, width))` for each side. The final result after `collapse_sharedspans` is a Python list of `(VSpan, VSpan)` pairs.

---

### What form does the result take?

The result is **not** raw I-address spans — the I-address intersection is done entirely inside `doshowrelationof2versions` and discarded before the response is serialized.

The result is **closest to a SpecSet pairing**, but at the granularity of individual `VSpan`s, not full `VSpec` objects. Concretely:
- A `VSpec` groups multiple local spans under one docid.
- The returned `(VSpan, VSpan)` pairs are each single-span entries: `VSpan(doca, Span(locala, width))` is equivalent to a one-span `VSpec` for doc1, and `VSpan(docb, Span(localb, width))` is a one-span `VSpec` for doc2.
- Adjacent pairs with the same shared width are merged by `collapse_sharedspans` (`client.py:946–969`), but the result is never further aggregated into multi-span `VSpec`s.

**Summary:** `compare_versions` returns a list of `(VSpan_in_doc1, VSpan_in_doc2)` pairs where each pair shares the same content-width and was identified as having common origin via shared I-address. The I-address is the internal mechanism; the exposed representation is V-space throughout.
