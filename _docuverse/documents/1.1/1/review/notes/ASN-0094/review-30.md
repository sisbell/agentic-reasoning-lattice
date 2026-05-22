# Review of ASN-0094

## REVISE

### Issue 1: Direct ASN-0093 citations
**ASN-0094, multiple sections**: The ASN cites ASN-0093 by number in several places:
- "*(c) ASN-0093 substrate invariants:* M0, M1, C0, C1, C1b, C1c, C-fin" (SubstrateConformingLayer Definition)
- "ChainMembershipForOrigin (ASN-0093)" (Lemma RetractionTargetNotOnChain Step II.1 / Case II)
- "ASN-0093 L0 (SubspacePartition)" (SharedDepthOneAllocator clause (c) and elsewhere)
- "via ASN-0093's class-decomposition of `↦`"
- "ASN-0093's structural chain"

**Problem**: Per standard 7, references to non-foundation ASNs should be flagged. The review foundations are ASN-0034, ASN-0043, ASN-0086 only — ASN-0093 is not in scope.

**Required**: Reframe these citations as consumption through ASN-0086's SubstrateConformingLayer Definition (the foundation interface that already catalogs this content). The framework's *Scope and Substrate Scaffolding* section already names the relevant clauses; proofs and definitions should cite those scaffolding names rather than dereferencing to ASN-0093 directly.

### Issue 2: Sh2/Sh3 stratification implicit on Sh0/Sh1
**ASN-0094, Target Domain section**: The Sh2 proof's universal `(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: slot_addrs(F) ⊆ shape(K).t_F^Σ)` presupposes `slot_addrs(F)` is well-defined for every τ ∈ L_K^Σ at every reachable Σ. The proof cites Sh-conf clause (d) at emission and R2 for preservation, but `slot_addrs` well-formedness across `↦*` is Sh0's conclusion — not separately established by Sh2's proof.

**Problem**: The stratification claim ("Sh0–Sh3 are each proved by their own independent inductions ... not part of Sh4's inductive hypothesis") is correct at the level of inductive scaffolding, but Sh2/Sh3 implicitly consume Sh0/Sh1 because `slot_addrs(·)` is only defined on canonical-slot endsets. The proofs do not cite this dependency explicitly.

**Required**: Either (a) make the dependence explicit ("by Sh0, every τ ∈ L_K^Σ has canonical-slot F, so `slot_addrs(F)` is well-defined") or (b) merge Sh0+Sh2 and Sh1+Sh3 into combined inductions covering canonical-form and target-domain together.

### Issue 3: AllocatedAddressAntichain Step 3.1 — proof structure
**ASN-0094, AllocatedAddressAntichain Lemma, Step 3.1**: The argument that `a`'s three zero positions equal `b`'s `{n_1, n_2, n_3}` proceeds by case-split on a hypothetical extra zero `m`, dispatching on `m ≤ #x` vs `m > #x` to derive contradictions with `zeros(x) = 3` and `zeros(a) = 3`.

**Problem**: The case dispatch is sound but unnecessarily complex. The forward derivation is straightforward: componentwise agreement at positions `1..#x` lifts `Z_x = {n_1, n_2, n_3}` to `{n_1, n_2, n_3} ⊆ Z_a`; cardinality `|Z_a| = 3` then forces equality. The current proof's two-case contradiction structure adds bookkeeping that obscures the simpler argument.

**Required**: Replace the case-split with a forward derivation: from `{n_1, n_2, n_3} ⊆ Z_a` and `|Z_a| = zeros(a) = 3 = |{n_1, n_2, n_3}|` (finite-set cardinality + subset relation), conclude `Z_a = {n_1, n_2, n_3}`.

### Issue 4: Lemma RetractionTargetNotOnChain — `home(a_emit(Σ, d))` evaluated outside `dom(Σ.L)`
**ASN-0094, Lemma RetractionTargetNotOnChain Step II.3**: "By L1a, `home(b) = N(b).0.U(b).0.D(b) = N(a).0.U(a).0.D(a) = home(a)`"

**Problem**: L1a is an invariant *over* `dom(Σ.L)`, but `a = a_emit(Σ, d)` is the fresh address K.λ *would* emit — not in `dom(Σ.L)` at state Σ. The function `home(·)` defined by the formula `N(·).0.U(·).0.D(·)` is well-defined on any T4-valid address with `zeros = 3` (T4b makes N, U, D total under that constraint), but citing "L1a" for this fact conflates the *function definition* with the *invariant content*. The framework needs to make this explicit.

**Required**: Either (a) note that `home(·)`, as a projection defined by `N(·).0.U(·).0.D(·)`, is well-formed on every T4-valid address with `zeros = 3` (independent of `dom(Σ.L)` membership), and cite T4b for the projection well-definedness; or (b) introduce a separate Definition naming `home : {t ∈ T : T4-valid(t) ∧ zeros(t) = 3} → T` and cite that Definition instead of L1a at this proof site.

### Issue 5: ASN-0086 Nullify backwards-compatibility — audit-slice multiplicity loss is buried
**ASN-0094, Nullify Compatibility section**: The framework extends `Emit_K`'s return type from `Σ' × A_rel^{Σ'}` to `(Σ' × A_rel^{Σ'}) ∪ {⊥}` and adopts set-semantics for the Retraction relation via Sh4 with `idem = ⊤`. NullifyActiveSubsetCompatibility establishes that *active-subset content* is preserved across the `⊥`-branch, but audit-slice multiplicity is not — duplicate Nullify-aliased calls do *not* add a second tuple to `L_R^Σ`.

**Problem**: ASN-0086's Nullify postcondition was specified under the assumption that every well-formed call produces a fresh `(Σ', _)` pair. The framework's deliberate set-semantics commitment changes this for *duplicate* calls. While documented, the change is buried in the "Audit-slice multiplicity is not preserved" paragraph and the NullifyActiveSubsetCompatibility Corollary's Case B discussion. Downstream layers that consumed ASN-0086's Nullify expecting multiset-semantics would silently break under this framework.

**Required**: Surface the audit-slice multiplicity loss as a top-level commitment in the *Interaction with Nullify* section, not buried in a paragraph after the Corollary. State explicitly: "Under this framework, two consecutive bare-form `Nullify(Σ, d_retr, a)` calls at the same target `a` produce only one tuple in `L_R^Σ`; layers requiring audit-grade multiset-semantics must use attributed retraction (`c_F ≥ 1`) to distinguish events."

### Issue 6: Length and density
**ASN-0094, overall**: The ASN runs roughly 50,000+ words covering: shape framework definitions, Sh-conf axiom + EffectiveWpSimplification corollary, Sh0–Sh4 preservation lemmas, three per-K layer-discipline contracts (Sh4, FDD, SHCD), the Sh5 META catalog with audit table, seven canonical shape rows + walkthroughs, and a Layer Composites section.

**Problem**: This is enough content for 3–5 ASNs. Cross-references between definitions and proofs require multiple passes; the audit table (~11 rows) introduces yet another verification surface. Single-ASN reviews at this scale are difficult — a reader can confirm individual pieces but cannot easily verify the framework's overall coherence.

**Required**: Consider splitting into multiple ASNs: (1) shape conformance framework (shapes, Sh-conf, Sh0–Sh4 preservation, EffectiveWpSimplification); (2) per-K layer disciplines (Sh4 contract, FDD contract, SHCD contract, with their preservation theorems); (3) template catalog (Sh5 META, per-shape walkthroughs, Layer Composites). Each ASN can then be reviewed independently.

### Issue 7: No concrete worked example for AllocatedAddressAntichain Step II's full NAT-card additivity
**ASN-0094, Lemma RetractionTargetNotOnChain Sub-case II.B worked example**: The example exhibits the position-6 mismatch directly (`b_6 = 0 ≠ 4 = a_6`) reaching contradiction at Step II.2, but the proof's general path through Step II.1's NAT-card additivity argument is shown only at `#w = 1` where the additivity is degenerate (`Z_w = ∅`, `|Z_w| = 0`).

**Problem**: The NAT-card additivity argument is the proof's load-bearing step in the general `#w ≥ 2` case (multiple zeros in the suffix could lift `zeros(a)` beyond 3). The current worked example never exercises this; it dispatches via the shorter Step II.2 contradiction at the first non-`b ≼ a` position.

**Required**: Add a worked example with `#w ≥ 2` showing the NAT-card additivity argument in action: e.g., a tumbler `a` whose suffix `w` would have `zeros(w) ≥ 1` if `b ≼ a` held, derive `zeros(a) ≥ zeros(b) + zeros(w) = 3 + 1 = 4`, and contradict `zeros(a) = 3` directly — exercising the proof's general additivity path rather than the degenerate `#w = 1` case.

### Issue 8: Sh5 catalog audit table — rejected row sits inside the catalog table
**ASN-0094, Sh5 catalog-wide citation audit table**: The eleventh row (`K_is_fresh`) is marked "**Rejected**" inline within the catalog audit table, with the note "*not* counted among the ten passing rows".

**Problem**: Including a rejected row in the same table as accepted catalog rows is visually confusing — at a glance the table looks like an eleven-row catalog. The framework's intent is "two-sided gate visibility", but the format creates ambiguity for any consumer scanning the catalog for available templates.

**Required**: Separate the rejected row into its own callout (a one-line note "*candidate rejected, relocated to Layer Composites: `K_is_fresh` citing `mtime`*") below the accepted-rows table. Keep the catalog audit table strictly for accepted rows.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate concurrency
Sh4, FDD, and SHCD contracts assume single-process within-call sequentiality between `Observe_K` and the substrate K.λ-step. Multi-process consistency (racing emitters at `~`-equivalent K) requires a coordination protocol outside this framework's scope. Acknowledged in the Sh4 contract's *Scope* clause and Open Questions.

### Topic 2: Ghost-targeting slot semantics
Shape conformance clause (d) rejects slot addresses outside `A^Σ`. L9 (ASN-0043) permits ghost spans in endsets generally; whether future shape families should admit ghost-targeting slot positions is an explicit Open Question.

### Topic 3: Composite shapes and closure of composition primitives
Whether a closure theorem holds on the composition language (Boolean operators + quantification over T_cat) is acknowledged as future work, not a gap in this ASN's scope.

### Topic 4: Higher-arity link support
The framework is restricted to arity-3 (standard-triple) links per the *Scope and Substrate Scaffolding* commitment. N>3 arity extension would require additional shape components per slot.

### Topic 5: Procedural recipe for catalog extension
Sh5's META observation explicitly notes templates are written by hand against canonical shapes with no mechanical-derivation procedure. Acknowledged as the cost of META status; a sharper procedural recipe would extend the framework's scope.

VERDICT: REVISE
