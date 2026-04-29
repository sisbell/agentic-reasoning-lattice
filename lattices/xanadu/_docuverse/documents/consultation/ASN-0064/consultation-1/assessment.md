# Revision Categorization — ASN-0064 review-1

**Date:** 2026-03-21 17:56

## Issue 1: DiscoveryQuery allows arbitrary Q ⊆ T, but decidability proof requires finite span-set representation
Category: INTERNAL
Reason: The fix is to constrain the definition to match the resolution pipeline already described in the ASN's own prose — queries are either T or finite span-sets produced by resolve(). Both the problem and the solution are visible within the ASN.

## Issue 2: F5 (CrossDocumentIdentity) is formally broken
Category: INTERNAL
Reason: The prose derivation is correct; the formal statement just needs to be rewritten to match it. The missing home(ℓ) ∈ E_doc assumption can be stated explicitly with a forward reference to the link-creation transition (ASN-0063). All three defects are internal consistency issues.

## Issue 3: F10 (ReverseSilentOmission) is tautological
Category: INTERNAL
Reason: The intended property is clearly described in the surrounding prose — the fix is to either reformalize as an existential (states exist where coverage(e) ⊄ ran(M(d))) or demote to an observation. No external evidence is needed to fix a statement that is A ⊆ A.

## Issue 4: F7 (VisibilityFiltering) depends on undefined predicates
Category: INTERNAL
Reason: The review's own suggested fix — relabeling F7 as a "Design Requirement" rather than INV and separating it from the grounded properties — is an honest-labeling change derivable from the ASN's own acknowledgment that Nelson left privacy unresolved. No consultation needed to say "this isn't grounded yet."

## Issue 5: No concrete worked example
Category: INTERNAL
Reason: All definitions needed to construct a worked example (resolution, overlap, satisfaction, block decomposition, span operations) are present in this ASN and its cited foundations. The example traces formal definitions with concrete tumblers — no design intent or implementation evidence beyond what's already cited is required.

## Issue 6: Pagination cursor domain is inconsistent
Category: INTERNAL
Reason: The zero tumbler violates the definition's own type constraint c ∈ dom(Σ.L). The fix — relaxing the cursor domain to T — is a self-contained consistency repair requiring no external input.
