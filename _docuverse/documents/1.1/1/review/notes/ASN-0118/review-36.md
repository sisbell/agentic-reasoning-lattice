# Review of ASN-0118

I verified the ASN's claims clause by clause: the composite decomposition against ASN-0047's transition contracts, the coupling discharges (J0, J1★, J1'★) against their full quantifiers, the tiling arithmetic against ASN-0034's shift lemmas, the resolution grounding against ASN-0058's run machinery, and the worked example numerically. Summary of the checks that carried the most risk:

**J1★/J1'★ over the full post-state quantifier** (the prior cycle's open obligation). The discharge is now complete. Off-destination documents are handled by the arrangement frames plus CP12's `E'_doc = E_doc`, making both couplings vacuous there. At the destination, the range equation `ran_C(Σ', d) = ran_C(Σ, d) ∪ {c₀,…,c_{W−1}}` is derived in both directions (⊇ from CP2/CP3a/CP3b with OrdShiftHom(a); ⊆ from CP3c's domain closure plus the per-range image inventory), which reduces J1★'s universal obligation to membership for placed addresses. The three-way branch (range-new unrecorded → fresh K.ρ, J1'★-admissible; range-new recorded → P2; not range-new → P4★ + P2, with P4★ licensed by the composite-boundary standing precondition) covers every placed address, and CP8's ⊆ direction follows from the fixed K.ρ inventory. J1'★'s constraint is checked against exactly the pairs the canonical inventory creates, and the redundant-K.ρ variant is correctly shown to contribute nothing to `R' \ R`.

**The displacing-case decomposition.** The argument that no K.μ⁺ can vacate a position — forcing contraction-then-extension — is structurally correct against ASN-0047's strict-extension definition. K.μ⁻'s per-subspace retention is handled properly, including the degenerate cases: `j = 0` (D-MIN★ vacuous at the intermediate state), `V_{s_L}(d) = ∅` (`n'_{s_L} = 0 = n_{s_L}` still satisfies "retain in full"), and the strict-contraction requirement supplied by `n'_{s_C} = j < N`. K.μ⁺'s image-membership precondition is discharged for both placement images (CP0(a) + content frame) and displaced images (S3★ at Σ carried through K.μ⁻'s frame). CP3c's production — vacated positions re-entering only under their single new binding — is argued explicitly rather than asserted.

**Resolution grounding under the relaxed V-spec.** Dropping ASN-0058's condition (iii) is sound as argued: C1a's general form needs only single-subspace confinement (supplied by content-residence directly, not via C0a), single-depth comes from S8-depth on the active positions themselves, and the per-position lockstep (MaximalRun condition 1) grounds every expanded address — run interiors included — as the image of a bound position, which is what CP0(a) needs through S3★. The two micro-examples of shape-mismatched admissible spans compute correctly (`[1,1,5] ⊕ [0,9,0] = [1,10,0]` capturing `[1,2]…[1,10]`; `[1,1,5] ⊕ [0,9] = [1,10]` capturing `[1,2]…[1,9]`).

**Tiling and CP4 exactness.** The three-range layout `[min,p) ∪ [p,p+W) ∪ [p+W,max+W]` is derived from TS1/TS2/TS3/TS4 with the gap-closure step shown via shift composition. CP4's "exactly W" survives the adversarial cases I constructed: shifted bindings into the placed set are replaced one-for-one (vacated by CP3c), non-text positions cannot bind content addresses (S3★ + SD), and the per-address occurrence-count refinement is consistent with the aggregate.

**Worked example.** All tumbler arithmetic checks: zero counts, origins, span denotations, the single-run decomposition of source A (`a₂ = a₁ + 1` in lockstep with `[1,2] = [1,1] + 1`), the post-state arrangement, the S4-based range-newness of all three placed addresses, and the self-transclusion variant exercising the P4★ + P2 branch.

**Anti-bloat scan.** I checked the flagged patterns specifically. The condition-(iii) paragraph's exhaustiveness sweep ("no clause of CP0–CP12 mentions `#s` or `#ℓ`") is a checkable discharge obligation for relaxing a foundation precondition, and it is true of the document; the closure-inventory paragraph establishes frame completeness (every state component bounded above), which is substantive specification content; the two REPLICATE passages are not duplicates — the second derives the new origin-multiset consequence from the first. The Gregory paragraphs are implementation evidence of the kind the standards require. No paragraph forced me to skip past meta-prose to reach a claim.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Correspondence between multiple appearances of shared content
**Why out of scope**: COPY establishes shared identity; the relation that lets a reference to one appearance serve as a reference to all appearances is a distinct mechanism, already flagged in the ASN's Open Questions.

### Topic 2: Transclusion into the link subspace
**Why out of scope**: This ASN restricts placements to `s_C` by precondition; link-by-reference placement is new territory, correctly deferred in the Open Questions.

### Topic 3: Width shortfall under partial binding
**Why out of scope**: The relationship between a partially-bound span's nominal extent and its smaller resolved width is a property of the resolution discipline, not of the placement this ASN specifies; the ASN is honest that ASN-0058's C2 does not apply and defers the question.

VERDICT: CONVERGED
