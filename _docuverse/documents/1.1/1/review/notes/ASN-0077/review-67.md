# Review of ASN-0077

## REVISE

### Issue 1: Proof-strategy narration in the (F1)≡(F3) equivalence chain

**ASN-0077, "Lifting origin to a V-span" (Equivalence chain lead-in)**: "The decomposition `{β₁, ..., βₖ} = ...` introduced above (via C1a, ASN-0058) is the basis for the equivalence. O2 (Block uniformity, just established) is the load-bearing fact in both inclusions: it collapses the per-block origins to one representative `origin(aⱼ)`."

**Problem**: This lead-in advances no reasoning. The two inclusions that follow are self-contained and re-cite O2 and the decomposition where they actually use them. "is the basis for the equivalence" / "is the load-bearing fact in both inclusions" is meta-narration announcing what the proof is about to do, and "introduced above (via C1a)" restates a decomposition already in hand. This is the forward-reference accretion pattern (proof-strategy prose in a structural slot).

**Required**: Delete the lead-in; begin directly at "(F1) ⊆ (F3)".

### Issue 2: WF_V definition framed by downstream-consumer enumeration

**ASN-0077, "Permanence" (preamble to the WF_V definition)**: "The preservation and admissibility claims that follow all turn on the same six well-formedness conditions for a V-span query."

**Problem**: This sentence sits immediately before the WF_V definition and enumerates the definition's downstream consumers ("preservation and admissibility claims") rather than advancing the definition's meaning — the flagged "definition's introduction enumerates downstream consumers" pattern. The definition stands on its own; the claims that depend on it cite WF_V at their own sites.

**Required**: Remove the framing sentence; let the WF_V definition be introduced by its own content.

### Issue 3: O11★★ proof previewed before it is given, with redundant pre/post specialization statements

**ASN-0077, paragraph preceding O11★★, and the sentence following its derivation**: "The single-step claims O11 and O11' lift to a multi-step version by induction on chain length. ... Corollary O11.1 supplies per-step well-formedness preservation at each arrangement-extension sub-case of the induction. We prove the general mixed-chain lemma directly and obtain the pure-K.μ⁺ and pure-K.μ⁺_L chains as one-line specializations." — and after the derivation: "The pure-K.μ⁺ and pure-K.μ⁺_L chains are the obvious specializations of O11★★ (sub-case (ii), respectively sub-case (i), never fires)."

**Problem**: The preceding paragraph restates the entire structure of the O11★★ proof (induction on chain length, O11/O11' for extension steps, O7 for non-extension steps, O11.1 for well-formedness) that the derivation immediately delivers — a preview that duplicates the proof. Additionally, "We prove ... and obtain the pure-... chains as one-line specializations" (before) and "The pure-... chains are the obvious specializations" (after) say the same thing in two places — the redundant-pair / strategy-announcement pattern.

**Required**: Drop the preview paragraph (the derivation already carries the sub-case split and the O11.1/O7 citations) and keep only the post-derivation specialization sentence, or vice versa — not both.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
