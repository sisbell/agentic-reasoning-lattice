# Divergences — O16 (AllocationClosure)

- **Line 13**: allocated_by is modeled as an allocator map (Tumbler → Principal) consistent with O5's SubdivisionAuthority. The map makes the existential witness explicit: every newly allocated address must have an entry mapping to a principal in the pre-state.
