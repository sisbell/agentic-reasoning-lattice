# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ admissibility is defined by clauses (i)–(iii), but the proof relies on subspace-preservation, which those clauses do not entail when two subspaces share a depth

**ASN-0047, *Decomposition of K.μ~*** (admissibility definition): "π is admissible iff (i) the induced post-state `M'(d)` would satisfy the arrangement-*shape* invariant package … S8a, S8-depth, S8-fin, D-CTG★, D-MIN★ … (ii) the net effect is non-trivial … (iii) π is *length-preserving*". And: "the remaining per-state arrangement invariants … — S3★, S3★-aux, CL-OWN, CL-UNIQ, S2, and S8★ — are *not* admissibility hypotheses but derived consequences."

**Problem**: Subspace preservation (`subspace(π(v)) = subspace(v)`) is proved only in **Step (A)**, and explicitly only "for every *realisable* π — every π that the K.μ⁻ + K.μ⁺ decomposition (full-clearance form) produces." But the **Necessity** proof, **K.μ~-FIX**, and the **link-subspace fixity** sub-steps all invoke subspace preservation on an *admissible* π ("Suppose K.μ~ admits some π … By Steps (A), (C), (D) …"). The document silently treats "admissible (per the iff)" and "realisable" as the same set.

They are not, when `m_{s_C} = m_{s_L}`. S8-depth permits distinct subspaces to share a depth, and the worked examples actually do so (link example Step 4: `V_{s_C}` and `V_{s_L}` both at depth 2). At a coinciding depth, the transposition `π` swapping a content position `[1,k]` with a link position `[2,j]` is length-preserving (clause iii), produces a post-state whose per-subspace V-position *sets* can still satisfy S8a/S8-depth/S8-fin/D-CTG★/D-MIN★ (clause i is about V-position domains, not values), and is non-trivial (clause ii) — hence "admissible" by the stated iff. But the full-clearance decomposition cannot realise it (K.μ⁺ writes only `s_C` positions; nothing can relocate a link into the content subspace), and S3★ fails on it (a `dom(C)` value would sit at an `s_L` position, contradicting S3★'s link clause + L14). So:

- "admissible ⟺ realisable" is asserted but false for this π.
- "S3★ is a *derived consequence*" is false for this π — S3★ is exactly what the cross-subspace swap breaks.

**Required**: Add subspace-preservation as an explicit admissibility clause (iv) `(A v : subspace(π(v)) = subspace(v))` — or equivalently fold S3★/S3★-aux into the admissibility hypotheses — so that Step (A) becomes a precondition check rather than a property claimed for an under-constrained π. Alternatively, prove that clauses (i)–(iii) entail subspace preservation; that proof must confront the coinciding-depth case, where it does not currently hold.

### Issue 2: P4★/K.μ~ cell misdescribes what K.μ~ preserves

**ASN-0047, *Class (b) verification matrix* / P4★ paragraph**: "K.μ~ preserves Contains_C exactly … carrying dom_C onto dom_C with values preserved".

**Problem**: K.μ~ does **not** preserve per-position values on `dom_C` — reassigning which V-position carries which I-address is the entire point of reordering (`M'(d)(π(v)) = M(d)(v)`). What is preserved is the *range* (the set of content I-addresses), which is why `Contains_C(Σ') = Contains_C(Σ)`. The set-equality the paragraph then writes is correct, but the justifying phrase "with values preserved" contradicts the operation's semantics and should read "range preserved."

**Required**: Replace "values preserved" with the range/set-equality justification (`{a : ∃u∈dom_C(M'(d)) : M'(d)(u)=a} = {a : ∃v∈dom_C(M(d)) : M(d)(v)=a}`), which is what actually discharges P4★.

### Issue 3: Duplicated section header restated verbatim as its own first sentence

**ASN-0047, *Decomposition of K.μ~* → Decomposition**: "**Decomposition.** Here we give the realisation of K.μ~ when the existence condition holds. / *Realisation of K.μ~ when the existence condition holds.* When `M(d)|_{dom_C(M(d))}` takes at least two distinct values …".

**Problem**: The sentence "Here we give the realisation of K.μ~ when the existence condition holds" and the italic run-in header "*Realisation of K.μ~ when the existence condition holds.*" are verbatim duplicates of each other (and of the surrounding section title). This is meta-prose occupying a structural slot — it advances no reasoning and forces the reader to skip past a restated title.

**Required**: Delete the redundant announcing sentence (and/or the run-in header); begin directly with the substantive "When `M(d)|_{dom_C}` takes at least two distinct values …".

## OUT_OF_SCOPE

### Topic 1: Concurrent allocation under a shared home document
The open questions raise serialization/coordination of concurrent link and content allocation. Concurrency and atomicity are listed OUT OF SCOPE; the ASN correctly defers these rather than specifying them.

### Topic 2: Link withdrawal / tombstoning mechanism
The open questions correctly defer a non-suffix link-withdrawal mechanism (status flag, tombstone) reconciling Nelson LM 4/9 with D-CTG★/D-MIN★. This is a future state-component/operation question, not a defect in this ASN's presentational-removal contract.

VERDICT: REVISE
