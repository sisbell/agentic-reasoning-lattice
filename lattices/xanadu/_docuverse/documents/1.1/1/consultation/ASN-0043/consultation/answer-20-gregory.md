## Question 20 [gregory]

> Nelson described links as connecting arbitrary spans across the entire address space — was there a design constraint that both endpoints of a link must reference content that actually exists at link creation time, or can a link be created with endsets pointing to I-addresses that have not yet been allocated (forward references)?

## KB Synthesis

The KB documents the answer through the V-to-I conversion chain at link creation time, not through any explicit "forward reference" test.

**Link creation converts V-spans to I-spans immediately.**

When `domakelink` receives endpoint specsets, it calls `vspanset2sporglset`, which immediately invokes `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` to look up the I-addresses corresponding to those V-spans in the document's current POOM [ST-LINK-CREATE, Finding 0037]. The endset stored in the link orgl is a set of sporgls (I-address ranges), not the original V-spans. The V-spans are transient inputs to link creation; the I-addresses are what get persisted.

This means: **if the V-span doesn't map to anything in the POOM, there are no I-addresses to store.** The I-to-V filtering invariant confirms this: "If an I-address has no POOM mapping, `retrieverestricted` returns NULL and the I-address is silently dropped" [INV-ITOV-FILTERING, Finding 0048]. An endpoint specset pointing at non-existent V-positions would produce an empty sporgl set.

**The I-address space has no reservation or forward-allocation mechanism.**

I-addresses are allocated strictly during INSERT, using a stateless query-and-increment over the granfilade [SS-ADDRESS-SPACE, Finding 0061; INV-MONOTONIC]. There is no mechanism to obtain an I-address before content is placed. The allocation function `next_iaddr(granf) = max_iaddr(granf) + 1` requires content to already exist in the granfilade before the resulting I-address can be referenced [SS-ADDRESS-SPACE, Finding 0077].

**The stated precondition is content existence.**

The combined precondition from the KB is: "source content exists AND target content exists AND both endpoint widths >= 1 AND home_doc is valid" [PRE-LINK-CREATE, Finding 0028]. The zero-width crash (Bug 0017) documents that the backend does enforce at least the width check, and a zero-width endpoint is semantically equivalent to an endset pointing at nothing [PRE-ZERO-WIDTH].

**The short answer:** No forward references. Link creation is a pure V→I lookup at call time. If content doesn't exist in the POOM at that moment, the endset is empty or the operation misbehaves. The system has no "create link now, bind it to content later" mechanism — I-addresses only exist after INSERT, and that's what links actually store.

---

## Code Exploration

I now have a complete picture of the full execution path. Here is my answer:

---

## Link Creation and Forward References in udanax-green

### Short Answer

There is no hard code-level constraint requiring endset content to exist at link creation time — but the *behavior* differs depending on how endsets are specified, and one practical constraint does exist: **if endsets are given as V-specs, the referenced document must exist in the granfilade**. Content at specific V-addresses does not need to exist.

---

### Execution Path

**`fns.c:100-112`** — Top-level handler:
```c
void createlink(typetask *taskptr) {
    if (getcreatelink(taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
    && docreatelink(taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa))
        putcreatelink(taskptr, &linkisa);
    else
        putrequestfailed(taskptr);
}
```

**`get2fe.c:147-180`** — Wire protocol parsing in `getspecset()`:

Each item in a specset is prefixed on the wire with either `'s'` (SPANFLAG) or `'v'` (VSPECFLAG):
```c
if (c == SPANFLAG) {
    specset = (typespecset)taskalloc(taskptr, sizeof(typespan));
    if (!getspan(taskptr, specset, ISPANID))   // raw I-span
        return(FALSE);
} else {
    specset = (typespecset)taskalloc(taskptr, sizeof(typevspec));
    if (!getvspec(taskptr, specset))            // V-spec (docisa + vspans)
        return(FALSE);
}
```

**Both wire formats are accepted.** FEBE clients can send either raw I-spans (`ISPANID`) or V-specs (`VSPECID`) as endsets. The Python client exclusively uses V-specs (via `SpecSet(VSpec(...))`), but the protocol is not restricted to them.

---

**`do1.c:207-220`** — Core of `docreatelink()`:
```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
return (
     createorglingranf(taskptr, granf, &hint, linkisaptr)   // allocate link ISA
  && tumbler2spanset(taskptr, linkisaptr, &ispanset)
  && findnextlinkvsa(taskptr, docisaptr, &linkvsa)
  && docopy(taskptr, docisaptr, &linkvsa, ispanset)
  && findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
  && specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)  // line 214
  && specset2sporglset(taskptr, tospecset, &tosporglset, NOBERTREQUIRED)      // line 215
  && specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)// line 216
  && setlinkvsas(&fromvsa, &tovsa, &threevsa)
  && insertendsetsinorgl(taskptr, linkisaptr, link, ...)
  && insertendsetsinspanf(taskptr, spanf, linkisaptr, ...)
);
```

All three endset conversions pass `NOBERTREQUIRED`. From `bert.c:52-61`:
```c
int checkforopen(tumbler *tp, int type, int connection) {
    if (type == NOBERTREQUIRED) {
        return 1;   /* Random > 0 — always passes */
    }
    ...
```
**No document needs to be open** for the endset lookup.

---

### Case 1: Raw I-span Endsets (`ISPANID`)

In `sporgl.c:19-22`:
```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *sporglsetptr = (typesporglset)specset;
    sporglsetptr = (typesporglset *)&((typeitemheader *)specset)->next;
}
```

The I-span is accepted and threaded into the sporglset **with no existence check of any kind**. There is no call to `findorgl`, no permascroll lookup, no validation that the tumbler addresses correspond to actual allocated content. A client sending `s\n<any_tumbler>~<any_width>~` as an endset will have it stored verbatim in the link's orgl and spanfilade.

**Conclusion: Raw I-span endsets admit true forward references to unallocated I-addresses.**

---

### Case 2: V-spec Endsets, Non-Existent Document (`VSPECID`, bad docisa)

In `sporgl.c:44-46`:
```c
if (!findorgl(taskptr, granf, docisa, &orgl, type)) {
    return(NULL);
}
```

`findorgl` (`granf1.c:17-41`) calls `fetchorglgr` to locate the document's node in the granfilade. If the document doesn't exist, `fetchorglgr` returns NULL, `findorgl` returns FALSE, `vspanset2sporglset` returns NULL, `specset2sporglset` returns FALSE, and `docreatelink` fails.

**Conclusion: If endsets are specified as V-specs, the referenced document must exist in the granfilade.** This is the only hard constraint uncovered in the code.

---

### Case 3: V-spec Endsets, Document Exists but V-Addresses Have No Content

`vspanset2sporglset` (`sporgl.c:47-58`) calls `vspanset2ispanset` to translate V-coordinates to I-coordinates:
```c
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
        // build sporgl entries
    }
}
```

`vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` queries the POOM enfilade for content at those V-coordinates. **If nothing has been written there, `retrieverestricted` returns NULL** and `ispanset` is never set. The inner loop body never executes. No sporgl entries are created for that endset. The function returns `sporglsetptr` (not NULL), so `specset2sporglset` returns TRUE.

`docreatelink` completes and succeeds, creating a link with an empty (dangling) endset.

**Conclusion: If a V-spec endset points to V-addresses with no content, the link is created with an empty endset. No failure, no error.**

---

### Critical Architectural Point: V-to-I Translation at Creation Time

The endsets are stored as **sporgls** — `(docisa, I-origin, I-width)` triples — not as V-specs. The translation from V-coordinates to I-addresses happens **at link creation time**, inside `vspanset2sporglset`. The link structure stores resolved I-coordinates, not the original V-spec.

This has a sharp implication for the "forward reference" question with V-specs: if you create a link pointing at a V-address before content is written there, the endset is stored empty. When content is later written to that V-address, following the link still returns nothing — the link was created with an empty endset and that emptiness is permanent.

Raw I-span endsets bypass this entirely: the I-address is stored directly, with no V-to-I translation and no validation. Whether that I-address will ever have content allocated to it is the client's concern, not the backend's.

---

### Summary Table

| Endset type | Document must exist? | Content must exist at V-addresses? | Forward reference to unallocated I-addr? |
|---|---|---|---|
| Raw I-span (`ISPANID`) | N/A | N/A | **Yes — no check at all** |
| V-spec (`VSPECID`) | **Yes** (`findorgl` fails otherwise) | No (empty endset stored) | Moot — V→I resolved at creation time |

**The design does not enforce that both endpoints reference existing content at link creation time.** Nelson's model of links as address-space entities is implemented permissively: a link can be created with endsets pointing to anything the client sends, including I-addresses never yet allocated. When endsets are given as V-specs, the document boundary is enforced but not the content boundary — a V-address with no content silently produces a null endset rather than a rejected request.
