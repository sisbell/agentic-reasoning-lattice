# Divergences — D15 (OwnerExclusiveModification)

- **Line 16**: predicate(State, DocId) cannot bind the actor (external to the state). Added actor parameter. The predicate is the authorization check that any operation modifying V(d) must satisfy as a precondition.
