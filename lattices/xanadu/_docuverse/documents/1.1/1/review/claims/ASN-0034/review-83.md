# Cone Review — ASN-0034/TumblerAdd (cycle 1)

*2026-04-16 12:14*

### Dangling reference to undefined property "TA0"
**Foundation**: PositiveTumbler section
**ASN**: PositiveTumbler section, final paragraph: "The condition `Pos(w)` in TA0 excludes all all-zero displacements regardless of length."
**Issue**: "TA0" is referenced as if it were an established property of this ASN (or a known external citation), but TA0 is neither defined within this ASN nor listed as a forward reference like T3 is in T1. The Depends list of every property in the ASN omits TA0. A reader cannot determine what TA0 is, where it lives, or what its `Pos(w)` precondition does. If TA0 is a sibling property (e.g., the addition-axiom name for TumblerAdd, or a successor to T0 in a planned numbering), the cross-section linkage is broken.
**What needs resolving**: Either introduce TA0 explicitly (with the same forward-reference annotation pattern used for T3 in T1), replace the reference with the correct property name (e.g., TumblerAdd uses Pos(w) as a precondition), or remove the sentence if the reference is vestigial from an earlier draft.

### Trailing sentence with no content before "Canonical form"
**Foundation**: T1 (LexicographicOrder) section
**ASN**: Final line of the T1 section before the `## Canonical form` heading: "Nelson requires that comparison be self-contained — no index consultation needed:"
**Issue**: The sentence ends with a colon promising a continuation that never appears — the next token is the `## Canonical form` heading. Whatever proposition T1 was about to introduce (motivating T3, presumably) has been dropped. A reader cannot tell whether this is editorial debris or a real claim that should have been stated and used.
**What needs resolving**: Either complete the sentence with the intended assertion (and connect it to T3's role as the canonical-form guarantee), or delete the dangling fragment.

### Informal terms "T1-positive" and "PositiveTumbler-positive" used without definition
**Foundation**: PositiveTumbler section
**ASN**: "Every all-zero tumbler of length ≥ 2 is T1-positive but not PositiveTumbler-positive."
**Issue**: Neither "T1-positive" nor "PositiveTumbler-positive" is defined anywhere. The reader must infer that "T1-positive" means "T1-greater than [0]" (or some similar baseline) and that "PositiveTumbler-positive" is a paraphrase of `Pos(t)`. The contrast is the key claim of the paragraph — that T1 ordering and the `Pos` predicate diverge — but the terms carrying the contrast are undefined. There is also no chosen baseline: T1-greater than `[0]`? than `[0,0]`? The set of all-zero tumblers has no minimum under T1 unless one is fixed.
**What needs resolving**: Replace the informal terms with the precise statement the paragraph is making, e.g., for the all-zero tumbler `[0,0]`: `[0] < [0,0]` under T1 yet `¬Pos([0,0])`, so the divergence between T1 ordering and `Pos` is exhibited concretely.
