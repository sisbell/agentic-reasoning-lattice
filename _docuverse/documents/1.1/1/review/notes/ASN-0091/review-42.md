# Review of ASN-0091

## REVISE

### Issue 1: RE-subpres sources π(v) ∈ dom(Σ'.M(d)) from the wrong premise, creating circularity with the RA-dom redundancy claim
**ASN-0091, "REARRANGE as Vstream-Only Operation" (RE-subpres, Stage 1)**: "RA-frame's `dom(Σ'.M) = dom(Σ.M)` together with RA-dom gives `π(v) ∈ dom(Σ'.M(d))`."
**Problem**: Two defects. (a) The cited chain places `v` (not `π(v)`) in `dom(Σ'.M(d))`: `dom(Σ'.M) = dom(Σ.M)` gives `d ∈ dom(Σ'.M)`, RA-dom gives `dom(Σ'.M(d)) = dom(Σ.M(d))`, so `v ∈ dom(Σ'.M(d))` — but the step needs `π(v)`, which comes from π's *codomain* (the RA-π signature `π : dom(Σ.M(d)) → dom(Σ'.M(d))`), not from RA-dom. (b) The "Remark on RA-dom's relation to the other clauses" derives RA-dom's redundancy *via* RE-subpres ("as RE-subpres derives below"), but RE-subpres as written *consumes* RA-dom. The redundancy derivation is therefore circular as literally stated.
**Required**: Re-source `π(v) ∈ dom(Σ'.M(d))` in RE-subpres from the bijection codomain (RA-π's signature) alone, removing the RA-dom citation. Then the Remark's claim that RA-dom follows from the bijection signature + RA-adm is non-circular.

### Issue 2: "Remark on RA-dom" is use-site inventory and redundancy justification, not argument
**ASN-0091, "Remark on RA-dom's relation to the other clauses"**: "We keep RA-dom as a separate definitional clause for ease of reference at each downstream use site — RE-dom, the RE-other clause, and several admissibility derivations cite it directly — not because it carries content independent of the bijection and the admissibility constraint."
**Problem**: This is exactly the flagged accretion pattern: a use-site inventory ("RE-dom, RE-other, several admissibility derivations") plus a justification for keeping a redundant clause. It advances no reasoning a reader needs to follow the definition. The substantive content (RA-dom is derivable) belongs in one sentence; the rest is defensive bookkeeping.
**Required**: Collapse to a single statement that RA-dom is implied by RA-π's signature + RA-adm + D-SEQ★, and delete the use-site enumeration and the "for ease of reference / not because" framing.

### Issue 3: Cycle-breaking prose justifies a non-existent cycle
**ASN-0091, "K.μ~ Admissibility Clauses" (RA-dom bullet) and "Forward Direction" clause (iii)**: "routing REARRANGE_K's RA-dom through K.μ~-FIX would create a cycle, since REARRANGE_K's clause (iii) discharge … is itself anchored independently"; and "with no appeal to RA-dom, RE-subpres, or S8-depth — this independence is what breaks the cycle (clause (iii) must not route through RA-dom…)."
**Problem**: Clause (iii) is discharged independently of RA-dom (the ASN states this). K.μ~-FIX derives domain fixity from clause (iii) + D-SEQ★. Since clause (iii) does not depend on RA-dom, sourcing RA-dom from K.μ~-FIX would not in fact close any cycle. The elaborate "we deliberately do not source from K.μ~-FIX / this independence breaks the cycle" prose is document-ordering justification for a problem that does not arise. This is the flagged "prose justifies document ordering / non-circularity" pattern.
**Required**: State plainly that REARRANGE_K's RA-dom is taken from ASN-0084's Pivot/Swap domain postcondition. Delete the cycle-avoidance narration in both locations.

### Issue 4: RE-sub and RE-ext carry duplicated "we display both clauses because…" justification
**ASN-0091, "Subspace Frame" and "In-Subspace Exterior Frame"**: RE-sub: "We display both clauses because the bijection's identity behaviour on non-S V-positions is the load-bearing strengthening — it is exactly what distinguishes RE-sub's pointwise form from a weaker subspace-preservation statement…"; RE-ext: "We display both clauses because the bijection's identity behaviour on in-subspace exterior V-positions is the load-bearing strengthening — exactly what distinguishes RE-ext's pointwise form from a weaker bounded-permutation statement…"
**Problem**: Two paragraphs in different sections saying the same thing in near-identical words (the flagged "two paragraphs say the same thing" pattern). Each also re-derives that the first conjunct implies the second under RA-π — itself a trivial substitution stated twice.
**Required**: State the π-fixity-implies-arrangement-preservation substitution once (or inline), and drop the "we display both clauses because" meta-justification from both RE-sub and RE-ext.

### Issue 5: RA-adm out-of-scope enumeration and repeated deferral pointers
**ASN-0091, definition of RA-adm**: "Three families of foundation results lie outside its scope and are discharged by their own arguments rather than by RA-adm: (i) the composite-boundary properties P4★, P4a, P7a … (ii) the state-independent theorems S5 … and T0(a)/T0(b) …"; with "discharged in the per-invariant subsections below" and "handled in the dedicated 'P4a Handling' subsection below."
**Problem**: The scope-carve-out reads as essay justification of an axiom (the flagged "new prose around an axiom explains why it is needed" pattern), and it stacks multiple forward deferrals to the same downstream subsections ("subsections below," "P4a Handling subsection below"). The load-bearing content — RA-adm ranges over per-state invariants only — is one clause; the family taxonomy and deferral inventory belong in the discharge subsections where the work is actually done, not in the definition.
**Required**: Reduce RA-adm's definition to the per-state-invariant restriction. Move (or delete) the three-family taxonomy and let each discharge subsection name what it handles, without forward pointers from the definition.

### Issue 6: "ASN-0036 S3/S8 Supersession" section is methodology rationale, not specification
**ASN-0091, "ASN-0036 S3/S8 Supersession and the Move to Per-Invariant Discharges"**: "We therefore do not invoke ASN-0084's rearrangement lemmas wholesale; we give self-contained per-invariant discharges, verifying for each load-bearing invariant that its discharge depends only on a subset of pre-state invariants that survives supersession."
**Problem**: The section explains the author's proof methodology (why lemmas are re-derived rather than cited) rather than stating a system guarantee. The one substantive fact — S3/S8 are superseded by S3★/S8★ and the legacy forms fail once the link subspace is populated — is a single sentence; the surrounding "we do not invoke wholesale / we give self-contained discharges" is procedural framing.
**Required**: Keep the supersession fact and the R-RI hypothesis-failure example; delete the methodology narration.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: The ASN fixes the cut subspace at S = s_C (CS3) and the open questions correctly defer "what semantics, if any, rearrangement should carry on the link subspace." This is new operational territory, not a gap in the present ASN.

### Topic 2: Net cardinality bound across a multi-step sequence
**Why out of scope**: RE-frag★/coal★/eq★ deliberately asserts only per-step direction arbitrariness and explicitly disclaims any net-change bound; the open question "what upper bound … on the increase from a single invocation" is a future quantitative result.

VERDICT: REVISE
