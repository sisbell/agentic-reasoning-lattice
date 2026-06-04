# Review of ASN-0091

## REVISE

### Issue 1: Collapse-case realiser claim conflates an operation invocation with the empty transition

**ASN-0091, "REARRANGE_K Realises the Abstract Class" / Net-effect split**: "in the *collapse case* (`M'(d) = M(d)` with π ≠ id) the transition is already the reflexive `Σ' = Σ` of ASN-0093's SequentialTransitionAxiom, so no realiser is needed and every RE-* claim below holds trivially as an identity."

**Problem**: REARRANGE_K is partial, "defined exactly where R-PRE(K) holds" (ASN-0084), and R-PRE does *not* include `M'(d) ≠ M(d)`. The collapse witness you supply (w_α = w_β = 2, cuts `([1,1],[1,3],[1,5])`, shared content under S5) satisfies R-PRE, so REARRANGE_K **is** invoked and produces `Σ' = Σ`. But its claimed realiser, the named composite K.μ~, has admissibility clause (ii) `M'(d) ≠ M(d)`, which fails here — so K.μ~ is *not* a valid composite in this case. The phrase "no realiser is needed ... reflexive `Σ' = Σ` of SequentialTransitionAxiom" sidesteps this: SequentialTransitionAxiom's reflexive closure is the *empty* transition sequence (zero atomic steps), which is not REARRANGE_K being applied. You leave REARRANGE_K(collapse) without a justified status as a member of the transition relation.

**Required**: Either (a) state that the collapse-case transition is realised by the *unbundled* K.μ⁻ + K.μ⁺ sequence (each elementary step is independently valid; only the named bundle K.μ~ carries clause (ii)), and that RA-adm holds at `Σ' = Σ` trivially; or (b) tighten REARRANGE_K's partiality so it is undefined when the construction would yield `M'(d) = M(d)`, and state this explicitly. As written, "no realiser is needed" is incorrect — a realiser exists, just not K.μ~.

### Issue 2: RA-adm discharged twice over for the same invariants

**ASN-0091, "Remaining per-state invariants" vs. "State-Component-Only Invariants"**: The first says ExtendedReachableStateInvariants discharges "S3★, S3★-aux, CL-OWN, CL-UNIQ, S8★ — together with the co-occurring ASN-0036 foundation and ASN-0093 substrate invariants and the composite-boundary properties P4★, P4a, and P7a." The second separately discharges "S4, S7a, S7b, S7d ... P6, P7, P7a, P8, NodeLineage, ActivatedEmission, L0, L1, L1a, L1b, L1c, L3, L14, L-fin, C1b, C1c ..." via frame inheritance.

**Problem**: A large set (S4, S7a, S7b, S7d, P6, P7, P7a, P8, NodeLineage, ActivatedEmission, L0, L1, L1a, L1b, L1c, L3, L14, L-fin, C1b, C1c, S8a, S8-fin, S8-depth, C-fin) is claimed discharged by *both* mechanisms. These invariants depend only on components RA-frame fixes verbatim, so the simpler frame-inheritance argument suffices; routing them through ExtendedReachableStateInvariants ("together with the co-occurring ... invariants") is redundant over-claiming. This is the flagged anti-bloat pattern: two paragraphs in different sections discharging the same content.

**Required**: Partition cleanly. Let ExtendedReachableStateInvariants discharge only the genuinely arrangement-dependent invariants it is needed for — `{S3★, S3★-aux, CL-OWN, CL-UNIQ, S8★}` and the composite-boundary `{P4★, P4a, P7a}`. Delete "together with the co-occurring ASN-0036 foundation and ASN-0093 substrate invariants" from the ExtendedReachableStateInvariants paragraph and let the State-Component-Only section own them exclusively.

### Issue 3: S2 derived twice with explicit cross-deferral

**ASN-0091, "S2 derivation at the abstract level" and "Shape package"**: S2 is fully derived in the abstract section, then the shape-package layer states "S2 additionally follows from the realiser-independent abstract derivation in 'REARRANGE as Vstream-Only Operation' (RA-dom, RA-π's bijectivity, pre-state S2)."

**Problem**: The same conclusion is established in two places, with the second deferring back to the first. Minor, but it compounds the redundancy of Issue 2.

**Required**: Derive S2 once (abstract section) and let the shape-package layer cite it by label without restating its premises.

## OUT_OF_SCOPE

### Topic 1: Joint reconstitution of a same-source span split across a cut
The RE-trans discussion correctly notes that each fragment carries its origin (RE-origin) but that whether two fragments *jointly reconstitute* the source span is not established. This is properly deferred to the first Open Question — new territory, not an error here.

### Topic 2: Rearrangement semantics on the link subspace
CS3 fixes the cut subspace to `S = s_C`, so link-subspace reordering is structurally outside REARRANGE_K. Correctly deferred to the second Open Question.

VERDICT: REVISE
