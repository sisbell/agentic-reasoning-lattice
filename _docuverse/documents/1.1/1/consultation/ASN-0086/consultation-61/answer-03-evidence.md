## Question 3 [evidence]

> Does ASN-0093's SubspaceConventionAxiom posit `s_C = 1 ∧ s_L = 2`, and is `s_C ≠ s_L` explicitly named as the SC-NEQ consequence in ASN-0093?

## KB Synthesis

Not answerable from the KB.

The KB contains no reference to ASN-0093, a "SubspaceConventionAxiom," or a consequence named "SC-NEQ." The KB does establish that text occupies V-positions `1.x` and links occupy `2.x` [SS-SUBSPACE-CONVENTION], and that these subspaces are independent [FC-SUBSPACE, INV-SUBSPACE-CONVENTION], but nothing about how or whether ASN-0093 formalizes these facts into named axioms or consequences.

---

## Code Exploration

**ASN-0093, SubspaceConventionAxiom, and SC-NEQ do not exist anywhere in this repository.**

A thorough search across `backend/`, `findings/`, `knowledge-base/`, `bugs/`, and all other directories finds no file named `*0093*`, no text matching `ASN-0093`, `SubspaceConventionAxiom`, or `SC-NEQ`. These names are not present in this codebase.

---

**What the code actually says about subspace values:**

The factual content of `s_C = 1 ∧ s_L = 2` is real — it reflects actual code behavior:

- **Content subspace = 1**: `do1.c:394-395` constructs a threshold tumbler at `1.0` and keeps only spans where `stream >= 1.0`. The comment at `do1.c:408` reads: `"Spans with stream < 1.0 are in link subspace — skip them"`. Text is stored at V-positions 1.x.

- **Link subspace = 2**: `do2.c:174-176` (`setlinkvsas`) sets the TO-endpoint V-address by calling `tumblerincrement(tovsaptr, 0, 2, tovsaptr)`, yielding V-position `2.1`. Finding 0038 (backed by `orglinks.c:173-221`) documents that links are internally stored at V-positions 2.x, with `xanadu.h:37` defining `LINKTOSPAN = 2`.

- **s_C ≠ s_L** is a direct arithmetic consequence (1 ≠ 2), but it is never named "SC-NEQ" or labeled as any named consequence anywhere in the source.

---

**Conclusion:** The subspace values `s_C = 1`, `s_L = 2` accurately reflect the C implementation. But "ASN-0093", "SubspaceConventionAxiom", and "SC-NEQ" are labels that do not appear in this repository under any form. They cannot be confirmed or denied as posited by any document here, because no such document exists.
