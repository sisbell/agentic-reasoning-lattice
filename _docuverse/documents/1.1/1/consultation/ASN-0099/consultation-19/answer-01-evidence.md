## Question 1 [evidence]

> In udanax-green, is the invariant "only CREATELINK writes LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN records" structurally enforced (e.g., by code architecture, access patterns, or module boundaries that make non-CREATELINK writes impossible), or merely a behavioral convention that no current routine violates?

## KB Synthesis

The invariant is **behavioral convention only** — there is no structural enforcement.

The evidence from the KB points consistently to a "convention over enforcement" architecture throughout udanax-green.

**The general mechanism is shared.** `insertspanf()` is a single general function that takes a type-constant parameter to select which sub-index to write into. The DOCISPAN sub-index (type 4) and the link endset sub-indices (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3) are differentiated only by which constant is passed. `insertendsetsinspanf()` is a thin wrapper that calls `insertspanf()` with the link type constants [INT-SPORGL-LINK-INDEX, SS-SPANF-OPERATIONS].

**Callers self-select the type constant.** INSERT/COPY call `insertspanf(..., DOCISPAN)` [FC-CONTENT-SPANF-ISOLATION, Finding 0036]. CREATELINK calls `insertendsetsinspanf()` which uses link type constants [ST-CREATE-LINK, Finding 0012]. Nothing in the function signatures, module boundaries, or access controls prevents any caller from passing link type constants instead.

**The system's pervasive pattern is convention over enforcement.** The subspace invariant (text at 1.x, links at 2.x) is unenforced — `acceptablevsa()` always returns TRUE [PRE-INSERT, PRE-ENF0-PLACEMENT-GAP, SS-SUBSPACE-CONVENTION]. BERT access control is advisory rather than a gate [INT-BERT-FEBE, EC-RESPONSE-BEFORE-CHECK]. The subspace isolation that INSERT and DELETE provide arises from implementation choices (the two-blade knife; the `strongsub` exponent guard), not from any module-level access restriction [FC-SUBSPACE]. This design philosophy runs throughout the codebase.

**Conclusion:** The invariant that only CREATELINK writes LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN records holds because no *current* routine in the codebase calls `insertspanf` with those constants except CREATELINK. There is no type system, module wall, or runtime gate preventing a future or malformed caller from doing so.

---

## Code Exploration

I now have everything I need to give a complete answer.

---

## Answer: Behavioral Convention, Not Structural Enforcement

The invariant is **a behavioral convention only**. No aspect of the code architecture, type system, or module boundaries makes it impossible for non-CREATELINK code to write LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN records.

---

### 1. The constants are bare `#define` integers in a shared header

```c
/* spanfilade span types */
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```
— `xanadu.h:35-39`

These are plain preprocessor constants. They carry no type information. They are indistinguishable from any other `INT` value at compile time. Any translation unit that includes `xanadu.h` has unrestricted access to all four constants.

---

### 2. `insertspanf` is a public, non-static function that accepts any `INT spantype`

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr, typesporglset sporglset, INT spantype)
```
— `spanf1.c:15`

The function is not declared `static`. No `static` declaration exists anywhere in the codebase (the grep for `static.*insertspanf` returned no matches). The `spantype` parameter is a raw `INT` with no typedef, no enum, no guard clause. Inside the function, `spantype` is consumed at line 22:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```
— `spanf1.c:22`

This embeds the `spantype` integer into the ORGL-axis of the spanfilade key, which is how LINKFROMSPAN records are distinguished from DOCISPAN records at retrieval time. The function has no check on what value was passed — it will write whatever type value the caller provides.

---

### 3. The actual write path to LINK*SPAN records

The only current code that passes LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN to `insertspanf` is `insertendsetsinspanf`:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
    typesporglset fromsporglset, typesporglset tosporglset, typesporglset threesporglset)
{  bool insertspanf();
  if (!(
    insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
      &&insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))
        return (FALSE);
  if (threesporglset) {
    if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN)){
        return (FALSE);
     }
  }
  return(TRUE);
}
```
— `do2.c:116-128`

And `insertendsetsinspanf` itself is called from exactly two places, both link-creation operations:

- `domakelink` (2-endpoint link): `do1.c:191`
- `docreatelink` (3-endpoint link): `do1.c:219`

So the call graph is: `docreatelink`/`domakelink` → `insertendsetsinspanf` → `insertspanf(... LINKFROMSPAN/TOSPAN/THREESPAN)`.

---

### 4. Non-link code calls `insertspanf` with a different constant — but nothing prevents it from using LINK*SPAN

Document content writes use the same `insertspanf` function with `DOCISPAN`:

- `do1.c:62` — `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` inside `docopy`
- `do1.c:79` — same pattern in `doinsert`

There is no type-system fence separating "link callers" from "document callers." Both use the same function, and both constants live in the same header. Any code that currently passes `DOCISPAN` could trivially be written (or accidentally modified) to pass `LINKFROMSPAN` instead — the compiler would not object.

---

### 5. The read path also uses the constants, but only as key ranges — not as an access control mechanism

`retrieveendsetsfromspanf` in `spanf1.c:190-235` assigns:

```c
fromspace.stream.mantissa[0] = LINKFROMSPAN;   // spanf1.c:210
tospace.stream.mantissa[0] = LINKTOSPAN;        // spanf1.c:213
threespace.stream.mantissa[0] = LINKTHREESPAN;  // spanf1.c:216
```

These are building `typespan` structs used as range keys passed to `retrievesporglsetinrange` — a read/query operation. This is not a guard; it's a lookup. The read path does not constrain what the write path does.

---

### Conclusion

The invariant is **a behavioral convention**. The current codebase happens to funnel all LINK*SPAN writes through `insertendsetsinspanf`, which is itself only called from link-creation functions. But:

- There is no opaque type wrapping `spantype` that would prevent non-link code from supplying `LINKFROMSPAN`.
- `insertspanf` is a public function with no origin check.
- The constants are unguarded `#define` integers visible to all translation units.
- Nothing in the K&R C module system prevents any function with a `typespanf` pointer from calling `insertspanf(..., LINKFROMSPAN)`.

The invariant holds because no one has violated it, not because the structure prevents violation.
