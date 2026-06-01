# Review of ASN-0086

## REVISE

### Issue 1: `at-most-one-key-per-home` is load-bearing for L-ContiguousPrefix/R0a but is not part of the substrate-conforming-state definition

**ASN-0086, Definition — substrate-conforming state**: clause (b) reads "emit the fresh link keys homed at each document as the next *contiguous chain segment* past that home's current sibling frontier," then narrows to "if a step adds a fresh key at home `d` ... that key occupies exactly chain index `J+1`." Separately: "A separate, auxiliary commitment of this note's vocabulary is the **at-most-one-key-per-home discipline**."

**Problem**: The substrate-conforming *state* is defined as reachable by transitions satisfying clauses (a) and (b) only; at-most-one is described as "separate, auxiliary." But L-ContiguousPrefix's proof cites it as if it were part of that definition: "By the at-most-one-key-per-home discipline (**auxiliary commitment, Definition — substrate-conforming state**), fix a home `d`." R0a Case 2 and the WP derivation then depend on L-ContiguousPrefix, so the entire antichain result inherits this unlicensed premise.

The note itself concedes clause (b) is incoherent without at-most-one: "the at-most-one commitment is precisely what guarantees a single step deposits at most one fresh key per home — making 'extends the prefix by one chain index' coherent rather than ambiguous." Clause (b) is also internally inconsistent — "next *contiguous chain segment*" (plural, admits a batch) versus "that key occupies exactly chain index `J+1`" (singular). A literal reader cannot tell whether a single conforming transition may deposit a contiguous batch `J+1..J+m` at one home.

By contrast, R7a correctly routes at-most-one through the *layer* definition (whose hypothesis "issued by a substrate-conforming layer" does bundle it). The mismatch is only on the state route, which L-ContiguousPrefix uses.

**Required**: Fold the at-most-one constraint into the substrate-conforming-*state* definition (or into clause (b) itself), and reword clause (b) to a single-key landing so "contiguous chain segment" and "occupies exactly `J+1`" stop contradicting each other. Then L-ContiguousPrefix may legitimately invoke it.

### Issue 2: Defensive meta-prose around the substrate-conforming definitions (anti-bloat)

**ASN-0086, Definition — substrate-conforming state**: "It is a genuine restriction, not a derived fact: a transition may deposit a single fresh key at a home ... yet land it off the sibling frontier ... so frontier-landing must be imposed separately." and "The two commitments are independent: at-most-one bounds *how many* keys a step adds per home, while frontier-landing fixes *where* an added key lands."

**Problem**: This is prose explaining *why* the constraint is needed and arguing for its independence, not stating *what* it requires — exactly the "explains why the axiom is needed rather than what it says" pattern the anti-bloat classifier flags. A reader following the definition must skip past two justificatory sentences to reach the actual constraint. (Tightening the definition per Issue 1 would also retire most of this prose.)

**Required**: State the two constraints as definitional clauses; drop the independence essay and the "genuine restriction, not a derived fact" defense.

### Issue 3: Repeated downstream deferral to the Weakest-Precondition Analysis (anti-bloat)

**ASN-0086**: Definition — Unit-depth retraction discipline: "The mechanism ... is analyzed in the Weakest-Precondition Analysis (*Substrate-conformance alone is insufficient*)." Open Questions: "(Definition, Three Operations; bypass mechanism analyzed in the Weakest-Precondition Analysis)."

**Problem**: Two sections in different parts of the note point forward to the same WP paragraph for the same crafted-span bypass mechanism. Per anti-bloat: "multiple paragraphs in different sections defer to the same downstream location."

**Required**: Keep the analysis at its single home (WP) and remove the redundant forward pointers; a one-clause statement of the discipline's enforcement boundary suffices at each definition site.

## OUT_OF_SCOPE

### Topic 1: L-ContiguousPrefix's relationship to ASN-0093 ChainMembershipForOrigin
L-ContiguousPrefix restates ASN-0093's ChainMembershipForOrigin (contiguous-initial-segment of `A_L(d)`) but over the broader substrate-conforming domain rather than `→*`-reachable states. The re-derivation is justified by the wider domain, so it is not pure reinvention. A one-line note citing the foundation lemma and stating "we extend it from `→*`-reachable to substrate-conforming states" would improve clarity, but the extension itself is legitimate and belongs to this ASN, not a future one.

### Topic 2: Concurrency / atomicity model for Observe vs. Emit
The Open Questions raise atomicity of Emit relative to concurrent Observe and the consistency model under which `A_K` transitions are observed. This is genuinely new territory — the present ASN's transition relation is sequential (SequentialAtomicTransitions, ASN-0093) — and belongs in a future note.

VERDICT: REVISE
