# Review of ASN-0101

## REVISE

### Issue 1: D8's three-group partition omits arrangement invariants for unmodified documents
**ASN-0101, D8**: "The per-state invariants fall into three groups: Group (i), the arrangement invariants on the modified document `d` ... Groups (ii)–(iii), the allocation, store, transition, and remaining per-state invariants, all preserved because they predicate only over components D0's frame leaves pointwise fixed."

**Problem**: The foundation arrangement invariants (S8a, S2, S8-fin, S8-depth, S3★, D-CTG★, D-MIN★, D-SEQ★, S8★, S3★-aux, CL-OWN, CL-UNIQ) are universally quantified over every `d ∈ dom(M)`. Group (i) discharges them *only for the modified document `d`*. They are not in Group (ii) (allocation/store) nor in Group (iii)'s enumerated list (M1, C0, P0, P1, P2, P3, P6, P7, P8, L12a, L12b). Group (iii)'s blanket argument explicitly covers only predicates over "the frame-fixed components `C`, `L`, `E`, `R`, `dom(M)`" — and `M(d')` for `d' ≠ d` is none of these (it is fixed by D5, but D5 is not invoked in D8). So the arrangement invariants over unmodified documents `d' ≠ d` are addressed by no group. Standard 4 (every invariant conjunct addressed) is violated for the `d' ≠ d` conjuncts.

**Required**: Add one clause to the partition stating that the arrangement invariants over every `d' ≠ d` are preserved by D5 (`M'(d') = M(d')`) inheritance, alongside Group (i)'s argument for the modified `d`.

### Issue 2: Meta-prose justifying inclusion in the "What is preserved" preamble
**ASN-0101, "What is preserved"**: "Each appears as a frame condition in D0; each deserves an explicit statement because each was load-bearing for Nelson's design intent."

**Problem**: "each deserves an explicit statement because..." is rationale for *why the following claims are stated*, not content that advances the argument. This is the meta-prose pattern the anti-bloat classifier targets — the claims D2–D7 stand on their own; the preamble explains the editorial decision to include them.

**Required**: Delete the inclusion-justifying clause; if a transition is wanted, a single sentence naming the frame conditions about to be unpacked suffices.

### Issue 3: "A note on recoverability" is a section heading wrapping a deferral
**ASN-0101, "A note on recoverability and historical reconstruction"**: "Reconstruction of a prior arrangement is a versioning concern, not a property of DEL; the mechanism is out of scope here. Open Question 1 carries the rest."

**Problem**: The section's only substantive content is the (already-implied) statement that DEL is information-destroying w.r.t. `M(d)`; the remainder defers to Open Question 1 and to out-of-scope versioning. A standalone section whose payload is a forward-pointer to an open question is the defer-to-downstream accretion pattern.

**Required**: Fold the one substantive sentence (DEL is information-destroying with respect to `d`'s current arrangement) into D8 or the Open Questions preamble and drop the section.

## OUT_OF_SCOPE

### Topic 1: Versioning / historical backtrack for arrangement reconstruction
**Why out of scope**: Recovering a pre-DELETE arrangement requires a versioning mechanism outside D0's frame; correctly routed to Open Questions and not an error in this ASN.

VERDICT: REVISE
