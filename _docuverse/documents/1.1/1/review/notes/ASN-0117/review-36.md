# Review of ASN-0117

The DELETE specification is in strong shape: the two-realisation effect (K.μ⁻ + K.μ⁺ composite for `R ≠ ∅`, lone K.μ⁻ for `R = ∅`) is correctly matched to ASN-0047's preconditions, including the strict-extension/strict-contraction edges; the J0/J1★/J1'★ coupling discharge is explicit and correct; the range refinement `ran(M'(d)) = ran(M(d)) \ A_del^{excl}` is exact (I verified both inclusions, including the SD-based disjointness that makes the link-subspace term vacuous in the subtraction); the wp is genuinely the weakest condition (the shrink-only direction is established, the per-link existential is the right quantifier shape); and the worked examples cover first-position, multi-position suffix shift, suffix delete, delete-everything, within-document sharing, and cross-document transclusion — the genuinely delicate boundaries. The S8★ re-cut discussion correctly distinguishes per-state from cross-state obligations. Two issues remain.

## REVISE

### Issue 1: LP17/LP18 invoked outside their stated hypotheses (local vs. global orphanhood)

**ASN-0117, "Link survival" section and P4**: "If the deletion removes the *last* V-position of `d` mapping into a link's coverage, that link becomes *undiscoverable from `d`*: an orphaned reference in the sense of **LP17 (GhostProjection)** (ASN-0098)." And in P4: "otherwise it is orphaned from `d` (LP17) yet persists (L12), remains discoverable from every other document that still arranges its coverage (LP12), and is re-discoverable from `d` should the content be re-arranged (LP18)." The claims table repeats both citations.

**Problem**: LP17's hypothesis is *global*: "no document's arrangement reaches any I-address in `coverage(Σ.L(a).eᵢ)` for any slot `i`" — only then is the link "orphaned: not discoverable from any document." LP18's hypothesis is "`a` is orphaned at `Σ`" in that same global sense. ASN-0117 invokes both lemmas for the strictly *local* notion "undiscoverable from `d`," in the very sentence that asserts the link may remain discoverable from other documents — a situation in which LP17's hypothesis is false and LP18 is inapplicable as stated. The conclusions the ASN wants are true, but these lemmas do not deliver them in the local case; the hedge "in the sense of" does not repair the mismatch, because the *sense* (global vs. per-document) is exactly what differs.

**Required**: Either (a) restrict the LP17/LP18 citations to the case where `d` was the link's sole arranging document, where both apply literally; or (b) derive the local statements from the foundation pieces that actually carry them — local undiscoverability directly from LP12 at `Σ'` (`coverage ∩ ran(M'(d)) = ∅`), and local re-discoverability from `d` by the chain Store Monotonicity★ (`a ∈ dom(Σ''.L)`) + LP3★ (coverage invariance) + LP12 at the later state — which is LP18's own proof chain, none of whose steps needs the global orphan premise. Adjust the body text, P4's statement, and the claims-table entry consistently.

### Issue 2: Meta-prose accretion (anti-bloat)

**ASN-0117, Effect/coupling paragraph**: "This is the *frame discharge* **(DEL-CFRAME)** that the frame clauses DEL-LIMM, DEL-FENT, and DEL-FPROV below cite."

**Problem**: This is a downstream-consumer inventory — it names which later clauses will cite the discharge rather than advancing the discharge itself. The naming alone ("We call this frame discharge DEL-CFRAME") carries all the content; the use-site list is noise the reader must skip. A second instance of the same pattern sits in the wp section: "(the two text summands from DEL-LEFT/DEL-SHIFT, the link summand from DEL-FSUB, the exhaustiveness of the three from S3★-aux, as P4's derivation records)" — this re-enumerates P4's derivation in the same breath as citing it; either the citation to P4's derivation or the enumeration suffices, not both.

**Required**: Trim the DEL-CFRAME sentence to the bare naming; in the wp section, keep the formula restatement (it is the refinement's starting point) but drop either the parenthetical re-enumeration or the "as P4's derivation records" clause.

## OUT_OF_SCOPE

### Topic 1: DELETE at text-subspace depth m > 2

**Why out of scope**: The precondition honestly pins `m = #p = 2`, inheriting ASN-0082's contraction scope (`#p = 2`). S8-depth permits reachable states whose text subspace is pinned at depth ≥ 3 (a fresh K.μ⁺ into an emptied subspace may re-pin any `m ≥ 2`), and DELETE is simply undefined there. Generalising requires extending the foundation contraction, not revising this ASN.

### Topic 2: Deletion in the link subspace

**Why out of scope**: The operation fixes `S = s_C`; removing link placements from a document's arrangement (K.μ⁻ on `s_L`, or retraction-style withdrawal) is a distinct operation with its own obligations (CL-OWN, CL-UNIQ interactions) and belongs to a future ASN.

VERDICT: REVISE
