# Review of ASN-0130

This is a dense note whose load-bearing claims are the registration wp, the acyclicity argument, and the expansion well-typing induction. I checked each against the foundations rather than taking the labels on faith; the verification record below is what supports the verdict.

**What was checked and held:**

- **PR-ENC / PR-ENC-uniq.** The chain identity `shift(x,1) = inc(x,0)` on T4-valid content addresses is correctly derived (TA5(c) rewrites the sig position, TA5-SigValid places it terminally, OrdinalShift adds one there), and C1b's `#E ≥ 2` keeps consecutive shifts within one origin — so residence plus shift-form *is* chain-segmenthood, making PR0(i) well-posed. The uniqueness proof consumes only prefix-freeness and correctly notes that overlap (a decodable suffix) is harmless under start-anchored identity. Boundary: the empty presentation self-excludes — injectivity from the infinite term domain forces infinitely many parse-valid sequences, so the empty sequence cannot be parse-valid (it would be a proper prefix of every other), and validation (i) cannot be discharged without a defined `min(A_def)`.
- **PR-SIG.** The stratification is properly motivated (the two-run mutual-reference loop shows content alone cannot ground typing), the `sig` induction is well-founded on first-registration order via SequentialAtomicTransitions, and the off-discipline failure mode (raw Multi-gate deposits minting witnesses for never-validated starts) is stated rather than hidden. Re-derivation determinism at later deposit events follows from S0 plus PR-ENC-uniq (one run per start, ever).
- **PR0.** Shape conformance checks out (`|F| = 1`, `|G| = n < ∞` for Multi). Registration discipline discharges I1a's premise exactly (every `register_pred` deposit is an `Emit_pdef` deposit branch), and the sharpening to one-active-registration-per-address correctly routes through PR-ENC-uniq making all same-start validated tuples I0-equal. The wp is verified in both directions: the hit direction needs canonical shaping (subtree equality forcing `a' = a` via mutual prefix), the miss direction needs C3's necessity (canonical shaping turns "no I0-equal incumbent" into "no active tuple denoting `a` at all", and the depositing step grows neither `L_R` nor any other active membership), and both off-discipline counterexamples (the `{a, a.x}` denotation split; the raw tuple with unrelated `G''`) are genuine. The scoping is honest — the equivalence is claimed only where it holds.
- **PR1.** Permanence is proved per-step (K.σ/K.λ_sh frames; K.α freshness from ASN-0093) plus induction, not by a single invalid transfer; the tuple side correctly uses L12 across genuine steps via B2/RP-b.
- **PR2.** The event-wise formulation survives de-registration/re-registration. Part (b) is complete: it closes both the deposit branch (no active witness for the own start at any miss) and the hit branch (a hit would need an incumbent whose own deposit the same argument excludes), so self-reference is unconstructible, not merely rejected once.
- **PR3 / PR3a.** Expansion is pinned to a function (fixed traversal order, least-indexed reserved names, fixed assignment order), and the freshness conditions invoked by WT-α and WT-W are exactly the ones PR3's renaming arranges — including the subtle cases: expansion-name binders inside already-expanded arguments are avoided by the "occurring nowhere in the Eⱼ" clause, and reference nodes in domain positions (filter predicates, set-valued domains) are covered because the structural induction passes through WT's filter and set-valued-domain rules with author-name contexts. The k-step PC2 discharge is capture-free and non-interfering as claimed. The "among the parameters" phrasing (rather than "exactly") is the correct strength.
- **PR-VIEW.** The syntactic class excludes precisely the constituents PC3 and UV make view-sensitive; admitting verdict-valued behavior atoms (`tip`, `target_of`, `age`, `is_filtered`, `is_in_chain`, `targets_keyed`) is right, since UV never rewrites them and they are fixed-view reads.
- **PR5 / PR5a.** The parameter reading is sound on PD0's own terms — PD0's side conditions are already phrased for bound values ("reading no state beyond its bound parameters"), so an environment-fixed parameter adds nothing PD0's ground doesn't consume. The lint's exactness-at-starts argument is complete: same-chain starts share length (so prefix forces equality), cross-origin starts extend prefix-incomparable anchors (so prefix between them contradicts length-ordering of prefixes). The worked example's verdicts check against PD0's actual rules: v1's `A_W` is not grow-only and its negated existential fits neither ST route, so refusal is correct; v2's `L_M` existential with a step-constant V-TUP body under the parameter reading is ST by the quantifier rule. The permanence paragraph correctly separates what is permanent (the expansion, its view-independence, its ST class) from what is not (the target's active registration), and notes why the lint is unharmed.
- **Seal coherence.** Extending the uniform exclusion to `pdef`/`pd_stable` leaves every transferred ASN-0128 result intact (SD/DR reasoning is about derivations, the wrapped emits keep I1's contract), and is the same structural move S3 makes for [R].
- **Citations.** Every cross-ASN reference is to a listed foundation; no foundation notation is reinvented (`coverage`, `addrs`/`enc`, `subtree`, slice notation `A_K`/`L_K`/`M_K` all used as defined upstream).

## REVISE

None. I found no claim whose proof is missing a case, no boundary left unhandled (empty presentation, `k = 0` signatures, first-ever registration, re-registration, self- and mutual reference, born-nullified deposits, de-registered referents at evaluation, overlapping runs, branch/⊥ at `tip` were all checked), and no derived label without its derivation.

## OUT_OF_SCOPE

### Topic 1: The concrete encoding format
**Why out of scope**: PR-ENC fixes the discipline (injectivity, prefix-freeness, decidable self-delimiting parse, reserved expansion-name supply) and everything downstream consumes only those properties; the byte format is a substrate parameter, parallel to the subspace identifiers, and the note says so explicitly.

### Topic 2: Activation / trigger binding
**Why out of scope**: binding predicates to emissions is protocol-layer territory ASN-0129 already fenced off; this note correctly limits itself to noting that a `pdef` address can serve as the P.

### Topic 3: Certifier completeness and further certificate classes
**Why out of scope**: sound-but-incomplete is the committed stance; completeness of the syntactic ST check is ASN-0129's Open Question 5 inherited, and SF/footprint/view-independence certificates are catalog growth for a future note.

### Topic 4: Naming, portability, and dangling-live-reference policy
**Why out of scope**: open questions 1–3 are policy choices, not soundness gaps — the note proves standing registrations, certificates, and evaluation are unaffected by de-registration, so what remains is genuinely a design decision for a successor note.

VERDICT: CONVERGED
