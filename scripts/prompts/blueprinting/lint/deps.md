# Missing Dependency Check

A deterministic label scan flagged potential missing dependencies for this ASN. Some may be real, some may be false positives. Your job is to classify each one.

## ASN Under Review

**{{asn_label}}**
**Declared depends**: {{depends}}

{{asn_content}}

## Declared Dependency Exports

These are the exports from the ASN's declared dependencies. Use them to determine whether a flagged label is a collision with a label defined here.

{{declared_exports}}

## Flagged Issues

{{findings}}

## Task

For each flagged issue, classify it as one of:

1. **MISSING** — The ASN uses this claim and it is NOT defined in any declared dependency export or locally. The dependency on the original source should be added. Transitive dependencies are not allowed — if you use a claim, you must depend on the ASN that originates it.
2. **COLLISION** — The label matches a claim in the flagged source, but the declared dependency exports define a different claim with the same label that the ASN is actually using. Not a real issue.
3. **LOCAL** — The ASN defines this label locally (status "introduced" in its claims table). The label happens to match one in the flagged source but they are independent claims. Not a real issue.
4. **CLEAN** — The deterministic scan matched the label text, but the ASN does not actually use this claim. The label appears in a non-referential context (e.g., a comment, example, or unrelated mention).

## Output

For each flagged source ASN, list every label with its classification. Be specific — for MISSING, say where in the ASN the claim is used. For COLLISION, say which declared dependency provides the label. For CLEAN, say why it's not a real reference.

End with a summary line: `RESULT: N MISSING, N COLLISION, N LOCAL, N CLEAN`
