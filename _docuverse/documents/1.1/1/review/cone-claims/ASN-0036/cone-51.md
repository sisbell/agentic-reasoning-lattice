Reading the full cone — foundation statements from ASN-0034 plus the ASN-0036 content — left to right, checking every precondition chain, case split, and postcondition discharge.

**S0, AX-1, AX-2, S1, S2:** All are axioms or immediate corollaries. S1's single proof step (S0's first conjunct) is complete. S2 follows from the partial-function declaration. No issues.

**S3 (ReferentialIntegrity):** Induction on transitions. Base case vacuous via AX-1 (empty domain). Inductive step: the inherited/new-or-redirected split is exhaustive — every `v ∈ dom(Σ'.M(d))` either has its image unchanged from Σ (covered by J0 + S1) or is new/redirected (covered by AX-2). AX-2's domain guard on `Σ.M(d)(v)` is correctly present and its explanation is accurate. The closing remark that S3 does not require `dom(C) ⊆ ⋃ran(M(d))` is correctly framed. Proof is sound.

**S8a, S8-fin, S8-depth, subspace:** Design constraints and definitions. S8a's zero-count unfolding via NAT-card and NAT-zero is correct. S8-depth's acknowledged scope overrun (non-text subspaces ungrounded) is noted and bounded to non-consuming scope within this ASN.

**OrdShiftHom (OrdinalShiftPreservation):** The component expansion via TumblerAdd is correctly invoked: `actionPoint(δ(n,m)) = m = #v`, so `m ≤ #v` is trivially `m ≤ m`. Part (a): since `m ≥ 2`, position 1 falls in the copy-from-v region (`1 < m`), giving `r₁ = v₁`, hence `subspace(r) = subspace(v)`. Part (b): copy region gives `rᵢ = vᵢ ≥ 1` for `i < m` (S8a hypothesis); action point gives `rₘ = vₘ + n ≥ 1` (OrdinalShift's exported lower bound). Hence `zeros(r) = 0` and `#r = m ≥ 2`, establishing S8a on `r`. Depth preservation `#r = m` comes from TA0 (`#(a ⊕ w) = #w`, instantiated at `#δ(n,m) = m`), unconditionally — not from S8-depth. The proof correctly grounds this in OrdShiftHom's frame.

**S8 (CorrespondenceRunPartition):** The proof constructs the lockstep-successor partial function `succ`, establishes its injectivity and acyclicity, then reads off maximal chains.

- *Succ well-defined:* `shift(v,1)` is uniquely determined by OrdinalShift; `M(d)(v)` is unique by S2. ✓
- *Succ preserves subspace/depth:* OrdShiftHom (a) and the frame `#shift(v,1) = #v` (TA0, unconditional). The text correctly disclaims S8-depth here — S8-depth requires both `v` and `shift(v,1)` active, which isn't yet known at this point in the argument. ✓
- *Injectivity:* `succ(u) = succ(u')` → `shift(u,1) = shift(u',1)` → depth equality via shift's frame → TS2 gives `u = u'`. Preconditions for TS2 (`u,u' ∈ T`, `#u = #u'`, `n=1 ≥ 1`) all discharge. ✓
- *Acyclicity:* TS4 gives `shift(v,1) > v`; a cycle would yield `v < v` via transitivity, contradicting T1 irreflexivity. ✓
- *Finite graph + in/out-degree ≤ 1 + acyclic → disjoint simple paths:* standard combinatorial fact, correctly applied. ✓
- *Displacement identity induction:* base `i=0` via convention `shift(t,0):=t`; step for `i=0→1` uses convention directly; step for `i≥1→i+1` applies TS3 with `n₁=i≥1`, `n₂=1`. Preconditions for TS3 (original `v ∈ T`, `#v=m`, both amounts ≥ 1) are satisfied at each application. TS3 is correctly applied to the original `v`, not to `vⁱ`, which is the right instantiation. The same pattern correctly applies to the image side (`a ∈ T` by `M(d):T⇀T`). ✓
- *Conjunct (b) (`shift(a,k) ∈ dom(Σ.C)`):* follows from `shift(a,k) = M(d)(vᵏ) ∈ ran(M(d)) ⊆ dom(Σ.C)` (S3). ✓
- *Partition:* empty case explicit; coverage via orbit membership; disjointness from orbit uniqueness; finiteness from S8-fin. ✓
- *Convention axiom:* correctly labeled in the formal contract; its interaction with TS3's `n₁ ≥ 1` precondition is explicitly handled in the case split. ✓

The S8 formal contract's note distinguishing S8-depth's role (subspace-wide depth framing) from OrdShiftHom's frame (unconditional per-step depth equality) is precise and the proof body matches.

No correctness issues found across the cone.

VERDICT: CONVERGED