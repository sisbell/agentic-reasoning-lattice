# Review of ASN-0122

This is a mathematically solid note. I checked the relation definition, the kernel algebra, the windowing identities, the canonical-report construction, the transport theorems, and the worked example, and the reasoning holds up — including the harder pieces (X4c's interval-intersection argument, X11's unique chain partition with fan-out, X7(iii)'s injectivity discharge via D-DP(a), and X6(b)'s composite-map argument). The worked example computes correctly in every part I re-ran (corr, the two maximal pairs, the swap tie-break, the window clip of γ₁ to a single pair, and the disjoint-window detector returning `{b}`). The wp analyses (X7 i/ii) are genuinely non-trivial, and the implementation deficiencies are correctly adjudicated against the abstract claims.

The findings below are the forward-reference and meta-prose accretion the `review-mode.anti-bloat` classifier targets, plus one real structural ordering defect.

## REVISE

### Issue 1: X4c is stated before the vocabulary and the result it depends on
**ASN-0122, "Windows: Restriction Is Exact"**: "and `γ = (d₁, u; d₂, w; n)` is a maximal pair of the wider comparison, then `⟦γ⟧ ∩ (P′ × Q′)` is the denotation of at most one pair. *Proof.* ... since γ is a maximal pair of the wider comparison it is confined to that comparison's regions (X11)..."

**Problem**: X4c uses the correspondence-pair notation `γ = (d₁, u; d₂, w; n)`, the pair denotation `⟦γ⟧`, "consistent," "confined," and "maximal pair" — every one of which is introduced *later*: the pair, its denotation, consistency, and confinement appear in "The Pair," and "maximal pair" is defined only in X11 ("The Report and Its Canonical Form"). The proof also forward-cites `(X11)` explicitly. A claim that consumes its entire vocabulary and a cited result two sections downstream is not linearly readable, and X4c is itself used only later (the worked example), so nothing earlier needs it where it sits.

**Required**: Relocate X4c to after X11 (or fold it into the report section). The dependency is one-directional — X11 does not rest on X4c — so the move is clean.

### Issue 2: X3's split carries a document-ordering justification and a downstream deferral
**ASN-0122, "What 'Correspond' Must Mean"**: "(The report-level consequence — pairwise transposition of the canonical list — is completed after the canonical list exists.)"

**Problem**: This parenthetical exists only to justify why X3 is split and to point the reader downstream to "X3 (continued)." It advances no part of the argument — it narrates document ordering, exactly the accretion pattern flagged for this note. The split itself is defensible (the report-level half genuinely needs X11), but the sentence announcing it is removable: a reader meeting "X3 (continued)" later loses nothing.

**Required**: Delete the parenthetical; keep the split.

### Issue 3: Throat-clearing in structural slots
**ASN-0122**, several sites where a sentence announces the document's thoroughness rather than carrying reasoning:
- "State, Instances, and Spec-Sets": "The boundary cases are part of the definition, not exercises left to the reader." (The enumeration that follows is the content; this sentence is skipped past to reach it.)
- "The Report and Its Canonical Form": "Completeness deserves its sentence of justification, because it is where this operation parts company with diff." (The falsehood-on-omission argument that follows is the substance and should be kept; this lead-in is filler, and "parts company with diff" restates the intro's diff framing.)

**Problem**: These are meta-prose in argument slots. They are not the substantive derivations — the "why address, not value" reasoning, the three demands, and the completeness justification itself are all genuine and should stay. Only the transitional throat-clearing should go.

**Required**: Strike the framing sentences; retain the surrounding substance.

## OUT_OF_SCOPE

No out-of-scope intrusion found. The note stays within SHOWRELATIONOF2VERSIONS — its use of the fork composite J4 (X6) is an illustrative foundation citation, not a definition of version creation. The Open Questions are correctly posed as future work (n-way alignment, derived-index consistency, subspace extension) and are not defects in this note.

META: (none — the ASN defines state instances, the correspondence relation, an observation operation, and stability invariants abstractly enough that any conforming implementation must satisfy R1–R3; it is squarely in specification territory.)

VERDICT: REVISE
