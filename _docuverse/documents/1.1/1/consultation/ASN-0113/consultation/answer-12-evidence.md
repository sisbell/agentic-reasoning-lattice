## Question 12 [evidence]

> The KB states the text subspace VSpec reports width in characters while links live internally at `2.x` but are normalized to `0.x` in output — does the returned link VSpec's start tumbler use the `0.x` form, and is its width measured in number-of-links or in I-space byte extent?

## KB Synthesis

## Link VSpec: Start Tumbler Form and Width Semantics

### Start Tumbler: Context-Dependent Normalization

The output form depends on document content composition, per [SS-DUAL-ENFILADE] Finding 0038 and [SS-VSPAN-VS-VSPANSET] Finding 0035:

- **Mixed document (text + links):** links are normalized to `0` (or `0.x`) in `retrievedocvspanset` output — the `retrievevspansetpm()` function zeroes `mantissa[1]` for the link span
- **Links-only document (no text):** links are reported at their actual internal V-position `2.x` (e.g., `{"start": "2.1", "width": "0.1"}`)

The internal representation is always `2.x`; `0.x` is a presentation artifact of `retrievevspansetpm()` when text is also present [FC-SUBSPACE].

### Width: V-Space Extent, Equal to Link Count

The width is **not** I-space byte extent. Each link orgl ISA occupies exactly one V-space unit in the `2.x` subspace. Links are placed sequentially at `2.1`, `2.2`, `2.3`, ... by `findnextlinkvsa` [SS-LINK-SUBSPACE]. Therefore:

- 1 link → `width: "0.1"`
- 3 links → `width: "0.3"`

This means width numerically equals link count. The ISA tumbler itself (e.g., `1.1.0.1.0.1.0.2.1`) is what the V-position maps to in I-space — but the V-space width measures positions in the `2.x` enumeration, not bytes of that ISA [SS-ADDRESS-SPACE] Finding 0024, [SS-POOM-BOTTOM-CRUM].

---

## Code Exploration

Now I have all the pieces. Let me synthesize the full picture from the code.

## Answer

The KB claim about `0.x` normalization is based on empirical observation that I need to correct against the actual code. Here is what the source establishes, with citations.

---

### Background: where links are stored internally

Links are placed in V-space at position `2.x` within a document's POOM. `findnextlinkvsa` in `do2.c:151–167` sets the first link VSA:

```c
tumblerincrement (&firstlink, 0, 2, &firstlink);  // mantissa[0]=2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // mantissa[1]=1 → firstlink = 2.1
```

`islinkcrum` in `orglinks.c:255–261` confirms this by identifying link crums as those with `cdsp.dsas[V].mantissa[0] == 1 && mantissa[1] != 0`. (Note: this is the *relative* displacement within the tree; the absolute position of these crums is in the 2.x range because they are offset from the root's grasp of ~1.1.)

`setlinkvsas` in `do2.c:169–183` places the three link endpoint sub-subspaces at `1.1`, `2.1`, `3.1` **within the link orgl itself** (FROM/TO/THREE end-sets). This is separate from the link reference stored in the home document.

---

### What `retrievedocvspanset` actually returns

`doretrievedocvspanset` → `retrievevspansetpm` (`orglinks.c:173–221`) branches on `is1story(&ccptr->cwid.dsas[V])`.

**Case A — document has only links, no text** (`is1story` = TRUE, because cwid_V = `0.1` = exp=−1, mantissa[0]=1):

```c
// orglinks.c:185–190
movetumbler (&ccptr->cdsp.dsas[V], &vspan.stream);   // actual V-address: e.g. 2.1
movetumbler (&ccptr->cwid.dsas[V], &vspan.width);    // e.g. 0.1 for 1 link
```

Output: `[{"start": "2.1", "width": "0.1"}]`. The start IS in `2.x` form.

**Case B — document has both text and links** (`is1story` = FALSE, because cwid_V = `1.m` for some m):

After text insertion and link insertion, `setwispnd` (`wisp.c:171–228`) computes the root's cwid by taking `lockmax` over all children's `(cdsp + cwid)`. A link child at absolute V=2.1 with cwid=0.1 contributes a `tempwid_V = 1.2` (after `dspsub` makes its relative cdsp `1.1`). Text contributes `tempwid_V = 0.10`. Result: `cwid.dsas[V] = 1.2` (mantissa[0]=1, mantissa[1]=2).

Then `retrievevspansetpm` computes two spans:

**The `linkvspan` (named for links, derived from cwid):**

```c
// orglinks.c:196–203
movetumbler (&ccptr->cwid.dsas[V], &linkvspan.stream);  // cwid = 1.2
linkvspan.stream.mantissa[1] = 0;                        // → 1.0
tumblerjustify(&linkvspan.stream);                       // mantissa[0]=1≠0, no change

movetumbler (&ccptr->cwid.dsas[V], &linkvspan.width);   // same
linkvspan.width.mantissa[1] = 0;
tumblerjustify(&linkvspan.width);
```

After zeroing mantissa[1]: `1.0` (exp=0, mantissa[0]=1, mantissa[1]=0). `puttumbler` outputs `0.1~`. Python `Tumbler_read` decodes that as `[1]` → `"1"`. Both stream and width = `"1"`.

**The `vspan` (named for text, derived from `maxtextwid`):**

```c
// orglinks.c:207–212
tumblerclear (&vspan.stream);           // zero tumbler → "0"
movetumbler (&maxwid, &vspan.width);    // maxwid e.g. 1.1
vspan.width.mantissa[0] = 0;           // → (exp=0, m[0]=0, m[1]=1)
```

`puttumbler` outputs `0.0.1~`. Python decodes as `[0,1]` → `"0.1"`.

After `putvspaninlist` sorts by stream: `[{"start":"0","width":"0.1"}, {"start":"1","width":"1"}]`.

---

### Resolving the KB claim

The KB states "links are normalized to `0.x` in output." Finding 0038 labels the `start="0"` entry as "links." **This labeling is incorrect.**

From the code:
- `start="0"` comes from `vspan` (the *text-derived* variable), computed via `maxtextwid` with `mantissa[0]` zeroed. Its width (`"0.1"` for "ABC" text, `"0.4"` after "AXXBC") tracks the **maximum absolute V-position of text crums**, not link count.
- `start="1"` comes from `linkvspan` (the *link-named* variable), computed from cwid with `mantissa[1]` zeroed. This boundary covers V-range [1, 2), which is the **text subspace**. It is stable regardless of how many links are added.

This is confirmed by `filter_vspanset_to_text_subspace` (`do1.c:386–410`), which **keeps** spans with `stream >= 1` for use in `compare_versions`. V-range [1, 2) contains text characters (1.x positions), so keeping `start="1"` correctly selects text content.

---

### Q1: Does the link VSpan start tumbler use `0.x` form?

**No.** When a document has both text and links, the span associated with link-position information (the `linkvspan` variable) has `start="1"` — a single-digit tumbler (exp=0, mantissa[0]=1). This represents the major-unit boundary of the text subspace, not `0.x`.

When a document has **only links** (no text), `retrievevspansetpm` takes the `is1story` branch and returns `start="2.1"` (or "2.2", etc.) — the actual internal 2.x form.

The `"0"` (zero tumbler) that appears at `start="0"` in the mixed-content output is the **text-derived** span, not the link span.

### Q2: Is the width measured in number-of-links or I-space byte extent?

**Neither directly.** The width depends on the case:

- **Only-links case** (`orglinks.c:170–172`): width = `cwid.dsas[V]` directly. The cwid for a link crum is computed by `insertpm` as `tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V])` where `inc = tumblerintdiff(lwidth, 0)` = the integer count of link endpoints (`insertpm`, `orglinks.c:115–117`). So `width = "0.n"` where **n = number of link endpoints** stored there. One link → `"0.1"`.

- **Mixed text+links case**: The `linkvspan.width = "1"` (derived from cwid's major digit) is the V-extent of the text subspace boundary — **not** a link count. The `vspan.width = "0.n"` is the V-sub-position of the last text crum — also not a link count.

So the width `"0.n"` meaning "n links" holds only in the only-links case where `retrievevspanpm`/`retrievevspansetpm` returns the raw cwid. Once text is also present, the width encoding changes entirely.

---

### Summary

| Condition | Start tumbler | Width | Code path |
|---|---|---|---|
| Only links | `"2.1"` (actual 2.x) | `"0.n"` where n = link count | `orglinks.c:165–172` simple branch |
| Text + links, link-named span | `"1"` (boundary of text subspace) | `"1"` (one major unit) | `orglinks.c:195–203` |
| Text + links, text-named span | `"0"` (zero tumbler) | `"0.n"` tracking last text V-position | `orglinks.c:207–212` |

The KB's `"0.x"` normalization claim is not supported by the code. Links stored internally at `2.x` do appear as `"2.1"` etc. when retrieved alone. In the mixed case, neither output span directly encodes link count or link V-position — the cwid arithmetic collapses both into a boundary value.
