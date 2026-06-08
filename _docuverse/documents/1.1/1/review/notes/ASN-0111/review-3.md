# Review of ASN-0111

## REVISE

### Issue 1: Consequence claims silently assume Σ satisfies the foundation invariants, but no such precondition is stated

**ASN-0111, "Deriving the read" / "Invariants governing the returned structure"**: The definition is given "For a state `Σ` and address `a`," and the guarantees RL-WF, RL-ARITY, RL-GEN, RL-REP, and RL5 are then asserted unconditionally — e.g. RL-ARITY: "`|readlink(a, Σ)| ≥ 3 ∧ readlink(a, Σ).e₃ ≠ ∅` (from L3, ASN-0043)."

**Problem**: L3, L0, L1, L1b, L0b are invariants that hold only at *reachable* states of the substrate. They are theorems, not facts about every conceivable `Σ`. As written, `readlink` is defined over an arbitrary `Σ`, so for a state that does not satisfy the foundation invariants (e.g. a hand-constructed state with an arity-2 link or a non-T4-valid link key), RL-ARITY, RL-WF, and RL4's appeal to `home(a)` (which needs L0b T4-validity to be defined) all fail. Every "guarantee a reader may assume" is licensed only when `Σ` is in the reachable/invariant-satisfying class.

**Required**: State explicitly that `readlink` is specified over states `Σ` that satisfy the foundation/state-local invariants (or are `→*`-reachable from the initial state), and make this the standing precondition under which RL-WF, RL-ARITY, RL-GEN, RL-REP, RL4, and RL5 are claimed.

### Issue 2: "exactly two asymmetries" asserted without justification of exhaustiveness

**ASN-0111, "Type is interpreted by address, not by content"**: "The genuine asymmetries between the type slot and the connective slots are exactly two, and the read reflects both."

**Problem**: The categorical "exactly two" is a completeness claim — it asserts no third asymmetry exists — but the note neither enumerates the candidate space nor excludes other distinctions (e.g. L7's directional-significance asymmetry, or the type slot's role in inducing the `same_type` partition of the store, which is arguably distinct from "interpreted by coverage without dereference"). This is a claim presented as a fact.

**Required**: Either justify exhaustiveness (enumerate and exclude alternatives) or soften to a non-categorical form ("the two asymmetries relevant to the read are…"), so the wording is not an unsupported universal.

## OUT_OF_SCOPE

### Topic 1: Conclusions a reader may draw about a relationship's continued *validity*
**Why out of scope**: The first Open Question asks what a reader can conclude about continued validity from a read alone. Validity/supersession semantics are a separate concern (link-type interpretation, future ASN), not a defect in the read specification given here.

VERDICT: REVISE
