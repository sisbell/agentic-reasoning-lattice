# Review of ASN-0087

## REVISE

### Issue 1: wp omits MAKELINK's own enabledness, diverging from the foundation's wp convention

**ASN-0087, "Weakest Precondition for Discoverability" / M-WP, Case 1**: "wp(MAKELINK, discoverable_from(ℓ, d_target, ·)) ≡ d_target ∈ dom(Σ.M) ∧ (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)"

**Problem**: The membership conjunct `d_target ∈ dom(Σ.M)` is about keeping `discoverable_from` *defined* at the post-state — it is not MAKELINK's applicability. For `d_target ≠ d`, the *home* document `d` of the new link must also satisfy `d ∈ dom(Σ.M)` (and the endset inputs must satisfy `N ≥ 3`, `eᵢ ∈ Endset`, `e₃ ≠ ∅`) for any post-state `Σ'` to exist at all. Case 1's wp captures none of this home-document enabledness. The foundation's own wp convention (LP12a, ASN-0098) writes wp as `enabled(K.μ⁻[d,R]) ∧ …`, explicitly conjoining the operation's applicability predicate. The Case 2 prose acknowledges the home-doc precondition ("automatically discharged by MAKELINK's own input precondition") only because there `d_target = d`; Case 1 silently drops it. As written, M-WP is not the weakest precondition for total correctness and is inconsistent with LP12a.

**Required**: Either conjoin `enabled(MAKELINK)` (home `d ∈ dom(Σ.M)` together with the endset-validity inputs) into both wp expressions, matching LP12a's convention, or state explicitly that M-WP computes the weakest *liberal* precondition and justify the omission.

### Issue 2: M-DepthConv's universal claim is in unresolved tension with the "regardless of its value" hedge

**ASN-0087, "Effect" and M-DepthConv**: M-DepthConv asserts "MAKELINK fixes the first link's V-position depth at the canonical minimal m = 2 … for the first link of every document," while the Effect section states "We do not assert m_L(d) = 2 universally here: … the operation computes v_ℓ correctly at that depth regardless of its value."

**Problem**: These two statements cannot both be load-bearing. If MAKELINK is the only operation that seeds a link-subspace V-position (the ASN itself argues via the J4/ForkComposite parenthetical that fork "copies only the content subspace V_{s_C} and never seeds link V-positions"), then every first link is placed at `m = 2`, `m_L(d) = 2` is universal, and the "regardless of its value" hedge is unreachable dead reasoning. If, on the other hand, some reachable path can place a document's first link at depth ≠ 2, then M-DepthConv's "first link of every document" is false. The ASN never identifies any such alternative path, so the hedge guards against an unestablished possibility while the claim asserts the opposite.

**Required**: Close the gap — either prove `m_L(d) = 2` is universal (MAKELINK is the sole placer of link-subspace V-positions, fork excluded, so no non-2 first link is reachable) and drop the hedge, or exhibit the reachable state in which a first link sits at depth ≠ 2 and weaken M-DepthConv accordingly.

## OUT_OF_SCOPE

(none — the ASN confines itself to MAKELINK and does not specify INSERT/DELETE/COPY/REARRANGE/version/replication mechanics; its references to K.μ⁻ and K.μ~ are used only to characterize the permanence of the created link, not to define those operations.)

VERDICT: REVISE
