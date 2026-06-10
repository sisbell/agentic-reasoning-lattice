# Review of ASN-0114

The note is mathematically sound. I checked F0–F8 and the worked instance: the derivations of F2 (from F1 + S0 convexity), F5 (from F1 + L12 composed by LP13), F7 (from F1 + the two S2 collapses), and the `R = ⟨⟩` wp are all correct, the boundary cases (empty endset, invalid selector, disconnected coverage, type-slot non-emptiness, content-absent targets) are covered, the worked example checks out arithmetically, and all cross-references are to foundation ASNs. The findings below are one precision gap and two instances of the accreted meta-prose the anti-bloat classifier flags.

## REVISE

### Issue 1: F6's confinement is coverage-level, but the prose and evidence assert representation-level non-exposure
**ASN-0114, F6 (SlotConfinement) / "Confinement: one end tells nothing of the others" / Synthesis**: "The result neither depends on nor returns any `eⱼ` with `j ≠ i`." … "requesting endset N cannot expose the content of endsets at N ± k" … (Synthesis) "while neither depending on nor revealing the other ends (F6)."

**Problem**: The *formal* F6 statement is correctly scoped — it asserts only that `coverage(followlink(Σ, a, i))` is a function of `coverage(Σ.L(a).eᵢ)` ("up to coverage"), which is immediate from F1. But the surrounding prose drops the qualifier and claims that *the result* does not reveal `eⱼ`, and offers the Q18 quote as support. The contract does not establish this. F1 binds only `coverage(R)`; F3 *explicitly* leaves the span decomposition of `R` free ("representation is free; coverage is bound," "below the abstraction"). A concrete implementation realizes one selection from the F1-admissible set, and the contract places no constraint forbidding that selection from depending on `eⱼ` — e.g., choosing how to split `eᵢ`'s coverage conditioned on a property of `eⱼ`. Such a result honors F1 yet exposes `eⱼ` at the representation a caller actually receives. The Q18 evidence ("cannot expose the content of endsets at N ± k") describes the *implementation's* bounded query, not a guarantee the abstract contract makes. By the ASN's own F3 reasoning — representation is below the abstraction — representation-level confinement is likewise an implementation property, not a contract guarantee. As written, the confinement *intent* (a caller learns nothing about `eⱼ`) exceeds what F1+F3 deliver.

**Required**: Coverage-scope the confinement prose throughout, matching the formal "up to coverage." State explicitly — exactly as F3 does for span ordering — that representation-level non-exposure of `eⱼ` is an artifact of the bounded-query implementation, not derivable from the contract. Present the Q18 quote as corroborating the implementation, not the abstract claim.

### Issue 2: F5 derivation is followed by a redundant premise recap
**ASN-0114, "Determinism over time", immediately after the ∎**: "F5 as stated is a *coverage*-permanence claim, and exactly two facts carry it: *coverage exactness* (F1) and *link immutability* (L12, composed along Σ →* Σ' by LP13)."

**Problem**: The derivation directly above already names F1 and L12 (via LP13) as the load-bearing facts and concludes the coverage equality. This trailing sentence adds only the "exactly two facts carry it" exhaustiveness framing — a use-site inventory the reader skips past after finishing the proof. It does not advance the argument.

**Required**: Delete the sentence; the labeled derivation stands on its own.

### Issue 3: F7's wp paragraph is bracketed by meta-commentary that does not advance it
**ASN-0114, "The empty end versus the invalid selector"**: "That boundary wp only restates F0's domain; no backward reasoning is exercised. The wp that actually probes F7's empty/non-empty split is the one asking when the result *is* the empty span-set." … and the trailing "The third conjunct is exactly the state-dependent condition F7 makes load-bearing: among the defined calls, those returning the empty success are precisely those over an empty end, while every non-empty end returns a span-set of coverage `coverage(Σ.L(a).eᵢ) ≠ ∅`."

**Problem**: The one substantive line — the backward chain `R = ⟨⟩ ⟹ coverage(eᵢ) = ∅ ⟹ eᵢ = ∅` yielding the `R = ⟨⟩` wp — is bracketed by defensive proof-method commentary ("no backward reasoning is exercised," pre-empting a reviewer) before it and a prose restatement of the wp's third conjunct after it. Both bracket sentences are skip-past-able relative to the formulas.

**Required**: Let the two wp formulas stand by themselves; drop the "no backward reasoning is exercised" pointer and compress or delete the trailing restatement of the third conjunct.

## OUT_OF_SCOPE

The "boundary we must respect" section and the Open Questions correctly route endset-against-document resolution, serialization of the `⟨⟩`/`⊥` distinction, and multi-document coverage reporting to future work. These are appropriately excluded; I have no out-of-scope content to add.

VERDICT: REVISE
