## Question 18 [gregory]

> Was the two-space architecture (mutable V-positions over immutable I-identities) present from the earliest Xanadu designs, or did it emerge during green's implementation as a solution to a specific problem like transclusion tracking or content-addressed linking?

## KB Synthesis

The KB does not contain information to answer this question.

The entries document what the implementation does and why specific mechanisms work the way they do, but contain no historical or archival evidence about design chronology — no references to design documents, early prototypes, Nelson's notebooks, or the evolution of the architecture over time.

What the KB *does* show is that the two-space architecture has strong internal coherence: the `acceptablevsa()` stub [SS-SUBSPACE-CONVENTION, Finding 0010] signals the subspace convention was a *planned* enforcement point that was never completed, suggesting the V/I distinction predates the green implementation as a design intent rather than emerging from it. The clean separation of `granf` and `spanf` into distinct global structures initialized at startup [SS-DUAL-ENFILADE, Finding 0012] also suggests deliberate upfront architectural choice rather than organic accretion.

But whether that design intent originated in 1960s Xanadu theory, the ZigZag period, or earlier in green's development — that's not answerable from this KB. You'd need the design documents or my direct recollection of those conversations, which isn't what this KB captures.

---

## Code Exploration

Now I have everything I need. Here is my full answer.

---

## The Two-Space Architecture in udanax-green: Code Evidence

The question is whether the V-position / I-identity split was designed from the beginning or emerged during implementation. The source code answers this decisively — but the answer requires tracing through the actual data structures rather than relying on retrospective accounts.

---

### What the Code Actually Defines

The two-space architecture is encoded in its most primitive, non-derivable form in `wisp.h:18-20`:

```c
/* wid and dsp indexes for pm */
#define I  0
#define V  1
```

These two constants — `I` for invariant, `V` for variant — are indices into every positional array in the system. They appear at the bottom of the type hierarchy, before any enfilade-specific logic.

The type that carries both coordinates is `typewid`/`typedsp`, defined at `wisp.h:48-55`:

```c
#define MAXLOXIZE 2    

struct structwid {
    tumbler dsas[MAXLOXIZE];
};
typedef struct structwid typewid;
typedef typewid typedsp;
```

`MAXLOXIZE = 2`: one slot for I, one for V. Both slots are tumblers — the system's arbitrary-precision address type. There is no asymmetry in representation; I and V are equal citizens in the struct.

The diagram in `wisp.h:29-44` makes explicit what each enfilade type carries in each dimension:

```
                   wid             dsp
    -----------------------------------------
   gr:  |           WIDTH           WIDTH
        |
   sp:  |         ORGLRANGE         ORGLRANGE
        |           SPANRANGE         SPANRANGE
        |
   pm:  |             I                 I
        |               V                 V
```

The POOM (permutation matrix) is the only enfilade that carries both I and V. This is the architectural fact: POOM is a **2D tree**, and its dimensionality is not an afterthought — it is what makes it a POOM.

---

### How the Two-Space Structure Propagates

Every crum in the tree carries both coordinates. From `enf.h:47-48` (the shared header for all crum types):

```c
typewid cwid;
typedsp cdsp;
```

`cwid` is the width in both dimensions; `cdsp` is the displacement in both dimensions. Since both are `typewid` (i.e., `tumbler dsas[2]`), every crum — from the apex down to each bottom leaf — simultaneously knows its extent in I-space (`dsas[I]`) and its extent in V-space (`dsas[V]`). This is not a mapping between two separate structures. It is one structure with two coordinate axes.

The rearrangement cut structure in `ndenf.h:12-16` makes the directional asymmetry visible:

```c
typedef struct structknives {
    INT nblades;
    tumbler blades[MAXCUTS];
    INT dimension;  /* always V, assigned by rearrange2d */
} typeknives;
```

The comment `/* always V, assigned by rearrange2d */` is the only dimension-specific comment in the headers. Document editing — rearranging content — happens exclusively in V-space. I-addresses do not move. They cannot move. They are the identity axis.

---

### The POOM Insertion: Where Both Axes Are Set

The core two-space assignment happens in `insertpm()` (`orglinks.c:75-134`). This is the function that records content into a document's permutation matrix. At lines 105 and 113:

```c
movetumbler (&lstream, &crumorigin.dsas[I]);   /* line 105 */
...
movetumbler (vsaptr, &crumorigin.dsas[V]);      /* line 113 */
```

`lstream` is the I-address: where the content lives in the permascroll. It comes from the sporgl (span-original), which was set when the content was first written — immutable by design. `vsaptr` is the V-address: where the user placed this content in the current document. It is mutable; it shifts when other content is inserted or deleted around it.

Both are written into the same `crumorigin` struct — into `dsas[I]` and `dsas[V]` respectively — and inserted into the POOM tree together via `insertnd()` at line 130:

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```

The `V` argument to `insertnd` tells the tree insertion code which dimension is the primary ordering axis (V-positions order the document). But the I-coordinate rides along, stored in the same crum, accessible immediately without a separate lookup.

The inline comment at line 114 is an artifact of the development era:

```c
/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/
```

This is a timestamped note — March 1, 1985 — from someone initialed "reg" who was uncertain about the tumbler shift calculation in `insertpm`. Note what is and is not in doubt: the arithmetic of one implementation detail is questioned; the two-axis structure of the crum origin is not questioned at all. It was not under review.

---

### The Conversion Functions: Architectural Symmetry

The V↔I conversion functions in `orglinks.c:389-454` exhibit perfect symmetry:

```c
/* line 389 */
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, 
                              typeispan *ispanptr, typevspanset *vspansetptr)
{
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}

/* line 397 */
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, 
                                 typevspanset vspanptr, typeispanset *ispansetptr)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

Both delegate to a single `permute()` at line 404:

```c
typespanset *permute(typetask *taskptr, typeorgl orgl, 
                     typespanset restrictionspanset, INT restrictionindex,
                     typespanset *targspansetptr, INT targindex)
```

`permute()` takes a restriction dimension and a target dimension as generic integer parameters. The logic is completely symmetric — `I→V` and `V→I` are the same function, called with swapped arguments. This is not the shape of a function that was added retroactively to solve a transclusion tracking problem. It is the shape of a function that was written knowing from the beginning that both directions would be needed in equal measure.

---

### The Type System Encodes the Distinction

From `xanadu.h:73-76`:

```c
typedef typespan typevspan;
typedef typevspan * typevspanset;
typedef typespan typeispan;
typedef typeispan * typeispanset;
```

`typevspan` and `typeispan` are identical in representation — both are `typespan` with `stream` and `width` tumblers. The distinction is semantic, not structural. This is a C-era design choice that says: "these two things are the same bits, but they must not be confused." The naming convention enforces at the type level what the architecture enforces at the data level. You do not build this vocabulary into your type system unless you plan to use it throughout.

---

### What the Code Cannot Tell Us

The code contains no design rationale comments explaining *why* I and V exist. Every comment in `orglinks.c`, `wisp.h`, and `enf.h` treats the two-space model as an established fact. There is no "we added this because..." note, no historical comment explaining the motivation. The vocabulary — permutation matrix, invariant, variant, virtual space address — is used without explanation, as though it required none.

The comment header of `orglinks.c:9` identifies the file's purpose:

```
/* orglinks.d - permutation matrix enfilade calls */
```

The name "permutation matrix" encodes the architecture: a matrix that permutes between two coordinate systems. This is what a POOM is. The naming is not incidental.

---

### The Answer

The two-space architecture was **present from the earliest design** and is not a solution to a problem discovered during implementation.

The evidence for this in the code:

1. **It is structurally irreducible.** `MAXLOXIZE = 2` is a named constant embedded in the lowest primitive type. Every crum — in every enfilade — carries a 2-slot array. You cannot peel the I/V duality off the data structure without redesigning the data structure.

2. **The conversion is symmetric.** `permute()` was written to handle both `I→V` and `V→I` with identical generality. This is first-class design, not a retrofit.

3. **The type system encodes it.** `typevspan` and `typeispan` are named distinct types despite being structurally identical. The distinction is semantic intent baked into the type aliases before any function was written.

4. **Rearrangement is V-only by invariant.** `ndenf.h:15` says `dimension; /* always V, assigned by rearrange2d */`. The I-axis does not rearrange. This is not a constraint added after the fact; it is the definition of what I means.

5. **The POOM is the architecture.** The POOM is a 2D tree. Its two dimensions ARE the two spaces. Transclusion tracking — finding every document containing a given I-address — is the natural query in this structure: walk the POOM restricted to a given I-range and collect all corresponding V-positions. This query (`ispan2vspanset`) is exactly what `permute()` provides.

The V/I separation corresponds to Ted Nelson's published distinction between "virtual" addresses (positions in a particular document) and "invariant" addresses (permanent locations in the permascroll). That vocabulary predates udanax-green. The code is a faithful implementation of a conceptual model that was already articulated before any of this C was written. The two-space architecture did not emerge to solve a specific implementation problem. It was the problem the implementation was designed to encode.
