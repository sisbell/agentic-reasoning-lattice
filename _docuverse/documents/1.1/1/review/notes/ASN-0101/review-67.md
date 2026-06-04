# Review of ASN-0101

## REVISE

### Issue 1: D10's non-DEL inductive case cites a theorem whose scope excludes DEL-containing histories
**ASN-0101, D10 boundary derivation**: "If its final step is *not* DEL, the entire composite lies in the pre-DEL vocabulary, and ASN-0047's ExtendedReachableStateInvariants theorem establishes P4★ and P7a at `B_{j+1}` directly."

**Problem**: The induction runs over boundaries `Σ₀ →* B₁ →* ... →* B_N` in a *DEL-extended* trace. A boundary `B_j` may therefore have been reached by an earlier composite that contained DEL. ASN-0047's ExtendedReachableStateInvariants is a reachability theorem: it guarantees the composite-boundary properties only for states reachable from `Σ₀` by composites drawn from ASN-0047's (pre-DEL) vocabulary. When the history to `B_j` includes DEL, `B_{j+1}` is *not* such a reachable state, so the theorem does not apply to it "directly." The ASN itself states this exclusion in the very next paragraph — "not a fresh appeal to ASN-0047's theorem, which does not cover the DEL-containing composite that may have produced `Σ`" — and then makes exactly that appeal for the non-DEL composite. The proof is internally inconsistent on whether the global theorem may be invoked over a DEL-touched history.

**Required**: Discharge the non-DEL inductive case the same way as the DEL-terminated case — inductively, from the IH at `B_j` plus the composite's coupling constraints (J0, J1★) and P2 monotonicity — rather than by re-citing ASN-0047's global theorem. (The DEL-terminated derivation already uses only IH + coupling + N1/N3-style neutrality, none of which is DEL-specific, so a single unified inductive step covers both cases.) Alternatively, establish that ASN-0047's theorem has a per-composite inductive form that propagates boundary properties across one composite regardless of prior history.

### Issue 2: Defensive meta-prose around N1–N3 explains the framing rather than advancing the argument
**ASN-0101, D10 boundary derivation**: "(A DEL step may itself sit at a non-boundary intermediate pre-state where P4★ need not hold — for instance after a K.μ⁺ whose provenance a later K.ρ has not yet recorded — which is why N1–N3 speak of DEL introducing no new violation rather than of P4★ holding at the DEL pre-state.)"

**ASN-0101, N1**: "Either way DEL cannot break P4★ — it is the monotone-shrinking-and-`R`-fixing direction that matters, not a (false) per-state assumption at the DEL pre-state."

**Problem**: Both passages are defensive justifications of *why* the argument is phrased as it is (anticipating and rebutting a "false per-state assumption" that the framing already avoids) rather than object-level content. This is the forward-reference/reviser-drift pattern the anti-bloat classifier flags: prose that explains the proof's framing choices instead of stating facts the proof needs. A reader must work around it to follow N1–N3.

**Required**: State N1–N3 as the bare facts ("DEL is content-subspace-monotone-shrinking and fixes `R`, so it introduces no new P4★ violation") and delete the meta-commentary about what assumption the framing avoids.

### Issue 3: Worked example and boundary cases verify D8/D9/D11 before those claims are stated
**ASN-0101, "A worked example"**: "*Verification of D8.* ... *Verification of D9 (link projection).* ... *Verification of D11* ..."

**Problem**: D8 is defined in "What is preserved," D9 in "Link discoverability," D11 in "Weakest precondition…" — all sections *after* the worked example and boundary-case sections that already verify them by label. The reader encounters "Verification of D8/D9/D11" before any of those claims exist, forcing a skip-ahead.

**Required**: Either move the verification subsections to follow the claim statements, or forward-name the claims at first verification with a one-line gloss so the example is readable cold.

## OUT_OF_SCOPE

### Topic 1: Reconstruction / reversibility machinery
The Open Questions correctly route version reconstruction, DEL-then-INSERT recovery, and orphan rediscovery to downstream ASNs. These are new territory (versioning, history), not defects here.

VERDICT: REVISE
