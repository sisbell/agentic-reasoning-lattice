# Review of ASN-0114

The mathematics is sound. I checked F1's two-inclusion decomposition, F2's `|R| ≥ 2` argument (lower bound from the first collapse, exclusion of `|R| = 1` via S0 convexity), the slot-3 discharge from L3 plus the two collapses, the F5 closure derivation, and the worked instance (the `a₃…a₈` example, the `q = a₅` disconnectedness witness, the `coverage(e₁) ∩ F = {a₃, a₄, a₇, a₈}` computation against LP-Fin). All hold. Boundary cases — empty end, invalid selector below 1 and above `|Σ.L(a)|`, `a ∉ dom(Σ.L)`, the never-empty type slot — are each addressed. Cross-ASN references are all to foundation ASNs. There is no correctness defect.

The findings below are residual meta-prose and one precision regression — the patterns the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: F5 derivation opens with a discarded lemma

**ASN-0114, F5 derivation**: "L12 (LinkImmutability) fixes a link's address and value across a *single* transition `Σ → Σ'`; F5 quantifies over the reflexive-transitive closure `Σ →* Σ'`, so the single-step fact must be composed along the sequence."

**Problem**: This sentence introduces L12 only to set it aside, then cites LP13 — which is itself the closure lemma — to do the actual work. The proof of F5 needs only the chain `LP13 ⟹ Σ'.L(a) = Σ.L(a) ⟹ Σ'.L(a).eᵢ = Σ.L(a).eᵢ ⟹` (F1 at each state) coverage equality. The L12-vs-closure preamble is a defensive justification of the citation choice; a reader checking the proof skips past it to reach LP13.

**Required**: Open the derivation directly at LP13.

### Issue 2: Disclosure paragraph closes with a restatement plus flourish

**ASN-0114, F6 section (the "What, then, *does* the result expose?" paragraph)**: "…and its success reveals no arity beyond the lower bound `i`. Confinement is the dual of exactness — exactness says the answer covers the whole of the selected end, confinement says it covers no part of any other."

**Problem**: The paragraph's substantive content — the partial home-document disclosure over the document-bearing slice, and the arity lower bound `|Σ.L(a)| ≥ i` — is a legitimate consequence derivation. But it has already landed both points before these closing clauses arrive. "reveals no arity beyond the lower bound `i`" restates the arity sentence two lines up; "Confinement is the dual of exactness…" is a rhetorical summary of F1/F6 that advances no claim. (The concrete instantiation "not the from-set when the to-set was asked, not the type" is fine — that is an example, not meta-prose.)

**Required**: Cut the arity restatement and the "dual of exactness" sentence; the derived disclosures stand on their own.

### Issue 3: Synthesis recaps the claims table and loosens F6's qualified disclosure

**ASN-0114, Synthesis**: "It reads one end and discloses only that end — the addresses it targets, the documents those addresses structurally name, and the fact that the link has at least that many slots — while its coverage turns on the selected end alone (F6)."

**Problem**: Two issues in the one paragraph.
(a) The middle of the synthesis restates F1–F8 one claim at a time, duplicating the Claims table that immediately follows. The paragraph's genuinely new content is the primary/corollary classification (F1, F4, F7 primary; the rest corollaries) and the implementation pass/fail summary (F1–F6, F8 hold; F7 fails). The per-claim recap can go; that framing should stay.
(b) "the documents those addresses structurally name" flattens the qualified disclosure the body was careful to establish — that the home document is readable *only* for the T4-valid, document-bearing slice (`zeros(t) ≥ 2`), while node/user-level, ghost, and non-T4-valid interior covered addresses name no document at all (L4, L9). Read plainly, the synthesis implies every covered address names a document, which the body explicitly denies.

**Required**: Trim the per-claim recap; preserve the document-bearing-slice qualification in the disclosure clause (e.g., "the documents that the document-bearing addresses among them structurally name").

## OUT_OF_SCOPE

None. The ASN correctly confines itself to reading the *recorded* endset and defers resolution-against-an-arrangement to a future ASN ("A boundary we must respect"); it defines no claims for the listed out-of-scope operations, and the open questions that point at resolution and protocol encoding are appropriately forward-looking.

VERDICT: REVISE
