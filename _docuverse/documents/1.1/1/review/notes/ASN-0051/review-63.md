# Review of ASN-0051

## REVISE

### Issue 1: (m ≥ 3, p ≥ 3) attainment lacks a concrete witness
**ASN-0051, SV11 "Witnessed attainment scope" / Conclusion**: "The `(m ≥ 3, p ≥ 3)` regime is marked *structurally admissible but not witnessed in this ASN*: it is constructible by the same nesting pattern with larger block sizes..."
**Problem**: The witness coverage explicitly stops at (m=3, p=2) and (m=2, p=3). For (m=3, p=3) and higher, the ASN provides only a "construction-pattern generalisation" hand-wave. The biconditional's ⇐ direction needs constructive witnesses to demonstrate that the conditions are simultaneously satisfiable across the claimed regime. Verifying that the M7/M12 realisability constraints "place no obstruction" at higher m and p requires actually exhibiting one.
**Required**: Exhibit a concrete (m=3, p=3) witness (B, e) with explicit tumbler values, block I-extents, and span coverages. Verify that all 9 (j,k) decomposition terms are non-empty and that within each of the three blocks the three terms are pairwise non-adjacent. If the construction fails for some structural reason at (m=3, p=3) that wasn't anticipated, the biconditional may need narrowing.

### Issue 2: Worked Example's "discover_from({a₃}) = {b}" assumes no other links
**ASN-0051, Worked Example "Initial state — projection, resolution, discovery"**: "discover_from({a₃}) = {b}, since coverage(F) ∩ {a₃} = {a₃} ≠ ∅"
**Problem**: discover_from({a₃}) returns all links `a ∈ dom(Σ.L)` with coverage(Σ.L(a).from) ∩ {a₃} ≠ ∅. The equality with `{b}` assumes b is the only such link in Σ. The worked example doesn't state this; it only mentions creating b. Strictly, the conclusion is `b ∈ discover_from({a₃})`, equality requires `dom(Σ.L) = {b}`.
**Required**: Either qualify the claim as `b ∈ discover_from({a₃})`, or explicitly state "Σ has only the single link b at this point" before asserting equality.

### Issue 3: The "Reordering that changes locate" K.μ~ swap admissibility is implicit
**ASN-0051, Worked Example "Reordering that changes locate" subsection**: "Apply a K.μ~ step whose reordering bijection ψ swaps v₁ and v₂ (and fixes v₃, v₄)"
**Problem**: ASN-0047's K.μ~ decomposes into K.μ⁻ + K.μ⁺ where K.μ⁻ must satisfy D-SEQ (upward-tail removal). The minimal {v₁, v₂}-only removal is *not* an upward tail of V_{s_C}(d) = {v₁, v₂, v₃, v₄}. The decomposition is realised by the larger {v₁, v₂, v₃, v₄}-remove-and-readd (an upward tail with n'=0). The prose doesn't note this, so a careful reader checking admissibility hits an apparent contradiction. Compare to Step 1 of the prior worked example, which *does* explicitly verify D-SEQ admissibility for its ψ.
**Required**: Add a one-sentence admissibility check matching the standard set by Step 1's explicit verification.

### Issue 4: SV6 precondition lists "T12-well-formed" redundantly with "in an existing endset"
**ASN-0051, SV6 statement**: "For a span (s, ℓ) in an existing endset where..." then under *Precondition*: "(s, ℓ) is T12-well-formed (T12, SpanWellDefinedness, ASN-0034: `Pos(ℓ) ∧ actionPoint(ℓ) ≤ #s`)"
**Problem**: Spans in existing endsets are already T12-well-formed by L3 (NEndsetStructure, ASN-0043) referencing the Span definition. Stating it as a separate precondition makes the list look like a substantive constraint rather than an inherited property. Also, the proof only uses the structural conditions (T12, T4-validity, zeros, action point) — "in an existing endset" is descriptive, not load-bearing. The "Note on 'newly allocated'" later in the proof correctly captures this. The same observation should govern the precondition list.
**Required**: Either remove the "in an existing endset" framing (since the proof is structural), or remove the T12 precondition (since it's implied by endset membership). The current dual form is inconsistent with the proof.

### Issue 5: SV2-SV5 proofs cite L12 for coverage invariance but the argument is more general
**ASN-0051, SV2 proof / SV3 proof / SV5 proof**: "Since coverage(e) is invariant (L12, ASN-0043)..."
**Problem**: For a fixed endset *value* e (a set of spans), coverage(e) is purely a function of e's spans — state-independent by construction, no foundation citation needed. L12 (LinkImmutability) is required only when e is the slot value of an existing link Σ.L(a).s and one wants to argue that "the value e doesn't change across the transition." The proofs work for any fixed endset value; citing L12 narrows the apparent scope unnecessarily and obscures what's actually load-bearing. The relevant invariance is: "e is a fixed set; coverage is a function of e; therefore coverage(e) doesn't depend on state."
**Required**: Tighten the proofs to read "coverage(e) is determined by e (a fixed set of spans), and therefore independent of state" — or add a clarifying parenthetical noting that L12 is invoked only for the typical case of e being the slot value of an existing link.

### Issue 6: The four-case structural lemma's case (IIIb) j* = n_{k₁} branch handling
**ASN-0051, SV11 disjoint-pair proof, four-case structural lemma**: "*(IIIb)* Some β_{k₁}-element e_{k₁,j*} is a proper prefix of y... When j* = n_{k₁}, the comparison with e_{k₁,j*+1} is vacuous and y > e_{n_{k₁}} alone holds — *T-linear separation past the last element.*"
**Problem**: The lemma classifies (IIIb) with j* = n_{k₁} as "T-linear separation past the last element." But the disjoint-pair proof then says "The T-interleaving sub-case rules out T-linear separation, so... the j* = n_{k₁} branch of (IIIb), and (IV) are all excluded." This excludes j* = n_{k₁} from the T-interleaving sub-case. But a mixed configuration where some β_{k₂}-elements fit (IIIb) with j* < n_{k₁} (interleaved) while others fit (IIIb) with j* = n_{k₁} (separated past last) needs to be ruled out by the uniformity argument. The uniformity argument shows j* is fixed by the shared q_{k₂} prefix — but this argument forces all elements to share the same j*, which by case-split must be either < n_{k₁} (all interleaved) or = n_{k₁} (all separated). The "all separated" case is then T-linear separation (case a), not T-interleaving. The proof flow is correct, but the case-elimination is not made explicit. A reader following the proof needs to construct this argument independently.
**Required**: Add a one-sentence note in the uniformity paragraph stating that the shared j* either forces all of β_{k₂} into T-linear separation past β_{k₁} (subsumed under case a) or all into a single interior window (case b), with no mixed configurations possible — making the exhaustiveness of the (a)/(b) sub-case split explicit.

## OUT_OF_SCOPE

### Topic 1: Concrete (m ≥ 4, p ≥ 4) attainment witnesses
**Why out of scope**: The biconditional in SV11 is established by counting argument; witnesses serve to demonstrate satisfiability in specific regimes. Exhaustive enumeration of witnesses for all (m, p) pairs is not necessary for the biconditional's correctness — issue 1 above flags the (m ≥ 3, p ≥ 3) gap as a representative missing case; resolving (m=3, p=3) suffices to demonstrate the construction pattern.

### Topic 2: Link-subspace contribution to π(e, d) (beyond text-subspace projection)
**Why out of scope**: SV11 explicitly scopes to π_text(e, d) and defers the link-subspace contribution to the Link Subspace ASN. The parenthetical in SV11 acknowledges this and identifies the deferral target.

### Topic 3: Survivability under fork (J4) as a multi-step composite analysis
**Why out of scope**: The TransclusionCouplingAbsence corollary explicitly notes that fork's discovery inheritance follows the same reasoning as transclusion. A standalone fork-analysis section would be useful but is properly the subject of a version-semantics ASN.

### Topic 4: Latency or timing guarantees for discovery
**Why out of scope**: SV claims are state-relative (Σ → Σ'), making no claims about when transitions occur. Discovery latency is an implementation policy question, not a specification invariant. The Open Questions section properly flags this.

VERDICT: REVISE
