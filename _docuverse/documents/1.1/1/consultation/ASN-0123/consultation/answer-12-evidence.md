## Question 12 [evidence]

> When the versioning user does not own the source document and `makehint` redirects allocation under the user's own account, is the source's identity encoded anywhere in the new version's tumbler address, or is the ancestry relationship then recoverable only through shared I-addresses?

## KB Synthesis

When a non-owner creates a version, the ancestry relationship is **not encoded in the tumbler address** — it is recoverable only through shared I-addresses.

## Address allocation for non-owner version

From [SS-VERSION-ADDRESS] / [ST-VERSION-OWNERSHIP] Finding 0068: when the ownership check `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)` fails, `makehint` uses `ACCOUNT, DOCUMENT, depth=2`, placing the version under the creating user's account — identical to how `CREATEDOCUMENT` behaves.

Concrete example from the KB:
```
Source (User A): 1.1.0.1.0.1
Non-owner version (User B, account 1.1.0.2): 1.1.0.2.0.1
```

The version's address is `user_account.0.N`. There is no prefix relationship to the source: truncating `1.1.0.2.0.1` to the length of `1.1.0.1.0.1` gives `1.1.0.2.0.1` ≠ `1.1.0.1.0.1`, so [SS-TUMBLER-CONTAINMENT]'s containment predicate returns false. The address is structurally indistinguishable from a freshly created document.

**Contrast with owned version**: owned versions land at `source_doc.N` (child address), so the lineage is directly readable from the tumbler prefix hierarchy. That signal is completely absent in the cross-user case.

## Ancestry is recoverable only through shared I-addresses

The I-address sharing mechanism is unaffected by ownership. From [ST-VERSION-CREATE] Findings 0043 and 0046: `docreatenewversion` always calls `docopyinternal` to copy the text subspace I-addresses to the new version, regardless of which account the version lands under. The version inherits all permascroll I-addresses from the source at creation time.

This means:

- `compare_versions(source, non_owner_version)` returns the full shared span — the same result you'd get from an owned version — because the I-address sets are identical at creation. [SS-COMPARE-VERSIONS]
- `FINDDOCSCONTAINING` queries return both the source and the non-owner version for any I-address that was in the source at version-creation time. [INV-IADDRESS-PERMANENT]
- [INV-TRANSITIVE-IDENTITY] holds: content identity flows through versioning regardless of ownership path.

## What is lost without the address encoding

The address hierarchy provides a structural shortcut for version-chain traversal — you can enumerate all versions of document D by finding all addresses with D as a prefix, without reading content. For non-owner versions that shortcut is gone. To discover that `1.1.0.2.0.1` is a version of `1.1.0.1.0.1`, you must perform an I-address-level query (`compare_versions` or `FINDDOCSCONTAINING`), which requires actually reading content identity rather than just traversing the address tree.

There is no metadata field, no link, and no back-pointer stored at creation time that records the source document's address. The only durable trace of the ancestry relationship is the shared I-address content in the granfilade.

---

## Code Exploration

I now have the full picture. Here is the complete answer.

---

## Answer: Source Identity in Cross-Ownership Versioning

### The Branch That Governs Everything

`docreatenewversion` (`do1.c:260–298`) contains the decisive guard at line 270:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
} else {
    /* This does the right thing for new version of someone else's document, as it
       duplicates the behavior of docreatenewdocument */
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

When the versioning user does not own the source, the `else` branch fires. `makehint` at `do2.c:78–84` merely copies its arguments into the hint struct:

```c
hintptr->supertype = typeabove;       // ACCOUNT
hintptr->subtype   = typebelow;       // DOCUMENT
hintptr->atomtype  = typeofatom;      // 0
movetumbler(isaptr, &hintptr->hintisa); // wheretoputit = user's account
```

**The source document's ISA is discarded before the address is computed.** Only `wheretoputit` (the versioning user's account tumbler) enters the hint.

---

### How the New Tumbler Address Is Built

`createorglingranf` → `createorglgr` → `findisatoinsertgr` → `findisatoinsertnonmolecule` (`granf2.c:203–242`):

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
// ACCOUNT != DOCUMENT → depth = 2

hintlength = tumblerlength(&hintptr->hintisa);
// hintisa = versioning user's account

tumblerincrement(&hintptr->hintisa, depth-1, 1, &upperbound);
findpreviousisagr(fullcrumptr, &upperbound, &lowerbound);

// Result: newISA = userAccount.0.N (next sequential doc under user's account)
```

This is identical to `docreatenewdocument` (`do1.c:239`), which also calls `makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)`. The source document's ISA (`isaptr`) is not consulted anywhere in this allocation path. **The new version's tumbler address is simply the next available slot under the versioning user's account.**

---

### The `homedoc` Field Is Also Zero

Each bottom crum of a POOM carries a `c2dinfo.homedoc` tumbler (`enf.h:129`, `type2dcbc`). One might hope this stores the source ISA. It does not, in this case.

`docopyinternal` (`do1.c:74`) calls `specset2ispanset`, which returns `ISPANID` items. When `insertpm` (`orglinks.c:100–101`) processes these through `unpacksporgl` (`sporgl.c:178–203`):

```c
if (((typeitemheader *)sporglptr)->itemid == ISPANID) {
    movetumbler(&((typeispan *)sporglptr)->stream, streamptr);
    movetumbler(&((typeispan *)sporglptr)->width, widthptr);
    tumblerclear(&infoptr->homedoc);   // ← ZERO
} else if (... SPORGLID) {
    // Only this branch sets homedoc to source doc ISA:
    movetumbler(&((typesporgl *)sporglptr)->sporgladdress, &infoptr->homedoc);
}
```

The SPORGLID path — which does set `homedoc` to the source document's ISA — is taken only when `specset2sporglset` is used (as in `docreatelink`/`domakelink`). `docopyinternal` uses `specset2ispanset`, so `homedoc` is cleared. **The source's identity does not appear in any explicit field of the new version's POOM crums.**

---

### What the New Version Does Contain

After the address is allocated, `docreatenewversion` (`do1.c:281–293`) retrieves the source document's full V-span and builds a vspec:

```c
doretrievedocvspanfoo(taskptr, isaptr, &vspan);   // do1.c:281

vspec.docisa    = *isaptr;    // source document's ISA  — do1.c:287
vspec.vspanset  = &vspan;     // source's full V-span   — do1.c:288

docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // do1.c:293
```

`docopyinternal` calls `specset2ispanset` with this vspec. At `do2.c:35–36`:

```c
findorgl(taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset(taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))
```

This looks up the source document's POOM and converts its V-addresses into I-addresses (permascroll spans). Those I-spans are then inserted directly into the new version's POOM via `insertpm`.

The resulting I-addresses carry the source document's ISA as a **structural prefix**, because they were originally allocated by `findisatoinsertmolecule` (`granf2.c:158–181`) with `hintisa = source_document_ISA`. Text atoms in the source document have I-addresses of the form `sourceISA.0.TEXTATOM.seq`. Both the source document's POOM and the new version's POOM now contain entries that point to the same I-span ranges in the granfilade.

---

### How Ancestry Is Recovered

`doshowrelationof2versions` (`do1.c:428–448`):

```c
specset2ispanset(taskptr, version1, &version1ispans, READBERT)
&& specset2ispanset(taskptr, version2, &version2ispans, READBERT)
&& intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
&& ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
```

The intersection of the two I-span sets is the sole structural evidence of common origin. There is no pointer from the new version's address back to the source. There is no `homedoc` field storing the source. The source document's ISA is implicit in the I-addresses themselves — embedded as a tumbler prefix — but not stored as an explicit reference in the new version's address or in any named field of the new version's POOM crums.

---

### Conclusion

**The source's identity is not encoded in the new version's tumbler address.** When `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` is called (`do1.c:275`), the source ISA is dropped and the hint carries only the versioning user's account. The resulting ISA — `userAccount.0.N` — is indistinguishable from a freshly created document.

**It is also not in the `homedoc` field** of the new version's POOM crums, because `docopyinternal` routes through `specset2ispanset` (ISPANID path), which clears `homedoc` to zero (`sporgl.c:183`).

**Ancestry is recoverable only through the shared I-addresses** in the permascroll. The new version's POOM references the same I-spans the source document references, because those permascroll positions carry the source document's ISA as their tumbler prefix. The `doshowrelationof2versions` operation exploits exactly this — it intersects I-span sets, not tumbler prefixes or explicit back-pointers.
