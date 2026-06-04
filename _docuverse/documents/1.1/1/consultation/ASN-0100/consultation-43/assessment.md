# Channel Assignment — ASN-0100 review-43

**Date:** 2026-06-04 14:01

## Issue 1: Composite atomicity is framed as an environmental precondition, but ValidComposite★ already supplies it — the residue is implementation mechanics
Reason: The fix turns on whether ValidComposite★'s definition makes a composite's transition sequence contiguous/atomic at the abstract level (so atomicity is definitional, not an extra environmental assumption). That fact lives in the foundation synthesis where ValidComposite★ is defined, which Gregory holds; the ASN's own text takes the opposite (environmental) framing, so it cannot self-resolve.
Gregory question: Does ValidComposite★ (ASN-0047) define a composite as a contiguous transition sequence Σ₀ → … → Σₙ in which no foreign elementary transition may interleave, making composite-level atomicity definitional rather than a stronger property the substrate must separately provide?

## Issue 2: I3-* lemmas cited as "discharged also by" are imprecise and redundant with the ASN's own re-derivations
Reason: The ASN already re-derives S2, S3★, S8a, S8-depth, S8-fin and already flags that I3-C/I3-S7 fail; the choice to drop or annotate the citations is editorial and fully supported by reasoning present in the text.

## Issue 3: Use-site inventory embedded in the S8a derivation
Reason: Deleting a sentence that merely enumerates downstream consumers is a pure editorial cut requiring no external input.

## Issue 4: Multiple sections defer to the same "I3 scope note"
Reason: Consolidating the single load-bearing fact (only I3's shift clause transfers; I3-C/I3-S7 fail) and removing repeated back-pointers is editorial and derivable from content already in the ASN.

## Issue 5: The m_C depth-fixing explanation is repeated four times
Reason: Stating the depth-fixing behaviour once and cross-referencing it is a deduplication edit using material already present.

## Issue 6: The first K.α "forced ordering" bullet is essay-length rationale in a structural slot
Reason: Reducing the bullet to its one-sentence dependency statement and dropping the counterfactual is an editorial trim of existing reasoning.
