# Review of ASN-0058

## REVISE

### Issue 1: C1a's generalization carryover is overstated and under-justified

**ASN-0058, C1a (RestrictionDecomposition), "Extension of M11/M12"**: "The argument structure carries over to f with a single textual substitution: wherever M12 invokes 'S8-depth (ASN-0036) applied to that subspace' to establish that two V-positions share depth m, that appeal is discharged here by C1a's common-depth assumption on dom(f) ... With that substitution, the rest of the argument is unchanged."

**Problem**: The "single textual substitution / rest unchanged" claim misrepresents the actual dependency surface of M11/M12. M12a and M12b — and the M-int lemma they invoke — do not rely only on S8-depth:

- M12a's "Equal starts (Case v₁ < v₂)" applies **M-int**, whose own proof uses **S8a** (`#x ≥ 2`) and **S8-depth** (depth equality via subspace).
- M12b invokes **S8a** ("S8a gives `#v ≥ 2` and `#v' ≥ 2`, discharging the depth preconditions of **OrdShiftHom**") and **S8-depth** separately.

These are all `M(d_s)`-specific properties, not consequences of conditions (i)–(iii). They hold in the *application* only because `dom(f) ⊆ dom(M(d_s))` makes the positions genuine V-positions of `d_s`. But C1a states the claim for "any finite partial function f : T ⇀ T satisfying (i) functionality, (ii) finite domain, (iii) common depth m ≥ 2" — and for an arbitrary such f, S8a (zero-free, positive components) need not hold, so the cited proofs do not run as written. The conclusion is in fact correct (every one of these appeals is used only to extract depth `m ≥ 2`, subsumed by (iii)), but the justification names exactly one regrounding when at least four appeals (M-int, S8a, S8-depth, OrdShiftHom) require it. The paragraph additionally restates the generalization point three times (the M7f sentence, "Both proofs require only the three conditions verified above," and the substitution sentence).

**Required**: Either (a) scope the generalization to "any restriction `M(d_s)|X` of an arrangement," so `dom(f) ⊆ dom(M(d_s))` makes S8a/S8-depth/M-int directly applicable and no substitution is needed; or (b) enumerate each `M(d_s)`-specific appeal in M12a/M12b/M-int and reground it explicitly in condition (iii). Drop "a single textual substitution" and "the rest of the argument is unchanged," and collapse the repeated restatements into one.

### Issue 2: M16a carries a use-site inventory that does not advance the proof

**ASN-0058, M16a (OriginInvarianceUnderShift), proof**: "T10a.4 ... applied to ASN-0036's framework-level T10a-conformance assumption — the standing precondition (named by S4 and listed in S7's preconditions) that the content store C is populated by a system conforming to T10a (ASN-0034) — gives T4-validity of every a ∈ dom(C) ..."

**Problem**: The parenthetical "(named by S4 and listed in S7's preconditions)" is a use-site inventory — it catalogs where the assumption is mentioned elsewhere rather than advancing the derivation. The proof needs only that the assumption holds; cataloging its appearance points is the kind of accreted meta-prose the precise reader must skip past. This matches the flagged forward-reference/inventory pattern.

**Required**: State the assumption and cite T10a.4; drop the parenthetical inventory of where the assumption is named.

## OUT_OF_SCOPE

### Topic 1: I-space discontinuity structure at canonical boundaries
The first Open Question (whether a non-mergeable boundary must be a forward gap or an arbitrary jump) characterizes the I-space gap structure. This is new territory, properly deferred — not an error here.

VERDICT: REVISE
