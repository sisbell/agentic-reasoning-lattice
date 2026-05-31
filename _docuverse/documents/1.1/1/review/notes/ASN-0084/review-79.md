# Review of ASN-0084

## REVISE

### Issue 1: Pre-loaded ℕ-cancellation fact with no downstream use
**ASN-0084, "Identification of singleton tumblers with natural numbers"**: "Cancellation of ℕ-addition, where used below, is the standard fact `a + c = b + c ⟹ a = b` on ℕ, immediate from NAT-order (trichotomy) and NAT-addcompat (order-compatibility of addition) of ASN-0034."

**Problem**: This sentence sets up a lemma "where used below," but no proof in the ASN invokes additive cancellation. The width arithmetic uses the right-inverse identity `n + (m − n) = m`; uniqueness of the truncated subtraction is discharged by TS5 injectivity; R-COMM, Split, and Merge use Extended Associativity. Cancellation `a + c = b + c ⟹ a = b` appears nowhere afterward. This is exactly the accretion the anti-bloat classifier flags: a defensive justification the precise reader must skip past, hedged by "where used below" so its deadness is not obvious. 

**Required**: Either cite the concrete proof step that consumes ℕ-cancellation, or delete the sentence.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4
**Why out of scope**: The ASN explicitly confines itself to n ∈ {3, 4} (CS1) and lists the generalization as an Open Question. New territory, not an error here.

### Topic 2: Weakest precondition for the post-state invariant suite, and composition of rearrangements
**Why out of scope**: Both are listed as Open Questions. The invariant-preservation audit discharges every S0–S8 conjunct for a single REARRANGE_K; wp and composition are legitimately deferred.

---

The mathematics is sound throughout. I verified all four R-PRE consequences, the R-PIV/R-SWP tiling (no gaps, no overlap), R-PPERM/R-SPERM bijectivity (finite self-injection), R-COMM's same-region discharge feeding R-BLK's S8-cons/S8-uniq, and all six worked examples — including the three μ sub-cases (forward, fixed at w_α=w_β, backward at w_β<w_α), the empty-right-exterior boundary, and the non-S pass-through. Every displacement and merge computation checks out. R-CS3's vacuity argument is internally consistent with R-PRE(iii) (which bundles CS3), so it is not a contradiction.

VERDICT: REVISE
