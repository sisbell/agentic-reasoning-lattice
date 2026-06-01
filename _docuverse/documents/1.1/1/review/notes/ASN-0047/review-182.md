# Review of ASN-0047

## REVISE

### Issue 1: TrackedEmission is a load-bearing per-state invariant but is omitted from the maintained invariant set
**ASN-0047, *The state model* (TrackedEmission) and *Extended reachable-state invariants*:** TrackedEmission is declared "Per-state invariant (EntityEmissionTracking)" and FrontierEquivalence opens by consuming it: "for every reachable state `Σ` and every operand `t ∈ Σ.E` with `¬IsNode(t)`, TrackedEmission supplies a tracked entity-level sub-allocator whose domain contains `t` — establishing existence."

**Problem**: FrontierEquivalence is invoked in the K.δ case (ii) k=0 discharge (and the entity-hierarchy worked example) to establish the freshness guard, so its well-definedness — hence TrackedEmission — must hold at every reachable state the main induction reaches. But the `ExtendedReachableStateInvariants` per-state conjunction enumerates every other declared per-state invariant (S2 … CL-UNIQ, including NodeLineage) and omits TrackedEmission; the Class (a) verification matrix likewise has no TrackedEmission row. The induction therefore never formally carries the one invariant FrontierEquivalence's existence claim rests on. (Its definition box gives a standalone preservation sketch, but that is not integrated into the master induction and is not cross-referenced from the conjunction.)

**Required**: Either add TrackedEmission to the `ExtendedReachableStateInvariants` per-state conjunction with a matrix row, or state explicitly in the conjunction that TrackedEmission is established by a separate self-contained induction and cite it where FrontierEquivalence consumes it.

### Issue 2: K.σ-subsumption stated twice in different sections
**ASN-0047, *Typing note (M total)* and *Elementary transitions* (K.δ):** The Typing-note bullet — "*ASN-0093 K.σ effect `dom(M') = dom(M) ∪ {d}`.* … ASN-0047 subsumes K.σ into K.δ for `IsDocument(e)`, whose effect `E' = E ∪ {e}` places `e` into E_doc with `M'(e) = ∅`" — restates the same content as the later K.δ paragraph "*Subsumption of ASN-0093's K.σ.* ASN-0047 has no separate K.σ primitive: when `IsDocument(e)`, K.δ carries document registration through the entry of `e` into `E_doc` (with `M'(e) = ∅` …), subsuming ASN-0093's K.σ."

**Problem**: Two paragraphs in different sections say the same thing in different words — the flagged "same thing in different words" / use-site duplication pattern.

**Required**: Keep the subsumption statement at one site (the K.δ definition) and reduce the Typing-note bullet to a pointer.

### Issue 3: Defensive meta-prose explaining why a lemma does not apply / why a guard is not a conclusion
**ASN-0047, *Link-subspace extension* (K.μ⁺_L) and *K.δ case (ii) discharge*:** Two instances of "explains why … needed rather than what it says":
- K.μ⁺_L: "Note: T7 (SubspaceDisjointness, ASN-0034) does not apply at V-positions because T7's hypothesis is element-level (zeros = 3) while V-positions have zeros = 0; T3 supplies the required distinctness at the V-position depth where T7 does not reach."
- K.δ: "The guard is a precondition, not a conclusion: at k ∈ {1, 2}, GlobalUniqueness (ASN-0034) establishes only that *distinct* allocation events stay distinct … it does not by itself yield `e ∉ E` … The at-most-once firing of each `(t, k')` child-spawn is itself *maintained by* always checking the guard; it is not the source of the guard."

**Problem**: Both passages argue about what a foundation result does *not* do, defending the choice of mechanism rather than advancing the claim. A precise reader must skip past them to reach the substantive discharge (T3 gives distinctness; the guard is checked).

**Required**: Replace the T7 note with the positive statement only ("V-positions differ in their first component, so T3 yields `v_ℓ ∉ V_{s_C}(d)`"); drop the guard-is-not-a-conclusion exposition, retaining only "the guard `e ∉ E` is caller-checked; GlobalUniqueness preserves distinctness thereafter."

### Issue 4: Three composite-boundary properties each defer to the same downstream "Class (b)" location
**ASN-0047, P4★ / P4a / P7a:** P7a — "Stated and proved under Class (b) in the *Extended reachable-state invariants* section." P4a — "Its derivation by induction with J1'★ as the coupling is given under Class (b)." P4★ — restated in *Content-scoped containment and provenance* with its discharge again in the Class (b) matrix.

**Problem**: Multiple paragraphs in different sections defer to the same downstream location — the flagged deferral-accretion pattern. Each property is introduced, partially characterized, and then bounced forward, forcing the reader to reassemble it across three sites.

**Required**: State each of P4★/P4a/P7a once at its definition with a single forward pointer, or move the full statement into the Class (b) discharge and leave only the label at the introduction site.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
The fork composite (J4) leaves the forked document's link subspace empty and notes "A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope." This is correctly deferred; not an error here.

### Topic 2: Interior link withdrawal / tombstoning
D-CTG★ confines K.μ⁻ to suffix truncation, so withdrawing an interior link is unsupported. The ASN catalogues this in Open Questions as needing a separate mechanism. Appropriate future-ASN territory.

VERDICT: REVISE
