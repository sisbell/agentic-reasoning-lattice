# Integration Review of ASN-0034

## REVISE

### Issue 1: Properties Introduced table status mismatch for D1 and D2
**ASN-0034, Properties Introduced table**: D1 status is "introduced", D2 status is "introduced"
**Problem**: The body text labels D1 as "(lemma)" and D2 as "(corollary)". The formal summary correctly marks D2 as "*(corollary of D1 + TA-LC)*". But the Properties Introduced table lists both as "introduced." The existing convention is consistent — T9 is "lemma (from T10a + TA5(a))", T6 is "corollary of T4", TA-LC is "lemma (from ⊕ defn + T3)" — derived properties carry their derivation source in the status column.
**Required**: Change D1's status to `lemma (from ⊕/⊖ defn + T3)` and D2's status to `corollary of D1 + TA-LC` in the Properties Introduced table.

VERDICT: REVISE
