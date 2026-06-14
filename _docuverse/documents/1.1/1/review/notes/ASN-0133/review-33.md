# Review of ASN-0133

This is strong, careful work — the H-RF/H-W separation, the three-case analysis of non-grow-only reachability (cases 1/2/3), and the regime-form reading of H-SFAIR through Q-EXT are all sound and non-trivial. I verified the core termination logic (Q1 absorption, Q5 injection, Q5a bound, Q6 regimes (i)/(ii), the grow-only/non-grow-only split, H-SFAIR ⟹ H-FAIR scoping) and the heterogeneous-rebuild worked example (value-preservation at Σ*). They hold. The REVISE items below are a precision defect in the fire taxonomy and the meta-prose accretion the anti-bloat classifier asks for.

## REVISE

### Issue 1: "real fire" conflates *trigger-true* with *state-advancing / trigger-consuming*

**ASN-0133, H-FAIR**: "real-fired (a non-no-op fire of (ρ, x) at a step past k)" … "a no-op fire discharges nothing — it neither advances the state nor consumes the trigger."

**Problem**: The note keys "no-op" on the trigger (RG: "if T_ρ(x, Σ) = ⊥, a no-op"), so "real" = trigger-true. But it then characterizes no-op as "neither advances the state nor consuming the trigger," implying real fires do both. Neither follows for a general registry:

- A trigger-true fire whose emission is an **idem=⊤ dedup hit** leaves `Σ' = Σ` (ASN-0128 I1: "No step: Σ' = Σ"). So a "real" (trigger-true, non-no-op) fire can advance the state by nothing.
- A real fire of a **non-extinction-disciplined** rule need not consume its trigger (only X-DEF forces that).

So H-FAIR's "real-fired" discharge can be vacuous (the occurrence's index is consumed, but the trigger stays true at the post-state, re-arming immediately). This is **benign for the load-bearing results** — extinction discipline forbids both pathologies (X-DEF would be violated by a Σ'=Σ trigger-true fire; Q3's audit-slice argument rules out the dedup hit), and H-RF excludes any vacuous-real-fire loop (each iteration is a real fire) — but the *characterization* as stated is wrong for the "any registry" generality Q6 claims, and a careful reader cannot tell whether a dedup-hit fire is a no-op or a real fire.

**Compounding, worked example ("A reached terminal state")**: "t is in-domain but trigger-false — discharged by in-place falsification, not removal." But T_P(t) was falsified at Σ₁ by ρ_P's own **real fire** (extinction), then held false by SF — not by an "in-place falsification" step, which H-FAIR defines as a discharge mechanism *distinct from* real-firing. The Σ₀ occurrence of (ρ_P, t) was discharged by real-firing; t's Σ₂ status is the SF aftermath. The label mis-assigns the discharge to the wrong H-FAIR category.

**Required**: Define "real fire" as "trigger-true fire," explicitly decoupled from state-change and trigger-consumption; state that H-FAIR's real-fired discharge is *effective* (consumes the trigger) only under extinction discipline, and that vacuous real fires are excluded by H-RF. Correct the worked-example parenthetical to "discharged by real-firing at Σ₁; remains in-domain-but-false at Σ₂ (the environment never unflagged t), SF-permanent thereafter."

### Issue 2: the H-RF/H-W separation is stated in full once, then re-stated or deferred-to from four further sites

**ASN-0133, H-RF / H-W / Q5 / Q5a / Q6**: The separation is given in full at H-RF ("The H-RF/H-W separation. H-RF bounds only the fires; H-W bounds trigger-true step-instances … the two come apart at starvation …"). It is then re-explained at H-W ("but is no usable route to it, for the reason drawn in full at the H-RF/H-W separation above"), re-touched at Q5 ("Extinction's leverage is elsewhere … it does not discharge H-W"), and cited verbatim from Q5a and Q6 — both reading "(the H-RF/H-W separation, H-RF)".

**Problem**: This is the named anti-bloat pattern — multiple paragraphs in different sections deferring to one canonical location, and two passages (H-RF's statement, H-W's re-explanation) saying the same thing in different words. The point is established once; the four downstream sites need only *use* H-RF, not re-justify why it differs from H-W.

**Required**: Keep the full separation at H-RF (or at H-W). At Q5/Q5a/Q6 drop the back-deferrals and the re-explanation; let those claims stand on H-RF directly without re-litigating the distinction.

### Issue 3: "reaching and holding splits by the grow-only line" deferred forward three times

**ASN-0133, Q6 / worked example / worked "Quiescence"**: Q6 develops the grow-only-vs-non-grow-only reaching/holding split at length; the worked-example aside then forward-defers it ("reaching and holding quiescent_R splits by the grow-only line, taken up under Quiescence below as an instantiation of Q6"); and the worked "Quiescence" paragraph re-states it ("Reaching and holding quiescent_R then split by the grow-only line of Q6").

**Problem**: The same split is announced, deferred, and re-applied across three slots. The forward pointer in the work-bound aside ("taken up under Quiescence below") is exactly the "defer to the same downstream location" pattern; the re-statement in "Quiescence" is the substance Q6 already carries.

**Required**: State the split once in Q6. In the worked example, instantiate it (resolver grow-only → reaches-and-holds under weak fairness; producer non-grow-only → defers to regime (i)/H-SFAIR) without the forward pointer or the re-announcement.

### Issue 4: use-site inventories and self-referential framing in structural slots

**ASN-0133, RG**: "every property below is a property of contracts and substrate state, never of algorithms, and every termination claim below is read universally over the admissible choices."
**Opening paragraph**: "The note's discipline is to put each hypothesis where it belongs — what the substrate guarantees unconditionally (recognizability, absorption), what a rule author can make checkable at registration (at-most-once firing), and what remains assumption (fairness, finite real fires …)."
**Q3**: "its scope fixes its standing against this note's own checkable/meta-level line, the line that disqualifies H-W and bounded domain growth precisely for quantifying over reachable states."

**Problem**: The RG sentence is a forward use-site inventory of how every later result reads; the opening sentence is a section-preview essay of the note's own structure; the Q3 clause is self-referential framing about the note's categorization scheme rather than the content of the condition. None advances the local reasoning — the reader skips past them to reach the claim. (The concrete counterexamples around them — the cmt-emits-res spinner, the starvation σ, cases 1/2/3 — are *not* meta-prose and should stay.)

**Required**: Delete the RG forward-inventory (the contracts-not-algorithms point is made where the body is excluded). Cut the structure-preview clause from the opening to the load-bearing statement (termination is conditional; hypotheses are named, not smuggled). In Q3, state the reachable-vs-schema-level decidability point directly without the "this note's own … line" framing.

## OUT_OF_SCOPE

### Topic 1: semantic cost of audit-slice rule domains

The worked example's resolver takes domain `L_cmt` (audit slice), which by construction includes nullified/born-nullified comment tuples — so the resolver fires on retracted comments. The note justifies the audit *trigger* spelling for SF-ness ("The audit spelling is the design choice, made checkable") but does not address that an audit *domain* makes rules process withdrawn content.

**Why out of scope**: This is an application-modeling tradeoff (audit domains: SF/terminating but process retracted content; active domains: semantically tighter but non-SF, needing H-W). ASN-0133's subject is termination, and the audit choice is correct *for that subject*. The semantic consequence belongs in an application-layer note that selects rule domains against domain semantics, not in this substrate note.

VERDICT: REVISE
