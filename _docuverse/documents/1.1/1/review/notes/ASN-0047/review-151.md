# Review of ASN-0047

## REVISE

### Issue 1: Promised strengthening of K.μ⁺ to the starred per-subspace forms is never delivered in text

**ASN-0047, K.μ⁺ elementary definition**: "the resulting arrangement satisfies D-CTG ... and D-MIN ...; the per-subspace strengthening to D-CTG★/D-MIN★ is introduced later and **adopted at the K.μ⁺ amendment**, not at this elementary-definition site."

**ASN-0047, K.μ⁺ amendment (ContentSubspaceRestriction)**: "The existing **D-CTG and D-MIN** postconditions carry forward, now complemented by K.μ⁺_L's parallel contiguity and minimum-position preconditions in the link subspace."

**ASN-0047, Class (a) matrix, D-CTG★/D-MIN★ row, K.μ⁺ cell**: "precondition discharge (K.μ⁺'s original precondition list ... requires the resulting M'(d) to satisfy D-CTG/D-MIN — **strengthened to D-CTG★/D-MIN★ in the extended state**...)".

**Problem**: The elementary definition defers the starred strengthening to "the K.μ⁺ amendment." The amendment text then carries forward only the *unstarred* D-CTG/D-MIN. The matrix nonetheless asserts K.μ⁺ discharges the *starred* per-state invariants by a precondition that was "strengthened to D-CTG★/D-MIN★." The locus where K.μ⁺'s precondition actually acquires the starred form is named twice but stated nowhere. Since D-CTG★/D-MIN★ are listed as per-state invariants of ExtendedReachableStateInvariants that every elementary step must preserve, this is a load-bearing gap, not cosmetics.

**Required**: State the strengthening explicitly at the K.μ⁺ amendment — i.e., that the amended K.μ⁺ precondition requires the resulting M'(d) to satisfy D-CTG★/D-MIN★ on the content subspace (link subspace preserved by frame) — so the matrix cell has a referent.

### Issue 2: S3★-under-K.μ~ is argued in three places with overlapping content

**ASN-0047, Generalized referential integrity (S3★ paragraph)**: "K.μ~ preserves S3★ by direct decomposition: K.μ⁻ restricts dom(M(d)) ... K.μ⁺ (amended) adds only content-subspace V-positions ... — S3★ holds for M'(d). The stronger derived property ... is established in *Decomposition of K.μ~* below."

The same preservation is then re-derived at length as Steps (A)→(B) of the dependency chain in *Decomposition of K.μ~* ("What the dependency chain supplies is the *realisability*..."; "the matrix entry ... for S3★ under K.μ~ holds by the admissibility filter ... Step (B) supplies only the realisability"), and again summarised in the Class (a) matrix S3★/K.μ~ cell.

**Problem**: Three statements of the same claim, with the Decomposition version layered in meta-prose about "what each step supplies" rather than advancing the argument. This is the reviser-drift pattern flagged in the anti-bloat note (a quick version plus a full version plus a matrix restatement, bridged by "established below" pointers).

**Required**: Pick the single authoritative site (Decomposition) and reduce the S3★-section sentence and matrix cell to a one-line pointer, dropping the "what supplies what" framing.

### Issue 3: Forward-reference / document-ordering meta-prose in structural slots

**ASN-0047, "Staging of the link store"**: "The link store L and everything that depends on it ... is characterised once, in the *Link store and extended system state* section below. Until that section, every Σ is read with L = ∅, under which all L-related conjuncts are vacuous; no result preceding that section depends on the link store's contents."

**ASN-0047, "System state and initial state (recap)"**: "The consolidated verification of every per-state invariant ... is the *Initial state invariant verification* paragraph at the original definition site, which already covers the link-store invariants on the strength of L₀ = ∅."

**Problem**: Both paragraphs justify document ordering and defer to other locations rather than advancing reasoning — exactly the "multiple paragraphs defer to the same downstream location" and "prose justifies document ordering" patterns the anti-bloat classifier solicits. The reader must skip past them to follow the argument.

**Required**: Delete the staging/recap meta-prose. State L₀ = ∅ once where the initial state is defined; let vacuity of L-conjuncts stand without a paragraph announcing it.

### Issue 4: "What the dependency chain supplies" framing around the K.μ~ admissibility filter

**ASN-0047, Decomposition of K.μ~ (opening)**: "S3★(Σ') for a K.μ~ event holds *by the admissibility filter* ... so the verification-matrix cell for S3★ under K.μ~ is true by construction, not derived from the decomposition. What the dependency chain supplies is the *realisability* that makes K.μ~ a non-vacuous operation..."

**Problem**: This paragraph and the (A)→(B)→(C)→(D)→(E) preamble explain *what each step's role is* before the steps are given, restating "admissibility stipulates / Step (B) realises / fixity is downstream" several times across the section. It is scaffolding about the proof rather than the proof. The substance (Steps A–E and the Decomposition derivation) stands on its own.

**Required**: Cut the role-narration preamble; let Steps (A)–(E) carry their own labels. Keep at most one sentence distinguishing "S3★ holds by the admissibility filter" from "Step (B) shows the decomposition realises an admissible π."

## OUT_OF_SCOPE

### Topic 1: Link-withdrawal mechanism (status flag / tombstone / retraction link)
**Why out of scope**: The ASN correctly confines K.μ⁻ to suffix truncation under D-CTG★/D-MIN★ and records interior link withdrawal as future work (Open Questions). A separate withdrawal mechanism is new territory, not a defect here.

### Topic 2: Abstract node-allocation registry protocol
**Why out of scope**: NodeUniqueAllocation / NodeRegistryBootstrap abstract the external registry as axioms (a guarantee, not mechanics); whether to specify the registry's issuing/persistence/concurrency model is appropriately deferred to a future ASN.

VERDICT: REVISE
