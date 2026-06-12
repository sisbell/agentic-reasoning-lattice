# Review of ASN-0120

## REVISE

No REVISE items. The verification work behind that conclusion, so it is checkable rather than asserted:

**The resolution machinery (ML1) holds up under adversarial reading.** The `wf` predicate's δ-form equivalence (`#ℓ_j = #u_j ∧ actionPoint(ℓ_j) = #u_j ⟺ ℓ_j = δ(n_j, m)`) is correct — equal length plus action point at the last component forces zeros below and a positive final component, which is exactly the δ shape. The prefix-confinement step discharging `ρ(R, Σ) ⊆ dom(Σ.C)` is sound: both interval endpoints share the length-(m−1) prefix (OrdinalShift), T5's preconditions are met (`#p ≥ 1` from `m ≥ 2`), and S3★ closes containment on the content-subspace positions T5 confines the interval to. The correspondence with ASN-0058's `resolve` is handled correctly under standard 7: rather than reinventing the foundation, the ASN proves agreement on `resolve`'s definedness domain (the B1/B3 two-step is complete in both inclusions) and extends it precisely where `resolve` is undefined — partial spans, depth mismatches, empty subspaces — each extension motivated by an input MAKELINK must accept.

**The recovery equation is the right postcondition, and the proof obligations around it are discharged.** The frontier-leak counterexample establishes why the store-trace alternative is too weak (it shows a concrete later-state discoverability violation through never-resolved content), and the parenthetical interior-overreach case completes the case split. The merge derivation is fully worked: TA5-SigValid converts `inc(·, 0)` to `shift(·, 1)` on T4-valid store addresses, the TS3 induction is stated with its `k = 1` (convention) and `k = 2` (no composition) base cases separated correctly, and the ASN-0053 S3 induction names the adjacency witness at each step. The extensional form is proven in both directions, and crucially the right-to-left reading does not skip the shift-form-to-chain-run identification — the one step that would otherwise be a hand-wave is made explicit.

**Both elementary preconditions of the composite are discharged, including the hard one.** K.λ's value precondition is closed by ML6 (necessity *and* sufficiency of `ρ(R₃, Σ) ≠ ∅`, each a short explicit argument). K.μ⁺_L's `a ∉ ran(M(d))` is discharged by the S3★/S3★-aux branch split with freshness against the *whole* store — the content-subspace branch, easy to forget, is covered. The coupling constraints J0/J1★/J1'★ are correctly vacuous, and the ASN distinguishes the two distinct reasons (no content allocation versus empty provenance delta) rather than waving at "vacuous."

**ML9's wp analysis is genuine, not trivial.** Fact (a)'s link-half (`coverage(eᵢ) ∩ dom(Σ'.L) = ∅`) is the load-bearing step and is proven by the subspace argument (`s_C` on every covered F-address via LP-Fin Corollary, `s_L` on every link address via LP-Sub/L0), which disposes of the fresh address `a` uniformly with pre-existing links. Fact (b) covers the boundary `d' = d` — the home document, exactly the case where the seating could have contaminated the test — and shows the added point inert on both sides of Fact (a)'s equation. The future-state extension correctly identifies which premises are state-uniform.

**Boundary cases are systematically present**: empty resolution (admitted for from/to with `e_j = ∅` the unique record; rejected for type), empty spec-set (`p = 0`), depth-mismatched specs in both directions, the contracted home where the store-keyed and arrangement-keyed branch selectors decouple (with the mixed case verified against freshness, the range precondition, and D-MIN★/D-SEQ★), source-equals-home in the frame, and first versus subsequent emission. The worked example verifies postconditions against concrete tumblers and — importantly — does not stop at the creation state: the K.μ⁻ edit exercises ML7, the stable trace, survivability over a partially-deleted span, and LP4-isolation of the other documents.

**Anti-bloat sweep** (per this note's classifier): I read specifically for deferral chains, consumer inventories, ordering justifications, and relocated-finding residue. The two deferrals (link-subspace endsets; one-sided link semantics) are single sentences each, placed where the precondition or boundary makes the scope decision, pointing at distinct Open Questions — not an accretion pattern. The recovery-equation rationale and the stored-positions thought experiment are failure-mode derivations that justify postcondition *strength*, not defensive meta-prose. The one near-duplication — the legality of `(∅, e₂, e₃)` and `(e₁, ∅, e₃)` stated in the boundary settlement and again in ML5 — is a one-clause reuse in a different argumentative role (classifying the Nelson slot convention as informative), below the threshold of a finding.

## OUT_OF_SCOPE

### Topic 1: Direct I-address endset arguments
The ASN restricts MAKELINK to V-spec arguments, so it provably cannot create ghost types (L9) or foreign endsets (full L4 generality). An operation accepting I-addresses directly — the route to those foundation-permitted shapes — is explicitly marked out of scope.
**Why out of scope**: a distinct argument shape requiring its own well-formedness and resolution contract; its absence here is a stated restriction, not a gap.

### Topic 2: Semantics of the one-sided link
What an empty non-type endset asserts about the connection. The ASN settles definedness, legality, and discoverability-inertness; meaning is the first Open Question.
**Why out of scope**: interpretation of a degenerate form, beyond the structural guarantees this operation must specify.

### Topic 3: Link-subspace endset specifications
A V-spec reaching into the link subspace (a link whose endset names another link via arrangement coordinates) is excluded by `wf`'s `subspace(u_j) = s_C` conjunct and deferred.
**Why out of scope**: requires extending `ρ` and the recovery equation to `s_L`-resident targets — new resolution territory, flagged as the second Open Question.

### Topic 4: Higher-arity link creation
The substrate's `Link` admits `N ≥ 3` (L3), but MAKELINK fixes the standard triple. An N-ary creation operation would need per-slot resolution rules beyond the three-argument signature.
**Why out of scope**: Nelson's MAKELINK is the arity-3 operation; N-ary creation is a future extension, not a defect in this contract.

VERDICT: CONVERGED
