## Question 17 [evidence]

> Does endset resolution require the target document to be opened with BERT access, or can endsets be resolved against a closed document's persisted POOM via direct enfilade query?

## KB Synthesis

## Endset Resolution and Document Open State

Endset resolution in FOLLOWLINK does **not** require the target document to be opened via BERT access.

### The distinction is architectural, not incidental

The open-document requirement is a gate implemented specifically in `findorgl()`, which checks whether a document orgl is in the per-session open list. This gate sits in the `specset2ispanset` path used by `retrieve_contents` — not in the `retrieverestricted()` path used by FOLLOWLINK's I-to-V conversion. [SS-DOCUMENT-LIFECYCLE]

### FOLLOWLINK's internal code path

FOLLOWLINK's endset resolution uses: `link2sporglset()` → `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()`. This is a direct enfilade tree query that bypasses `findorgl` entirely. When an I-address has no POOM mapping, it is silently dropped rather than triggering a "not open" error. [SS-FOLLOWLINK]

### Behavioral evidence

The three-phase lifecycle is explicit in the KB:

1. `find_links` — span-f I-address lookup, no open-doc requirement
2. `follow_link` — reads link orgl, resolves via `retrieverestricted()`, **no open-doc requirement**
3. `retrieve_contents` — calls `findorgl()`, **requires document open**

The concrete example from [INT-LINK-FOLLOW-LIFECYCLE] confirms this: `follow_link(link_id, LINK_SOURCE)` succeeds and returns a SpecSet referencing doc_A even when doc_A is not open; only the subsequent `retrieve_contents(specset_referencing_A)` fails.

### Summary

Endset resolution (FOLLOWLINK's I→V conversion) queries the homedoc's POOM directly via `retrieverestricted()`. BERT open-list checking is confined to `findorgl()`, which is only in the `retrieve_contents` path. The answer to the question: no BERT/open requirement for endset resolution; yes for the downstream content retrieval step. [PRE-FOLLOWLINK], [PRE-RETRIEVE-CONTENTS]

---

## Code Exploration

All line numbers confirmed. Here is the full answer.

---

## Endset Resolution and BERT Access: Full Analysis

**Answer: Endset resolution does NOT require BERT access. It operates directly against the persisted POOM via enfilade query on both the link document and the target document, whether or not either is open.**

---

### The Call Chain

The FEBE `followlink` handler in `fns.c:114-127`:

```c
void followlink(typetask *taskptr)
{
    getfollowlink(taskptr, &linkisa, &whichend)
    && dofollowlink(taskptr, &linkisa, &specset, whichend)
    → putfollowlink(taskptr, specset);
}
```

This drops into `dofollowlink()`:

**`do1.c:223-232`** — the definitive statement:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  bool link2sporglset(), linksporglset2specset();

	return (
	   link2sporglset (taskptr, linkisaptr, &sporglset, whichend,NOBERTREQUIRED)
	&& linksporglset2specset (taskptr,&((typesporgl *)sporglset)->sporgladdress, sporglset, specsetptr,/* ECH 6-29 READBERT */NOBERTREQUIRED));
}
```

Both calls pass `NOBERTREQUIRED`. The inline comment `/* ECH 6-29 READBERT */` at `do1.c:230` is historically significant: this was once `READBERT` and was deliberately changed to `NOBERTREQUIRED`. The old value is preserved in the comment.

---

### The BERT Gateway: `findorgl()`

Every access to a document's granfilade entry (its POOM root) routes through `findorgl()`.

**`granf1.c:17-41`**:

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)/*BERT*/
{
  typeorgl fetchorglgr();
  int temp;

	if (/*backenddaemon &&*/(temp = checkforopen(isaptr, type, user)) <= 0) {
		if (!isxumain) {
			return FALSE;
		}
	}
	*orglptr = fetchorglgr(taskptr, granfptr, isaptr);   // line 39
	return (*orglptr ? TRUE : FALSE);
}
```

The guard is `temp <= 0`. The value of `temp` is whatever `checkforopen()` returns.

---

### The BERT Bypass: `checkforopen()`

**`bert.c:52-61`**:

```c
int checkforopen(tumbler *tp, int type, int connection)
{
  conscell *p;
  bertentry *bert;
  int foundnonread = FALSE;

  if (type == NOBERTREQUIRED) {
    return 1;	/* Random > 0 */
  }
  // ... BERT table lookup for READBERT / WRITEBERT ...
```

When `type == NOBERTREQUIRED`, `checkforopen()` returns `1` immediately — no table lookup, no connection check, no ownership check. Back in `findorgl()`, `temp = 1 > 0`, so the guard does not fire. `fetchorglgr()` proceeds unconditionally at `granf1.c:39`.

---

### Endset Extraction: `link2sporglset()` and `sporglset2vspanset()`

**`sporgl.c:67-95`** — `link2sporglset()` extracts the raw endset pointers from the link's POOM:

```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa, typesporglset *sporglsetptr, INT whichend, int type)
{
    if (!findorgl(taskptr, granf, linkisa, &orgl, type))   // line 77: NOBERTREQUIRED
        return FALSE;
    // ... construct vspan for whichend ...
    if (context = retrieverestricted((typecuc*)orgl, &vspan, V, NULL, I, NULL))  // line 83: direct enfilade query
    {
        for (c = context; c; c = c->nextcontext) {
            // ... build sporglset from returned context ...
        }
        return TRUE;
    }
}
```

`retrieverestricted()` at `sporgl.c:83` is a pure enfilade traversal — no BERT involved at any level. It calls `retrieveinarea()` → `findcbcinarea2d()`, which walks the POOM tree. None of those functions contain BERT checks.

**`sporgl.c:141-176`** — `sporglset2vspanset()` resolves I-coordinates back to V-spans on the *target* document:

```c
int sporglset2vspanset(typetask *taskptr, typeisa *homedoc, typesporglset *sporglsetptr, typevspanset *vspansetptr, int type)
{
    (void) findorgl(taskptr, granf, homedoc, &orgl, type);   // line 152: NOBERTREQUIRED on target doc
    // ...
    vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);   // line 157: V↔I conversion
}
```

The target document's POOM is fetched with `NOBERTREQUIRED`. The document addressed by the endset need not be open.

---

### Contrast: Operations That DO Require BERT

Every operation that modifies a document calls `findorgl()` with `WRITEBERT`. Every explicit read call uses `READBERT`:

| Operation | File:Line | BERT Type |
|-----------|-----------|-----------|
| `dorearrange()` | `do1.c:40` | `WRITEBERT` |
| `docopy()` | `do1.c:55` | `WRITEBERT` |
| `dodeletevspan()` | (do1.c) | `WRITEBERT` |
| `doretrievedocvspan()` | `do1.c:318` | `READBERT` |
| **`dofollowlink()`** | **`do1.c:229-230`** | **`NOBERTREQUIRED`** |

There is one outlier: `doretrievedocvspanfoo()` at `do1.c:301-308` also uses `NOBERTREQUIRED`, but its own comment calls it "a kluge not yet kluged" — it is an incomplete internal variant, not a production code path.

---

### Architectural Conclusion

The `NOBERTREQUIRED` bypass in `dofollowlink()` is a deliberate design decision, evidenced by the preserved `/* ECH 6-29 READBERT */` comment showing a conscious rollback from a stricter requirement. The architecture separates two concerns:

1. **BERT** controls *exclusive access* — it gates operations that mutate document state, preventing concurrent modification. A document must be open (checked out) to be written or explicitly read via the FEBE interface.

2. **Enfilade traversal** is *structurally read-only* — the POOM nodes are persistent data structures. Following a link reads the link's POOM to find endset I-coordinates, then reads the target document's POOM to convert those to V-spans. Neither operation modifies any data structure, so no lock is needed.

Endset resolution can therefore succeed against any document whose granfilade entry (`typeorgl`) is present in the granfilade — even if that document has never been opened in the current session. The only failure mode is if `fetchorglgr()` at `granf1.c:39` returns `NULL`, meaning the document has no entry in the granfilade at all (i.e., it does not exist), not that it is merely closed.
