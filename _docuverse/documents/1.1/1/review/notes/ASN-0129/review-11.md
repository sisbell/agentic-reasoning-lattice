# Review of ASN-0129

The technical core is sound — the trace is genuinely computed and checks out against the upstream contracts, PD0's induction is grounded case-by-case, and PC6's circularity risk is honestly parameterized. The findings below are one grounding gap in the base audit, one redundant argument, two clusters of accumulated meta-prose (this note carries the anti-bloat classifier), and a typing-hygiene defect.

## REVISE

### Issue 1: QD-audit grounds a membership test, then grants an enumeration
**ASN-0129, QD-audit (BaseReadAudit)**: "`M_dom` is a read no upstream surface exposes, admitted deliberately — document-residence `d ∈ dom(Σ.M)` is the emit surface's own gating clause (I1/I5, ASN-0128), the one store-domain test the upstream contracts themselves perform, and a gating discipline written in PL must be able to state what the surface checks."

**Problem**: The cited ground justifies a *membership* predicate on one address — that is all the emit surface checks (I1's miss branch, I5). The admitted base is strictly stronger: PC6 fixes it as "enumeration, not membership, because PC1/PC2a fold over these domains," and the grant therefore licenses `(∀ d ∈ M_dom :: …)`, `count(M_dom)`, `max_{T1}(M_dom)`, and QD-refl reflection of the full document set into term position. No upstream contract performs any of these (L1a, L-ContiguousPrefix, and ASN-0127's `image` all consume `dom(Σ.M)` as a membership precondition or meta-quantifier, never as a read that lists documents), and none of this note's own examples enumerates documents — PD2's pricing sentence speaks only of "document-residence." The audit's announced method is "measured against the upstream read surface," and the strengthening from test to enumeration is never measured: a membership-only admission (an oracle atom in `V_atom`, with `M_dom` kept out of QD's bases, exactly the shape `is_K` already has) would meet the stated need.

**Required**: Either ground the enumeration capability — name the consumer or warrant for quantifying and folding over all documents — or state in QD-audit that the grant strictly exceeds the gating-clause ground and record why the membership-only alternative is rejected (e.g., uniformity of QD's base discipline). The audit must price what it admits, not a weaker read.

### Issue 2: V-IDX argues a case its own premises exclude
**ASN-0129, V-IDX (IndexedFamilies)**: "their records are fixed (S1–S3: …) — no behavior family is attached at all three, and R-C0's compatibility clauses foreclose any registry that would be: BH1 requires Unary and fails at the two Binary designates, BH2 and BH3 require Binary and fail at `retired`, BH4 requires `idem = ⊥` and fails at all three."

**Problem**: With the designated records fixed (R-C1 makes the three entries mandatory; S3 fixes `R`'s behaviors as ∅), "no behavior family is attached at all three" follows by inspecting one record: `R` attaches none, so no family is universal. The trailing foreclosure clause re-derives the same conclusion for registries whose designate records *differ* from S1–S3 — registries the foundation does not admit. This is prose defending against a case the carrier already excludes, and the BH-by-BH compatibility walk exists only to serve that counterfactual.

**Required**: Keep the inspection argument (`R`'s record attaches no behavior family, hence none is universally attached) and delete the R-C0 foreclosure clause with its four-family walk. If the foreclosure is intended as robustness against a future relaxation of S1–S3, that intent must be stated — as written it is unmotivated duplication.

### Issue 3: the vocabulary section audits itself
**ASN-0129, V (AtomicVocabulary)**: "This note's own additions are exactly four, each conservative and each fenced where introduced: … Only the first two of the four extend what the vocabulary *reads* — V-PRIM reads no state, and the totalization changes no defined value — and neither of those two extends what the *substrate* exposes: … The vocabulary audit is therefore not the whole read audit: the one read this note admits that no upstream surface exposes enters at QD's bases, audited and grounded there (QD-audit)."

**Problem**: This is an accounting of the note's own deltas — an exhaustiveness claim ("exactly four"), per-addition conservativity assertions, and a forward deferral to QD-audit — when each addition is already introduced, typed, and fenced at its own site (V-AUD, V-TUP, V-PRIM, the totalization), and the load-bearing read accounting lives in QD-audit and PC6's base enumeration. Adjacent instances of the same accretion: the totalization's "That definedness-stability ground carries the totalization alone" defends the sufficiency of the rationale just given — reviewer-directed, not reader-directed; consumer inventories at definition sites ("PD0 leans on this" in V-TUP; "everything downstream of QD-fin (PC1, PC2a, PC5) inherits it" in H-init); forward pointers of the "below" kind in PC4 and the argument-regimes paragraph; and the Gregory add-then-compare point stated twice in full (`tumbleradd`/`intervalcmp` in V-TUP, the same read-path line again in PC6's granularity paragraph).

**Required**: Compress the additions paragraph to a one-sentence declaration of the four items; cut the sufficiency-defense sentence and the consumer inventories; state the Gregory read-path evidence once (PC6, where the granularity claim needs it) and cite it from V-TUP.

### Issue 4: QD-audit's content-store entry carries a prior excision as advocacy
**ASN-0129, QD-audit (BaseReadAudit)**: "A content-existence base would be this note's invention, grounded in neither authority, and the note declines it."

**Problem**: The negative entry for `dom(Σ.C)` is necessary content — PC4, PD2, and Structural-reads-only lean on it — but the paragraph argues it at finding-resolution depth: write-path forensics ("the codebase's one existence-style check guards the insertion path, content-store occupancy being maintained as a write-path invariant — an I-address propagates only after its bytes are stored, and the store is append-only") and a closing refusal addressed to a challenger rather than a reader. This reads as a prior cycle's excision of the content base relocated into justification prose rather than removed.

**Required**: Reduce the entry to the boundary fact: `dom(Σ.C)` has no base; no upstream contract consults it; content is reached only through arrangement reads, which are ASN-0127's layer and outside PL. Drop the insertion-path narration and the "this note's invention / declines it" framing.

### Issue 5: the state index is dropped inconsistently across signatures
**ASN-0129, PC2a (AggregationClosure)**: "`⋃(D, f) : ℘_fin(T)` for an address- or tuple-valued `D` … and a set-valued PL term `f : D → ℘_fin(T)`: the union `⋃_{x ∈ [D]_Σ} f(x, Σ)`"

**Problem**: The fold body is typed without the state argument it is then applied to — `f : D → ℘_fin(T)` cannot be evaluated at `(x, Σ)`. The same convention slip runs through the atom signatures: V types `is_K : T → Bool` and `members(K, view) : ℘_fin(T)` with no state index, while PC0 and PC1 type their constituents over `S` (`P, Q : S → Bool`, `P : D × S → Bool`) and PC2 distinguishes `f : S → C₁` from "state-indexed" `g : C₁ × S → C₂`. `S` itself — presumably ASN-0128's `→_sh*`-reachable extended-record states — is never fixed in this note. A smaller instance of the same looseness: PC2a's idem discussion says "the active-view per-class count is at most 1 (I1a…)" where "class" means I0-class, in a note where unqualified "class" elsewhere means coverage class K; the citation disambiguates, the prose should.

**Required**: Define `S` once; fix one convention (every PL term is `S`-indexed, with atom signatures eliding `S` by stated convention) and correct PC2a's fold signature to `f : D × S → ℘_fin(T)`; qualify "per-class" as per-I0-class in the PC2a counting commitments.

## OUT_OF_SCOPE

### Topic 1: general value-position conditionals
PL admits branching only through PC2's definedness guard; a Boolean-conditioned value branch (`if P then t₁ else t₂` for arbitrary Boolean `P`, value-typed branches) is not formable, so e.g. a term selecting between two addresses on an `is_K` test has no spelling. **Why out of scope**: the ceiling is internally consistent without it — the evaluation class's node vocabulary excludes it symmetrically — and PC6's own vocabulary-axis analysis identifies the closure route (paired V-PRIM-style admission). Whether protocols need it is a future-extension question, not an error here.

### Topic 2: precise statement of C-reach
The conjecture says "transitive closure over the denoted graph" without fixing the graph (which K, which view, edge relation `y ∈ succs_K(x)`, reflexivity convention). **Why out of scope**: the note explicitly defers the proof obligation to Open Question 6; sharpening the statement belongs to that successor, and nothing in this note's theorems rests on the conjecture's exact form.

VERDICT: REVISE
