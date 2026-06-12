## Question 2 [evidence]

> In udanax-green's link retrieval (e.g., findLinksFromToThree and its specset arguments), is the state being queried — which document versions' spans are searched — supplied by the caller on each query, or fixed by the backend, and can historical (non-current) versions be queried the same way as current ones?

## KB Synthesis

The query state is entirely **caller-supplied on each call**, and historical versions are fully queryable on equal footing with current documents.

## How the query state is supplied

`find_links` (and the related RETRIEVEENDSETS/FOLLOWLINK operations) work through a V→I conversion driven by the caller's specset. Each specset encodes a `(docid, vstart, vwidth)` triple [SS-SPECSET]. The backend consults **that document's POOM** to convert the V-span to I-addresses, then searches the global spanfilade for I-address intersections [ST-FIND-LINKS, SS-FIND-LINKS].

The caller selects "which state to query" implicitly by choosing which document address to put in the specset. Nothing about the current session account, a connection-level cursor, or any backend-held pointer determines what document is searched — it is fully in the caller's hands each call.

FOLLOWLINK has an analogous explicit parameter: `follow_link(link_id, whichend, homedoc)` — the caller names the document whose POOM is used for the I→V resolution step [SS-FOLLOWLINK]. A caller that passes a different `homedoc` gets a different (or empty) result for the same link.

## Historical versions are first-class query targets

Versions are independent documents with their own POOM trees and their own addresses (child addresses under the source document) [SS-VERSION-ADDRESS]. Because CREATENEWVERSION copies text I-addresses from the source rather than allocating new ones [ST-VERSION-CREATE, INT-LINK-VERSION], a version's POOM maps its V-spans to the **same** I-addresses that the source maps its V-spans to.

Consequence: passing a specset referencing a historical version's address is mechanically identical to passing one referencing the current document. The spanfilade is indexed by I-address, which is shared. Links discoverable from the source are discoverable from any version [INT-LINK-VERSION Finding 0032]:

> "`find_links(source) = find_links(version)` at creation time, diverging only as edits create new I-addresses in either document."

The document must be open for the POOM lookup to succeed [SS-DOCUMENT-LIFECYCLE, PRE-RETRIEVE-CONTENTS], but no special mode or flag is needed to query a version versus its source.

## One caveat: the orgl-range filter is disabled

`find_links` accepts an orgl-range parameter that was designed to restrict which documents' links are returned. This filter is entirely non-functional due to a `TRUE||!homeset` guard that always fires [EC-FIND-LINKS-GLOBAL, PRE-FIND-LINKS Finding 0069]. All searches are effectively global in the orgl dimension — only the I-address (span dimension) match matters. A caller cannot scope a `find_links` call to "only links homed in version V"; it will always get all links whose endpoints share I-addresses with the query, regardless of where those links live.

---

## Code Exploration

I now have everything I need to give a complete, code-cited answer.

---

## Link Retrieval in udanax-green: Version State, Specsets, and Access Control

### 1. The specset arguments are fully caller-supplied, per query

The FEBE command for `find_links` is command 30, dispatched to `findlinksfromtothree` [`fns.c:189`]. Its request parser reads **four arguments** directly from the wire:

```c
// get1.c:110-125 (interactive) / get1fe.c:104-113 (FEBE frontend)
bool getfindlinksfromtothree(...)
{
    getspecset(taskptr, fromvspecsetptr)    // source content constraint
    getspecset(taskptr, tovspecsetptr)      // target content constraint
    getspecset(taskptr, threevspecsetptr)   // type/third-endset constraint
    getspanset(taskptr, homesetptr, ISPANID) // home document filter
}
```

Each `specset` is a caller-constructed linked list of items, each tagged either:
- **`VSPECID`** — a `typevspec` containing a `docisa` (tumbler naming a specific document or version) plus a set of V-spans within that document [`get2fe.c:182–190`]
- **`ISPANID`** — a raw I-span (absolute permascroll address) that requires no document resolution [`get2fe.c:167–170`]

The `docisa` in a VSpec is whatever tumbler the caller put on the wire. There is no backend mechanism that silently substitutes a "current" version. The caller owns this state.

---

### 2. The homeset filter is parsed but discarded

The most striking thing in `fns.c:197–199`:

```c
// fns.c:197-199
if (
    getfindlinksfromtothree(taskptr, &fromvspecset, &tovspecset,
                            &threevspecset, &homeset)
 && dofindlinksfromtothree(taskptr, fromvspecset, tovspecset,
                            threevspecset, (typeispan*)NULL/*homeset*/, &linkset))
```

The `homeset` is parsed but then **explicitly replaced with `NULL`** at the call site. This is Bug 015 (documented in `docs/client-api.md`): the `homedocids` filter has no effect because it is never forwarded.

Even if it were forwarded, `sporglset2linkset` in `sporgl.c:227` has a second layer of suppression:

```c
// sporgl.c:227
if (TRUE||!homeset) {
    // unconditionally builds a nullhomeset with width 100
    // the passed homeset is ignored regardless
}
```

The `TRUE||` makes the condition always take the nullhomeset path regardless of the argument.

---

### 3. The access control path bypasses open-state checks entirely

`dofindlinksfromtothree` in `do1.c:348` delegates to `findlinksfromtothreesp` with the global `spanf`:

```c
// do1.c:348-353
bool dofindlinksfromtothree(typetask *taskptr, typespecset fromvspecset,
    typespecset tovspecset, typespecset threevspecset,
    typeispan *orglrangeptr, typelinkset *linksetptr)
{
    return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset,
                                  threevspecset, orglrangeptr, linksetptr);
}
```

`findlinksfromtothreesp` converts each specset with `NOBERTREQUIRED` [`spanf1.c:71–75`]:

```c
// spanf1.c:70-75
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (tovspecset)
    specset2sporglset(taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);
if (threevspecset)
    specset2sporglset(taskptr, threevspecset, &threesporglset, NOBERTREQUIRED);
```

`specset2sporglset` in `sporgl.c:14` calls `findorgl(..., type)` to resolve each VSpec's `docisa` to a granfilade node. `findorgl` in `granf1.c:17` calls `checkforopen`:

```c
// granf1.c:17-41
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr,
              typeorgl *orglptr, int type)
{
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        // ... return FALSE if not open
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

`checkforopen` in `bert.c:52–61`:

```c
// bert.c:59-61
if (type == NOBERTREQUIRED) {
    return 1;  /* Random > 0 */
}
```

When `type == NOBERTREQUIRED`, `checkforopen` immediately returns success (> 0) without consulting the bert table at all. The document named in the specset does **not** need to be open for link queries to succeed. This is in deliberate contrast to content retrieval, which uses `READBERT` [`do1.c:344`], and writes, which use `WRITEBERT` [`do1.c:40`].

---

### 4. Historical versions are queryable identically to current ones

Because:
1. The `docisa` in each VSpec is fully caller-supplied and unvalidated at the query level
2. Access control is entirely bypassed (`NOBERTREQUIRED`)
3. The version's granfilade entry (its V→I mapping at the time of its existence) remains in the granfilade

…a caller can name any historical version's tumbler address in the specset VSpec and the backend will use that version's V→I mapping to find links. The caller does not need to `open_document` the historical version first.

The only constraint on historical queries is structural: the spanfilade (`spanf`) is a global append-only index where links are recorded by I-address (permascroll identity). A link is findable via a historical version's specset only if the V-spans named in that specset map to I-addresses that were registered in the spanfilade at link-creation time. Because the spanfilade is never pruned (Finding 0057: it is write-only), links attached to content that existed in historical versions remain discoverable even if those versions are no longer current.

---

### 5. Contrast with content retrieval

For comparison, `doretrievev` in `do1.c:338–346` uses `READBERT`:

```c
// do1.c:344
specset2ispanset(taskptr, specset, &ispanset, READBERT)
```

This requires the document to be open for reading. Link search (command 30) intentionally skips this requirement — the search operation is designed to work across arbitrary document versions without forcing the caller to open each one.

---

### Summary

| Aspect | Behavior |
|--------|----------|
| **Which versions are searched** | Entirely caller-supplied via `docisa` in each VSpec; no backend "current version" substitution |
| **Historical versions** | Queryable identically to current versions; no open handle required |
| **Access control** | Bypassed via `NOBERTREQUIRED` in all three specset conversions [`spanf1.c:71–75`] |
| **homeset filter** | Parsed, then discarded (passed as `NULL`) at `fns.c:198`; also unconditionally overridden at `sporgl.c:227` |
| **Search scope** | Global spanfilade `spanf` — all links ever created, across all documents [`do1.c:352`] |
| **NULL specset argument** | Acts as wildcard (unconstrained) for that endset dimension |
