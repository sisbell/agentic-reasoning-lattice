# Review of ASN-0091

## REVISE

### Issue 1: Composite-boundary properties presuppose Σ is a composite boundary, but REARRANGE's stated domain is all reachable states

**ASN-0091, "Composite-Boundary Properties"**: "Throughout, Σ is a reachable pre-state, so each property holds at Σ as a composite-boundary property of ASN-0047's ExtendedReachableStateInvariants."

**Problem**: ExtendedReachableStateInvariants splits its conclusion: per-state invariants hold at *every* state reachable by elementary transitions, but **P4★ ∧ P4a ∧ P7a hold only at composite boundaries**. The operation's domain, however, is stated as "every Σ reachable from Σ₀ by a finite sequence of elementary transitions drawn from valid composites" — which includes states *interior* to a composite. At such an interior Σ, P4★/P4a/P7a need not hold, so "holds at Σ ... by ExtendedReachableStateInvariants" is unjustified, and the inheritance-to-Σ' arguments for P4★ and P7a collapse. The note tries to close this with "A REARRANGE is itself a composite ... so its endpoints are composite boundaries," but that asserts the conclusion: it is true only if Σ is already a boundary. RA-reg and R-PRE impose no such precondition.

**Required**: Add an explicit precondition that the pre-state Σ is a composite boundary (so Σ' is too), or restrict the composite-boundary claims to that case. With Σ' established as a *reachable composite boundary*, P4★ ∧ P4a ∧ P7a follow directly from ExtendedReachableStateInvariants — which is also the clean route (see Issue 3).

### Issue 2: P4a misstated as existential; one-trace argument does not establish the universal

**ASN-0091, "Composite-Boundary Properties"**: "P4a asserts that along *some* valid trace to Σ' every `(a, d) ∈ Σ'.R` is witnessed ... appending the REARRANGE composite — which records no new provenance — preserves the witnessing."

**Problem**: The foundation P4a is universally quantified over traces: `(A valid trace Σ₀ →* ... →* Σ_n = Σ :: (A (a,d) ∈ R :: (E Σ_k ...)))`. The note reads it as "some valid trace" and discharges it by exhibiting exactly one trace (trace-to-Σ + REARRANGE step). That establishes the existential, not the required universal — an arbitrary valid trace to Σ' need not end in this REARRANGE step. The discharge is therefore both weakened and incomplete.

**Required**: State P4a with its universal quantifier and discharge it accordingly — most directly by citing ExtendedReachableStateInvariants at the reachable composite boundary Σ' (which gives P4a for all valid traces), once Issue 1 is resolved.

### Issue 3: Manual P4★/P7a re-derivations are redundant given the foundation theorem (anti-bloat)

**ASN-0091, "Composite-Boundary Properties"**: the paragraph-by-paragraph re-derivation of P7a (from RE-C + RE-R), P4★ (from RE-ran + RE-C + RE-R + the Contains_C structural form), and P4a.

**Problem**: Once Σ' is a reachable composite boundary (Issue 1), ExtendedReachableStateInvariants delivers P4★ ∧ P4a ∧ P7a at Σ' in one citation. The hand re-derivations re-establish exactly what the theorem already guarantees, and the P4a re-derivation additionally introduces the error of Issue 2. This is accreted discharge prose around a result the foundation already owns.

**Required**: Replace the section with the single boundary-citation. Keep a derivation only if it proves something the theorem does not (it does not, here).

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
The note fixes the cut subspace at s_C (CS3) and leaves link-subspace reordering to an open question. Correctly deferred — defining a link-subspace REARRANGE and its invariants is new territory, not a defect here.

### Topic 2: Reconstitution of a same-source span split across a cut
RE-trans establishes per-byte origin invariance but explicitly declines to show that two fragments *jointly reconstitute* the source span. That joint-reconstitution guarantee is a future-ASN obligation, not an error in this one.

VERDICT: REVISE
