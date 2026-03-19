# Test Cases — Example 1: Total order at the prefix boundary

Source: vault/5-examples/{ASN label}/examples-1.md, Example 1

## TC-001: proper prefix orders before its extension (user → document)
**Property:** T1 case (ii)
**Given:**
```
p = [1, 0, 3]
d = [1, 0, 3, 0, 2]
```
**Assert:** `compare(p, d) == Less`

## TC-002: proper prefix orders before its extension (document → element)
**Property:** T1 case (ii)
**Given:**
```
d  = [1, 0, 3, 0, 2]
e1 = [1, 0, 3, 0, 2, 0, 1, 1]
```
**Assert:** `compare(d, e1) == Less`

## TC-003: divergence at final component determines order
**Property:** T1 case (i)
**Given:**
```
e1 = [1, 0, 3, 0, 2, 0, 1, 1]
e2 = [1, 0, 3, 0, 2, 0, 1, 5]
```
**Assert:** `compare(e1, e2) == Less`

## Skipped
- T2: describes algorithm behavior (components read per comparison), not a computable result from inputs
- T5: universal quantification over all x in interval [e₁, e₂] — requires "for all"