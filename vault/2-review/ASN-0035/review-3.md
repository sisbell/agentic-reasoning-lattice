# Review of ASN-0035

## REVISE

### Issue 1: BAPTIZE operation signature omits `actor`

**ASN-0035, Baptism section**: "BAPTIZE(p) — Create a new node as a child of p. *Precondition:* `p ∈ Σ.nodes ∧ authorized(actor, p)`"

**Problem**: The operation is parameterized as BAPTIZE(p) — a single argument — but the precondition references `authorized(actor, p)` where `actor` is a free variable. No implicit-parameter convention is declared, and `actor` does not appear in the operation signature. In a specification that aspires to formal rigor (preservation proofs, postconditions with frame conditions), an unbound variable in a precondition is a well-formedness gap.

**Required**: Either (a) parameterize the operation as BAPTIZE(actor, p), making the invoking agent an explicit input, or (b) declare a convention — e.g., "all operations are invoked by an agent `actor`, implicit in the operation context" — that binds the variable for this and future ASNs. Option (a) is cleaner given that N15 makes substantive claims about `authorized`'s permanence properties ("once a subtree is delegated, the recipient's authority over it is irrevocable"), which future account-ontology work will need to formalize against a concrete parameter.

## OUT_OF_SCOPE

None. The ASN stays within its declared scope. The deferred topics (account ontology, document lifecycle, I-space/V-space, replication) are correctly excluded, and no property overreaches into them.

---

**Notes on what this ASN does well.** The N2 derivation is a clean induction on reachable states, correctly using TA5's prefix-preservation (part (b)) to lift `r ≼ p` to `r ≼ n`. The N5 initial-segment property is established by the right argument: first child gets last component 1 from `inc(p, 1)`, subsequent children advance by exactly 1 via `inc(·, 0)`, monotonicity (N4) prevents gaps. The N8 preservation proof correctly partitions invariants into state-dependent (N2–N5, requiring BAPTIZE preservation proofs) and structural (N9, N10, N16, following from the algebra alone), and the implicit argument — that operations not modifying `Σ.nodes` trivially preserve node invariants — is sound. The concrete trace through three BAPTIZE steps verifies all state-dependent invariants at each stage. The freshness argument (`n ∉ pre(Σ.nodes)`) is non-trivially correct: it uses parent-closure (N3(b)) to reduce the question to "is `n` among `children(p)`?", then the sequential-children property to answer no.

VERDICT: REVISE
