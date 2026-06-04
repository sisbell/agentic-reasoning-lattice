# Review of ASN-0101

## REVISE

### Issue 1: D8 claims "per-state invariant" scope but proves transition invariants too
**ASN-0101, D8**: "the post-state satisfies every foundation *per-state* invariant that the pre-state was required to satisfy. The per-state invariants fall into three groups: Group (i), the arrangement invariants (...); and Groups (ii)–(iii), the allocation, store, transition, and remaining per-state invariants."

**Problem**: The headline sentence asserts D8 covers "every foundation per-state invariant," yet the body places transition invariants squarely in scope. Group (iii) is itself titled "*transition and per-state invariants*" and lists M1 (ArrangementMonotonicity), C0 (ContentImmutability), P0, P1, P2, P3, L12a, L12b — every one quantified `(A Σ → Σ' :: …)`, i.e., transition invariants, not per-state. Group (ii) likewise includes L12 (LinkImmutability), also a transition invariant. A precise reader cannot reconcile "every foundation per-state invariant" with a group explicitly labelled "transition and per-state." The proof itself is sound (the frame-fixed argument discharges transition invariants too — `dom(M')=dom(M)`, `C'=C`, `L'=L`, `E'=E`, `R'=R` give M1/C0/L12/P0–P3 directly), so this is a defect in the *stated* scope, not the argument.

**Required**: Rephrase the D8 statement to "every foundation per-state invariant and every transition invariant the pre-state transition discipline imposes" (or equivalent), so the umbrella matches the group labels. As written, the headline undersells and contradicts what D8 proves.

### Issue 2: Implementation commentary the ASN itself declares irrelevant (anti-bloat)
**ASN-0101, D6 justification**: "Gregory's `tumblersub` uses an exponent-guarded subtraction… positional ordering puts text addresses entirely below link addresses… Two unrelated mechanisms — arithmetic short-circuit and positional ordering — converge on the same abstract guarantee. The abstract specification does not care which mechanism is used; it requires only the guarantee itself."

**Problem**: D6's actual proof is a single line ("The effect clauses of D0 state that the post-state agrees with the pre-state on every V-position in subspaces other than `S`"). The two implementation paragraphs that follow do not advance that proof, and the closing sentence concedes as much — prose that ends by declaring its own subject irrelevant is the anti-bloat tell. The same pattern recurs in "What shifts": the two-phase "knives"/POOM-crum protocol paragraphs are immediately followed by "The abstract specification is silent on the tree structure but does require *some* such mechanism." This is implementation mechanics occupying a justification slot whose abstract content is one sentence.

**Required**: Trim the mechanism walkthroughs to the load-bearing fact (subspace isolation holds; the abstract spec is mechanism-agnostic) or relocate to a single dedicated implementation-evidence aside. Flagging placement, not the existence of the evidence.

## OUT_OF_SCOPE

### Topic 1: Reconstruction / reversibility mechanisms
The Open Questions (DEL+INSERT recovery, orphan re-discovery, causal ordering across transcluding documents) correctly defer versioning and rediscovery to downstream ASNs. No coverage gap here — these are future territory, not errors in this ASN.

VERDICT: REVISE
