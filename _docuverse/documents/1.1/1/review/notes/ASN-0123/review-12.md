# Review of ASN-0123

I checked the operation contract, the apparatus (PS, trunc, Z-mono, SA, nextv, VN-B1), and the proofs of V0–V13 and V-WF against the foundations. The ASN is unusually thorough: VN-B1's induction is complete across all four K.δ cases; the severance theorem (V9a) closes both comparability branches; G2's necessity argument correctly converts subtree coverage to address identity via SA + S3★; V-WF discharges both ValidComposite★ clauses with the couplings pinned from both sides; and the boundary-dependence of V9w on P4★ is handled with the care it needs. I found one rigor gap.

## REVISE

### Issue 1: B2's stated precondition is not discharged by VN-B1

**ASN-0123, "State and Local Apparatus," nextv (VersionFrontier)**: "The realized children `E ∩ S(d, 1)` form a contiguous prefix `{c₁, …, c_m}` of the stream — this is VN-B1, stated and proved next — so by B2: `nextv(E, d) = c_{hwm(E, d, 1) + 1}` — the gap-free successor."

**Problem**: B2 (HighWaterMarkSufficiency, ASN-0040) carries the stated precondition "B satisfies B1 for all B6-valid (p, d)." The ASN proves VN-B1, which is the contiguity invariant for *version namespaces* `S(d, 1)` (T4-valid `d`, `zeros(d) = 2`) **only**. It establishes nothing about the other entity-level B6-valid namespaces that also populate `E` — the document-creation namespace `(account, 2)` and the account-creation namespace `(node, 2)`, both B6-valid and both emitting entities (`zeros = 2` and `zeros = 1` respectively) that land in `E`. Taken as a black box with its stated precondition, B2 cannot be cited here, because its global B1 hypothesis is not met. This is the ASN's own concern turned on itself: VN-B1 exists precisely because (in the ASN's words) "ASN-0040's B1 ... does not transfer to ASN-0047's K.δ vocabulary by citation, so we prove its analog" — but the proved analog is version-namespace-local, while the cited B2 wants the full invariant.

**Required**: Either —
(a) drop the B2 appeal and derive the result directly from facts already in hand: VN-B1 gives `E ∩ S(d,1) = {c₁,…,c_m}`; S0 (StreamOrdering) gives `c_m = max`; the stream recurrence gives `inc(c_m, 0) = c_{m+1} = c_{hwm+1}` (and the empty case `inc(d,1) = c₁ = c_{0+1}` directly). No global B1 is needed for this conclusion; or
(b) generalize VN-B1's induction to the entity-level namespaces present in `E`, thereby discharging B2's precondition as stated.

Route (a) is clean and removes the dependency entirely; the conclusion (nextv well-defined and equal to the gap-free frontier) is sound under either fix.

## OUT_OF_SCOPE

None. The ASN keeps to the fork — document creation, version comparison, editing, link creation, content delivery, and replication are touched only through frame conditions or foundation invariants. The cross-owner branch's reliance on document creation is handled by re-specifying and validating the single K.δ it actually consumes (`Document(v) ∧ v ∉ E ∧` O5 wrt π), not by importing the out-of-scope operation wholesale. The open questions correctly defer the genuinely new territory (VD soundness against non-version allocators, concurrent-fork serialization, derivation-direction recovery).

VERDICT: REVISE
