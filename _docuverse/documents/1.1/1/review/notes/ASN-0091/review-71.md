# Review of ASN-0091

## REVISE

### Issue 1: Empty-case discharge is a use-site inventory of downstream claim labels
**ASN-0091, "REARRANGE as Vstream-Only Operation" (degenerate cases)**: "the arrangement-indexed claims (RE-ran, RE-proj, RE-μ) hold vacuously (ranges, projections, and multiplicities are all over the empty set), and the component-global claims (RE-C, RE-L, RE-R, RE-origin, RE-cov) hold by RA-frame ... REARRANGE_K rules this out for the concrete operation via R-PRE(iv) ... so `V_S(d) ≠ ∅` is a precondition of every REARRANGE_K invocation."
**Problem**: This enumerates eight downstream RE-* labels to assert each holds vacuously, in a case the concrete operation then *excludes* via R-PRE(iv)/CS2. It is a use-site inventory attached to a case the precondition already rules out — exactly the forward-reference accretion this classifier flags. The roll-call of labels does not advance the argument; the reader who wants any specific RE-* claim reads it where it is derived.
**Required**: Collapse to a single statement — the abstract class admits `dom(Σ.M(d)) = ∅` with π the empty bijection (every claim vacuous), and REARRANGE_K excludes it via R-PRE(iv)/CS2 — dropping the per-label enumeration.

### Issue 2: Identity-case carries a blanket downstream-coverage sentence
**ASN-0091, "REARRANGE as Vstream-Only Operation" (identity case)**: "Every claim derived below holds uniformly across the identity and non-identity cases — under π = id all RE-* claims reduce to identities of Σ with itself."
**Problem**: The same paragraph already derives `Σ' = Σ`. Once that is established, "all RE-* claims reduce to identities of Σ with itself" is an immediate restatement, not new reasoning — a blanket forward assertion of coverage over every downstream claim. It is the "two paragraphs say the same thing" pattern compressed into one trailing sentence.
**Required**: Delete the sentence; `Σ' = Σ` already settles the identity case without a downstream roll-up.

### Issue 3: Standalone S2 derivation duplicates RA-adm
**ASN-0091, "REARRANGE as Vstream-Only Operation" (*S2 derivation at the abstract level*)**: "The post-state arrangement `Σ'.M(d)` is a partial function — foundation invariant S2 — derived directly from RA-π."
**Problem**: RA-adm is defined two paragraphs earlier as "every per-state foundation invariant satisfied by Σ is satisfied by Σ'," and S2 (ArrangementFunctionality, ASN-0036) is a per-state foundation invariant. S2 at Σ' is therefore already discharged by RA-adm. Singling out S2 for a separate from-RA-π derivation duplicates that coverage and reads as relocated content — why S2 and not the other per-state invariants RA-adm carries?
**Required**: Either remove the paragraph (RA-adm covers it), or, if the intent is to show RA-adm imposes no S2 burden, state that purpose explicitly rather than re-proving S2 as if it were an independent obligation.

## OUT_OF_SCOPE

### Topic 1: Same-source span reconstitution after a splitting cut
**Why out of scope**: The first Open Question (whether two fragments jointly reconstitute a same-source transcluded span) is correctly deferred — RE-trans establishes per-fragment origin retention, and joint reconstitution is genuinely new territory, not a gap in this ASN's stated claims.

### Topic 2: Link-subspace rearrangement semantics
**Why out of scope**: The ASN restricts REARRANGE_K's cut subspace to content (RE-sub/RE-ext), and the second Open Question flags link-subspace reordering as future work. This is a deliberate scope boundary, not an error.

VERDICT: REVISE
