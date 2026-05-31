# Review of ASN-0084

## REVISE

### Issue 1: Worked examples assert "Canonical partition" using machinery the ASN explicitly defers
**ASN-0084, all six "Worked Example" sections / R-BLK / Open Questions**: Each example ends "**Canonical partition:** {...}". Yet R-BLK's own statement says "yielding a run partition B′ ... **maximality not claimed**," and within several examples the run-partition paragraph states "B′ is a run partition of M'(d) — disjoint and covering; **maximality is not claimed**" — immediately followed by a "Canonical partition: {...}" conclusion.

**Problem**: R-BLK produces a non-maximal partition B′. To conclude that the post-merge-check partition equals the **S8-unique maximal (canonical)** partition, one needs the lemma "a covering run partition with no V-adjacent *and* I-adjacent pair admits no forward/backward run extension, hence is the maximal partition." That lemma is never stated or proven. Worse, the ASN's own Open Questions section asks "does iterated merging of V-adjacent, I-adjacent runs always terminate at [the canonical partition], and is the result confluent" — i.e., the ASN admits this connection is unresolved, while the examples assert the resolved result. The examples verify a guarantee (canonicity) that the ASN's machinery does not establish.

**Required**: Either (a) add and prove the bridging lemma — no mergeable adjacent pair ⟹ each run admits no forward/backward extension ⟹ (by S8 uniqueness) the partition is canonical — and remove the matter from Open Questions; or (b) weaken every example's final line from "Canonical partition" to "B′ after exhausting mergeable pairs" without claiming maximality. As written, the examples and the R-BLK contract / Open Questions contradict each other.

### Issue 2: Properties table lists region non-emptiness as part of the precondition R-PRE, but the body derives it
**ASN-0084, "Properties Introduced" table, R-PRE row**: "Precondition: M(d) exists, V_S(d) non-empty, cuts satisfy CS1–CS4, affected range covered, **every region non-empty (w_α, w_β ≥ 1 in both forms; w_μ ≥ 1 when n = 4)**".

**Problem**: The actual R-PRE definition has only clauses (i)–(iv); region non-emptiness is **not** a precondition clause. The body establishes w_α, w_β, w_μ ≥ 1 as the derived "Width positivity" *consequence* of R-PRE(iii)+(iv)+CS2. The table presents a derived guarantee as an assumed input, which obscures whether REARRANGE_K requires the caller to ensure non-empty regions or guarantees it. This is exactly the kind of conflation the rigor standard warns against (a derived guarantee stated as if primitive).

**Required**: Move the "every region non-empty" parenthetical out of the R-PRE precondition cell and either drop it or label it as a derived consequence (Width positivity), consistent with the body.

## OUT_OF_SCOPE

### Topic 1: Operational recovery of the canonical partition from B′ (termination/confluence of iterated merge)
**Why out of scope**: The general process by which iterated merging reduces B′ to the S8-unique maximal partition — and its confluence — is genuinely new territory, correctly parked in Open Questions. It is not an error in this ASN provided Issue 1 is fixed (i.e., the examples stop asserting the canonical result they cannot yet justify).

### Topic 2: k-cut rearrangements for k > 4 and composition of rearrangements
**Why out of scope**: Generalization beyond the 3/4-cut primitives and the algebra of composing multiple REARRANGE operations are future work, properly listed under Open Questions; the present ASN's depth-2, single-operation scope is internally complete.

VERDICT: REVISE
