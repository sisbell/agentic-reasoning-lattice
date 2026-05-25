# Channel Assignment — ASN-0097 review-2

**Date:** 2026-05-24 10:36

## Issue 1: Π11's "single closed form" is just `iproj`'s definition
Reason: The fix is internal — the author can either drop the line they themselves acknowledge as definitional, or compose a genuine transition-level closed form using `iproj`'s definition and the K.μ frame contracts already stated in Π8/Π9/Π10. No external evidence or intent is needed.

## Issue 2: Mode II asserts `ran(M(d_v)) ⊆ ran(M(d))` without derivation
Reason: The fix is internal — J4's contract lives in ASN-0047 (project corpus), so the author can either restate it and derive the inclusion, promote it to an explicit Π-claim, or fall back to the reviewer's option (c) and label it as a versioning assumption. All paths stay within the project's own materials.

## Issue 3: `iproj = Σ.M(d)(proj)` asserted but not derived
Reason: The fix is internal — a one-line bidirectional set-equality proof from the two definitions (`proj` and `iproj`) already given in the ASN's "The Projection" section.

## Issue 4: Π6 has no proof, only a restatement
Reason: The fix is internal — derivation follows from Π5 applied twice (once for `d`, once for `d'`) plus the fact that `M(d)` and `M(d')` are disjoint state components in `Σ.M : D × T ⇀ T`, which the ASN already cites from ASN-0036.

## Issue 5: `K.μ⁺_L` listed in Π12 but never defined or analyzed
Reason: The fix is internal — the minimal correct fix is to remove `K.μ⁺_L` from the enumeration with a parenthetical note that link-subspace extension is out of scope for this ASN's endset-projection analysis, or to state that Π8's argument applies generically. Both are editorial decisions within the ASN's purview.

## Issue 6: Π12's enumeration confuses "frame on other documents" with "no document target"
Reason: The fix is internal — restructure Π12 using a uniform "operations whose write set does not include `M(d)`" framing, or restrict Π12 to document-targeted operations and let Π13/Π14 absorb `K.α` and `K.λ`. Pure editorial restructuring.

## Issue 7: Π13's claim does not match Π13's proof scope
Reason: The fix is internal — a quantifier correction. Replace the unbound `ℓ` with either `(A d, e :: ...)` or `(A d, ℓ, i :: ...)` and apply the same fix to Π14.

## Issue 8: Worked example does not test cross-document or reverse-orphaning claims
Reason: The fix is internal — extending the example with a second document `d'` and a reverse-orphaning step requires only the definitions and Π-claims already present in the ASN; no external evidence or intent is consulted to construct the witness.

## Issue 9: Π11's transition claim and "transition content" sentence contradict each other
Reason: The fix is internal — editorial collapse of redundant framing or substitution of a genuinely new composed-inequality synthesis. The author's own statements provide the material.
