# Review of ASN-0043

I read the full note, checked every L-claim's proof against its preconditions, traced the allocation chains in L1c/L9/L11a against T10a's discipline (including the at-most-once child-spawn constraint), and re-verified the worked example's six extension steps. The mathematics is sound: the subspace-separation argument (L1d), the FSP/FSE factoring, the PrefixSpanCoverage applications in L8/L10/L13, and the coverage-equality computation in Step 6 all hold. The one issue I can defend under this note's anti-bloat mandate is a genuine duplication.

## REVISE

### Issue 1: L0b re-derives projection well-definedness that L1c's postcondition already establishes over all of dom(Σ.L)

**ASN-0043, L0b — LinkAddressValidity**: "With every link address T4-valid and element-level (L1, `zeros(a) = 3`), T4b's `E`, `N`, `U`, `D` projections (UniqueParse, ASN-0034) are well-defined on all of `dom(Σ.L)`, so `subspace_I(a) = E(a)₁` and `home(a)` exist for every `a ∈ dom(Σ.L)`."

**Problem**: L1c's "Postcondition: T4-validity of a" paragraph already concludes, for the chain terminus, that "T4b's projections `N(a)`, `U(a)`, `D(a)`, `E(a)` are well-defined; in particular, the document-level prefix `home(a)` ... is well-defined." Because L1c's contract is universally quantified over `dom(Σ.L)` (`(A a ∈ dom(Σ.L) :: (E s ... ))`), that postcondition already covers every link address. L0b's body then states the identical T4-valid ⇒ projections-well-defined ⇒ `home`/`subspace_I`-exist chain a second time. This is the "two paragraphs say the same thing" pattern: a precise reader who has absorbed L1c's postcondition must skip past L0b's re-derivation to reach the only new content, which is the bare named statement `(A a ∈ dom(Σ.L) :: T4-valid(a))`. The Notational convention is the third site stating the T4-valid ⇒ `subspace_I`-defined link; together the conclusion appears three times.

**Required**: L0b is a legitimately-cited handle (L1d(a), L9), so keep the *statement*. Trim its body to the bare claim plus citation — e.g., "Every link address is T4-valid: the T4-validity postcondition of L1c's chain, quantified over `dom(Σ.L)`." Drop the re-statement of projection well-definedness, which L1c's postcondition already delivers.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace residence (extending disjointness beyond the s_C slice)
**Why out of scope**: The note deliberately scopes L1d(b)/L14/L14a to `s_C`-resident content and records this as the first Open Question. Promoting `s_C`-residence to a content-side invariant is new content-model territory (an ASN-0036 amendment), not a defect here.

### Topic 2: Compound/faceted link well-formedness and transclusion-consistency invariants
**Why out of scope**: The constraints governing link-to-link compound structures (L13 chaining) and link/content consistency under shared I-addresses are listed as Open Questions; they are future relational-structure ASNs, not gaps in the link primitive defined here.

VERDICT: REVISE
