# Review of ASN-0086

I checked the proofs (R0–R7a), the worked sketch, and both wp analyses against the foundations. The mathematics is sound — the worked example computes correctly (a₁=1.0.1.0.1.0.2.1 through b₂=1.0.1.0.1.0.2.4, with the active/audit slices tracking exactly), the antichain/contiguity induction in R0a/R0a-Cor1 is non-circular, and the Case 2 wp is genuinely weakest. The findings below are the anti-bloat patterns the `review-mode.anti-bloat` classifier asks me to surface; they are prose defects, not logic errors.

## REVISE

### Issue 1: `a_emit` definition enumerates its downstream consumers
**ASN-0086, Definition — `a_emit(Σ, d)`**: "We use `a_emit(Σ, d)` as the single canonical name for this address throughout — in R0, Emit_K and its function-ness Lemma, R7a, and the wp analysis — rather than re-spelling the two branches at each site."
**Problem**: This is the use-site inventory pattern — a definition's introduction listing the places it is later consumed. The list ("R0, Emit_K and its function-ness Lemma, R7a, and the wp analysis") advances nothing about what `a_emit` *means*; it rots as sections move. The recent commit "hoist a_emit definition" left this scaffolding behind.
**Required**: Delete the use-site clause. End the definition at "The outcome is determined by `(Σ, d)` alone, so `a_emit` is a function of `(Σ, d)`."

### Issue 2: same `a_emit` well-definedness fact stated three times
**ASN-0086, `a_emit` def / R0 subsequent branch / Emit_K function-ness Lemma**: respectively "the unique T1-extremum of a finite (L-fin) non-empty set, by T1 trichotomy alone — no contiguity or conformance appeal"; "so T1 trichotomy alone furnishes the unique maximum, with no contiguity or →*-reachability hypothesis consumed"; "rests on L-fin and T1 trichotomy alone — no conformance or contiguity hypothesis is consumed beyond L-fin."
**Problem**: One fact — `a_emit`'s max is well-defined from L-fin + T1 trichotomy without conformance — is asserted in three sections in three wordings. Establish it once at the definition; the later sites should cite, not re-argue.
**Required**: Keep the claim in the `a_emit` definition. In R0's subsequent branch and the function-ness Lemma, replace the re-derivations with a bare reference to the definition.

### Issue 3: R6b's "insensitivity" point is formulation-defense, and is duplicated by its own proof
**ASN-0086, R6b, Remark**: "...but it belongs in the conclusion's *insensitivity* to `b`'s status, not in a redundant antecedent conjunct."
**Problem**: Two defects. (a) This sentence justifies *why the claim is phrased the way it is* (a redundant conjunct was removed in the "tighten R6b antecedent" revision) — reviser drift explaining a formulation choice rather than the claim. (b) The Remark and the proof state the identical content: Remark says "the conclusion is therefore unaffected by whether `b ∈ nullified(Σ)`"; the proof says "the conclusion `a ∈ nullified(Σ)` is insensitive to whether `b ∈ nullified(Σ)`: it holds with or without it." R6b is a definitional unfolding of `nullified`; the insensitivity belongs once, in the proof.
**Required**: Drop the "not in a redundant antecedent conjunct" clause and the surrounding meta-commentary. State the insensitivity once (in the proof) and let the Remark, if retained, only name that `b`'s own status does not undo its prior retractions.

### Issue 4: R7a discharge (4) part (ii) proves order-independence the claim does not need
**ASN-0086, R7a proof, discharge (4)(ii)**: "Cross-home interleaving in the Δ-enumeration is therefore immaterial — any iteration order produces the same outcome at each home..."
**Problem**: R7a's conclusion is existential — it must exhibit *one* `→`-sequence with `Σ_m.L = Σ'.L`. Proving that *every* iteration order yields the same outcome is defensive exhaustiveness beyond the obligation. The load-bearing fact (each `a_k` lands at its home's next chain index, via origin-scoped K.λ determinism) is already carried by (i) and (iii); (ii)'s "any order is immaterial" framing is surplus.
**Required**: Reduce (ii) to the one sentence that is used — K.λ's emission predicate at `d_k` is origin-scoped, so earlier emissions at other homes do not perturb the outcome at `d_k` — and drop the order-independence generalization.

## OUT_OF_SCOPE

### Topic 1: elevating the unit-depth retraction discipline to a substrate guarantee
**Why out of scope**: The note correctly identifies (Open Questions; wp Case 2 regime (ii)) that K.λ constrains emission addresses but not endset shape, so crafted-span retractions are admissible. Whether to add a designated retraction K-operation with a shape constraint is a substrate-design change belonging in ASN-0093 or a successor, not a revision here.

### Topic 2: higher-arity typed relations `L_K^{(n)}`
**Why out of scope**: The restriction to standard-triple links (`|Σ.L(a)| = 3`) is stated explicitly, and the higher-arity construction is named as not pursued. The binary-projection-vs-n-ary question is genuinely new territory.

VERDICT: REVISE
