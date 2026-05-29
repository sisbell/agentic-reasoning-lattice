# Review of ASN-0036

## REVISE

### Issue 1: OrdinalShift postcondition restated three times
**ASN-0036, "Singleton span partition" / "Valid insertion position"**: The same OrdinalShift fact (`shift(v,1)` preserves components `< m`, sets last to `v_m + 1`, hence preserves the subspace identifier for `m ≥ 2`) is spelled out in three places:
- Singleton intro: "By OrdinalShift's postconditions, `shift(v, 1)` agrees with `v` on positions `1 ≤ i < m` and has `shift(v, 1)_m = v_m + 1`; for `m ≥ 2` the first component … is therefore preserved."
- Empty-case prose: "For `m ≥ 2`, OrdinalShift (ASN-0034) preserves component 1, so the subspace identifier is preserved under shift."
- Non-empty derivation: "By OrdinalShift (ASN-0034), whose postconditions give `shift(v, n)ᵢ = vᵢ` for `i < m` and `shift(v, n)_m = v_m + n` …"

The latter two are adjacent and say the same thing in different words — exactly the "two paragraphs say the same thing" pattern.
**Problem**: Foundation postcondition restated rather than cited; the precise reader must re-read identical content across sections.
**Required**: State the consequence (`shift` preserves the subspace identifier and increments the ordinal) once, and cite OrdinalShift by reference at later use-sites.

### Issue 2: V-position definition duplicated with wording drift
**ASN-0036, S8a**: The prose says "A V-position is, by definition, an element-field tumbler of depth at least 2," while the Formal Contract Definition says "A V-position is, by definition, an isolated element field of depth at least 2."
**Problem**: Same definitional commitment stated twice with drifting phrasing ("element-field tumbler" vs "isolated element field"). Two phrasings invite divergence under future revision.
**Required**: One canonical phrasing in the Definition slot; the prose should reference it, not re-state it.

### Issue 3: Rhetorical meta-prose in the S7 Permanence proof
**ASN-0036, S7 proof, "Permanence"**: "The attribution cannot be severed because it is not a separate datum attached to the content — it is a structural property of the address itself. To retrieve content at `a`, a system must know `a`; to know `a` is to know `origin(a)`."
**Problem**: The derivation is already complete (S0 gives persistence; `origin` is a deterministic function of `a`'s components; S4 prevents reuse). These closing sentences restate the conclusion rhetorically without advancing the chain — meta-prose in a proof slot.
**Required**: End the proof at the established conclusion; drop the rhetorical restatement or move it to surrounding exposition.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG/D-MIN/S2
The ASN defines `ValidInsertionPosition` but how INSERT/DELETE/COPY/REARRANGE preserve contiguity is correctly deferred (Open Questions; Scope excludes operation-specific effects). Not an error here.

### Topic 2: Subspace alignment between `subspace(v)` and the I-address element field
Whether `M(d)(v)`'s first element-field component must match `subspace(v)` is correctly raised as an operations-layer obligation, not a state invariant. Belongs in a future ASN.

Note on correctness: the substantive proofs — S8's singleton partition (within-subspace incompatibility lemma covering `j < m` and `j = m`, the `m = 2` boundary, and the cross-subspace T5/T10 argument), D-CTG-depth (including the `j = m−1` boundary), and D-SEQ — were checked case by case and are sound. The worked example correctly exercises S0/S3/S5/S7/S8/D-SEQ across transclusion and deletion. No correctness defect found; the findings above are bloat/redundancy under the `anti-bloat` classifier.

VERDICT: REVISE
