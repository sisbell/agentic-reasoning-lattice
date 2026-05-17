# Review of ASN-0047

## REVISE

### Issue 1: K.δ case (ii) k = 1 with live operand — operational T10a allocator unnamed

**ASN-0047, K.δ case (ii) discharge analysis ("Two scopes of T10a's domain")**: "T10a's GlobalUniqueness (ASN-0034) applies *at the entity-allocator layer*: every inc-produced address from an operand satisfying `InEntityAllocatorDomain` is distinct from every previously allocated address in that allocator's domain, so `e ∉ E` follows."

**Problem**: The live-operand k = 1 sub-case (where `t ∈ E_doc`) claims T10a's GlobalUniqueness underwrites `e ∉ E` at the entity-allocator layer. The ASN names content sub-allocators (A_C(d)) and link sub-allocators (A_L(d)) via SubAllocatorAxiom, yet does not formally identify a "version sub-allocator at t" for the k = 1 case. T10a's at-most-once spawning constraint implies inc(t, 1) activates a new child-allocator at e, but this lift is implicit. The asymmetry with SubAllocatorAxiom — which explicitly names content/link sub-allocators with operational underwriting — leaves the discharge chain for the live-operand k = 1 path underspecified compared to k ∈ {0, 2}. A K.δ k = 1 event at a live `t` should name which T10a allocator's domain contains e as a fresh emission for GlobalUniqueness to apply.

**Required**: Either (a) extend SubAllocatorAxiom to activate a version sub-allocator at each document (parallel to content and link), or (b) note explicitly that K.δ at k = 1 from a live operand t activates a new T10a allocator at e via standard child-spawning (with spawnPt at t, spawnParam = 1), and GlobalUniqueness on the parent allocator's emission history then yields `e ∉ E`.

### Issue 2: Worked Example 4 (ghost-base versioning) under-enumerates per-invariant verifications

**ASN-0047, "Worked example: ghost-base document versioning", Step 1, Verification against Σ₇**: "*P8 (operative):* parent(`1.0.1.0.5.1`) = `1.0.1` ∈ E₇ — discharged through parent(·), bypassing the ghost base. ✓ — *All other per-state and per-transition invariants:* vacuous or frame-preserved by K.δ on a document."

**Problem**: This worked example is engineered to exercise the K.δ k = 1 ghost-base relaxation, but Step 1's verification glosses every invariant except P8 with "vacuous or frame-preserved." The "fork with subsequent insertion" example by contrast enumerates each invariant per step. For an example whose explicit purpose is verifying the correctness of the ghost-base relaxation against the full invariant set — and which is cited in the coordinating coverage table as exercising the "layer-aware `e ∉ E` discharge" — glossing the verification is a notational regression. The Step 1 paragraph references P8 alone but does not verify NodeUniqueAllocation (vacuous on non-node), NodeLineage (vacuous on non-node), J0/J1★/J1'★ (vacuous on no content/arrangement/provenance change), or the arrangement-side invariants on the freshly created empty M(e₁).

**Required**: Enumerate per-invariant verification at each step at the same level of detail as Example 2 (fork). Each invariant should be explicitly verified or noted as vacuous/frame-preserved with justification, particularly at the K.δ ghost-base step where the discharge mechanism is novel.

### Issue 3: K.μ⁻ admissibility precondition — joint role of two clauses obscured

**ASN-0047, K.μ⁻ "Precondition" enumeration**: "*Admissible removal pattern (per-subspace suffix or full clearance).* ... *At least one subspace contracts strictly.* `(E S ∈ {s_C, s_L} : V_S(d) ≠ ∅ : n'_S < n_S)` — some subspace's post-state index `n'_S` is strictly less than the pre-state `n_S` over a non-empty pre-state subspace..."

**Problem**: K.μ⁻'s precondition has two distinct clauses that are jointly necessary: per-subspace pattern admissibility (suffix or full clearance, compatible with D-CTG★/D-MIN★) and "at least one subspace contracts strictly" (whole-arrangement strictness witness). The per-subspace clause alone admits the trivial "no change" assignment `n'_C = n_C ∧ n'_L = n_L`, which would yield M'(d) = M(d) and violate the strict-subset effect clause `dom(M'(d)) ⊂ dom(M(d))`. The second clause is therefore load-bearing for closing the effect clause at the whole-arrangement level. The two clauses' joint role and individual insufficiency are noted in a parenthetical but not signposted as the load-bearing structure of the precondition.

**Required**: Either consolidate into a single conjunctive precondition with explicit indication that the per-subspace clause governs D-CTG★/D-MIN★ compatibility while the strict-contraction clause closes the effect-clause strictness; or restructure so the joint role is presented at the head of the precondition list rather than as a discovery deep in the supporting prose.

## OUT_OF_SCOPE

(No items. The ASN's open questions list correctly defers tombstone-style link withdrawal, version-management semantics beyond bare entity membership, account-level k = 1, and non-T10a allocator admissibility to future ASNs.)

VERDICT: REVISE
