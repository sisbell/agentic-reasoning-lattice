# Review of ASN-0084

## REVISE

### Issue 1: Commutativity mislabeled as associativity
**ASN-0084, SwapPostcondition tiling verification**: "By associativity of ordinal addition, the last position is c₀ + (w_β + w_μ + w_α) = c₀ + (w_α + w_μ + w_β)."
**Problem**: The equality `w_β + w_μ + w_α = w_α + w_μ + w_β` is commutativity of natural-number addition, not associativity. TS3 (ShiftComposition) establishes associativity of shift composition `(c₀ + j) + k = c₀ + (j + k)`, which is correctly cited elsewhere in the ASN (notation section, R-SWP proof). But rearranging the order of summands within the parentheses requires commutativity — a property of ℕ that TS3 does not provide.
**Required**: Replace "By associativity of ordinal addition" with "By commutativity of natural-number addition" for this step. The associativity citations elsewhere in the ASN are correct and should remain unchanged.

### Issue 2: R-BLK Phase 1 description overstates what CS2 guarantees
**ASN-0084, R-BLK Phase 1**: "CS2's strict ordering (c₀ < c₁ < ... < c_{n−1}) guarantees that each later cut falls either at a block boundary already created by an earlier split, or in the right-hand piece of an earlier split — so the process is well-defined."
**Problem**: A later cut can also fall interior to an entirely unrelated block that no earlier cut touched. The 4-cut worked example demonstrates this: c₁ = [1,4] and c₂ = [1,5] each coincide with the starts of different original blocks (b₂ and b₃), not with boundaries or pieces created by splitting at c₀. The description as written implies every cut relates to a prior split, which is false when cuts span multiple original blocks. What CS2 actually guarantees is narrower: when two cuts fall in the *same* original block, the later one falls in the right-hand piece of the earlier split.
**Required**: Restate to something like: "Each cut position either coincides with a boundary in the current decomposition or falls interior to some block. When a later cut falls in a block already split by an earlier (strictly smaller) cut, it necessarily falls in the right-hand piece. The process is well-defined because B1–B3 are maintained after each split."

### Issue 3: No explicit bridge from postconditions to ArrangementRearrangement
**ASN-0084, gap between R-PPERM/R-SPERM and the invariant preservation argument in "State and Vocabulary"**
**Problem**: The invariant preservation argument is stated for arrangement rearrangements in general. The postconditions are defined later, and R-PPERM/R-SPERM construct the bijection π. But the ASN never explicitly concludes "the pivot/swap satisfies the ArrangementRearrangement definition." A downstream ASN citing "pivot preserves D-CTG" must assemble the connection across three sections: (1) the postcondition states `dom(M'(d)) = dom(M(d))`, (2) the frame condition states `C' = C`, (3) R-PPERM provides the bijection. The conclusion that these jointly satisfy the abstract definition is left implicit.
**Required**: After R-PPERM, add a statement such as: "The pivot postcondition preserves `dom(M(d))`, preserves C (R-FRAME-P(c)), and admits the bijection π satisfying `M'(d)(π(v)) = M(d)(v)` (R-PPERM); it therefore constitutes an arrangement rearrangement, and the invariant preservation established above applies." Add the analogous statement after R-SPERM.

## OUT_OF_SCOPE

### Topic 1: Generalization to k-cut rearrangements (k > 4)
**Why out of scope**: The ASN explicitly restricts to n ∈ {3, 4} and raises generalization as an open question. The two forms suffice for the transposition class they model.

### Topic 2: Composition of rearrangements
**Why out of scope**: Whether the composition of two rearrangements is expressible as a single rearrangement concerns the algebraic closure of the operation class — future ASN territory on editing sequences.

### Topic 3: Generalization beyond depth-2 V-positions
**Why out of scope**: The depth-2 restriction is explicit, and the reduction via D-CTG-depth (ASN-0036) is sound: contiguity at depth m ≥ 3 reduces to the last component, making depth-2 representative. Formal verification of this reduction is future work.

VERDICT: REVISE
