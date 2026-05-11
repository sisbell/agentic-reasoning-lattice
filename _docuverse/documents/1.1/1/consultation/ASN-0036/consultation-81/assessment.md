# Channel Assignment — ASN-0036 review-81

**Date:** 2026-05-11 01:40

```
## Issue 1: OrdAddS8a contract carries a redundant precondition inconsistent with OrdAddHom
Reason: Pure formal consistency issue between two adjacent lemma contracts. The fix is mechanical — adopt one convention (either remove the redundancy with a parenthetical note, matching OrdAddHom's treatment, or restore it to both). Derivable from ActionPoint's contract in ASN-0034, already cited.
```

```
## Issue 2: S7's Well-definedness step uses T4b's projections without explicitly establishing T4-validity
Reason: The bridge from zeros(a) = 3 to T4-validity comes from T10a.4 (T4PreservationUnderDiscipline), which is a foundation postcondition the ASN already depends on via T10a. The fix is to insert the explicit citation and add T10a.4 to the Depends list — entirely internal.
```

```
## Issue 3: S8's contract postcondition asserts subspace preservation under shift but the proof does not address the k ≥ 1 case
Reason: The needed derivation uses only S7b (zeros(aⱼ) = 3), S7c (#E(aⱼ) ≥ 2), and TumblerAdd's prefix-copy rule — all already in the ASN. The fix is to add an explicit one-paragraph geometric derivation locating the action point #aⱼ strictly after the subspace identifier's position.
```

```
## Issue 4: D-CTG-depth's construction at j = m − 1 elides a check on the n bound that uses T0(a)'s exact statement
Reason: Bridging from T0(a)'s "witness exceeding any bound" to "infinitely many values" is a pure foundation argument — iterative application of T0(a), or NAT-wellorder plus injection. Derivable from the addressing-foundation properties already in scope; no design or implementation input needed.
```
