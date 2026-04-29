# Proof Verification: D-MIN

RESULT: FOUND

**Problem**: The property section contains no proof of D-MIN. The paragraph beginning "We now derive the general form" is circular — it invokes D-MIN itself ("By D-MIN, min(V_S(d)) = [S, 1, …, 1], so those shared components have value 1") to conclude that shared components are 1 and the minimum last component is 1. That paragraph derives *consequences* of D-MIN (the [S, 1, …, 1, k] structure), not D-MIN itself.

The listed dependencies cannot establish D-MIN:
- D-CTG + S8-fin establish that V_S(d) is a finite contiguous block.
- D-CTG-depth establishes that at depth m ≥ 3, all positions share components 2 through m − 1.
- But none of these constrain *where* the block starts. V_S(d) = {[S, 5, 3, k] : 1 ≤ k ≤ n} satisfies D-CTG, D-CTG-depth, S8-depth, and S8-fin equally well. Nothing forces the shared prefix to be [S, 1, …, 1] or the minimum last component to be 1.

Additionally, no `*Formal Contract:*` section is provided (checklist item 6).

**Required**:
1. **Clarify the status of D-MIN.** If it is an axiom (a design constraint that V-position numbering starts at 1, paralleling Nelson's "addresses 1 through 100" and the tumbler convention that ordinals begin at 1 as noted at the end of the D-CTG-depth section), declare it as such with an axiom formal contract. If it is a theorem, provide a non-circular proof — this would require dependencies not currently listed (e.g., properties of how the initial document state assigns V-positions, and how each operation preserves the minimum).
2. **Add a formal contract.** If axiom: `*Formal Contract:* — *Axiom:* min(V_S(d)) = [S, 1, …, 1] for every document d and subspace S with V_S(d) non-empty.` If theorem: preconditions (V_S(d) non-empty, S8-depth, etc.) and postcondition (`min(V_S(d)) = [S, 1, …, 1]`).
3. **Separate the corollary.** The "general form" derivation (every position is [S, 1, …, 1, k] for 1 ≤ k ≤ n) is a valid consequence of D-MIN + D-CTG-depth + D-CTG + S8-fin, but it should be clearly labeled as a corollary that follows *from* D-MIN, not as the proof *of* D-MIN.
