# Rebase Review of ASN-0036

## REVISE

### Issue 1: S7 derivation summary omits GlobalUniqueness

**ASN-0036, Structural attribution (S7)**: "S7 follows from S7a (document-scoped allocation ensures the document-level prefix identifies the allocating document), S7b (element-level restriction ensures all three identifying fields are present), and T4 (FieldSeparatorConstraint, ASN-0034)."

**Problem**: The summary sentence enumerates three dependencies (S7a, S7b, T4) but the properties table lists four: `from S7a, S7b, T4, GlobalUniqueness (ASN-0034)`. GlobalUniqueness is cited two sentences earlier in the same section ("GlobalUniqueness (ASN-0034) directly guarantees that distinct documents have distinct tumblers, and therefore distinct document-level prefixes") and appears in the properties table, but is absent from the "follows from" enumeration. Without GlobalUniqueness, S7a + S7b + T4 establish that `origin(a)` extracts the allocating document's prefix, but do not guarantee that distinct documents have distinct prefixes — that is, `origin` is well-defined but not shown to be injective over documents.

**Required**: Add GlobalUniqueness to the summary: "S7 follows from S7a …, S7b …, T4 …, and GlobalUniqueness (ASN-0034) (distinct document creations produce distinct prefixes)."

VERDICT: REVISE
