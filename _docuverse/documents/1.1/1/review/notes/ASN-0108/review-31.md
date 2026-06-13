# Review of ASN-0108

This is a strong, deeply-worked note: the weakest-precondition analysis (W2), the partition proof under a variable size schedule (W4), and the battery of concrete walks (cut-point, cancellation, tail-reorder, blind-spot, cursor-survival, W9c divergence, four termination walks) all meet the depth bar. The findings below are one substantive precision gap and several instances of the forward-reference accretion the review mode flags.

## REVISE

### Issue 1: The matched-content key's state-stability is grounded on an assumption the key's own definition violates

**ASN-0108, "The Enumeration Order" (concretely) and W5/W8**:

The key is *defined* as the currently-matched endpoint: "the key is the **I-address of the content endpoint** each link matched … keys on the matched content's I-address … established during that traversal."

But its state-stability — load-bearing for W5 and W8 — is *grounded* on its being a fixed function of the endset:
- W5: "its value is a fixed function of the immutable endset (L12) over permanent I-addresses (S0), so both clauses hold for it as well."
- W8: "its value persists, since orphaning … leaves … the link's immutable endset … intact."

**Problem**: These are incompatible for multi-endpoint links under the very satisfaction semantics the note imports. `Match` is `findlinks_V` (any-slot discoverability, ASN-0127 LP12: discoverable iff *some* slot's coverage meets `ran(Σ.M(d_q))`), and an endset is a finite set of spans (ASN-0043) covering possibly many I-addresses. Take a link `L` whose from-endset covers I-addresses `{X, Y}`. At `Σ`, `X ∈ ran(M(d_q))` but `Y ∉` — `L` matches via `X`, key `= X`. After a `K.μ⁻` removes `X`'s V-position and a `K.μ⁺` admits `Y`'s, `L` matches via `Y`, key `= Y ≠ X`. Each I-address is individually permanent (S0), and the endset is immutable (L12) — yet the *selected* I-address that serves as `L`'s key has moved. If `X` and `Y` straddle a held cursor's key, that is precisely a clause-1 (cut-point) violation, so the asserted state-stability fails. The cited grounding (S0 + L12) establishes that each I-address is permanent and the endset is fixed, but state-stability of the *key* additionally requires the *selection* of which I-address represents a given link to be state-invariant — which "the endpoint each link matched … during that traversal" is not, for multi-endpoint links.

**Required**: Commit to one reading. Either (a) define the key as a genuinely fixed function of the immutable endset (e.g., the minimal I-address in the relevant slot's coverage, computed without consulting the arrangement), which restores state-stability and obliges correcting the "matched … during that traversal" language; or (b) acknowledge that for multi-endpoint links the currently-matched-endpoint key is *not* state-stable, which would force W5/W8/W9 to treat it as a partial case rather than a permanent key. The note clearly intends (a) (it wants both identity keys robust); it must say so, since the single-endpoint case is silently assumed throughout. W8's "its value persists" should likewise distinguish *computability* (always evaluable — true) from *value-invariance* (false under reading (b)); W8's purpose needs only the former.

### Issue 2: The "concretely" section pre-states the W5/W6/W8 verdicts before those claims exist

**ASN-0108, "The Enumeration Order"**: "Because the matched-content key is read from permanent content identity … it is, like the link-address key, *state-stable* (the W5 sense …) and *computable in every state* (the W8 sense …). The two permanent keys therefore differ in **exactly one** abstract respect — *allocation-monotonicity* (W6) …"

**Problem**: This is a use-site inventory: before W5, W6, or W8 are stated, it announces what each will conclude for each key. The same applies to the foil's pre-announcement ("a POOM-style walk … moves under K.μ~ and vanishes under K.μ⁻" — the W5 clause-1 and W8 computability hazards, stated in advance). The conclusions belong in (and are re-stated in) those claims; pre-stating them here forces the reader to verify three forward consistency obligations to follow the introduction of a definition.

**Required**: Introduce the three keys here (their definitions and the non-injectivity caveat are legitimate), and let W5/W6/W8 deliver their own verdicts. Cut the per-key pre-statement of downstream conclusions.

### Issue 3: The "two permanent keys differ only at W6 / W5 and W8 vacuous for both" thesis is restated at five sites

**ASN-0108**, the identical thesis appears in:
- "The Enumeration Order": "The two permanent keys therefore differ in **exactly one** abstract respect — *allocation-monotonicity* (W6)."
- W5: "W5 therefore does **not** separate the two identity keys at all; that separation is W6's … and W5 is vacuous for both."
- W6: "W5 and W8 are vacuous for it (both keys being permanent), so W6 is the entire abstract difference between the design intent and the implementation."
- W8: the parenthetical re-deriving the same vacuity.
- Claims table: W5 row ("so W5 does not separate them"), W6 row ("the sole discriminator from the link-address key"), W8 row.

The "ladder of key conditions" additionally re-derives the value-totality ⟹ state-stability relationship and the "Gregory's key is state-stable yet not value-total" fact that W5 and W8 also state.

**Problem**: A single comparative fact stated five-plus ways is exactly the accretion the review mode targets — the reader must hold five phrasings and confirm they agree.

**Required**: State the comparison once (W6 is its natural home — it is the discriminator) and let the other sites cite it without restating. The ladder may remain as a glossary if it stops re-deriving the inter-condition implications that W5/W8 already carry.

### Issue 4: The allocation-orthogonality argument is duplicated across W5 and W8 with mutual cross-deferral

**ASN-0108, W5**: "Allocation axioms enter only orthogonally … but none of these is what freezes the key … (W8 below leans on this same orthogonality of allocation and refers back to it rather than re-deriving it.)"

**ASN-0108, W8**: "Allocation enters only *orthogonally* here, exactly as set out under W5 (T8/LP13/GlobalUniqueness bear on the cursor's standing as an address, not on the computability of `κ(c)`) — **we do not repeat the argument**."

**Problem**: W5 forward-points to W8; W8 back-points to W5 and announces it will not repeat — then restates the argument's conclusion (T8/LP13/GlobalUniqueness bear on standing, not on the key). This is the "multiple paragraphs defer to the same location" pattern combined with a "do not repeat" disclaimer that repeats. The Claims-table W8 row carries it a third time ("T8/GlobalUniqueness only orthogonal (see W5)").

**Required**: State the orthogonality argument once (W5), and at W8 cite it by name without restating the conclusion. If W8 genuinely "does not repeat," the sentence after the disclaimer should not re-list T8/LP13/GlobalUniqueness.

## OUT_OF_SCOPE

The note scopes correctly. Count-only sizing is deferred at W10 ("a separate cardinality query — a distinct operation, out of scope here") and again in Open Question 5; multi-document enumeration is deferred to Open Question 1; the satisfaction predicate and type-refinement (ASN-0086) are explicitly handed to query construction. No claims stray into MAKELINK, FOLLOWLINK, FINDLINKS, or BEBE. No OUT_OF_SCOPE additions are needed.

META: Not warranted — W0–W11 are abstract guarantees on ordering, cursors, windows, and termination that any windowing implementation must honour; the udanax-green/spanfilade references are evidence for which key is used, not claim content, so the note has not drifted into implementation mechanics.

VERDICT: REVISE
