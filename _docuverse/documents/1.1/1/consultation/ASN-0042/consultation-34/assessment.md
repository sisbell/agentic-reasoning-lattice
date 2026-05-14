# Channel Assignment — ASN-0042 review-34

**Date:** 2026-05-14 03:07

```
## Issue 1: O10 summary table missing O18 in derivation
Reason: Bookkeeping correction — O10's proof already explicitly cites O18 (baptismal coupling); the summary table simply needs to reflect the existing derivation. No design or implementation evidence needed.
```

```
## Issue 2: Confusing prose around O18's bootstrap base case
Reason: The fix is an internal restatement to align with O14's actual second clause and to separate the "bootstrap reading" as an explicit posit. No new design intent or implementation evidence required — both O14 and O18 are already stated in the ASN.
```

```
## Issue 3: Compressed derivation in NestingByDelegation
Reason: The fix expands an already-present argument into three explicit sub-cases using only the Prefix relation and condition (ii) of `delegated`. Pure proof-expansion, internal to the ASN.
```

```
## Issue 4: Covering-chain lemma is used implicitly across multiple proofs
Reason: Refactoring/extraction of a lemma already derived from the Prefix (PrefixRelation) definition of ASN-0034. No external evidence needed — the lemma's content is foundational tumbler algebra already imported.
```

```
## Issue 5: Property statements omit reachability while proofs require it
Reason: Audit of formal contracts against existing proof bodies — the reachability convention is already stated in the ASN; the fix is to apply it uniformly. Internal contract-tightening, no expert consultation needed.
```
