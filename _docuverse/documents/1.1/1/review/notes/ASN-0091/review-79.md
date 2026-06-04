# Review of ASN-0091

## REVISE

### Issue 1: RA-adm discharge silently assumes Σ is reachable
**ASN-0091, "REARRANGE_K Realises the Abstract Class"**: "The per-state foundation invariants hold at every reachable state (ASN-0047's ExtendedReachableStateInvariants), so RA-adm reduces to establishing that Σ' is reachable, given Σ reachable from Σ₀..."
**Problem**: RA-adm is defined as an unconditional preservation clause — "every per-state foundation invariant satisfied by Σ is satisfied by Σ'." The realisation discharges it *only via reachability* (Σ reachable ⟹ Σ' reachable ⟹ Σ' satisfies the invariants). For a Σ that satisfies all per-state invariants but is not reachable, the argument supplies nothing — yet the abstract definition and the realisation claim both quantify over arbitrary Σ. The assumed input (Σ reachable) is not stated in either the RA-adm definition or the realisation claim.
**Required**: Either scope RA-adm (and the realisation theorem) explicitly to reachable states, or supply a direct invariant-by-invariant preservation argument that does not route through reachability.

### Issue 2: RE-trans (iii) skips the step establishing a ∈ dom(C)
**ASN-0091, "Cross-Document Transclusion Preserved"**: "*Conclusion (iii)* ... by C2 (ASN-0093) `origin(a) ∈ dom(Σ.M)`, so RE-other applies at `d' = origin(a)`..."
**Problem**: C2 governs *content* addresses only. The premise is `a ∈ ran(Σ.M(d_view))`, which by S3★ may be a link-subspace image in dom(L), where C2 does not apply. The reason `a` must be content is that link-subspace images satisfy CL-OWN (`origin(M(d)(v)) = d_view`), contradicting the transclusion premise `origin(a) ≠ d_view` — so the link case is excluded and `a ∈ dom(C)`. This step is load-bearing for invoking C2 but is omitted.
**Required**: State the CL-OWN exclusion that forces `a ∈ dom(C)` before citing C2.

### Issue 3: Composite-boundary properties not addressed at the abstract level
**ASN-0091, abstract class section vs. Worked Example 1**: RA-adm covers only "per-state foundation invariants." The composite-boundary properties P4★, P4a (and P7a, which is never mentioned) are discharged *only* in Worked Example 1's concrete trace.
**Problem**: A REARRANGE is itself a composite (K.μ~) whose endpoints are composite boundaries, so Σ' must satisfy P4★ ∧ P4a ∧ P7a to be a valid boundary state. These follow trivially from frame-fixity of C and R, but the abstract Vstream-only class never derives them — leaving the abstract admissibility notion incomplete for guaranteeing Σ' is a valid composite boundary. P7a is not discharged anywhere.
**Required**: Derive P4★, P4a, P7a preservation at the abstract level (one line each from RE-ran/RE-R), or state explicitly that composite-boundary preservation is established only for the REARRANGE_K realiser.

### Issue 4: ChainDisjointAdjacency lemma is buried inline yet load-bearing across sections
**ASN-0091, "Run Decomposition Is Not Invariant"**: the "Inline lemma (ChainDisjointAdjacency)" is stated mid-prose inside the coalescence witness.
**Problem**: This lemma is referenced from the coalescence witness (RE-coal), the equality witness (RE-eq), and Worked Example 4 — three separate sections. A reusable result invoked across multiple sections is a top-level claim, not inline example prose; the current placement forces the reader to locate it inside an unrelated witness.
**Required**: Promote ChainDisjointAdjacency to a named lemma in a claims slot and reference it, rather than embedding it in one witness.

## OUT_OF_SCOPE

### Topic 1: Link-subspace REARRANGE semantics
**Why out of scope**: The Open Questions correctly defer "what semantics rearrangement should carry on the link subspace." REARRANGE_K's CS3 fixes cuts to the content subspace; link-subspace reordering is genuinely new territory.

### Topic 2: Span reconstitution after fragmenting a same-source transclusion
**Why out of scope**: Whether two fragments "jointly reconstitute" the original source span (noted as not established in RE-trans) is a future-ASN question, correctly flagged rather than hand-waved.

META: Not applicable — the ASN defines an operation on arrangement state with abstractly-stated invariants an alternative implementation must satisfy; it is on-track, only verbose.

VERDICT: REVISE
