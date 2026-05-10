# Review of ASN-0042

## REVISE

### Issue 1: ω domain in Properties table
**ASN-0042, Properties Introduced table**: "`effectiveOwner : ValidAddress → Principal`"
**Problem**: O2 defines ω only for `a ∈ Σ.alloc` — allocated addresses. The type `ValidAddress → Principal` suggests ω is total over all T4-valid tumblers, which it is not. ValidAddress (T4) includes every well-formed tumbler regardless of allocation status; ω is undefined for non-allocated tumblers. A downstream ASN relying on this table entry could assume totality and apply ω to an unallocated address, where O4 (the existence guarantee feeding O2's well-definedness) does not hold.
**Required**: Restrict the domain to allocated addresses: `effectiveOwner : Σ.alloc → Principal`, or note the precondition `a ∈ Σ.alloc` in the table entry.

### Issue 2: O14 prose/formal mismatch — "allocatable" vs "allocated"
**ASN-0042, State Axioms (O14)**: "The initial state contains at least one principal whose domain covers all initially **allocatable** addresses"
**Problem**: The formal statement quantifies over `Σ₀.alloc` — addresses that ARE allocated in the initial state. The prose says "allocatable," which denotes the (potentially infinite) set of addresses that COULD be allocated under the initial principals' domains. These are different sets. The formal controls, but the prose could mislead a reader into thinking O14 makes a stronger claim about the entire allocatable space.
**Required**: Change "initially allocatable addresses" to "initially allocated addresses" in the prose to match the formal `Σ₀.alloc`.

## OUT_OF_SCOPE

### Topic 1: Fork-to-source content relationship
O10 establishes that a fork creates a new owned address and leaves the original unchanged. The ASN correctly notes the content identity relationship "belongs to the content model, not the ownership model." A future ASN should specify what invariants hold between the fork address and the source address — whether the fork must carry content identity (transclusion), version lineage, or merely an associative link.
**Why out of scope**: O10 is an ownership property (who owns the fork). The content semantics of forking are a separate specification concern.

### Topic 2: Delegation event recording
The open questions ask whether delegation events must be recorded or whether the address hierarchy suffices. This is a genuine future-ASN concern: the structural evidence (prefix nesting) proves that delegation COULD have occurred, but does not distinguish between a delegated sub-account and an undelegated sub-account namespace (both produce the same prefix structure until you check Π). Whether conforming implementations must maintain an audit trail of delegation acts is unresolved.
**Why out of scope**: The ownership model defines the constraints on delegation, not the operational infrastructure around it.

VERDICT: REVISE
