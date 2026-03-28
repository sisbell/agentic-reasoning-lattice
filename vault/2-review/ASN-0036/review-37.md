# Review of ASN-0036

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Maximal correspondence run decomposition
**Why out of scope**: S8 proves existence of a finite partition via singletons. Whether a unique maximal decomposition (fewest runs) exists is a separate structural question that the ASN correctly lists as an open question.

### Topic 2: Operation preservation of arrangement contiguity
**Why out of scope**: D-CTG and D-MIN are design constraints on well-formed states. Verifying that each editing operation preserves them is the obligation of operation-specific ASNs, as the ASN correctly notes.

### Topic 3: Orphan discoverability and content store queryability
**Why out of scope**: S6 establishes that orphaned content is permanent. Whether the system must maintain a mechanism to discover such content is an architectural question beyond the two-stream invariants.

VERDICT: CONVERGED
