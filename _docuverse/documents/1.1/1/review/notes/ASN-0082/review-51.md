# Review of ASN-0082

## REVISE

### Issue 1: Worked-example meta-commentary ("What this example adds")
**ASN-0082, Post-Contraction Shift / Post-Insertion Shift worked examples**: e.g. "**What this example adds.** Beyond the cross-subspace example, the one novel fact is that I3 operates correctly when the *active* subspace is sparse and D-CTG-exempt." and "The example exercises D-CS concretely: the link subspace V_2(d) — sparse with a tombstone gap, exempt from D-CTG/D-MIN/D-SEQ by the foundation — is unaffected..."
**Problem**: The concrete tables and per-clause verifications are object-level and earned; the surrounding paragraphs that narrate *why each example exists* and *what it adds over the previous one* are meta-prose. They do not advance the verification — the reader must skip them to reach the next check. This is the anti-bloat "essay content in structural slots" pattern.
**Required**: Delete the "What this example adds" / "The example exercises … concretely" framing paragraphs. Keep the tables, the per-clause ✓ checks, and the closing one-line contrast where genuinely informative.

### Issue 2: Repeated deferral to the same downstream location ("(Scope)" / composing INSERT)
**ASN-0082, Post-Insertion Shift**: the composing-INSERT deferral recurs in the Scope paragraph, in I3-C's prose, in "Arrangement invariants not preserved" ("which the composing INSERT operation fills and re-validates (Scope)"), and in "Gap region" ("where newly inserted content will be placed by the composing INSERT operation (Scope)").
**Problem**: Multiple paragraphs in different sections defer to the same downstream location — exactly the flagged pattern "multiple paragraphs … defer to the same downstream location." The deferral is established once in Scope; the later repetitions are noise.
**Required**: State the composing-INSERT boundary once (Scope) and remove the parenthetical "(Scope)" re-deferrals from I3-C, "Arrangement invariants not preserved," and "Gap region."

### Issue 3: wp-remainder paragraphs explaining what is *not* worked
**ASN-0082, both wp analyses**: "The remaining post-state lemmas — I3-S2 (functionality), I3-VD … admit wp derivations of the same form as I3-VP … we do not work them in detail because the obligations they surface are subsumed by those already exposed for I3-VP." (mirrored in the contraction wp: "are established by the preservation lemmas above, exactly as the insertion-half remainder is subsumed by I3-VP.")
**Problem**: These paragraphs are meta-prose about why further wp work is omitted. The substantive content (each remaining lemma's actual discharge) is already given in the preservation lemmas themselves; restating "we don't work these because they're subsumed" advances no reasoning.
**Required**: Drop the "admit wp derivations of the same form … we do not work them in detail" prose. If a remaining lemma's discharge is non-obvious, work it in its own lemma; otherwise the lemma proofs already stand.

### Issue 4: Defensive precondition-classification prose in I3-S
**ASN-0082, Span Width Preservation**: "The precondition is therefore definitional — it selects spans whose displacement arithmetic is compatible with ordinal shift. The logical content of I3-S rests on level-uniformity and ordinal-levelness alone; region membership (s ≥ p, subspace(s) = S) is the *scoping context* under which I3-S connects to the point-level shift I3, not a hypothesis the proof consumes. We state it as the general ordinal-level span fact and invoke it within the shifted region where I3 applies."
**Problem**: This is reviser-style rationale explaining which preconditions are "real" versus "scoping context" — a defensive justification of the lemma's statement rather than a step in its proof. It explains why the precondition is shaped as it is, not what the lemma establishes.
**Required**: State I3-S's preconditions (level-uniform, actionPoint(ℓ)=m) directly and proceed to the derivation. The scoping connection to I3 is already implicit in "invoke it within the shifted region"; the meta-discussion can be cut to a clause.

### Issue 5: D-I frame note enumerates downstream consumers and re-argues strength
**ASN-0082, D-I (ContentStoreFrame)**: "This is strictly stronger than S0 (ContentImmutability, ASN-0036), which permits `dom(Σ'.C) ⊃ dom(Σ.C)`. The exact equality matches the strength of D-CD and D-CS, and ensures that invariants over dom(Σ.C) — in particular S7a, S7b — are trivially preserved."
**Problem**: The frame's content is `Σ'.C = Σ.C`. The trailing sentences justify the choice of equality and enumerate downstream consumers (S7a, S7b) — the flagged pattern "a definition's introduction enumerates downstream consumers" plus rationale-for-strength prose. S7-post already cites D-I where it needs it.
**Required**: Keep the frame statement and the one operational clause ("contraction allocates/deallocates no I-addresses"). Remove the "strictly stronger than S0 / matches D-CD and D-CS / in particular S7a, S7b" commentary; let S7-post cite D-I at its use site.

### Issue 6: Duplicated statement of assignment-region disjointness
**ASN-0082, I3-S2 wp remainder**: "for I3-S2 this is exactly the pairwise disjointness already enumerated and attributed (TS2 injectivity, TS4 strict increase, subspace preservation at m ≥ 2, I3-V's exclusion clause) in the Consistency paragraph."
**Problem**: The pairwise disjointness of assignment regions is fully enumerated once in the Consistency paragraph and once in I3-S2's proof, then re-summarized a third time in the wp section. Two paragraphs say the same thing in different words.
**Required**: Prove I3-S2 by a single citation of the Consistency paragraph's disjointness result; drop the re-enumeration in the wp remainder.

## OUT_OF_SCOPE

### Topic 1: Depth > 1 (ordinal depth ≥ 2) contraction
**Why out of scope**: The contraction is explicitly scoped to #p = 2 by the depth axiom, and the round-trip generalization is correctly recorded as an Open Question. The TA4 zero-prefix incompatibility with S8a at intermediate components is a genuine future-ASN problem, not a defect here.

### Topic 2: External-reference update after a shift
**Why out of scope**: How external state tracking a V-position learns of its repositioning is correctly listed as an Open Question; it belongs to a future notification/reference ASN, not to the arrangement-layer characterization specified here.

VERDICT: REVISE
