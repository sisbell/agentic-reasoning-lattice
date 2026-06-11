# Review of ASN-0115

The mathematics of this ASN is in good shape — I checked the Confinement lemma (TumblerAdd prefix-copy + T5), the deep-case override argument (both sub-cases close correctly), UnitSpec (b)–(d), the R6 frontier analysis (canonical start forced by D-SEQ★ + Confinement, no-interior-hole, terminal overrun), the R7 agreement argument including the depth re-pinning step, and the R8 vacuity argument (CL-OWN forcing `d = d'`, CL-UNIQ forcing `v = v'`); all five worked instances check out against their claims. The remaining issues are one unsound proof discharge, one compressed-and-forward-deferred derivation, and accumulated meta-prose flagged under the anti-bloat mode.

## REVISE

### Issue 1: Cross-substrate invariant discharge — M0 (and SD) cited over the wrong state space
**ASN-0115, UnitSpec proof (a) and "The substrate we build on"**: "`zeros(d) = 2` by M0 (DocumentTumblerWellFormed, ASN-0093) … applicable because the standing reachability precondition places `Σ` in M0's range." Also: "Content and link stores are disjoint (ASN-0093, SD)."
**Problem**: The standing precondition makes every `Σ` an *ASN-0047*-reachable state (the ASN says so explicitly, and the R11 worked instance uses K.μ⁻ and forking — ASN-0047 vocabulary). M0 is an invariant of ASN-0093's substrate, whose transition vocabulary is only K.σ/K.α/K.λ. Nothing establishes that ASN-0047-reachable states lie "in M0's range," and the transfer pattern is demonstrably unsound: ASN-0093's M2 (EmptyArrangement) is an invariant of the same range and is false at every ASN-0047 state with a populated arrangement. The fact being discharged is true, but via ASN-0047's own structure: `dom(M) = E_doc` (ASN-0047, M1) and `Document(d)` (ASN-0045) give `T4-valid(d) ∧ zeros(d) = 2`. The SD citation has the same shape: the in-model invariant over ASN-0047 states is L14 (StoreDisjointness), which ASN-0047 lists in ExtendedReachableStateInvariants — SD (ASN-0093) is the wrong route even though the conclusion is identical.
**Required**: Re-route both discharges through ASN-0047's invariants — UnitSpec (a) via `dom(M) = E_doc` + Document (ASN-0045); store disjointness via L14 (ASN-0047) — and delete the "places Σ in M0's range" justification.

### Issue 2: Nominal-extent attainment biconditional is asserted before, and not fully covered by, its supporting analysis
**ASN-0115, §"Exactness and arrangement-relativity"**: "The delivered quantity attains the nominal extent, `|act(ρ, Σ)| = ℓ_{#ℓ}`, iff the spec is depth-compatible at `Σ` and every member of the bindable slice is bound … Both directions follow from the R6 frontier analysis."
**Problem**: This is a compressed multi-branch proof presented as a one-line deferral, and the deferred analysis does not actually cover all branches. R6's frontier analysis establishes bound-iff-`k ≤ n_S` only in the `V_S(d) ≠ ∅ ∧ #s = m_S(d)` case. The biconditional additionally needs: (i) the depth-incompatible branch — `act = ∅` while `ℓ_{#ℓ} ≥ 1`, where `ℓ_{#ℓ} ≥ 1` rests on ActionPoint's postcondition `w_{actionPoint(w)} ≥ 1` and is nowhere cited; (ii) the `V_S(d) = ∅` branch — the slice is non-empty (`ℓ_{#ℓ} ≥ 1` members) and wholly unbound, so both sides are false; (iii) the step `act ⊆` depth-`#s` slice, which needs S8-depth and appears only inside the later R6 body. Compounding this, the paragraph defers three times to a section that has not yet occurred ("the bindable slice of §'Partial delivery'", "the canonical start that a non-empty act forces (§'Partial delivery')", "the R6 frontier analysis") — claim stated ahead of every piece of its apparatus.
**Required**: Either move the nominal-extent corollary after the R6 frontier analysis, or assemble the three-branch argument in place: depth-incompatible (`act = ∅ ≠ ℓ_{#ℓ} ≥ 1`, citing ActionPoint), `V_S(d) = ∅` (slice wholly unbound), and the S8-depth step placing `act` inside the depth-`#s` slice.

### Issue 3: Anti-bloat — defensive justifications in claim slots and intra-section duplication
**ASN-0115, multiple sections** (this note carries `review-mode.anti-bloat`):
- **R7 box**: "The relabelling is harmless precisely because spec-set-hood is anchored at the earlier state, whichever member was given first." — a defense of the WLOG inside the claim statement; this is prior-finding-response prose, not claim content. The box also carries the M1 discharge ("M1 (ArrangementMonotonicity, ASN-0047) at each atomic step of `Σ →* Σ'` gives `dom(Σ.M) ⊆ dom(Σ'.M)`") — proof material in the claim slot; the box should state the hypothesis and conclusion, with discharge in the body.
- **§Faithfulness**: "R2 is a *single-state* denotational equality, and the invariants it needs are correspondingly few." — explains why invariants are *not* cited rather than what R2 says. And the frame limit is stated twice in adjacent sentences: "So R2 governs the denotation of `deliver`; it does not promise that an intervening wire delivers those bytes intact. This is a *frame limit*, not a claim: the abstract specification asserts faithfulness … and asserts nothing about the medium." — same content, two phrasings.
- **§Arrangement-relativity (R4 body)**: "Naming `dⱼ` does *not* freeze that arrangement, however: resolution is against the *current* `Σ.M(dⱼ)`, which is mutable …, so naming a version does not freeze it." — the sentence's head and tail say the same thing.
- **UnitSpec preamble**: "Several worked instances below need a spec that names *exactly one* bound position" — a use-site inventory justifying the lemma's existence. The substantive half ("'names `v`' alone does not determine a span, since many ordinal spans contain `v`…") is worth keeping; the consumer enumeration is not.
**Problem**: Each instance is meta-prose the precise reader must skip past — justification of document structure, defense of hypotheses, or restatement — and several have the shape of relocated responses to prior findings rather than removed ones.
**Required**: Strip the duplicated sentences and the WLOG/use-site defenses; move the M1 discharge from the R7 box into the body proof.

## OUT_OF_SCOPE

### Topic 1: Failure semantics for ill-formed requests
A spec naming an unallocated document (`d ∉ dom(Σ.M)`) or a malformed span violates V-spec well-formedness, and the ASN deliberately stops there (its R6 boundary note and Open Question 2 both acknowledge this).
**Why out of scope**: Behavior under precondition violation — error signalling, whole-request failure — is new territory the ASN correctly poses as an open question, not a gap in the delivery semantics it defines.

### Topic 2: Formal placement of RETRIEVEV in a query vocabulary
The ASN asserts pure-query status informally ("modifies no component of `Σ` and appears in no transition of the substrate's vocabulary, cf. ASN-0086, Observe") without giving RETRIEVEV an operation signature in the style of ASN-0086's `Observe_K`.
**Why out of scope**: A query-algebra treatment (signatures, view selectors, decidability of the resolution procedure) is a future ASN; the denotational definition here is self-sufficient for the invariants it proves.

VERDICT: REVISE
