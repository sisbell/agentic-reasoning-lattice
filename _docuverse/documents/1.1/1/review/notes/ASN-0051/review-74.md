# Review of ASN-0051

## REVISE

### Issue 1: SV11 attainment biconditional — proof of (⇒) surjectivity argument has a gap
**ASN-0051, SV11 (⇒) direction**: "By surjectivity of Φ, the codomain cardinality (the fragment count) is bounded by the domain cardinality (the non-empty-term count), which is in turn bounded by m · p (the total term count)"

**Problem**: Surjectivity of Φ from a finite set A to a finite set B gives |A| ≥ |B|, not |A| ≤ |B|. The proof has the inequality direction wrong: surjectivity bounds the codomain BELOW by the domain, so |non-empty terms| ≥ |fragments|. The conclusion needs this corrected direction. The argument still works (fragment count ≤ non-empty term count ≤ m·p, with equality at m·p forcing both), but the cited direction of surjectivity is backwards.

**Required**: Either restate as "surjectivity gives |non-empty terms| ≥ |fragments|, so |fragments| ≤ |non-empty terms| ≤ m · p" or rephrase to make the bounding direction unambiguous.

### Issue 2: SV6 four-case lemma — case (IV) verification missing exhaustiveness check
**ASN-0051, SV6 proof, "Four-case structural lemma"**: "(IV) #y ≠ #e and no prefix relationship holds"

**Problem**: The four cases are claimed exhaustive but the boundary between (III) and (IV) at "no prefix relationship" needs explicit handling when #y < #e. Specifically, when #y < #e and y is not a prefix of q_{k₁} (so y diverges from q_{k₁} at some p ≤ #y < #e-1), this goes to case (IV). But the text says case (IIIa) requires "y must be a prefix of q_{k₁}" — when #y < #e and y is NOT a prefix of q_{k₁}, case (IIIa) is excluded, leaving case (IV). The proof's case-(IV) treatment then uses position p ≤ min(#y, #e − 1), which is well-defined, but the routing from "#y < #e and not a prefix" to case (IV) is implicit rather than stated.

**Required**: One sentence making the case routing explicit: "If #y < #e and y is not a prefix of any β_{k₁}-element (excluding case (IIIa)), then by the structure of β_{k₁}-elements y must diverge from q_{k₁} at some p ≤ #y ≤ #e − 1, placing y in case (IV)."

### Issue 3: SV13(h) BilateralVitality predicate is over-specified
**ASN-0051, Endset Projection section**: "`F ≠ ∅ ∧ π(F, d) ≠ ∅`   and   `G ≠ ∅ ∧ π(G, d) ≠ ∅`"

**Problem**: The conjunct `F ≠ ∅` is redundant given `π(F, d) ≠ ∅`: if F = ∅, then coverage(F) = ∅ (vacuous union), so π(F, d) = ∅. Therefore `π(F, d) ≠ ∅` implies `F ≠ ∅` definitionally. The "and" is presented as separating two independent conjuncts, when one implies the other.

**Required**: Either acknowledge the redundancy as intentional emphasis ("equivalently: `π(F, d) ≠ ∅ ∧ π(G, d) ≠ ∅`, since π non-emptiness implies endset non-emptiness") or simplify the predicate.

### Issue 4: SV5 composite-endpoint reading needs clearer separation of two different "intermediate states"
**ASN-0051, Worked Example, K.μ~ admissibility note**: "We name the post-K.μ~ state `M_reord(d)` — 'reordered' — reserving the term 'intermediate' for the SV5-style elementary-stage state internal to K.μ~ (post-K.μ⁻, pre-K.μ⁺), which has contracted domain and is a different state from the one named here."

**Problem**: The naming convention is established only inline within Step 1, after the reader may have already been confused. The distinction between (i) the SV5-style internal state within a single K.μ~ (contracted domain), (ii) the post-K.μ~ state M_reord(d) (full domain, reordered), and (iii) the post-Stage-2-K.μ⁻ state M'(d) (contracted to 4 positions) is critical for the SV14(d) witness instantiation. The witness instantiation says: "instantiate SV14(d)'s `Σ →_{K.μ⁻} Σ'` existential with the elementary K.μ⁻ step `Σ_reord →_{K.μ⁻} Σ'`" — readers must distinguish these three states to follow.

**Required**: Either introduce the state-naming convention up-front (before Step 1) or add a brief table mapping the three states (Σ, Σ_reord, Σ') to their domains and arrangements.

### Issue 5: Coverage paragraph's "in any order" lift commutativity is asserted without verification
**ASN-0051, SV11 Coverage paragraph**: "apply (α) `m* − 3` times and (β) `p* − 3` times in any order starting from W(3, 3)"

**Problem**: "In any order" requires that (α) and (β) commute when applied to W(m, p) — i.e., (α)∘(β)(W(m, p)) = (β)∘(α)(W(m, p)). This is plausible since (α) modifies (m, sibling count, span set) and (β) modifies (p, block count), but the equality of intermediate parameters at the lifted blocks needs verification. Specifically, after (β) the new block β_{p+1} has I-extent identical to β_p; when (α) is then applied, β_{p+1}'s extent grows by 2 alongside β_p's, maintaining identity. The commutativity holds, but the ASN doesn't show it.

**Required**: Either add a one-paragraph commutativity verification ((α)∘(β) and (β)∘(α) both yield W(m+1, p+1) with identical block sizes and span configurations), or weaken "in any order" to a specific order ("apply (β) first, then (α)") with a note that the alternative order is verified analogously.

## OUT_OF_SCOPE

### Topic 1: Same-origin coverage growth at sub-element levels
**Why out of scope**: Explicitly deferred to ASN-0034's allocator-discipline treatment. The ASN correctly states "this ASN makes no formal SV claim about same-origin coverage growth" and provides descriptive content motivating SV6. The detailed coverage-growth conditions belong with the allocator-hierarchy machinery.

### Topic 2: Broader-level spans (k ≤ p₃)
**Why out of scope**: Explicitly noted in the SV6 scope discussion. Spans with action point at or before the third field separator (covering across document, account, or node prefixes) are admitted by L4 but their survivability behavior requires the prefix-region allocator discipline, deferred to ASN-0034.

### Topic 3: Link-subspace contribution to projection
**Why out of scope**: Explicitly deferred to the Link Subspace ASN. The note acknowledges π_text(e, d) ⊆ π(e, d) and that K.μ⁺_L can add link-address contributions to the projection, but full treatment requires the reflexive-addressing machinery from L13.

### Topic 4: Bilateral vitality survival across forks (J4)
**Why out of scope**: Listed in Open Questions; depends on fork operation semantics (J4 in ASN-0047) which are themselves a composite of K.δ + K.μ⁺ + K.ρ. The survivability analysis composes the SV claims slot-by-slot through the elementary stages; the specific composite-level guarantees for forks belong with the version-graph treatment.

### Topic 5: Discovery latency / eventual consistency
**Why out of scope**: Listed in Open Questions; touches on system-architecture timing properties orthogonal to the I-space/V-space survivability model developed here.

VERDICT: REVISE
