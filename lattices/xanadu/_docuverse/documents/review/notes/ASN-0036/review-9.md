# Review of ASN-0036

## REVISE

### Issue 1: S8a formal quantifier contradicts acknowledged scope
**ASN-0036, S8a**: "(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v > 0)"
**Problem**: The quantifier ranges over ALL V-positions in ALL documents. The Remark immediately following acknowledges that link-subspace V-positions (with `v₁ = 0`) would have `zeros(v) ≥ 1`, violating the property. The prose says "this ASN treats only the text subspace, where `v₁ = 1`," but prose scoping does not restrict a formal quantifier. S8a as stated is false for any system that has link-subspace V-positions — and the ASN's own Remark confirms this.
**Required**: Restrict the formal quantifier to text subspace. Either `(A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : zeros(v) = 0 ∧ v > 0)` or introduce `dom_text(M(d)) = {v ∈ dom(M(d)) : v₁ ≥ 1}` and quantify over that. The Remark's acknowledgment is appropriate but must be preceded by a correct formal statement.

### Issue 2: S5 within-document witness omits S0 and S1
**ASN-0036, S5**: "S2 holds — each vᵢ maps to exactly one I-address (namely a). S3 holds — a ∈ dom(C). The within-document sharing multiplicity is N + 1 > N."
**Problem**: S5 claims consistency with S0–S3. The cross-document witness explicitly notes "S0 is vacuous — single state, no transition to check." The within-document witness checks only S2 and S3, never mentioning S0 or S1. Since S5's formal statement asserts `Σ satisfies S0–S3`, every conjunct must be addressed for each witness.
**Required**: Add the vacuity note for the within-document case. One sentence suffices: "S0 and S1 are vacuous as above (single state, no transition)."

### Issue 3: S8 properties table omits foundation dependencies
**ASN-0036, Properties Introduced table**: "S8 … theorem from S8-fin, S8a, S2, S8-depth"
**Problem**: The S8 uniqueness proof directly invokes T5 (ContiguousSubtrees), PrefixOrderingExtension, TA5(c), and TA7a — all from ASN-0034. Other entries in the same table do list foundation dependencies (S7 lists "T4, GlobalUniqueness (ASN-0034)"). The omission makes S8 appear self-contained within this ASN when it is not.
**Required**: Add the foundation dependencies: "theorem from S8-fin, S8a, S2, S8-depth, T5, PrefixOrderingExtension, TA5(c), TA7a (ASN-0034)."

## OUT_OF_SCOPE

### Topic 1: Maximal span decomposition
S8 proves existence of a decomposition (via singletons). Whether a unique maximal decomposition (fewest runs) exists, and whether merging adjacent compatible singletons always yields it, is a separate question. The ASN correctly lists this as an open question.
**Why out of scope**: This is a structural property of decompositions, not an error in the existence proof.

### Topic 2: Operation-level correspondence run guarantees
The ASN argues informally that forward allocation (T9) produces natural correspondence runs of length > 1, but does not formalize this. The open questions ask under what conditions operations guarantee non-trivial runs.
**Why out of scope**: This requires operation definitions (INSERT, COPY, etc.), which are explicitly out of scope.

VERDICT: REVISE
