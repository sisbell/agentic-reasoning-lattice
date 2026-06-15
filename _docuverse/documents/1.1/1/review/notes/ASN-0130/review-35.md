# Review of ASN-0130

## REVISE

### Issue 1: register_pred's multi-read validation cites the wrong ASN-0134 consistency clause

**ASN-0130, PR0 (and PR5a, "exactly as PR0")**: "so validation is the operation's own gate evaluated against its one committed pre-state Σ (SnapshotRead A3; MIC clauses 1 and 4, ASN-0134), the idem-⊤ dedup-read-and-deposit atomic per coverage class (MIC clause 7)."

**Problem**: `register_pred`'s validation is a *multi*-bounded-access read. It reads at least two distinct link-store slices: the `pdef` **audit** slice for ever-registration in (iii) (`sig(r)` definedness), and the `pdef` **active** slice `A_pdef` for (iv), which is `L_pdef ∖ nullified` and so additionally reads `L_R`. ASN-0134's MIC clause 4 (V0) covers only *single*-bounded-access reads and explicitly routes multi-access reads elsewhere: "The several-access reads — cross-type joins and `stale` — are clause 6's, not this clause's." A multi-read verdict needs MIC clause 6 (V2, per-verdict reader snapshot) to pin all constituents to *one* committed index; clause 4 guarantees only that each read individually lands on *some* committed state, not that they share one — which is exactly what "one coherent pre-state Σ" asserts. The note already cites clause 6 correctly for the structurally identical multi-slice lint read in PR5 ("a multi-slice read over `A_pdef` and `A_pd_stable`, sound only as a statement about the single committed state its constituent reads are pinned to (VerdictReaderSnapshot V2 / MIC clause 6)"), so the `register_pred` citation is internally inconsistent.

**Required**: Either (A) cite MIC clause 6 for the validation (as the lint does), since pinning all constituent reads to one index is what the "one coherent pre-state" claim requires; or (B) relax the claim and argue that (i)–(iii) are individually order-insensitive (content residence/values monotone by C0/S0; ever-registration and `sig` permanent), so the *only* order-sensitive read is (iv)'s active-slice check, whose staleness is benign — PR2 needs only that referents registered *earlier* (which an earlier active read still witnesses) and PR3 evaluation keys on ever-registration. Under (B) clause 4 + monotonicity suffice, but then the "one coherent pre-state" phrasing must be softened. As written, clause 4 justifies neither.

### Issue 2: The adversary check (worked composition, step 5) attributes the frontier-ghost rejection to the wrong condition

**ASN-0130, Worked composition, step 5**: "A registration whose term references `d_b`'s current content frontier `a₃` — unallocated, the next slot its chain would fill — is rejected at condition (iv) — no active tuple denotes `a₃` ... a resident, parse-valid, unregistered run still fails (iv)."

**Problem**: `a₃` is *unallocated*, hence never content, hence never-registered. PR0 (iii) states explicitly: "a never-registered referent leaves `sig(r)` undefined — hence no typing judgment, and (iii) fails there." Since the checks run in order (iii before iv), a definitional reference to never-registered `a₃` fails at **(iii)** (sig undefined), and execution never reaches (iv). The generalization "a resident, parse-valid, *unregistered* run still fails (iv)" is wrong for the same reason: an unregistered (never-registered) run has `sig` undefined and fails (iii). (iv) is the operative gate *only* for ever-registered-but-de-registered referents — precisely the distinction PR0 itself draws: "a de-registered referent types at (iii) yet is rejected at (iv)." The example conflates the frontier-ghost / never-registered case (closed by iii) with the de-registered case (closed by iv), and so contradicts PR0.

**Required**: Attribute the unallocated/never-registered frontier-ghost rejection to (iii) (`sig` undefined), and reserve (iv) for the resident, ever-registered-but-de-registered case; or replace the adversary's `a₃` with a de-registered referent if the intent is to illustrate (iv). The conclusion ("no definition can come to mean something by a later allocation") is correct; only the cited mechanism is wrong.

### Issue 3: Anti-bloat — discursive comparison in the worked composition's step-1 parenthetical

**ASN-0130, Worked composition, step 1**: "The abstract substrate is cleaner in a different respect — its link chain is disjoint from its content chain, where the implementation's same-subspace link allocation can split runs across separate insertions — but on intra-run contiguity under concurrency the two stand or fall together, each on the run's critical section."

**Problem**: The substantive content here (the abstract substrate's link/content chains are disjoint, so `d_b`'s link deposits cannot split the content run — H1/DisjointSubAllocatorChains) is relevant. The editorial wrapper ("cleaner in a different respect," "stand or fall together") is essay content that does not advance the registration the step is demonstrating; the reader must work past the comparison to recover the one relevant fact. Relatedly, the consistency-model reliance ("survives concurrent allocators by ASN-0134's consistency model, not by an assumption of serialized execution") is stated in PR0 and again near-verbatim in the "What this note doesn't cover" bullet — the bullet's enumeration of the four mechanisms largely restates what PR0 and this step already establish.

**Required**: Trim the comparative editorializing to the load-bearing fact (link/content chain disjointness keeps the run intact under concurrent link traffic). Consider reducing the doesn't-cover consistency bullet to a pointer rather than a re-enumeration.

## OUT_OF_SCOPE

### Topic 1: Access control on registration and de-registration
`register_pred` validates residence but imposes no ownership constraint (a run allocated under one document can be registered under another's home, and `idem = ⊤` makes registration first-home-wins), and de-registration is the shipped `Nullify_Binary`, whose `P0` admits *any* `d_retr ∈ dom(M)` as retractor — so any party can de-register any definition. PR1's permanence is audit-slice; active registration is withdrawable by anyone.
**Why out of scope**: Governance/ownership of definitions is new territory; the foundations' ownership ASNs are not among this note's dependencies, and the note's invariants correctly claim only audit-slice permanence.

### Topic 2: A validated supersession surface
PR4 reuses raw `supersedes` with no check that either endpoint is a registered definition, so `tip(a₁)` can resolve to a never-registered target.
**Why out of scope**: Deliberately deferred ("shipped semantics carry over without addition"); a validated `supersede_pred` checking both endpoints is a natural future class, not an error here.

VERDICT: REVISE
