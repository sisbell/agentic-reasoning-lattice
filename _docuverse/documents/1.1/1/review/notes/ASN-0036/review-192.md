# Review of ASN-0036

## REVISE

### Issue 1: S8a carries residual status meta-prose duplicating the properties table
**ASN-0036, S8a (V-position componentwise positivity and depth)**: "S8a is the per-component unfolding of the domain-restriction axiom via T0, not an independent obligation."
**Problem**: This sentence states S8a's *logical status* (derived, not new), not what S8a *says*. The same status is already recorded in the Properties table ("alias of the domain-restriction axiom, T0"). A precise reader skips it to reach the claim. The prior cycle flagged S8a accretion; the latest revision trimmed "alias framing" but left this status line — it is the same category of meta-prose.
**Required**: Delete the closing sentence. The derivation chain ("By T0, zeros(v) = 0 holds exactly when every component is positive, so the domain-restriction axiom yields…") already shows the formula is an unfolding; no separate status assertion is needed.

### Issue 2: The δ / shift foundation definition is restated back-to-back
**ASN-0036, "Shift preservation for V-positions" intro and OrdShiftHom proof**: intro — "advances a V-position by `shift(v, n) = v ⊕ δ(n, m)` (OrdinalShift), where `δ(n, m) = [0, ..., 0, n]` of length m (OrdinalDisplacement)"; proof — "Write `shift(v, n) = v ⊕ δ(n, m)` with `δ(n, m) = [0, ..., 0, n]` of length m (OrdinalShift, OrdinalDisplacement)."
**Problem**: Two adjacent passages restate the identical foundation definition in different words. OrdinalShift and OrdinalDisplacement are foundation claims (ASN-0034) that may be cited and used without re-derivation; restating the same expansion twice within a few lines is the "two paragraphs say the same thing" pattern this note is classified to surface.
**Required**: State the `shift = v ⊕ δ(n,m)` / `δ(n,m) = [0,…,0,n]` expansion once (in the lemma proof, where it is load-bearing), and have the subsection intro simply name the lemma's role without re-expanding the definition.

### Issue 3: OrdinalShift's positional behavior is re-described at each use site
**ASN-0036, OrdShiftHom proof, ValidInsertionPosition Derivation, worked example**: e.g. ValidInsertionPosition — "By OrdinalShift, for m ≥ 2 shift preserves components 1 ≤ i < m and increments position m, so `shift([1,...,1], j) = [1,...,1,1+j]`."
**Problem**: The "preserves leading components, increments the last" behavior of OrdinalShift/TumblerAdd is a foundation guarantee re-narrated at three separate sites. (The worked-example occurrence is acceptable — concrete examples are exempt — but the OrdShiftHom proof and the Derivation both re-derive the generic positional behavior that the foundation already fixes.)
**Required**: Derive the positional behavior once (OrdShiftHom already does this from TumblerAdd); downstream uses should cite OrdShiftHom rather than re-deriving from OrdinalShift.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG / D-MIN / S2 under INSERT, DELETE, COPY, REARRANGE
**Why out of scope**: The contiguity invariants are stated here as well-formedness constraints on states; whether each editing operation re-establishes them is operation-specific frame/postcondition work, correctly deferred to a future ASN and already named in the Open Questions and Scope sections. Not an error in this ASN.

### Topic 2: Canonical choice of empty-subspace depth `m` in ValidFirstInsertionPosition
**Why out of scope**: The ternary predicate leaves `m ≥ 2` free; pinning the convention is an allocation-policy decision at the operations layer, appropriately flagged as open rather than resolved here.

VERDICT: REVISE
