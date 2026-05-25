## Question 17 [evidence]

> When two documents share I-addresses originating from a third document (transitive transclusion via COPY chains), is the correspondence result identical to the case where doc1 directly transcluded from doc2 — i.e., is provenance forgotten in favor of pure identity intersection?

## KB Synthesis

Yes — `compare_versions` operates purely on I-address intersection, so provenance chains are entirely forgotten.

**Mechanism:**

`compare_versions` (SHOWRELATIONOF2VERSIONS) converts each document's V-spans to sporgls via `vspanset2sporglset`, then intersects on `sporglorigin` (the I-address field) [INT-SPORGL-VERSION-COMPARE, Finding 0013]. The `sporgladdress` field carries which document each span came from for output purposes — but the *intersection predicate* is solely I-address equality [SS-COMPARE-VERSIONS, Finding 0015]:

> Two spans correspond if and only if they map to the same permascroll content identities.

There is no "hops from origin" weighting, no depth tracking, no provenance filter.

**Transitive identity confirms this:**

[INV-TRANSITIVE-IDENTITY] states the explicit invariant: `shares_identity(A, B) ∧ shares_identity(B, C) ⟹ shares_identity(A, C)`. The KB notes this "falls out of the state-transition definition of vcopy" — COPY preserves I-addresses rather than copying them, so once the I-addresses exist in a document, that document is indistinguishable from any other holder for comparison purposes [ST-VCOPY, Finding 0018].

**Concrete implication:**

If B holds I-addresses α₁..α₅ (from original insertion), A copies from B, and C copies from B independently:

```
compare_versions(A, C):
  A's sporgls: sporglorigin = α₁..α₅
  C's sporgls: sporglorigin = α₁..α₅
  Intersection: α₁..α₅  →  same result as compare_versions(A, C) where A copied directly from C
```

The fact that both derived their I-addresses from B is irrelevant — `correspond.c` sees two sets of I-addresses and intersects them [SS-COMPARE-VERSIONS].

**One caveat:** `compare_versions` crashes when either document contains link-subspace entries [EC-COMPARE-VERSIONS-LINK-CRASH], and the operation is restricted to text subspace I-addresses [PRE-COMPARE-VERSIONS]. Those constraints apply equally to direct and transitive cases.

---

## Code Exploration

I now have everything I need for a complete answer. Let me compile the full code-cited analysis.

---

## Answer: Transitive COPY Chains and Correspondence — Provenance Is Forgotten

The short answer: **yes, the correspondence result is identical**. Transitive transclusion via COPY chains produces the same result as direct transclusion. Provenance is not stored or consulted. The system reasons purely over I-address identity.

Here is the full trace.

---

### 1. What `docopy` Does to I-Addresses

`docopy` [do1.c:45–65]:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    ...
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   /* the meat */
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
    );
}
```

The pipeline is:

- `specset2ispanset` [do2.c:14–46] converts each V-spec to I-spans by calling `vspanset2ispanset` [orglinks.c:397–401] → `permute` [orglinks.c:404–422] → `span2spanset` [orglinks.c:425–454] → `retrieverestricted` [retrie.c:56–85]. This queries the *source* document's org and returns whatever I-addresses map to the requested V-range.

- `insertpm` [orglinks.c:75–134] then writes those I-addresses into the *destination* document's org:

```c
for (; sporglset; ...) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);   /* I-address preserved as-is */
    movetumbler (&lwidth,  &crumwidth.dsas[I]);
    movetumbler (vsaptr,   &crumorigin.dsas[V]);   /* only V-position changes */
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```

[orglinks.c:100–131]

**No new I-addresses are created.** The I-address range from the source is placed verbatim into the destination's org. Only the V-position (where it appears in the destination document) is new.

This applies transitively: if doc3 contains I-span [A..B], and doc1 copies from doc3, doc1's org now contains crums at some V-position with I-addresses [A..B]. If doc2 also copies from doc3, doc2's org similarly contains [A..B]. The two documents are now I-address peers — the fact that both copied from doc3 leaves no further record.

---

### 2. How Correspondence Is Computed

The correspondence function is `doshowrelationof2versions` [do1.c:428–448]:

```c
bool doshowrelationof2versions(typetask *taskptr, typespecset version1, typespecset version2, typespanpairset *relation)
{
    typeispanset version1ispans = NULL;
    typeispanset version2ispans = NULL;
    typeispanset commonispans  = NULL;

    filter_specset_to_text_subspace(taskptr, version1);   /* strip link subspace */
    filter_specset_to_text_subspace(taskptr, version2);

    return
        specset2ispanset(taskptr, version1, &version1ispans, READBERT)
     && specset2ispanset(taskptr, version2, &version2ispans, READBERT)
     && intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
     && ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation);
}
```

Step by step:

1. **`specset2ispanset(version1, ...)`** — walks version1's org via `permute` and returns the I-spans that appear in it. Same for version2.

2. **`intersectspansets`** [correspond.c:145–188] — pure tumbler range intersection, nothing more:

```c
for (; set1; set1 = set1->next) {
    for (p = set2; p; p = p->next) {
        if (comparespans (taskptr, set1, p, set3, spantype))
            set3 = &(*set3)->next;
    }
}
```

`comparespans` [correspond.c:191–208] calls `spanintersection` [correspond.c:210–265], which is pure tumbler arithmetic — it computes the overlap of two address ranges. There is no document-identity check, no provenance field, no copy-chain traversal.

3. **`ispansetandspecsets2spanpairset`** [do2.c:185–207] — takes the common I-spans and maps them back to V-positions in each document via `restrictvspecsetovercommonispans` → `ispan2vspanset` → `permute`, then assembles the pair-set. This is also purely I-address driven.

**The correspondence algorithm is: intersect the I-address sets of the two documents. That's it.**

---

### 3. Is Provenance Tracked Anywhere?

The bottom-level crum struct (`type2dcbc`) contains a `homedoc` field (visible in `isanextensionnd` [insertnd.c:301–309]):

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);   /* can't merge crums from different homedocs */
    ...
```

This is used only during *insertion* to decide whether to extend an existing crum rather than create a new one. It is a compaction heuristic, not a provenance record visible to callers.

During *retrieval*, `retrieverestricted` [retrie.c:56–85] accepts a `docisaptr` that would populate `infoptr->homedoc` for filtering, but `span2spanset` [orglinks.c:435] always passes `(typeisa*)NULL`:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
                                                                  ^^^^^^^^
```

And `findcbcinarea2d` [retrie.c:247–250] treats a non-NULL `infoptr` as a hard error in the production build:

```c
#else
    if (infoptr)
        gerror("!NULL");
#endif
```

The debug comment above it reads: *"not NULL infoptr versions mumble specialcase 11/27/84 shouldent happen till we try something fancier"* — this was an experimental path never completed. `homedoc`-based retrieval filtering was never put into production.

**Conclusion: the copy chain is not stored in any retrievable form, and the retrieval path explicitly refuses a homedoc filter.**

---

### 4. Direct Answer to the Question

Given:
- doc3 contains content with I-spans **[A..B]**
- doc1 copies from doc3 → doc1's org contains crums mapping some V-range to **[A..B]**
- doc2 copies from doc3 → doc2's org contains crums mapping some V-range to **[A..B]**

`compare_versions(doc1, doc2)` computes:
```
version1ispans = [A..B]    (from specset2ispanset on doc1)
version2ispans = [A..B]    (from specset2ispanset on doc2)
commonispans   = [A..B]    (from intersectspansets)
```

`compare_versions(doc1, doc3)` computes exactly the same commonispans. So does any pairing of documents that happen to contain the same I-span range.

**The result is identical regardless of how many COPY hops separate the documents from their common ancestor.** The system has no mechanism to distinguish:
- doc1 and doc2 both copied from doc3 (transitive)
- doc1 copied directly from doc2 (direct)
- doc1 and doc2 both independently inserted the same permascroll content (coincident)

In all cases, I-address identity is the only criterion. Provenance is forgotten the moment the content is inserted into a document's org via `insertnd`. The enfilade is a permutation matrix between V-space and I-space — it records *where* content lives, not *how it arrived there*.
