# Review of ASN-0134

This is a strong, unusually careful note. The conflict theory of §4 (H0–H3) is sound, the origin-based H1 argument genuinely improves on the cited ASN-0093 lemmas for nesting homes, the §7/§8 worked traces check out address-by-address, and the operation-level order-dependence analysis (the two families, and the sharp observation that instance (ii) survives emit-before-retract while the target-residence race does not) is correct and honestly hedged. The MIC minimality argument is sound. My findings are precision/consistency gaps, not soundness holes in the central thesis.

## REVISE

### Issue 1: A6's "per-state canonicity package" omits the contiguity invariant that §2 and §4 depend on

**ASN-0134, §2 (A6)**: "the *per-state canonicity package* of the `→_sh` stack — *every* invariant of the stack that is a predicate of a single state... This package is the conjunction of [SD, C1/C1b/C1c, C2, L0, L1/L1a/L1b/L1c, L3, M0, M2, C-fin/L-fin, P6, registry-fixity]."

**Problem**: The enumeration, billed as "*every* invariant of the stack that is a predicate of a single state," omits `ChainMembershipForOrigin` (ASN-0093) and its link analog `L-ContiguousPrefix` (ASN-0086) — the gapless-contiguous-prefix property, which is a per-state invariant of every reachable state. C1c/L1c are *conformance* (a chain exists), not *contiguity* (the homed set is a gapless initial segment); these are different invariants. The omission matters because:

1. §2's own prose makes gaplessness part of canonicity: "A reader who lands mid-batch sees a state that is *completely* canonical: ... every chain gapless and conformant." A6's formal package does not contain the invariant that discharges "every chain gapless."
2. §4 leans on it explicitly: "By `ChainMembershipForOrigin` (ASN-0093), `P_S(d, Σ)` is a *contiguous initial segment* of the chain `A_S(d)`."
3. §5's W3 classifies that same contiguity as **serialization-borne**, "not the data model."

These are reconcilable but the note runs two distinct notions together. "Canonical on `𝔼`" (A6's actual subject) holds at every state of the *totally ordered* `𝔼`, where contiguity **does** hold (the total order serializes every same-home pair), so A6 should include it and §2's "gapless" is correct. "Model-intrinsic = robust to arbitrary non-serialized interleaving" (§5's notion) correctly **excludes** contiguity (W3), because a non-serializing implementation breaks it. A6's enumeration silently uses the §5-flavored list (no contiguity) while its "every single-state invariant" billing and §2's prose assert the broader, on-`𝔼` notion. A reader cannot tell whether A6's "fully per-state-canonical" certifies gaplessness or not.

**Required**: State which notion A6 means. If A6 is "holds at every state of `𝔼`" (as its use in the mid-batch argument and §2's prose require), add `ChainMembershipForOrigin`/`L-ContiguousPrefix` to the package — they ride the same B2/RP-a transfer as the others — and note that they hold on `𝔼` precisely because `𝔼` is totally ordered, while §5's W3 ("serialization-borne") is the *separate* claim that an implementation needs per-home serialization to *produce* such executions. Do not let the "every single-state invariant" billing coexist with an enumeration that drops an invariant the note itself invokes.

### Issue 2: A1 and §8 give inconsistent accounts of multi-type behavioral reads

**ASN-0134, §1 (A1)**: "a *read-only query* — an `Observe_K`, or any of ASN-0128's behavioral reads `members`, `is_K`, `targets_of`, ..., `target_of`, `targets_keyed`, `age`, `stale`, `is_filtered` ... each a total function of the single state it reads."

**ASN-0134, §8**: "the substrate exposes no whole-state read, only the per-type `Observe_K`... a predicate over several types or homes — the realistic quiescence condition, and ASN-0128's `targets_keyed` already *joins across every Binary type* — is several [reads]."

**Problem**: A1 places `targets_keyed` (and the default-view reads `members(K', default)`/`targets_of(x, default)`, which §"ReadFilter (BH1)" defines as joins across every BH1 type) among reads that are "a total function of the **single** state it reads." §8's entire clause-7 argument depends on the opposite: a cross-type read is realized over the per-type surface as **several** `Observe_K` calls that may straddle multiple indices and so is subject to inter-index drift. Taken at face value for A1's purpose — characterizing a read's relationship to the indices of `𝔼` — A1 grants `targets_keyed` the single-index atomicity that §8 says must be *constructed* via clause 7. ASN-0128 defines `targets_keyed` as a join, so §8 is the correct realization story; A1 is conflating "definitionally `f(Σ)`" with "reads one index."

**Required**: Distinguish the two in A1. The load-bearing claim there is *zero steps* (no mutation), which holds for all of them. Separate that from read-atomicity: a single-type read (`Observe_K`, per-type `is_K`/`members`) genuinely touches one index, while a cross-type read (`targets_keyed`, default-view reads) is the §8 multi-read and acquires single-index atomicity only under clause 7. Otherwise A1 contradicts §8's premise that the substrate exposes "only the per-type `Observe_K`."

### Issue 3: clause 7 is a *global* reader exclusion, mis-framed as "the dual of W4"

**ASN-0134, §9 (MIC clause 7) / §8 (V2)**: "all its constituent reads pinned to one committed index — a reader-side critical section holding the read sequence against **any interleaving writer step** (the dual of clause 5)"; V2: "the exact dual of W4's writer-side run contiguity."

**Problem**: Clause 5/W4 is a **local** exclusion — per-`(d, s_C)`, "strictly weaker than any cross-home exclusion." Clause 7, "against any interleaving writer step," is **global**: any writer step at any home advances the index, so pinning `p` reads to one index requires excluding *all* writers for the read's duration. Calling clause 7 "the dual of W4" implies a locality parity that does not hold. This bears directly on the note's headline ("per-home, not global"): that liberation is a **writer-side** result (clause 2 / G1). Reader-side multi-read isolation is not per-home — even V2's weaker sufficient condition ("no `Q`-affecting step between the reads") is **type-scoped**, not home-scoped, because a type-`K` tuple may be homed anywhere, and clause 7 escalates that to global "for constructibility." The note never tells the reader that the "per-home, not global" promise stops at writers.

**Required**: State plainly that clause 7 is a (transient) global reader-side exclusion, asymmetric with per-home writer serialization, and that V2's minimal condition is type-scoped — neither is per-home. The reader/writer "dual" is fine as a role distinction; drop or qualify the implied scope symmetry with W4, and add the one sentence the "What this note commits" bullets are missing: the per-home liberation is writer-side; multi-read verdict isolation is not.

## OUT_OF_SCOPE

### Topic 1: order-dependence of batch/composite operations

**Why out of scope**: §4 characterizes operation-level non-confluence with two families (active-membership toggle, target-residence race) and claims "any further cross-home operation that toggles a coverage-equal tuple's active-membership would extend the first family rather than open a third." A batch like `retract_stale`, whose target set is `stale(h)` evaluated against the *active* subset at batch entry, has committed effects that depend on prior cross-home nullifies/emits in a way not cleanly captured by either single-operation family. The note explicitly disclaims closure ("the families we have found"), and `retract_stale` is a non-atomic batch (A5), so a complete taxonomy of composite-operation order-dependence is reasonably a future note — not a defect here. Worth noting only so the "would extend the first family" claim is read as scoped to single operations.

META: (none — the note defines invariants (W0–W6), a linearization model, and an implementation-agnostic contract (MIC) that any realization must satisfy; it is a consistency model, squarely specification, not implementation mechanics.)

VERDICT: REVISE
