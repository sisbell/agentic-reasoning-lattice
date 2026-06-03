# Review of ASN-0075

## REVISE

### Issue 1: Classification granularity over multiply-occurring I-addresses is left implicit

**ASN-0075, "The Three States of Content"**: "`CURRENT(a, d) ≡ a ∈ ran(M(d))`" and "`DELETED(a, d) ≡ (a, d) ∈ R ∧ a ∉ ran(M(d))`".

**Problem**: Both predicates are defined on *set* membership in `ran(M(d))`. The foundation this note builds on establishes that a single I-address may occupy multiple V-positions within one document (ASN-0036 S5 / M13, ASN-0058 M14: `(E d, a :: |{v : M(d)(v) = a}| > 1)`). Consequently, if `d_A` references `a` at two V-positions and removes one, `a ∈ ran(M(d_A))` still holds, so `a` is classified `CURRENT`, not `DELETED` — a genuine per-occurrence deletion event in a document is invisible to an operation literally named SHOWDELETIONS. The note never states that classification is at I-address-set granularity, and the worked example uses only single-occurrence arrangements, so the exhaustiveness claim (D-EXH) and the "show deletions" intent read as complete when they silently collapse multiplicity. This is an unstated semantic choice with observable consequences.

**Required**: State explicitly that CURRENT/DELETED/NEVER_INCLUDED classify at I-address-set granularity, and acknowledge the consequence: removal of one among several V-occurrences of `a` within `d` does not make `a` DELETED while `a` persists elsewhere in `d`. The note should either justify this as the intended cross-document set-comparison semantics or scope per-occurrence detection out explicitly.

## OUT_OF_SCOPE

### Topic 1: Multiplicity-aware (per-occurrence) deletion detection
**Why out of scope**: Surfacing the removal of individual duplicate V-occurrences while the I-address persists elsewhere would require a multiplicity-counting or position-level notion of deletion. That is a refinement of the operation's granularity and belongs in a future ASN; the present I-address-set treatment is internally coherent once Issue 1 is stated.

### Topic 2: Three-document and family generalizations
**Why out of scope**: The note's own Open Questions raise the witness-in-a-third-document case and >2-document families. These are genuine future territory, correctly deferred rather than attempted here.

VERDICT: REVISE
