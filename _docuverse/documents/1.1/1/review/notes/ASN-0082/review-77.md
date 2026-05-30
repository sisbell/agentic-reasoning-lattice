# Review of ASN-0082

## REVISE

### Issue 1: D-SEP(a) cites the wrong clause of OrdinalExceedsDisplacement

**ASN-0082, D-SEP, *Proof of (a)***: "By OrdinalExceedsDisplacement (i), `ord(r) ⊖ w_ord = ord(p)`. ✓"

**Problem**: OrdinalExceedsDisplacement clause (i) states only the inequalities "`ord(r) ≥ w_ord` and `ord(r) > w_ord`" — it does **not** state the equation `ord(r) ⊖ w_ord = ord(p)`. The equation is the content of clause (iii) ("`ord(v) ⊖ w_ord` … equal to `ord(p)` when `v = r`"), instantiated at `v = r`. As written, the proof attributes to (i) a postcondition that (i) does not carry; the equation only appears inside (i)'s proof body and is properly exported by (iii). This is exactly the kind of reach-into-proof-body citation a precise reader has to stop and reconcile.

**Required**: Cite OrdinalExceedsDisplacement (iii) at `v = r` for the equation in D-SEP(a).

### Issue 2: Defensive "independently of the order relation" prose in OrdinalExceedsDisplacement (ii)

**ASN-0082, OrdinalExceedsDisplacement, clause (ii) derivation**: "the hypothesis `#v = 2` together with `#r = #w = #p = 2` … gives `#v = #r` **independently of the order relation, which is what licenses OrdinalOrderEquivalence (precondition #v₁ = #v₂)**; from `v ≥ r` it then yields `ord(v) ≥ ord(r)`"

**Problem**: The bolded clause is reviser-drift meta-prose — it preempts a worry (that the length equality might depend on the order relation) that no reader needs raised. The load-bearing facts are just `#v = 2 = #r`; the parenthetical re-statement of OrdinalOrderEquivalence's precondition and the "independently of the order relation" hedge do not advance the argument. This pattern (defensive justification of why a precondition is satisfiable) is the accretion the anti-bloat classifier targets.

**Required**: State the length equality and the OrdinalOrderEquivalence application directly; drop the "independently of the order relation, which is what licenses" hedge.

### Issue 3: Scoping-axiom prose explains *why the axiom is needed* rather than what it constrains

**ASN-0082, *Scoping axioms***: "*Subspace axiom: S = 1.* The contraction operation is defined only on the text subspace; **the foundation's D-CTG, D-MIN, D-SEQ supply the contiguity preconditions only for V_1(d)**."

**Problem**: The clause after the semicolon is rationale for *why* the restriction is imposed (which foundation invariants happen to be text-scoped), not a statement of *what* the axiom constrains. This is the "new prose around an axiom explains why the axiom is needed" pattern. The axiom's content is `S = 1`; the justification belongs in the ASN's motivation, not bolted onto the axiom statement, where it recurs as noise each time the axiom is read.

**Required**: Reduce the subspace axiom to its content (`S = 1`, contraction operates on the text subspace). If the dependence on text-scoped foundation invariants must be recorded, state it once in the scope/motivation prose, not on the axiom.

## OUT_OF_SCOPE

### Topic 1: Contraction at ordinal depth greater than 1

**Why out of scope**: The contraction's depth axiom (`#p = 2`) is a deliberate restriction, and the obstruction (TA4's zero-prefix precondition colliding with S8a positivity at intermediate components) is already recorded in Open Questions. Generalizing D-SEP/D-DP/D-S to deeper ordinals is genuinely new territory, not a defect in this ASN's depth-2 treatment. The asymmetry with the insertion side (I3/I3-S handle general `m ≥ 2`) is consistent with this scoping.

VERDICT: REVISE
