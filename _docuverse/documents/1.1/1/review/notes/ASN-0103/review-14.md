# Review of ASN-0103

## REVISE

### Issue 1: Strict-advance proof asserts a universal over "any entity" that is only justified for document-level (zeros = 2) entities

**ASN-0103, Effect One, subsequent-case version-dominance**: "Consider any version v baptised under A — any entity with A ≼ v and #v > #A + 2. ... A version is created by a K.δ case-(ii) k=1 fork off a document operand (ASN-0047)..."

**Problem**: The proof equates "version baptised under A" with the bare predicate "any entity with `A ≼ v` and `#v > #A + 2`", then immediately asserts every such entity arose from a `k=1` fork chain off a document — from which it derives `v_{#A+1} = 0` and `v_{#A+2} = i`. But the bare predicate `A ≼ v ∧ #v > #A + 2` does not by itself entail `Document(v)` (zeros = 2), and the `k=1`-fork characterization holds only for zeros = 2 entities. The ASN itself flags exactly this kind of slip elsewhere: in the freshness paragraph it correctly notes that `Account(A')` alone does not pin structure (giving the nesting witness `[N,0,5]` ≼ `[N,0,5,3]`). The same care is needed here. A zeros = 1 entity extending `A` (e.g. an account of the form `[N,0,U,x…]`) would satisfy `A ≼ v ∧ #v > #A + 2` yet have `v_{#A+1} ≠ 0`, falsifying the derivation as literally written.

This is not soundness-breaking — the CND.monotone claim is scoped to *document addresses*, so non-document entities are outside what must be dominated, and freshness against zeros ≠ 2 entities is separately handled by the zero-count argument. But the proof's universal quantifier is stated broader than it is justified, and the load-bearing step ("v is created by a k=1 fork") silently consumes `zeros(v) = 2`.

**Required**: Restrict the quantifier to `Document(v)` (equivalently `zeros(v) = 2`) entities with `A ≼ v ∧ #v > #A + 2`, and add the one-line justification that `Document(v) ∧ A ≼ v ∧ #v > #A + 2` forces the single-`k=2`-off-`A`-plus-`k=1`/`k=0` derivation (no `k=2` step can recur once zeros = 2 is reached, since `k=2` requires `zeros(operand) ≤ 1`). With `Document(v)` in hand the "v is a version" leap is licensed; without it, it is not.

## OUT_OF_SCOPE

(none beyond the topics already declared out of scope, which the ASN correctly defers — forking, content/link allocation, account provisioning, the `ω`-valued ownership statement, and concurrency are all appropriately handled as deferrals or open questions rather than overreached.)

VERDICT: REVISE
