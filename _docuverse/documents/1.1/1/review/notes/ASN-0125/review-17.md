# Review of ASN-0125

The mathematics is sound. I traced the operation contracts (EL6, EL7), the discipline-maintenance induction (EL-DM), the discovery biconditional (EL11a), the commutation argument (EL13), the currency cases (EL14a–c), and the worked example's address arithmetic end to end; the reasoning holds, the edge cases (empty store at Σ₀, fork, mutual-supersession standoff, retraction-valued successor, position reuse) are each handled, and the weakest-precondition framing of EL0 is correct. The findings below are the anti-bloat residuals the classifier targets — forward-reference accretion and duplicated prose.

## REVISE

### Issue 1: EL7(ii) accretes EL11's discoverability characterization by forward reference

**ASN-0125, EL7(ii) (EditContract)**: "The edited reading is therefore archivally present from birth — `out(a', Σ₂) ∋ e_b` with `new(e_b) = a'` (EL11b), the successor named as its claim's superseding endpoint — yet *contextually dark* in every current view: its from-side projects into no document (the symmetric EL11a for `new`, the gate `listed(a', d, Σ₂)` empty everywhere), so nothing volunteers it until a separate `K.μ⁺_L` seats it under `home(a') = d_s`."

**Problem**: EL7 is the edit operation's contract — what is allocated and what the new reading is. The bare fact that the successor is *born unlisted* (not seated in any arrangement, by S3★ freshness; listing is a separate `K.μ⁺_L` act) is a legitimate "what the operation does not do" statement and should stay. But the sentence above goes further: it runs the archival-vs-contextual discoverability characterization — `out`/`in` membership, from-side projection, the `listed` gate — by forward-citing EL11a and EL11b, which are stated four claims downstream. This previews EL11's theorem inside EL7's contract, the exact "meta-prose around forward references" pattern. The discoverability semantics belong in EL11, where discovery is characterized; EL7 should state the user-facing fact and point forward, not re-derive it.

**Required**: Trim EL7(ii) to the bare unlisted fact ("the successor lies in no arrangement range, so it is auto-listed by no document; seating it is a separate `K.μ⁺_L` act") plus a single pointer to EL11. Remove the EL11a/EL11b-previewing "archivally present / contextually dark / from-side projects into no document" derivation.

### Issue 2: EL4 and Df-SUCC both state the `Ŝ^Σ = S^Σ` coincidence

**ASN-0125, EL4 (SingleTarget)**: "…at an edit-disciplined state every claim conforms, so `Ŝ^Σ = S^Σ`."
**ASN-0125, Df-SUCC (Successor relations)**: "…At an edit-disciplined state `Ŝ^Σ = S^Σ`, so the comprehensions range over the whole supersession slice and coincide with the unrestricted reading."

**Problem**: The same fact — schema-conformance is total at disciplined states, so `Ŝ^Σ = S^Σ` — is asserted in two adjacent passages. EL4 introduces `Ŝ^Σ` and the coincidence; Df-SUCC re-asserts the coincidence before using the restriction. Df-SUCC's *purpose* clause (totality at all reachable states, why accessors are undefined on non-conforming tuples) is new and belongs there; the restatement of the disciplined-state coincidence is the duplication.

**Required**: State the `Ŝ^Σ = S^Σ` coincidence once (EL4, where `Ŝ^Σ` is introduced). In Df-SUCC, keep only the restriction's purpose and use `Ŝ^Σ` without re-deriving its disciplined-state collapse.

## OUT_OF_SCOPE

The eight Open Questions are well-formed deferrals (authority on cross-asserter retraction, supersession/retraction independence, meta-claim stratification, currency non-emptiness under open authorship, temporal witnesses, span-level endset correspondence, edit-to-listing coupling, prefix-rooted subtype closure). None is content this ASN omits in error; each names genuinely new territory. No additional out-of-scope topics to raise.

VERDICT: REVISE
