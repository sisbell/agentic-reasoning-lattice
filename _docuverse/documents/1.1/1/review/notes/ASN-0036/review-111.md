# Review of ASN-0036

## REVISE

### Issue 1: S5 statement and proof disagree on the V-positions used
**ASN-0036, Unrestricted sharing (S5)**: the prose states "`N + 1` documents `d₁, ..., d_{N+1}`, each with `M(dᵢ) = {vᵢ ↦ a}` for distinct V-positions `vᵢ`", but the proof fixes "a single V-position `v = [1, 1]` ... shared across all `N + 1` documents" and defines `M_N(dᵢ) = {v ↦ a}`.
**Problem**: The cross-document construction in the proof uses one shared `v`, contradicting the "distinct V-positions `vᵢ`" of the statement it is supposed to discharge. A reader cannot tell which construction is canonical.
**Required**: Make the statement and proof agree — either distinct `vᵢ` throughout, or a single shared `v` throughout.

### Issue 2: S5 Frame contradicts the S5 proof body
**ASN-0036, S5 Formal Contract Frame**: "S5 ranges over S0–S3 only; the witnesses are not claimed to satisfy later invariants."
**Problem**: The proof body does exactly the opposite, twice: "strengthening the construction beyond the S0–S3 scope of S5 to also satisfy strand-model V-position well-formedness" (it verifies S8a for `[1,1]` and `[1,k]`). The Frame's disclaimer and the proof's S8a verification are in direct conflict. The S8a verification is also scope creep — S5 is about sharing multiplicity under S0–S3.
**Required**: Remove the S8a verification from the S5 proof (it belongs nowhere in S5), or remove the Frame disclaimer. They cannot both stand.

### Issue 3: S9 adds no formal content over S0
**ASN-0036, S9 proof**: "The consequent of S9 is a special case of S0's universal guarantee, restricted to transitions that modify some arrangement."
**Problem**: S0 already holds for *every* transition. S9's antecedent (`Σ'.M(d) ≠ Σ.M(d)`) restricts to a *subset* of transitions with the *identical* consequent — so S9 is strictly weaker than S0 and proves nothing S0 does not already give unconditionally. As a distinct labeled property it is pure restatement.
**Required**: Either fold S9 into S0's prose as "the named consequence," or justify what formal content the antecedent restriction adds. As written it is a redundant property.

### Issue 4: S1's T8 relationship is stated twice (duplication)
**ASN-0036, S1**: Before the proof — "It is the content-store specialisation of T8 (allocation permanence, ASN-0034): T8 guarantees that allocated addresses persist ...; S1 ensures that the content ... persists as well." After the proof — "it specialises T8 ... from the abstract address space to the content store. T8 guarantees `allocated(s) ⊆ allocated(s')` ...; S1 guarantees `dom(Σ.C) ⊆ dom(Σ'.C)` ...".
**Problem**: The same T8-vs-S1 scoping point is made twice in different words, on either side of a one-line proof. Two paragraphs saying the same thing.
**Required**: Keep one. Delete the other.

### Issue 5: "S0-persistence bridge" is a forward-reference deferral repeated across six contracts
**ASN-0036, S0-persistence bridge**: "We cite this as the *S0-persistence bridge* in the contracts below rather than restating it." It is then cited identically in S7a, S7b, S7c, S7d, ShiftPreservation, and S7 ("S0 (content immutability) — the S0-persistence bridge (above)").
**Problem**: This is the multiple-paragraphs-defer-to-one-location accretion pattern. The "bridge" content reduces to "S0 fixes `a`'s identity, so any property established at allocation persists" — a single fact that each contract could cite as a plain S0 dependency.
**Required**: Drop the named "bridge" device; have each contract cite S0 directly. If the persistence step is non-obvious anywhere, state it once at S7's preamble, not as a recurring forward-reference label.

### Issue 6: S7a's `zeros(a) ≥ 2` conditioning is dead weight, discharged immediately by S7b
**ASN-0036, S7a**: the axiom is conditioned `a ∈ dom(Σ.C) ∧ zeros(a) ≥ 2`, and its Depends entry explains that "S7b ... universally discharges S7a's `zeros(a) ≥ 2` conditioning by supplying the strictly stronger `zeros(a) = 3 ≥ 2` for every `a ∈ dom(Σ.C)`."
**Problem**: Since S7b (which holds for the same domain) already forces `zeros(a) = 3` for *all* `a ∈ dom(Σ.C)`, the conditioning in S7a is never not-satisfied. The conditioning plus the paragraph explaining how S7b removes it is a presentation-order artifact (reviser drift) — prose explaining why a clause is there rather than advancing the claim.
**Required**: State S7a unconditionally over `dom(Σ.C)` (justified by S7b), and delete the conditioning-and-discharge meta-prose.

### Issue 7: S8 existence proof and the worked example re-litigate the same "singleton vs displayed run" distinction
**ASN-0036, S8 existence proof**: "The singleton witness thus exercises `shift` only at `k = 0` ... We state this distinction once; the contract slots below cite their dependencies without re-litigating which `k` exercises them." **Worked example, Check S8**: re-states it at length — "The non-singleton form is admitted ... but is *not produced* by S8's existence proof ... The 'single run of length 5' form is the witness we choose to display here precisely because it exercises ShiftPreservation's `k ≥ 1` cases."
**Problem**: The proof explicitly promises to state the distinction "once," then the worked example states it again across a full paragraph (plus the *Non-canonicality* paragraph makes it a third time). This is the relocated-prior-finding accretion pattern.
**Required**: Keep the distinction in one place. In the worked example, verify the `k = 3` arithmetic and stop — do not re-explain existence-vs-display.

### Issue 8: S8a labels an axiomatic conjunct as "derived"
**ASN-0036, S8a**: The Definition says "The `zeros(v) = 0` and componentwise-positivity conjuncts of the postcondition are derived ..., not independently posited," and the proof says of `#v ≥ 2` "This is a design commitment for V-positions." Yet the contract line reads "*Postconditions (derived):* `(A v ... :: zeros(v) = 0 ∧ #v ≥ 2 ∧ ...)`" — labeling the whole conjunction, including the definitional `#v ≥ 2`, as derived.
**Problem**: `#v ≥ 2` is axiomatic by the section's own admission; bundling it under "Postconditions (derived)" mislabels what was proved versus posited.
**Required**: Split the postcondition: mark `#v ≥ 2` as definitional and `zeros(v) = 0`, componentwise positivity as derived.

### Issue 9: `#runs(d)` performance discussion is implementation essay in a structural slot
**ASN-0036, after S8**: "Gregory identifies the inner loop ... responsible for 40% of processing time ... A consolidation function ... was started ... and abandoned mid-expression — the function body stops with an incomplete conditional: `if(`."
**Problem**: The CPU-percentage and abandoned-`if(` anecdote describe implementation performance characteristics, not a state property, operation, or invariant of the strand model. It does not advance the span-decomposition argument.
**Required**: Trim to the one load-bearing sentence (run count drives translation cost, so any implementation must consolidate or pay for fragmentation) and drop the performance/anecdote detail.

## OUT_OF_SCOPE

### Topic 1: Subspace alignment `subspace(v) = subspace_I(M(d)(v))`
**Why out of scope**: Already correctly identified as an operations-layer obligation and posed as an Open Question; not an error in this ASN.

### Topic 2: Link-subspace (S = 2) contiguity semantics
**Why out of scope**: The ASN explicitly binds D-CTG/D-MIN/D-SEQ to the text subspace and defers link-subspace tombstone semantics to a future ASN. Correct scoping.

VERDICT: REVISE
