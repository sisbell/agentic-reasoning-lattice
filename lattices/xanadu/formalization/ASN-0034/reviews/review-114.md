# Cross-cutting Review — ASN-0034 (cycle 1)

*2026-04-17 01:05*

Scanning for cross-cutting issues between properties — definitions, precondition chains, and citation conventions.

### NAT-* axioms are stated but never cited; ℕ facts are misattributed to T0

**Foundation**: (foundation ASN — no parent foundations)
**ASN**: ASN-0034 defines five separate axioms for ℕ-level facts (NAT-closure, NAT-order, NAT-discrete, NAT-addcompat, NAT-wellorder) with the stated intent "Each proof cites only the ℕ facts it actually uses" (T0). Yet across every Depends clause that invokes those ℕ facts — ActionPoint, TA-Pos, T1, TA5, TumblerAdd, T10a-N, Prefix, T10, TumblerSub, Divergence, and others — the citation is consistently to T0. For example, T10a-N says *"T0 (CarrierSetDefinition) — the parametric length step rests on four ℕ-level facts that T0 enumerates. First, from `k > 0` in ℕ, T0's discreteness (`m ≤ n < m + 1 ⟹ n = m`, instantiated at `m = 0`) gives `k ≥ 1`... T0's order-compatibility of addition... T0's strict successor inequality `n < n + 1`..."* But T0's own Axiom clause states only "T is the set of all finite sequences over ℕ with length ≥ 1, equipped with length `#· : T → ℕ` ... and component projection"; it does not enumerate discreteness, order-compatibility, strict successor, or well-ordering.
**Issue**: The five NAT-* axioms are defined but zero properties cite them in Depends. Every proof that needs discreteness cites T0's "discreteness axiom", which T0 doesn't contain; every proof that needs well-ordering of ℕ cites T0 rather than NAT-wellorder; every proof that needs order-compatibility cites T0 rather than NAT-addcompat. The separation that T0 explicitly announces is not carried out.
**What needs resolving**: Either the depends clauses across the ASN must be rewritten to cite the appropriate NAT-* axioms for each ℕ fact used (discreteness, well-ordering, order-compatibility, strict successor, additive identity, closure), or T0's axiom must be extended to actually enumerate these facts and the NAT-* axioms removed as redundant. As stated, the NAT-* axioms are orphaned.

### T12 and TA-assoc formal contracts omit Depends clauses

**Foundation**: (internal consistency)
**ASN**: T12 (SpanWellDefinedness) and TA-assoc (AdditionAssociative) each carry a proof that invokes other properties, but their formal contracts list only Preconditions/Definition/Postconditions with no Depends line. T12's proof uses TA0 (endpoint existence), TA-strict (non-emptiness), and T1 (transitivity of ≤ via T1(c)). TA-assoc's proof uses TumblerAdd's piecewise definition, TA0's result-length identity, and T3 for component-wise conclusion. Other theorems in the same ASN (e.g., D0, D1, D2, T10, T10a.5, GlobalUniqueness, TA5, TumblerAdd, PartitionMonotonicity) include explicit Depends.
**Issue**: Inconsistent formal-contract format. Readers who rely on Depends to reconstruct the proof graph will miss the dependencies of T12 and TA-assoc, and downstream reviewers cannot verify precondition chains from the contract alone.
**What needs resolving**: T12 and TA-assoc need Depends clauses enumerating the properties their proofs actually invoke, matching the citation granularity used elsewhere in the ASN.

### Span defined three times with drifting framing (set vs. pair vs. well-formedness predicate)

**Foundation**: (internal consistency)
**ASN**: (1) Vocabulary: *"span(s, ℓ) — set of tumblers in range: {t ∈ T : s ≤ t < s ⊕ ℓ}..."* — span **is a set**. (2) Definition (Span) section: *"A *span* is a pair `(s, ℓ)` where `s ∈ T` is a start address and `ℓ ∈ T` is a length... denoting the contiguous range..."* — span **is a pair that denotes a range**. (3) T12 (SpanWellDefinedness): *"A span `(s, ℓ)` is well-formed when `Pos(ℓ)` and the action point `k` of `ℓ` satisfies `k ≤ #s`..."* — span **is a pair with a well-formedness predicate**. Additionally, Definition (Span) and T12 both carry Preconditions/Definition clauses for `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}` — the two formal contracts duplicate each other, with T12 adding postconditions.
**Issue**: Downstream properties refer to "span" without a single authoritative referent. Is `span(s, ℓ)` a function returning a set (Vocabulary), a pair (Definition), or a pair with a side-condition for well-formedness (T12)? Two separate formal contracts for what should be one concept invite drift under future revision: a precondition added to one will not propagate to the other automatically.
**What needs resolving**: Consolidate to one authoritative definition with one formal contract. If Definition (Span) is meant to introduce the symbol and T12 is meant to prove its properties, their preconditions/definitions should not be separately restated — T12 should cite Definition (Span) and only state its theorem-level postconditions.

### Divergence vs. zpd: T1's trichotomy proof defines the concept informally before Divergence formalizes it, and cyclically

**Foundation**: (internal consistency)
**ASN**: T1's Trichotomy proof (part b) says *"Define the *first divergence position* `k` as the least positive integer at which `a` and `b` disagree — either because `aₖ ≠ bₖ` at some `k ≤ min(m, n)`, or because one tumbler is exhausted at position `k = min(m, n) + 1`..."* — T1 introduces the divergence concept ad hoc in its own proof. Divergence (the named property) later defines this same concept verbatim and cites T3 for exhaustiveness. T1's Depends does not list Divergence (and cannot, since Divergence's own Depends contains T3 which is itself proved from T0 in this ASN; but T1 must also be available because case analyses depend on the ordering). Divergence's Depends lists only T3, not T1 — yet "exactly one case applies" is argued via Divergence equality cases that rely on T3 only.
**Issue**: The "first divergence position" is introduced twice — once informally inside T1's proof, once as Divergence. There's no cross-reference, and a reviser who tightens one definition will not be alerted to update the other. Also, Divergence's Depends claims exhaustiveness rests on T3 alone, but establishing that "no prior divergence exists" implicitly uses the well-ordering of ℕ (minimality of `k`) — same citation gap as Finding 1.
**What needs resolving**: T1's proof should cite Divergence (or vice versa) to make the shared concept explicit, and Divergence's Depends should acknowledge the well-ordering step its minimality argument rests on (whether that attributes to T0 or NAT-wellorder per Finding 1).
