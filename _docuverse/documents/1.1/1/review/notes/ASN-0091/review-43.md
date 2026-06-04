# Review of ASN-0091

## REVISE

### Issue 1: Bijection-characterization mega-paragraph is exhaustiveness/defensive bloat
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: the single paragraph following RA-frame proves a full forward-and-reverse biconditional ("π witnesses Σ → Σ' iff it restricts to a bijection between corresponding pre-image sets"), with sub-inferences (a)–(d) and the self-justifying aside that (b), (c), (d) "are listed explicitly to make the chain unambiguous."
**Problem**: This is a textbook fact (a bijection of a set respects any partition into fibers). The four enumerated sub-inferences plus the full reverse reconstruction plus the parenthetical defending why they are spelled out are exactly the exhaustiveness-claim + defensive-justification pattern the anti-bloat pass targets. The biconditional's only load-bearing use is the non-uniqueness worked example, which can cite the fiber-restriction fact in one sentence.
**Required**: Collapse to the statement of the fiber-restriction characterization plus a one-line justification; delete the (b)/(c)/(d) enumeration and the reverse-direction reconstruction.

### Issue 2: Definition enumerates downstream consumers (use-site inventory inside the definition)
**ASN-0091, RA definition**: "The `dom(Σ'.M) = dom(Σ.M)` clause discharges, in particular, the implicit precondition needed for downstream lemmas to evaluate state-relative predicates at Σ' (RE-disc applies LP12 at Σ', which requires `d ∈ dom(Σ'.M)`; RE-trans's home-document clause requires `origin(a) ∈ dom(Σ'.M)`)."
**Problem**: A definition's clause justifies itself by inventorying which later claims consume it. This does not advance the meaning of the clause; it is the "definition introduction enumerates downstream consumers" pattern.
**Required**: State the clause; drop the consumer list. The same sentence appears in compressed form twice (also in the RA-π signature discussion) — remove both.

### Issue 3: "Remark on RA-dom's relation to the other clauses" is meta-prose about clause redundancy
**ASN-0091, *Remark on RA-dom's relation to the other clauses***: "RA-dom is implied by RA-π's signature together with RA-adm and foundation D-SEQ★..."
**Problem**: This paragraph argues about the *structure* of the definition (whether a clause is redundant) rather than advancing what the operation does. It is new prose explaining why a clause is needed/redundant — the named anti-bloat pattern.
**Required**: Either drop RA-dom and keep the derivation as the sole justification, or keep RA-dom as primitive and delete the remark. Do not keep both the clause and a paragraph debating its redundancy.

### Issue 4: Full RA-adm verification duplicated across Worked Examples 1 and 2
**ASN-0091, "Worked Example" and "Worked Example — 4-cut Swap"**: both *Admissibility (RA-adm)* blocks spell out S2, S8a, S8-depth, S3★, D-CTG★, D-MIN★, D-SEQ★, S3★-aux, CL-OWN, CL-UNIQ, P4★, S8★, the state-component-only list, and P4a in near-identical prose.
**Problem**: Two passages saying the same thing in different words. The note itself concedes the redundancy in Worked Example 4 ("We omit the per-invariant repetition here"). If repetition is omittable there, it is omittable in Example 2.
**Required**: Verify the per-invariant package once (Example 1), then in Examples 2–4 verify only the clauses whose discharge *differs* (e.g., the μ-region displacement in the 4-cut case, shared I-addresses in Example 4). Reference the Example 1 package for the rest.

### Issue 5: RE-trans over-derives conclusions (i) and (ii)
**ASN-0091, "Cross-Document Transclusion Preserved"**: conclusions (i) `a ∈ ran(Σ'.M(d))` and (ii) multiplicity preservation are routed through "CL-OWN ... S3★ ... a ∈ dom(Σ.C). By RE-C, the address `a` remains in `dom(Σ'.C)`..."
**Problem**: Conclusions (i) and (ii) as stated follow immediately from RE-ran and RE-μ (a ∈ ran(Σ.M(d)) by hypothesis ⟹ a ∈ ran(Σ'.M(d)); multiplicity by RE-μ). The CL-OWN + S3★ + C2 + RE-C chain establishes content *persistence* (`a ∈ dom(Σ'.C)`), which is not part of (i) or (ii). It is surplus reasoning attached to a claim that does not assert it.
**Required**: Derive (i)/(ii) from RE-ran/RE-μ directly. If content persistence is a wanted consequence, state it as an explicit extra conclusion; otherwise delete the routing.

### Issue 6: Repeated cross-deferrals between claims and worked examples
**ASN-0091, multiple sites**: "exhibited concretely in the 'Worked Example — Bijection Non-Uniqueness' trace below"; "A concrete two-step trace ... appears in the ... section below"; "exercised concretely in the third Worked Example ... above"; RE-sub/RE-ext each defer forward to the same traces.
**Problem**: Multiple paragraphs in different sections defer to the same downstream locations — the named forward-reference accretion pattern.
**Required**: Keep at most one pointer per worked example, placed at the claim it most directly illustrates; remove the rest.

### Issue 7: Defensive justification in RE-subpres
**ASN-0091, *Subspace preservation at the abstract level***: "The binary constraint cannot be skipped, because S3★ at Σ' is a pair of conditional implications ... both vacuously satisfied if `subspace(π(v))` were some third value..."
**Problem**: Prose explaining why a proof step is necessary rather than performing it. Stage 1 simply applies S3★-aux; the meta-explanation of why Stage 1 precedes Stage 2 is noise.
**Required**: Run Stage 1 then Stage 2; drop the "cannot be skipped" justification.

## OUT_OF_SCOPE

### Topic 1: Dependency-audit recommendation (ASN-0053 removal)
**Why out of scope**: The "Dependency audit" paragraph correctly identifies that ASN-0053 has no use site and recommends removing it from `depends:`. As a *recommendation* this is actionable and useful, but as standing prose in a claims section it is a use-site inventory. The action (drop 0053 from depends) belongs in the inquiry's dependency frontmatter; the paragraph itself should not persist in the note body.

### Topic 2: Bounds on run-cardinality growth
**Why out of scope**: The open question "What upper bound ... on the increase in maximal-run-decomposition cardinality from a single rearrangement" is genuine future territory, not a gap in this ASN's REARRANGE characterization.

VERDICT: REVISE
