# Review of ASN-0077

This is a detailed, careful specification. The proofs are mostly rigorous, edge cases are systematically addressed, and the worked example exercises the main claims. The extension of `origin` to `dom(L)` (O0) is well-justified by the three-piece argument with closure step made explicit. Monotonicity claims O11/O11' are split appropriately for the two arrangement-extending transitions. The wp characterizations include a non-trivial case (single-origin sufficiency), and the singleton I-span structural argument is fully unpacked.

A few items to verify:

- **O0(b) closure step** enumerates non-K.λ transitions to show only K.λ modifies `dom(L)`. For K.μ⁺, K.μ⁻, K.ρ the argument is "effect targeting only other components" — this is reasonable but relies on a frame convention (unmentioned components preserved) that ASN-0047 does not state as a meta-axiom. The convention is standard; flagging this only as a foundation-level concern rather than an ASN-0077 defect.
- **Singleton I-span derivation** for `#b > #a`: the T1 analysis forcing `b` to be a proper extension of `a`, combined with the K.α emission-length invariant, is rigorous. The ASN does walk through the structural argument completely.
- **Transition coverage**: O11/O11' cover K.μ⁺ and K.μ⁺_L. The worked example demonstrates K.μ~ (mapping reassignment) and K.μ⁻ (admissibility loss). K.α/K.δ/K.λ/K.ρ preserve `M(d)` exactly and therefore preserve `origins_V` via O7 — this is implicit but not explicitly stated. Acceptable for a spec where the claim chain is traceable.
- **Worked example K.μ~ admissibility**: verified — `|dom_C(M(d₃))| = 7 ≥ 2`, the swap preserves S8a, S8-depth, D-CTG★, D-MIN★, S3★, and `π ≠ id`. The chosen σ_{3} demonstrates origin reassignment cleanly.

## OUT_OF_SCOPE

### Topic 1: Unified I-span lift across subspaces
**Why out of scope**: The I-span lift's restriction to `dom(C)` (silently dropping link addresses) is a design choice that the ASN flags in Open Question 1. Resolving this would be a future ASN that defines the unified I-span semantics.

### Topic 2: Operation surfacing transclusion chains
**Why out of scope**: Open Question 2. SHOWORIGIN reports the original allocator, not the chain of intermediate documents. A separate operation would be needed.

### Topic 3: Distinguishing native vs transcluded content within a document
**Why out of scope**: Open Question 3. SHOWORIGIN as defined does not separate native from transcluded — this is a distinct operation.

### Topic 4: Historical containment operation
**Why out of scope**: Open Question 5. The ASN correctly notes that historical containment (from `Σ.R`) is a different concern from current-arrangement origin.

VERDICT: CONVERGED
