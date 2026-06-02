# Review of ASN-0047

## REVISE

### Issue 1: Document-organization meta-prose in §K.δ case (ii) discharge
**ASN-0047, §K.δ case (ii) discharge and parent-allocator activation (opening paragraph)**: "This section is the single owner of the per-k parent-allocator identification: every other site (the K.δ box, the worked examples) cites here... We consume one reusable primitive from ParentAllocatorDispatch... but the per-k organisation itself lives only here."

**Problem**: This is prose about *where content lives in the document*, not about the system being specified. It enumerates downstream consumers ("the K.δ box, the worked examples") and justifies document ordering ("lives only here") — exactly the forward-reference accretion the anti-bloat classifier flags. A reader chasing the parent-allocator discharge must skip past this to reach the per-k content.
**Required**: Delete the opener; begin the section with the substantive k=0/k=1/k=2 discharge. The fact that other sites cite this one is self-evident from the citations and needs no announcement.

### Issue 2: Same downstream location deferred to from multiple sites
**ASN-0047, K.δ box and both worked examples**: K.δ box — "Identification of the parent allocator each step acts on, and the spawnPt premise — for every k including the k = 0 freshness dispatch: §K.δ case (ii) discharge and parent-allocator activation." The two fork worked examples each repeat a deferral ("Owning allocator via ParentAllocatorDispatch", "A_v(d₁) activation discharge ... Per the K.δ k = 1 case discharge").

**Problem**: Three sections in different parts of the document defer the same obligation (parent-allocator identification) to one downstream section. This is the "multiple paragraphs defer to the same downstream location" accretion pattern. The deferrals add navigation overhead without advancing any local argument.
**Required**: State the discharge once at its owner and let the worked examples instantiate concretely (a concrete trace is not meta-prose); drop the explicit "per the §X discharge" pointers, which restate the citation graph rather than the reasoning.

### Issue 3: Definition introductions that enumerate downstream consumers
**ASN-0047, J-LV (Link-subspace provenance vacuity)**: "Two consequences follow, **cited throughout the provenance reasoning**: (i) *no trigger*... (ii) *no witness*..." and **P4★** prose: "P4★ bounds provenance by the content-subspace restriction of containment, **scoped so it coexists with P7**... the link-subspace pairs that an unscoped Contains(Σ) ⊆ R would demand are exactly the ones P7 forbids."

**Problem**: J-LV's "cited throughout the provenance reasoning" is a use-site inventory; the consequences stand on their own. P4★'s scoping paragraph is a defensive justification of why the property is scoped (rationale) rather than a statement of what it asserts. Both make the reader process accretion before the actual claim.
**Required**: For J-LV, state the two consequences without the "cited throughout" framing. For P4★, state the bound `Contains_C(Σ) ⊆ R`; the coexistence-with-P7 rationale belongs (at most) in a single terse parenthetical, not a justifying clause.

### Issue 4: Properties Introduced "Valid composite" row misstates validity conditions
**ASN-0047, Properties Introduced table, "Valid composite" row**: "Σ →* Σ' valid iff: (1) elementary preconditions at each intermediate state, (2) J0/J1★/J1'★ for the composite; **P0/P1/P2 derived as lemma**."

**Problem**: ValidComposite★ in the body defines validity by clauses (1) and (2) only; P0/P1/P2 are per-transition monotonicity facts (synthesized as P3 under *Destruction confinement*), not validity conditions and not "derived as lemma" from ValidComposite★. Appending "P0/P1/P2 derived as lemma" inside the validity definition conflates two distinct notions and contradicts the body's ValidComposite★.
**Required**: Drop the "P0/P1/P2 derived as lemma" fragment from the validity row, or relocate it to the P3/ExtendedTransitionInvariants entry where it belongs.

## OUT_OF_SCOPE

### Topic 1: Interior link-subspace deletion (renumbering-aware contraction)
**Why out of scope**: The ASN already records this as an Open Question (K.μ⁻ models suffix removal only; the implementation's interior `DELETEVSPAN` compacts-and-renumbers). Operation specifications including DELETEVSPAN are explicitly out of scope per the Scope section, so the missing interior-contraction operation is future territory, not a defect here.

### Topic 2: Transitive transclusion-chain provenance guarantees
**Why out of scope**: Listed in the ASN's own Open Questions; provenance over chains of transclusion introduces new state obligations beyond the single-hop K.ρ recording this ASN specifies.

VERDICT: REVISE
