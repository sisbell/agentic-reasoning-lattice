# Review of ASN-0094

## REVISE

### Issue 1: BundledDirectedPair admits `c_G = 0` but the case is unaddressed
**ASN-0094, BundledDirectedPair section and Walkthrough**: The shape `(1, *, A_doc, A_doc, ⊤)` admits emissions with `slot_addrs(G) = ∅` because `match(0, *) = true`. The walkthrough exhibits `|slot_addrs(G)| = 3` and `|slot_addrs(G)| = 1` but never `|slot_addrs(G)| = 0`.
**Problem**: The catalog row's motivating semantics ("bundled dependency-style citation emissions where a single citing document depends on a finite set of cited documents") implies `n ≥ 1`. The empty-G case is formally admissible: what does an "outgoing reference with no targets" mean? Does Sh4 suppression at slot-pair `({a}, ∅)` interact correctly with role semantics?
**Required**: Either (a) introduce a `1..*` cardinality bound and tighten `c_G`, (b) walk through the `n = 0` case explicitly to document admissibility, or (c) reference Retraction's symmetric `c_F = 0` (Nullify-alias) handling and confirm the boundary is intentional.

### Issue 2: AllocatedAddressAntichain Step 3.1 cites an uncited set-theoretic fact
**ASN-0094, AllocatedAddressAntichain Lemma, Step 3.1**: "A finite subset whose cardinality equals the cardinality of its containing set is equal to its containing set: `{n_1, n_2, n_3} ⊆ Z_a ∧ |{n_1, n_2, n_3}| = |Z_a| ⟹ {n_1, n_2, n_3} = Z_a`."
**Problem**: This standard fact is asserted without citation. The surrounding paragraph already cites NAT-card for adjacent reasoning; the subset-equality-by-cardinality principle is load-bearing for closing Case 3 and should be derived with the same rigor.
**Required**: Derive from NAT-card's uniqueness clause (apply the strictly-increasing enumeration of `Z_a` and `{n_1, n_2, n_3}` and conclude equality of enumerations), or cite the foundation property that licenses the inference.

### Issue 3: Tuple-Classifier walkthrough lacks a rejection case
**ASN-0094, Additional Worked Examples, Tuple-Classifier**: The walkthrough exhibits admission only; no rejection.
**Problem**: The Classifier walkthrough's Rejection case 1 (G targeting a tuple address against `t_G = A_doc`) is exactly mirrored by Tuple-Classifier rejection of a document target against `t_G = A_rel`. Omitting the symmetric case weakens the bipartite gate demonstration the catalog explicitly motivates.
**Required**: Add a Tuple-Classifier rejection case where G targets some `d ∈ A_doc^{Σ}`, showing Sh-conf clause (d) failing because `d ∉ A_rel^{Σ}` (by R4, ASN-0086).

### Issue 4: Coverage walkthrough describes the empty-`S_d` path but doesn't exhibit it
**ASN-0094, Coverage walkthrough, "Empty-`S_d` baseline at Σ_0" paragraph**: The walkthrough describes the `latest_K_for_addr(d_subject) = ⊥` case in prose but never exhibits it as a worked computation. The non-empty path is walked through Σ_1–Σ_3.
**Problem**: The framework's claim that `latest_K_for_addr` is partial with `⊥`-dispatch obligation is asserted but the consumer's failure path (e.g., `from₁(latest_K_for_addr(d_subject))` at Σ_0) is not numerically exhibited.
**Required**: Add an explicit "Template evaluation at Σ_0" table showing `latest_K_for_addr(d_subject) = ⊥` and the consumer's required dispatch, parallel to the "Template evaluation at Σ_3" table.

### Issue 5: Sh4 Case D's "by Case B's argument" obscures the chain
**ASN-0094, Sh4 proof, Case D**: "First, by Case B's argument: the *Sh4 idempotency contract* clause (iii) confirmed `C(F_{τ_new}, G_{τ_new}, Σ) = ∅` against the full `A_R^Σ`..."
**Problem**: Case B is structurally restricted to `K ≁ R`; Case D handles `K ~ R`. The contract clause (iii) fires uniformly regardless, but the phrasing "by Case B's argument" suggests Case B is being invoked as a theorem. The dependence is on the *contract*, not on Case B's conclusion.
**Required**: Replace "by Case B's argument" with explicit citation of the *Sh4 idempotency contract* clause (iii), noting that the contract fires uniformly across both `K ≁ R` and `K ~ R` regimes.

### Issue 6: Opt-in registry well-formedness is informal
**ASN-0094, "Per-K opt-in registry is partitioned by base shape" paragraph**: The framework asserts FDD attaches only to DirectedPair and SHCD only to NonIdempotentDirectedPair Coverage; mutual exclusion is enforced by the `idem` flag.
**Problem**: The `idem` flag rules out FDD + SHCD at the same K, but doesn't prevent registering FDD at a shape with `c_F = 0` (e.g., Tuple-Classifier `(0, 1, -, A_rel, ⊤)`). FDD's preservation argument cites `from₁(τ)` and the `K_target_of` template lands in `A_doc^Σ ∪ {⊥}` — neither well-formed when `c_F = 0` or `t_F ≠ A_doc`.
**Required**: State FDD's structural preconditions explicitly (`c_F = 1 ∧ t_F = A_doc`) as part of its Definition, or generalize FDD to admit any `c_F = 1` shape with documented codomain shifts.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate atomicity for Sh4 and FDD contracts
The framework's *Sh4 idempotency contract* and *FDD functional-dependency contract* commit to single-process substrates with within-call sequentiality. Multi-process coordination is a separate scope.
**Why out of scope**: Acknowledged in Open Questions; extending requires a coordination protocol outside the framework's commitments.

### Topic 2: Closure under composition of the template language
Whether composite predicates can express patterns beyond the eleven catalog rows is a property of the composition language, not of the shape framework.
**Why out of scope**: This belongs in a future ASN that defines the composition vocabulary.

### Topic 3: Ghost-targeting slot semantics
Sh-conf clause (d) requires slot addresses to be allocated at emission time. L9 (ASN-0043) permits ghosts in general endsets; extending to slot positions is a future design question.
**Why out of scope**: Flagged in Open Questions; requires a new state-dependent conformance rule.

VERDICT: REVISE
