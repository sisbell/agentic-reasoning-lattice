# Review of ASN-0047

## REVISE

### Issue 1: J4 derivation incorrectly claims `ran(M(d_src)) ⊆ dom(C)`
**ASN-0047, J4 fork composite, "Discharge of arrangement-side invariants"**: "Step (ii)'s K.μ⁺ creates only content-subspace V-positions (by the K.μ⁺ amendment) targeting addresses in `ran(M(d_src)) ⊆ dom(C)` (by S3★ at the pre-state)"
**Problem**: When d_src has link-subspace V-positions, ran(M(d_src)) includes link addresses (in dom(L), disjoint from dom(C) by L14). S3★'s content clause only gives `ran(M(d_src)|_{V_{s_C}(d_src)}) ⊆ dom(C)`. The unrestricted chain is incorrect.
**Required**: Replace with `ran(M(d_src)|_{V_{s_C}(d_src)}) ⊆ dom(C)`. Also tighten J4's effect clause `ran(M'(d_new)) ⊆ ran(M(d_src))` to make the content-subspace projection explicit.

### Issue 2: K.μ~ link-subspace fixity step (4) cites CL-UNIQ at Σ' as if established
**ASN-0047, "Decomposition of K.μ~", Link-subspace fixity proof step (4)**: "CL-UNIQ at Σ' — link-subspace injectivity of `M'(d)|_{dom_L}` — uniquely identifies the link-subspace V-position mapping to ℓ as v, giving `π(v) = v`."
**Problem**: CL-UNIQ at Σ' is the inductive target — the very invariant the broader ExtendedReachableStateInvariants proof must discharge at Σ'. It cannot be cited as a known fact within the proof that establishes it. The argument is recoverable (step (3) shows `M'(d)|_{dom_L} = M(d)|_{dom_L}`, so v, π(v) ∈ dom_L(M(d)) both mapping to ℓ under M(d) by step (3) yields π(v) = v via CL-UNIQ at Σ from inductive hypothesis), but the proof as written inverts the logical flow.
**Required**: Either explicitly derive CL-UNIQ at Σ' from CL-UNIQ at Σ + step (3) before step (4), or invoke CL-UNIQ at Σ (the pre-state, inductive hypothesis) directly.

### Issue 3: J2 and J3 statements omit L' = L
**ASN-0047, "Coupling and isolation", J2 and J3**: "J2 (Contraction isolation)... C' = C ∧ E' = E ∧ R' = R" and "J3 (Reordering isolation)... C' = C ∧ E' = E ∧ R' = R"
**Problem**: In the extended state, K.μ⁻ and K.μ~ also hold L' = L (per the "Frame extension" paragraph). The J statements predate the L extension and were not updated.
**Required**: Amend J2 and J3 to include `L' = L`, or explicitly note that the Frame extension paragraph supersedes them in the extended state.

### Issue 4: "Why S7d★ rather than S7d" meta-prose
**ASN-0047, ExtendedReachableStateInvariants proof, S7d★ Foundation invariants entry**: "*Why S7d★ rather than S7d.* ASN-0036's S7d states that every document is the result of an allocation event under T10a; the ghost-base sub-case admits documents allocated via direct E-inspection... S7d★ widens S7d's clause... while retaining the structural identity... and the cross-document distinctness consequence — the two properties downstream consumers (the Cross-document disjointness chain lemma; the K.μ⁻ admissibility analysis; J4's d_src/d_new requirements) actually rely on."
**Problem**: This is the anti-bloat pattern of explaining why an axiom is needed rather than what it says, plus a use-site inventory of downstream consumers. The S7d★ statement itself is the content; the comparative justification is meta-rationale.
**Required**: Delete the "Why S7d★ rather than S7d" subsection. If a one-line note that S7d★ widens ASN-0036's S7d to admit ghost-operand discharge is needed, fold it into S7d★'s statement.

### Issue 5: NodeAllocationRegistry definition contains essay content
**ASN-0047, State model, NodeAllocationRegistry definition**: "...the realisation is unspecified at this layer — Nelson's design is contractual (single root authority delegating recursively under the 'owned numbers' principle, LM 4/17–4/22), and Gregory's implementation realises it concretely as the single global granfilade with query-and-increment dispatch (the granfilade tree serving as the registry, append-only by L1c/T10a discipline)."
**Problem**: The Definition slot contains substantial implementation rationale citing Nelson and Gregory. The actual definitional content is one short sentence; the rest is essay content in a structural slot.
**Required**: Trim the definition to its essential content (deterministic discipline issuing node addresses with monotonic registry, consulted at every IsNode K.δ). Move Nelson/Gregory citations to design notes or commit messages.

### Issue 6: Link-withdrawal gap content spread across four sections
**ASN-0047**: The gap regarding interior link-subspace withdrawal appears in: (a) "Elementary transitions"' "Known gaps from the catalogue" paragraph, (b) "Amendments to existing transitions"' "Justification for uniform contiguity" paragraph, (c) the dedicated "Link-withdrawal gap under D-CTG★ / D-MIN★" paragraph, (d) Open Questions.
**Problem**: Multiple paragraphs in different sections defer to or restate the same content — the multi-section deferral pattern flagged by the anti-bloat classifier.
**Required**: Consolidate to one canonical statement (the dedicated paragraph). Replace the other three with brief pointers, or remove the redundant ones entirely.

### Issue 7: Worked examples violate the invariant verification convention
**ASN-0047, "Invariant verification convention" and subsequent worked examples**: The convention states "Per-transition invariants P0/P1/P2/P3★/L12 are discharged uniformly by ExtendedTransitionInvariants." The fork example then includes "*P3★:* C₂ = C₁; E₂ ⊇ E₁; R₂ ⊇ R₁; L₂ = L₁ = ∅. Only M changed. ✓", and similar P3★ enumerations appear in subsequent steps and in the K.λ/K.μ⁺_L/K.μ~/K.μ⁻ examples.
**Problem**: The convention's stated discipline is violated by every worked-example step. Either the convention is too strict or the examples are too verbose; the current text is internally inconsistent.
**Required**: Either remove P3★ verifications from worked examples (in keeping with the convention) or amend the convention to permit explicit enumeration of per-transition invariants for didactic clarity.

### Issue 8: "Justification for uniform contiguity" paragraph is design rationale
**ASN-0047, Amendments to existing transitions, after D-CTG★/D-MIN★**: "*Justification for uniform contiguity.* The strengthening to D-CTG★/D-MIN★ is justified by separating the load-bearing requirement (link-address permanence) from the disposition under which that requirement is achieved (V-position arrangement discipline)..."
**Problem**: The paragraph explains why the design choice is principled rather than what the invariants assert. The first sentence is meta-discussion; the Nelson/Gregory citations and L12-separation argument are design context. This is essay content in a structural slot.
**Required**: Condense to a one-line acknowledgement that D-CTG★/D-MIN★ trade interior link-withdrawal expressibility for uniform contiguity, with the trade-off mitigated by L12 + a future withdrawal mechanism. Move detailed rationale to design notes.

### Issue 9: "Reading" footnote on D-CTG★
**ASN-0047, Amendments to existing transitions, D-CTG★**: "*Reading.* `m_S` is fixed per non-empty subspace by S8-depth (ASN-0036), and 'positive tuple' denotes the S8a-compatible domain of V-positions (components in ℕ⁺); the closed-interval form is only well-defined once S8-depth and S8a have been established at the state under consideration..."
**Problem**: The "Reading" footnote is parenthetical interpretive guidance — explaining how to interpret the invariant rather than asserting the invariant itself. This is meta-prose in a structural slot.
**Required**: Either integrate the clarifications inline into D-CTG★ (terser) or delete the footnote.

### Issue 10: K.μ⁻ exhaustiveness lemma's case (b) precondition is too restrictive
**ASN-0047, K.μ⁻ "Exhaustiveness lemma (K.μ⁻ per-subspace partition)"**: "(b) *Hole at an interior index.* There exist `k_lo < k_hi` in K' with some `k₀ ∈ K \ K'` satisfying `k_lo < k₀ < k_hi`."
**Problem**: Consider K = {1, 2, 3, 4} and K' = {1, 3} (suffix-removed at the top, with an interior hole). The partition proof at "If `K'` is not contiguous over `[k_min, k_max]`, there is some `k₀ ∈ (k_min, k_max) ∩ (K \ K')` — (b) with k_lo := k_min, k_hi := k_max" routes this to case (b) — but K' = {1, 3} has k_max = 3 < n_S = 4, so this configuration violates *both* "interior hole" (case b at k₀ = 2) *and* "suffix not removed past 3". The proof handles this via (b) at the interior hole, but the relationship between case (b) and the surrounding suffix structure is not fully articulated.
**Required**: Verify that case (b) correctly absorbs all non-contiguous K' with a present minimum (i.e., 1 ∈ K'). The current text lands the routing correctly, but the exhaustiveness argument should be more explicit about how non-suffix removals always exhibit an interior hole reachable via the proof's k_min/k_max construction.

### Issue 11: NodeAllocationRegistry and SubAllocatorAxiom asymmetric stratification
**ASN-0047, State model and Allocator hierarchy under documents**: NodeAllocationRegistry is described as "external to T10a's allocator-state machinery" with NodeUniqueAllocation as the axiomatic uniqueness condition. SubAllocatorAxiom is introduced separately as the activation discipline for d's content and link sub-allocators.
**Problem**: The asymmetry is unexplained — why is node allocation external to T10a while document/account allocation operates within T10a, and content/link sub-allocators are activated by SubAllocatorAxiom? The ASN doesn't explicitly map which K.δ cases use T10a-GlobalUniqueness vs. NodeUniqueAllocation vs. direct E-inspection vs. SubAllocatorAxiom's FirstEmission. The "Freshness discharge" paragraph at K.δ partially addresses this but doesn't include all paths.
**Required**: A consolidated discharge table or paragraph showing, for each freshness obligation (K.δ IsNode/IsAccount/IsDocument live/IsDocument ghost-base, K.α first/subsequent, K.λ first/subsequent), which axiom or T10a result closes the obligation. The current discharges are spread across multiple sections.

### Issue 12: Convention-dependent chain in L1c discharge
**ASN-0047, ExtendedReachableStateInvariants proof, L1c Foundation invariants entry**: "Under SubspaceConventionAxiom (`s_C = 1`, `s_L = 2`), the chain `t₀ = d, t₁ = inc(d, 2) = b_C(d) = [d.0.1], t₂ = inc(t₁, 0) = [d.0.2] = b_L(d), t₃ = inc(t₂, 1) = ℓ = [d.0.2.1]` is T10a-conforming... The step `t₂ = inc(t₁, 0) = b_L(d)` is *convention-dependent* (it relies on `s_L = s_C + 1`); under a convention with non-consecutive subspace identifiers, the chain to `b_L(d)` would extend with additional `inc(·, 0)` steps..."
**Problem**: The convention-dependence note appears at the chain construction, then is repeated in the Allocator hierarchy section and in SubAllocatorAxiom's prose. Three separate places handle the same caveat. Worse, the convention-dependence is loose: under SubspaceConventionAxiom (which the ASN fixes globally), `s_L = s_C + 1 = 2` holds, so the convention-dependent chain *is* the chain under the axiom — there's no other convention to defend against in this ASN.
**Required**: Either commit fully to SubspaceConventionAxiom (omit the "convention-dependent" qualifiers since the convention is axiomatized) or articulate why convention-independence matters at this layer.

## OUT_OF_SCOPE

### Topic 1: Concurrent transition discipline
**Why out of scope**: The ASN explicitly defers concurrent and multi-protocol execution to a future ASN (Open Question on ghost-base soundness under concurrency). SequentialTransitionAxiom commits to single-event sequential semantics.

### Topic 2: Concrete node-allocation registry mechanism
**Why out of scope**: NodeUniqueAllocation is the abstraction boundary; the realisation (single granfilade, distributed registry, etc.) is outside the docuverse layer's specification scope.

### Topic 3: Link-withdrawal mechanism for interior link-subspace positions
**Why out of scope**: This requires a separate mechanism (status flag, tombstone, retraction link) outside K.μ⁻'s presentational-removal contract; the present ASN documents the gap but defers the mechanism's specification.

### Topic 4: Version-management contract beyond k = 1 ghost-base
**Why out of scope**: Lineage acyclicity, arrangement invariants for version k > 1, version DAG structure are deferred to a version-management ASN.

### Topic 5: Account-level depth-1 tumbler extension (account versioning)
**Why out of scope**: The ASN excludes this at K.δ's precondition with a documented rationale; admitting it would require account-renaming or multi-account-identity scope.

### Topic 6: Operations and operation-level decompositions
**Why out of scope**: Named operations (INSERT, DELETE, COPY, REARRANGE, MAKELINK) are explicitly out of scope per the review framing.

VERDICT: REVISE
