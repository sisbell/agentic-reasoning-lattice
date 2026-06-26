The dependency chain is straightforward: Σ.C → S7b + S7a → S7 → postconditions, with S7d and GlobalUniqueness feeding the uniqueness step. I'll trace S7's well-definedness proof first, then check cross-claim consistency.

**Well-definedness** (S7, fixing `a ∈ dom(Σ.C)`): T4-validity flows correctly — S7a provides `A_element ∈ 𝒯` and `a ∈ dom(A_element)`, T10a.4 instantiates there to yield T4-validity, S7b supplies `zeros(a) = 3`, and T4b's projections become defined. The component map `r` for `origin(a)` is well-typed: field positions carry `ℕ⁺` components from T4b's postcondition, separator positions carry `0 ∈ ℕ` from NAT-zero, total length `p = #N(a) + #U(a) + #D(a) + 2 ≥ 5` satisfies T0's comprehension precondition `p ≥ 1`, and T0's comprehension clause places `origin(a) ∈ T`. The zero-count computation `zeros(origin(a)) = 2` is correct: NAT-card reads the two-element index set `{#N(a)+1, #N(a)+#U(a)+2}` whose members are distinct (difference `#U(a)+1 ≥ 2` from T4a's non-emptiness of U) and lie in `{1,…,p}` (since `#N(a)+#U(a)+2 ≤ p` because `#D(a) ≥ 1`). The strictly-increasing enumeration `1 ↦ #N(a)+1`, `2 ↦ #N(a)+#U(a)+2` witnesses cardinality 2. ✓

**Identification** (S7): S7a asserts the document-level prefix of `a` is the allocating document's tumbler; `origin(a)` is that prefix by construction. The claim that `origin(a)` IS the document's tumbler (not merely identifies it) is grounded in S7a's baptism framing. ✓

**Uniqueness** (S7): S7d's two facts are correctly separated — "distinct documents have distinct events" is event-level; GlobalUniqueness lifts event-distinctness to address-distinctness. The documents are abstract entities whose distinctness is not circular with tumbler-distinctness because S7d's "distinct events" axiom precedes any tumbler comparison. ✓

**Permanence** (S7): S0 preserves `a ∈ dom(Σ'.C)`, and `origin(a)` is a pure function of `a`'s fixed component sequence, so it is state-invariant. ✓

**Dependency coverage**: All thirteen of S7's declared dependencies are consumed in the proof. S0, S7a, S7b, S7d, GlobalUniqueness, T0, T3, T4, T4a, T4b, T10a.4, NAT-card each appear at a specific step. ✓

The proof is sound. Two structural findings follow.

---

### Meta-prose in S7b: use-site inventory belongs in S7, not in the axiom
**Class**: REVISE
**Foundation**: N/A (structural placement error)
**ASN**: S7b (ElementLevelIAddresses) — second paragraph: "We read this domain carefully: T4b carves it out of `dom(N)`… Our axiom supplies only the second conjunct; the first, T4-validity, S7b does not establish, and `zeros(a) = 3` alone does not place `a` in `dom(E)`. That conjunct is discharged downstream, in S7's well-definedness step, where S7a's allocation discipline instantiates T10a.4 (T4PreservationUnderDiscipline, ASN-0034) at `a` to yield `a ∈ dom(N)`. There the two conjuncts meet…"
**Issue**: S7b's claim is the axiom `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`. The second paragraph does not advance that axiom's reasoning — it explains what S7b does NOT establish, names where the missing conjunct is discharged, and describes how the two conjuncts meet inside S7's well-definedness step. That is a use-site inventory of S7's internal proof written from within S7b. The text "That conjunct is discharged downstream, in S7's well-definedness step" and "There the two conjuncts meet" are S7's reasoning relocated into S7b, matching the reviser-drift pattern: prior finding content migrated rather than removed. A precise reader of S7b must skip this paragraph to reach the axiom's own content; a precise reader of S7 finds the proof pre-narrated in S7b before they can read it there.
**What needs resolving**: Remove the second paragraph from S7b. The material about T4-validity being the missing conjunct and the account of how S7 discharges it belongs in S7's well-definedness step, where it is already present and correctly stated.

---

### Meta-prose in S7a: T10a.4 instantiation description belongs in S7, not in the premise-supplier
**Class**: REVISE
**Foundation**: N/A (structural placement error)
**ASN**: S7a (DocumentScopedAllocation) — sentence: "These two memberships are the premises that, in S7's well-definedness step, license T10a.4's preservation invariant — quantified over allocators `A ∈ 𝒯` and domain elements `t ∈ dom(A)` — to be instantiated at `A := A_element, t := a`."
**Issue**: S7a's content is the allocation claim: every `a ∈ dom(Σ.C)` has an element allocator `A_element` with `A_element ∈ 𝒯` and `a ∈ dom(A_element)`, and the document-level prefix of `a` identifies the allocating document. The sentence above does not add to that claim — it describes S7's internal instantiation step, naming S7's proof variable assignments and the quantifier form of T10a.4 that S7 consumes. This is S7a explaining S7's proof from the outside, the same reviser-drift pattern: S7a points at what S7 does with S7a's output, rather than stating what S7a itself asserts.
**What needs resolving**: Remove that sentence from S7a. S7a's second paragraph can end after establishing the two memberships as facts ("`A_element ∈ 𝒯`… and `a ∈ dom(A_element)`"). The account of how S7 instantiates T10a.4 at those memberships is already in S7's well-definedness step and need not be pre-narrated inside the premise.

---

VERDICT: REVISE