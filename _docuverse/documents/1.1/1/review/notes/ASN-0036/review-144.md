# Review of ASN-0036

## REVISE

### Issue 1: Citations to a dissolved "ordinal-shift prefix lemma"

**ASN-0036, ValidInsertionPosition (prose) and Worked example (Σ₁)**: "By the ordinal-shift prefix lemma, `shift([1, 1, ..., 1], j)` keeps components 1 through `m − 1` unchanged and sets the last to `1 + j`." and "`shift(1.1, 1) = [1, 2]` by the ordinal-shift prefix lemma (component 1 preserved, last component `1 + 1 = 2`)."

**Problem**: The most recent revision dissolved the ordinal-shift prefix lemma (commit ba0e13a), but two derivations still cite it by name. There is no lemma of that name defined anywhere in the ASN — these are dangling references to a non-existent claim. The `Depends` lists already name `OrdinalShift, TumblerAdd, T3 (ASN-0034)`, so the prose and the contract are now inconsistent: the contract delegates to OrdinalShift while the prose delegates to a phantom.

**Required**: Replace both citations with a direct appeal to OrdinalShift (ASN-0034), whose postconditions give `shift(v, n)ᵢ = vᵢ` for `i < m` and `shift(v, n)_m = v_m + n` for `n ≥ 1`. Note the `j = 0` case separately as the local identity convention (OrdinalShift requires `n ≥ 1`, so it does not cover `shift(·, 0)`).

### Issue 2: S8 partition proof omits the empty-arrangement boundary

**ASN-0036, S8 proof**: "By S8-fin, `dom(M(d))` is finite. By S2 (ArrangementFunctionality), `M(d)` is a function, so each `v ∈ dom(M(d))` has a uniquely determined image..."

**Problem**: The canonical boundary case — `dom(M(d)) = ∅` — is never named. Postconditions (a) and (b) hold vacuously and the singleton collection is the empty partition, but a partition theorem must state that its empty instance is covered. The base-case note at the end of the D-CTG section addresses D-CTG/D-MIN vacuously but not S8.

**Required**: Add one line to the proof: when `dom(M(d)) = ∅`, the singleton collection is empty and conjuncts (a), (b) hold vacuously.

### Issue 3 (anti-bloat): Downstream-consumer justification in D-CTG

**ASN-0036, D-CTG**: "D-CTG-depth and D-SEQ are unaffected: their constructed intermediates are already zero-free."

**Problem**: This sentence does not advance D-CTG's own meaning; it defends the `zeros(v) = 0` guard against its effect on two downstream claims. This is the "definition enumerates downstream consumers" pattern the anti-bloat classifier flags — a reader following D-CTG must skip past a claim about D-CTG-depth and D-SEQ that belongs (if anywhere) in those proofs.

**Required**: Remove the sentence. If the zero-freeness of the constructed intermediates matters to D-CTG-depth/D-SEQ, it is already established locally in each of those proofs ("we also verify that w satisfies S8a").

### Issue 4 (anti-bloat): S3 one-directionality stated twice; S8a forward-justifies S8-depth

**ASN-0036, S3 prose vs. S3 Frame**: the prose ("We observe a deliberate asymmetry. S3 says arrangement implies existence... It does NOT say existence implies arrangement...") and the Frame line ("S3 is one-directional — content may exist in `dom(C)` without being referenced...") restate the same asymmetry in different words.
**ASN-0036, S8a prose**: "...grounding the application of tumbler ordering properties to V-positions and justifying S8-depth's reference to 'within a subspace.'"

**Problem**: The S3 duplication is the "two paragraphs say the same thing" pattern across a prose slot and a formal-contract slot. The S8a clause forward-justifies why a later claim (S8-depth) is well-formed rather than advancing S8a's own content.

**Required**: Drop the redundant half of the S3 statement (keep the richer prose, trim the Frame to the formal `ran(M(d)) ⊄ dom(C)`-style assertion). In S8a, end the sentence at the T5 contiguity fact; remove the "justifying S8-depth's reference" tail.

## OUT_OF_SCOPE

### Topic 1: Operation preservation of D-CTG/D-MIN
The Open Questions correctly defer whether DELETE/INSERT/COPY/REARRANGE preserve D-CTG, D-MIN, and S2 to a future operations ASN. The worked example's suffix-deletion is illustrative only; mid-span deletion and renumbering are operation semantics, properly out of scope.

### Topic 2: Subspace-alignment between `subspace(v)` and the I-address's element field
Whether `v₁` must match the I-address's first element-field component is correctly flagged as an operations-layer obligation, not a state invariant of this ASN.

VERDICT: REVISE
