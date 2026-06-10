# Review of ASN-0114

I checked the proofs that carry real weight — F2 (disconnectedness ⇒ `|R| ≥ 2`), F5's composition of L12 through LP13, the two S2 collapses in F7, and the worked instance — and they are sound. The F2 argument (convexity S0 + S2 to rule out `|R| ∈ {0,1}`) is correct; F5 correctly notes L12 is single-step and reaches for LP13 to close the `→*` gap; the worked example's tumbler arithmetic (`a₃ ⊕ δ(2,#a₃) = a₅`, LP-Fin Corollary giving `{a₃,a₄}`, `a₅` as the disconnection witness) checks out. The residual issues are precision and one structural/redundancy defect.

## REVISE

### Issue 1: F0's stated content does not match its "three clauses" billing, and duplicates F1
**ASN-0114, "The selector and its domain" / F0**: "We must justify each of the three clauses of this definition — the coverage relationship, the frame, the error case — and extract their consequences."

**Problem**: F0, the definition this sentence points at, states exactly two things: the domain/error behavior (`defined iff … ; otherwise ⊥`) and the coverage relationship `coverage(R) = coverage(Σ.L(a).eᵢ)`. It contains **no frame clause**. The frame is introduced two sections later as F4 and justified from the pure-read principle — not as unpacking F0 — so the "three clauses of this definition" roadmap names a clause the definition does not carry. Separately, the one substantive clause F0 *does* state (coverage) is then re-stated verbatim as F1 (CoverageExactness): "We state this as the central postcondition," when F0 already stated it. So F0 simultaneously over-claims its structure (a frame clause it lacks) and duplicates the equation F1 owns. The anti-bloat classifier flags exactly this kind of verbatim re-statement.

**Required**: Align F0's content with its billing. Either (i) state F0 with domain/error only and let F1 be the sole carrier of the coverage equation, with the frame acknowledged as separately established (F4); or (ii) genuinely place all three clauses in F0. As written, the roadmap names an absent clause and the coverage equation appears twice.

### Issue 2: The "single term" licensing for the multi-valued `followlink` is scoped too narrowly for its own uses
**ASN-0114, "Status of the result — a relation"**: "we read `followlink(Σ, a, i)` as a relation … wherever it appears as a single term inside `coverage(·)`, that term is well-defined."

**Problem**: The paragraph is careful that `followlink` is a relation, determinate only up to coverage, and it licenses the single-term notation **only inside `coverage(·)`**. But F7 and the worked instance write the bare equalities `followlink(Σ, a, i) = ⟨⟩` (valid empty end) and `followlink(Σ, a, 4)` "returns `⊥`" — neither of which sits inside `coverage(·)`. These uses are sound, but only because the relation collapses to a single value in precisely those two cases (`⟨⟩` is the unique empty-coverage span-set, from F7's first S2 collapse; `⊥` is fixed by F0). The note never extends its own well-definedness argument to cover them, so the notation in F7 and the worked instance is used ahead of the statement that authorizes it.

**Required**: Widen the licensing to record that `followlink` is single-valued in the empty-end case (forced to `⟨⟩`) and the out-of-domain case (`⊥`), legitimizing the bare equalities; or write those uses as coverage-equalities. The facts are present in the note; the meta-statement that sanctions the bare-term notation is not.

## OUT_OF_SCOPE

### Topic 1: Resolution of the recorded endset against a document's arrangement (V-position filtering, shrinkage, per-document divergence)
**Why out of scope**: The note correctly isolates this in "A boundary we must respect," matching the scope declaration ("resolving an endset's spec-set to V-positions of a specific document"). The implementation evidence describing V-positions (Q11, Q15, Q20) belongs to that separable concern, not to FOLLOWLINK's contract with the recorded end. I confirm this is *not* a missing-coverage gap in this ASN — the boundary is drawn where it should be, and F1's exactness is correctly exactness-to-the-recorded-end (invariant by F5/L12), with arrangement-conditional shrinkage left to resolution.

VERDICT: REVISE
