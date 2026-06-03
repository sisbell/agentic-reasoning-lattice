# Review of ASN-0068

## REVISE

### Issue 1: Worked examples and CV-SELF forward-reference claims stated later
**ASN-0068, "The Input"/"Worked Examples"**: CV-SELF's justification reads "Under CV-MAX (established below), the diagonal portion `D` aggregates into runs…" and "The off-diagonal portion `X` typically resolves to width-1 runs (CV-ATOM)." Example 3 states "The CV-ATOM byte-granular admissibility shows up directly," and Example 4 states "Under CV-SPAN-VIEW with `(m_a, m_b) = (2, 3)`, the projection produces…" — all three claims (CV-MAX, CV-ATOM, CV-SPAN-VIEW) are defined *after* these sections.
**Problem**: Multiple sections defer to the same downstream locations ("established below"). A reader following the argument hits named claims with no definition in hand. This is forward-reference accretion: the prose leans on results the document has not yet stated.
**Required**: Order CV-MAX, CV-ATOM, and CV-SPAN-VIEW before the worked examples and CV-SELF, or drop the forward-pointing prose and let the examples stand on the raw run/maximality definitions.

### Issue 2: Example 4 consumes CV-SPAN-VIEW, then prose justifies the ordering
**ASN-0068, after Example 4**: "The span projection used in Example 4 is the natural presentational view of a correspondence run, which we now promote to a labeled corollary."
**Problem**: This is document-ordering justification — the example uses `π_{m_a,m_b}` and `δ(n,m)` projection notation, and the prose then rationalizes introducing the claim afterward. The CV-SPAN-VIEW machinery should precede the example that exercises it; the "we now promote" framing is the kind of ordering meta-prose flagged for this note.
**Required**: Move CV-SPAN-VIEW ahead of Example 4 (which is its natural illustration) and delete the promotion sentence.

### Issue 3: The identity-vs-value and provenance-forgotten themes are restated across four sections
**ASN-0068**: The point "correspondence is by I-address, not stored value" appears in the intro ("exposes I-address overlap, not textual equivalence"), in CV-IDENT, in the standalone section "Why I-Address Identity Suffices," and again in "What the Result Cannot Express" (ii). The "no lineage" point appears in CV-PROV-FORGOTTEN, in "Pairwise Scope," and again in (iii) ("Whether `d_a` transcluded from `d_b`… is not visible in the result").
**Problem**: Two paragraphs (here, several) saying the same thing in different words. "Why I-Address Identity Suffices" is rationale essay that advances no claim — it explains *why* the criterion was chosen rather than stating system structure.
**Required**: State each point once (CV-IDENT, CV-PROV-FORGOTTEN carry it). Fold or delete the "Why I-Address Identity Suffices" section and the redundant clauses of "What the Result Cannot Express."

### Issue 4: Action-point justification paragraph accretes explanatory tangents
**ASN-0068, "The Input"**: The V-position-capture argument is interleaved with asides: "(Whether `⟦σ⟧` also contains tumblers outside subspace `S` depends on `width(σ)_1`; …that question is independent of the failure.)" and "The depth-`m_σ` projection itself arises from intersection with `dom(M(d))`… without this intersection, `⟦σ⟧` would also contain higher-depth tumblers extending `start(σ)` as a proper prefix."
**Problem**: The necessity argument itself is legitimate, but these tangents do not advance it — the reader must skip past them to follow the capture argument to its conclusion. Essay content padding a precondition justification.
**Required**: Reduce the paragraph to the capture argument and its conclusion (`actionPoint(width(σ)) = m_σ` forces agreement at positions `1 ≤ i < m_σ`). Drop the parenthetical and the higher-depth-projection aside.

### Issue 5: Self-comparison admissibility paragraph is defensive clause-walking
**ASN-0068, "The Input"**: "*Self-comparison is admissible.*" then a clause-by-clause verification ending with "The 'single span literal lies in `R_a ∩ R_b` with `m_a ≠ m_b`' inadmissibility caveat is vacuous since `m_a = m_b = m_d`."
**Problem**: A paragraph that re-walks every CV-IN clause to conclude "reduces to per-side admissibility against `d`, with no additional structural obligation," and then notes that a caveat introduced earlier is vacuous in this case. Noting that an earlier caveat does not fire is accretion around CV-IN, not new reasoning.
**Required**: Reduce to a single sentence ("CV-IN does not exclude `d_a = d_b`; the per-side clauses apply independently against `M(d)` at the common depth `m_d`"). Delete the vacuous-caveat sentence.

## OUT_OF_SCOPE

### Topic 1: Concurrent modification, replication, version-history walking, multi-document composition
The Open Questions list these correctly as future work, not as gaps in this ASN. No action needed — they are properly deferred and consistent with the declared scope exclusions.

VERDICT: REVISE
