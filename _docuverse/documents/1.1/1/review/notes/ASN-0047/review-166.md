# Review of ASN-0047

## REVISE

### Issue 1: Verification matrix includes rows that are not in the invariant set it claims to discharge

**ASN-0047, *Extended reachable-state invariants*, Class (a) verification matrix**: The Class (a) preamble fixes the per-state invariant set as exactly:

> "These are all per-state properties except P4★, P4a, and P7a: S2, S3★, S3★-aux, S4, S7a, S7b, C1b, S7d, S8a, S8-fin, S8-depth, S8★, C-fin, D-CTG★, D-MIN★, D-SEQ★, P6, P7, P8, NodeLineage, L0, L1, L1a, L1b, L1c, L3, L14, L-fin, CL-OWN, CL-UNIQ."

But the matrix immediately below carries two additional rows — **"Entity distinctness (derived…)"** and **"Link distinctness (derived… the L11a obligation in the extended state)"** — that do not appear in that conjunction, and the per-invariant prose then substantiates them as if they were claimed invariants.

**Problem**: A verification matrix advertised as discharging "the per-state invariants" should be in bijection with the stated invariant set. A precise reader checking that every conjunct has a discharge and every discharged row is a conjunct finds two unmatched rows. Either the two distinctness properties are genuine per-state invariants (then they belong in the conjunction and in ExtendedReachableStateInvariants) or they are derived corollaries (then they should be presented outside the matrix, e.g., as lemmas, not interleaved with invariant rows). The current presentation leaves their status ambiguous.

**Required**: Reconcile the matrix rows with the Class (a) conjunction — either add "Entity distinctness" and "Link distinctness" to the enumerated invariant set, or move their verification to a separate derived-corollary paragraph clearly outside the per-state invariant matrix.

### Issue 2: Defensive-justification prose explaining why a clause/axiom is needed rather than stating its content

**ASN-0047, *Link-subspace extension* (m_L(d) definition) and *Elementary transitions* (K.μ⁺)**: Per the anti-bloat directive on this note, two paragraphs argue the *absence* of an axiom or the *consequence of omitting* a clause rather than advancing the claim:

- m_L(d): "This depth is not fixed by a separate axiom — it is pinned operationally… No new axiom is needed: S8a supplies the lower bound, S8-depth supplies fixity, and the operation's precondition supplies the first-insertion choice."
- K.μ⁺: "Without the value-preservation clause, K.μ⁺ could silently replace values at existing positions, conflating extension with replacement. The decomposition of replacement into K.μ⁻ followed by K.μ⁺ depends on each being a pure operation."

**Problem**: Both are defensive justifications ("no new axiom is needed," "without the clause X could happen") that explain why the design is as it is rather than stating what the construct does. The m_L(d) paragraph in particular spends its bulk rebutting a hypothetical "separate axiom" reading that the definition already excludes. This is the reviser-drift pattern the classifier flags: prose the precise reader must work around to reach the operative content (m_L(d) ≥ 2, fixed at first insertion, held by S8-depth).

**Required**: Reduce each to the operative statement. For m_L(d): state the depth, its lower bound (S8a), and its fixity (S8-depth), and drop the "no new axiom needed" rebuttal. For K.μ⁺: the value-preservation clause is already in the effect; the rationale for it belongs in the PR description, not the operation body.

## OUT_OF_SCOPE

### Topic 1: Account-level depth-1 extension semantics
The final Open Question (account renaming / multi-account identity requiring `K.δ k=1` on accounts) is correctly deferred — it is a genuine future extension, not a defect in this ASN's transition set.

### Topic 2: Node-allocation registry protocol
The minimal-protocol question for NodeUniqueAllocation/NodeRegistryBootstrap is genuinely a future-ASN concern; NodeUniqueAllocation as an axiom boundary is an acceptable abstraction for this layer.

VERDICT: REVISE
