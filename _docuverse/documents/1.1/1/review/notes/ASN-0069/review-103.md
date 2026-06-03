# Review of ASN-0069

## REVISE

### Issue 1: V11's "Properties Introduced" table entry is a full-paragraph restatement
**ASN-0069, §"Properties Introduced", V11 row**: "Transitive identity along unedited fork chains: for every fork chain `d_src → d¹_new → ... → d^k_new` starting from initial state `Σ`, where each step is the first fork of its immediate source (so step `i`'s content operand `d_op = d^{i-1}_new`) and each step's source has its content-subspace arrangement (set and pointwise values) unchanged between the prior step's post-state and the current step's pre-state, `v ∈ dom(M^k(d^k_new))` at post-step-k and `M^k(d^k_new)(v)` at post-step-k equals `M(d_src)(v)` at `Σ`, for every `v ∈ V_{s_C}(d_src)` evaluated at `Σ`"

**Problem**: Every other row in the table is a one-line summary; this row is an ~80-word verbatim transcription of the lemma statement already given in full in §"Composability: Fork of a Fork". This is essay content in a structural slot — the table is meant to index the properties, not re-state them. The full statement and its two premises already live at the lemma site.

**Required**: Reduce the row to a one-line summary in line with the other entries (e.g., "Transitive identity along unedited first-fork chains: `d^k_new` inherits `d_src`'s I-addresses at every shared content-subspace V-position"). The premises belong at the lemma, not in the index.

### Issue 2: The final two Open Questions ask the same question in different words
**ASN-0069, §"Open Questions", last two items**:
- "What additional structure must the system provide to relate independently-typed but textually identical content across documents — counterpart correspondence that I-address identity alone, which assigns such content distinct addresses, cannot express?"
- "What must distinguish two distinct I-addresses holding equal byte values, if the specification is to treat them as non-identical content rather than collapse them by value?"

**Problem**: Both questions concern the same gap — content that is byte-equal but address-distinct, and how the specification should relate or distinguish it. One frames it as "counterpart correspondence," the other as "distinguish two I-addresses holding equal byte values," but the underlying open territory is identical. This is the "two paragraphs say the same thing in different words" pattern; carrying both is accretion.

**Required**: Collapse to a single open question covering byte-equal/address-distinct content, or sharpen the two so they ask genuinely distinct things (e.g., one about *typed* counterpart correspondence specifically, one about value-vs-identity collapse) rather than overlapping restatements.

## OUT_OF_SCOPE

### Topic 1: Concurrent-fork and snapshot-vs-living-fork semantics
**Why out of scope**: The Open Questions about concurrent modification during fork and the snapshot/living distinction correctly point to future ASNs; they are not defects in this derivation, which works under SequentialTransitionAxiom.

META: not applicable — the ASN stays in state/operation/invariant territory (entity creation, arrangement extension, provenance) stated abstractly enough to bind an alternative implementation.

VERDICT: REVISE
