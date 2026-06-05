## Question 12 [evidence]

> Must the caller supply a V-address (requiring the document to be open and in their BERT list per PRE-DOCUMENT-OPEN), or can content be read directly by I-address without the document being open?

## KB Synthesis

Two distinct access paths exist, with fundamentally different open-document requirements:

## Path 1: V-address → content (requires document open)

`retrieve_contents` always requires the target document to be open. The call chain is:

`doretrievev` → `specset2ispanset` → `findorgl(doc, READBERT)` → I-addresses → `ispanset2vstuffset` → bytes

`findorgl` checks the backend's open-document list. If the document is not open, it returns FALSE and the operation fails immediately with an error. [PRE-RETRIEVE-CONTENTS], [SS-DOCUMENT-LIFECYCLE]

There is no caller-accessible operation that accepts raw I-addresses as input to retrieve bytes — the public API entry point is always a VSpec (document + V-position + width), which mandates POOM lookup and therefore requires the document to be open.

## Path 2: I-address index operations (document open NOT required)

Operations that work exclusively through the spanf enfilade bypass `findorgl` entirely:

- **`find_links`**: converts the query VSpec to I-addresses, then searches the spanf. The *referenced* document need not be open. [SS-DUAL-ENFILADE], [SS-FIND-LINKS]
- **`retrieve_endsets`**: same mechanism — spanf search by I-address range. [SS-RETRIEVE-ENDSETS]
- **`follow_link`**: reads the link orgl directly (no POOM check), returning a SpecSet as a *deferred reference*. The target document is not consulted. [SS-FOLLOWLINK]

However, resolving that deferred SpecSet via `retrieve_contents` then falls back to Path 1 and requires the referenced document to be open. [INT-LINK-FOLLOW-LIFECYCLE]

## Summary

| Operation | Open document required? | Mechanism |
|-----------|------------------------|-----------|
| `retrieve_contents` | **Yes** — fails if closed | findorgl → POOM → permascroll |
| `find_links` | No | spanf I-address index only |
| `retrieve_endsets` | No | spanf I-address index only |
| `follow_link` | No (deferred reference) | link orgl direct; POOM consulted only at resolution |

The architectural reason: the granf/POOM path (content retrieval) is gated by `findorgl`'s open-list check; the spanf path (link discovery) never calls `findorgl`. [SS-DUAL-ENFILADE, FC-CONTENT-SPANF-ISOLATION]

---

## Code Exploration

I now have everything I need from the source. Here is my complete answer.

---

## Answer: V-address vs. I-address — Does retrieval require the document to be open?

**Short answer:** I-address retrieval bypasses BERT entirely. V-address retrieval requires the document to be open in the caller's BERT list.

---

### The retrieval entry point

`retrievev()` [`fns.c:175`] is the sole content-retrieval handler. It delegates immediately:

```c
void retrievev(typetask *taskptr)
{
  typespecset specset;
  typevstuffset vstuffset;
    if (
       getretrievev (taskptr, &specset)
    && doretrievev (taskptr, specset, &vstuffset))
        putretrievev (taskptr, &vstuffset);
```

`doretrievev()` [`do1.c:338`]:

```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr)
{
    return
       specset2ispanset (taskptr, specset, &ispanset, READBERT)
    && ispanset2vstuffset (taskptr, granf, ispanset, vstuffsetptr);
}
```

The type parameter `READBERT` is passed to `specset2ispanset`. That function is where the divergence happens.

---

### The fork: `specset2ispanset` [`do2.c:14`]

The specset is a heterogeneous list. Each item is either an `ISPANID` (I-address span) or a `VSPECID` (V-address + document ISA). The function handles them differently:

**ISPANID path [`do2.c:24–26`] — no access check:**
```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *ispansetptr = (typeispanset)specset;
    ispansetptr = (typeispanset *)&((typeitemheader *)specset)->next;
}
```
The I-span is spliced directly into the output `ispanset`. There is no call to `findorgl()`, no call to `checkforopen()`. The document does not need to be open or even known.

**VSPECID path [`do2.c:27–38`] — document open required:**
```c
} else if (((typeitemheader *)specset)->itemid == VSPECID) {
    if (iszerotumbler (&((typevspec *)specset)->docisa))
        qerror ("retrieve called with docisa 0\n");
    if (!(
      findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)/*BERT*/
    && (ispansetptr = vspanset2ispanset (taskptr, docorgl, ...)))){
         return (FALSE);
    }
}
```
`findorgl()` is called with the document ISA and `type=READBERT`.

---

### `findorgl` enforces the BERT gate [`granf1.c:17`]

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
  int temp;
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        if (!isxumain) {
            return FALSE;
        }
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

The condition is `<= 0` — both zero and negative return values from `checkforopen` cause failure.

---

### `checkforopen` return values [`bert.c:52`]

The comment header documents the semantics precisely:

```
Open state -->
type            Not Open        Open READ       Open WRITE
  |         !owned | owned   conn== |conn!=  conn== |conn!=
  v         -------+-------  ------+------  ------+------
READ           0   |   0     READ  |   0    WRITE | -1
WRITE         -1   |   0      -1   |  -1    WRITE | -1
```

For `type == READBERT`:
- Document **not in BERT table** → returns `0` (neither owned nor write-locked case)
- Document open READ by **same connection** → returns `READBERT` (> 0, allowed)
- Document open READ by **different connection** → returns `0` (blocked in `findorgl`)
- Document open WRITE by **same connection** → returns `WRITEBERT` (> 0, allowed)
- Document open WRITE by **different connection** → returns `-1` (denied)

Both `0` and `-1` cause `findorgl` to return `FALSE`. Therefore: **any V-address retrieval requires the caller to have the document open in their BERT list** — a read-open by the same connection is sufficient.

The `NOBERTREQUIRED` fast path [`bert.c:59–61`] bypasses this:
```c
if (type == NOBERTREQUIRED) {
    return 1;    /* Random > 0 */
}
```
But `doretrievev` always passes `READBERT`, never `NOBERTREQUIRED`. The `NOBERTREQUIRED` value appears in `dofinddocscontaining` [`do1.c:21`], `docopy` [`do1.c:54`], and the link operations [`do1.c:187–230`], but not in the content-retrieval path.

---

### Summary

| Input type | Access check | Document must be open? |
|---|---|---|
| `ISPANID` (I-address) | None | **No** |
| `VSPECID` (V-address + doc ISA) | `findorgl` → `checkforopen(READBERT)` | **Yes — read or write open required** |

A caller who knows the I-address of content can supply it as an `ISPANID` in the specset and retrieve that content without any document open in their BERT list. The BERT/PRE-DOCUMENT-OPEN precondition is only enforced when the specset contains `VSPECID` items. The V→I translation (`vspanset2ispanset`) is the gated operation; once content is addressed by I-address, it is freely readable.
