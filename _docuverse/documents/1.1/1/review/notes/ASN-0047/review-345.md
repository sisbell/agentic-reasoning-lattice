# Review of ASN-0047

I read the full ASN, checked the proof obligations against the invariant list, walked the K.δ/K.μ trichotomies, and verified the four worked examples' tumbler arithmetic and coupling discharges. The state/transition/invariant structure is sound and the per-state matrix is genuinely complete (modulo the issue below). The one finding is a duplicated proof mechanism that the anti-bloat mandate asks me to surface at source.

## REVISE

### Issue 1: SSGU and CrossNodeAccountBase restate the same zero-separator-at-`#N+1` divergence argument in full, joined by a forward reference that does not prevent the restatement

**ASN-0047, *NodeRootedForest (SSGU)* and *CrossDocEntityDisjoint (CrossNodeAccountBase)***:

SSGU's *Nested nodes* case argues, for `N ≼ N'` with `#N < #N'`:
> "any non-node `inc`-output `a` assigned to `N`'s subtree carries the field-separating zero introduced by its first descent off the node `N` at position `#N + 1`, so `a_{#N + 1} = 0`; whereas `a'` with `N' ≼ a'` agrees with `N'` at position `#N + 1`, where `(N')_{#N + 1} ≠ 0` because `N'` is a node ... The two diverge at position `#N + 1`, so `a ≠ a'`."

CrossNodeAccountBase then argues, for the same `N₁ ≼ N₂` configuration:
> "`b_account(N₁)` carries the field-separating zero at position `#N₁ + 1`, whereas `b_account(N₂)` carries `(N₂)_{#N₁+1}` there, which is nonzero because `N₂` is a node ... The two bases thus diverge at position `#N₁ + 1`."

These are the same mechanism. SSGU even labels its own statement "(the CrossNodeAccountBase mechanism, below, generalised from account bases to arbitrary `inc`-outputs)" — so SSGU is explicitly the *general* form and CrossNodeAccountBase a *strict special case* (`a := b_account(N₁)`, `a' := b_account(N₂)`), yet both spell the position-`#N+1` zero-divergence out in full.

**Problem**: This is the anti-bloat "two paragraphs in different sections say the same thing" pattern, compounded by a forward reference from the earlier-appearing general statement (SSGU) to the later special case (CrossNodeAccountBase) that nonetheless restates the argument. The duplication is load-bearing for nothing: CrossDocEntityDisjoint already routes its *same-parent cross-chain* sub-case through SSGU directly, so the account-non-nesting obligation that CrossNodeAccountBase discharges is a special instance of a result the ASN already has in general form.

**Required**: State the zero-separator-at-`#N+1` divergence once (the SSGU general form), and have CrossNodeAccountBase *cite* it at the instantiation `a = b_account(N₁)`, `a' = b_account(N₂)` rather than re-deriving it. Remove SSGU's forward pointer to CrossNodeAccountBase, since the mechanism should be defined where it is first proved, not deferred to its own special case.

## OUT_OF_SCOPE

None. The ASN defines state components, elementary/composite transitions, and their invariants at the abstract level — squarely the kind of content the specification should carry. J4 (fork) and the worked examples reference CREATENEWVERSION/`docreatenewversion` only as motivation and verification evidence; they specify the abstract K.δ+K.μ⁺+K.ρ composite and its φ-bijection constraint, not the named operation's interface, so they remain in-scope.

VERDICT: REVISE
