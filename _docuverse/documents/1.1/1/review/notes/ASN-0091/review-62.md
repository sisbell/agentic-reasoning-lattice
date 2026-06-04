# Review of ASN-0091

## REVISE

### Issue 1: Net-effect split restates the same distinction four times
**ASN-0091, "REARRANGE_K Realises the Abstract Class" → *Net-effect split***: "This makes π non-identity *as a permutation of V-positions*, but that is strictly weaker than ASN-0047's K.μ~ admissibility clause (ii)... The realisation therefore splits on net effect, but in both cases a realiser exists — the distinction is only whether the named bundle K.μ~ is available or whether the realiser must be the *unbundled* K.μ⁻ + K.μ⁺ sequence. In the *non-trivial case*... In the *collapse case*..."
**Problem**: The single fact — "π ≠ id is weaker than `M'(d) ≠ M(d)`; the non-trivial case uses K.μ~, the collapse case uses K.μ⁻+K.μ⁺ and yields Σ'=Σ" — is asserted, then re-asserted as "the distinction is only whether...", then again case-by-case, then once more ("clause (ii) ... is borne *solely* by the named bundle"). A precise reader must skip past three reformulations to extract one claim plus one concrete witness.
**Required**: State the distinction once, give the S5 collapse witness once, name the two realisers once. Delete the intervening restatements.

### Issue 2: Repeated deferrals to ExtendedReachableStateInvariants and meta-citation prose
**ASN-0091, RA-adm discharge / "State-Component-Only Invariants" / Worked Example**: "S2 is already established once... we cite it by label here rather than restate it"; "they are not routed through ExtendedReachableStateInvariants"; "The composite-boundary property P7a, by contrast, is discharged once via ExtendedReachableStateInvariants above and not re-claimed here"; "P4a ... is delivered at the K.μ~ composite boundary by ASN-0047's ExtendedReachableStateInvariants, alongside P4★ and P7a."
**Problem**: Multiple paragraphs in different sections defer to the same downstream discharge and narrate the routing ("not re-claimed here," "not routed through," "cite by label rather than restate"). This is protocol rationale about where each invariant is discharged, not advancement of any invariant's content.
**Required**: Discharge each invariant once at its natural site without cross-section bookkeeping prose about which discharge path it travels.

### Issue 3: RE-trans (iii) asymmetry over-elaborated
**ASN-0091, "Cross-Document Transclusion Preserved"**: "*Conclusion (iii)*... requires the additional restriction `origin(a) ≠ d_tgt`... When `origin(a) = d_tgt`... so (iii) does *not* hold... Note that when `d = d_tgt`... the side-condition... is forced... so (iii) holds in that sub-case automatically. The asymmetry between (i)+(ii) and (iii) thus surfaces only when..."
**Problem**: The d-vs-d_tgt distinction is genuine and worth one statement, but the paragraph enumerates every use-site combination (d = d_tgt sub-case, origin(a) = d_tgt case, the surfacing condition) — a use-site inventory that the RE-trans claim row and RE-trans★ row already carry. The reader works through three case-splits to recover one side condition.
**Required**: State (i)+(ii) unconditional, (iii) conditioned on `origin(a) ≠ d_tgt`, in one sentence; drop the enumerated sub-cases.

### Issue 4: "Remaining per-state invariants" discharge asserts K.μ~ validity unconditionally
**ASN-0091, RA-adm discharge → *Remaining per-state invariants***: "With K.μ~'s admissibility clauses (i)–(v) closed above, K.μ~ is a valid composite, so ASN-0047's ExtendedReachableStateInvariants establishes that it preserves the full per-state invariant package..."
**Problem**: Clause (ii) (`M'(d) ≠ M(d)`) holds only in the non-trivial case; in the collapse case K.μ~ is *not* the realiser (the unbundled K.μ⁻+K.μ⁺ is) and RA-adm is discharged separately by triviality (Σ'=Σ). The paragraph asserts "K.μ~ is a valid composite" without scoping to the non-trivial case, so the RA-adm discharge appears to rest on a premise that fails in the collapse case it is also meant to cover.
**Required**: Scope this paragraph explicitly to the non-trivial case, and cross-reference that the collapse case's RA-adm is the trivial Σ'=Σ discharge from the net-effect split.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: The note correctly confines REARRANGE_K's cut subspace to content (CS3, s_C) and frames the link subspace via RE-sub. A REARRANGE that reorders the link subspace, and the invariants it must preserve, is genuinely new territory — appropriately listed as an Open Question, not an error here.

### Topic 2: Reconstitution of a same-source span split across non-contiguous pieces
**Why out of scope**: RE-trans + RE-origin establish each fragment carries its origin; whether two fragments *jointly reconstitute* the source span is explicitly deferred to the first Open Question. This is a future-ASN concern, not a gap in the present claims.

VERDICT: REVISE
