# Review of ASN-0120

## REVISE

### Issue 1: Range-containment step cites S3★ alone where S3★-aux is also load-bearing
**ASN-0120, "The invariants MAKELINK preserves" (ML9, Fact (a) and the future-state paragraph)**: "By generalized referential integrity (S3★, ASN-0047) at the post-state, an arrangement's images lie in the post-state store: `ran(Σ'.M(d')) ⊆ dom(Σ'.C) ∪ dom(Σ'.L)`" — and again at the close of ML9: "that range lies in `dom(Σ''.C) ∪ dom(Σ''.L)` (S3★)".

**Problem**: S3★ is conditional per subspace: it constrains the image of a V-position only when `subspace(v) = s_C` (image in `dom(C)`) or `subspace(v) = s_L` (image in `dom(L)`). For a V-position in any other subspace, S3★ says nothing. The unconditional containment `ran(M(d')) ⊆ dom(C) ∪ dom(L)` requires the exhaustiveness invariant S3★-aux (SubspaceExhaustiveness, ASN-0047) to rule out the third case. The gap is real, not cosmetic: without S3★-aux the inference does not go through, and Fact (a) — the step that collapses the coverage/`ρ` gap and on which the whole wp derivation of ML9 rests — is incompletely licensed. The ASN demonstrably knows this pairing is required: the `a ∉ ran(M(d))` discharge for `K.μ⁺_L` correctly invokes "S3★-aux ... every image is a link-subspace one or a content-subspace one, each branch closed separately." The two ML9 occurrences cite S3★ alone, an inconsistency with the ASN's own (and the corpus's) per-step citation discipline.

**Required**: At both occurrences, cite S3★ together with S3★-aux (or route the containment through the pairing already established in the `K.μ⁺_L` discharge paragraph), so the subspace-exhaustiveness premise of `ran ⊆ store` is discharged rather than implicit.

### Issue 2: The extensional-pinning sentence is garbled at a load-bearing step, and its right-to-left use of the merge identity leaves the chain-run identification implicit
**ASN-0120, "What the endset arguments name..." (extensional coverage paragraph)**: "...so the span is the merge of a fully-resolved chain run and its denotation — the merge identity above, read right to left — is the union of exactly those addresses' unit subtrees;"

**Problem**: Two defects in one sentence. (a) Grammatically, the sentence splices two predications ("the span is the merge … and its denotation … is the union …") in a way that invites the garden-path reading "the merge of [a fully-resolved chain run] and [its denotation]"; the reader must re-parse to recover the intended "the span is the merge of a fully-resolved chain run, and its denotation … is the union of those addresses' unit subtrees." This is the crux step of the extensional form on which ML2 and ML9's Fact (a) both rest; it cannot afford ambiguity. (b) Substantively, applying the merge identity right-to-left to an *arbitrary* admissible span requires identifying the span's `F`-trace `{shift(s, k) : 0 ≤ k < n}` as an `inc(·, 0)` chain run — i.e., `shift(s, k+1) = inc(shift(s, k), 0)` — which holds only because each trace member lies in `ρ(R_j, Σ) ⊆ dom(Σ.C)` and is therefore T4-valid (StoreT4Validity, ASN-0093), making `sig = #` (TA5-SigValid) so that the sibling step coincides with the last-component shift. That transfer was made explicit in the original left-to-right derivation of the merge identity but is silently presupposed here, where the hypothesis arrives in shift-form rather than inc-form.

**Required**: Split the sentence into two, and either restate or explicitly back-reference the T4-validity/sig transfer that licenses reading the span's `F`-trace as a sibling chain run before invoking the merge identity right to left.

## OUT_OF_SCOPE

### Topic 1: Endset arguments supplied directly as I-addresses (ghost and foreign endsets)
**Why out of scope**: The ASN correctly observes that V-spec resolution can only produce content-backed endsets and that reaching ghost addresses (L9) or the full generality of L4 requires a different argument shape. Specifying that argument shape is a distinct operation surface, properly deferred.

### Topic 2: Endset arguments referencing the link subspace (links pointing at links)
**Why out of scope**: `wf` confines specs to the content subspace, and the link-to-link case is explicitly deferred to an Open Question. The resolved record's well-formedness under link-subspace references is new territory, not an error here.

### Topic 3: Semantics of the empty non-type endset (the one-sided link's meaning)
**Why out of scope**: The ASN settles definedness, L3-legality, and inertness in ML9's test — everything the operation's contract needs — and correctly defers what the degenerate connection *asserts* to a future ASN.

VERDICT: REVISE
