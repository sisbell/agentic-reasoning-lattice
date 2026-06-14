# Review of ASN-0134

This is a careful, self-aware note. I checked the load-bearing proofs and they hold: A4's no-torn-step disjunction (the excluded middle is denied by A0); H0's frontier case-split (the `(d',S')≠(d,S)` analysis correctly covers the cross-subspace pair via the `origin=d` filter alone); H1's commutation across *both* axes (origin for `d≠d'`, subspace anchors for `d=d'`, correctly noting `CrossDocumentDisjointness`'s single-`·` statement does not name the cross-document cross-subspace case); H2's boundary case (first-emission collision on `[d.0.S.1]` handled alongside the interior); H3's distinction between disjoint-write (a) and distinct-element non-interference (b); G1(i)'s discipline of securing validity/reachability *before* invoking A6; W3's "collision, never a hole" argument; and §8's V2 strict-implication chain with both converse-failure witnesses. G2 is a genuinely sharp self-catch (the literal vs operative reading of I1a's `K`-surface-emittedness). The note is not META — MIC is a contract abstracted from mechanism, SAFE derives state invariants any faithful realization must meet; this is specification territory.

The findings below are the residue the `anti-bloat` classifier asks for, plus one scope boundary.

## REVISE

### Issue 1: The "clause 7 is the one non-per-home operation-level clause" classification is restated at four sites

**ASN-0134, §9 (clause 7 body, post-MIC paragraph, claims table) + §4**: The taxonomic placement of clause 7 — non-per-home, per-coverage-class, operation-level, role-distinct from 2/5/6 — appears near-verbatim three+ times:
- clause 7 body: "this is a **non-per-home**, *per-coverage-class* serialization: orthogonal to clause 2 ..., and the one *operation*-level guarantee that resists the per-home thesis — *role*-distinct from the allocation clauses 2/5 and the reader-side clause 6."
- post-MIC paragraph: "Clauses 6 ... and 7 ... are the contract's only non-per-home obligations, both reader- and operation-level rather than allocation disciplines"
- claims table (MIC row): "clause 7 ... is the one non-per-home operation-level clause, alongside the reader-side clause 6"

**Problem**: The post-MIC paragraph and the table row carry no information the clause-7 body does not. This is meta-prose about a clause's classification, not its content — the precise reader re-reads the same "role-distinct, non-per-home" sentence three times.

**Required**: State the classification once (in clause 7's body, where it belongs). The post-MIC paragraph should either be deleted or reduced to the one non-redundant thing it adds; the table row should state what clause 7 *requires*, not re-rank it.

### Issue 2: The shared-frontier / collision-free conditional is re-derived in full at five sites

**ASN-0134, §4 (multiple paragraphs), H3, the post-H3 lift paragraph, MIC clause 2, SAFE(c)**: The case-split "on a shared-frontier realization X; on a collision-free scheme Y" is spelled out in full repeatedly — §4 para 3 ("two such bracket the design"), §4 para 4 ("the rejection bites; ... it never fires"), §4 para 5, H3 statement + proof, then the post-H3 paragraph re-derives it inside both "(i) Validity" and "(ii) Confluence," then MIC clause 2 ("discharges this sub-clause vacuously"), then SAFE(c) ("a collision-free document scheme has no such failure mode").

**Problem**: The conditional is genuinely load-bearing, but its full two-branch form is not needed at every consumer. The post-H3 lift paragraph in particular re-proves validity and confluence that H3 (commutation) and G1 (the linearization theorem) already establish — the only new content is the *combination*, which a single sentence ("H3 supplies the missing commutation; G1 then extends verbatim, the `≺`-incomparable kinds now three") delivers. MIC clause 2 and SAFE(c) re-spell the dichotomy a reader has by then seen four times.

**Required**: Derive the conditional once (§4 + H3). The post-H3 paragraph should reference rather than re-derive; MIC clause 2 and SAFE(c) should cite "(§4, account-tier of clause 2)" instead of restating both branches.

### Issue 3: A6's per-state package presents as exhaustive but isn't, and the enumeration does not carry the claim

**ASN-0134, A6**: "satisfies the *per-state canonicity package* ... *every* invariant of the stack that is a predicate of a single state ... The package conjoins [long list]," followed by the parenthetical "(shape- and idem-stability `P2`/`R2` are, by contrast, mere *corollaries* ... not conjuncts the package must carry)."

**Problem**: A6's own closing sentence concedes the real proof — "Every conjunct and the transition clause alike rest on one reachability base ... on which the foundations' transfer lemmas carry every cited invariant." Reachability (`B2`/`RP-a`/`RP-b`) carries *every* foundation invariant whether named or not, so the enumeration does no work in the argument; it is a use-site inventory in a structural slot. Two symptoms follow. (a) The "*every* invariant ... that is a predicate of a single state" framing overpromises: the list includes single-state *lemmas* (`ChainMembershipForOrigin`, `L-ContiguousPrefix`) yet omits another single-state lemma of the same character — ASN-0086's `R0a` (FlatLinkDomain, `dom(Σ.L)` a prefix-antichain). Either the criterion admits single-state lemmas (then `R0a` belongs) or it does not (then the chain-contiguity lemmas do not). (b) The `P2`/`R2` "mere corollaries ... not conjuncts the package must carry" aside defends a non-inclusion no reader would contest.

**Required**: State the canonicity claim as what it is — "reachable ⟹ every stack invariant holds, by the transfer lemmas" — cite a few representative members for §2's "nothing is marked mid-batch" point, and drop both the exhaustive-list framing and the `P2`/`R2` parenthetical.

## OUT_OF_SCOPE

### Topic 1: Arrangement-layer (POOM) concurrency

**Why out of scope**: §1 commits `𝔼` to "ASN-0093's allocation model carried up through ASN-0086/0126/0128," and §4 fixes an *allocation step* as "a K.α or a K.λ_sh." On that stack `M2` holds (`M(d)=∅`); ASN-0047's arrangement operations — `K.μ⁺`/`K.μ⁻`/`K.μ~`, which populate, contract, and reorder a document's POOM `M(d)` — never appear. So the isolation model deliberately excludes a same-document conflict class distinct from allocation frontiers (two agents reordering one document's arrangement) and the one non-monotonic operation in the broader system (`K.μ⁻`'s contraction, which W0's monotonicity does not cover). This is correctly excluded by the stack choice, not an error — but "the home is the unit of contention" and the monotonicity partition (§5) are claims about the *allocation* substrate, and a future note must extend the model to the arrangement layer. One line in "What this note does not cover" naming this exclusion would prevent a reader from over-reading the per-home thesis as covering POOM edits.

VERDICT: REVISE
