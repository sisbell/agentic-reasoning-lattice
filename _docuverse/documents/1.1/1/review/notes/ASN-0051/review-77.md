# Review of ASN-0051

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Link-subspace projection contribution
The ASN restricts SV11 and the partial-survival analysis to the text-subspace projection `π_text(e, d)`, explicitly deferring link-subspace contributions ("the Link Subspace ASN") and reflexive-addressing cases.
**Why out of scope**: This is a deliberate scoping choice; the SV11 machinery (decomposition terms, maximal fragments, attainment) extends to link-subspace contributions term-for-term using the same B-block structure, and the deferral is acknowledged.

### Topic 2: Broader-level spans (action point k ≤ p₃)
The ASN explicitly does not formalize survivability for spans whose action point lies at or before the third field separator (spans that cross document, account, or node prefixes).
**Why out of scope**: The ASN provides three reasons (SV2–SV5/SV11 carry through symmetrically, SV6 exclusion is by design replaced by opt-in allocator growth at broader levels, and no implementation evidence exists from udanax-green). Treatment belongs in ASN-0034's address-hierarchy machinery.

### Topic 3: Higher-arity links (|L(a)| > 3)
The ASN works within the standard-triple framework (F, G, Θ).
**Why out of scope**: L3 admits |L(a)| ≥ 3. The ASN scopes to N = 3 and notes that the generalisation to N > 3 follows by applying SV2–SV13 slot-wise.

### Topic 4: Same-origin coverage growth as a formal SV claim
The ASN treats same-origin coverage growth (sequential overshoot, child-depth entry) descriptively rather than as a formal SV claim.
**Why out of scope**: The ASN correctly identifies that this is allocator-discipline-dependent and defers formal treatment to ASN-0034. The descriptive content suffices to motivate the SV6 cross-origin formal claim and to clarify that endset coverage stability is architectural rather than definitional.

### Topic 5: Open questions enumerated at the end
The ASN lists eight open questions (resolution under within-document sharing, dormant link revival mechanism, canonical fragment ordering, etc.).
**Why out of scope**: These are explicitly framed as questions for future ASNs.

## Observations on rigor (not REVISE items)

The proofs are uniformly explicit. SV6's sandwich argument carries the no-early-divergence reduction through a three-case T1 decomposition (t = s, s ≺ t, divergence at j) without "by similar reasoning" skips. SV11's biconditional proof uses an explicit surjection Φ and discharges both directions. The four-case structural lemma for the SV11 disjoint-pair non-attainment (I/II/IIIa/IIIb/IV) handles the awkward `#y < #e` non-prefix boundary case by explicit case routing. The inductive lift schema for SV11 attainment supplies explicit per-recipe verifications for (α), (β), (α_2), (β_2) and proves (α)/(β) commutativity by exhibiting both compositions and comparing endpoints. The Worked Example's three-span variant exhibits both mechanism (a) and (b) of the SV11 biconditional jointly. SV14(d)'s witness instantiation explicitly threads a fresh K.λ allocation through the Worked Example's composite and verifies the strict shrinkage.

Foundation citations are abundant and accurate (T0, T0(a), T1, T3, T4, T4b, T5, T7, T8, T10a, T10a.4, T12, TA0, TA5, TA5a, TA5-SigValid, D0, D1, D2, S0, S2, S5, S7, S7b, S7c, S7d, S8a, S8-depth, S8-fin, S0 convexity, L0, L3, L4, L9, L12, L12a, L13, L14, M0/M1/M3, M7, M11, M12, C1a, K.μ~-FIX, J0, J1★, P1, P2, D-CTG, D-MIN, D-SEQ, NoDeallocation/AllocatedSet via T8, OrdinalShiftBase). No non-foundation ASNs are referenced by number.

The state-naming convention in the Worked Example (Σ, Σ_int_kμ~, Σ_reord, Σ') is a good engineering choice for distinguishing the SV5-style internal stage from the K.μ⁻-trailing endpoint that SV14(d) reads.

VERDICT: CONVERGED
