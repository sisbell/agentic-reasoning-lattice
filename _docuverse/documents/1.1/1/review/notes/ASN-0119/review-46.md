# Review of ASN-0119

The technical core of this note is sound. I verified the worked pivot and swap arithmetic position by position (R-P1/R-P2 and R-S1/R-S2/R-S3 destinations, the π tables, the composed bijection π₂∘π₁ in the atomicity section, and the middle-region displacement `w_β − w_α`), and all check out. The RA2a closure argument is correct (the non-S identity branch plus injectivity plus S8-fin), the S3★ derivation correctly routes text positions through `π⁻¹` and link positions through the frozen frame, the set-invariance factoring for the key-set-only invariants is legitimate and explicitly names its exceptions (S8★, CL-OWN, CL-UNIQ) rather than hand-waving them, the J-coupling discharges are each closed by their own empty antecedent with the content-subspace range invariance doing the genuine work for J1★, the P4a trace-induction extension handles the only new case, and the contiguity analysis (RA7c plus four boundary configurations exercising both sides) is the non-trivial wp analysis the operation actually needs. The value-degenerate identity-effect instance and the distinctness stipulation backing RA8b's inequalities both close holes a careless draft would have left open. Two items remain.

## REVISE

### Issue 1: The five-clause K.μ~-coincidence parenthetical is a forward-reference inventory, and its clause-(v) citation is wrong
**ASN-0119, "The two streams"**: "(Coincidence is a five-clause claim — K.μ~'s admissibility (i)–(v) — and the four clauses beyond non-triviality (ii) are discharged by derivations later in this note: the post-state shape package (i) … by the set-invariance argument of the invariant-preservation section …; length preservation (iii) by the depth-2 closed forms of R-PPERM/R-SPERM …; subspace preservation (iv) by RA2a; and link-subspace fixity (v) by R-NS.)"

**Problem**: Two defects, one structural and one substantive.

(a) This is a ten-line nested parenthetical sitting in the second sentence of the model-setup section, enumerating four discharge sites that all live later in the note — before RA2, RA2a, or the set-invariance argument has been introduced. The reader must skip over it to reach the substantive caveat that immediately follows ("The coincidence is not an equality of domains…"). This is exactly the use-site-inventory / multi-deferral accretion pattern: the discharge mapping is needed, but not here and not in this form.

(b) The citation for clause (v) is incorrect. K.μ~ admissibility (v) (ASN-0047) demands `π(v) = v` for every `v ∈ dom_L(M(d))` — a key-level fact about the bijection. R-NS (ASN-0084) states only the value-level identity `M'(d)(v) = M(d)(v)` on non-S positions; it does not pin π. The key-level fixity is supplied by the non-S branch of R-PPERM/R-SPERM — which the note's own RA2a derivation correctly invokes ("Every position with `subspace(v) ≠ s_C` is fixed pointwise by `π`'s non-S branch"). The parenthetical cites the wrong lemma for the one clause that is about π rather than about values.

**Required**: Reduce the claim-site text to the coincidence assertion plus one deferral sentence. Consolidate the five-clause discharge into a short paragraph placed after the invariant-preservation section, where RA2a, the shape package, and the closed forms are all in hand. In that discharge, cite the non-S branch of R-PPERM/R-SPERM for clause (v), not R-NS.

### Issue 2: Width positivity recast as an independent R-PRE demand, with a duplicated degenerate-case parenthetical
**ASN-0119, "Well-definedness, and a caveat"**: "R-PRE demands a strictly ascending cut sequence whose affected interval `[c₀, c_{n-1})` lies wholly within the active text subspace (R-PRE(iv)) and whose two moved-region widths are each ≥ 1 (a zero-width moved region is degenerate)."

**Problem**: In ASN-0084, width positivity is listed under R-PRE's *Consequences* — it is entailed by CS2's strict ascent, not a separate clause of the precondition. The note states this correctly in "Cuts and regions" ("its widths read off the R-PRE consequences"), then here recasts it as a third demand of R-PRE. Since this paragraph is precisely the one characterizing the operation's domain of definition ("defined exactly where R-PRE holds"), an auditor reading it would conclude there is an extra width condition to check beyond CS1–CS5 and R-PRE(i)–(iv); there is not. Additionally, the "(a zero-width … region is degenerate)" parenthetical appears in both sections — twice imagining a case that CS2's strict ascent already excludes, which is the reviser-drift pattern of decorating an entailed fact with a defensive aside.

**Required**: Attribute width positivity once, as a consequence of CS2, and characterize the partiality boundary by R-PRE's actual clauses. Drop both degenerate-region parentheticals.

## OUT_OF_SCOPE

### Topic 1: Rearrangement beyond depth 2 and beyond the text subspace
**Why out of scope**: The note explicitly confines itself to `s_C` at depth 2, which is the exact scope at which ASN-0084's closed-form permutations exist (CS3/CS4). A REARRANGE for deeper V-position arrangements, or a position-permuting operation on the link subspace that honours the link-placement disciplines (CL-OWN, CL-UNIQ, K.μ⁺_L's frontier), is new machinery requiring its own permutation lemmas — a future ASN, not a defect here.

### Topic 2: Concurrency, serialization independence, and prior-arrangement recoverability
**Why out of scope**: Order-independence of two unserialized rearrangements and reconstruction of a superseded arrangement from the permanent store are both correctly parked in Open Questions; neither is needed to specify the single-operation semantics this note establishes.

VERDICT: REVISE
