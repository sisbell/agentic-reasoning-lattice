# Review of ASN-0102

I read the full note, verified the X16 tiling, the X7 displacement/no-overwrite argument, the S3★ weakest-precondition reduction, and the X8 within-reference / inter-reference merge analysis. The core construction is sound and the operation is on-track (it specifies state, an operation, and invariants abstractly). Two issues require revision.

## REVISE

### Issue 1: P4★ cited at a non-boundary pre-state
**ASN-0102, "A self-transclusion scenario" worked example**: "adds nothing not already present (`R'∖R = ∅` since `(x_3, d) ∈ Σ.R` by P4★ at the pre-state)."

**Problem**: P4★ (`Contains_C(Σ) ⊆ R`) is a *composite-boundary property* in ASN-0047's ExtendedReachableStateInvariants — it holds only at composite boundaries, not at every elementary-reachable state. COPY is one elementary transition (X15) and may sit as a non-first step inside a composite, so its pre-state `Σ` need not be a composite boundary. The conclusion `(x_3, d) ∈ Σ.R` therefore does not follow from P4★ for an arbitrary pre-state. The honest route is via the SL of whatever operation placed `x_3` at `[1,3]` plus P2 (ProvenancePermanence) — which still requires `Σ` to be a reachable boundary to be sure the placing operation's record survives unmasked.

**Required**: Either state that the worked example takes `Σ` to be a reachable composite boundary (so P4★ applies), or replace the P4★ citation with the SL+P2 justification under an explicit reachability assumption. As written the premise is unjustified.

### Issue 2: "single elementary transition changing M and R" repeated three times
**ASN-0102, Definition / X14 / X15**: Definition says "added to ValidComposite★'s atomic vocabulary … as a new elementary transition kind, changing two state components — the arrangement M and the provenance relation R." X14 opens "COPY is a *single elementary transition*…" and later "COPY changes two components — M and R…". X15 opens "COPY is a *single* elementary transition (Definition), not a composite of K.μ steps…".

**Problem**: The same framing fact (COPY is one elementary transition mutating exactly M and R) is asserted in three separate sections in different words. This is the forward-reference/restatement accretion the anti-bloat classifier targets — the reader re-encounters the same setup three times before each uses it.

**Required**: State the fact once (the Definition's amendment clause is the natural home). X14 and X15 should *use* it, not re-establish it. X15's Atomicity claim can cite the Definition for "single elementary transition" rather than re-narrating it.

## OUT_OF_SCOPE

(none — the note correctly defers INSERT/DELETE/REARRANGE mechanics, link semantics, and version creation to their own ASNs via the Open Questions, without smuggling claims about them.)

VERDICT: REVISE
