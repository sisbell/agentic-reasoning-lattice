## Question 1 [evidence]

> Does ASN-0093 define K.σ/K.α/K.λ as the primitive operations corresponding to ASN-0086's classes (i)/(ii)/(iii), and do K.λ's preconditions impose the sibling-frontier discipline (first emission at d.0.s_L.1, subsequent at inc(ℓ_prev, 0))?

## KB Synthesis

The KB does not contain ASN-0093, nor does it reference the notation K.σ / K.α / K.λ or the "sibling-frontier discipline" by those names. ASN-0086's classes (i)/(ii)/(iii) are likewise not defined in the KB.

The closest related material is [SS-ADDRESS-ALLOC] / [ST-ADDRESS-ALLOC], which documents the query-and-increment allocation mechanism (`findisatoinsertnonmolecule`), the first-child convention (`parent.0.1`), and monotonic increment within a bounded address range — but these are described in implementation terms, not as named algebraic operations K.σ / K.α / K.λ.

This question is not answerable from the KB as provided.

---

## Code Exploration

**The referenced specifications do not exist in this repository.**

I searched the entire working tree — `knowledge-base/`, `findings/`, `docs/`, `bugs/`, and all source files — for:

- `ASN-0093`, `ASN-0086` → **no matches**
- `K.σ`, `K.α`, `K.λ` (and spelled-out variants) → **no matches**
- `sibling-frontier` → **no matches**

The repository uses English-named operations (`INSERT`, `DELETE`, `COPY`, `CREATELINK`, `CREATENEWVERSION`, `REARRANGE`) throughout `kb-formal.md` and `findings/`. There is no formal specification layer that defines operation classes with Greek-letter identifiers or a "sibling-frontier discipline" by that name.

**What I can say from the code:**

There *is* a sibling-ordering concept in the enfilade trees — new entries are inserted as right siblings [`genf.c:419`] and I-address allocation proceeds monotonically [`granf2.c`, per `kb-formal.md:769`] — but this is never formalized as a "K.λ precondition" or "d.0.s_L.1 first-emission rule" anywhere accessible to me.

**Conclusion:** ASN-0093 and ASN-0086 are not documents in this repository. I cannot confirm or deny whether K.σ/K.α/K.λ correspond to any operation classes or whether sibling-frontier preconditions exist in them — those specifications live outside this codebase. I will not speculate on their content.
