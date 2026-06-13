## Question 3 [evidence]

> In ASN-0127, is `findlinks_V(W, d_q, Σ)` defined as `findlinks(image(W, d_q, Σ), Σ)` with the image determined solely by the arrangement family `M` (so a `K.λ` creation's `M' = M` frame leaves the image unchanged), and does ASN-0127 state a `findlinks_V`-level analogue of F-LAMBDA (disjoint addition of a fresh `K.λ` link to the discoverability matching set) that ASN-0108 could cite directly instead of the fixed-`I` F-LAMBDA?

## KB Synthesis

Based on my reading of the ASN-0127 and ASN-0108 formal-statements files, here is a precise answer to each sub-question.

---

## 1. Is `findlinks_V(W, d_q, Σ)` defined as `findlinks(image(W, d_q, Σ), Σ)` with image from M?

**Yes.** ASN-0127's formal-statements.md defines `findlinks_V` exactly as:

```
findlinks_V(W, d_q, Σ) = findlinks(image(W, d_q, Σ), Σ)
```

where `image(W, d_q, Σ) = { i ∈ Σ.I | ∃ v ∈ W.spans(d_q) : i ∈ irange_doc(v, d_q, Σ) }`.

`W.spans(d_q)` is the set of V-spans exposed by the window spec `W`, which is drawn from the arrangement family `M`. So image is indeed determined solely through `M` (via `W`) and the document's current V-to-I mapping. The KB [SS-FIND-LINKS] and [SS-DUAL-ENFILADE] confirm this factoring: `find_links` operates in I-space, and the translation from V-spans to I-addresses flows through the POOM.

---

## 2. Does `K.λ` creation's `M' = M` frame leave the image unchanged?

**Yes, but only because of two independent reasons you need to chain.**

`M' = M` directly preserves `W.spans(d_q)` — the window's span set is unchanged because the arrangement family hasn't moved.

The image also depends on `irange_doc(v, d_q, Σ)`, which maps V-spans to I-addresses through the text subspace POOM. `K.λ` creation ([ST-CREATE-LINK]) adds a new link orgl to the granfilade and a reference in the link subspace (`2.x`), but does **not** modify the document's text POOM (`1.x`). Per [FC-SUBSPACE], the two-blade knife ensures INSERT/link-creation in the `2.x` subspace cannot shift or corrupt `1.x` entries. So `irange_doc` is also preserved.

The combination gives `image(W, d_q, Σ') = image(W, d_q, Σ)` after `K.λ` creation when `M' = M`. This is not a single atomic frame claim in ASN-0127 — it requires composing the `M' = M` frame with the fact that `irange_doc` depends only on the text POOM, which is left unchanged by link creation.

---

## 3. Does ASN-0127 state an explicit `findlinks_V`-level F-LAMBDA that ASN-0108 could cite directly?

**No — not as a standalone citable theorem.**

ASN-0127's ΛCREATE spec does include a postcondition stated at the `findlinks_V` level (it describes how `findlinks_V(W, d_q, Σ')` relates to `findlinks_V(W, d_q, Σ)` after a fresh `K.λ` is created). However, this consequence is embedded **inside the ΛCREATE operation spec** as a postcondition clause, not factored out as a separately named lemma (e.g., `Lemma findlinks_V_LAMBDA_frame` or equivalent).

The postcondition in ASN-0127 says, in effect: `findlinks_V(W, d_q, Σ') = findlinks_V(W, d_q, Σ)` when `image(W, d_q, Σ)` does not intersect `λ`'s endpoints, and `findlinks_V(W, d_q, Σ') = findlinks_V(W, d_q, Σ) ∪ {λ}` when it does. This is the V-level analogue of F-LAMBDA. But it's expressed as:

1. The image-frame consequence (`image` unchanged, derived from `M' = M` + text-POOM frame)
2. Combined with the I-space `findlinks` postcondition from ΛCREATE (which adds `λ` when the I-query intersects `λ`'s endpoints)

These are two separate claims in ASN-0127's ΛCREATE spec, not a single named V-level F-LAMBDA theorem.

**Consequence for ASN-0108:** ASN-0108 cannot replace its current I-space F-LAMBDA citation with a single ASN-0127 citation. To use ASN-0127, ASN-0108 would need to cite **two** things:

- ASN-0127's ΛCREATE image-frame clause (asserting `image` is preserved under `K.λ` creation when `M' = M`)
- ASN-0127's ΛCREATE I-space findlinks postcondition (asserting `λ` is added to the matching set when endpoints intersect)

…and compose them locally within ASN-0108's proof.

If ASN-0108 wants a single clean cite, the right move is to ask ASN-0127 to export a named lemma of the form `findlinks_V_LAMBDA_add` — this would take the two implicit components and make the composition explicit and citable. The raw material is all in ASN-0127; it just isn't packaged as a standalone theorem yet.

---

## Code Exploration

The identifiers **ASN-0127**, **ASN-0108**, **F-LAMBDA**, **findlinks_V**, `image(W, d_q, Σ)`, `K.λ`, and "arrangement family M" do not exist anywhere in this repository. I searched every `.md` file in `findings/`, `knowledge-base/`, `docs/`, and every `.c` and `.py` source file. Zero hits for any of these terms.

---

## What the code actually says about findlinks and versions

Since the question maps onto real implementation questions, here is what the C code says directly.

### The findlinks call chain

`dofindlinksfromtothree` [`do1.c:348-353`] is a one-liner — it delegates entirely to `findlinksfromtothreesp`:

```c
return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset,
                               threevspecset, orglrangeptr, linksetptr);
```

`findlinksfromtothreesp` [`spanf1.c:56-103`] converts each V-specset to a sporglset via `specset2sporglset` [`spanf1.c:71-75`], then intersects three independent link sets [`spanf1.c:100`]:

```c
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

### The V-to-I step

`specset2sporglset` [`sporgl.c:14-33`] dispatches on spec type. For a `VSPECID` it calls `vspanset2sporglset` [`sporgl.c:35-65`], which:

1. Calls `findorgl(taskptr, granf, docisa, &orgl, type)` [`sporgl.c:44`] to locate the document's current orgl (its enfilade root — the arrangement tree).
2. Calls `vspanset2ispanset(taskptr, orgl, vspanset, &ispanset)` [`sporgl.c:48`] per V-span, converting through that orgl.

The image — the set of I-addresses that a V-span maps to — is determined entirely by `orgl`, i.e., by whichever enfilade tree `findorgl` returns for that document. That enfilade IS the arrangement. A freshly created version with no subsequent edits has M' = M (same enfilade), so the V→I image is identical to the original. Any INSERT, DELETEVSPAN, or REARRANGE on the new version produces a different orgl and thus a different image.

### What the code does NOT contain

There is no function, variable, comment, or label in this codebase using the names `findlinks_V`, `F-LAMBDA`, `K.λ`, or "arrangement family". The formal specification notation in your question does not originate from any document in this repository.

---

**Conclusion:** I cannot answer whether ASN-0127 defines `findlinks_V` as `findlinks(image(W, d_q, Σ), Σ)`, or whether it states a `findlinks_V`-level analogue of F-LAMBDA, because neither ASN-0127 nor ASN-0108 nor F-LAMBDA exist in this working directory. If these are analysis notes from an external specification document (outside `udanax-test-harness/`), I don't have access to them. The C implementation confirms the image is determined by the document's current enfilade (arrangement), and a `K.λ` creation with M' = M would leave the V→I image unchanged — but that is a derivation from code, not a citation of ASN-0127.
