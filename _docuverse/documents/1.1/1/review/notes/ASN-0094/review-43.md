# Review of ASN-0094

## REVISE

### Issue 1: AllocatedAddressAntichain Sub-case 3b discharged "by symmetry"
**ASN-0094, AllocatedAddressAntichain proof, Step 3.3b**: "By symmetry (Sub-case 3b: `x ∈ dom(Σ.C), a ∈ dom(Σ.L)`). The argument swaps the side labels of Sub-case 3a... Sub-case 3b vacuous by the Case-symmetry argument above."
**Problem**: The proof claims symmetry between the two sub-cases but does not walk Step 3.3b under the side-label swap. The "Case-symmetry across Sub-cases 3a and 3b" preamble argues the steps are sub-case-independent, but the actual subspace-contradiction step (3.3) differs in which side carries which identifier. A concrete numerical example is provided in the worked walkthrough, but the formal proof step is not explicitly stated.
**Required**: Walk Step 3.3b explicitly under the side-label swap, mirroring the structure of Step 3.3a. The framework already exhibits the swap concretely; promoting that exhibition into the proof body would close the "by symmetry" gap.

### Issue 2: NAT-card and NAT-sub appendix invokes background facts not in the foundation
**ASN-0094, Appendix: Local NAT Primitives**: "Two facts about ℕ-arithmetic invoked in the NAT-sub derivation are not literally enumerated among the foundation's listed NAT axioms: (1) ℕ-commutativity of addition... and (2) ℕ-associativity of addition..."
**Problem**: The framework acknowledges these as background facts but the appendix's derivations of NAT-card and NAT-sub depend on them. NAT-sub's Case A existence step requires commutativity (`m + 0 = 0 + m = m`); the uniqueness step requires associativity (`n + (p_1 + 1) = (n + p_1) + 1`). The foundation list does not enumerate these. Downstream proofs (AllocatedAddressAntichain Step 3.1, LinkAddressNotPrefixOfEmit Step II.0/II.1) consume NAT-card/NAT-sub and inherit the dependency.
**Required**: Either derive ℕ-commutativity and ℕ-associativity from the listed NAT axioms (NAT-closure, NAT-order, NAT-discrete, NAT-addcompat, NAT-wellorder), or add them explicitly to the foundation. The current "background ℕ-arithmetic facts" framing leaves a small but real gap.

### Issue 3: Sh5 body-shape-level uniformity enforced only by hand-review
**ASN-0094, Sh5(a) Status of per-shape uniformity**: "The framework provides no mechanical procedure guaranteeing that two independent drafts registering the same shape will arrive at identical base-template bodies... auditor-side review is what enforces convergence at the body-shape level."
**Problem**: Sh5(b)'s mechanical falsifiability operates on the citation-side discipline (every cited data symbol within categories (i)–(iv)) but does not constrain body-shape convergence between shape-mates. A divergent body would pass the literal name-citation check but violate uniformity. The framework acknowledges this as the cost of META status; a strict review notes that "auditor hand-review" is exactly the kind of informal gate Dijkstra warns against.
**Required**: Either tighten the discipline into a procedural recipe (a documented difference table, or a body-shape derivation procedure from shape components), or explicitly demote per-shape uniformity from a commitment to an aspiration. The current language commits to uniformity without a mechanical enforcement path.

### Issue 4: Document size and prose redundancy impede review
**ASN-0094, throughout**: Gate Ordering is stated in Sh-conf, restated in Sh4's contract section, restated in FDD's section, restated in SHCD's section; the "Convention for per-walkthrough registered-catalog declarations" is invoked in every walkthrough; scope clarifications are repeated across multiple sections.
**Problem**: The document is significantly longer than necessary. Reviewers and downstream consumers must repeatedly re-read essentially identical material. While not a correctness issue, the redundancy makes it hard to verify that all instances stay synchronized — a discipline drift in one restatement could go unnoticed.
**Required**: Consolidate Gate Ordering into a single canonical statement; replace per-section restatements with citations. Same for per-walkthrough scaffolding and scope clarifications.

### Issue 5: Sh5 audit-table extension lacks a procedural commitment
**ASN-0094, Sh5(b) Status of the audit table**: "The framework does not commit a procedure for extending the table: there is no documented review checklist, no decision-record format, no auditor role with a stable interface, and no process specification for adding a row."
**Problem**: The framework defers catalog extension to "manual editorial activity on this document" without specifying who/when/how. This means a downstream consumer adding a row has no guidance on what constitutes acceptance. The mechanical falsifiability is preserved per-row, but the entry path is unspecified.
**Required**: Either commit to a minimal review checklist (e.g., "symbol-by-symbol classification against the four categories, with the result inlined into the row's audit cell"), or explicitly downgrade the catalog from "extensible" to "fixed at this draft, extensions require a new ASN."

## OUT_OF_SCOPE

### Topic 1: Cross-process atomicity for Sh4/FDD contracts
**Why out of scope**: Already flagged in Open Questions as a scope boundary. The framework commits to single-process substrate scope and notes that multi-process extension would require a coordination protocol outside the current framework.

### Topic 2: Composite predicate closure theorem
**Why out of scope**: Already flagged in Consequences (b) and Open Questions. Whether composition of atomic templates expresses predicates beyond the catalog is a property of the composition language adopted, not a structural guarantee of Sh5.

### Topic 3: Ghost-targeting slot semantics
**Why out of scope**: Already flagged as an open design question. The framework forbids ghost addresses in slot positions; admitting them would require a new shape family with state-dependent conformance rules.

### Topic 4: Higher-arity link shapes
**Why out of scope**: Already flagged as a scope boundary in "Arity scope" at the framework's introduction. The framework restricts to standard-triple (arity 3) links; higher-arity shapes would require additional shape components per extra slot.

VERDICT: REVISE
