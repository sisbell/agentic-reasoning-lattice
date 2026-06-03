# Review of ASN-0071

## REVISE

### Issue 1: Currency section restates one claim three to four times
**ASN-0071, "Currency: state dependence"**: "`find(Q)(Σ)` is a function of `Σ`. It depends only on the current state — specifically on `Σ.E_doc` and `Σ.M`. ... So `find` reads only `Σ.E_doc` and `Σ.M`." followed by "History does not enter the definition. The operation does not consult past states, past arrangements, or past transitions. It is a pure function of the present."
**Problem**: "reads only `E_doc` and `M`" is asserted as the opening sentence and re-asserted verbatim as the closing sentence of the same paragraph, sandwiching the supporting derivation. The next three sentences then say "no history" three different ways. This is the anti-bloat "two sentences say the same thing in different words" pattern.
**Required**: State the claim once, give the one-line reason (`iaddrs` and the membership predicate read only `M`/`E_doc`), and delete the bookend restatement and the triple "no history" gloss. The substantive `R`-vs-current distinction afterward should stay.

### Issue 2: Duplicate downstream deferrals in "What we do not specify"
**ASN-0071, "What we do not specify" (ii) and (iii)**: "...replica-divergent views in a distributed deployment are out of scope — see the corresponding open question." / "...layering Nelson's visibility policy ... is out of scope — see the corresponding open questions."
**Problem**: Two items in the same list each defer to the Open Questions section with the same "see the corresponding open question(s)" pointer. This is the "multiple paragraphs defer to the same downstream location" pattern; the pointers add nothing the reader cannot see one section down.
**Required**: Drop the "see the corresponding open question(s)" tails; "out of scope" already does the work, and the Open Questions follow immediately.

### Issue 3: Proof roadmap and editorial ranking are meta-prose
**ASN-0071, "The query"**: "The proof is a forward chain through a componentwise fact, totality, and prefix agreement."
**ASN-0071, "Discovery through sharing"**: "The most architecturally significant consequence concerns transclusion."
**Problem**: The first sentence enumerates the three subsection labels (*Componentwise fact*, *Totality*, *Prefix agreement*) that immediately follow it as headers — it advances no reasoning. The second is an editorial ranking ("most architecturally significant") rather than a statement of what the operation does.
**Required**: Delete the roadmap sentence; the labeled subsections are self-navigating. Drop "The most architecturally significant" and open directly with the transclusion consequence.

### Issue 4: PC closure step mis-attributed to trichotomy
**ASN-0071, "The query," Componentwise fact**: "By NAT-order trichotomy (T0), `t_p = u_p` wherever `t_p` exists with `p < #u`."
**Problem**: The preceding argument derives a contradiction only at the *first* position of disagreement ("`t` cannot first disagree with `u` at `p`"). Concluding agreement at *every* `p < #u` requires that any non-empty disagreement set has a least element (well-ordering of positions) — that least element is the one the contradiction excludes. T0 trichotomy supplies only the per-position case split (`<`/`=`/`>`), not the universal closure over all `p`. The cited justification does not establish the stated conclusion.
**Required**: Name the actual closure step — well-ordering/induction over positions excludes a least disagreement — and reserve the T0 citation for the within-position case split where it belongs.

## OUT_OF_SCOPE

(none — the deferred topics in §"What we do not specify" and the Open Questions are correctly routed to future ASNs.)

VERDICT: REVISE
