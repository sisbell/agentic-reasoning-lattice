# Review of ASN-0103

## REVISE

(none)

I checked the load-bearing arguments specifically:

- **The frontier identity `D_A = E ∩ S(A,2)`.** Both inclusions hold. The hard direction (`D_A ⊆ S(A,2)`) is genuinely proven via the T4b parse: `Document(e) ∧ parent(e)=A ∧ #e=#A+2` forces `e = A.0.D(e)` with `#D(e)=1`, hence canonical `[A,0,n]`. The length filter `#e=#A+2` correctly excludes version-chain elements, which carry length `≥ #A+3` (a version off a length-`#A+2` document via `inc(·,1)` is length `#A+3`, preserved-or-grown thereafter). This is the one place collision could creep in and it is handled.

- **Both branches of the boundary split** (`D_A = ∅` → `inc(A,2)`; `D_A ≠ ∅` → `inc(max(D_A),0)`). Document-level (`zeros=2` via B5/B5a), validity (B6 bound `zeros(A)+1=2≤3`, TA5a), and freshness (`d ∈ S(A,2)\D_A = S(A,2)\E ⟹ d ∉ E`, covering *all* of E, not just `D_A`) each discharged.

- **The worked example is concrete and load-bearing** — it exhibits a version `v1` that satisfies the *unrestricted* `Document(·) ∧ parent=A` predicate yet must be excluded, and shows the unfiltered choice would re-baptise `[1,0,1,0,1,2]`, colliding with a future fork. This verifies the necessity of the length restriction against a specific scenario, not just its sufficiency.

- **Ownership derivation (CND.own)** spells out prefix transitivity component-wise rather than asserting it; `A ≼ d` is justified from the `[A,0,j]` emission form. Effective-ownership is explicitly left open and routed to a single Open Question, not hand-waved as established.

- **Invariant discharge** is partitioned into directly-verified / vacuous-on-`dom(M'(d))=∅` / frame-inherited, and the two non-trivial cases (S7d, ActivatedEmission) name their witness `A_doc(A)`, with activation supplied by the standing assumption CND.A-act — which is legitimately owed by out-of-scope account provisioning.

- **Coupling** (J0, J1★, J1'★) is vacuous since no `K.α`/content-`K.μ⁺`/provenance step occurs; atomicity follows from the single-`K.δ` decomposition. Correct.

I also looked for forward-reference accretion per the anti-bloat classifier: `CND.A-act` is referenced three times but each is a load-bearing use of a named assumption, not meta-prose; there is a single deferral pointer ("effective ownership — see Open Questions") with no duplicate deferrals to the same site; no "Scope/Rationale/Why-needed" sub-paragraphs around axioms; no ordering-justification prose. Nothing to flag.

## OUT_OF_SCOPE

(none — the ASN correctly confines itself to document allocation; forking, content/link allocation, and account provisioning are deferred without intruding on the claims.)

VERDICT: CONVERGED
