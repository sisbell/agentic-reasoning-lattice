# Review of ASN-0108

## REVISE

### Issue 1: Direction of the "stronger than" relation between frozen-prefix and membership-identity is reversed

**ASN-0108, W2 (CursorByIdentity), offset-cursor wp analysis**: "The frozen-prefix condition is in turn strictly stronger than the membership-identity condition 'ranks 1..j of Σ' are exactly the j links already delivered': orphan one delivered link a_k (k ≤ j, key <_K κ(c)) and create one fresh matching link a' with κ(a') <_K κ(c); the net count at or below the cut stays j, so the offset window is correct — R holds — yet membership has changed (a_k gone, a' present). So three conditions nest strictly — membership-identity ⊃ frozen-prefix j' = j ⊃ the genuine weakest —"

**Problem**: The prose sentence and its own supporting example contradict each other.

- The example constructs a state where frozen-prefix holds (`j' = j`) but membership-identity fails (`a_k` gone, `a'` present). That is a state in `frozen-prefix \ membership-identity`, which proves frozen-prefix has models membership-identity excludes — i.e. membership-identity is the **smaller/stronger** condition, not frozen-prefix.
- Independently: if membership-identity holds (ranks `1..j` of `Σ'` are exactly the `j` delivered links), then the cursor `c` (the `≺`-max of the delivered links) sits at rank `j`, so `j' = |{a : κ(a) ≤_K κ(c)}| = j` — frozen-prefix follows. Thus membership-identity ⟹ frozen-prefix, confirming membership-identity is strictly stronger.
- The subsequent nesting "membership-identity ⊃ frozen-prefix ⊃ the genuine weakest" (read as implication) is therefore **correct**, but it directly contradicts the introductory sentence "frozen-prefix ... strictly stronger than the membership-identity condition." Under either reading of ⊃ (implication or superset-of-models) the example refutes the introductory sentence.

**Required**: Reverse the directionality in the prose: "The **membership-identity** condition is in turn strictly stronger than the **frozen-prefix** condition," so the sentence agrees with both the worked example (which exhibits a frozen-prefix model violating membership-identity) and the nesting line that follows. This is a load-bearing step in the wp analysis distinguishing the three precondition strengths, so the inverted claim cannot stand.

## OUT_OF_SCOPE

(none — the deferred multi-document ordering, satisfaction-predicate, and progress-sizing concerns are correctly relegated to Open Questions rather than asserted as claims here.)

VERDICT: REVISE
