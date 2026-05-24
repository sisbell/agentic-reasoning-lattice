# Review of ASN-0094

## REVISE

### Issue 1: Lemma — RetractionSelfFreshness stated mid-proof
**ASN-0094, Idempotency (Sh4) section, between Case C and Case D**: "**Lemma — RetractionSelfFreshness.** Let Σ be reachable from `Σ_init`..."
**Problem**: The lemma is stated and proved *inside* the Sh4 induction proof (between Case C and Case D), then immediately consumed by Case C's `K ~ R` sub-case (above it!) and Case D. This is a structural inversion: Case C textually precedes the lemma yet uses it. The stratification clause acknowledges this dependency but the text layout creates a forward reference within the proof.
**Required**: Promote RetractionSelfFreshness to a standalone lemma stated and proved before Sh4's induction begins (alongside LinkAddressNotPrefixOfEmit and EffectiveWpSimplification), so Sh4's case analysis cites it without textual inversion.

### Issue 2: Sub-case 3b worked example uses substrate-impossible configurations
**ASN-0094, AllocatedAddressAntichain, Sub-case 3b worked example**: "*Reader's warning: under R0a-Cor2 (a strict strengthening of L1b to `#E(·) = 2`), Sub-case 3b's configuration is structurally impossible on the substrate-conforming layer.*"
**Problem**: The example demonstrates the proof's argument path against a tumbler `a'` of length 9 with `#E(a') = 3` — a configuration the substrate never produces. An illustrative example that cannot occur in any reachable state on the substrate-conforming layer is pedagogically misleading. If the case is vacuous, say it's vacuous and stop; if it's substantive under some weaker substrate, name that substrate.
**Required**: Either replace the example with one reachable on the substrate, remove the worked example for Sub-case 3b entirely (the formal proof's argument suffices), or explicitly scope the example as exhibiting "the proof's logic under L1b alone, where R0a-Cor2 does not hold" — and clarify what hypothetical substrate that names.

### Issue 3: Sh5(b) per-shape uniformity admitted to be aspirational
**ASN-0094, Sh5(b) status paragraph**: "The present draft explicitly downgrades this from a commitment to an *aspiration*: the framework provides no mechanical procedure guaranteeing that two independent drafts registering the same shape will arrive at identical base-template bodies"
**Problem**: This is a substantive weakening that admits two ASN authors could register the same shape with divergent template bodies. The framework's claim to provide a structured predicate vocabulary collapses when bodies are "hand-curated" with no enforcement gate. The Sh5(b) discipline is reduced to citation-checking of symbols, not body-shape convergence.
**Required**: Either (a) commit to a mechanical body-derivation procedure keyed off shape components, (b) demote Sh5 entirely to a non-load-bearing META observation and acknowledge templates are layer-supplied, or (c) provide a documented body-shape derivation procedure as a falsifiable per-row check parallel to step 0 of the minimal review checklist.

### Issue 4: Preservation theorems are "theorems under layer-discipline contracts"
**ASN-0094, Sh4 Status paragraph**: "Sh4 is a *theorem under the Sh4 idempotency contract*, not a substrate-enforced axiom."
**Problem**: Sh4, FDD, and SHCD all preserve their invariants *only if* layers honor specific contracts. If any layer breaks any contract clause, the corresponding theorem fails. The framework's preservation theorems are not substrate guarantees; they are conditional theorems whose antecedents must be checked at every layer registration. The abstract framing "the framework's preservation theorems" obscures this conditionality.
**Required**: Either (a) explicitly tag each preservation theorem in its statement as conditional on the named contract (e.g., "Sh4 (conditional on the *Sh4 idempotency contract*)"), or (b) lift the contracts into Sh-conf at the substrate gate so the theorems become unconditional. The current "theorem under contract" framing is correct but the prose treats them as framework-level guarantees, which they are not.

### Issue 5: ASN-0086's Nullify postcondition is changed; audit-slice multiplicity is lost
**ASN-0094, Nullify Compatibility section**: "ASN-0086's `Nullify` postcondition was specified under the implicit assumption that every well-formed call produces a fresh `(Σ', _)` pair, which is *no longer true* for duplicate bare-form calls under this framework."
**Problem**: The framework modifies ASN-0086's stated contract for duplicate Nullify calls. The NullifyActiveSubsetCompatibility Corollary patches this at the active-subset level but explicitly does not preserve audit-slice multiplicity. This is a substantive interface change that downstream consumers of ASN-0086's Nullify must migrate against. The framework records this as "deliberate" but it amounts to weakening a prior ASN's postcondition.
**Required**: This should be flagged as a *revision to ASN-0086* requiring its own consultation cycle, not an internal commitment of ASN-0094. The Migration discipline (M1-M5) belongs in an ASN-0086 revision, not buried in ASN-0094's Nullify Compatibility section.

### Issue 6: Length and scope sprawl
**ASN-0094, document as a whole**
**Problem**: The ASN exceeds 600KB of prose covering: shape definitions, conformance axiom, four preservation theorems, three per-K disciplines, a template catalog with seven shape rows, eight worked examples, an extensive appendix on NAT primitives, NullifyActiveSubsetCompatibility, SubstrateConsumerActiveSubsetCompatibility, the gate ordering, the migration discipline, and per-walkthrough conventions. Single ASNs in this corpus are typically 1/10th this size. The sheer volume makes verification fragile.
**Required**: Split into multiple ASNs: (a) the core shape framework (Sh-conf, Sh0-Sh4, slot accessors); (b) the template catalog (Sh5); (c) the per-K disciplines (Sh4 contract, FDD, SHCD); (d) the Nullify compatibility revision (as an amendment to ASN-0086); (e) the NAT primitives appendix (as a foundation extension).

### Issue 7: Three Peano supplements introduced in the appendix
**ASN-0094, Appendix: Local NAT Primitives**: "We therefore admit (Peano-pred) as the third added Peano-core axiom of this appendix, alongside (Peano-rec) and (Peano-zero-least)."
**Problem**: NAT-card and NAT-sub derivations require three axioms beyond the listed foundation NAT axioms. These are admittedly standard Peano clauses, but ASN-0094 is consuming them without their being foundation-citable. The appendix derives ℕ-commutativity, ℕ-associativity, successor injectivity, right-identity, and successor-distributivity from these supplements — a sizeable mathematical apparatus that belongs in the foundation, not in a derived ASN.
**Required**: Promote (Peano-rec), (Peano-zero-least), (Peano-pred) and the derived properties (ℕ-commutativity, ℕ-associativity, successor injectivity) to a foundation extension ASN. ASN-0094 should cite them as foundation, not derive them in its own appendix.

### Issue 8: Coverage walkthrough's Rejection case C4 is structurally orthogonal
**ASN-0094, Coverage walkthrough, Rejection case C4**: "By the *single-home commitment* clause (i), the home check `d_other = d_K` fails... so the layer rejects the call outright at its pre-substrate gate"
**Problem**: The walkthrough exercises SHCD's rejection but does not exercise SHCD's *substantive* claim — that `emission_order` is well-defined on `S_d`. The case C1-C3 emissions produce three tuples at the same `d_K`; the walkthrough should verify (not merely assert) that `chain_index(addr(τ_i), d_K) = i-1` for i=1,2,3 by exhibiting that K.λ's deposit addresses match the chain enumeration.
**Required**: Add explicit chain-index verification at C1, C2, C3 — show `addr(τ_1) = [d_K.0.s_L.1]`, `addr(τ_2) = inc(addr(τ_1), 0)`, etc., and confirm `emission_order(τ_i) = i - 1` by direct computation against the substrate's chain enumeration.

## OUT_OF_SCOPE

### Topic 1: Cross-process consistency of shape registry
**Why out of scope**: Multi-process substrate coordination is acknowledged as a scope boundary; extending the framework to multi-process settings would require a distributed protocol outside the current single-process commitment.

### Topic 2: Mechanical body-derivation procedure
**Why out of scope**: The text proposes this as a future sharpening of Sh5(b); the current draft's META status admits this gap explicitly and routes it to future work.

### Topic 3: Ghost-targeting slot semantics
**Why out of scope**: The framework deliberately restricts slot addresses to allocated targets; admitting ghost-targeting under a state-dependent conformance rule is open design work, not a flaw in the current ASN.

META: The ASN attempts to specify state, operations, and invariants abstractly — it remains in spec territory — but the META admissions of Sh5(b), the hand-curated template bodies, and the layer-discipline-contract framing of every preservation theorem suggest the framework is reaching beyond what a single ASN can carry; the work is real but should be partitioned across multiple ASNs to be reviewable.

VERDICT: REVISE
