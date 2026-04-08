# Dependency Lint — ASN-0040

Declared depends: [34]


## Uncertain (needs LLM verification)

- UNCERTAIN ASN-0036: uses [S0, S1]

## LLM Verification

## Classification: FLAGGED ASN-0036 — [S0, S1]

### S0 (StreamOrdering)

**LOCAL**

S0 is introduced in ASN-0040 itself. The sibling stream section defines it explicitly:

> **S0 (StreamOrdering).** `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)`.

It appears in ASN-0040's own Properties Introduced table with status "from TA5(a), T1" — meaning it is derived here, not imported. ASN-0036 happens to use the same label, but ASN-0040's S0 is an independent local definition.

### S1 (StreamPrefix)

**LOCAL**

S1 is introduced in ASN-0040 itself. The sibling stream section defines it explicitly:

> **S1 (StreamPrefix).** `(A n : n ≥ 1 : p ≼ cₙ)` — every stream element extends p as a prefix.

It appears in ASN-0040's Properties Introduced table with status "from TA5(b), TA5(c), TA5(d)". Same situation as S0 — locally originated, independent of whatever ASN-0036 defines under the same label.

---

`RESULT: 0 MISSING, 0 COLLISION, 2 LOCAL, 0 CLEAN`
