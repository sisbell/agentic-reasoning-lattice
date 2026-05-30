# Review of ASN-0043

This ASN carries the `review-mode.anti-bloat` classifier. The mathematics is sound — I verified PrefixSpanCoverage, the L1c chains (worked example reaching `1.0.1.0.1.0.2.1`), L8 discrimination (`g₈=1` vs `g'₈=2` forcing disjoint cones), and the L14a scoping argument, and found no correctness defects. The findings below target accreted meta-prose, defensive justification, and table/body duplication.

## REVISE

### Issue 1: L1a justifies the L1a/L1c division of labor
**ASN-0043, L1a**: "The producibility of `a` from this prefix by a finite chain of T10a-conforming `inc` steps is the separate content of L1c (below); separating membership and producibility places the state-level constraint here and the allocator-discipline constraint there."
**Problem**: The final clause is pure document-organization rationale — it explains *why the invariant was split into two* rather than stating what L1a asserts. This is the "prose justifies document ordering / division" accretion pattern.
**Required**: Delete the clause. L1a should state the membership invariant and stop; L1c states its own content.

### Issue 2: Properties table re-proves L1c and L11a
**ASN-0043, Properties Introduced (L1c row)**: "single chain-existential clause: producer chain seeds at a T4-valid document-level tumbler `s` with `zeros(s) = 2`, first step `k₁ = 2` (the only `kᵢ = 2` step admissible — TA5a's `zeros ≤ 2` precondition fires only once before zeros reaches the element-level value 3)... T4-validity via T10a.4 ... the equality via CPP".
**ASN-0043, Properties Introduced (L11a row)**: "a corollary of L1c plus T10a's GlobalUniqueness ...: L1c discharges GlobalUniqueness's sole precondition (T10a-conformance) ... Within a single state, identification by tumbler equality follows from Σ.L's partial-function structure ... Persistence of the address-to-link binding across state transitions is L12, not L11a".
**Problem**: The summary table reproduces the full proof bodies verbatim in prose. A summary row should state the claim, not re-derive it. This is body/table duplication.
**Required**: Collapse each row to its one-line statement; the proof lives once, in the body.

### Issue 3: L12b states its conclusion twice
**ASN-0043, L12b**: After the three-line "*Derivation*" (which fully establishes the inclusion via L12a + L1a), a second paragraph re-states it: "L12b is the joint consequence of L1a (applied at every reachable state) and L12 ... once a link exists, its home document cannot be removed ... This is the link-side dual of S7a's persistence guarantee ... lifted across L12a's monotonicity to constrain the arrangement store's evolution."
**Problem**: Two paragraphs say the same thing in different words. The second adds only an S7a analogy.
**Required**: Keep the derivation; delete the restatement (retain the one-clause S7a analogy if desired).

### Issue 4: L3's non-emptiness paragraph is why-needed essay plus forward consequence
**ASN-0043, L3**: "The non-emptiness conjunct ... rules out the same family of malformed states from a second angle: an arity-3 link `(F, G, ∅)` ... defeating the purpose of slot 3. ... the spelling chosen is the more direct, but the coverage formulation is equivalent and may be invoked interchangeably below. Under this conjunct, L8's `same_type` equivalence relation has only non-degenerate classes ..."
**Problem**: Three accretion patterns in one paragraph: (i) "Why the conjunct is needed" rationale; (ii) "may be invoked interchangeably below" use-site note; (iii) anticipation of an L8 downstream consequence. None advances L3's statement.
**Required**: State the conjunct. Move the `≠ ∅ ⟺ coverage ≠ ∅` equivalence to where it is actually used; drop the L8 anticipation.

### Issue 5: L9 preconditions get load-bearing essays
**ASN-0043, L9**: "The precondition `dom(Σ.M) ≠ ∅` is the natural scope of L9: any state in which a link already exists has `dom(Σ.M) ≠ ∅` by L1a ..." and "The `s_C`-residence precondition is load-bearing for content-side disjointness ... without the precondition, `dom(Σ.C)` might contain addresses in the chosen `s_X` and the disjointness would fail."
**Problem**: These are "why the precondition is needed" justifications attached to a lemma statement — exactly the accretion pattern. The `s_C`-residence point is already exercised constructively in the proof (T7 against `s_X ∉ {s_C, s_L}`); the standalone justification is redundant.
**Required**: Drop the standalone rationale paragraphs; let the construction's use of each precondition speak for itself.

### Issue 6: StateExtension definition enumerates its downstream consumers
**ASN-0043, Definition — StateExtension**: "the special case `Σ'.C = Σ.C`, `Σ'.M = Σ.M` (only `Σ.L` grows) is the form used by the existential lemmas below."
**Problem**: A definition closing by naming which later lemmas use it — the "definition's introduction enumerates downstream consumers" pattern.
**Required**: End the definition at the extension condition. Drop the use-site clause.

### Issue 7: L0 explains why L0a is stated separately
**ASN-0043, L0**: "The companion content-side universal is stated separately as L0a below, since its derivational status differs."
**Problem**: Meta-prose justifying why the content-side claim was placed in a separate property — document-ordering rationale, not L0 content.
**Required**: Delete. L0a's separate existence needs no in-text apologetic.

### Issue 8: L11a body "Derivation" is itself a re-narration
**ASN-0043, L11a**: "*Derivation.* We do not re-prove uniqueness here; it is exactly GlobalUniqueness (ASN-0034) instantiated at link addresses. GlobalUniqueness's sole precondition is T10a-conformance of the events. L1c ... discharges precisely that precondition ... Instantiating GlobalUniqueness at the link-address events therefore yields `a₁ ≠ a₂`."
**Problem**: This is sound but, combined with Issue 2's table duplication and the body's surrounding "*Consequence — identification within a state*" paragraph, the same one-step instantiation is told three times across the document.
**Required**: Pick one home for the derivation (the body), reduce the table to a pointer, and ensure the "Consequence" paragraph adds genuinely new content rather than re-narrating.

## OUT_OF_SCOPE

(none)

META: The ASN remains squarely in-scope — it defines link-store state, its invariants, and their structural consequences abstractly — so this is bloat to trim, not drift to terminate.

VERDICT: REVISE
