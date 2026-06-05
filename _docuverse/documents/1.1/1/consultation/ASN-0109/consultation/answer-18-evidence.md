## Question 18 [evidence]

> Does reading endsets require the link's home document to be open under BERT, or can endsets be read by link address without an open-document precondition?

## KB Synthesis

## Reading Endsets: Open-Document Requirement

**FOLLOWLINK does not require the link's home document to be open under BERT.**

The operation proceeds in two phases with distinct requirements:

**Phase 1 — Endset I-address extraction** (`link2sporglset`): Reads the link orgl directly by I-address via `retrieverestricted()`. No `findorgl` BERT check against the home document occurs at this stage. The only precondition is that the link ISA itself exists in the granfilade. [PRE-FOLLOWLINK], [SS-FOLLOWLINK]

**Phase 2 — I-to-V conversion** (`linksporglset2specset`): Looks up the endset I-addresses in the specified `homedoc`'s POOM. If an I-address has no POOM mapping, it is silently dropped — no error is raised. [SS-FOLLOWLINK]

This matches the general architectural rule: operations working through I-address lookup bypass the open-document requirement, while operations resolving V→I mappings within a document orgl require it to be open. [SS-DOCUMENT-LIFECYCLE], [INT-LINK-FOLLOW-LIFECYCLE]

**Consequence:** `follow_link(link_id, endpoint)` returns a SpecSet without requiring the home document open. The open-document precondition only kicks in at the *next* step — `retrieve_contents` on the returned SpecSet — because that call goes through `findorgl` with BERT enforcement. [INT-LINK-FOLLOW-LIFECYCLE]

**RETRIEVEENDSETS** is similar: it searches the spanfilade by I-address (no document-open requirement for the link side), but the input specset conversion from V-spans does require the querying document to be open. [SS-RETRIEVEENDSETS]

---

## Code Exploration

I now have all the information needed. Let me compile the complete answer.

---

## Answer: Endset Reading Requires No Open-Document Precondition

**Both `followlink` and `retrieveendsets` pass `NOBERTREQUIRED` throughout every call in their chain. No open-document check is ever enforced for reading endsets.**

---

### The BERT bypass mechanism

`checkforopen` in `bert.c:59-61` is the sole gate:

```c
int checkforopen(tumbler *tp, int type, int connection)
{
  if (type == NOBERTREQUIRED) {
    return 1;    /* Random > 0 */
  }
  // ... BERT table lookups follow ...
}
```

Returning `> 0` signals success. Passing `NOBERTREQUIRED` short-circuits everything.

`findorgl` in `granf1.c:22` calls this gate:

```c
if (/*backenddaemon &&*/(temp = checkforopen(isaptr, type, user)) <= 0) {
    // fail / return FALSE
}
```

So `findorgl(..., NOBERTREQUIRED)` always proceeds, regardless of BERT state.

---

### Call chain for `followlink`

`fns.c:122` → `dofollowlink` (`do1.c:223`):

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr,&((typesporgl *)sporglset)->sporgladdress, sporglset, specsetptr,
                              /* ECH 6-29 READBERT */ NOBERTREQUIRED));
}
```

`do1.c:229-230`

The comment `/* ECH 6-29 READBERT */` is a preserved artifact: this was **explicitly changed from `READBERT` to `NOBERTREQUIRED`** — a deliberate design decision to remove the precondition.

`link2sporglset` at `sporgl.c:77` passes `type` straight to `findorgl`:

```c
if (!findorgl (taskptr, granf, linkisa, &orgl, type)) {
    return (FALSE);
}
```

`linksporglset2specset` at `sporgl.c:116` dispatches to `linksporglset2vspec`, which calls `sporglset2vspanset` at `sporgl.c:152`:

```c
(void) findorgl (taskptr, granf, homedoc/*&sporglptr->sporgladdress*/, &orgl, type);
```

All with `type = NOBERTREQUIRED`.

---

### Call chain for `retrieveendsets`

`fns.c:356` → `doretrieveendsets` (`do1.c:369`):

```c
bool doretrieveendsets(typetask *taskptr, typespecset specset, typespecset *fromsetptr, typespecset *tosetptr, typespecset *threesetptr)
{
    return retrieveendsetsfromspanf(taskptr, specset, fromsetptr, tosetptr, threesetptr);
}
```

`retrieveendsetsfromspanf` at `spanf1.c:190` passes `NOBERTREQUIRED` to every downstream call:

```c
if (!(specset2sporglset (taskptr, specset, &sporglset, NOBERTREQUIRED)          // spanf1.c:222
    && ...
    && linksporglset2specset (taskptr, &...->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)  // spanf1.c:224
    && ...
    && linksporglset2specset (taskptr, &...->docisa, tosporglset,   tosetptr,   NOBERTREQUIRED)  // spanf1.c:226
```

And the three-endset path at `spanf1.c:231`:

```c
&& linksporglset2specset(taskptr, &...->docisa, threesporglset, threesetptr, NOBERTREQUIRED)
```

`specset2sporglset` at `sporgl.c:14` chains to `vspanset2sporglset` at `sporgl.c:44`, which calls:

```c
if (!findorgl (taskptr, granf, docisa, &orgl, type)) {
    return (NULL);
}
```

Again `type = NOBERTREQUIRED`.

---

### Contrast with operations that *do* require BERT

For comparison, operations that read document *content* all use `READBERT`:

| Operation | File:Line | BERT type |
|---|---|---|
| `doretrievedocvspan` | `do1.c:318` | `READBERT` |
| `doretrievedocvspanset` | `do1.c:327` | `READBERT` |
| `doretrievev` | `do1.c:344` | `READBERT` |
| `specset2ispanset` (content retrieval) | `do2.c:35` | `READBERT` (passed from `doretrievev`) |

---

### Conclusion

**Endset reading requires no open-document precondition.** Both `followlink` (`do1.c:229-230`) and `retrieveendsets` (`spanf1.c:222-231`) pass `NOBERTREQUIRED` to every `findorgl` invocation in their call chains. `checkforopen` (`bert.c:59-61`) bypasses all BERT table lookups when it receives `NOBERTREQUIRED`, returning unconditional success. A link's endsets can be read by link address alone — no prior `open` call on the link's home document is required. The comment `/* ECH 6-29 READBERT */NOBERTREQUIRED` at `do1.c:230` confirms this was an explicit architectural choice to remove the home-document open precondition from link traversal.
