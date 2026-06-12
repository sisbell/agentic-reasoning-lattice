# Review of ASN-0129

This note is in strong late-cycle shape: the vocabulary audit is genuinely complete, WT closes the typing gap, the PC6 converse is argued leaf-by-leaf rather than waved, the conjectures (C-reach, C-emit) are scrupulously fenced as conjectures with honest accounts of why shortcut proofs are unsound, PD0's polarity rules are individually grounded in upstream frames, and the worked trace actually computes the dynamics claims at five concrete states (including the empty-store boundary, with the vacuous-⊤ warning made explicit). I verified the trace's evaluations step by step (Σ₀–Σ₄, all three views) and they are correct. Two issues remain.

## REVISE

### Issue 1: The parity candidate's fragment characterization is an invalid inference

**ASN-0129, PC6 (ExpressiveClosure), "What the relativization costs" paragraph**: "at a *BH4-free registry* — … — counts and literals are the only ℕ-valued leaves, a parity term would be a Boolean combination of comparisons among sums of counts and literals, and that fragment supplies no halving or modular operator, no ℕ quantifier, and no evident domain expression denoting a half-sized witness"

**Problem**: The premise bounds the ℕ-valued *leaves*; the conclusion characterizes *all parity terms* — and the inference does not go through. At a BH4-free registry, PL's Boolean fragment is not exhausted by ℕ-comparison combinations: it contains terms with no ℕ-valued subterm at all — PC1 quantifications over `L_dom` and the slices with V-PRIM/V-TUP bodies (membership, `≼`, T1-order), filters, reflected-set tests. A hypothetical parity term could a priori live in that quantificational fragment (the order-and-membership analogue of the classical FO-parity question), and the assessment neither rules that route out nor records it as part of the proof obligation. The asymmetry with C-reach is what makes this a finding rather than a quibble: C-reach explicitly enumerates the three reasons shortcut citations are unsound for PL (walk atoms, counting beyond FO, built-in total orders) and states what a proof must handle; the parity assessment, facing the structurally identical gap, instead asserts a normal form that is false as stated and thereby narrows the recorded obligation to the halving-witness gap alone. The conjecture's plausibility likely survives — but the obligation as written understates what Open Question 6 must discharge for this candidate.

**Required**: Either scope the sentence to ℕ-fragment routes ("a parity term reaching the count through ℕ-valued subterms would be a Boolean combination of …") and add the quantificational Boolean route to the parity candidate's recorded obligation, parallel to C-reach's enumeration; or supply an argument that every Boolean PL term's parity-relevant content factors through count comparisons (no such argument is currently plausible, so the first fix is the realistic one).

### Issue 2: Forward-reference accretion around the content-store exclusion

**ASN-0129, PC4 / QD-audit / PC6 / "Structural reads only"**: QD-audit closes with "`dom(Σ.C)` has no base and no membership atom — the content-store exclusion's normative statement and grounds live at Structural reads only (below)"; PC4 states the exclusion in full ("no atom or domain expression reads a content value `Σ.C(a)`, the content domain `dom(Σ.C)`, or an arrangement binding `Σ.M(d)(v)`") and points to "(Structural reads only, below)"; PC6's base enumeration points a third time ("`dom(Σ.C)` has no base read at all, Structural reads only"); and "Structural reads only" then restates the same triple in different words ("no read primitive touches the content store — value or domain — and none dereferences an arrangement binding `Σ.M(d)(v)`").

**Problem**: This is the flagged accretion pattern in both of its forms: three sections defer to the same downstream location, and the exclusion itself is stated in full twice (PC4 and "Structural reads only"), with QD-audit's second clause being pure pointer prose that advances nothing ("the normative statement and grounds live at X below"). A secondary instance of the same pattern: QD-audit carries the P-tgt disjunct decomposition (residence spellable as reflected-`L_dom` membership, self-emit not) and defers to C-emit; C-emit restates the decomposition's conclusion and points back to QD-audit — a mutual-deferral pair where one site should own the content.

**Required**: One normative home for the content-store exclusion ("Structural reads only"), carrying the full statement and grounds once; PC4 cites it as the premise of its purity claim without re-enumerating the triple; PC6's parenthetical citation may stand; QD-audit's sentence reduces to the bare exclusion plus citation. For P-tgt: the decomposition lives in QD-audit (where the audit needs it) and C-emit identifies its subject in one clause without restating the residence-disjunct analysis.

## OUT_OF_SCOPE

### Topic 1: Temporal composition over PL terms
PD0–PD2 classify how a single term's truth behaves across steps, which is exactly what the note promises. The natural next layer — temporal operators over `→_sh` traces ("eventually P," "P until Q") with PL terms as atoms, giving protocol authors a verification logic rather than a stability taxonomy — is new territory. **Why out of scope**: the note deliberately ships no temporal operators and positions the dynamics classes as the designed substitute; a trace logic is a future ASN, not a gap here.

### Topic 2: Evaluation cost bounds
PC5 proves termination but states no complexity guarantees (e.g., evaluation polynomial in `|dom(Σ.L)|`, fold-nesting cost). A protocol author choosing between an audit-view trigger and an active-view trigger will eventually need cost guidance alongside the stability guidance PD0–PD2 supply. **Why out of scope**: complexity is a new analytical dimension over a correct foundation, not an error in it.

### Topic 3: The PL / ASN-0127 meet
The note draws a clean boundary against the arrangement-reading query layer ("neither subsumes the other, by design"). A combined language — triggers conditioned on `findlinks_V` results, say — would need its own dynamics theory, since ASN-0127's D-NONMONO interacts with PD0's monotone classes. **Why out of scope**: the boundary is a deliberate design commitment of this note; the joint layer is future work.

VERDICT: REVISE
