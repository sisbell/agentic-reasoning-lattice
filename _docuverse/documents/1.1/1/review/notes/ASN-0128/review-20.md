# Review of ASN-0128

## REVISE

### Issue 1: "no query could select" in I0 is a multi-step claim argued from an incomplete inventory
**ASN-0128, I0 (SamenessIsCoverageEquality)**: "but under it the active subset could hold coverage-equal tuples that no *matching* surface distinguishes: the membership predicates, `Observe` patterns, and `same_type` all test coverage, never decomposition (TypeEquivalence, ASN-0086), so no query could *select* one such tuple over the other by content."

**Problem**: The inventory lists only the coverage-matched surfaces, but the note's own AM gives the forward enumeration family *denotation-keyed* argument matching (`x ∈ addrs(F)`), which is sensitive to decomposition: on the face of it, `targets_of(t.x)` consults a tuple whose F denotes `{t, t.x}` and not a coverage-equal one denoting `{t}` — exactly I0a's separating pair. The universal conclusion does survive, but only through facts the paragraph never marshals: (a) the gate's `|F| = 1` (P3/P6 via RP) makes F-side denotation differences unstorable — two single spans with equal coverage are the *same* span (equal half-open intervals fix the start, and the sum's length is the action point, fixing the displacement), so the F-keyed family consults coverage-equal incumbents identically; (b) Binary's `|G| = 1` rules out G-side separating pairs the same way; (c) the one surviving case — Multi G-slot pairs — is consulted by `targets_of` in aggregate over all F-matching tuples, so no argument selects one member over the other. As written, a reader checking "no query" against AM finds the denotation-keyed family unaddressed; "X follows from a three-item list" is a claim, not the required case analysis.

**Required**: Either close the denotation-keyed case explicitly (two sentences along the lines of (a)–(c) above), or restrict the stated claim to the coverage-matched surfaces and let the rejection rest on the assertion-semantics ground I0 already gives ("sameness for de-duplication is sameness of assertion").

### Issue 2: "surface-emitted" and SD are derivation properties phrased as state predicates, where the foundation already supplies the correct idiom
**ASN-0128, I1a / SD**: "Call a state's K-history *surface-emitted* when every tuple in `L_K^Σ` was deposited through `Emit_K`"; "A substrate is *surface-disciplined* iff at every reachable state Σ, every tuple in `L_R^Σ` was deposited through this note's operation surface."

**Problem**: "Was deposited through" is not a predicate of a state. A surface miss *is* a `K.λ_sh` step, and a raw `K.λ_sh` step depositing the same value lands at the same frontier address (FrontierUnification) and produces the identical post-state — so a disciplined and an undisciplined derivation can reach the same Σ, and the state does not determine its history. The proofs already betray this: I1a's induction runs over `→_sh*` derivations, and DR reasons per-tuple about deposit-time pre-states — both need the hypothesis attached to derivations, not states. The foundation owns the precise idiom: ASN-0086's RelationalLayer states its discipline as a predicate over steps ("every `→`-step with `L_R^Σ ⊊ L_R^{Σ'}` is a `Nullify`") and LayerReachable as reachability by a step sequence obeying it. The note reinvents this loosely instead of instantiating it — a foundation-notation violation as well as an imprecision.

**Required**: Restate both notions as step-classification commitments in the RelationalLayer/LayerReachable form — e.g., a derivation is surface-disciplined iff every `L_R`-growing step is a `Nullify_Binary` invocation, and K-history is surface-emitted along a derivation iff every `L_K`-growing step is a surface deposit — and quantify I1a, DR, I4's last sentence, and I6's disciplined-domain reduction over states reached by such derivations.

### Issue 3: the idem=⊥ half of the exposed surface has no consolidated postcondition or wp
**ASN-0128, I5 / The operation set**: "`Emit_K` is normatively fixed by the exposed signature and I6 (Idem operational semantics)" — but I6 is "the caller-facing contract for `Emit_K` under `idem(K) = ⊤`", and I5 ends at "the new tuple appears in `A_K^{Σ'}` (modulo I3's born-nullified cases)."

**Problem**: The note holds itself to consolidated contracts — I6 for idem=⊤, DR for the wrapper — but the idem=⊥ branch gets outcome prose with a "modulo I3" hedge precisely where a wp is the honest statement, and the operation-set sentence cites only I6. The missing analysis is one line: the idem=⊥ contract is I6's with `hit ≡ ⊥`, i.e. `wp(Emit_K under idem = ⊥, POST) ≡ pre ∧ d ∈ dom(Σ.M) ∧ C3` (C2 absorbed into `pre` exactly as in I6), reducing on a surface-disciplined substrate to `pre ∧ d ∈ dom(Σ.M)`. Note POST as I6 states it does fail in the born-nullified case even when an earlier idem=⊥ duplicate is active elsewhere, since POST is evaluated at the returned address — so the formula is exact, but nobody has said so.

**Required**: State the idem=⊥ wp — either by widening I6 to cover both flag values (its miss branch is already the idem=⊥ case) or as a one-line corollary in I5 — and have "The operation set" cite it alongside I6.

### Issue 4: the Φ-grounding is stated in full twice (anti-bloat)
**ASN-0128, BH1 Rewrite scope / View selection**: BH1: "Φ itself is never empty: every constructible `Σ_init` carries the shipped `retired` with BH1 (S1, mandatory by R-C1), so a no-filter-anywhere case names no conforming substrate. Where the two views do coincide is where the subtraction removes nothing — …" View selection: "On every constructible substrate the two readings are distinct queries on each `K'` with `Φ \ {K'} ≠ ∅` — at least every `K' ≠ retired`, since `retired` ships with BH1 (S1, R-C1) — coinciding only where the rewrite's subtraction removes nothing (the coincidence cases, BH1's Rewrite scope)."

**Problem**: The same fact — Φ contains the shipped `retired` by S1/R-C1, and the two readings coincide exactly where the subtraction removes nothing — is argued in full in both sections, citations included. This reads as residue of the revision that dropped the Φ-empty coincidence case: the grounding was installed at both sites rather than owned by one. Two paragraphs saying the same thing in different words is the pattern this review mode exists to catch.

**Required**: Let BH1's Rewrite scope (where the rewrite is defined) own the Φ-nonemptiness and coincidence analysis; reduce View selection's sentence to the selector commitment plus a citation.

## OUT_OF_SCOPE

### Topic 1: the serializing authority behind I4
**Why out of scope**: I4 correctly notes that `→_sh` inherits ASN-0086's sequential model and that concurrency is resolved by "a serializing authority" ahead of the relation — but that authority's own contract (ordering guarantees, interaction with `retract_stale`'s non-atomic batches) is new machinery, a future ASN rather than an error in this one.

### Topic 2: registry construction and multi-app merge
**Why out of scope**: R-VAL and R-C1 state the constraints a constructed `Σ_init.registry` must satisfy; the protocol by which several apps' declarations (and the shipped three) are merged and collisions resolved is declared as Open question 8 and is genuinely new territory.

VERDICT: REVISE
