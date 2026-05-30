# Review of ASN-0036

The mathematical core is sound. I checked S1, S4, S5, OrdShiftHom, S8, D-CTG-depth, D-SEQ, and the ValidInsertionPosition derivation; the proofs hold, edge cases (empty arrangement, singleton runs, depth-2 vs depth ≥3, the Σ₀ base state) are handled, and the worked example exercises the postconditions concretely. My findings are confined to the accreted prose the `anti-bloat` classifier asks me to surface, plus one redundant property name.

## REVISE

### Issue 1: Duplicated "structural encoding, not a lookup" claim across S7a and the S7 proof
**ASN-0036, S7a prose / S7 proof "Identification"**: S7a states "the home document is ascertainable from the address alone — not from a separate lookup table." The S7 proof's *Identification* paragraph restates: "This is not a lookup or annotation: the address structurally encodes its provenance."
**Problem**: Two paragraphs in the same note assert the same fact in different words — the reviser-drift pattern (restatement rather than removal). The proof paragraph is the load-bearing site; the S7a aside duplicates it.
**Required**: Drop the duplicated assertion from one location. Keep it in the S7 proof where it discharges the *Identification* step; remove the "not from a separate lookup table" gloss from S7a (or vice versa).

### Issue 2: S8a is a renamed alias of the domain-restriction axiom
**ASN-0036, S8a and the Properties table**: S8a is labeled "per-component unfolding of the domain-restriction axiom" with status "alias of the domain-restriction axiom." The domain-restriction axiom (`zeros(t) = 0 ∧ #t ≥ 2`) and S8a (`#v ≥ 2 ∧ (∀i : vᵢ > 0)`) are logically identical by T0.
**Problem**: Two labels for one constraint forces the reader to track that "S8a" and "the domain-restriction axiom" name the same thing — exactly the kind of accretion that compounds across cycles. Every downstream Depends line that cites "S8a" is citing the axiom under an alias.
**Required**: Either fold S8a's per-component form directly into the domain-restriction axiom's postconditions (and cite the axiom downstream), or demote the "alias" row to a one-line notational note rather than a numbered property. Do not carry both as first-class entries.

### Issue 3: Implementation-internals grounding for S5 reaches into out-of-scope territory
**ASN-0036, S5 prose**: "The global index that records which documents reference which I-addresses accumulates entries without cap — 'no counter, cap, MAX_TRANSCLUSIONS constant, or any other limiting mechanism anywhere in the code path.' Each referential inclusion adds one entry."
**Problem**: The abstract claim S5 needs is "S0–S3 entail no finite bound on multiplicity," and the proof establishes that independently and completely. The global transclusion index is enfilade/spanfilade machinery (Scope: "enfilade implementation internals") — citing its code path as grounding adds implementation mechanics the formal claim does not rest on. The Nelson quotation already supplies adequate architectural grounding.
**Required**: Trim the "global index / code path / MAX_TRANSCLUSIONS" sentences. The proof and the Nelson quote carry S5; the implementation detail is surplus and crosses into out-of-scope internals.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG / D-MIN / S2 under INSERT/DELETE
The note correctly defers (Open Questions) what each editing operation must guarantee to preserve contiguity, including insertion onto an occupied V-position. This is operation-specific frame/postcondition territory — a future ASN, not a gap here.

### Topic 2: Canonical choice of V-position depth `m` for an empty subspace
The strand model fixes only `m ≥ 2` and flags the specific value as an operation-layer convention. Pinning `m` (e.g., `m = 2` for basic INSERT) is an operations question, properly left open.

### Topic 3: Subspace-alignment between `subspace(v)` and the element-field subspace of `M(d)(v)`
Treated as an operations-layer preservation obligation. Belongs to the operation ASNs, not the state model.

VERDICT: REVISE
