## Question 16 [evidence]

> If two VSpecs in one SpecSet resolve to the same shared I-addresses (transclusion within a document), does RETRIEVECONTENTS return the identical bytes twice, once per V-position?

## KB Synthesis

Yes — RETRIEVECONTENTS returns the identical bytes twice.

**Why:** The retrieval path is `SpecSet → specset2ispanset → ispanset2vstuffset → bytes`. Each VSpec is converted to I-addresses independently via the POOM, then the permascroll is dereferenced for each I-span in order. There is no deduplication step anywhere in this chain.

**Each layer confirms this:**

**[SS-SPECSET] / [INV-SPECSET-ORDER]:** SpecSet is a `seq<VSpec>` — a sequence, not a set. `retrieve` concatenates results in VSpec order. The example explicitly states: "Retrieve returns: 'quicklazy' — concatenated in VSpec order." Order and multiplicity are preserved.

**[PRE-RETRIEVE-CONTENTS] (Finding 0010):** `doretrievev` calls `specset2ispanset` then `ispanset2vstuffset(taskptr, granf, ispanset, vstuffsetptr)`. Each VSpec in the SpecSet contributes its I-span(s) to the accumulated ispanset. The permascroll lookup is a pure byte-range fetch — it has no concept of "I already returned these bytes."

**[SS-POOM-MULTIMAP]:** The POOM is a multimap where multiple V-positions map to the same I-address. This is the structure that makes internal transclusion possible, but the retrieval layer doesn't inspect or collapse this — it processes each V-position's I-addresses as an independent query.

**[ST-VCOPY] Finding 0039:** Explicitly shows two V-positions (1.10 and 1.19) mapping to the same I-addresses i₁..i₄ after internal transclusion. Both are valid, independently addressable positions in the document.

**Concrete consequence:** If a SpecSet contains `VSpec(doc, start=1.10, width=0.4)` and `VSpec(doc, start=1.19, width=0.4)`, and both V-ranges map to i₁..i₄, RETRIEVECONTENTS returns 8 bytes: the 4-byte sequence from i₁..i₄ concatenated with itself.

This is coherent with the design: SpecSets address V-space, and the caller is responsible for not duplicating ranges if they want deduplicated output [INT-CLIENT-VALIDATION].

---

## Code Exploration

I now have all the verified code. Here is my complete answer.

---

## RETRIEVECONTENTS and Transclusion: Do Shared I-Addresses Return Bytes Twice?

**Yes. When two VSpecs in one SpecSet resolve to the same I-address range, RETRIEVECONTENTS returns the identical bytes twice — once per V-position — with no deduplication anywhere in the call chain.**

Here is the full traced path.

---

### 1. Entry Point — `fns.c:175-187`

```c
void retrievev(typetask *taskptr)
{
  typespecset specset;
  typevstuffset vstuffset;
  bool getretrievev(), doretrievev();

       if (
      getretrievev (taskptr, &specset)
       && doretrievev (taskptr, specset, &vstuffset))
        putretrievev (taskptr, &vstuffset);
     else
        putrequestfailed (taskptr);
}
```

The full SpecSet — potentially containing multiple VSpecs — is passed intact to `doretrievev`. No filtering here.

---

### 2. V→I Conversion — `do2.c:14-46`

`specset2ispanset` is the function that converts the SpecSet of VSpecs into an ispanset. The loop at `do2.c:23` iterates through every item in the SpecSet:

```c
for (; specset; specset = (typespec *)((typeitemheader *)specset)->next) {
    if (((typeitemheader *)specset)->itemid == ISPANID) {
        *ispansetptr = (typeispanset)specset;
        ispansetptr = (typeispanset *)&((typeitemheader *)specset)->next;
    } else if (((typeitemheader *)specset)->itemid == VSPECID) {
        if (!(
          findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl,type)
        && (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr)))){
               return (FALSE);
        }
    }
}
```

Each VSpec gets independently routed to `vspanset2ispanset`. There is **no cross-VSpec deduplication**. If VSpec-A and VSpec-B both map to I-range X, I-range X will appear in the resulting ispanset twice — appended once per VSpec.

---

### 3. V-span → I-span — `orglinks.c:397-422`

`vspanset2ispanset` at `orglinks.c:397-401` delegates to `permute`:

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, typeispanset *ispansetptr)
{
  typespanset *permute();
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` at `orglinks.c:404-422`:

```c
typespanset *permute(typetask *taskptr, typeorgl orgl, typespanset restrictionspanset, INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
  typespanset *span2spanset();
  typespanset *save;
    save = targspansetptr;
    /*consolidatespans(restrictionspanset);
foospanset("restrictionset after consolidation is ",restrictionspanset);    */
       for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
        targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex, targspansetptr, targindex);
    }
    return (save);
}
```

**The critical observation is at `orglinks.c:412-413`**: `consolidatespans` is **commented out**. Even within a single VSpec, if two V-spans map to overlapping I-addresses, those I-spans are not merged. The commented-out stub at `orglinks.c:455-462` confirms this was intended but never completed:

```c
/*
consolidatespanset(spanset);
  typespan *spanset;
{
    for(;spanset->next;spanset = spanset->next){
        if(
    }
}*/
```

`span2spanset` at `orglinks.c:425-454` calls `retrieverestricted` then `onitemlist`. `onitemlist` at `orglinks.c:464-537` is a simple list append — for `ISPANID` items it does `movmem` and appends unconditionally. No equality check, no overlap check.

---

### 4. Content Retrieval — `granf1.c:57-74` and `granf2.c:286-318`

`ispanset2vstuffset` [granf1.c:57-74] iterates through every I-span in the ispanset:

```c
bool ispanset2vstuffset(typetask *taskptr, typegranf granfptr, typeispanset ispanset, typevstuffset *vstuffsetptr)
{
typevstuffset *save;
  typevstuffset *ispan2vstuffset();
save = vstuffsetptr;
    *vstuffsetptr = NULL;
    for (; ispanset; ispanset = ispanset->next) {
        vstuffsetptr = ispan2vstuffset (taskptr, granfptr, ispanset, vstuffsetptr);
    }
    return (TRUE);
}
```

For each entry in the ispanset, `ispan2vstuffset` [granf2.c:286-318] independently calls `retrieveinspan` on the I-address range and appends what it finds:

```c
typevstuffset *ispan2vstuffset(typetask *taskptr, typegranf fullcrumptr, typeispan *ispanptr, typevstuffset *vstuffsetptr)
{
  ...
    *vstuffsetptr = NULL;
    movetumbler (&ispanptr->stream, &lowerbound);
    tumbleradd(&lowerbound, &ispanptr->width, &upperbound);
    context = retrieveinspan ((typecuc*)fullcrumptr, &lowerbound, &upperbound, WIDTH);
    for (temp = context; temp; temp = temp->nextcontext) {
        if (context2vstuff (taskptr, temp, ispanptr, &vstuffset)) {
            *vstuffsetptr = vstuffset;
            vstuffsetptr = (typevstuffset *)&((typeitemheader *)vstuffset)->next;
        }
    }
    contextfree (context);
    return (vstuffsetptr);
}
```

Each call is self-contained. If the same I-address range appears twice in the ispanset (from two different V-positions that transclude the same content), `retrieveinspan` is called twice on the same range, and the bytes are appended twice to the vstuffset.

---

### Summary

The deduplication never happens. The chain is:

| Step | Function | File | What happens |
|------|----------|------|--------------|
| 1 | `retrievev` | `fns.c:175` | Passes full SpecSet to `doretrievev` |
| 2 | `specset2ispanset` | `do2.c:23-40` | Loops over VSpecs independently, no cross-VSpec dedup |
| 3 | `permute` | `orglinks.c:404-422` | `consolidatespans` **commented out** at line 412 |
| 4 | `onitemlist` | `orglinks.c:464-537` | Simple append, no duplicate check |
| 5 | `ispanset2vstuffset` | `granf1.c:67-69` | Loops over ispanset, calls `ispan2vstuffset` per entry |
| 6 | `ispan2vstuffset` | `granf2.c:286-318` | Independent fetch per I-span, no awareness of prior calls |

If two VSpecs in one SpecSet point to V-positions that transclude the same I-content, the result is the identical bytes appearing twice in the response — once per V-position — interleaved with each position's vstuff metadata.

The commented-out `consolidatespans` at `orglinks.c:412-413` is the architectural scar where deduplication was planned but never implemented.
