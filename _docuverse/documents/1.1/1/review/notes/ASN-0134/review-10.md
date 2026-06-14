# Review of ASN-0134

This is a strong, unusually careful note — the boundary handling in H2 (first-emission vs. interior), the step/operation seam in §4, the active-membership-toggle instance (ii) that *survives* emit-before-retract, and the V2 worked trace are all done to standard. Two issues block convergence, both in load-bearing proofs.

## REVISE

### Issue 1: H1/W1 anchor-incomparability is justified by an argument that fails for nesting homes

**ASN-0134, §4 (H1 proof) and §5 (W1)**: "the anchors `b_S(d) = [d.0.S…]` and `b_{S'}(d') = [d'.0.S'…]` *diverge already at the document component `d ≠ d'`*, which precedes the subspace digit … *document-level divergence subsumes every `d ≠ d'` pair within the ASN-0093 stack*." (W1: "for `d ≠ d'` the anchors diverge at the document component, prefix-incomparable *regardless of subspace*.")

**Problem**: In the ASN-0093 stack a document is *any* caller-supplied T4-valid address with `zeros = 2` (K.σ precondition: `d ∉ dom(M) ∧ T4-valid(d) ∧ zeros(d) = 2`). Nothing forbids two registered documents from nesting under the prefix order. Concretely, `d = [1.0.1.0.1]` and `d' = [1.0.1.0.1.1]` are both T4-valid with `zeros = 2` and both K.σ-registrable, yet `d ≼ d'`. For this pair the *document components do not diverge* — `d` is a prefix of `d'`. The H1 cross-subspace branch (`S ≠ S'`, `d ≠ d'`) is settled *only* by document-level divergence, since the note explicitly states `CrossDocumentDisjointness`'s single-`·` form "names only the `S = S'` instance." So that branch is unproven for nesting homes, and the blanket "document-level divergence subsumes every `d ≠ d'` pair" is simply false.

The *conclusion* survives — `b_C(d) = [1.0.1.0.1.0.1]` and `b_L(d') = [1.0.1.0.1.1.0.2]` are prefix-incomparable because they first differ at index 5, the field-separator `0` after `d` versus `d'`'s necessarily-nonzero continuation (a third zero there would break `zeros(d') = 2`) — but not by the reason given.

**Required**: Replace the document-divergence justification (H1's `d ≠ d'` branch and W1) with an argument valid when `d ≼ d'`. Cleanest is the origin projection: an address allocated into `(d, S)` has `origin = d`, so for `d ≠ d'` the two deposits carry distinct origins and are unequal *regardless of subspace*, with no anchor reasoning. Alternatively invoke the separator-vs-nonzero-continuation argument `CrossDocumentDisjointness` itself uses. (§7's worked example sidesteps this by choosing sibling homes `[1.0.1.0.1]`/`[1.0.1.0.2]`; either add the nesting case or state that homes are assumed pairwise prefix-incomparable.)

### Issue 2: A6's "per-state canonicity package" is presented as exhaustive but enumerates a subset

**ASN-0134, §2 (A6)**: "the *per-state canonicity package* of the `→_sh` stack — the invariants that are predicates of a single state … : ASN-0093's per-state store invariants `SD`/`C1c`/`L1c` (inherited by ASN-0086), ASN-0126's `P6` … and the *registry-fixity predicate*" and "a `→_sh` state is either *fully* per-state-canonical or unreachable."

**Problem**: `SD`/`C1c`/`L1c` are not "ASN-0093's per-state store invariants" — they are three of them. ASN-0093 carries many more single-state invariants the package omits: `C2` (`origin(a) ∈ dom(M)`), `L0` (content/link subspace partition), `L1a` (link origin allocated), `M0` (document well-formedness), `M2` (empty arrangement), `L-fin`, `C-fin`. None of these is subsumed by the listed five — `P6` constrains stored link *values* (shape-conformant triples), not address subspace (`L0`) or home-allocation (`C2`). So "the invariants that are predicates of a single state" and "*fully* per-state-canonical" overstate what the enumeration certifies. This is load-bearing downstream: §2's "an observation is therefore never *corrupt*" and V0's "`Σ_r` is always a coherent referent" rely on every state being *fully* structurally well-formed, which the listed subset does not establish.

**Required**: Either complete the enumeration over all per-state invariants of the 0093/0086/0126/0128 stack, prove the omitted ones follow from the listed five, or reframe `SD`/`C1c`/`L1c`/`P6`/registry-fixity as a representative load-bearing subset and drop "fully." The easy route is already in hand: A6 proves every `Σ_k` is `→_sh*`-reachable, and reachability yields *all* per-state invariants via the same `B2`/`RP-a` transfer the proof already invokes — so defining "structurally canonical" as "satisfies every per-state invariant of the stack" is both stronger and no harder to discharge.

## OUT_OF_SCOPE

### Batch read-atomicity, durable quiescence, cross-server composition
I checked whether the note's deferrals hide real gaps and they do not. The interior-prefix readability of even a W4-contiguous run (Open Question 4), promotion of a sound verdict to a durable one (V1 / Open Question 5), and per-home order composed across servers (Open Question 6) are correctly future territory — each names new contract surface (reader-side batch isolation, writer linearization-point hypotheses, BEBE) rather than an error in this note's claims. A5 and V1 are honest that the substrate stops at the single step; deferring the strengthenings is right.

META: (not applicable — the note specifies abstract system guarantees and a contract any faithful realization must meet, not implementation mechanics; it has not drifted.)

VERDICT: REVISE
