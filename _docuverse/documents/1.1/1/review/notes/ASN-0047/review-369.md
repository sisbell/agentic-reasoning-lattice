# Review of ASN-0047

I checked the elementary transitions against their boundaries (empty document, single-position content, full clearance, duplicate-I-address sources, depth re-pinning after clearance), traced the coupling constraints J0/J1★/J1'★/J4 through the worked examples, and verified the Class (a) matrix covers every listed per-state invariant. The construction holds up under this scrutiny. Specific checks that passed and are worth recording:

- **Couplings do real work, not decoration.** J1'★'s post-state witness conjunct is exactly what forbids a place-record-remove composite, which is what makes P4a's trace-witnessing discharge sound. I tried to break P4a with a composite that records `(a,d)` then removes `a` before Σ'; J1'★ correctly rejects it as invalid.
- **K.μ~ firing precondition is exactly right at the hard case.** A content subspace where every position transcludes one I-address (`M(d)|_{dom_C}` constant) correctly does *not* fire — net-identity effect, no reordering possible — and the necessity/sufficiency proof distinguishes net-effect from map-level `π ≠ id` under S5.
- **Depth re-pinning after full clearance is contained.** After K.μ⁻ clears `V_{s_C}(d)`, the depth `m_{s_C}` is unpinned, so the K.μ⁺ rebuild in K.μ~ could in principle choose a new depth and break K.μ~-FIX — but admissibility clause (iii) (length preservation) forecloses this, and the full-clearance realisation honors it.
- **Entity model is internally consistent.** Node-nesting (SSGU zero-separator divergence), account/document/version dispatch (ParentAllocatorDispatch), and the k=0/1/2 freshness discharges (FrontierEquivalence vs. ChildSpawnFreshness, the latter correctly admitting node operands) all close. The worked example exercising a multi-component node (`1.2`) confirms the nested-node path.
- **Cross-ASN references are all to foundation ASNs** (0034, 0036, 0043, 0045, 0093) — no Standard 7 violation. No reinvented notation; `subspace`/`subspace_I`/`origin`/`parent` are used per their foundation definitions or introduced cleanly.

## REVISE

(none — see note below)

## OUT_OF_SCOPE

### Topic 1: Transitive-transclusion provenance, concurrency/serialization, address-space exhaustion, renumbering-aware interior link contraction
The ASN's Open Questions correctly defer these. Each requires machinery this ASN does not (and need not) introduce: transitive provenance is a closure over chains the current R does not track; concurrent allocation is excluded by SequentialTransitionAxiom; interior link renumbering (`DELETEVSPAN`-style compaction) is a named-operation concern, and the ASN is explicit that K.μ⁻ models suffix removal only. These belong in future ASNs, not as revisions here.

### Topic 2: Link-subspace reordering
K.μ~ fixes the link subspace pointwise (clause (v), via LRP + CL-UNIQ), so there is no elementary or composite mechanism to reorder links within a document. This is a deliberate consequence of CL-UNIQ/link permanence, not an error; whether link reordering is ever needed is future territory.

I was directed to surface sprawl, example-volume, and split concerns under the anti-bloat classifier, but the two declined findings on this ASN already adjudicated exactly those (structural split, example-to-companion extraction, matrix-cell expansion) as invalid, with the reviser's rationale that the argument is a single coupled unit. I will not re-raise variants. After exhaustive correctness, boundary, and coupling checks I found no substantive defect, missing case, or under-derivation, and the one phrasing I flagged on first pass ("the range-changing K.μ⁻+K.μ⁺ pair identified in the *Elementary transitions* section") admits a charitable reading (the transitions are *defined* there; "range-changing pair" is the example's own framing), so it does not rise to a REVISE.

VERDICT: CONVERGED
