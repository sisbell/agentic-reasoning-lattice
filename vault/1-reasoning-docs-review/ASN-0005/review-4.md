# Review of ASN-0005

## REVISE

### Issue 1: DEL7 classification not mutually exclusive for empty endsets
**ASN-0005, Ghost links and partial resolution**: "Live in d: `(A a ∈ A : (E q : poom(d).q = a))`" and "Ghost in d: `¬(E a ∈ A, q : poom(d).q = a)`"
**Problem**: For A = ∅, the universal in "live" is vacuously true, and the negated existential in "ghost" is also true (¬false = true). The three categories are intended to partition the space but fail mutual exclusivity for empty endsets. The same issue affects the global classification.
**Required**: Add "A is non-empty" as a premise to DEL7, or reformulate ghost as "not live and not partial." No theorem in the ASN depends on the empty-endset case; this is a minor formal fix.

### Issue 2: poom declared as total function but used as partial
**ASN-0005, The state we need**: "`poom(d) : Pos → Addr`"
**Problem**: The arrow → denotes a total function, but poom(d) is used throughout as partial — `q ∈ dom.poom(d)` appears in the precondition, DEL1's domain definition, DEL7's quantifiers, and the concrete example (where dom.poom(d) shrinks from {1,...,5} to {1,2,3}). The ispace declaration correctly uses ⇀ for partial; poom should match.
**Required**: Change `poom(d) : Pos → Addr` to `poom(d) : Pos ⇀ Addr`.

## OUT_OF_SCOPE

### Topic 1: Concurrent DELETE semantics
**Why out of scope**: The ASN specifies DELETE as a single-operation state transformation. Interleaved V-space modifications, conflict resolution, and serializability under concurrent access are new specification territory.

### Topic 2: Formal UNDO operation
**Why out of scope**: The ASN characterizes reversibility via COPY (DEL11–DEL14) but does not specify an UNDO operation with its own preconditions and journal interaction. This would be new specification, not a correction.

VERDICT: CONVERGED
