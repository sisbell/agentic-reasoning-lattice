## Question 1 [evidence]

> Does udanax-green permit creating a link with an empty to-set (G = ∅) — i.e., does MAKELINK / the link-store path enforce a non-empty target endset, or does it store a link with no targets without complaint?

## KB Synthesis

The KB does not directly answer this question for the case of passing `NOSPECS` (a null/absent to-set) to MAKELINK. The relevant evidence is limited to the zero-width case.

**What the KB does say:**

[PRE-ZERO-WIDTH] and [PRE-LINK-CREATE] (both from Finding 0028) establish that link creation with a **zero-width target span** crashes the backend (Bug 0017). The stated precondition is: `source content exists AND target content exists AND both endpoint widths >= 1`.

[ST-LINK-CREATE] (Finding 0037) shows the call chain for link creation: `domakelink` → `vspanset2sporglset` → `insertendsetsinspanf`. If NOSPECS is passed, `vspanset2sporglset` would receive an empty specset and produce an empty sporglset. Whether `insertendsetsinspanf` with an empty sporglset is accepted, silently ignored, or crashes is not recorded in any finding.

**Conclusion:**

The KB cannot answer whether `NOSPECS` for the to-set is accepted, stored as an empty endset, or crashes — no finding tests that path. For zero-width target spans the answer is a crash. For a fully absent target specset, the behavior is not answerable from the KB as documented.

---

## Code Exploration

Awaiting your approval to write the finding. Here is my full answer based on direct source reading:

---

## Does udanax-green permit MAKELINK with an empty to-set (G = ∅)?

**Yes — completely, silently, and with a success response.**

---

### The Call Chain

**`fns.c:100-112`** — `createlink()` parses with `getcreatelink()` and executes with `docreatelink()`. No validation of the to-set occurs at this level.

**`sporgl.c:18-32`** — `specset2sporglset()` is what converts the wire-parsed `tospecset` into `tosporglset`. Its structure:
```c
*sporglsetptr = NULL;                   // line 18
for (; specset; specset = ...) { ... }  // line 19 — loop body never runs on empty input
*sporglsetptr = NULL;                   // line 30
return (TRUE);                          // line 32 — always TRUE
```
An empty `tospecset` → `tosporglset = NULL`, return `TRUE`. No failure, no error.

**`do1.c:214-219`** — `docreatelink()` passes `tosporglset` straight through with **no guard**:
```c
&& specset2sporglset(taskptr, tospecset, &tosporglset, NOBERTREQUIRED)   // line 215
&& insertendsetsinorgl(..., tosporglset, ...)                            // line 218
&& insertendsetsinspanf(..., tosporglset, ...)                           // line 219
```

**`do2.c:132-133`** — `insertendsetsinorgl()` calls `insertpm(... tosporglset)` **unconditionally** — no NULL check. Contrast with the three-endset at `do2.c:136` which has `if (threevsa && threesporglset)` — an explicit optional guard that from/to lack entirely.

**`orglinks.c:86-133`** — `insertpm()` with `sporglset = NULL`:
- Line 86: guards on `iszerotumbler(vsaptr)` — about the VSA, not the sporglset
- **Line 99**: `logbertmodified(orglisa, user)` — executes **before** the loop; the link orgl is marked modified regardless
- Line 100: `for (; sporglset; ...)` — loop body (and `insertnd`) **never reached** with NULL
- Line 133: `return (TRUE)`

**`spanf1.c:25-53`** — `insertspanf()` with `sporglset = NULL`: identical structure — loop skips, returns `TRUE`.

---

### What Gets Stored

With empty `tospecset`:
1. A new orgl is allocated with a valid link ISA (`createorglingranf`, `do1.c:209`)
2. The link ISA is copied into the document POOM (`docopy`, `do1.c:212`)
3. `logbertmodified()` marks the orgl as modified (`orglinks.c:99`)
4. **Zero `insertnd` calls are made for the to-endset** — neither the POOM nor the spanfilade receives any to-endset data
5. `putcreatelink()` sends success back to the client with the new link ISA

The link is a real stored object. `follow_link` on its to-end returns an empty specset. `find_links` on the to-side never discovers it (no spanfilade entries). The data structures remain consistent — the link is degenerate but not corrupting.

---

### Design Note

The asymmetry between three-endset (explicitly guarded as optional) and from/to endsets (called unconditionally) confirms that from and to were *assumed* always non-empty by design convention — but that assumption is **never enforced**. This is consistent with Finding 0011 (convention-over-enforcement).
