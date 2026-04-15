# Cone Review — ASN-0036/S5 (cycle 1)

*2026-04-13 14:58*

I'll read the full ASN content carefully, focusing on cross-property interactions.

### S3 induction base case relies on an unstated initial-state axiom
**Foundation**: (internal — foundation ASN)
**ASN**: S3 proof, base case: "In the initial state Σ₀, no operations have been performed, so dom(Σ₀.M(d)) = ∅ for every document d."
**Issue**: The proof's inductive base case asserts `dom(Σ₀.M(d)) = ∅` for all `d` — an assumption about the initial state that is not captured anywhere in S3's formal contract. The contract lists preconditions as S1 and per-operation obligations, but the induction requires a third condition: S3 holds in the initial state. The empty-arrangement claim is sufficient for the base case but is itself an axiom (or a consequence of some unstated initial-state specification). Without it, the induction has no ground to stand on. More generally, the proof would work for any initial state satisfying S3 — the contract should require this, rather than the proof silently assuming the narrower condition of emptiness.
**What needs resolving**: S3's formal contract must include an initial-state precondition — either "dom(Σ₀.M(d)) = ∅ for every document d" if that is the intended axiom, or the weaker "S3 holds in Σ₀" if arbitrary valid initial states are permitted.

---

### S5 consistency claim covers S0–S3 but narrative binds S5 to S4
**Foundation**: (internal — foundation ASN)
**ASN**: S5 formal statement: `(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ ...))` vs. S5 narrative: "The combination of S4 and S5 gives the system its distinctive character. S4 says identity is structural — determined by I-address, not by value."
**Issue**: S5's formal claim and proof check consistency with S0–S3 only. The narrative presents S4 and S5 as architecturally coupled ("the combination … gives the system its distinctive character"), and S6 is referenced parenthetically ("possibly zero for orphaned content (S6)"). If S4 imposes constraints on states — for instance, distinguishing content by I-address rather than by value — then the constructions must be shown to satisfy S4 for the consistency claim to cover the ASN's actual property set. The constructions likely satisfy S4 trivially (single I-address), but "likely trivial" is not "established." The formal claim is weaker than the narrative suggests: it shows S0–S3 don't cap sharing, but doesn't show that S0–S5 together don't cap sharing.
**What needs resolving**: Either extend S5's formal statement and proof to check all properties of the ASN (including S4 and any others), or explicitly scope the narrative to match the formal claim — make clear that S5 establishes consistency with a strict subset of the ASN's properties, and state why the remaining properties are excluded.

---

### S5 quantifies over states but S0/S1 are transition properties
**Foundation**: (internal — foundation ASN)
**ASN**: S5 formal statement: `(E Σ :: Σ satisfies S0–S3 ∧ ...)` and S5 proof: "S0 and S1 are vacuous — single state, no transition to check."
**Issue**: S0 and S1 are universally quantified over state transitions (`Σ → Σ'`). S2 and S3 are predicates on individual states. S5's existential quantifier `∃Σ` ranges over states, then claims "Σ satisfies S0–S3" — but satisfaction of S0/S1 is undefined for an isolated state without transitions. The proof resolves this by noting vacuity (no transitions means S0/S1 hold trivially), which is logically sound but proves something weaker than the design intent. Nelson's claim that transclusion is "recursive and unlimited" is about sharing *growing through operations* in a system where S0/S1 are non-vacuously enforced. The current proof shows only that high-sharing states *exist*, not that they are *reachable* through a sequence of transitions that genuinely respect content immutability and store monotonicity.
**What needs resolving**: The formal statement needs to quantify over systems (behaviors/execution traces), not isolated states, so that S0/S1 are non-vacuously satisfied. Alternatively, construct a multi-state model — an initial state, a sequence of content-creation and arrangement operations, and a resulting state with multiplicity > N — demonstrating that unbounded sharing is achievable through transitions that substantively satisfy S0 and S1.
