# Review of ASN-0134

This is a careful, honest note. The conflict analysis (H0–H2), the invariant partition (W0–W6), and the operation-level caveats of §4 are rigorous, and the worked traces in §7 and §8 are concrete and correct. I checked the §8 quiescence trace and the §4 "incumbent-nullify" instance (ii) in detail — both hold, including the born-active argument for `a_A ∉ subtree(a_T)` via the `R0a` antichain. Two completeness gaps remain.

## REVISE

### Issue 1: The transition-invariant enumeration omits M1 (document permanence), but the text claims it is complete

**ASN-0134, A6 (transition clause and summary)**: "for every `k ≥ 1`, the step `Σ_{k-1} → Σ_k` on `𝔼` preserves `C0` and `L12`" … "every step maintains the two transition invariants — there is no third class of obligation reserved for composite boundaries." And **W0**: "Append-only monotonicity and value-immutability — `C0` … and `L12` … — are model-intrinsic."

**Problem**: ASN-0093 carries a third transition invariant, **M1 (ArrangementMonotonicity)**: `(A Σ → Σ' :: dom(M) ⊆ dom(M'))` — documents are never removed (`K.σ` only adds; `K.α`/`K.λ_sh` frame `M`). M1 is purely relational, exactly like `C0`/`L12`, with no per-state form, so it belongs in the transition clause — yet it appears in neither the per-state package (which lists `M0` and `M2` but not `M1`) nor the transition clause. The framing "the two transition invariants / no third class" is therefore inaccurate; there are three (M1, C0, L12). This is not cosmetic: document permanence is load-bearing for the whole frontier theory — `P_S(d, ·)` and every contiguity/confluence argument presuppose that a home `d ∈ dom(M)` stays in `dom(M)` across the execution, which is precisely M1. The note even leans on it in H0's proof ("a `K.σ`, which registers a document"), without ever asserting it as a preserved invariant. W0 has the same omission: its "model-intrinsic monotonicity" covers content and links but not the document set, though document permanence is as model-intrinsic as the other two (no step removes a document).

**Required**: Add M1 to the transition clause and to W0's model-intrinsic monotonicity list, and correct "the two transition invariants" to three — or explicitly justify M1's exclusion (it is not derivable from the per-state package: the package's `C2`/`L1a` forbid removing a document that *hosts* content, but not removing a childless document, so M1 is independent).

### Issue 2: G1's confluence is proven only for K.σ-free schedules, but the liberation result and contract govern full executions that contain K.σ

**ASN-0134, G-PO / G1 / §4**: G-PO defines a schedule as "a finite set `O` of allocation steps (`K.α`, `K.λ_sh`) into homes already registered at `Σ` — **no `K.σ` is scheduled**"; §4 states "the conflict, confluence, and contract results that follow accordingly quantify over allocation steps only"; and the note presents "G1 is the practical payload."

**Problem**: Executions `𝔼` (and the executions MIC is a contract for) contain `K.σ` steps — documents get registered during operation. G1's confluence is established only for the registration-free fragment. The note proves H1 (cross-home allocation *commutation*) and gives the same-`d` `K.σ` *collision* — "a same-address collision, structurally like H2 below … resolved by rejecting the loser" — but it never establishes the corresponding **cross-`d` `K.σ` commutation** (the H1-analog) that would lift confluence to executions containing registration. As written, the central liberation claim "per-home serialization suffices" is not proven for any execution that registers a document. The bridge is short — under the assumed document-address freshness, a `K.σ` registering `d_new` frames `C`/`L` and so commutes with every `K.α`/`K.λ_sh` (which frame `M`) and with every `K.σ` for `d'_new ≠ d_new` — but it must be stated, because the headline result currently has a hole exactly where real executions live.

**Required**: Either (a) state and prove the `K.σ`-commutation lemma (the H1-analog) under register-before-allocate and the freshness assumption, extending G1(ii)'s confluence to full executions; or (b) explicitly scope the liberation to registration-quiescent phases and defer registration-interleaving confluence — noting, to keep the contract intact, that MIC's safety theorem M1 rests on H1/H2/clauses directly and does **not** depend on full-execution confluence.

## OUT_OF_SCOPE

### Topic 1: Batch read-atomicity and durable quiescence
**Why out of scope**: The note correctly *declines* to make a multi-step batch appear atomic to a reader (A5, Open Question 4) and correctly separates verdict soundness from durability (V1, Open Question 5). These are genuinely future contracts (a snapshot-readable completion marker, a writer-linearization hypothesis), not defects in this ASN — the note neither claims them nor needs them for MIC/M1. Cross-server confluence under home migration (Open Question 6) is likewise properly deferred.

META: (none — the note specifies an abstract consistency contract that any faithful implementation must present, explicitly refusing to name a lock/transaction/scheduler; it has not drifted into implementation mechanics.)

VERDICT: REVISE
