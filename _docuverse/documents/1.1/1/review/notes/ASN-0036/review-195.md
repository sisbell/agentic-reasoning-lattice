# Review of ASN-0036

## REVISE

### Issue 1: S8a abbreviation stated three times — residual meta-prose from the demotion
**ASN-0036, Σ.M(d) contract / "Notation" paragraph / Properties table**: The same fact — that "S8a" is shorthand for the per-component domain restriction — appears in three places:
1. Σ.M(d) postcondition: "We abbreviate this unfolded form 'S8a' wherever it is cited below."
2. The standalone *Notation* paragraph after S8-fin: "Throughout, 'S8a' abbreviates the per-component form of the domain-restriction axiom... It is not a separate property; every citation of S8a below is a citation of the domain-restriction axiom in this unfolded shape."
3. The Properties table row "S8a (notation)".

**Problem**: This is exactly the accretion the anti-bloat classifier targets. The same statement is made in different words across sections, and the *Notation* paragraph's closing sentence ("It is not a separate property...") explains the *status* of the abbreviation rather than advancing any claim — the residue of the recent S8a demotion left behind as meta-prose the reader must skip. A reader following an S8a citation does not need a second-order assurance that S8a is "not a separate property."
**Required**: Keep one canonical statement — the per-component postcondition under the Σ.M(d) contract — and the one-line Properties-table pointer. Delete the standalone *Notation* paragraph (including the "It is not a separate property" sentence). The single postcondition note carries everything downstream citations need.

### Issue 2: ValidFirstInsertionPosition lists dependencies its derivation never uses
**ASN-0036, ValidFirstInsertionPosition (empty case), Depends**: "*Depends:* D-MIN; S8a, S8-depth; OrdinalShift, TumblerAdd, T3 (ASN-0034)."
**Problem**: The empty-case definition is `v = [1,1,...,1]` of depth `m`, with `m` supplied as a parameter precisely because no state-determined depth exists when `V_1(d) = ∅`. Its postconditions (subspace = 1, `#v = m`, S8a, exactly one `v`) follow directly from the constant tuple. None of the cited dependencies is load-bearing: D-MIN's antecedent (`V_1(d) ≠ ∅`) is false in this case; S8-depth is vacuous on an empty subspace; OrdinalShift and TumblerAdd describe a shift the definition never performs; T3 is not needed to see a fully-determined constant tuple is unique for fixed `(d, m)`. By contrast the non-empty (binary) case genuinely needs OrdinalShift/T3 — so this is not a uniform-citation artifact, it is an over-broad list.
**Required**: Trim the empty-case Depends to what the trivial definition actually consumes (S8a for the `m ≥ 2` lower bound; T0 for componentwise positivity if cited at all). If D-MIN is mentioned only to motivate that `[1,...,1]` matches the eventual minimum, state that as a one-line note rather than a dependency.

## OUT_OF_SCOPE

### Topic 1: Preservation of D-CTG, D-MIN, S2 under editing operations
**Why out of scope**: How INSERT/DELETE/COPY/REARRANGE re-establish contiguity, the minimum position, and functionality is operation-layer territory (operation-specific effects are explicitly excluded by Scope). The ASN correctly defers this in its Open Questions rather than asserting operation postconditions here; no error.

### Topic 2: Subspace-identifier alignment between V-positions and their I-address images
**Why out of scope**: Whether `subspace(v) = v₁` must match the element-field component of `M(d)(v)` is named as an operations-layer preservation obligation in the Open Questions. Treating it as a future obligation rather than a state invariant is appropriate; not a gap in this ASN.

VERDICT: REVISE
