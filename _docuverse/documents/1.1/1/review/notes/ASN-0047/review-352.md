# Review of ASN-0047

## REVISE

### Issue 1: Clause (v) of K.μ~ admissibility is given two incompatible boundaries

**ASN-0047, *Decomposition of K.μ~***: The definition states "π is admissible iff (i) ... (v) π is *link-subspace fixing*", making (v) a defining conjunct of admissibility. The very next prose then says: "What enforces (v) is therefore the *realization*, **not the admissibility criteria (i)–(iv)**: K.μ~ realizes only link-fixing π ... the criterion thus characterizes exactly the realizable π set, rather than being deduced from (i)+(iv)+CL-UNIQ." Later, the *Necessity and sufficiency* paragraph says "Necessity assumes π admissible, so subspace-preservation (iv) and link-fixity (v) both enter as hypotheses — (v) being the explicit fifth admissibility criterion."

**Problem**: The text cannot decide whether the admissibility predicate is (i)–(iv) or (i)–(v). The phrase "the admissibility criteria (i)–(iv)" explicitly excludes (v) from admissibility, while the "iff (i)…(v)" definition and the necessity proof treat (v) as a defining conjunct that "enters as a hypothesis." A precise reader cannot tell whether, in the necessity argument, "π admissible ⟹ π link-fixing" is true *by definition* (if (v) ∈ admissibility) or *by realization* (if admissibility is only (i)–(iv) and realizability is a separate notion). The two readings give the necessity proof different logical content. This is exactly the reviser-drift pattern flagged for this note: defensive prose accreted to argue non-derivability has left the core definition self-contradictory.

**Required**: Fix one boundary. Either (a) admissibility ≡ (i)–(v), and (v) is a genuine defining conjunct that the *realization* happens to guarantee (in which case delete "not the admissibility criteria (i)–(iv)" and rephrase as "(v) is not *derivable from* (i)–(iv)+CL-UNIQ, but is guaranteed by the full-clearance realization"); or (b) admissibility ≡ (i)–(iv) and *realizability* is the strictly stronger notion adding (v), in which case the "iff (i)…(v)" definition and the necessity proof's "(v) enters as a hypothesis" must be re-stated against realizability, not admissibility. As written, the necessity/sufficiency theorem is stated against an ambiguous predicate.

### Issue 2: Redundant non-derivability restatement in the same passage

**ASN-0047, *Decomposition of K.μ~***: The clause-(v) passage asserts non-derivability twice in adjacent sentences — first "Clause (v) is a genuine fifth criterion, **not** derivable from (i)–(iv) + CL-UNIQ", then "the criterion thus characterizes exactly the realizable π set, **rather than being deduced from (i)+(iv)+CL-UNIQ**." Between them sits a logical-status sentence ("What enforces (v) is therefore the realization, not the admissibility criteria (i)–(iv)") that asserts no object-level fact about the operation.

**Problem**: Two sentences state the same claim (v is not a consequence of the other clauses) in different words, with a meta-sentence about "what enforces" the criterion wedged between — none of which advances the proof. The concrete link-swap counterexample carries the entire load; the restatements and the logical-status sentence are the defensive meta-prose this note's classifier targets. (The counterexample itself is fine — only the surrounding restatement is flagged.)

**Required**: Keep the counterexample and one statement of non-derivability; remove the second restatement and the "what enforces (v)" framing sentence (which is also the source of Issue 1).

## OUT_OF_SCOPE

None — the Scope section and Open Questions correctly fence off named operations, authorization, concurrency, and enfilade internals, and the ASN does not smuggle claims about them into normative text.

VERDICT: REVISE
