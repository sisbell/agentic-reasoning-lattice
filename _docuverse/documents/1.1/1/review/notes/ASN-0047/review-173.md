# Review of ASN-0047

## REVISE

### Issue 1: Per-step vacuity boilerplate repeated across every worked example

**ASN-0047, worked examples (fork, interior replacement, link allocation):** the same "vacuously satisfied" note is restated 10+ times in slightly varying words. E.g. in *fork with subsequent insertion*:

> "*J1'★ (vacuous):* K.μ⁻ holds R in frame, so `R' \ R = ∅`. No new provenance entries to check; J1'★ is vacuously satisfied."

and the near-identical block re-appearing at the K.μ~ step, the K.λ steps, and K.μ⁺_L; and:

> "*L-invariants vacuously satisfied:* `dom(L₂) = dom(L₁) = ∅` ... so L0 (L-clause), L1, L1a, L1b, L1c, L3, L-fin, CL-OWN, and CL-UNIQ are vacuous at Σ₂ ..."

restated nearly verbatim at Σ₂, Σ₃, Σ₄, Σ₅.

**Problem**: This is the anti-bloat pattern "two paragraphs in the same document say the same thing in different words," recurring at every R-framing or L-framing step. The reader must skip identical text to find the one or two substantive checks in each step. The vacuity follows mechanically from the frame conditions that P3 already establishes.

**Required**: State the convention once (e.g., "any step that frames R discharges J1'★ vacuously; any step over a state with `dom(L) = ∅` discharges the L-invariants vacuously — we omit per-step repetition") and delete the per-step copies, leaving only the non-vacuous checks in each worked step.

### Issue 2: P7a transient-failure narrative duplicated four times

**ASN-0047, *Extended reachable-state invariants***: the fact "P7a transiently fails after K.α before K.μ⁺/K.ρ, restored at the boundary" is stated (a) in the bullet immediately after the ExtendedReachableStateInvariants statement ("a composite that allocates fresh content (K.α) violates P7a at the post-K.α intermediate state..."), (b) in the full "Concrete trace illustrating transient failure" table, (c) in the Class (b) composite-boundary matrix row for P7a, and (d) in the Class (b) P7a prose.

**Problem**: The same transient-failure-and-restoration claim is carried by four separate artifacts in one section. This is inventory/essay duplication, not four distinct arguments — only the Class (b) prose does load-bearing work (the S3★ + L14 + S3★-aux derivation that the witness V-position is content-subspace).

**Required**: Keep the Class (b) prose (the only one that derives the subspace of the witness) and the matrix row; cut the standalone trace table and fold the introductory bullet's content into the matrix, so the transient-failure claim is asserted once.

### Issue 3: "Properties Introduced" rows that declare non-properties

**ASN-0047, *Properties Introduced* → New properties table**: the rows for J1, J1', and P4 each read, in effect, "Link-free (`dom(L) = ∅`) reading of the operative X★ ...; not a separate property."

**Problem**: A table titled "New properties introduced by this ASN" listing three entries whose content is "this is not actually a property" is meta-prose occupying a structural slot. It restates the superseding relationship already stated inline at J1★/J1'★/P4★.

**Required**: Remove the J1/J1'/P4 rows from the new-properties table (or collapse to a single pointer line), since the operative forms J1★/J1'★/P4★ already carry the definitions and the "link-free reading" remark lives at their definitions.

## OUT_OF_SCOPE

### Topic 1: Interior insertion / link withdrawal mechanisms
The constraint that K.μ⁺ can only append at the contiguous max (interior content insertion and interior link withdrawal require compound or separate mechanisms) is correctly deferred to Open Questions and to the named operations layer (INSERT/DELETE), which is out of scope. No revision needed.

### Topic 2: M-totality override of the foundation typing
The Typing note overrides ASN-0093's partial-M typing with total M, carried by the identity `d ∈ dom(M) ⟺ d ∈ E_doc`. Because every inherited per-state invariant quantifies over `v ∈ dom(M(d))` and `M(d) = ∅` for non-documents, the override is invariant-preserving and adequately translated. This is a documented, sound design decision, not an error.

Note on substantive content: I checked the load-bearing proofs — D-SEQ★ (both m=2 and m≥3 cases, including the u_M finiteness contradiction), the K.μ~ admissibility/necessity/sufficiency biconditional and link-subspace fixity (Steps 1–4 under CL-UNIQ), the K.μ⁻ constructive/post-state equivalence, FrontierEquivalence, and the K.δ case-(ii) discharge tree — and found them rigorous with edge cases (empty subspace, singleton, first/subsequent emission, orphan links) covered. The findings above are prose-density, not correctness.

VERDICT: REVISE
