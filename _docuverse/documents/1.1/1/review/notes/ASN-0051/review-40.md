# Review of ASN-0051

## REVISE

### Issue 1: Forward reference — Maximal Endset Fragment uses π_text before SV11 defines it
**ASN-0051, Partial Survival section**: The "Definition — Maximal Endset Fragment" uses `π_text(e, d) ∩ I(β_k)` in its formal characterisation, but `π_text` is first defined inside the body of SV11 below it. A reader encountering the fragment definition has no formal grounding for `π_text` and may conflate it with the earlier-defined `π(e, d)` (the full projection).
**Required**: Lift the definition of `π_text(e, d) = coverage(e) ∩ ran_text(M(d))` into the Endset Projection section alongside `π(e, d)`, so both projections are introduced together before any property uses them.

### Issue 2: "Full projection" wording contradicts the formal definition
**ASN-0051, Definition — Maximal Endset Fragment**: "A *maximal fragment* of e in d is a maximal contiguous subsequence of I-addresses within a single mapping block's ordinal sequence taken within the *full* projection."
**Problem**: "Full projection" suggests `π(e, d)`, but the formal predicate uses `π_text(e, d)` (text-subspace only). The link-subspace contribution is explicitly excluded.
**Required**: Replace "full projection" with "text-subspace projection" (or "content-subspace projection") to align prose with the formula. Note explicitly that fragments here are confined to the content subspace, with link-subspace fragments deferred.

### Issue 3: Bilateral vitality defined but never used in any SV claim
**ASN-0051, Endset Projection section** introduces both slotwise and bilateral vitality with a careful semantic split, but no SV-labelled claim (SV2–SV11, SV13) targets either predicate. The forward claims are stated in terms of `π(e, d) ≠ ∅` for individual endsets.
**Problem**: A defined-but-unused predicate signals incomplete coverage. Either bilateral vitality is genuinely load-bearing (and the missing claim should be added — e.g., "BilateralVitalityUnderContraction: bilateral vitality is preserved iff each non-empty endset retains a witness"), or it is documentation only (and that purpose should be stated to prevent the reader from hunting for the missing theorem).
**Required**: Either prove an SV claim using bilateral vitality, or state explicitly that the predicate is introduced for downstream consumers (e.g., link semantics ASNs) without internal use here.

### Issue 4: "Discovery through a document" is informal in SV8 caveat
**ASN-0051, SV8 caveat**: "Discovery through a specific *document* may change, because the document's contribution of I-addresses changes with its arrangement."
**Problem**: The phrase "discovery through document d" is used informally. The SV10 corollary (TransclusionCcouplingAbsence) does formalise `A_Σ(d) = ran(Σ.M(d))` as the document-derived address set, but this is buried in a corollary rather than promoted to a definition. The result is that SV8's caveat reads as informal commentary rather than a precise statement.
**Required**: Introduce a definition like `discover_through(d) ≡ discover_s(ran(M(d)))` (or analogous form) up front, then state the discovery caveat formally: `discover_through_Σ(d)` may shrink across K.μ⁻ even though `discover_s(A)` is permanent for any fixed A.

### Issue 5: SV5 worked-example explanation conflates two distinct preservation claims
**ASN-0051, Worked Example, after-reordering subcase**: The example states `locate(F, d) = {v₂, v₃}` after the swap, then notes "this worked example illustrates a special case where the locate *set* is preserved because the swap exchanges two V-positions that both belong to the locate set."
**Problem**: The witness for SV5's general inequality is given inside the SV5 discussion, but the worked example doesn't exercise it — both v₂ and v₃ are in locate before and after. A reader checking SV5 against the worked example sees set-equality and may wrongly conclude the set is invariant in general.
**Required**: Either choose a worked-example swap that exhibits the set-change behaviour, or add an explicit note in the worked example that this particular swap is degenerate with respect to SV5's general claim and direct the reader to the SV5 discussion witness.

### Issue 6: SV13(e) bullet on K.μ~ omits the locate-set transformation formula
**ASN-0051, SV13(e) third bullet**: States that reordering preserves π(e, d) and that locate is transformed by ψ, but the synthesis simply says "The locate *set* may change."
**Problem**: SV13 is the consolidated guarantee. SV5 establishes the precise form `locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)}`, which is more informative than "may change." A downstream consumer reading only SV13 loses this transformation rule.
**Required**: In SV13(e)'s K.μ~ bullet, restate the transformation rule explicitly: `locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)}` where ψ is the reordering bijection.

## OUT_OF_SCOPE

### Topic 1: Detailed treatment of fork (J4) survivability
The CrossDocumentDecoupling corollary mentions forking once, but a systematic treatment of SV2–SV11 under J4 composites is deferred. This is appropriate for a downstream ASN that builds on both ASN-0047's fork-composite definition and the survivability framework established here.
**Why out of scope**: Forks are valid composites under J4, and the per-elementary-transition analysis here covers them termwise; a synthesis-level fork-survivability theorem belongs after composites have been more fully analysed.

### Topic 2: Broader-level span survivability (k ≤ p₃)
SV6 explicitly bounds itself to element-field action points (k > p₃). The note on the "Content Allocation and Coverage Stability" section defers broader-level spans (account, node, document prefixes) to ASN-0034's allocator/address-hierarchy treatment.
**Why out of scope**: Broader-level coverage growth is by design (Nelson: "may at a later time contain a million documents"); its formal characterisation belongs in the allocator-discipline ASN.

### Topic 3: Same-origin coverage growth formal characterisation
The "Same-origin coverage growth" subsection is descriptive — it identifies the mechanisms (sequential overshoot, child-depth entry) but explicitly disclaims any SV-labelled claim about which same-origin allocations enter which spans.
**Why out of scope**: The precise conditions depend on allocator-discipline choices that belong in ASN-0034, not in the survivability ASN.

### Topic 4: Link-subspace endset contributions to projection
Endsets referencing link addresses (admitted by L4 and isolated by L13's reflexive-addressing case) contribute to projection via K.μ⁺_L, but the detailed analysis is deferred to a future "Link Subspace ASN."
**Why out of scope**: The framework here applies term-for-term; only the link-subspace-specific analysis is deferred.

### Topic 5: Eventual-consistency / latency guarantees for discovery
Open Question 7 asks about discovery latency. This concerns timing semantics outside the abstract state-transition model.
**Why out of scope**: Latency belongs in implementation or distributed-protocol ASNs.

VERDICT: REVISE
