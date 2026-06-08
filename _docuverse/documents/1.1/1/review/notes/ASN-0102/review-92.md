# Review of ASN-0102

## REVISE

### Issue 1: X14's already-resident reconciliation indexes residency on the wrong state

**ASN-0102, X14 (ContainmentRecording)**: "For an already-resident a — one with `a ∈ ran_{s_C}(Σ.M(d))` already at the pre-state (the self-transclusion case) — the pair `(a, d)` is already present in R: at the embedding composite's initial boundary Σ_0, `(a, d) ∈ Contains_C(Σ_0) ⊆ R` by P4★ (a composite-boundary property, so invoked at Σ_0, not at COPY's possibly-mid-composite pre-state), and it persists to COPY's pre-state by P2."

**Problem**: The case is defined by residency at COPY's **pre-state Σ**, but the inference `(a,d) ∈ Contains_C(Σ_0)` requires residency at the **composite-initial boundary Σ_0**. These differ when COPY is embedded mid-composite. K.μ⁺ adds a content-subspace V→I mapping with frame `R' = R` (ASN-0047) — it records nothing. So a composite `⟨K.μ⁺ (makes a resident), COPY (copies a)⟩` reaches COPY's pre-state with `a ∈ ran_{s_C}(Σ.M(d))` but `(a,d) ∉ R` (a was not resident at Σ_0, and no step recorded it). COPY then writes `(a,d)`, which **is** R-new at the composite level — directly contradicting the quoted "already present in R." The parenthetical "(... not at COPY's possibly-mid-composite pre-state)" flags the gap rather than closing it.

The result is not actually unsound: for such `a`, J1'★ is satisfied via its *range-new* branch (a is not in `ran_{s_C}(Σ_0.M(d))`, so it is range-new over the composite, and COPY's write is exactly the recording J1★ demands). But the stated derivation is wrong for this case. The genuine reconciliation needed for J1'★ — which compares against the composite-initial state — is precisely *Σ_0-residency*, and P4★ at Σ_0 supplies `(a,d) ∈ R` *only* for that subset.

**Required**: Split the case on Σ_0-residency, not pre-state residency: (i) `a` resident at Σ_0 ⟹ `(a,d) ∈ R` by P4★ at Σ_0 + P2, so COPY's write adds no composite-R-new pair (J1'★ vacuous); (ii) `a` resident at COPY's pre-state but not at Σ_0 ⟹ `a` is range-new over the composite, so COPY's write is the required J1★/J1'★ recording via the range-new branch. State the comparison point as Σ_0 throughout.

### Issue 2: Inventory/announcement prose in a structural slot (anti-bloat)

**ASN-0102, X14**: "As an elementary transition (Definition), COPY discharges here what such a transition owes: its frame, the per-state invariants, the transition invariant P3, and the *local* recording fact below."

**Problem**: This sentence is a pure forward inventory of the section's own contents — a reader following the argument skips it to reach the actual discharge. The subsequent paragraphs already name each obligation as they discharge it (the per-state list, the P3 paragraph, the SL definition), so the announcement carries no reasoning the body does not restate at point of use. This is the announce-then-do pattern the anti-bloat pass targets.

**Required**: Delete the announcement sentence; let the discharge paragraphs stand on their own.

OUT_OF_SCOPE

(none — the four Open Questions correctly defer discoverability, downstream containment, time-varying views, and unreachable-origin identity to future ASNs.)

VERDICT: REVISE
