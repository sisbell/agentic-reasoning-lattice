# Review of ASN-0100

This is a thorough, careful specification. It covers all three INSERT effects, verifies the full ExtendedReachableStateInvariants conjunction (S2, S3★, S4, S7a–d, S8a/fin/depth, S8★, C-fin, D-CTG★/MIN★/SEQ★, P6, P7, P8, L0/1/1a/1b/1c/3/12/14/fin, CL-OWN/UNIQ, plus boundary P4★/P4a/P7a), handles position-0, append, interior, and empty-document boundaries, supplies a concrete worked example, and gives two non-trivial wp derivations. Cross-ASN citations are all to foundation ASNs (0034, 0036, 0047, 0058, 0082, 0093, 0098) — no violations. The disclaiming of ASN-0082's I3-V/I3-CS/I3-CX (which describe a shift-only model whose post-state is strictly contained in INSERT's) is exactly the kind of care the standard demands.

I found one genuine defect.

## REVISE

### Issue 1: Atomicity scope is stated as "precisely two-fold" but the K.ρ-commutation argument requires R to also be protected

**ASN-0100, §Operation's Formal Contract (INS.pre / Environmental Assumptions)**: "The required atomicity scope is precisely two-fold: (i) `A_C(d)`'s chain emission state … and (ii) `M(d)`'s text subspace `V_{s_C}(d)` must not be modified between INSERT's elementaries."

**ASN-0100, §Atomicity and Canonical Order (commutation analysis, K.ρ ↔ K.μ⁺)**: "Under INS.pre's composite-atomicity precondition, no other composite can observe this intermediate as a boundary candidate … R is implicitly within the atomicity envelope for INSERT-discharged J1'★ pairs because R-entries with (a_k, d) for fresh a_k are coupled to the same A_C(d) chain."

**Problem**: The commutation argument licenses firing K.ρ(a_k, d) *before* K.μ⁺ places `a_k`, conceding that the resulting intermediate has `(a_k, d) ∈ R` while `a_k ∉ ran(M(d))` — a configuration that "would violate J1'★ if it were observable as a composite boundary." The argument's safety then leans on R being shielded ("R is implicitly within the atomicity envelope"). But the scope was declared "precisely two-fold," and R is not one of the two named resources. The word "precisely" and the later "implicitly within the envelope" are in direct tension: either the K.ρ-before-K.μ⁺ ordering is *unsafe* under the stated scope, or the stated scope is wrong. This is the spec contradicting its own atomicity definition.

**Required**: Resolve the tension by one of: (a) extend the stated atomicity scope to explicitly include R-entries `(a_k, d)` for INSERT's fresh addresses, dropping "precisely two-fold"; (b) restrict the commutation claim so K.ρ must follow K.μ⁺ (the canonical order already does this — the flexibility claim is not load-bearing); or (c) if J1'★ is genuinely a per-composite coupling on the *other* composite's own R'\R (and thus cannot be tripped by INSERT's intermediate unmatched pair), say so and delete the appeal to an "implicit" R envelope. The current text asserts all three regimes at once.

## OUT_OF_SCOPE

### Topic 1: Insertion into the link subspace
**Why out of scope**: The ASN correctly bounds itself to the content subspace `s_C` and defers `K.μ⁺_L`/`K.λ`-based link insertion to a future ASN (§Bounding the Scope, first Open Question). No fix required; the deferral is appropriate.

### Topic 2: Closure of INSERT under composition; concurrent-INSERT serialization basis
**Why out of scope**: These appear as Open Questions and are genuinely new territory, not gaps in the present per-state effect specification. The composite-atomicity *precondition* is specified; the *mechanism* securing it is correctly left to implementation/future work.

VERDICT: REVISE
