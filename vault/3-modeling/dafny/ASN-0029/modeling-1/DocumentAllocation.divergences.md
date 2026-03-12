# Divergences — D1 (DocumentAllocation)

- **Line 32**: allocated_before(d1, d2) is encoded by parameter ordering convention, not as an explicit temporal relation. The full D1 invariant — that temporal allocation order agrees with tumbler address order — is enforced by the inc mechanism (T10a) being monotone. This predicate captures the structural consequence for a given pair where d1 is known to have been allocated before d2.
