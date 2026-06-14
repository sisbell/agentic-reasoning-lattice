# Review of ASN-0134

This is a careful, technically sound note. I checked the load-bearing proofs — the commutation lemmas (H0/H1/H2), the confluence theorem (G1) and its lift to `K.σ` (H3), the two order-dependence families (G2 + instances i/ii + the target-residence race), the verdict strict-implication chain (V0/V2/V1), and the safety theorem (SAFE) with its minimality argument. The genuinely novel results — per-home suffices for writers while clause 6 (reads) and clause 7 (idem dedup) require global discipline — are correctly established. I confirmed the worked traces in §7 and §8 compute as claimed, including the boundary cases (first-emission collision, `m=0`/`m=1` degenerate batches, empty-slice `stale`).

In particular I want to record that the target-residence-race argument in §4 is correct and *not* the error it first looks like: `P-tgt` is an operation-surface rejecting precondition, not a `K.λ_sh` step precondition, so the raw two-step set `{A, B}` genuinely commutes (a born nullified either way, H1) while the operation-level *rejection* is the order-dependent fact. The note's distinction between raw-step confluence and operation-level realization holds.

The findings below are accretion (the directed focus) plus one labeling defect.

## REVISE

### Issue 1: §4 opening previews and duplicates the H3 conditional-`K.σ` rationale

**ASN-0134, §4 (second opening paragraph)**: "The one fact the frontier theory needs in advance is why that carry-over is conditional. The committed stack specifies K.σ by bare freshness-by-test ... and carries no document-allocator-conformance invariant ... Whether K.σ instead behaves as a per-home allocation against a shared per-account frontier is a property of the realization, not of 𝔼; we defer that treatment ... to H3."

**Problem**: This whole paragraph is a "why it's conditional" preamble that defers to H3 — and the post-G1 H3 treatment then restates the identical point: *"Neither is forced by the committed stack: `A_doc` is ASN-0047's allocator over an entity set E that 𝔼's K.σ does not carry ... which is exactly why the dependence is conditional rather than a theorem of 𝔼."* Same content (the committed stack carries no `A_doc`-conformance over E, so `K.σ`'s frontier status is realization-conditional), in two places, with an explicit defer-to-downstream between them. This is exactly the forward-reference-accretion pattern: a defer-then-repeat preamble whose prose explains *why the conditional treatment is needed* rather than advancing it, fully duplicated at its target.

**Required**: Collapse the §4 opening's second paragraph to a one-line scoping pointer (e.g., "`K.σ`'s frontier status is realization-conditional; established as the account-tier corollary in H3"), and keep the rationale only at H3 (or vice versa). The first opening paragraph's definition of "allocation step" should stay.

### Issue 2: A6's representative invariant list uses labels overloaded across the note's own foundations

**ASN-0134, A6 (Claims table row)**: "every per-state stack invariant holds at it (representative: SD/L0, P6, chain-contiguity, registry-fixity)"

**Problem**: Both `SD` and `P6` are overloaded within this note's foundation set, and one reading of `P6` names an invariant the substrate `𝔼` provably cannot satisfy.

- `P6` is **ExistentialCoherence** (ASN-0047): `(A a ∈ dom(C) :: origin(a) ∈ E_doc)` — over the *entity set* `E_doc`. It is also **ReachableConformance** (ASN-0126), a genuine `→_sh`-stack per-state invariant. Only the latter applies: the note repeatedly stresses that `𝔼` is built on the ASN-0093→0086→0126→0128 stack, whose document set is `dom(M)`, and that this stack carries no `E` ("an entity set E that 𝔼's K.σ does not carry"). If `P6` reads as ASN-0047's, the representative list cites a non-stack invariant; the stack's existential-coherence analogue is ASN-0093's **C2** (`origin(a) ∈ dom(M)`), not `P6`.
- `SD` is **StoreDisjointness** (ASN-0093, the intended per-state invariant) but also **SurfaceDiscipline** (ASN-0128, a derivation predicate, not a per-state invariant).

The note is otherwise scrupulous about qualifying labels ("ASN-0093's M1", "ASN-0047's A_doc", "ASN-0093's M1 (document-set monotonicity)"), so the bare `SD`/`P6` here is an inconsistency in its own discipline — and a reader cannot tell which claim is meant.

**Required**: Disambiguate by name and ASN (e.g., "P6 ReachableConformance (ASN-0126)", "SD StoreDisjointness (ASN-0093)"), and confirm the intended `P6` is ASN-0126's, not ASN-0047's. If existential coherence over `dom(M)` was intended, cite `C2`.

### Issue 3: Section-closing paragraphs recap results their sections already establish

**ASN-0134, §8 (closing paragraph)**: "The substrate's contribution is exactly and only the snapshot: a single canonical state, read atomically ... Whether a verdict so obtained licenses terminating the system is the separate, conditional question a termination layer answers ..."

**Problem**: The soundness-vs-durability distinction is stated three times in §8 — V1's formal claim ("a verdict ... is retrospective ... durability requires an additional hypothesis the substrate does not supply"), the two "Soundness"/"Durability" bullets immediately after it (which are the precise formalization), and then this closing recap. The closing duplicates the Soundness bullet's "the verdict is a true statement about Σ_r, full stop" and the Durability bullet's "a relationship the substrate cannot certify," adding only the "reached-and-held referent" phrase. The same pattern appears at the end of §4 ("The honest statement is therefore two-level ... each instance's own analysis has already settled ...") — an explicit-back-reference recap of the two-families result the instances just proved, adding only the taxonomic-closure sentence. These closers compound the meta-prose the anti-bloat pass targets.

**Required**: Trim each closer to its genuinely new content — keep the taxonomic-closure sentence in §4 and the termination-layer hand-off in §8, but drop the restatements the V1 bullets and the §4 instances already carry.

## OUT_OF_SCOPE

None to add. The "What this note does not cover" section and the Open Questions delimit deferred territory (cross-server replication, batch reader-atomicity, the concrete primitives realizing each clause) cleanly and by descriptive role rather than ASN number, so they neither overreach nor create non-foundation cross-references.

VERDICT: REVISE
