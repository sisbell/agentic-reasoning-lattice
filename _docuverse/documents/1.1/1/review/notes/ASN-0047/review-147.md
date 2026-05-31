# Review of ASN-0047

## REVISE

### Issue 1: Internal contradiction over which step of the K.μ~ chain consumes CL-UNIQ

**ASN-0047, *Decomposition of K.μ~* (dependency-chain preamble) vs. *Decomposition* (necessity argument)**: The chain preamble states "(C) establishes the link-subspace functional identity `M'(d)|_{dom_L} = M(d)|_{dom_L}` (Steps 1–3 …)" and "(D) derives pointwise fixity … (Step 4 below; premise: CL-UNIQ at the pre-state Σ, **the only step consuming it**)." But the necessity argument later writes: "Step (C) gives `M'(d)|_{dom_L} = M(d)|_{dom_L}` **(premise: CL-UNIQ at the pre-state Σ, inductive hypothesis)** and Step (D) gives `π|_{dom_L} = id` pointwise."

**Problem**: These two statements directly contradict each other on whether CL-UNIQ is consumed by Step (C) or only by Step (D). The link-subspace fixity proof's Steps 1–3 are explicitly stated elsewhere to *not* invoke CL-UNIQ (the "Dual consequence" paragraph: "they appeal only to the bijection equation, subspace preservation, K.μ⁺'s amendment … and the K.μ⁻ value-preservation clause"). The necessity argument's attribution is therefore wrong, and it matters: the necessity proof's logical structure depends on which premises Step (C) actually consumes.

**Required**: Correct the necessity argument so Step (C) is cited without CL-UNIQ (matching Steps 1–3 and the chain preamble), with CL-UNIQ entering only at Step (D).

### Issue 2: S9 "follows from P0 unconditionally" — derived guarantee without derivation

**ASN-0047, *Extended reachable-state invariants* / *Properties Introduced***: "ASN-0036's S9 (TwoStreamSeparation) follows from P0 unconditionally." (Repeated in the ExtendedTransitionInvariants entry: "S9 follows from P0.")

**Problem**: S9 is asserted as a derived consequence but no derivation is shown — the premises and the chain are not named. Standard 6 requires derived guarantees to be derived explicitly. This is a one-line argument (every M-mutating transition frames C, so no arrangement op alters the content store), but the ASN states the conclusion as if self-evident.

**Required**: Supply the one-line derivation (the K.μ⁺/K.μ⁺_L/K.μ⁻/K.μ~ frames hold C unchanged, so P0's append-only/immutable content store is untouched by any arrangement mutation), or drop the claim.

### Issue 3: LinkVPositionDepthAxiom asymmetry — content first-insertion depth left underdetermined with no stated reason

**ASN-0047, *Link-subspace extension* (LinkVPositionDepthAxiom)**: The axiom fixes a per-document link-subspace depth `m_L(d) ≥ 2`, justified by "S8-depth forces a common depth among *existing* link-subspace positions but is vacuous when `V_{s_L}(d) = ∅`, so the depth of the *first* link-subspace position is otherwise unconstrained."

**Problem**: This identical underdetermination applies verbatim to the **content** subspace: when `V_{s_C}(d) = ∅`, S8-depth is equally vacuous, and K.μ⁺'s preconditions (S8a + S8-depth + D-MIN★) do not pin the depth `m_{s_C}` of the first content insertion either. Yet no `ContentVPositionDepthAxiom` is introduced, and the link axiom's justification gives no reason for the asymmetry. Either the content subspace needs the same axiom, or the justification must explain why it does not (e.g., that content first-insertion depth is fixed by ASN-0036's `ValidFirstInsertionPosition`, while links have no such foundation predicate). As written, the same gap the axiom is introduced to close is silently left open for content.

**Required**: Either add the content-subspace analog, or extend the axiom's justification to state precisely why the content subspace's first-insertion depth is already determined (citing the foundation mechanism) while the link subspace's is not.

### Issue 4: Redundant A2-dispatch induction retained despite an admitted one-line alternative

**ASN-0047, *K.δ case (ii) discharge…*, sub-case A ("Termination of the A2 dispatch by induction on chain position")**: A multi-sentence well-founded induction on chain position `n(t)` discharges the A2 recursive dispatch, immediately followed by: "(Alternative direct discharge: by T10a.6 …, every emission of `A_account(parent(t))` … inhabits its tracked domain … independent of which K.δ event placed it. The case-split form above is preserved because it parallels the K.δ k ∈ {0,1} discharges and makes the inductive structure explicit.)"

**Problem**: The ASN itself states the entire inductive A2 construction is unnecessary — a single T10a.6 application discharges the obligation directly. Retaining the elaborate induction "because it parallels" is meta-prose that does not advance the argument; the reader must work through a derivation the author concedes is superfluous. This is the reviser-drift pattern flagged in the anti-bloat note (prose retained for parallelism, with a parenthetical admitting a one-line alternative suffices).

**Required**: Replace the inductive A2 dispatch with the direct T10a.6 discharge; drop the parallelism justification.

### Issue 5: Forward-reference duplication in the K.μ~ proof — summary plus "full proof below" for the same case analysis

**ASN-0047, *Decomposition of K.μ~*, "Proof of Step (A)"**: Step (A) summarises the `s_C → s_L` / `s_L → s_C` case analysis, then states: "The full case-by-case proof is in the body's *Case `s_C → s_L`* and *Case `s_L → s_C`* paragraphs." Those two paragraphs then re-present the same two-case L14 contradiction in full.

**Problem**: The same case analysis appears twice — once as a summary in Step (A) and once in full immediately below — with an explicit deferral pointer connecting them. This is the "two paragraphs say the same thing in different words" + "defer to the same downstream location" pattern. The Step (A) summary adds no content the full paragraphs lack.

**Required**: Keep one presentation. Either let Step (A) cite the full paragraphs without restating the derivation, or inline the case analysis once and delete the deferral.

### Issue 6: Use-site inventories and downstream-consumer enumerations (anti-bloat)

**ASN-0047, *Properties Introduced* (FrontierEquivalence entry) and the Class (a) verification-matrix preamble**: The FrontierEquivalence table entry ends "Cited by the K.δ case (ii) k = 0 rationale and freshness discharge, and by the S4 row of the Class (a) verification matrix." The matrix preamble carries four explanatory sub-paragraphs ("Frame entries against link-store invariants…", "K.μ~ entries invoke the full-clearance form…", "K.μ~ admissibility-stipulated invariants vs. mechanically-derived invariants", "Entity-distinctness and Link-distinctness rows are…") whose function is to justify cell labels rather than advance any claim.

**Problem**: These are use-site inventories and defensive justifications in structural slots — the explicitly-flagged anti-bloat patterns. A definition's meaning is not advanced by enumerating its downstream consumers; a matrix's cells are not strengthened by a preamble explaining why "frame" appears where it does.

**Required**: Remove the downstream-consumer inventory from the FrontierEquivalence entry; fold the load-bearing content of the matrix-preamble sub-paragraphs into the relevant cells (or delete where purely defensive).

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: Whether a forked document should carry its source's home links (via K.μ⁺_L steps in the fork composite) is new mechanism, not an error in this ASN's fork definition; it is already correctly deferred in the Open Questions and the J4 discharge ("A mechanism for link inheritance under forking … is outside this ASN's scope").

VERDICT: REVISE
