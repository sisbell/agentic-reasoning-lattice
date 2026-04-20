## Open Questions

What constraints must an implementation's representable range satisfy to ensure that no reachable allocation state exceeds the representation — can these constraints be stated as a finite-model property of the abstract algebra?

Must allocation counter durability across crashes be a global-history property or only a per-session property, and what recovery mechanism restores monotonicity after a crash that loses the counter state?

What minimal auxiliary structure must the system maintain to reconstruct version-derivation history, given that it is not decidable from addresses alone (T6(d))?

What must the system guarantee about the zero tumbler's interaction with span arithmetic — if a span endpoint is the zero sentinel, how must containment and intersection operations behave?

Does left cancellation extend to a ⊕ x ≤ a ⊕ y ⟹ x ≤ y (left cancellation for the order)? This would strengthen TA1-strict.

The equivalence-class characterization (TA-MTO converse) suggests that TumblerAdd at action point k is a projection that discards information below level k. Does this projection have useful algebraic properties (idempotence, composition)?
