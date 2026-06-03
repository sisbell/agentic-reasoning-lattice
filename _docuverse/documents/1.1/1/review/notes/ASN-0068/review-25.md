# Review of ASN-0068

## REVISE

### Issue 1: The restriction — the operation's defining feature — is never exercised by any example
**ASN-0068, The Input / Worked Examples**: "Restriction is therefore not a separate filtering stage — it is part of what defines the operation, the lens through which it is asked to look." Yet every worked example states "Take `R_a` and `R_b` to span the full arrangement of each document" (Examples 1, 3, 4; Example 2 likewise full).
**Problem**: The non-trivial behavior of `R_a/R_b` is run-splitting: a restriction whose span-set has a gap, or whose reach cuts through an otherwise I-contiguous region, must terminate a run at the restriction boundary (right-maximality via `v_a + n ∉ ⟦R_a⟧`) even though the underlying I-addresses remain contiguous in `dom(M)`. No example demonstrates a restriction that strictly narrows or fragments a run. The feature the note insists is constitutive of the operation is verified nowhere. Per review standard 6, a key postcondition without a concrete example is a REVISE item.
**Required**: Add an example with a proper restricting span-set (e.g., `R_a` covering only `[1,1]..[1,2]` of a longer I-contiguous arrangement, or a two-span `R_a` with a middle gap) and check that the result splits at the restriction boundary as the run conditions require.

### Issue 2: CV-SPAN-VIEW has accreted bloat and presentational essay prose
**ASN-0068, CV-SPAN-VIEW**: the set-level injectivity verification — "if `π*(M¹) = π*(M²)`, then for each `r¹ ∈ M¹` there is some `r² ∈ M²` with `π(r¹) = π(r²)`, whence `r¹ = r²` by per-run injectivity and `M¹ ⊆ M²`; the symmetric argument gives `M² ⊆ M¹`" — spells out the generic fact that an injection lifts to an injection on the powerset; it advances nothing once per-run injectivity (b) is in hand. Postcondition (c)'s closing sentence — "so neither `π` nor `π*` is a universal isomorphism on `Result`" — is explain-what-it-is-not meta-prose. The motivating prose ("the natural form for a user-facing rendering: a client can highlight `σ_a` in `d_a`... synchronously") is presentational/implementation essay sitting in a claim's body.
**Problem**: Trivial-lift elaboration and UI-rendering narrative are noise the precise reader must skip; (c)'s negative aside justifies a property by saying what it isn't.
**Required**: State `π` injective, note the powerset lift inherits injectivity in one clause, drop the "universal isomorphism" aside and the client-rendering paragraph (or move the latter to a single line of motivation).

### Issue 3: Open Questions restate matters already settled in the body
**ASN-0068, Open Questions**: "What guarantees must the operation make when restrictions overlap V-positions that have been contracted from the arrangement but are still referenced in the provenance relation `R`?" is already answered by CV-DETERM: "a K.μ⁻ contraction that removes a V-position eliminates the corresponding pair even though `R` retains the historical fact... so stale provenance can never generate a phantom correspondence." Similarly, "What must the system guarantee about the result's representation when V-position depths differ between the two compared documents?" is discharged by CV-SPAN-VIEW (well-formedness at differing `m_a, m_b`) and Example 4.
**Problem**: Two paragraphs in different sections (open question + resolved claim) carry the same content; an "open" question already closed in the body is a defer-to-elsewhere accretion.
**Required**: Remove these two questions, or rewrite them to name the genuinely-open residue not covered by CV-DETERM / CV-SPAN-VIEW.

## OUT_OF_SCOPE

### Topic 1: Link-subspace specialization (CV-LINK-DEGEN, CV-LINK-SELF)
**Why out of scope**: These claims characterize `compareversions` over `S = s_L` and rest entirely on link-specific invariants (CL-OWN, CL-UNIQ, S7). The declared scope lists "link semantics" as out of scope, and the note itself concedes "the operation specializes to `s_C` in practice." The `s_L` behavior belongs in a link-focused note; here it is new territory rather than an error. (Defensible to retain since CV-IN admits `S ∈ {s_C, s_L}`, but the link-invariant reliance is scope-adjacent.)

VERDICT: REVISE
