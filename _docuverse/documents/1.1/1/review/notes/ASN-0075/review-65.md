# Review of ASN-0075

## REVISE

### Issue 1: D-IDENT carries downstream-recovery essay that does not advance the claim
**ASN-0075, "Identity Preservation"**: The claim D-IDENT is "the returned reference is precisely the I-address `a` — not a copy with new identity." The first justification paragraph ("The output sets are defined as subsets of `dom(C)`... We return addresses, not values.") fully establishes it. The remaining block — "An operation that recovers content using these references dereferences existing entries in `C`..." followed by the *Link survival* (P3, L12, L3) and *Transclusion integrity* (S2, S3★, P0) bullets — reasons about a hypothetical **recovery/restoration operation** (itself an Open Question and a future ASN) and about transition-invariant preservation that holds independently of SHOWDELETIONS.
**Problem**: SHOWDELETIONS modifies nothing (D-OBS), so "link survival" and "transclusion integrity" are not consequences of this operation's output; they are forward-reference accretion justifying why identity-preservation will matter to a downstream operator. This is "why it matters" essay in a structural slot, of the kind the anti-bloat classifier targets.
**Required**: Cut the recovery paragraph and the two bullets. If a consequence is worth keeping, state it as a one-line corollary of "output ⊆ dom(C)" without importing the future restoration operation.

### Issue 2: Per-occurrence removal stated twice in "The Three States of Content"
**ASN-0075, "The Three States of Content"**: One paragraph closes with "A per-occurrence removal within `d` is therefore *invisible* to this classification while any occurrence of `a` survives in `d` — `a` becomes DELETED against `d` only when the *last* V-occurrence is removed." The very next paragraph repeats: "Per-occurrence removal — distinguishing which of several V-positions holding the same I-address went away — is a V-position (Vstream) concern that our I-address-set predicates do not address, and we scope it out of this operation."
**Problem**: Two adjacent paragraphs make the same point (per-occurrence removal is invisible / out of scope) in different words — the "two paragraphs say the same thing" pattern.
**Required**: Merge into a single sentence: the granularity consequence plus the one-clause scope-out.

### Issue 3: Defensive meta-sentence in D-DISJ proof
**ASN-0075, Lemma D-DISJ proof**: "The argument covers the special case of one or both `R`-projections being empty without separate handling."
**Problem**: This is a meta-statement asserting the proof's own completeness rather than reasoning content; the three-group partition already manifestly subsumes the empty-projection case (an empty projection simply leaves Group 1 or Group 2 empty). It tells the reader the proof handles a case instead of just handling it.
**Required**: Delete the sentence.

## OUT_OF_SCOPE

### Topic 1: Restoration consuming SHOWDELETIONS output
**Why out of scope**: The interaction between a deletion report and a restoration operation (raised in the Open Questions) is correctly deferred; it should not be argued inside D-IDENT (see Issue 1), but the *question* itself belongs to a future ASN, not this one.

The mathematical core is sound: D-WIT, D-EXH, the D-DISCR two-history discrimination argument (verified agreement on `(C,L,E,M)` with divergence only in `R`), the worked example's classification table and ({b},{c}) output, and the disjointness of the two report halves all check out. The findings above are bloat, not correctness.

VERDICT: REVISE
