# Review of ASN-0133

## REVISE

### Issue 1: The worked example's "iff" contradicts Q5a's own strict-implication result

**ASN-0133, Worked composition (Bound)**: "Hence real fires ≤ |targets the environment ever flags| + |comments ever| … — so the registry's real fires are finite, its work terminates, **iff** that flagged population, and any direct environment comment traffic, is bounded."

**Problem**: This asserts a biconditional — real fires finite ⟺ flagged population bounded — whose forward direction (real fires finite ⟹ flagged population bounded) is false, and is established false **by this very note** at Q5a.

Q5a states: "In the open sequence the domain bound is *strictly stronger* than H-RF: it implies H-RF … but **H-RF does not imply it** — a fair scheduler facing an environment that flags infinitely many distinct targets and retracts each before its fire keeps the real-fire count at zero while `⋃_k [D_ρ]` grows unbounded. So Q5a is a genuine *route*: a *sufficient* condition on external input."

Instantiate exactly that counterexample in the worked registry: the environment flags `t₁, t₂, …` and unflags each before `ρ_P`'s scheduled fire. A fair scheduler discharges each trigger-true occurrence by *removal* (H-FAIR's removal escape), so there are **zero** real fires (H-RF holds), zero comments deposited, yet `⋃_k [D_{ρ_P}] = {t₁, t₂, …}` is unbounded (flagged population unbounded). "Real fires finite" is true while "flagged population bounded" is false — the iff's forward direction fails. The worked example therefore re-asserts precisely the implication Q5a went to lengths to deny, and labels as *necessary* (`iff`) what Q5a labels *sufficient*.

**Required**: Change `iff` to `if` (sufficient, not necessary), and reconcile with Q5a — the bound is `real fires ≤ |flagged| + |comments|`, so *bounded input ⟹ finite work*, but not conversely in the open model. The point Q5a is at pains to make (open ⟹ strict one-way; closed ⟹ biconditional) is undone by the worked example claiming the biconditional.

### Issue 2: The "at-most-once is registration-checkable" formulation is restated near-verbatim 4–5 times (anti-bloat)

**ASN-0133, Q-EXT / Q5a / Q6 / Worked composition / intro / "What this note commits"**: the single fact — *for Marker-pattern rules, at-most-once-per-argument is registration-checkable because the SF spelling is decided by the spelling class and the extinction discipline reduces to a decidable syntactic match (the fire emits exactly the witness the trigger's ∃ is missing)* — is spelled out, in nearly identical words, in:

- Q-EXT: "The check is registration-time and spelling-level … with the extinction half here in Q3's decidable-match case (the fire emits exactly the marker the trigger's `∃` is missing) …"
- Q5a: "at-most-once-per-argument is a registration-time fact … the SF spelling decidable by the spelling class, and the extinction discipline by a strong-enough contract whose Q3 obligation reduces, for these rules, to a decidable syntactic match (each fire emits exactly the witness its SF trigger's `∃` is missing)"
- Q6: "at-most-once-per-argument (Q-EXT, checkable at registration … from both the SF spelling, via the spelling class, and the extinction discipline, whose Q3 obligation reduces there to a decidable syntactic match)"
- Worked composition: "each contract depositing exactly the witness its trigger's `∃` quantifies over … 'strong enough' is settled by syntactic comparison of trigger spelling against emission form"

The companion editorial point — *H-RF, not H-W, is the operative hypothesis; H-W is a strictly-stronger foil* — is likewise re-stated in the commit-list, the H-RF definition ("This — not H-W — is the operative hypothesis"), Q5a ("it does not establish H-W"), Q6 ("exactly why the hypothesis is H-RF rather than H-W"), and W/H-W ("not a usable route … but a foil").

**Problem**: This is the "two paragraphs say the same thing in different words" pattern the anti-bloat classifier targets, compounded across five sites each. The reader who has absorbed Q-EXT + Q3 re-encounters the same sentence reassembled in Q5a, Q6, and the worked example. None of the repetitions advances the argument; they re-establish an already-established fact.

**Required**: State the formulation once (Q-EXT, against Q3's decidable-match case) and have Q5a/Q6/Worked-composition cite it rather than re-derive it. Likewise consolidate the "H-RF is operative / H-W is a foil" point to its home (W/H-W) and cite. The "What this note commits" bullets for Q-FLIP and Q5/Q5a/Q6 duplicate their sections' editorial framing verbatim and can be cut to claim labels.

### Issue 3: Q0's "view-stable" enumeration omits `target_of`

**ASN-0133, Q0**: "Everything else a Boolean trigger or a QD domain can read — the verdict/optional atoms `is_in_chain`, `tip`, `age`, `targets_keyed` (never UV-rewritten, by UV's Verdicts-and-optionals and Booleans clauses) … — *is* genuinely view-stable."

**Problem**: This list claims to cover "everything else" (the residual after the view-parameterized four and the six UV-rewritten collections), but the very UV clause it cites — "tip, **target_of**, age, and targets_keyed report the active structure's verdict" — names `target_of`, a `T ∪ {⊥}`-valued fixed-view atom that is dropped from the list. Soundness survives (`target_of` is in fact view-stable, so it needs no rebuild and the conclusion that every view-sensitive constituent can be moved to a common view is unaffected), but the enumeration that carries Q0's "for *every* registry" claim is incomplete as stated.

**Required**: Add `target_of` to the view-stable list (or replace the explicit list with the category "all BH2/BH3/BH4 verdict-, optional-, and `Map_fin`-valued atoms, which UV never rewrites").

## OUT_OF_SCOPE

### Topic 1: Contract realizability (does a `Post_ρ`-satisfying emission set exist at a trigger-true state?)

RG defines a real fire as "the application of *some* emission set satisfying `Post_ρ`," and H-FIN constrains such sets to be finite — but nothing requires `Post_ρ` to be *satisfiable* at a trigger-true `(x, Σ)`. An unsatisfiable contract on a persistently-trigger-true argument cannot be discharged by real-firing, so a fair scheduler may not exist for it (H-FAIR's "real-fired" escape is unavailable, and if the environment never removes/falsifies, no fair σ exists). A `register`/well-formedness obligation "every registered rule's contract is satisfiable at every trigger-true reachable state" would close this, but it is rule-well-formedness territory adjacent to the deferred scheduler/activation layers.

**Why out of scope**: This is a realizability hypothesis the note could name but its absence does not make any stated claim wrong — the termination theorems are conditional and reasonably presuppose fireable rules. It belongs with the activation/scheduler machinery the note explicitly defers, not in a revision of the present claims.

VERDICT: REVISE
