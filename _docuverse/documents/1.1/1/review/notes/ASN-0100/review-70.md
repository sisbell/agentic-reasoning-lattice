# Review of ASN-0100

## REVISE

### Issue 1: Repeated deferral of the same result to one downstream section
**ASN-0100, §A Worked Example, §INSERT vs. COPY, §Weakest-Precondition Analysis**: four separate paragraphs hand off the same `N_{ℓ,i}` / tight-endset result to one location:
- "(This numeric instance specialises the general projection-shift law INS.proj, stated and proved in §Coverage and link discoverability.)"
- "is the tight/non-tight `N_{ℓ,i}` consequence stated in §Coverage and link discoverability."
- "This is the tight-endset case of the `N_{ℓ,i}` consequence established in §Coverage and link discoverability"
- "by the tight/non-tight `N_{ℓ,i}` consequence established in §Coverage and link discoverability (via LP19a; ASN-0098)"

**Problem**: Multiple paragraphs in different sections deferring to the same downstream location is exactly the forward-reference accretion pattern this note is flagged for. The reader must hold an unresolved pointer four times.
**Required**: State the tight/non-tight consequence once at its proof site; let the worked example and corollaries cite the claim label (INS.proj / INS.identity.tightsurv) without re-narrating the deferral.

### Issue 2: "First insertion fixes m_C = m" restated five times
**ASN-0100**: the same fact appears in §The Operation's Inputs ("S8-depth fixes `m_C = #p` for `d` at every state…"), §Sequential text-subspace structure ("this first insertion fixes `m_C = m` for `d`"), §Post-state V-position well-formedness ("so this first insertion fixes `m_C = m` for `d`"), INS.inv.depth ("empty case fixes `m_C = m` on first insertion"), and §Position Constraints ("triggers S8-depth's enforcement of `m_C = m`").
**Problem**: Two-plus paragraphs saying the same thing in different words; the depth-pinning fact is load-bearing in exactly one place (the empty-case verification).
**Required**: Assert it once where it is proved (the empty-case D-SEQ★ verification) and reference it elsewhere.

### Issue 3: Defensive elaboration of a uniformly-handled case
**ASN-0100, §A Worked Example**: "The variant where `V_{s_C}(d) = ∅` but `V_{s_L}(d) ≠ ∅` produces the same INSERT post-state shape on the content subspace: the operation's text-subspace effect … depends only on `V_{s_C}(d) = ∅`, not on whether `V_{s_L}(d)` is empty; the link subspace is preserved verbatim by the cross-subspace frame in either variant."
**Problem**: The cross-subspace frame (INS.frame.subspace) already handles `V_{s_L}(d)` uniformly; this paragraph re-argues a case the frame condition covers, i.e. reviser drift restating coverage the proof already supplies.
**Required**: Delete; the frame condition is the argument.

## OUT_OF_SCOPE

### Topic 1: Recovery of canonical order after partial failure
**Why out of scope**: The first Open Question (implementation recovery from partial composite failure) is genuinely implementation-level and correctly deferred — no action needed.

VERDICT: REVISE
