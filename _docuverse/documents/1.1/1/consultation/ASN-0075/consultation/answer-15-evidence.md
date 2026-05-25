## Question 15 [evidence]

> For a version V created from source D, do the I-addresses unique to D's POOM (those not appearing in V's POOM) constitute the "added since version" set, and is this directly enumerable?

## KB Synthesis

**Short answer:** Mostly no to the first question, and no to the second.

---

**Why the framing is incomplete**

At creation time, V's POOM is an exact copy of D's text POOM [ST-VERSION-CREATE, Finding 0043]. After that point, the two POOMs diverge independently [FC-VERSION-ISOLATION]. The difference set has *two* directions:

- **I-addresses in D's POOM but not V's POOM** = content inserted into D after versioning. This is the "added since version" set you're asking about.
- **I-addresses in V's POOM but not D's POOM** = content deleted from D after versioning (V still holds it). [SS-POOM-MUTABILITY], [ST-DELETE]

So "unique to D's POOM" only captures additions; it omits the deletions-from-D dimension. The full "what changed" picture requires examining both directions.

---

**Why it's not directly enumerable**

The KB describes no operation that returns the I-address set-difference between two POOMs. The closest mechanism is `compare_versions`, which returns the *intersection* (shared spans) [SS-COMPARE-VERSIONS]. The unshared spans from D are the complement — but that complement requires:

1. Full POOM traversal of both D and V (via RETRIEVEDOCVSPANSET to get V-spans, then V→I conversion)
2. Set subtraction on the resulting I-spans

There is no single FEBE opcode for this. Additionally, `compare_versions` crashes when either document contains links [EC-COMPARE-VERSIONS-LINK-CRASH].

---

**A further complication: granfilade vs. POOM**

From [INV-IADDRESS-PERMANENT] and [FC-GRANF-ON-DELETE]: I-addresses removed from D's POOM by DELETE still exist in the granfilade. [FINDDOCSCONTAINING / INV-IADDRESS-PERMANENT] will still report D as containing those addresses. So "what I-addresses live in D's granfilade but not D's current POOM" includes deleted content — not just additions since the version was taken.

---

**What you'd actually need**

To enumerate "added to D since V was created":

1. Use `compare_versions(D, V)` to identify shared I-span pairs
2. The V-spans in D not covered by any shared pair = additions since version

Subject to the link-crash bug, this is feasible for text-only documents. There is no monotonic watermark stored at version creation time [INV-MONOTONIC, Finding 0077 notes no `Σ.next` counter], though in practice all new I-addresses in D will be numerically greater than all I-addresses shared with V, given allocation is strictly monotonically increasing.

---

## Code Exploration

---

## Analysis: I-Addresses Unique to D's POOM and the "Added Since Version" Set

### What the POOM Actually Stores

The POOM is a 2D enfilade indexed on two independent axes [wisp.h:18–20]:

```c
#define I  0
#define V  1
```

Each bottom crum records both a V-span (virtual document position) and an I-span (permascroll address). The POOM is thus a map from V-positions to I-positions. The "I-addresses in a document's POOM" means: the set of I-span intervals from the global granfilade that the document currently references.

---

### How Version Creation Initializes V's POOM

`docreatenewversion` (do1.c:260–299):

1. Creates a **new, empty POOM** for V [do1.c:277]:
   ```c
   createorglingranf(taskptr, granf, &hint, newisaptr)
   ```

2. Retrieves D's V-span [do1.c:281]:
   ```c
   doretrievedocvspanfoo(taskptr, isaptr, &vspan)
   ```
   This reads `((typecuc*)orgl)->cdsp.dsas[V]` and `cwid.dsas[V]` directly [orglinks.c:159–160].

3. Builds a vspec pointing to D with D's V-span, then calls `docopyinternal` [do1.c:293]:
   ```c
   docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
   ```

`docopyinternal` (do1.c:66–82) does:
```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)  // D's V-spans → I-spans via D's POOM
insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)         // writes those I-spans into V's POOM
```

The conversion `specset2ispanset` → `vspanset2ispanset` (do2.c:36, orglinks.c:397–402) calls `permute()` which walks D's POOM projecting the V-dimension onto the I-dimension.

**Critical consequence:** After version creation, V's POOM contains the identical I-span values as D's POOM. They reference the same granfilade content. Both documents share every I-address.

---

### What Happens When Content Is Added to D (or V)

New insert to D via `doinsert` (do1.c:87–123):
```c
inserttextingranf(taskptr, granf, &hint, textset, &ispanset)   // alloc new I-addresses
docopy(taskptr, docisaptr, vsaptr, ispanset)                    // record in D's POOM
```

`inserttextgr` (granf2.c:83–109) calls `findisatoinsertgr` → `findisatoinsertmolecule` (granf2.c:158–181), which increments from the highest existing I-address. The new I-spans land in D's granfilade and D's POOM — but V's POOM is **not touched**.

---

### Does "I-Addresses in D's POOM but Not V's POOM" = "Added Since Version"?

**Partly, but not exactly.** The set has two components:

| Source | Explanation |
|--------|-------------|
| Content inserted into D after V branched | New I-addresses in D's granfilade, new entries in D's POOM — V's POOM never saw them |
| Content deleted from V (that D retains) | V called `deletevspanpm` (orglinks.c:145–152) → `deletend`, removing those POOM crums from V; D's POOM retains them |

The set "I-addresses in D but not V" = **(added to D after branching) UNION (deleted from V after branching).**

This is more accurately described as "content D has that V doesn't," not purely "added since version." If only V has been edited and D has not, the entire set is deletions from V, not additions at all.

The true "added to D since V" would require knowing the temporal branching point, which is not recorded in the POOM itself — it's structural state only.

---

### The Link-Subspace Complication

The POOM stores content in two V-subspaces [orglinks.c:37–48]:

- **V-space `< 1.0`** (link subspace): document metadata — link ISAs with unique identities, not transcludable content
- **V-space `>= 1.0`** (text subspace): actual transcludable content with shared permascroll identity

`doshowrelationof2versions` (do1.c:437–441) explicitly filters before any comparison:
```c
filter_specset_to_text_subspace(taskptr, version1);
filter_specset_to_text_subspace(taskptr, version2);
```

This is because link-subspace ISAs are allocated by `findisatoinsertnonmolecule` (granf2.c:203–242) with LINKATOM hints — they are unique per document and have no "common origin" across documents [do1.c:377–384]. Any I-address comparison that doesn't filter the link subspace would produce spurious non-overlapping content that is meaningless as a difference.

---

### Is It Directly Enumerable?

**Individually: yes.** The I-span coverage of any document is enumerable:
1. `doretrievedocvspanset` (do1.c:322–334) → V-spans
2. `specset2ispanset` → `vspanset2ispanset` (orglinks.c:397–402) → `permute()` (orglinks.c:404–422)

`permute()` walks the 2D enfilade projecting V→I via `retrieverestricted` (retrie.c), producing a complete ispanset. This is a full traversal of the POOM tree.

**The set difference: not a primitive.** The codebase provides:
- `intersectspansets()` — intersection of two ispansets (used by `doshowrelationof2versions`)
- **No `differencespansets()`** exists anywhere

To enumerate the difference, you would need to:
1. Enumerate D's full ispanset (D_ispans)
2. Enumerate V's full ispanset (V_ispans)
3. Compute: `D_ispans - intersect(D_ispans, V_ispans)`

Step 3 is not implemented. `doshowrelationof2versions` gives you the intersection half [do1.c:443–448]:
```c
specset2ispanset(taskptr, version1, &version1ispans, READBERT)
specset2ispanset(taskptr, version2, &version2ispans, READBERT)
intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
```

You'd have to subtract `commonispans` from D's full ispanset — a subtraction loop over sorted I-span intervals. The data is there; the subtraction primitive is absent.

---

### Summary

The I-addresses unique to D's POOM (absent from V's POOM) are **not** cleanly "the added-since-version set." They are the union of additions to D and deletions from V — both produce the same structural signature (an I-address D has that V doesn't). Without external temporal metadata, the POOM alone cannot distinguish these two cases.

Enumerability is feasible but indirect: walk both POOMs via `permute()` to get ispansets, then compute the set difference manually. That subtraction operation is absent from the current codebase. The existing `doshowrelationof2versions` computes only intersection. Any "added since" analysis would also need to filter to text subspace (V ≥ 1.0) before the comparison, exactly as `filter_specset_to_text_subspace` (do1.c:386–411) does, since link-subspace ISAs carry no cross-document identity.
