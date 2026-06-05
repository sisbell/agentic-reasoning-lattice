# Review of ASN-0102

The arrangement mechanics (the three-class displacement, the tiling in X16, S2/S3★ discharge, the four worked examples) are rigorous and the invariant sweep in X14 is appropriately exhaustive. My findings are confined to forward-reference accretion and duplicated prose flagged by the anti-bloat classifier.

## REVISE

### Issue 1: Source-designation paragraph previews and duplicates X8

**ASN-0102, "The source designation and its resolution"**: "Across references, however, `k` may strictly *exceed* the number of maximal I-runs the combined source occupies: when two consecutive references draw I-adjacent content of shared origin, the concatenation carries the inter-reference boundary as two runs... The canonical (maximally-merged) count of the copied region, which may differ from this constructed `k`, is characterised in X8."

**Problem**: This paragraph establishes the constructed-vs-canonical distinction and the within-reference / across-reference fragmentation analysis without proof, then explicitly defers to X8 — which re-establishes the identical content ("Two cases separate: Within a single reference... Across an inter-reference boundary...") with the proof. Two paragraphs say the same thing; the earlier one is an unproven preview deferring downstream. The definition of `k` needs only `k = (+ i : k_i)` for the effect to use; the fragmentation editorializing and the canonical-count preview belong solely in X8.

**Required**: Reduce the source-designation paragraph to the bare definition of `k` and `W` needed by `B_copy`. Move the canonical-vs-constructed discussion entirely into X8, deleting the forward pointer.

### Issue 2: Use-site inventory in P2

**ASN-0102, P2**: "We use whichever form is salient — `dom(Σ.M)` for arrangement reasoning, `E_doc` for the provenance typing `Σ.R ⊆ T_elem × E_doc` and the `E_doc`-quantified couplings J1★/J1'★/P4★ (X14)."

**Problem**: This enumerates downstream consumers of the `dom(Σ.M) = E_doc` identity rather than advancing the precondition. The standing identity and its one load-bearing use ("the pair `(a_j+i, d)` is well-typed precisely because `d ∈ E_doc`") suffice; the inventory of which form is used where is the anti-bloat use-site-inventory pattern.

**Required**: Delete the "we use whichever form is salient" sentence with its consumer list; keep the identity and the well-typedness consequence.

### Issue 3: Definition slots carry pre-emptive discharge claims and repeated deferrals to X14

**ASN-0102, "Definition of COPY"**: e.g. "**Link store — untouched.** `Σ'.L = Σ.L`. COPY creates no link and alters none; this discharges the `s_L`-routing conjunct of S3★ below and preserves L12 ... vacuously." and "**Provenance.** ... it is the effect that discharges the coupling invariant J1★ ... — see X14."

**Problem**: The effect-definition subsections repeatedly state *what invariant they will discharge downstream* ("discharges the `s_L`-routing conjunct ... below," "preserves L12 ... vacuously," "discharges ... J1★ ... — see X14"). These are proof obligations that X3's wp computation and X14 already establish in full; placing the claims in the definition mixes definition with proof and creates multiple deferrals to the same downstream location (X14). A definition should pin the effect, not anticipate its own discharges.

**Required**: Strip the "this discharges / preserves / see X14" clauses from the effect subsections, leaving the bare state-component effects. Let X3 and X14 carry the discharge claims where the work is actually shown.

## OUT_OF_SCOPE

### Topic 1: Re-displacement of copied content by later operations

**Why out of scope**: This is the first Open Question and concerns INSERT/DELETE/REARRANGE interaction with already-copied content — operation mechanics excluded by the stated scope.

VERDICT: REVISE
