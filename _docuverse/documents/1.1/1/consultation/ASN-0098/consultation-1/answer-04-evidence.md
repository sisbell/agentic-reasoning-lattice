## Question 4 [evidence]

> Does udanax-green's link allocation (the K.λ analogue) verify that each address referenced by an endset is already present in the content store, or does it accept endsets that name unallocated addresses?

## KB Synthesis

## Link Allocation and Endset Validation

Link creation does **not** perform an explicit check against the granfilade (content store). Validation is indirect and silent.

### The Creation Path

`domakelink` takes V-spans as input, not raw I-addresses [ST-LINK-CREATE, Finding 0037]. The validation that occurs is implicit in the V→I conversion chain:

```
V-span → vspanset2sporglset → vspanset2ispanset
       → permute → span2spanset → retrieverestricted (POOM lookup)
```

`retrieverestricted` searches the document's POOM for context entries. If a V-position has no POOM mapping, it **silently drops** the address — no error, no V-span added to the result [SS-FOLLOWLINK, Finding 0048]. This means a V-span referencing non-existent positions produces an empty sporglset, and the link is created with an empty endset.

### What Is Guaranteed

Because the POOM can only reference I-addresses that were previously allocated by the granfilade (granfilade is append-only, INV-IADDR-IMMUTABILITY [INV-IADDR-IMMUTABILITY]), any I-address successfully retrieved through the POOM is necessarily present in the content store. The POOM lookup is the implicit membership test.

### What Is Not Guaranteed

- No error is raised if the V-span resolves to nothing at creation time — the link simply gets a partial or empty endset [EC-GHOST-LINK]
- The system accepts zero-width endpoint specsets without validation; zero-width **crashes** only [PRE-LINK-CREATE, Finding 0028]  
- `specset2sporglset` validates only that the referenced **document exists**, not that element-level addresses are well-formed [PRE-SPECSET]

### Post-Creation Staleness

Ghost links arise *after* creation when content is deleted. At creation time the POOM lookup implicitly confirms content presence; afterward, no mechanism removes or invalidates the stored I-addresses [EC-GHOST-LINK, INV-SPANF-WRITE-ONLY]. So the system accepts "today's content" as the endset, but makes no forward commitment that it will remain resolvable.

**Summary:** The system never accepts raw I-addresses that name unallocated locations — the V→POOM→I path makes that structurally impossible. But it accepts V-spans that map to nothing and silently produces empty endsets rather than rejecting the call.

---

## Code Exploration

I now have the complete picture. Let me compile the full answer with precise citations.

---

## Does udanax-green's link allocation verify endset addresses against the content store?

**Short answer: Partially.** Link creation verifies that the *document* named by each endset exists in the granfilade, but does **not** verify that the *specific virtual spans* within that document have content mapped to them. A link naming non-existent virtual addresses within a real document is silently stored with an empty internal-span set, with no error.

---

### The call chain

**Entry point — `fns.c:100`**

```c
void createlink(typetask *taskptr)
{
    if (getcreatelink(taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
     && docreatelink(taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa))
        putcreatelink(taskptr, &linkisa);
    else
        putrequestfailed(taskptr);
}
```

**`do1.c:195` — `docreatelink`**

```c
bool docreatelink(...)
{
    ...
    return (
         createorglingranf(taskptr, granf, &hint, linkisaptr)
      && tumbler2spanset(taskptr, linkisaptr, &ispanset)
      && findnextlinkvsa(taskptr, docisaptr, &linkvsa)
      && docopy(taskptr, docisaptr, &linkvsa, ispanset)
      && findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
      && specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)   // line 214
      && specset2sporglset(taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)   // line 215
      && specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED) // line 216
      ...
    );
}
```

The `NOBERTREQUIRED` flag is passed to all three endset conversions. This matters.

---

### Gate 1 — BERT access check: **bypassed**

`findorgl` (`granf1.c:17`) calls `checkforopen` before doing the actual lookup:

```c
// granf1.c:22
if ((temp = checkforopen(isaptr, type, user)) <= 0) {
    ...
    return FALSE;
}
```

But in `bert.c:59`:

```c
int checkforopen(tumbler *tp, int type, int connection)
{
    if (type == NOBERTREQUIRED) {
        return 1;   /* Random > 0 */    // bert.c:60
    }
    ...
```

`NOBERTREQUIRED` short-circuits immediately — the document does **not** need to be opened/checked-out by the calling user. This means any document address can be referenced in an endset regardless of whether the current user has it open, which is a broader permission than what BERT would normally enforce.

---

### Gate 2 — Document existence: **enforced**

After the BERT bypass, `findorgl` still calls `fetchorglgr` (`granf1.c:39`):

```c
*orglptr = fetchorglgr(taskptr, granfptr, isaptr);
return (*orglptr ? TRUE : FALSE);
```

`fetchorglgr` (`granf2.c:22`) performs a real lookup in the granfilade tree:

```c
// granf2.c:31-40
if (tumblercmp(&((typecuc*)fullcrumptr)->cwid.dsas[WIDTH], address) == LESS)
    return (NULL);   // address beyond tree bounds

if ((context = retrievecrums((typecuc*)fullcrumptr, address, WIDTH)) == NULL)
    return NULL;     // not found in tree

if (!tumblereq((tumbler*)&context->totaloffset, address)) {
    crumcontextfree(context);
    return (NULL);   // found a node, but it doesn't match this address exactly
}
```

Three distinct failure modes — all return NULL. If the document ISA named in an endset is not in the granfilade, `fetchorglgr` returns NULL, `findorgl` returns FALSE, `vspanset2sporglset` returns NULL (`sporgl.c:44-46`), `specset2sporglset` returns FALSE (`sporgl.c:25-27`), and `docreatelink` returns FALSE, aborting the link. This is real enforcement.

---

### Gate 3 — Specific virtual spans within the document: **not enforced**

Once `findorgl` succeeds and an `orgl` handle is obtained, `vspanset2sporglset` (`sporgl.c:47`) converts each requested vspan to ispans:

```c
// sporgl.c:47-58
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
        sporglset = (typesporgl *) taskalloc(taskptr, sizeof(typesporgl));
        ...
        *sporglsetptr = (typesporglset)sporglset;
    }
}
return (sporglsetptr);
```

`vspanset2ispanset` (`orglinks.c:397`) delegates to `permute` → `span2spanset` → `retrieverestricted`. If the virtual addresses requested have no content mapped in the POOM enfilade, `retrieverestricted` returns NULL context. `span2spanset` handles this at `orglinks.c:446`:

```c
if (!context) {
    return (targspansetptr);   // silent empty return — no error
}
```

The result: if an endset names V-spans `[5, 3)` in a document that only has content in `[1, 2)`, the conversion yields an empty ispanset. The sporgl-building loop body at `sporgl.c:49` never executes. `vspanset2sporglset` returns a valid (but unchanged) `sporglsetptr`. `specset2sporglset` returns TRUE. The link is created and stored referencing those non-existent spans — silently, with no error.

---

### Summary

| What is checked | Verdict |
|---|---|
| Document ISA exists in the granfilade | **Yes — hard failure if missing** (`fetchorglgr` → NULL → link aborted) |
| Document is open/checked-out by user | **No — bypassed** (`NOBERTREQUIRED` in `bert.c:59` returns 1 unconditionally) |
| Virtual spans within document have content | **No — silent empty sporglset** (`span2spanset` returns quietly when `retrieverestricted` finds nothing, `orglinks.c:446`) |

Udanax-green's link allocation is therefore not a full K.λ-style integrity check. It enforces document-container existence but does not enforce span-level referential integrity. A link can be created that names virtual addresses with no backing content, and the system will store it without complaint — the endset simply maps to an empty internal-span set when later followed.
