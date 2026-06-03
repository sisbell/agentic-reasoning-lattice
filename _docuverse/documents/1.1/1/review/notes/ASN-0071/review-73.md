# Review of ASN-0071

The mathematics here is unusually careful. PC, PC-RANGE, and F-DEEP are derived with explicit case splits, the totality argument is non-circular, and the worked scenario discharges every precondition concretely (self-inclusion, cross-source dedup, the shallow/deep duals). I checked the PC componentwise-fact, the `#v = #u` / `#v > #u` boundary handling in PC-RANGE, and the finiteness chain — all hold. My findings are confined to forward-reference accretion, which this note's classifier asks me to surface.

## REVISE

### Issue 1: Forward-pointing justification inside the vspec definition
**ASN-0071, *The query***: "Relaxing depth-pinning is precisely what admits the cross-depth cases (F-DEEP and the shallow-anchor capture of Q_E below), in which `#u ≠ m_C`."
**Problem**: This sits in the definitional slot but does not advance the definition's meaning. It is a defensive justification of *why* a clause was relaxed, citing two downstream labels (`F-DEEP`, `Q_E`) the reader cannot yet evaluate. The definition already stands on its own preconditions; the reader must skip past this to reach the next obligation. This is the flagged "definition's introduction enumerates downstream consumers" / forward-pointer pattern.
**Required**: Delete the sentence. The cross-depth behavior is established where it is derived (PC-RANGE, F-DEEP); the definition needs only the relaxed precondition list.

### Issue 2: Proof-choice meta-prose in *Resolution*
**ASN-0071, *Resolution***: "We reprove its integrity (`iaddrs(Q)(Σ) ⊆ dom(Σ.C)`, below) rather than cite ASN-0058's C1, because dropping well-formedness places vspecs outside C1's hypothesis." and "It is the set-image counterpart of ASN-0058's `resolve(d_s, σ)`, which returns an ordered, width-annotated sequence … because membership in `find` is order- and multiplicity-insensitive."
**Problem**: Both passages narrate *why a different object/proof is used* instead of advancing the argument. The first explains why a citation is unavailable; the second compares against a foundation object the reader does not need. The subset claim's actual proof (subspace confinement + S3★) follows immediately and is self-contained — the meta framing is skippable.
**Required**: Drop the "rather than cite C1 because…" clause and the "set-image counterpart of resolve…" comparison. State `iaddrs_one` as a definition and prove the subset claim directly. If the order/multiplicity distinction matters, one clause ("`find` is set-valued, so order and multiplicity are discarded") suffices.

## OUT_OF_SCOPE

### Topic 1: Relationship between current-state result and the historical relation R
**Why out of scope**: The three Open Questions (R-vs-current correspondence, reject-vs-filter policy for unresolvable positions, contraction invariant) are correctly deferred. F-CUR fixes the present-tense semantics cleanly; tying it to `R` or to K.μ⁻ transitions is new territory, not a defect here.

VERDICT: REVISE
