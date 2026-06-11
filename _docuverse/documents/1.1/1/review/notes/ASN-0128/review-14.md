# Review of ASN-0128

## REVISE

### Issue 1: The exposed surface's input type contradicts AD's encoding claim
**ASN-0128, Idem operational semantics ("The exposed signature") vs. Denotation and views (AD)**: "`Emit_K : Σ × T × Endset × Endset ⇀ Σ' × A_rel^{Σ'}`, a partial operation with three outcomes" — versus — "The operation surface speaks addresses: `Emit_K` and `Nullify_Binary` present F and G as finite address sets, encoded one canonical span per address — so every surface-emitted endset is address-denoting by construction."

**Problem**: These are two incompatible descriptions of the same surface. If `Endset × Endset` is the caller-facing domain, arbitrary endsets — non-unit-depth spans included — are presentable at the surface, and AD's "address-denoting by construction" is false. That single claim is load-bearing: it carries AD's verdict that nonconforming tuples are "reachable only off-surface (raw `K.λ_sh`)", BH3's attribution of the non-denoting-G ⊥-case to raw bypass, and I1's irredundant-presentation discussion. If instead the surface domain is `℘_fin(T) × ℘_fin(T)` with canonical encoding (which "The operation set" paragraph also asserts: "endsets presented as address sets, AD"), then the displayed signature is wrong. A secondary symptom of the same confusion: I6's uniform `pre` lists "arity 3" as a checked precondition, while ASN-0126's WP explicitly discharges precondition (0) by construction with no wp conjunct — under an address-set surface that builds the triple itself, arity 3 cannot fail and should not appear as a checkable clause.

**Required**: Pick one normative caller-facing domain and state the signature in it. If the surface takes address sets, restate the signature over `℘_fin(T) × ℘_fin(T)`, let AD's encoding be the definition of how those sets become endsets, and drop the vacuous arity conjunct from I6's `pre`. If the surface genuinely accepts arbitrary endsets, rewrite AD's "by construction" claim, the nonconforming-tuple verdict, and every downstream use of "surface-emitted endsets are address-denoting."

### Issue 2: Three of "the four [R] configurations" are discussed; Multi is silently dropped
**ASN-0128, Standard registrations (S3)**: "Binary is a *choice* among the four [R] configurations ASN-0126 sweeps: unregistered [R] gives an audit-only substrate where no `Emit_R` has a `→_sh` image, and Unary [R] forces `G = ∅`, emptying every retraction's to-coverage — retraction-inert. Shipping Binary selects the one configuration where retraction is expressible..."

**Problem**: Four configurations are announced; two are eliminated; Binary is then declared "the one configuration where retraction is expressible." Multi [R] is never examined — and under Multi, the wrapper's `|F| = 1`, `|G| = 1` emission passes `Sh-conf` (`|G| < ∞`), so retraction is perfectly expressible under a Multi registration. The uniqueness claim is false as written. The real ground for Binary appears to be *containment*, not expressibility: Binary's gate forces single-span to-endsets even on raw off-surface deposits — exactly the form ASN-0126's P6 records and RangeSterilization's hypothesis relies on — whereas Multi would admit range-valued to-endsets through the gate.

**Required**: Either eliminate Multi explicitly (the containment argument is available and one sentence long), or weaken "the one configuration where retraction is expressible" to the claim the text actually supports.

### Issue 3: BH1's informal Effect overstates the committed rewrite; the filtered-argument boundary is unpinned
**ASN-0128, BH1 (Effect) and S1**: "Addresses carrying an active tuple of this type are excluded from the default view of enumeration queries on every other registered type." / S1: "Marks an address as lifecycle-retired: the default view on every other type excludes it."

**Problem**: The rewrite-scope equations filter only *result* sets — filtered sources are subtracted from `members(K')`, filtered targets from `targets_of(x)`'s result. Nothing touches arguments: a filtered (retired) source `x` still answers default-view `targets_of(x)` with its full target set (minus filtered targets). So the retired address has not "vanished from default queries" — it is fully forward-queryable as an argument, and `members(K')` for some `K'` may be empty of it while `targets_of(x)` is not. The Effect sentence and S1's gloss claim more than the equations commit. This is the committed default surface, not the BH2/BH3 interaction Open question 1 defers, so it must be pinned here.

**Required**: One sentence fixing the filtered-argument case — either "the rewrite is result-side only; a filtered address remains valid as a `targets_of` argument in the default view" (matching the equations) or a chosen exclusion — and align the Effect and S1 glosses to it.

### Issue 4: AM misstates `stale`'s argument
**ASN-0128, Denotation and views (AM)**: "(`members` takes no address argument; BH4's `age` and `stale` take exact chain addresses and match no endset at all.)"

**Problem**: `stale(h)` takes an ordinal horizon `h ∈ ℕ`, not a chain address — BH4's own signature is "`stale(h) → set of event-addrs` ... for an ordinal horizon `h ∈ ℕ`". Only `age(a)` takes an address.

**Required**: Correct the parenthetical (e.g., "`age` takes an exact chain address; `stale` takes an ordinal horizon; neither matches an endset").

### Issue 5: Forward-deferral accretion to AD and DR
**ASN-0128, throughout the idem section and earlier**: I0 ("`addrs` per AD, Denotation and views"), I0a (built entirely on AD's vocabulary), and I1 ("AD, Denotation and views") all lean on a section defined two sections later. "(DR, Standard registrations)" is forward-cited from the commitments list, RP-c, I4, I6's disciplined-domain reduction, and the example's born-nullified case — five-plus references from different sections to one downstream derivation, with I6's reduction substantively *depending* on "DR's derivation" a section before DR exists.

**Problem**: This is the flagged accretion pattern: multiple paragraphs in different sections deferring to the same downstream location. The reader of I0–I6 must hold two unproved machines (AD's denotation regime, DR's discipline argument) on credit to follow the contracts.

**Required**: Reorder — "Denotation and views" before the idem section (I0a is natively an AD lemma), and the surface-discipline definition plus DR before I4/I6 — or consolidate the forward references to a single explicit forward pointer each.

### Issue 6: Defensive authority-appeal prose around already-specified contracts
**ASN-0128, I0, I1**: I0's closing — "The authorities draw the line in the same place: Gregory's store preserves each link's span decomposition verbatim yet decides every match by I-address intersection, and Nelson's equivalence among links is computed at query time, never stored as identity (I1)." I1's home-validation — "Validate-where-read is the implementation's discipline as well: Gregory's back end never validates a request's document argument as an unconditional entry check..." I1's closing paragraph — "And it is Nelson's architecture: the back end never merges links — ... A dedup hit creates nothing and merges nothing; `idem = ⊤` is exactly such a computed equivalence, located at the operation surface, with the substrate beneath it pluralistic."

**Problem**: Each of these defends a choice the contract has already fully specified; none adds a constraint, a case, or a derivation step. This is justification addressed to a skeptical reviewer, not specification — the anti-bloat pattern of prose explaining why the rule is right rather than what it says. (Contrast BH2's cyclic-topology evidence and BH4's no-wall-clock evidence, which *pin semantics* — general digraph, ordinal time — and should stay.)

**Required**: Trim the three quoted passages or compress each to a one-clause provenance note.

### Issue 7: The operation surface is stated three times
**ASN-0128, "The exposed signature" (idem section), "The operation set" (end of Standard registrations), and the final commitments bullet**: The signature paragraph restates I1's and I5's branch semantics ("once for both idem values"); "The operation set" states the surface again; the commitments bullet pre-narrates DR's result ("restoring the disciplined-domain wp simplification ASN-0126 had to abandon as layer-scoped (DR, Standard registrations)") before any of the machinery exists.

**Problem**: Same content in different words across three sections — home validation alone is specified in I1, restated in I5, and restated again in the signature paragraph. The commitments bullet's accomplishment inventory is the "essay content in structural slots" pattern.

**Required**: Make the signature paragraph the one normative statement of the surface; reduce "The operation set" to a pointer; cut the commitments bullet's nested DR narrative to its bare commitment.

## OUT_OF_SCOPE

### Topic 1: The serializing authority behind I4
**Why out of scope**: I4 correctly inherits the sequential interleaved relation and notes that "a serializing authority orders the two calls before either becomes a step" — but what that authority is, and what fairness or ordering guarantees it provides, is a concurrency model this note rightly does not open. A future ASN, not an error here.

### Topic 2: Rejection observability
**Why out of scope**: "No step, no address" fixes the state-side semantics of every rejection, but whether a caller can distinguish a gate failure from an invalid-`d` rejection from a P-tgt rejection is an error-surface question — new operational territory, not a gap in the contracts given.

### Topic 3: Σ_init construction and multi-app merge
**Why out of scope**: R-VAL fixes the verdict semantics of construction-time validation; the protocol that assembles competing declarations into one passing registry is the note's own Open question 8 and is properly deferred.

VERDICT: REVISE
