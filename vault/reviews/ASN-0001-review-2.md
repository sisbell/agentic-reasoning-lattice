# Review of ASN-0001

## REVISE

### Issue 1: Missing axiom for strict increase under addition
**ASN-0001, T12 (Span well-definedness)**: "s ⊕ ℓ > s when ℓ > 0 … (a consequence of TA1 with a = s, b = s ⊕ ℓ)"
**Problem**: The derivation is circular. TA1 says: if a < b then a ⊕ w < b ⊕ w. Instantiating with a = s, b = s ⊕ ℓ requires the premise s < s ⊕ ℓ — which is the conclusion being established. The axioms TA0–TA4 admit a degenerate model where a ⊕ w = a for all a, w (the no-op model): TA0 holds (result is in T), TA1 holds (a < b implies a < b), TA2–TA3 hold symmetrically, TA4 holds (a ⊖ w = a gives (a ⊕ w) ⊖ w = a ⊖ w = a). Every axiom is satisfied, yet spans are empty. The algebra as stated does not exclude this.
**Required**: Either add an axiom — e.g., **(TA-strict)** `(A a ∈ T, w > 0 : a ⊕ w > a)` — or restructure the existing axioms so that strict increase is derivable. Without it, T12's non-emptiness claim is unsupported and every span-dependent argument downstream (content reference, link attachment, POOM tiling) rests on an unproven assumption.

### Issue 2: TA5 under-specified
**ASN-0001, TA5 (Hierarchical increment)**: "when k = 0, the last significant component advances … when k > 0, a new component is introduced k positions deeper"
**Problem**: Three ambiguities. (a) "Last significant component" is undefined. For a tumbler like `[1, 0, 3, 0]`, is the last significant component position 3 (value 3, last nonzero) or position 4 (value 0, last component)? T3 makes these distinct tumblers — `[1, 0, 3, 0]` ≠ `[1, 0, 3]` — so the distinction is load-bearing. (b) For k > 0, the value of the newly introduced component is unstated. Gregory's example shows it becomes 1 (the first child), but the formal statement does not say so. (c) If intermediate positions must be introduced between the current end and the new component (e.g., k = 2 on a tumbler of length 4 produces length 6), the values of those intermediate positions are unstated.
**Required**: Define "last significant component" precisely. State the value assigned to new components at each introduced position. Verify that the specification is consistent with the claim that inc(t, k) > t for all valid t and k.

### Issue 3: Global uniqueness proof omits cross-level case
**ASN-0001, Theorem (Global uniqueness)**: "If they occur in different partitions, T10 guarantees a ≠ b because non-nesting prefixes produce distinct addresses."
**Problem**: T10 requires non-nesting prefixes. But the hierarchy contains nesting allocator relationships: a server (prefix `[1]`) and its user (prefix `[1, 0, 3]`) have nesting prefixes — `[1]` is a prefix of `[1, 0, 3]`. T10 does not apply. The proof covers same-level allocators (siblings with non-nesting prefixes) and misses cross-level allocators (parent-child with nesting prefixes).
**Required**: Add a cross-level case. The argument is straightforward — addresses produced at different hierarchical levels have different numbers of zero-valued components (T4), hence are distinct by T3 — but the proof must state it. Two cases: same level (T10), different levels (T4 + T3).

### Issue 4: Reverse inverse corollary cites wrong property
**ASN-0001, Corollary (Reverse inverse), Case 2**: "TA1 gives y < a ⊖ w (since y ⊕ w < a and subtracting w preserves order)"
**Problem**: The argument subtracts w from both sides of y ⊕ w < a. Subtraction preserving order is TA3, not TA1. TA1 concerns addition. The logic is correct — TA3 applies since both y ⊕ w ≥ w (established by TA4's definedness) and a ≥ w (by hypothesis) — but the cited property is wrong.
**Required**: Replace "TA1" with "TA3" and verify the preconditions of TA3 explicitly (both operands ≥ w).

### Issue 5: Minimality claim is false
**ASN-0001, Formal summary**: "Removing any property breaks a system-level guarantee. This is the minimal algebra."
**Problem**: T6 and T7 are explicitly acknowledged as derived: T6 "follows immediately from T4," and T7 is "a trivial consequence of T3 … and T4." Removing T6 from the property list does not break any guarantee — it remains derivable from T4 and T1. Removing T7 does not break any guarantee — it remains derivable from T3 and T4. The claimed minimality is false for at least these two properties.
**Required**: Either demote T6 and T7 to corollaries (derived properties stated for emphasis, not independent axioms) and remove them from the minimality claim, or demonstrate that each occupies a genuinely independent position in the axiom set. The "Required by" table conflates "this property guarantees X" with "this property is the only thing guaranteeing X."

## DEFER

### Topic 1: Concrete computation model for ⊕ and ⊖
**Why defer**: The ASN deliberately specifies the algebraic contract (order preservation, inverse) without prescribing digit-level computation. The worked example assumes single-component addition reduces to natural-number addition, which is reasonable but unproven. A future ASN should establish at least one concrete model satisfying all axioms (including the strict-increase axiom from Issue 1 once added), verifying that the axioms are satisfiable and not vacuously true over an empty model.

### Topic 2: Crash recovery and allocation monotonicity
**Why defer**: The ASN's open questions already identify this. T9 guarantees monotonicity within a running allocator; what happens after a crash that loses counter state is a durability and recovery question, not an algebraic one.

### Topic 3: Conditions for shift composition
**Why defer**: The ASN explicitly disclaims associativity and lists the composition question ("(a ⊕ w₁) ⊕ w₂ = a ⊕ (w₁ ⊕ w₂)?") as an open question. Whether the system ever needs composed shifts is an operational question for the editing-operations ASN.
