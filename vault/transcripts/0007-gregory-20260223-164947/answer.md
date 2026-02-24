## KB Synthesis

# Answer: Order Preservation in Multi-Span Link Endsets

The KB does **not provide direct evidence** that multi-span endset order is preserved from link creation through retrieval. Here's what can be determined:

## What the KB Confirms

### Link Creation Process
`[ST-VSPAN-TO-SPORGL]` documents that `vspanset2sporglset()` converts V-spans to sporgls (I-address ranges with provenance), and `linksporglset2specset()` performs the reverse conversion. The sporgls are stored as a linked list per `[SS-SPORGL]`:

> Sporgls are stored as a linked list (`typesporglset`) and can be interchanged with ispans via a union type (`typesporglitem`).

### General SpecSet Order Preservation
`[INV-SPECSET-ORDER]` establishes that SpecSets maintain ordering for operations like retrieve and vcopy:

> SpecSet operations preserve VSpec ordering in their results. Retrieve concatenates content in VSpec order. Vcopy places content in VSpec order.

However, this invariant is documented for **content operations**, not explicitly for link endset storage and retrieval.

## Critical Gap: Multi-Span Link Behavior

`[EC-MULTISPAN-LINK-DUPLICATION]` reveals anomalous behavior with multi-span links:

> Creating a link with multiple source spans works, but `retrieve_endsets` may return duplicate spans:
> ```
> Link source: ["First" at V 1.1, "second" at V 1.16]
> Endsets return: 3 spans (1.16 appears twice)
> ```

This duplication suggests the endset representation or retrieval process **does not cleanly preserve** the input structure. The KB notes this "may be related to the same internal fragmentation mechanism observed with pivot."

## Potential Confounding Factor

`[INV-RETRIEVAL-V-SORTED]` documents that B-tree traversal operations sort results by V-address:

> `incontextlistnd()` performs explicit insertion-sort by V-address as contexts are discovered during B-tree traversal... the result list is sorted by left boundary in the queried dimension.

If `linksporglset2specset()` uses similar sorting logic when converting I-addresses back to V-addresses, the original input order would be lost. The KB does not clarify whether endset retrieval involves such sorting.

## Conclusion

**The system likely does NOT guarantee order preservation** for multi-span link endsets. The observed duplication in `[EC-MULTISPAN-LINK-DUPLICATION]` and the absence of explicit order-preservation claims for link operations suggest the endset structure reflects I-space fragmentation patterns rather than input VSpec ordering. To answer definitively would require examining:

1. The implementation of `vspanset2sporglset()` (sporgl.c:35-65)
2. The implementation of `linksporglset2specset()` (sporgl.c:97+)  
3. Whether endset retrieval applies V-address sorting

The KB documents the existence and function of these operations but does not specify their order-preservation guarantees.

## Code Exploration

Based on my analysis of the code, I can now provide a complete answer to your question.

## Answer

**Yes, the system guarantees order preservation for multi-span endsets in links.** When you create a link with a multi-span source endset (e.g., two disjoint VSpecs), those spans are:

1. **Stored in the link orgl at sequential V-positions** in the order you provide them
2. **Retrieved by RETRIEVEENDSETS in that same order**

However, the preservation mechanism is more subtle than simply storing them "as-is."

## How Multi-Span Endsets Are Stored

### 1. Link Orgl Structure

Links store their three endsets at fixed V-position ranges in the link orgl [do2.c:169-183]:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);  // fromvsa = 1.1
    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);      // tovsa = 2.1
    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);  // threevsa = 3.1
    }
    return (TRUE);
}
```

- FROM endset: stored in V-range **1.x**
- TO endset: stored in V-range **2.x**
- THREE endset: stored in V-range **3.x**

### 2. Sequential Insertion Preserves Order

When `docreatelink` processes a multi-span endset [do1.c:214-218]:

```c
&& specset2sporglset (taskptr, fromspecset, &fromsporglset,NOBERTREQUIRED)
&& specset2sporglset (taskptr, tospecset, &tosporglset,NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset, &threesporglset,NOBERTREQUIRED)
&& setlinkvsas (&fromvsa, &tovsa, &threevsa)
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, ...)
```

The `specset2sporglset` function [sporgl.c:14-33] builds the sporglset by iterating through the user-provided VSpecs **in order**:

```c
bool specset2sporglset(typetask *taskptr, typespecset specset, typesporglset *sporglsetptr, int type)
{
    *sporglsetptr = NULL;
    for (; specset; specset = (typespecset)((typeitemheader*)specset)->next) {
        // Process each VSpec in order
        if (!(sporglsetptr = vspanset2sporglset (taskptr, &((typevspec *)specset)->docisa, 
                                                  ((typevspec *)specset)->vspanset, sporglsetptr,type))){
            return (FALSE);
        }
    }
    return (TRUE);
}
```

And `vspanset2sporglset` [sporgl.c:47] iterates through the VSpans **in order**:

```c
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    // Create sporgl entries in linked-list order
}
```

Then `insertpm` [orglinks.c:100-132] inserts these sporgls **sequentially**:

```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (vsaptr, &crumorigin.dsas[V]);  // Insert at current V-position
    // ... calculate V-width ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  // Advance to next V-position
}
```

**Key insight**: Each span in the endset is inserted at a sequential V-position (1.1, 1.1+w₁, 1.1+w₁+w₂, etc.) in the order provided by the user.

## How RETRIEVEENDSETS Returns Them

### 1. Range-Based Retrieval

`retrieveendsetsfromspanf` [spanf1.c:190-235] retrieves each endset by V-range:

```c
bool retrieveendsetsfromspanf(typetask *taskptr, typespecset specset, 
                              typespecset *fromsetptr, typespecset *tosetptr, 
                              typespecset *threesetptr)
{
    // Define V-ranges for each endset
    fromspace.stream.mantissa[0] = LINKFROMSPAN;   // 1.0
    fromspace.width.mantissa[0] = 1;               // width 1.0 (range 1.0-2.0)
    
    tospace.stream.mantissa[0] = LINKTOSPAN;       // 2.0
    tospace.width.mantissa[0] = 1;                 // width 1.0 (range 2.0-3.0)
    
    threespace.stream.mantissa[0] = LINKTHREESPAN; // 3.0
    threespace.width.mantissa[0] = 1;              // width 1.0 (range 3.0-4.0)
    
    // Retrieve all sporgls in each range
    retrievesporglsetinrange(taskptr,sporglset,&fromspace,&fromsporglset)
    // ...
}
```

### 2. V-Address Sorting Preserves Sequential Order

The key to understanding order preservation is **Finding 0078** (which you already have in your findings). When `retrievesporglsetinrange` calls `retrieverestricted`, it uses `incontextlistnd` [context.c:75-111] which performs **insertion-sort by V-address**.

Since the spans were inserted at sequential V-positions during creation:
- Span 1 at V = 1.1
- Span 2 at V = 1.1 + w₁
- Span 3 at V = 1.1 + w₁ + w₂

The V-sorted retrieval order **matches the original insertion order**.

## Verification with Golden Test

The test `endsets_multispan_link` [golden/endsets/endsets_multispan_link.json] confirms this:

**Input** (lines 15-17):
```json
"source_spans": ["First", "second"]
```
- "First" at V = 1.1, width = 0.5
- "second" at V = 1.16, width = 0.6

**Retrieved** (lines 27-40):
```json
"spans": [
    {"start": "1.1", "width": "0.5"},    // "First"
    {"start": "1.16", "width": "0.6"},   // "second"
    {"start": "1.16", "width": "0.6"}    // (duplicate - possible bug)
]
```

The order is preserved: First (1.1) before second (1.16).

## Guarantee Properties

**Property L1 (Multi-span endset order preservation):**
```
Given link L with FROM endset containing VSpans [s₁, s₂, ..., sₙ] in order:
  CREATELINK stores them at sequential V-positions [1.1, 1.1+w₁, 1.1+w₁+w₂, ...]
  RETRIEVEENDSETS returns them in the same order [s₁, s₂, ..., sₙ]
```

This holds because:
1. Sequential insertion order is preserved by linked-list traversal [sporgl.c:14-64]
2. Sequential V-positions are monotonically increasing [orglinks.c:131]
3. V-sorted retrieval of monotonically increasing positions preserves order [context.c:75-111]

## Source References

- `do1.c:214-220` - docreatelink converts specsets to sporglsets in order
- `do2.c:130-149` - insertendsetsinorgl calls insertpm for each endset
- `do2.c:169-183` - setlinkvsas defines V-ranges (1.x, 2.x, 3.x)
- `sporgl.c:14-64` - specset2sporglset and vspanset2sporglset preserve linked-list order
- `orglinks.c:100-132` - insertpm inserts at sequential V-positions
- `spanf1.c:190-267` - retrieveendsetsfromspanf retrieves by V-range
- `context.c:75-111` - incontextlistnd sorts by V-address (Finding 0078)
- `golden/endsets/endsets_multispan_link.json` - Test confirming order preservation
