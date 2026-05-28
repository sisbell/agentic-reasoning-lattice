# Review of ASN-0077

I worked through the ASN's derivations and edge cases against the foundation lemmas it cites.

## REVISE

### Issue 1: Wording confusion in the "outside this working frame" parenthetical
**ASN-0077, O0 derivation (b)**: "Every other transition in the working frame either declares an explicit `L' = L` frame clause (K.α, K.δ in all sub-cases — IsNode, IsAccount, and IsDocument — K.μ~, K.μ⁺_L) or has both effect and frame that name only other components... (Document-registration transitions outside this working frame are governed by LP8 (DocumentRegistrationInvariance, ASN-0098)... LP8 covers (K.σ, K.δ-IsDocument)..."
**Problem**: The text first asserts K.δ-IsDocument is in the working frame with explicit `L' = L`, then describes LP8 as covering "document-registration transitions outside this working frame" while listing K.δ-IsDocument among those LP8 covers. A reader cannot tell whether K.δ-IsDocument is inside or outside the working frame.
**Required**: Clarify that K.δ-IsDocument is in the working frame (with its own explicit `L' = L` frame), and that the parenthetical's purpose is only to discharge K.σ (which is outside ASN-0047's vocabulary) — LP8's mention of K.δ-IsDocument is incidental, not the reason LP8 is invoked.

### Issue 2: Notational ambiguity between V_{s_C}(d) at Σ and at Σ'
**ASN-0077, O11 derivation, case (ii) sub-case (a) step (4)**: "Hence `v ∈ V_{s_C}(d) ⊆ dom(M'(d))` has `#v = m' = m`."
**Problem**: The symbol `V_{s_C}(d)` is used without state subscript, but the surrounding argument has just established `V_{s_C}(d)` at Σ ⊆ `V_{s_C}(d)` at Σ' and is now reasoning about the post-state set. The conclusion `v ∈ V_{s_C}(d)` requires the post-state reading (since v ∈ dom(M'(d)) but v ∉ dom(M(d))). Without an explicit state label here, a careful reader has to backtrack to determine which set is meant.
**Required**: Add explicit state subscripts (e.g., `V_{s_C}(d)|_{Σ'}` or similar) to the symbols appearing in steps (1)–(4) of this sub-case wherever the same set could be read in either state, particularly at the step where v's membership is being asserted.

### Issue 3: Framing convention adopted without formal status
**ASN-0077, O0 derivation (b)**: "We adopt the standing framing convention that each transition's Effect and Frame clauses jointly constrain Σ' — components of Σ named in neither Effect nor Frame are unchanged across the transition."
**Problem**: The "framing convention" is invoked repeatedly (for K.μ⁺, K.μ⁻, K.ρ, and via LP8's premise) but is introduced as a convention adopted within the proof rather than discharged by a foundation axiom. Foundation ASN-0098's LP6, LP7, LP14 are cited as "the operational reading" that uses the convention — but those lemmas themselves don't establish the convention; they assume it. If a later transition (in some yet-to-be-written ASN) modifies L without saying so in its Frame clause, every claim in O0(b), O5, O5★, and downstream would silently rest on the assumption that this can't happen.
**Required**: Either replace the convention with explicit per-transition appeals (e.g., cite K.α's, K.μ⁺'s, K.μ⁻'s, K.ρ's frame clauses directly and case-analyze L's absence), or downgrade the convention's standing claim to a precondition — "Under the assumption that each transition's effect/frame is exhaustive..." — so that downstream users see what they are inheriting.

## OUT_OF_SCOPE

### Topic 1: Cross-subspace I-span (link addresses in I-stream range)
**Why out of scope**: ASN-0077 explicitly defines `origins_I` over `dom(C)` only and flags the link-address case as Open Question 1. Extending the I-span lift to `dom(C) ∪ dom(L)` is a future ASN, not a defect in this one.

### Topic 2: Operation surfacing intermediate transclusion chain
**Why out of scope**: ASN-0077 deliberately reports direct origin (the original allocator) and explicitly excludes transitive provenance. A separate operation to walk transclusion chains is future work.

### Topic 3: Distinguishing native vs transcluded content in a queried document
**Why out of scope**: SHOWORIGIN as specified reports origin uniformly. A separate operation that partitions a document's arrangement into "native to this document" and "transcluded from elsewhere" is future scope.

### Topic 4: Operation reporting historical containment from Σ.R
**Why out of scope**: ASN-0077 explicitly distinguishes current arrangement (the subject of SHOWORIGIN) from historical containment (recorded in Σ.R, governed by P4★ in ASN-0047). A complementary operation querying Σ.R is future work.

VERDICT: REVISE
