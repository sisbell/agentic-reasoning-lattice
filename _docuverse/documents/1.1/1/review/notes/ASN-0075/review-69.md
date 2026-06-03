# Review of ASN-0075

## REVISE

### Issue 1: No-write property duplicated across two sections with a self-referential forward pointer
**ASN-0075, "The SHOWDELETIONS Operation" (wp discussion) and "Observational Frame" (D-OBS)**:

In the SHOWDELETIONS section: *"The operation's definition is a pair of set-builder comprehensions over Σ: it allocates nothing, rewrites no component, and invokes no transition relation, so it writes no state component. (This no-write property is recorded formally as D-OBS in the Observational Frame section below; here we rely only on the evident structure of the definition.)"*

In D-OBS: *"It allocates nothing, rewrites nothing, and invokes no transition relation — observationality is immediate from the definition, which is a pair of set-builder comprehensions over Σ."*

**Problem**: The same reasoning ("allocates nothing / invokes no transition relation / pair of set-builder comprehensions over Σ") is stated in both sections, and the first occurrence carries an explicit forward pointer justifying the duplication ("recorded formally as D-OBS ... below; here we rely only on..."). This matches two of the anti-bloat patterns this note is classified to surface: two paragraphs saying the same thing in different words, and a forward pointer added to manage that duplication rather than removing it. The no-write fact is what the wp pass-through rule (`wp(SHOWDELETIONS, P) = (precondition) ∧ P(Σ)`) depends on, so it is load-bearing once — not twice.

**Required**: State the no-write property a single time as D-OBS, and have the wp discussion cite D-OBS rather than re-deriving it. Delete the parenthetical forward-reference and the duplicated "set-builder comprehensions / allocates nothing" sentence from the SHOWDELETIONS section.

## OUT_OF_SCOPE

None. The Open Questions are framed as questions, not claims, and the note defines no claims for the excluded operation/link/version/replication topics.

VERDICT: REVISE
