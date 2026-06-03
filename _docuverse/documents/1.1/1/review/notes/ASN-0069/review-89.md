# Review of ASN-0069

## REVISE

### Issue 1: V4's design-commitment justification appeals to its own downstream corollary
**ASN-0069, §"The Arrangement Layer", V4**: "The literal-inheritance form has two structural justifications." → *Why V-positions are not rebased.* "...would (a) require selecting a target depth/subspace identifier scheme... and (b) destroy the structural correspondence that **V8 below** requires."

**Problem**: V4 is the design commitment from which V8 is explicitly derived ("**V8** ... corollary of V4 + content-source operand frame"). Justifying V4 by appeal to "the structural correspondence that V8 below requires" is circular — the premise is defended by a consequence of the premise. Beyond the logical loop, the two "Why X is not rebased" sub-paragraphs are defensive rationale rebutting an *imagined* rebasing alternative, paralleling the duplication-vs-transclusion rationale already carried in full by §"Sharing, Not Duplication". This is the accreted "why the commitment is made" prose the anti-bloat pass targets, not advancement of V4's consequences.

**Required**: Remove the circular V8 appeal. If a justification for fixing `φ` to the identity is kept, ground it in forward-independent facts only (V-positions do not encode the owning document; I-address permanence by P0/S0), and trim the "(a)/(b)" enumeration. The rebasing rebuttal should not re-litigate the design choice already settled upstream.

### Issue 2: V9b derivation closes with cross-claim branch-accounting that does not advance the claim
**ASN-0069, §"Provenance Recording", V9b derivation**: "The direct-allocation branch of V9a's enumeration of acquisition paths is therefore vacuous for fresh forks; only the fork-from-`d_src` and transclusion-from-third-document branches contribute."

**Problem**: V9b's claim is `origin(a) ≠ d_new`, fully discharged by the preceding sentence (S7 + `A_C(d_new)` emitted nothing pre-fork). The closing sentence is a use-site annotation about which branches of *another* property's (V9a's) prose enumeration survive — it adds no step to V9b's proof and forces the reader to cross-reference V9a's informal "three pieces" list to parse it.

**Required**: Delete the closing sentence. The derivation is complete at `origin(a) ≠ d_new`.

### Issue 3: V8c carries notation-domain bookkeeping in a structural slot
**ASN-0069, §"Structural Correspondence", V8c**: "The set is taken over `(d_op, d_new)` to match V8's domain — the content source operand `d_op`, which equals `d_src` only on a first fork; on a subsequent fork `d_op = d_prev` and the displayed set is the first-fork specialization."

**Problem**: V8c's substantive claim is that the corresponding-position set is symmetric and document-type-untyped (invariant under operand swap). The quoted sentence is bookkeeping explaining why the displayed set uses `(d_op, d_new)` — a re-statement of the operand convention already fixed at §"What Must Be Constructed" and in V8. It interrupts the symmetry argument with redundant operand-tracking.

**Required**: Reduce to the symmetry/untypedness claim. The operand convention is already established; V8c need not re-derive which operand is which.

### Issue 4: Editorializing adjectives in structural prose
**ASN-0069, §"Subspace Selectivity"**: "The content-subspace restriction is therefore **principled, not arbitrary**: CL-OWN requires..." — and V8 header "(*positional correspondence — corollary of V4 + content-source operand frame*)" followed by "**This is V4 re-expressed in post-state coordinates**."

**Problem**: The CL-OWN sentence carries the actual content (transcluding `d_op`'s links would violate CL-OWN since `origin = d_op ≠ d_new`); "principled, not arbitrary" is editorial framing that adds nothing. Similarly "This is V4 re-expressed in post-state coordinates" is meta-commentary on V8's relationship to V4 that sits before the derivation already proving exactly that relationship.

**Required**: Drop "principled, not arbitrary" and "This is V4 re-expressed in post-state coordinates"; let the CL-OWN consequence and the V8 derivation stand on their own.

## OUT_OF_SCOPE

### Topic 1: Mixed first/subsequent-fork chains in V11
**Why out of scope**: V11 scopes its claim to chains where every step is a *first* fork of its immediate source. Transitive identity along chains that interleave first and subsequent forks (or branch) is genuinely new territory — a future ASN, not a defect here. V11 correctly states its premises.

### Topic 2: Concurrent fork during source modification, descendant enumeration, snapshot-vs-living forks
**Why out of scope**: These are raised correctly in §"Open Questions" as future work; they require operations and guarantees this ASN does not introduce.

VERDICT: REVISE
