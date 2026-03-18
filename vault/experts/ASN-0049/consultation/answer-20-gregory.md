## Question 20 [gregory]

> When `docreatenewversion` copies the text subspace of a document that itself contains transcluded content (shared I-addresses with other documents), does the version's POOM preserve the original I-addresses from the transclusion source — making the version discoverable through `find_links` for links created against any document in the transclusion chain?

## KB Synthesis

Yes. The version's POOM preserves the original I-addresses from the transclusion source, and the version is fully discoverable through `find_links` for links anywhere in the transclusion chain.

**Mechanism: CREATENEWVERSION shares, not copies, I-addresses**

`docreatenewversion` copies the text subspace by calling `docopyinternal` → `insertpm`, which places existing I-addresses into the new POOM without allocating fresh ones [ST-VERSION-CREATE, Finding 0046]. If the source document's text subspace contains I-addresses that originated in a transclusion source (placed there by a prior `docopy`/vcopy), those same I-addresses appear verbatim in the version's POOM.

**Why transclusion I-addresses are preserved through version creation**

Vcopy preserves I-addresses from its source [ST-VCOPY, Finding 0018]. So if document A transcluded "shared text" from document B, A's POOM contains B's I-addresses at those V-positions. When V = CREATENEWVERSION(A), `docopyinternal` reads A's current vspan and copies all its I-addresses — including the ones that originated in B — into V's POOM. V now holds B's I-addresses directly [INT-VERSION-TRANSCLUSION, Finding 0032].

**Why find_links works across the full chain**

`find_links` operates entirely in I-space via the spanf index: it converts the query V-span to I-spans, then searches the spanfilade for links whose endpoints intersect those I-addresses [INT-LINK-VERSION, Finding 0046]. Since V shares I-addresses with both A and B, `find_links(V)` will discover:
- Links created against A's text (same I-addresses)
- Links created against B's text (same I-addresses, shared through transclusion)
- Links created against any document in the transclusion chain, by transitivity [INV-TRANSITIVE-IDENTITY, Findings 0007, 0008]

This is confirmed experimentally: CREATENEWVERSION of a document with transcluded linked content produces a version where `find_links` returns links from the original chain [INT-LINK-TRANSCLUSION, Finding 0043]:

> "Despite CREATENEWVERSION not copying link subspace entries to the version's POOM, find_links still works on the version. This is because link discovery operates on content identity (I-addresses), not POOM structure."

**The version has no link subspace entries but that is irrelevant**

The version's POOM contains no entries in the 2.x subspace — it has no link orgls of its own [ST-VERSION-CREATE, Finding 0043]. But link discoverability is independent of POOM link storage; it depends solely on I-address intersection in the spanf [INT-LINK-TRANSCLUSION, Finding 0043]. The spanf was populated when the original INSERT/COPY operations occurred and is never modified by version creation [INV-SPANF-WRITE-ONLY].

**Summary**

The invariant is: `version(doc) inherits the complete I-address set of doc.text_subspace`, and `find_links` is a pure function of I-address intersection, so the version is discoverable for every link reachable through any document sharing those I-addresses — the full transclusion chain, including transitive chains of transclusion and versioning [INV-TRANSITIVE-IDENTITY, Finding 0008].

---

## Code Exploration

Now I have everything I need to give a complete, code-grounded answer.

---

## Answer

**Yes — `docreatenewversion` preserves original I-addresses from the transclusion source, and those preserved I-addresses make the version discoverable via `find_links` for links targeting any document in the transclusion chain.**

Here is the precise mechanism, traced from source:

---

### 1. What `docreatenewversion` actually copies

`docreatenewversion` [do1.c:260–299]:

```c
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) return FALSE;   // line 281

vspec.itemid = VSPECID;
movetumbler(isaptr, &vspec.docisa);   // vspec points to the SOURCE document
vspec.vspanset = &vspan;              // ...over its full V-span

docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);   // line 293
```

The `vspec` passed to `docopyinternal` identifies the **source** document (`docisa = isaptr`) and covers its entire V-span. `doretrievedocvspanfoo` calls `retrievedocumentpartofvspanpm` [orglinks.c:155–162], which reads `cdsp.dsas[V]` and `cwid.dsas[V]` from the root crum — the bounding box of the source's entire V-space (including all transcluded content within it).

---

### 2. V→I translation: the source document's POOM is the oracle

`docopyinternal` [do1.c:74] calls `specset2ispanset`:

```c
if (!specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)) return FALSE;
```

`specset2ispanset` [do2.c:34–38] handles a `VSPECID`:

```c
findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)  // source doc's ORGL
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))
```

It looks up the **source document's** enfilade (not the new version's) and calls `vspanset2ispanset` [orglinks.c:397–402]:

```c
typeispanset *vspanset2ispanset(...) {
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` [orglinks.c:414–416] calls `span2spanset` for each span, which in turn calls:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);   // [orglinks.c:435]
```

The `(typeisa*)NULL` last argument means **no ISA filtering**. `retrieverestricted` walks the source POOM enfilade and returns every (I-range, V-range) crum whose V-coordinates intersect the query. `context2span` then extracts the **I-coordinates** from those crums.

**Outcome:** The `ispanset` produced is the complete set of permascroll I-addresses that the source document's V-space maps to — including any shared I-addresses from transcluded content (content that was itself inserted via `docopy` from another document, carrying over the same permascroll I-addresses).

---

### 3. I-addresses inserted into the new version's POOM unchanged

`docopyinternal` [do1.c:78] then calls:

```c
insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
```

In `insertpm` [orglinks.c:100–131]:

```c
for (; sporglset; sporglset = ...) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);   // I-address placed here UNCHANGED
    movetumbler (&lwidth, &crumwidth.dsas[I]);
    movetumbler (vsaptr, &crumorigin.dsas[V]);     // new V-address assigned here
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);   // line 130
}
```

The I-coordinates (`lstream`, `lwidth`) come from the `ispanset` derived above and are placed into `crumorigin.dsas[I]` / `crumwidth.dsas[I]` **without modification**. Only the V-coordinates are freshly assigned (from `vsaptr`). The resulting POOM crums in the new version map new V-positions to exactly the same permascroll I-addresses as the source document had.

---

### 4. The spanfilade also records the shared I-addresses

`docopyinternal` [do1.c:79] also calls:

```c
insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

`insertspanf` [spanf1.c:15–54] indexes into the global spanfilade using the I-addresses from `ispanset` (the `ISPANID` branch, lines 26–29), keyed under the new document's ISA. This is what allows `find_links` to locate the version when searched by I-address.

---

### 5. How `find_links` discovers the version

`find_links` calls `dofindlinksfromtothree` [do1.c:348] → `findlinksfromtothreesp` [spanf1.c:56–103].

The query path: V-specs → `specset2sporglset` (V→I translation through the **queried** document's POOM) → `sporglset2linkset` (spanfilade search by I-address).

When a link was created against document A pointing to content at permascroll I-address X (stored in the spanfilade at I-address X), and document B's POOM maps some V-position to that same I-address X:

- B's `find_links` query translates B's V-position → I-address X → finds the link
- After versioning B → C via `docreatenewversion`, C's POOM also maps a V-position to I-address X (because `insertpm` preserved it unchanged)
- C's `find_links` query likewise resolves to I-address X → finds the same link

Links index the spanfilade by permascroll I-address. Transclusion and versioning both preserve those I-addresses. The identity of content _is_ its I-address.

---

### Summary

| Step | Code | What happens |
|------|------|-------------|
| `doretrievedocvspanfoo` | do1.c:281, orglinks.c:155 | Retrieves bounding V-span of source doc |
| `specset2ispanset` | do2.c:34–38 | Translates source doc's V-span → I-spans via **source's** POOM |
| `vspanset2ispanset` → `retrieverestricted` | orglinks.c:397, 435 | Walks source POOM; produces actual permascroll I-addresses including those from any transclusions |
| `insertpm` | orglinks.c:105–109 | Writes I-addresses **unchanged** into new version's POOM crums |
| `insertspanf` | spanf1.c:49–51 | Indexes those same I-addresses in global spanfilade under new version's ISA |
| `find_links` query | spanf1.c:70–100 | Converts query V-spec → I-addresses via new version's POOM; hits same spanfilade entries |

The POOM of the new version is not a snapshot of V-coordinates — it is a new mapping of new V-positions onto the **same underlying permascroll I-addresses**. Those addresses are the stable content identity in Xanadu. Any link ever created against content at those I-addresses — regardless of which document's V-space it was expressed in at link-creation time — is discoverable through the version.
