# Review of ASN-0114

I worked through F0–F8, the two collapses, the wp derivations, and the worked instance. The mathematics is sound: F1's two inclusions are the two faithfulness failure modes, F2 is correctly derived from F1 + span convexity (S0), the F5 chain through LP13 is valid, the slot-3 discharge via the two collapses is correct, and the worked example's tumbler arithmetic (a₃ ⊕ δ(2,#a₃) = a₅, disconnectedness witness q = a₅, the F vs T distinction) checks out. The ASN stays properly abstract — it binds the contract at coverage, leaves representation free (F3), and carefully separates the contract from implementation artifacts (span ordering, bounded queries, the resolution-into-arrangement step). No META.

Two findings remain.

## REVISE

### Issue 1: The set of "primary" claims is stated two incompatible ways

**ASN-0114, "The selector and its domain" vs. "Synthesis"**:

- Selector section: "Three commitments remain — F1, F4, F7. We take them in turn."
- Synthesis: "under five primary constraints — F1, F4, F5, F7, F8 — with F2, F3, and F6 following as corollaries of F1."

**Problem**: These disagree on whether F5 (TemporalDeterminism) and F8 (ContentIndependence) are primary commitments or derived consequences. The selector section names *three* and excludes F5/F8 (implying they fall out of F1/F4/F7); the synthesis names *five* and elevates F5/F8 to primary (implying they do not). The Claims table reinforces the first reading for F5 ("from F1 and L12 … composed by LP13") while the synthesis contradicts it. The "we take them in turn" promise then delivers eight sections (F1–F8), not three. A reader cannot tell from the document which claims the ASN actually *commits* to versus which it *derives* — and that is precisely the load-bearing distinction the claim inventory is supposed to settle.

**Required**: Pick one characterization and make the selector section, the synthesis, and the Claims-table status column agree. If F1, F4, F7 are the genuine independent commitments and F2/F3/F5/F6/F8 are consequences (F5 from F1 + immutability, F8 from F0 + F1, etc.), say so in both places; if F5 and F8 are primary, change "Three commitments remain — F1, F4, F7" accordingly.

### Issue 2: Citation-procedure meta-prose in the F5 derivation

**ASN-0114, "Determinism over time" (F5 derivation)**: "This composition is exactly LP13 … — '…' — which ASN-0098 obtains from L12 via its closure schema (★). We invoke that closure as established rather than re-running it here."

**Problem**: F5's chain needs only two links: LP13 gives `Σ'.L(a) = Σ.L(a)`, and F1 at each state gives coverage equality. The clause explaining *how ASN-0098 internally derives* LP13 (from L12 via schema ★), and the sentence justifying that we cite rather than re-prove a foundation lemma, advance neither link. This is exactly the "why we cite rather than derive" accretion the anti-bloat classifier targets — provenance-and-procedure prose the reader skips to follow the argument. (Citing LP13, a foundation lemma, needs no defense.)

**Required**: Trim to the direct citation — LP13 gives `a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)`, whence `Σ'.L(a).eᵢ = Σ.L(a).eᵢ` and F1 equates the coverages. Keeping the one-line motivation that single-step L12 is insufficient for the `→*` quantifier is fine; the provenance clause and the "rather than re-running it here" remark are not.

## OUT_OF_SCOPE

No out-of-scope errors. The ASN correctly defers resolution-into-arrangement (the V-position projection / filtering described in the implementation evidence), protocol/wire encoding of the ⟨⟩/⊥ distinction, returned-span-set normal form, and multi-document reporting to its Open Questions and the "boundary we must respect" section, consistent with the harness scope list. These are genuine future territory, not gaps in this note.

VERDICT: REVISE
