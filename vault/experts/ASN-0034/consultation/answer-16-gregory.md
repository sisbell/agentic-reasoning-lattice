## Question 16 [gregory]

> The `.0.` digit acting as a hierarchical separator is described as convention, not enforcement — were there ever plans to make the algebra aware of hierarchy (e.g., parent-child ordering guarantees), or is hierarchy purely an interpretation layer above flat digit sequences?

## KB Synthesis

The KB is clear on this: hierarchy is and was always an interpretation layer, not an algebraic property. The evidence points consistently one direction.

**What the algebra knows about hierarchy: nothing.**

The tumbler operations — compare, add, subtract, increment — operate on flat digit sequences. [SS-TUMBLER] Finding 0031 states explicitly: "The zero-separator convention is semantic, not structural — the data type itself does not enforce hierarchy boundaries." `tumblercmp` is a pure lexicographic total order with exponent alignment [INV-TUMBLER-TOTAL-ORDER]. There is no "parent of" or "child of" primitive in the arithmetic layer.

**Hierarchy is imposed from outside the algebra, at two levels:**

1. **Allocator bounds**: `findisatoinsertnonmolecule` enforces containment by computing an upper bound (`tumblerincrement(hintisa, depth-1, 1)`) and bounding its search to the parent's address range [SS-ADDRESS-ALLOC]. The `makehint` function packages a depth integer to pass this information to the allocator [SS-ADDRESS-SPACE]. Hierarchy is injected as a search constraint, not as a type constraint.

2. **Containment predicate**: `tumblertruncate` + `tumblereq` implements "is A under B?" as a derived utility — truncate A to B's length, compare [SS-TUMBLER-CONTAINMENT]. This is a predicate built on top of the algebra, not part of it.

**Was enforcement ever planned?**

There are fragments suggesting it was. `acceptablevsa()` in `do2.c:110-113` always returns `TRUE` — Finding 0049 calls this "a stub that was presumably intended for validation." That's the clearest signal: a validation hook was designed into the architecture but never implemented. Bug 0013 shows that the allocator originally didn't even enforce account containment, requiring a post-hoc fix to add the truncation/comparison check [PRE-ADDRESS-ALLOC].

The two-blade knife in INSERT [SS-TWO-BLADE-KNIFE] is the one place where something like hierarchy-awareness appears in an operation: the second blade is computed as `(N+1).1`, isolating shifts to within a subspace. But this is using the digit-value structure of the address space, not `.0.` boundaries — it's subspace isolation, not hierarchy enforcement.

**Bottom line:** The `.0.` separators were always a docuverse convention layered over flat arithmetic. The algebra was designed to be hierarchy-oblivious — fast, simple, composable. Hierarchy enforcement was supposed to live in the allocation machinery and input validation (`acceptablevsa`), not in the arithmetic itself. The allocator got its enforcement (with the Bug 0013 fix). The input validation never did.

---

## Code Exploration

Zero matches for `isparent`, `isancestor`, `ischild`, or hierarchy predicates of any kind — only the license boilerplate's "contains" phrase.

---

## Full Answer

The question asks whether the `.0.` digit's role as a hierarchical separator was ever planned to be enforced by the algebra itself, or whether it has always been purely an interpretation layer.

The truth is a three-way split, visible in the code:

---

### 1. Core Arithmetic Is Completely Flat (By Design)

`tumblercmp`, `abscmp`, `tumbleradd` (`functiontumbleradd`), `strongsub`, `weaksub`, and `tumblerincrement` — all in `tumble.c` — treat every mantissa slot identically. `abscmp` at `tumble.c:99-108` is the canonical example: it walks the mantissa array left-to-right with `*a++ - *b++`, no zero-special logic anywhere. Comparison, addition, and subtraction are all positional arithmetic over a flat unsigned-integer sequence.

The struct definition (`common.h:59-65`) has no field for depth, level, parent, or hierarchy. The macro `iszerotumbler` (`common.h:72`) only tests `mantissa[0]` — the zero tumbler test, not a "is this a hierarchical separator" test. No constant, macro, enum, or comment in `common.h` or `tumble.c` distinguishes "structural zeros" from "content digits."

---

### 2. The Zero Digit HAS Algebraic Meaning in One Place

`tumbleraccounteq` (`tumble.c:38-70`) is the exception. Its own comment is explicit:

> *"Key insight: When account has a zero, it marks the boundary of the account's address space. The document can have any value there (continuing to sub-addresses). We only check for exact match on non-zero account positions."*

A zero digit in the *account* (right-hand) tumbler is a wildcard: it matches any document digit at that position. Two consecutive zeros terminate the match and return `TRUE`. This is hierarchy-awareness baked into the algebra: account address `1.1.0` will match document address `1.1.0.1`, `1.1.0.1.0.3`, etc.

This function is load-bearing in `do1.c:270` for `docreatenewversion`: whether the new version goes under your own account (DOCUMENT→DOCUMENT, depth=1) or under another's account (ACCOUNT→DOCUMENT, depth=2) depends on `tumbleraccounteq` returning the right answer.

---

### 3. Hierarchy Is Constructed by Address Generation via `depth`

The `.0.` gap itself is produced in `granf2.c:209` (`findisatoinsertnonmolecule`):

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

When the object being created is a *different type* than its container (e.g., an ACCOUNT creating a DOCUMENT, or a DOCUMENT creating an ATOM), `depth=2`. This means `tumblerincrement` writes at `last_occupied_slot + 2`, leaving slot `last_occupied_slot + 1` as zero. That gap IS the `.0.` separator.

When creating a same-type object (DOCUMENT creating DOCUMENT = versioning), `depth=1` — no gap, a flat increment.

The convention comment at `granf2.c:219-227` is explicit about this being convention-by-construction:

> *"BUG FIX #1: If nothing exists under the hint (lowerbound is zero after findpreviousisagr), create the first child address as hintisa.0.1. The original code would produce just '1' due to truncate/increment on a zero tumbler, causing the first document to get the wrong address."*

The bug being fixed was that the first document under an account was *not* getting the `.0.` separator — the fix explicitly enforces the convention. But this enforcement lives in `granf2.c` (address generation), not in `tumble.c` (arithmetic).

---

### 4. Hierarchy-Manipulation Primitives Exist but Are Not Used Broadly

`prefixtumbler` (`tumble.c:641-651`) prepends a digit, wrapping an address into a sub-namespace. `beheadtumbler` (`tumble.c:673-683`) removes the first digit, stepping up. `docidandvstream2tumbler` (`tumble.c:685-699`) explicitly concatenates a document ISA with a V-stream address by appending after the last non-zero digit (creating the `docid.0.vstream` structure).

These functions exist in the arithmetic layer, not the address-generation layer. They are hierarchy-aware primitives. But they are narrow in scope: `prefixtumbler` appears to be unused in the live call graph, `beheadtumbler` is used only in the (ifdef'd-out) old `abscmp` branch. `docidandvstream2tumbler` is present but I found no callers in the current codebase. They read like primitives that were built in anticipation of operations that were never fully wired up.

---

### 5. Domain Subspace Interpretation Is Pure Convention

`istextcrum` and `islinkcrum` in `orglinks.c:246-261` read specific mantissa slots to classify crums:

```c
bool istextcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[1] == 0 && is1story(...)) { return TRUE; }
```

```c
bool islinkcrum(typecorecrum *crumptr)
{
    if(...mantissa[0] == 1 && ...mantissa[1] != 0){  /* if the tumbler is a 1.n tumbler where n!= 0 */
```

The inline comment says it directly: this is "if the tumbler is a 1.n tumbler where n!= 0." The algebra never established that `mantissa[1]` means "this is in link space" — this is the application layer reading positional conventions back out. The arithmetic has no concept of "link space" vs. "text space."

Similarly, `findvsatoappend` in `orglinks.c:37` creates `linkspacevstart` as tumbler `2.0` (literally `tumblerincrement(..., 0, 2, ...)`) and uses `tumblercmp` against it to decide whether to append in text or link territory. This is a numeric boundary comparison that happens to correspond to the `.0.` convention — the algebra doesn't "know" it's a domain boundary.

---

### The Naming Tells You the Intended Mental Model

`nstories` and `is1story` (`tumble.c:249-247`) are the most revealing function names in the codebase. "Stories" = floors of a building. The designers were explicitly thinking in spatial/hierarchical terms. `nstories` counts occupied mantissa positions; a "1-story" tumbler has only one significant digit. But this naming maps hierarchical intuition onto a count of flat array positions — the hierarchy is a metaphor for the digit depth, not an enforced structural property.

---

### Summary: The Architecture as Built

| Layer | Hierarchy Awareness | Evidence |
|---|---|---|
| Core arithmetic (`tumblercmp`, `tumbleradd`, etc.) | None | `abscmp` walks mantissa uniformly, `tumble.c:99-108` |
| Account matching (`tumbleraccounteq`) | Partial — zero is a wildcard | `tumble.c:47-62` comment; zero-termination protocol |
| Hierarchy-manipulation primitives (`prefixtumbler`, `beheadtumbler`) | Yes — explicit | `tumble.c:641-683`; but narrow scope, limited callers |
| Address generation (`findisatoinsertnonmolecule`) | Yes — `depth` encodes level | `granf2.c:209`; `depth=2` produces the `.0.` gap |
| Domain interpretation (`istextcrum`, `islinkcrum`) | Pure convention | `orglinks.c:246-261`; reads `mantissa[1]` by position |

**The design is deliberate, not accidental.** The arithmetic layer is kept flat so that span arithmetic, retrieval, and comparison are O(NPLACES) simple operations with no parsing of semantic structure. Hierarchy is "enforced" through two mechanisms: (a) `tumbleraccounteq`'s zero-wildcard semantics for ownership, and (b) the `depth` parameter in address generation which produces the `.0.` pattern by construction. There are no parent-child ordering guarantees from comparison, no hierarchy predicates, and no structural enforcement that a zero at any given position is "the separator" rather than an ordinary digit.

The question of whether hierarchy was ever planned to be more deeply embedded in the algebra probably has this answer: the primitives (`prefixtumbler`, `beheadtumbler`, `docidandvstream2tumbler`) were built to support it, but the usage never materialized. The real work is done by `tumbleraccounteq` (zero-as-boundary) and the address-generation layer. Everything else is convention that the algebra happens to respect by the accident of lexicographic ordering — `1.0.2 < 1.1 < 1.1.0.1` by pure arithmetic, which also happens to be the correct hierarchical ordering.
