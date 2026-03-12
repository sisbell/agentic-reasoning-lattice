# Divergences — D5 (OwnershipRights)

- **Line 11**: Foundation.State lacks publication status and associate lists introduced by ASN-0029. DocState wraps it with these fields.
- **Line 44**: D5 constrains operations, not single states. The four rights (a)-(d) restrict which actors may perform each operation class. As predicate(State, DocId) we express the structural prerequisite: ownership metadata exists and the authorization checks (OwnerExclusive, VisibilityRight) are well-defined for d. Operational enforcement is in D15 (OwnerExclusiveModification).
