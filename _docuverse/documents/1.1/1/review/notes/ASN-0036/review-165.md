# Review of ASN-0036

The state model (S0–S5, S7-family) and the partition/contiguity chain (S8, D-CTG, D-CTG-depth, D-MIN, D-SEQ) are, as far as the proofs go, sound. I checked the S8 within-subspace incompatibility lemma (both branches `j < m` and `j = m`), the across-subspace argument via T5 + T10, the D-CTG-depth infinite-intermediate construction, and the four-step D-SEQ assembly — each case is covered and the boundary cases (empty arrangement, `m = 2`, `m ≥ 3`) are handled. The worked example exercises S0/S3/S7/S8/D-SEQ at depths 2 and 3 and includes both an ill-formed-state check and the higher-depth violation. The findings below are anti-bloat and clarity items, which this note's `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: S8a is an admitted alias retained "for downstream citation"
**ASN-0036, S8a (V-position componentwise positivity)**: "S8a is a per-component alias for that conjunct, retained as a name for downstream citation."
**Problem**: This is the flagged reviser-drift pattern — a property whose introduction justifies its existence by downstream consumers rather than advancing meaning, and which the prose itself concedes is "definitionally equivalent" to the domain-restriction axiom's `zeros(v) = 0`. Carrying both the domain-restriction axiom and S8a as separate named properties (the Properties table even lists S8a as "alias of the domain-restriction axiom over T0") is duplicated state the precise reader must reconcile.
**Required**: Either fold the per-component form into the domain-restriction axiom's postconditions (and have S8-depth/D-CTG/D-SEQ cite the axiom directly), or keep S8a as the sole carrier and delete the axiom's redundant `zeros(v) = 0` conjunct. Remove the "retained as a name for downstream citation" justification regardless.

### Issue 2: The S8a ≡ `zeros(v)=0` equivalence is restated four times
**ASN-0036, S8a**: the same equivalence appears in the body ("definitionally the statement that every component is strictly positive… `zeros(v) = 0 ⟺ …`"), the Postconditions ("definitionally equivalent to the axiom's `zeros(v) = 0` over the ℕ-carrier"), the Depends ("over which `zeros(v) = 0` and per-component positivity are the same statement"), and the Properties table ("definitionally equivalent over the ℕ-carrier").
**Problem**: Two-or-more paragraphs saying the same thing in different words — compounds the bloat of Issue 1.
**Required**: State the equivalence once, at the carrier of S8a; drop the restatements in the Postconditions/Depends/table.

### Issue 3: "Strand" is never defined
**ASN-0036, title and §"The strand model fixes only the lower bound…"**: the ASN is titled "Strand Model" and refers to "the strand model" / "strand-level commitment," but the body describes the construct only as the "two-stream architecture" / "two-component model."
**Problem**: The central term naming the ASN is never introduced; the shared vocabulary has no "strand" entry. A self-contained ASN should define its titular object.
**Required**: Add a one-line definition tying "strand" to the two-component state `(Σ.C, Σ.M)`, or rename to match the terminology the body actually uses.

### Issue 4: "Why the axiom is needed" prose on the domain-restriction axiom
**ASN-0036, §"Two components of state", Σ.M(d) domain-restriction axiom**: "This is definitional, not derived: it fixes what kind of tumbler may serve as a V-position."
**Problem**: Status/rationale prose in a structural slot — the "definitional not derived" claim is already carried by the axiom label. Minor, but it is the kind of meta-justification that accretes across cycles.
**Required**: Drop the sentence, or compress to the axiom label itself.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG/D-MIN/S2 and subspace alignment
The Open Questions correctly defer how INSERT/DELETE/COPY/REARRANGE preserve the contiguity invariants and establish `subspace(v) = v₁` alignment with the mapped I-address. This is operation-layer territory (per Scope), not a gap in this ASN.

### Topic 2: Sharing-inverse computability and `Val` typing
The cost bound for the I-address→referencing-documents inverse and the structure of `Val` are genuinely new territory raised in Open Questions, not errors here.

VERDICT: REVISE
