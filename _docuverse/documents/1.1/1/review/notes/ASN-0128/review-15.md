# Review of ASN-0128

The technical core of this note is in good shape: I0a's minimal-elements proof is complete in both directions, I1a's induction covers every step kind including the wrapper-routed K ~ R case, DR's subtree/antichain argument for C3 is airtight (distinctness at the pre-state, R0a at the post-state), and the hit-branch re-establishment of the wrapper's guarantees at `Σ' = Σ` is done clause by clause rather than waved through. The wp analyses (I6, DR) are non-trivial and the necessity halves are argued honestly, including the subtle observation that DR's postcondition holds vacuously at a P0-rejected call and only the attainability convention makes P0 necessary. The remaining issues are one structural gap and two accretion findings.

## REVISE

### Issue 1: The extended-record transition relation is never defined, only implied

**ASN-0128, The registration record / I1**: "the transition relation `→_sh` is ASN-0126's, unchanged" (I1); "but the state space changed (registry values are now triples, not shapes); we cross the change as ASN-0126 crosses its own, with a projection and transfer clauses" (registration record).

**Problem**: The note asserts properties *of* `→_sh`-steps over extended-record states before any such relation exists: R1's proof is frame-based ("every step kind carries `Σ'.registry = Σ.registry` in its frame") — but those frames are clauses of a relation this note never states; RP(ii) quantifies over "each `→_sh` step over extended-record states," presupposing the relation; RP-c lifts steps into it. "ASN-0126's, unchanged" cannot be literally true — ASN-0126's `→_sh` is defined over states whose registry values are bare shapes, and the note itself concedes the state space changed. The actual definition (gate precondition (ii) reads the record's shape component; "K is registered" is key-side; each step kind's registry frame now frames the triple-valued registry) is fully determined, but the reader must assemble it from three scattered remarks in two sections. For a relation that every invariant, transfer lemma, and contract in the note quantifies over, definition by implication is not acceptable.

**Required**: One displayed definition, placed before R1 (which is the first claim to lean on the frames): the extended-record `→_sh` is `K.σ ∪ K.α ∪ K.λ_sh` with ASN-0126's step effects and preconditions, where `K.λ_sh`'s preconditions (i)/(ii) are read against the extended record (registration key-side, `Sh-conf` against the shape component) and each step kind's frame `Σ'.registry = Σ.registry` ranges over the extended registry. I1's "ASN-0126's, unchanged" should then cite that definition.

### Issue 2: "surface-disciplined" is defined twice, in different words

**ASN-0128, SD (Idem operational semantics) and S3 (Standard registrations)**: SD: "Call a substrate *surface-disciplined* when every tuple in `L_R^Σ` was deposited through this note's operation surface." S3: "Call a substrate *surface-disciplined* (SD's forward note, Idem operational semantics) when every tuple in `L_R^Σ` was deposited through this operation set — equivalently, every retraction is wrapper-routed …, and therefore … deposited with a P-tgt-valid target."

**Problem**: One term, two definitional sentences ("this note's operation surface" vs. "this operation set"), in two sections — the exact configuration in which definitions drift apart under future revision. S3 even cites SD and then re-defines rather than instantiates. DR's scope, I1a's application to R, and I6's disciplined-domain reduction all hang on this predicate; it must have exactly one defining occurrence.

**Required**: Define once. Either SD carries the definition and S3 opens with "On a surface-disciplined substrate (SD) — equivalently, since the `K ≁ R` precondition leaves the wrapper as the only surface route into `L_R`, every retraction wrapper-routed and hence P-tgt-valid —", or the definition moves wholly to S3 and SD reduces to the borrowed fact plus citation. The "equivalently" derivation is substantive and stays with whichever copy survives.

### Issue 3: Meta-prose accretion around forward references and repeated statements

**ASN-0128, multiple sections** — instances of the anti-bloat patterns this note is flagged for:

- **SD**: "The notion belongs to S3's retraction policy (Standard registrations), where DR derives the one fact this section borrows … I4 and I6 cite SD for exactly this; the proof is DR's, and this is the section's one forward dependence." A use-site inventory plus a document-ordering justification. The reader needs the definition and the borrowed fact; which sections cite SD, and an audit of the section's dependence count, is the author addressing a reviewer.
- **The operation set**: "— a pointer, not a second statement:" — defensive framing of the paragraph's own status. The paragraph's content (naming the three operations and where each is fixed) is legitimate; the self-characterization is noise.
- **I6 opener**: "the consolidation is needed because the inherited analyses no longer serve." The concrete reason that follows (the inherited postcondition `(a, F, G) ∈ A_K^{Σ'}` does not type-check against a hit's return) is the substance; the need-justification preceding it is redundant with it.
- **Result-side-only, stated three times**: BH1's Effect ("The exclusion is result-side only: a filtered address remains a valid query argument"), BH1's Rewrite scope ("The rewrite is *result-side only* — arguments are never filtered: a filtered source `x` remains a valid default-view `targets_of` argument…"), and S1 ("result-side only, the address remaining a valid query argument"). Likewise the default view's mechanics are spelled out both in Views ("when some Unary type registered with BH1 has an active tuple whose F-coverage contains an address, that address is subtracted from the two enumeration surfaces…") and in BH1's Rewrite scope, which is the normative statement.

**Required**: Each fact stated once in its normative slot; other occurrences become bare citations. Drop the ordering/dependence narration in SD and the self-characterizations in The operation set and I6.

## OUT_OF_SCOPE

### Topic 1: A default-view selector for `Observe_K`
The note fixes that raw `Observe_K` never filters (Views; BH1's "Nothing else is rewritten"), so the default view is reachable only through the shipped predicates. Whether `Observe_K` should grow a third `View` selector for the filtered lens is a coherent successor question.
**Why out of scope**: The note's commitment (hist/oper unchanged, default view predicate-only) is internally consistent; extending the read operation's signature is new surface, not an error here.

### Topic 2: Constituent ordering of `retract_stale`
BH4 fixes the batch as a non-atomic sequence with interleaving permitted and shows every constituent is admitted regardless of order, but the order itself — and hence which frontier slots the constituent retraction tuples occupy — is unspecified. The nullified set is order-independent, so nothing the note claims is affected.
**Why out of scope**: Pinning constituent order (or proving full outcome-determinism modulo address assignment) is refinement of an operation the note correctly specifies at the level it commits to.

VERDICT: REVISE
