# Review of ASN-0099

## REVISE

### Issue 1: Single-step/two-step atomicity distinction stated twice

**ASN-0099, "Link-Store-Inert Preservation"**: The V-definition prose says "a transition produced by a `V_atomic` operation is single-step (`Σ → Σ'`), whereas a transition produced by K.μ~ is the two-step composite `Σ →* Σ'` (its K.μ⁻ + K.μ⁺ decomposition)." A1a immediately restates the identical fact: "preserves the link store across its transition — single-step Σ → Σ' for the atomic operations, the two-step composite Σ →* Σ' for K.μ~."

**Problem**: Two paragraphs in the same section carry the same single-step/two-step bookkeeping in different words. The distinction is load-bearing exactly once — in A1a, whose conclusion form differs by it. The pre-statement in the V definition is recap the reader must read past.

**Required**: State the single-step/two-step distinction once. The V definition can introduce `V ≡ V_atomic ∪ {K.μ~}` without re-deriving A1a's transition-shape split; let A1a own it.

### Issue 2: Self-referential notation commentary in the V definition

**ASN-0099, "Link-Store-Inert Preservation"**: "`V` is local notation for this note, deliberately distinguished from ValidComposite★'s atomic vocabulary `V_atomic`."

**Problem**: This is meta-commentary about the notation choice ("local notation for this note," "deliberately distinguished") rather than content that advances the preservation argument. It is essay content in a structural slot — the kind of accretion the anti-bloat pass targets.

**Required**: Drop the self-referential framing. Defining `V = V_atomic ∪ {K.μ~}` and using it is sufficient; the reader does not need to be told the symbol is local or that the distinction is deliberate.

### Issue 3: Foundation-design rationale quoted to justify K.μ~'s exclusion

**ASN-0099, "Link-Store-Inert Preservation"**: "The named reordering K.μ~ is *not* atomic — ASN-0047 states it 'is not atomic; it may appear in the sequence as shorthand for its K.μ⁻ + K.μ⁺ decomposition.'"

**Problem**: The verbatim ASN-0047 quote explains the foundation's design (why K.μ~ is non-atomic) rather than stating what this ASN needs (that K.μ~ preserves `Σ.L`, established by transitive composition in A1a). It is rationale prose deferring to foundation text where a one-line statement of K.μ~'s status would do.

**Required**: Replace the quote with the operative fact: K.μ~ is the K.μ⁻ + K.μ⁺ composite, so A1a applies to it by transitivity. No quotation of ASN-0047's atomicity rationale is needed.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
