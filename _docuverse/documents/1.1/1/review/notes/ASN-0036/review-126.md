# Review of ASN-0036

## REVISE

### Issue 1: S8 image-structure-preservation corollary is orphaned from the theorem it sits in

**ASN-0036, S8 Postconditions**: "(*Corollary (image structure-preservation).*) For every `a ∈ ran(M(d))` and every `k ≥ 1`, the shifted image `shift(a, k)` preserves the structural properties of `a`... The fact holds on `dom(Σ.C)` independently of any run cardinality."

**Problem**: The S8 existence proof constructs only the singleton decomposition, where every `nⱼ = 1` and conjunct (b) is exercised solely at `k = 0`. A shift by `k ≥ 1` *within a run* never occurs in the structure the theorem actually builds. The corollary is, by its own admission, just ShiftPreservation composed with S3 (`ran(M(d)) ⊆ dom(Σ.C)`) — it is "independent of any run cardinality." Attaching a property about multi-element-run shifts to a theorem that proves only singleton existence is scope drift: it states a guarantee about a structure (coalesced runs) that the ASN explicitly defers to an open question.

**Required**: Either remove the corollary from S8 and state it as a standalone consequence of ShiftPreservation + S3, or move it to the deferred coalescing work. Do not present it as a postcondition of the singleton-existence theorem.

### Issue 2: "Why the axiom is needed" prose inside Depends fields

**ASN-0036, S7b Depends**: "T10a.4 bounds `zeros ≤ 3`, and this axiom is the strict-equality strengthening that pins down `zeros(a) = 3` for content-bearing addresses."

**Problem**: This explains *why* S7b exists relative to T10a.4 rather than stating *what* it depends on. It is exactly the reviser-drift pattern flagged for this cycle (new prose around an axiom justifying its necessity). The Depends slot should name the dependency and its use, not argue for the axiom's existence.

**Required**: Reduce to the dependency relation (T10a.4 supplies surrounding T4-validity bounded `zeros ≤ 3`; S7b strengthens to equality). Drop the justification clause.

### Issue 3: D-CTG-depth non-triviality bound explained twice in different words

**ASN-0036, D-CTG-depth proof**: "`m ≥ 3` (the lemma's non-triviality bound, supplied as an additional precondition rather than by S8-depth — S8-depth on its own guarantees only `m ≥ 2`, inherited from S8a)."
**ASN-0036, D-CTG-depth Formal Contract Preconditions**: "`m ≥ 3` (the lemma's non-triviality bound, additional to S8-depth — at `m = 2` the conclusion holds vacuously since the range of shared components 2 through `m − 1` is empty)."

**Problem**: Two paragraphs in the same property say the same thing — "`m ≥ 3` is an extra precondition, not from S8-depth, and `m = 2` is vacuous" — in different words. Redundant meta-prose about precondition provenance.

**Required**: State the `m ≥ 3` precondition once (with the `m = 2`-vacuous note), in the contract. Strip the parenthetical from the proof opening.

### Issue 4: S8a proof is meta-commentary on what counts as a derivation

**ASN-0036, S8a proof**: "The depth `#v ≥ 2` and the field-separator-free property `zeros(v) = 0` are definitional... Only componentwise positivity requires a derivation... this is a restatement of the 'isolated element field' commitment, not a derivation from prior axioms."

**Problem**: The "proof" spends most of its length narrating which conjuncts are definitional versus derived, rather than deriving. The single load-bearing step (positivity from `zeros = 0` + ℕ-carrier) is one line; the surrounding paragraphs are commentary classifying the other conjuncts as definitional. This is essay content in a proof slot.

**Required**: Collapse to: V-positions are isolated element fields (so `zeros(v) = 0`, `#v ≥ 2` by definition); positivity follows from `zeros(v) = 0` and T0/NAT-discrete. One short paragraph.

### Issue 5: ShiftPreservation conclusion (i) over-narrates "nonzero ⇒ ≥ 1"

**ASN-0036, ShiftPreservation, Conclusion (i)**: "since `0` is the least element of T0's carrier ℕ we have `0 ≤ a_{#a}`, and NAT-discrete at `m = 0` (`0 ≤ n < 0 + 1 ⟹ n = 0`) contrapositively excludes `a_{#a} < 1`, so NAT-order's trichotomy on `(a_{#a}, 1)` leaves `a_{#a} ≥ 1`."

**Problem**: Four cited axioms to conclude a nonzero natural is `≥ 1`. The same one-liner is re-derived in the S8 within-subspace lemma and in D-SEQ. The repeated multi-axiom expansion of an elementary ℕ fact is accretion, not rigor — it forces the reader to re-parse the same trivial chain at every occurrence.

**Required**: Establish "for `n ∈ ℕ`, `n ≠ 0 ⟹ n ≥ 1`" once (it is already implicit in T4/T0 usage elsewhere) and cite it by name thereafter, rather than re-expanding the trichotomy/discreteness chain at each site.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG, D-MIN, subspace alignment

The open questions correctly defer whether DELETE/INSERT/COPY/REARRANGE preserve D-CTG/D-MIN, what the displacement mechanism must guarantee, and the subspace-alignment obligation `subspace(v) = subspace_I(M(d)(v))`. These are operation frame/postcondition concerns, not state invariants of the strand model. Properly out of scope — no error.

### Topic 2: Unique maximal (coalesced) run decomposition

S8 proves only singleton existence; whether arrangements admit a unique minimal-count decomposition is deferred to an open question. Correctly scoped — the coalescing theorem belongs in a future ASN.

VERDICT: REVISE
