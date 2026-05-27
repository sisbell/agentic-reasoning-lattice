# Channel Assignment — ASN-0100 review-1

**Date:** 2026-05-27 11:40

## Issue 1: Composite vs. primitive ambiguity is unresolved
Reason: Resolving INSERT's substrate status (new primitive vs. composite governed by ValidComposite★) requires Nelson's intent on whether INSERT belongs in the elementary vocabulary, and Gregory's evidence on how udanax-green realizes the operation against the underlying allocator/arrangement primitives.
Nelson question: Was INSERT intended as a substrate-level elementary transition, or as a user-facing composite built from K.α, K.μ⁺, K.μ⁻, and K.ρ?
Gregory question: Does udanax-green implement INSERT as a single atomic operation or as a sequence of lower-level allocation/extension/retraction/provenance steps, and what guarantees its atomicity?

## Issue 2: Provenance recording (R) not addressed
Reason: ASN-0047 already mandates R as state and J1★ already forces `(a_k, d) ∈ R'`; the fix is to add R to the formal effect and include K.ρ in the decomposition using existing foundation work.

## Issue 3: No concrete worked example
Reason: Constructing a worked example uses only the operation's own contract; no external channels required.

## Issue 4: Foundation lemmas not cited in proofs
Reason: All cited lemmas (I3 from ASN-0082, LP3★/LP9/LP19a from ASN-0098, ChainPrefixExtension/ChainEnumerationInjectivity from ASN-0093, S8-depth from ASN-0036, TS2 from ASN-0034) are already established in prior ASNs; the fix is citation hygiene.

## Issue 5: shift(p, 0) = p convention not cited
Reason: OrdinalShiftBase is established in ASN-0058; the fix is a citation or clause split using existing material.

## Issue 6: Frame condition for E (entities) missing
Reason: The fix is to add `E' = E` to the frame, derivable from the state structure already defined in ASN-0047.

## Issue 7: "Edge cases require no special handling" claim contradicts the spec
Reason: The contradiction is internal to the ASN; resolving the prose requires no external evidence.

## Issue 8: Discoverability preservation is argued informally, not stated as a postcondition
Reason: The projection-shift correspondence is fully derivable from INS.M-left, INS.M-shift, and coverage definitions already in scope; the fix is to formalize what's already argued.

## Issue 9: Atomicity decomposition argument doesn't use the substrate decomposition
Reason: The fix follows directly from Issue 1's resolution — either drop the three-candidate argument (primitive path) or replace it with the substrate composite from ASN-0047 (composite path); both paths are derivable from substrate work already done once Issue 1 is settled.

## Issue 10: The "n successive emissions" of A_C(d) requires justification
Reason: Path (a) — citing ChainEnumerationInjectivity from ASN-0093 and re-deriving freshness against intermediate states — is fully internal and works regardless of Issue 1's resolution.

## Issue 11: Out-of-scope topics correctly flagged as Open Questions, but one belongs in this ASN
Reason: Moving the projection question from Open Questions to a derived postcondition is a structural fix using the ASN's own content.

## Issue 12: INS.identity claim lacks derived consequences
Reason: The required corollaries (cross-document independent allocations, tight-endset non-capture) derive from LP19a in ASN-0098 and the operation's own freshness clause; no external input needed.

## Issue 13: Empty-case post-state's depth fixation not formally derived
Reason: S8-depth from ASN-0036 supplies the invariant; the fix is to cite it and state the post-state depth condition explicitly.
