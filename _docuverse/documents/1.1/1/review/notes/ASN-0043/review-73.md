# Review of ASN-0043

## REVISE

### Issue 1: T10a.8 is cited as a foundation claim but is not in the foundation

**ASN-0043, L9 (Case B), L11b, Worked Example Step 1**: "By T10a.8 (UniformSiblingZeroCount, ASN-0034) `zeros(a) = zeros(b) = 3`" / "T10a.8 (UniformSiblingZeroCount, ASN-0034) gives `zeros(a') = zeros(a) = 3`" / "`zeros(a') = zeros(a) = 3` by T10a.8".

**Problem**: The ASN-0034 foundation supplied for this review defines T10a.1 through T10a.7 and T10a-N — there is no T10a.8 (UniformSiblingZeroCount). The zero-count-preservation step under `inc(·, 0)` is load-bearing in three separate places (L9 Case B freshness/zero-count, L11b conformance, worked-example Step 1), and each discharges it by citing a foundation claim that does not exist in the foundation. The fact itself is true (TA5(c): `inc(·, 0)` modifies only the `sig` position, incrementing a nonzero component, so no zero is added or removed) but it is not licensed by the cited authority.

**Required**: Either derive zero-count preservation inline from an existing foundation claim (TA5(c) + TA5-SigValid) at each use site, or — if T10a.8 genuinely exists in ASN-0034 — confirm it belongs to the foundation set. As written against the provided foundation, the citation cannot be discharged.

### Issue 2: L9 reasons at length about a case its own precondition excludes

**ASN-0043, L9**: "The excluded case `dom(Σ.M) = ∅` requires constructing a fresh document, which presupposes the system's allocator tree 𝒯 (S7d, ASN-0036) admits document-level allocation — equivalently, `zeros(r) ≤ 2` on the carrier root `r` of 𝒯. T10a's discipline forces this whenever any document is reachable from `r` ... but the joint L- and S-invariants do not constrain `r` itself, so a malformed empty state with `zeros(r) > 2` would vacuously satisfy them while precluding any document allocation. The cleanest fix is to restrict L9 to states with at least one document..."

**Problem**: This is reviser drift — a full paragraph analyzing the carrier-root question for `dom(Σ.M) = ∅`, a case the precondition `dom(Σ.M) ≠ ∅` already excludes. The paragraph narrates the design decision ("The cleanest fix is to restrict L9...") rather than advancing the claim. Once the precondition is stated, the excluded case needs no carrier-root excursion.

**Required**: Reduce to one sentence noting the precondition's scope (`dom(Σ.M) ≠ ∅` is the natural regime, satisfied by any state from or into which a link is added) and drop the `zeros(r)` analysis.

### Issue 3: L1c narrates the draft's own revision history

**ASN-0043, L1c, "Why `k₁ = 2`, not `k₁ = 1`"**: "The earlier draft admitted `k₁ ∈ {1, 2}` for symmetry with TA5's general step-size admission, but `k₁ = 1` is structurally unreachable by a position-of-zero argument..."

**Problem**: "The earlier draft admitted..." is meta-prose about the editing process, not object-level content. The structural argument that follows is legitimate, but it should be stated in its own terms, not framed as a correction to a prior revision. This is exactly the accretion pattern the anti-bloat classifier targets.

**Required**: Delete the "earlier draft" framing; state the `k₁ = 2` necessity argument directly.

### Issue 4: Use-site inventories instead of meaning-advancing prose

**ASN-0043, multiple sites**:
- PrefixSpanCoverage: "It is invoked in this ASN by L10 (TypeHierarchyByContainment), L13 (ReflexiveAddressing), and the L8 worked-example coverage computations."
- *Notation from ASN-0036*: "We use `dom(Σ.M)` ubiquitously below — in L1a, the worked example, and the L9/L11b proofs."
- L-fin: "...the extension proofs (L9, L11b) depend on the existence of unoccupied addresses."

**Problem**: Each enumerates downstream consumers rather than advancing the definition/axiom's meaning. Downstream claims already cite their premises; the forward inventory is redundant and rots as the note evolves.

**Required**: Remove the consumer lists. A definition is justified by what it says, not by who later uses it.

### Issue 5: PrefixSpanCoverage relocation note repeated across three locations

**ASN-0043**: the "awaits relocation to a span/tumbler-algebra ASN once that ASN exists" note appears in the axiom statement, again in the Properties table ("axiomatized pending relocation to span/tumbler-algebra ASN"), and a third time in Open Questions ("It should be re-homed as a derived lemma...").

**Problem**: Three paragraphs in different sections defer to the same future location — the "multiple paragraphs deferring to the same downstream location" accretion pattern. One statement of the relocation intent suffices.

**Required**: Keep the relocation note in one place (Open Questions is the natural home) and strip the duplicates.

### Issue 6: L-fin prose explains why the axiom is needed rather than what it says

**ASN-0043, L-fin**: "Without this axiom, a model could map every valid link address to a link value, leaving no room for fresh allocation; the extension proofs (L9, L11b) depend on the existence of unoccupied addresses."

**Problem**: This is "why the axiom is needed" justification (plus a use-site inventory of L9/L11b), not a statement of the axiom's content. The axiom — `|dom(Σ.L)| < ∞` — speaks for itself.

**Required**: Trim to the parallel-with-S8-fin observation; drop the necessity essay.

### Issue 7: A proof sketch sits under a clause declared an axiom

**ASN-0043, PrefixSpanCoverage**: declared "Axiom ... (pending relocation)" but immediately followed by "The identity follows from PrefixRelation and OrdinalShift ... together with the prefix characterization ... — all ASN-0034 primitives."

**Problem**: If the identity is derivable from ASN-0034 primitives (as the sketch asserts), it is a lemma, not an axiom; axiomatizing it while sketching its proof is internally inconsistent. Either prove it as a lemma here or state it as an axiom without the derivation essay.

**Required**: Choose one — derive it (LEMMA) with the full chain shown, or assert it (AXIOM) without the partial proof.

## OUT_OF_SCOPE

### Topic 1: Zero-count behavior of `inc(·, 0)` as a standalone foundation result
**Why out of scope**: If the spec genuinely needs a named UniformSiblingZeroCount result, that belongs in ASN-0034 (the allocator-discipline foundation), not invented or assumed in the link model. The fix to Issue 1 may motivate adding it upstream, but ASN-0043 should not be the site that introduces it.

VERDICT: REVISE
