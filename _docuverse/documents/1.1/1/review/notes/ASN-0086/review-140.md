# Review of ASN-0086

## REVISE

### Issue 1: L-ContiguousPrefix proof contradicts its own attribution

**ASN-0086, L-ContiguousPrefix proof**: "The contiguous-prefix form follows from **conformance clause (b) alone**, by induction on the conformance-witnessing transition sequence... Step: ... **By the at-most-one-key-per-home discipline (auxiliary commitment, Definition — substrate-conforming state)**, fix a home `d`. If the step adds no fresh key homed at `d`... Otherwise the step adds exactly one fresh key..."

**Problem**: The lemma asserts the result follows from clause (b) *alone*, then the step immediately invokes the *auxiliary* at-most-one-key-per-home commitment — which the document is at pains to call independent of clause (b). The two are not interchangeable here. The frontier-landing clause (b) is framed per-single-key ("if a step adds *a* fresh key... that key occupies exactly chain index `J+1`"); if one step deposited two fresh keys at home `d`, both would see the same pre-step frontier `J` and both would be required to land at `J+1` — the clause is not well-defined for a multi-key step. The at-most-one commitment is precisely what makes "extends the prefix by *one* chain index" coherent. So the at-most-one commitment is load-bearing for the induction step, contradicting "clause (b) alone."

**Required**: Restate the lemma's basis as "follows from clause (b) together with the at-most-one-key-per-home auxiliary commitment," or demonstrate that frontier-landing well-defines the multi-key case (e.g. by sequencing the keys at `J+1, J+2, …`) and then remove the at-most-one invocation. As written the proof's premises and the stated premise disagree.

### Issue 2: The "crafted-span / direct-K.λ-caller" point is restated three times

**ASN-0086, Definition — Unit-depth retraction discipline**: "a crafted-span retraction emitted by a direct K.λ caller ... is L-invariant-conforming yet violates it."
**WP "Substrate-conformance alone is insufficient"**: "a substrate-conforming Σ may still carry a crafted (non-unit-depth) retraction span emitted by a direct K.λ caller..."
**Open Questions**: "...or is it correctly a layer convention that callers may bypass via direct K.λ with crafted retraction spans?"

**Problem**: The same observation — that K.λ constrains emission *address* but not endset *shape*, so a direct caller can craft a non-unit-depth retraction span — is developed at length in three locations. The anti-bloat classifier flags "two paragraphs say the same thing in different words." The WP paragraph adds a span-coverage derivation, which is the one place the point earns its space; the discipline-definition aside and the Open-Questions restatement repeat it without advancing the argument.

**Required**: State the mechanism once (in the WP analysis, where the coverage interval is computed), and reduce the discipline-definition aside and the Open-Questions item to a back-reference.

### Issue 3: R0 cross-home parenthetical is anticipatory meta-prose with a forward reference

**ASN-0086, R0 proof, subsequent-emission cross-home bullet**: "(This is the conformance-free home-equality argument of R0a Case 1; we need only distinctness `a ≠ ℓ'`, not the stronger prefix-incomparability, so the per-position field-separator analysis there is not required. **We do *not* claim `d, d'` are prefix-incomparable** ... **so T10 is not invoked**.)"

**Problem**: This parenthetical (a) forward-references R0a Case 1, which appears later in the document, and (b) defensively enumerates which foundation lemma is *not* invoked and which stronger property is *not* claimed. Per the forward-reference-accretion patterns, "defensive justifications" and "prose justifies which foundation lemma is not invoked" are noise the reader must skip past — the home-projection argument in the bullet already stands on its own (`home(a) = d`, `home(ℓ') = d'`, equality forces `d = d'`).

**Required**: Delete the parenthetical, or compress to a single clause noting the argument needs only address-distinctness via the home projection. The "we do not claim... so T10 is not invoked" anticipation should be removed.

## OUT_OF_SCOPE

### Topic 1: Behavior of Nullify on a non-A_rel target (e.g. a document tumbler)
The Definition states "only P0 gates emission," so `Nullify(Σ, d_retr, a)` executes even when `a ∉ A_rel^Σ`. If `a` is a document tumbler `d`, the to-span coverage `{t : a ≼ t}` contains *every* link homed at `d`, so `nullified(Σ')` would absorb all of them — single-tuple scope (which needs P1 and R0a's link-antichain) does not apply. The note correctly conditions its guarantees on P1, so this is not an error, but the surprising over-nullification of a prefix-target is not characterized.

**Why out of scope**: The documented Nullify contract requires `a ∈ A_rel^Σ ∧ |Σ.L(a)| = 3`; characterizing malformed-target semantics is a separate concern, not a defect in the stated guarantees.

### Topic 2: Cardinality/ratio bound on nullified(Σ) relative to dom(Σ.L)
Already listed in Open Questions; genuinely new territory.

**Why out of scope**: Belongs to a future ASN on retraction economics, not this layer's structural lemmas.

VERDICT: REVISE
