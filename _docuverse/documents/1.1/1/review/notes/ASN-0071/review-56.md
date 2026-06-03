# Review of ASN-0071

This is a careful, largely sound specification. The PC proof (componentwise fact + totality + well-ordering closure) is rigorous, PC-RANGE's depth-split biconditional checks out in both directions, and the worked scenario exercises single-address, multi-address, and cross-depth queries against concrete states. My findings are structural/precision issues consistent with the anti-bloat mandate, not gaps in the core mathematics.

## REVISE

### Issue 1: F-DEEP introduced by forward-reference to an undefined label
**ASN-0071, *Resolution* ("Which positions resolve")**: "We record this dual boundary of F-FILT as **F-DEEP**: a vspec whose anchor is deeper than the source's arrangement depth resolves to nothing."
**Problem**: F-FILT is first characterized in prose only later, in *A worked scenario* ("...are silently dropped (F-FILT)"), and formally in the claims table — both downstream of this sentence. So F-DEEP is anchored to a label the reader has not yet met. The "dual boundary of F-FILT" phrasing is also editorial framing: F-DEEP (empty resolution when `#u > m_C`) and F-FILT (dropping positions in `⟦σ⟧ \ dom(M)`) are distinct mechanisms, and the cross-reference advances neither claim.
**Required**: State F-DEEP on its own terms (`#u > m_C ⟹ iaddrs_one = ∅`, via S8-depth `#v = m_C < #u`) without the "dual boundary of F-FILT" gloss; or introduce F-FILT before F-DEEP references it.

### Issue 2: `wp-defined` used in *Resolution* before it is defined in *The operation*
**ASN-0071, *Resolution*** (opening): "...we evaluate at a state `Σ` where each named arrangement `Σ.M(d_s)` is defined — the semantic precondition `wp-defined` established in *The operation*."
**Problem**: The entire Resolution section depends on a precondition whose definition appears in a later section, and the prose explicitly defers downstream ("established in *The operation*"). `wp-defined` is also the gating condition in the F-iaddrs table row, so it logically belongs with `iaddrs`, not after it.
**Required**: Define `wp-defined: (A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)` at or before the first `iaddrs_one` use, removing the forward pointer.

### Issue 3: PC-RANGE prose gloss overstates the captured set
**ASN-0071, *Resolution***: "The captured set ... is the union of `ℓ_{#u}` sibling subtrees ... The width-1 case `ℓ_{#u} = 1` ... captures the single subtree under the prefix `u`."
**Problem**: The captured set is `⟦σ⟧ ∩ dom(M(d_s))`, not the geometric union of subtrees. Under D-SEQ★ the intermediate components of every arrangement position are pinned to `1`, so most of those geometric subtrees contain no arrangement positions — and if some `u_j ≠ 1` for `2 ≤ j < #u`, the intersection is empty even when `#u ≤ m_C`. The set equation itself is correct; the gloss reads as if the subtrees are populated.
**Required**: Qualify the gloss — the captured set *lies within* the union of `ℓ_{#u}` sibling subtrees, with actual membership determined by `∩ dom(M(d_s))` (and constrained by D-SEQ★'s prefix pinning).

## OUT_OF_SCOPE

(none — the three Open Questions correctly defer the `R`-relationship, reject-vs-filter policy, and contraction-boundary invariant to future ASNs.)

VERDICT: REVISE
