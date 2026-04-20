# Review of ASN-0002

## REVISE

### Issue 1: AP4 "partition" undefined; derivation from AP4+AP4b to AP2 has an unstated premise

**ASN-0002, The freshness obligation**: "the allocation frontier is maintained *per partition*, but AP2 requires freshness across *all* of dom.ispace. The implication holds only because partitions have structurally disjoint address ranges: AP4b (Partition disjointness)."

**Problem**: The term "partition" in AP4 is never defined. The implementation evidence describes per-document allocation (the allocation function queries "the highest existing address below a computed upper bound" — the upper bound is computed per-document from the tumbler hierarchy). If "partition" means subspace (text or link), then AP4 asserts a single frontier per subspace, but different documents allocate independently within each subspace — a fresh address in document d is above d's per-document frontier but may be below document d''s per-document frontier (hence below the global subspace frontier). Step 1 of the derivation — "a fresh address produced by partition p is above p's frontier, hence disjoint from all existing addresses in p" — is false under the global-frontier interpretation because the fresh address can be below another document's addresses in the same subspace.

The conclusion (AP2) is correct because different documents' address ranges within each subspace are structurally disjoint (guaranteed by the tumbler prefix hierarchy). A fresh address in d's range cannot collide with addresses in d''s range regardless of relative frontier heights. But this per-document range disjointness is never stated as a property.

**Required**: (a) Define "partition" precisely — per-document allocation range within a subspace, not the subspace itself. (b) State per-document range disjointness as a property, e.g.: *AP4c (Within-subspace document disjointness). Distinct documents' allocation ranges within any subspace are disjoint, guaranteed by the tumbler prefix structure.* (c) Revise the derivation: fresh address > document's frontier in its range (AP4), disjoint from other documents in same subspace (AP4c), disjoint from other subspace (AP4b), therefore not in `dom.ispace`.

### Issue 2: Worked example forward-references AP14

**ASN-0002, Worked example, Step 3**: "AP14 holds: `vspace(d)` is unchanged (COPY's target is `d₂`, and `d` is read-only)."

**Problem**: AP14 (Cross-document independence) is introduced in the Cross-document isolation section, two sections after the worked example. The underlying property is already established in COPY's frame conditions ("COPY modifies `vspace(d₂)` (the target) but not `vspace(d₁)` (the source)"), but the label AP14 is used before it is defined. The worked example serves as verification; verifying against an undefined label undermines that purpose.

**Required**: Either (a) move the formal statement of AP14 into the operation-by-operation analysis section (where each operation's frame conditions already state the property informally — AP14 merely names and unifies them), or (b) replace the AP14 citation in Step 3 with the substantive claim from COPY's frame conditions.

## OUT_OF_SCOPE

### Topic 1: Crash recovery and frontier monotonicity
**Why out of scope**: AP4 requires the allocation frontier to never retreat. Whether this survives a crash — where in-memory state may be lost and the frontier must be recovered from persistent data — is a systems-level concern requiring a recovery model. The ASN correctly lists this as an open question.

### Topic 2: Concurrency model for interleaved operations
**Why out of scope**: The ASN treats each operation as an atomic transformation of Σ to Σ'. Concurrent or interleaved operations could violate invariants if not properly serialized. A concurrency model (serializability, isolation levels) belongs in a separate specification.

VERDICT: REVISE
