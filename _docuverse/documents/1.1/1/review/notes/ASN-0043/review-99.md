# Review of ASN-0043

## REVISE

### Issue 1: L11b invokes FSP without discharging FSP's `s_C`-residence hypothesis

**ASN-0043, L11b — NonInjectivity, *Conformance of `Σ'`***: "This is another fresh-sibling extension, so we appeal to FSP (FreshSiblingConformance ...) for the shared invariant set, discharging its hypotheses for `a'` and payload..."

**Problem**: FSP's blanket hypothesis is "*Let `Σ` satisfy the state-local L- and S-invariants **with `s_C`-resident content**.*" But L11b's precondition is only "*`Σ` satisfying the state-local L- and S-invariants*", and `s_C`-residence is **not** among the listed state-local invariants (the set is L0, L1, L1a–c, L3, L5, L6, L11a, L14, L14a, L-fin, S0–S3, S7a, S7b, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ — none asserts `(A b ∈ dom(Σ.C) :: subspace_I(b) = s_C)`). FSP genuinely *uses* this hypothesis:

- FSP's *L0* bullet: "`dom(Σ'.C) = dom(Σ.C)` is `s_C`-resident, so `a ∉ dom(Σ'.C)`" — this is how FSP establishes that the fresh link address `a'` (in `s_L`) does not collide with a content address. Without `s_C`-residence, content could occupy `s_L`, and `a' ∉ dom(Σ.C)` is not established (L0 alone gives only the `s_C`-scoped disjointness).
- FSP's *L14a* bullet: "since `dom(Σ.C) ∩ dom(Σ'.L) = ∅` by L0 (above)" — this cites an **unscoped** disjointness, but the L0 bullet only proved `dom(Σ'.L) ∩ dom(Σ'.C)|_{s_C} = ∅`. The step from scoped to unscoped is licensed solely by `s_C`-residence.

By contrast, L9 *does* carry `s_C`-residence in its precondition and so discharges FSP correctly. L11b is the one invocation that leaves FSP's hypothesis unmet.

**Required**: Add `(A b ∈ dom(Σ.C) :: subspace_I(b) = s_C)` to L11b's precondition (matching L9), and have the *Conformance of `Σ'`* paragraph cite it when appealing to FSP. Separately, tighten FSP's L14a bullet to make the scoped→unscoped step explicit ("`Σ'.M(d)(v) ∈ dom(Σ.C)|_{s_C}` by S3 + `s_C`-residence, and `dom(Σ'.L) ∩ dom(Σ.C)|_{s_C} = ∅` by L0") rather than citing the unscoped `dom(Σ.C) ∩ dom(Σ'.L) = ∅`.

### Issue 2: Synthesizing forward-pointer paragraph in *Home and Ownership* restates downstream claims without advancing them

**ASN-0043, *Home and Ownership*, second paragraph**: "...Address-level distinctness across distinct allocation events — including links allocated under distinct documents — is carried by L11a (LinkUniqueness). How this owning document is fixed — by the address alone, independent of what the link points to — **is the content of L2.**"

**Problem**: The paragraph's only new object-level content is `home(a) = s = d`. The remainder re-states L1a (membership), the S7 analog, and L11a, then closes by forward-pointing to L2 — which is the very next claim and states exactly "the home document ... is determined entirely by the link's address and is independent of the link's endsets." This is the forward-reference accretion the anti-bloat classifier targets: a meta-paragraph that defers to the immediately following claim and re-describes invariants stated elsewhere. A reader must skip past it to reach L2's actual statement.

**Required**: Keep the load-bearing clause (`home(a) = s = d`, citing L1c) and delete the synthesizing restatement and the "is the content of L2" pointer; let L2 stand on its own.

## OUT_OF_SCOPE

### Topic 1: Globalizing content-side disjointness beyond the `s_C` slice
The note scopes all content/link disjointness to `dom(Σ.C)|_{s_C}` and lists the global extension as the first Open Question. Fixing Issue 1 (adding the `s_C`-residence hypothesis to L11b) keeps the note internally consistent without resolving whether a future content-side invariant should fix a global content subspace — that belongs in the content ASN, not here.

VERDICT: REVISE
