# Review of ASN-0043

## REVISE

### Issue 1: T6 citation misapplied for element-field prefix decidability
**ASN-0043, Endset Structure**: "Because tumbler containment is decidable (T6, ASN-0034), type addresses support hierarchical relationships: a type at address `p` and a subtype at an address extending `p` are related by prefix ordering."
**Problem**: T6 (DecidableContainment) establishes decidability for four specific field-level questions: same node field (a), same node+user fields (b), same node+user+document-lineage fields (c), and whether the *document field* of one tumbler is a prefix of the *document field* of another (d). None of these cover full-tumbler prefix containment. For type hierarchy, the question is whether `p ≼ c` for arbitrary element-level tumblers — a general prefix check, not a field-scoped containment test. T6(d) is the nearest case but it is explicitly restricted to the document field.
**Required**: Replace the T6 citation with PrefixRelation (ASN-0034) — which defines `p ≼ t` as `#p ≤ #t ∧ (A i : 1 ≤ i ≤ #p : pᵢ = tᵢ)`, decidable by finite component-wise equality — combined with T2 (IntrinsicComparison), which guarantees computability from the tumblers alone without external data structures. The formal proof of L10 is unaffected (it relies on T5 and PrefixSpanCoverage, not T6), and the motivating claim is correct — only the citation is wrong.

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage as a foundation lemma
**Why out of scope**: PrefixSpanCoverage is a general result about tumbler spans — it depends only on ASN-0034 definitions (OrdinalDisplacement, T1, T12) and would serve any future ASN needing span-coverage characterizations (arrangement spans, content spans, query ranges). Promoting it to the tumbler algebra or a dedicated span algebra ASN would make it citable without restating. Not an error in this ASN — it is fully proved here and correctly used — but it is a structural debt.

### Topic 2: Link presence in document arrangements
**Why out of scope**: The ASN correctly notes that S3 (`M(d)(v) ∈ dom(Σ.C)`) precludes link addresses from appearing in arrangements, while Gregory's implementation does place links in V-positions within a dedicated document subspace. Extending the arrangement semantics to accommodate link V-positions is new territory requiring modifications to S3 and the POOM model — a future ASN, not a defect here.

VERDICT: REVISE
