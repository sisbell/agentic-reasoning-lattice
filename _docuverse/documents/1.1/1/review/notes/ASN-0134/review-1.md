# Review of ASN-0134

This is an ambitious and largely well-argued note. The step-as-atom analysis (A0–A4), the snapshot-read isolation (A4), and the soundness/durability split for quiescence (V0/V1) are correct and sharply stated. But the note straddles two substrate models without reconciling them, two of its headline safety claims overstate what the proofs deliver, and the central "per-home suffices" theorem is formalized in a model that cannot express it. These must be fixed before layers build on it.

## REVISE

### Issue 1: `𝔼` ranges over an undefined state combining two incompatible substrate stacks

**ASN-0134, §1**: "each `Σ_i → Σ_{i+1}` is one atomic step `σ_i` drawn from the step vocabulary `K = {K.σ, K.α, K.λ_sh, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ}`."

**Problem**: This vocabulary fuses two distinct foundations that have different state signatures and different, mutually exclusive document-creation steps.

- `K.σ` is ASN-0093's `DocumentRegistration` over the three-component state `(C, M, L)`, where every document carries `M(d) = ∅` (ASN-0093 M2). ASN-0086/0126/0128 (and `Emit_K`, `Nullify_Binary`, `Observe_K`, the registry, `idem`) all build on *this* model. It has no `K.δ`, no `E`, no `R`.
- `K.δ` is ASN-0047's `EntityCreation` over the five-component state `(C, L, E, M, R)`, where `M(d)` is an *arrangement* (a non-empty V→I map governed by D-SEQ★) and documents are created as entities on version chains. It has no `K.σ` and no registry.

Listing both `K.σ` and `K.δ` is not a typo — H0's proof relies on it: "Any other step either frames `dom_S` (`K.σ`, `K.μ`, `K.ρ`, `K.δ` leave the relevant store fixed)." So the note treats them as distinct co-resident steps. But document creation is `K.σ` in one model and `K.δ` in the other; they cannot both be primitive over one `Σ`. Worse, the two models disagree on `M`: A6 imports ASN-0047's `ExtendedReachableStateInvariants` (which constrains `M` as an arrangement, D-CTG★/D-SEQ★), while A1/A4/W5 use ASN-0128's operations (which inherit ASN-0093's `M(d) = ∅`). If `M` is empty, A6's arrangement invariants are vacuous and the "structurally canonical arrangement" story collapses; if `M` is arrangement-bearing, the registry-gated surface of 0128 has no defined action on it. No foundation defines the `(C, L, E, M, R, registry)` state the note silently presumes.

**Required**: Commit `𝔼` to one stack. Since ASN-0133 (which builds on this note) lives in the 0093→0086→0126→0128 stack, the natural choice is to draw `K` from `→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh` and recast A6, A5's batch examples (fork, provenance), and H0's framing list without 0047's `K.δ`/`K.μ`/`K.ρ`/arrangement-`M`. Alternatively, if the arrangement layer is genuinely needed, first construct the unified state, reconcile `K.σ` vs `K.δ` document creation and empty-`M` vs arrangement-`M`, and prove the combined transition system — *then* reason about `𝔼`. As written, the object every claim quantifies over is undefined.

### Issue 2: M1(b) "no duplicated effect" is false for `idem = ⊥`, and commit-before-acknowledge does not deliver it

**ASN-0134, §8, M1 proof**: "(b) *No duplicated effect.* ... idempotent types collapse semantic repeats to zero-step hits ...; and sharing is by reference to one permanent address, never by copy ... Clause 3 forbids an at-least-once retry from committing a second time before acknowledgment."

**Problem**: Two of the three defenses cover only `idem = ⊤`, and the fourth (clause 3) is simply wrong.

- For `idem = ⊥`, ASN-0128 I5 and ASN-0086 R2's consequence are explicit: two emissions with identical `(F, G, K)` produce **distinct addresses**, and "both tuples appear in `A_K^{Σ₂}`." A reader observing `A_K` then sees two tuples of identical content — a duplicated effect — *by design*. The reference-sharing principle ("one permanent address, never by copy") is about transclusion of content; it does not apply to two distinct link tuples that happen to carry equal endsets.
- The clause-3 sentence conflates ordering with exactly-once delivery. Commit-before-acknowledge (A7) guarantees the response is produced at-or-after `lin(op)`. It says nothing about a *lost* acknowledgment: a client that times out and retries issues a second operation, which for `idem = ⊥` commits a second tuple. A7 neither detects nor suppresses this. What collapses semantic repeats is idempotency, not clause 3.

So M1(b) as stated is false, and MIC contains no clause that would make it true.

**Required**: Scope (b) to what is actually proved: (i) no *single* operation's effect appears at two indices (A1, unique index), and (ii) `idem = ⊤` collapses semantic repeats (0128 I1). Then state plainly that `idem = ⊥` permits content-duplicated tuples by design (0128 I5, 0086 R2) and that MIC does not — and is not meant to — prevent it. Delete the claim that commit-before-acknowledge forbids retry double-commit.

### Issue 3: §2/A6 — "the precise and only sense of incomplete" omits the coupling-complete-but-transient case

**ASN-0134, §2**: "but that may be *coupling-incomplete*: a freshly allocated content address may not yet have its provenance recorded ... This is the precise and only sense in which an observation can be 'incomplete.' It is never *corrupt*; it is at worst *mid-coupling*."

**Problem**: A reorder is a foundation-defined named composite `K.μ~ = K.μ⁻ + K.μ⁺` (ASN-0047), and both constituents are in the note's own `K`. In `𝔼` it appears as a `K.μ⁻` step then a (possibly non-adjacent) `K.μ⁺` step, and by A0 the intermediate state `Σ_{i+1}` is observable. Consider `d` arranged `[A, B, C]` reordered to `[C, A, B]`, realized as a contraction (often to empty) followed by a re-extension. The intermediate shows `d` with content *transiently removed* — content present both before and after.

Crucially, this intermediate is **not** coupling-incomplete. `K.μ⁻` frames `C` and `R`, so by P0/P2 the removed content and its provenance persist; `Contains_C` only shrinks, so P4★ (`Contains_C ⊆ R`) and P7a still hold. The mid-reorder state therefore satisfies *every* per-state invariant **and** the composite-boundary properties — it is indistinguishable, by the entire invariant framework, from a settled deletion — yet it is transient. The note's dichotomy (canonical+complete = trustworthy vs canonical+incomplete = mid-batch) is not exhaustive: coupling-completeness does **not** signal settledness. The "half-populated mid-fork" example the note does give is monotone-growing; it never confronts the non-monotone shrink-then-grow case, which is exactly the one that defeats "at worst mid-coupling."

**Required**: Retract "the precise and only sense." Add the transient-content case explicitly and conclude that a fully-coupled snapshot may still be mid-transformation, so coupling-completeness is not a reliable settled-vs-transient discriminator. (This actually *reinforces* §7's V1 — durability needs a future hypothesis — but it contradicts §2's reassurance and must be reconciled with it.)

### Issue 4: G1 is vacuous in the note's single-total-order model

**ASN-0134, §4, G1**: "Let `𝔼` be any realization in which, for every `(d, S)`, the `S`-allocations to `d` are totally ordered among themselves (per-home serialization), each step is applied atomically (A0) ... Then `𝔼` preserves every per-state invariant ... *as if* globally serialized."

**Problem**: By A0/G0, `𝔼` is *already* a single total order of atomic steps. A total order serializes everything, cross-home included, so the hypothesis "per-home serialization" adds nothing and the conclusion "as if globally serialized" reduces to "it is globally serialized." The intended content — that an implementation need only *coordinate* per-home and may leave cross-home steps genuinely concurrent — cannot be stated, because the note has no execution model weaker than a total order to contrast against. The proof's "transform into a global serial order by ... transposing adjacent cross-home steps" transposes within an already-total order, yielding another total order with the same committed states; that is a true commutativity fact (H1), but it is not "per-home suffices." The note conflates the implementation's coordination discipline (which steps it forces to be ordered) with `𝔼`'s ordering structure (always total).

**Required**: Either (a) introduce a genuine concurrency model — a partial order on steps in which same-`(d,S)` steps are ordered and cross-`(d,S)` steps may be incomparable — and prove that *every linearization* of a per-home-ordered partial order is a valid invariant-preserving total order (the H1 transposition argument now has a non-trivial source); or (b) restate G1 as the commutativity fact it actually establishes (cross-home transpositions of a total order preserve all committed states and invariants), dropping the per-home-vs-global framing that the model cannot support.

### Issue 5: H2's proof skips the first-emission boundary

**ASN-0134, §4, H2 proof**: "`SubsequentEmissionFreshness` derives a fresh address from `a = inc(a_prev, 0)` with `a_prev = max P_S(d, Σ_pre)`. Two emissions with the same pre-state population read the same `a_prev`, hence compute the same `a`."

**Problem**: When `P_S(d, Σ_pre) = ∅`, `a_prev = max ∅` is undefined and `SubsequentEmissionFreshness` does not apply. This is the boundary case — two writers racing the *first* allocation into a fresh home. Both fire ASN-0093's first-emission predicate (`{a' : origin(a') = d} = ∅`) and both compute `a = [d.0.s_C.1]` (resp. `[d.0.s_L.1]`), colliding via `FirstEmission`/`FirstEmissionFreshness`, not the subsequent mechanism the proof cites. The conflict is just as real, but H2 as written does not cover it. Boundary cases are mandatory.

**Required**: Add the `P_S(d, Σ_pre) = ∅` case, showing two concurrent first emissions both land at the determinate first slot and collide.

### Issue 6: no concrete worked example

**Problem**: The note is entirely abstract. Every key claim (H1 commutation, H2 collision, W4 run fragmentation, M1(c) collision-freedom) is argued in prose over generic `(d, S)`, never instantiated against specific tumblers. The standards require at least one concrete scenario verifying the key postconditions.

**Required**: Add a worked scenario with explicit addresses — e.g. two writers into home `d = [1.0.1]`: both read content frontier `φ_{s_C} = 3`, both compute `[d.0.s_C.4]`, exhibiting the H2 collision; the same two writers into `d` and `d' = [1.0.2]` showing H1 commutation; and a 3-atom run into `(d, s_C)` with one interleaved foreign `K.α` showing the W4 fragmentation. Concrete addresses would also surface the Issue-1 and Issue-5 ambiguities directly.

### Issue 7: self-containedness — load-bearing references to non-foundation ASNs

**ASN-0134, intro/§6/§7**: "Predicates are evaluated by *any* observer (ASN-0129)"; "one contiguous run ... (ASN-0130)"; "ASN-0133's Q0 wants quiescence"; "a definition's content run (ASN-0130: one `K.α` per atom)".

**Problem**: ASN-0129, ASN-0130, and ASN-0133 are not foundation ASNs. The note references them by number and by claim label (`Q0`), and organizes whole sections (§6 around 0130's run requirement, §7 around 0133's quiescence) such that the *motivation* for W4 and V0/V1 cannot be understood without them. Per the self-containedness standard, this is a defect — the substrate guarantees should stand on their own.

**Required**: State each guarantee abstractly without the ASN numbers — "a layer that requires a definition's content to occupy one contiguous run," "a layer that must recognize quiescence while writers remain active," "predicates evaluated by an arbitrary observer." Keep the dependency list, but remove imported labels and non-foundation claim references from the body.

## OUT_OF_SCOPE

### Topic 1: cross-server composition of per-home orders
The note flags this itself (Open Question 5; "What this note does not cover"). How per-home orders compose when homes live on different servers, and the weakest cross-server contract preserving cross-home uniqueness under ownership migration, is correctly a separate note. G1 (once repaired per Issue 4) is the right seam for it.

### Topic 2: a general batch-atomicity contract
Making a multi-step batch (fork, retraction set) appear atomic without reintroducing global serialization is correctly deferred (Open Question 3). W4 supplies the one batch the corpus demands be locally contiguous; the general construction belongs to a future note.

VERDICT: REVISE
