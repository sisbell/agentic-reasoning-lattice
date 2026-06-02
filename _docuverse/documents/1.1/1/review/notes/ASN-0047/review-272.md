# Review of ASN-0047

## REVISE

### Issue 1: Wrong-direction cross-reference — P4a "stated below"
**ASN-0047, Scoped coupling constraints (J1'★ derivation)**: "J1'★ is the *converse* coupling. Its derivation runs wp backward from P4a (Trace witnessing, **stated below**)..."

**Problem**: P4a is defined in the *Coupling and isolation* section, which precedes *Scoped coupling constraints* in document order (the "P4a (Trace witnessing — trace property)" box sits between J0 and J2, above the J1'★ derivation). The parenthetical "(stated below)" points the reader in the wrong direction. The same derivation paragraph correctly treats P4★ as already established (above), so the directional slip is isolated to this P4a pointer.

**Required**: Change "(Trace witnessing, stated below)" to "(Trace witnessing, stated above)", or drop the directional qualifier.

### Issue 2: Editing-history prose in Link-subspace fixity
**ASN-0047, Decomposition of K.μ~ (Link-subspace fixity)**: "For an admissible π this is admissibility clause (v) directly — fixity **is now a *hypothesis*** on the admissible class, **not a theorem derived over it**. The sub-steps below confirm the K.μ⁻ + K.μ⁺ full-clearance realisation is consistent with clause (v)..."

**Problem**: The block is labeled "Link-subspace fixity" and headed by the result "`π(v) = v` for every `v ∈ dom_L(M(d))`", then immediately states the result is actually a hypothesis (clause (v)), then proves a *different* claim (realisation-consistency) in sub-steps (1)–(4). The phrase "is now a hypothesis ... not a theorem derived over it" describes a change from a prior version of the ASN (the demotion of a former theorem to an admissibility clause) rather than advancing the current argument. A reader arriving cold must reconcile a header that promises a derived fixity result with prose that retracts the derivation. The load-bearing content of the sub-steps is *realisability* (`M'(d)|_{dom_L} = M(d)|_{dom_L}` and post-state CL-UNIQ), which is distinct from clause (v) itself.

**Required**: Re-title the block to what the sub-steps actually establish (realisation preserves the link subspace functionally and carries CL-UNIQ to Σ'), and delete the "is now a hypothesis … not a theorem derived over it" framing. State that clause (v) supplies pointwise fixity for admissible π and that sub-steps (1)–(4) show the full-clearance decomposition realises it — without narrating the demotion.

### Issue 3: Near-vacuous restatement of the link-row frame note
**ASN-0047, Class (a) verification matrix (post-matrix prose)**: "The link-row 'frame' cells under K.α, K.μ⁺, and K.μ⁻ are covered uniformly by the matrix note above."

**Problem**: The substantive justification (that link-row `frame` cells rest on the amended `L' = L` conjunct, not the pre-link transitions) is already given in full in the matrix preamble immediately above the table. This trailing sentence is a pure back-pointer that adds no reasoning and forces the reader to confirm it refers to text they have already read. Per the anti-bloat classifier, prose that does not advance the argument is noise to work around.

**Required**: Delete the post-matrix sentence; the preamble note already covers the link-row `frame` cells.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link withdrawal
The ASN's K.μ⁻ contracts the link subspace by suffix removal only, and explicitly defers interior-link withdrawal (compact-and-renumber) to a future ASN (Open Questions, *interior-withdrawal entry*). This is correctly scoped out — modelling `DELETEVSPAN`-style renumbering is new territory, not an error here, and link permanence is independently discharged by L12.

VERDICT: REVISE
