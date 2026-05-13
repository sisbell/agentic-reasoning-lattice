# Review of ASN-0043

## REVISE

### Issue 1: L9 quantifier scope contradicts the proof's domain
**ASN-0043, L9 (TypeGhostPermission)**: "For any state Σ satisfying all invariants of this ASN (L0–L14, L-fin) together with all ASN-0036 invariants (S0–S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ), there exists a conforming state Σ' extending Σ with a standard-triple link whose type endset references an address outside dom(Σ'.C) ∪ dom(Σ'.L)"

**Problem**: The proof's case (ii) introduces an informal restriction — "we read the L9 quantifier as ranging over states whose allocator tree carries a T10a-discipline-conforming root — the only setting in which the L- and S-invariants are jointly inhabitable in the first place." This restriction is not part of L9's formal statement. The proof itself shows that a carrier root with zeros(r) > 2 can reach neither a document-level tumbler nor anything beneath it (TA5a blocks `inc(·, 2)`, and `inc(·, k)` for k ∈ {0, 1} does not reduce the zero count). Yet a state with such r and dom(Σ.M) = dom(Σ.C) = dom(Σ.L) = ∅ vacuously satisfies every L- and S-invariant. For that Σ, the L9 existential is unattainable: no conforming extension Σ' with a link can be constructed because no document can be allocated. L9 as stated is therefore false for degenerate but otherwise-conforming Σ; the proof acknowledges this and retreats to a restricted reading of the universal that is not formalized.

**Required**: Either (a) add an explicit precondition to L9 — for example, `zeros(r) ≤ 2`, or the existence of at least one document-level node in 𝒯 — and discharge it in the construction, or (b) prove a separate lemma establishing that the joint L- and S-invariants entail `zeros(r) ≤ 2` in any state whose existential conclusion is being claimed. The current "informal reading of the quantifier" is a hand-wave at a real gap.

### Issue 2: L1a uses home(a) and L1c before they exist
**ASN-0043, L1a (LinkScopedAllocation)**: "(A a ∈ dom(Σ.L) :: home(a) ∈ dom(Σ.M) ∧ a is producible from home(a) by a finite sequence of T10a-conforming inc steps)"

**Problem**: L1a's formal statement uses `home(a)`, which is defined in the later "Home and Ownership" section, and references the producibility-by-`inc`-steps notion, which is L1c (introduced two paragraphs after L1a). The prose acknowledges both forward references with "(defined below…)" and "(L1c, below)". The producibility clause also overlaps with L1c's content, making L1a essentially restate L1c plus the home-document-allocated tightening. A reader encountering L1a in sequence cannot evaluate the predicate without flipping forward, and the overlap with L1c blurs the boundary between the two invariants.

**Required**: Either define `home(a)` and L1c before L1a, or restate L1a using only the field-extraction formula directly (e.g., `N(a).0.U(a).0.D(a) ∈ dom(Σ.M)`) and let L1c carry the producibility content. The current presentation order forces the reader to do the structural work.

### Issue 3: L6's formal statement is a definitional consequence of tuple typing
**ASN-0043, L6 (SlotDistinction)**: "(A a ∈ dom(Σ.L), π : (E i : 1 ≤ i ≤ |Σ.L(a)| : Σ.L(a).e_{π(i)} ≠ Σ.L(a).eᵢ) ⟹ permute(Σ.L(a), π) ≠ Σ.L(a))"

**Problem**: Given that `Link` is defined as a tuple type `{(e₁, ..., eₙ) : N ≥ 3, each eᵢ ∈ Endset}` and `permute((e₁, ..., eₙ), π) = (e_{π(1)}, ..., e_{π(N)})`, L6 reduces to "if the permuted tuple differs at some position, then the permuted tuple differs from the original" — an immediate restatement of componentwise tuple equality. The substantive content of L6 ("slots are first-class structural positions, not multiset members") lives in the prose, not in the formula. As an invariant the statement carries no constraint beyond what the type definition already gives.

**Required**: Either drop the formal statement and recast L6 as a structural commitment on the `Link` type (a definitional note rather than an invariant), or strengthen the formal claim to something not implied by tuple typing — e.g., a positional accessor predicate distinguishing slot indexing from set membership, mirroring how L5 explicitly forbids positional accessors within an endset.

VERDICT: REVISE
