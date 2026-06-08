# Review of ASN-0102

## REVISE

### Issue 1: J1★ discharge is circular

**ASN-0102, X14 (coupling discharge), J1★ paragraph**: "COPY's range additions are a subset of `New ⊆ A`; **(BD-New) records each into `R_clo`**, and together with each other step discharging its own additions, composite-wide J1★ holds."

**ASN-0102, X14, Boundary dichotomy (BD-New)**: "If instead `a ∉ ran_{s_C}(B.M(d))` but `a ∈ ran_{s_C}(Σ_clo.M(d))`, then **composite-wide J1★ gives `(a, d) ∈ R_clo`**".

**Problem**: The J1★ discharge grounds COPY's range additions in (BD-New), but (BD-New) derives `(a,d) ∈ R_clo` *from* composite-wide J1★. The proof of J1★ thus invokes a step whose own justification is J1★. This is circular. The non-circular ground is already available — (SL) states "COPY records `(a, d)` for every `a ∈ A` (Definition)... by provenance permanence (P2) every recorded pair persists into `R_clo`" — i.e., COPY's *own* provenance write puts the pair in `R_clo`, with no appeal to J1★.

**Required**: Discharge COPY's J1★ contribution from (SL) directly (COPY records every laid-down address, so any address it makes range-new is in `Σ'.R ⊆ R_clo`). Reserve (BD-New) for the *witnessing* role (P4a), where invoking the already-assumed composite coupling is legitimate, and do not cite it inside the proof of that coupling.

### Issue 2: Forward-reference / use-site inventory in the resolution section

**ASN-0102, "The source designation and its resolution"**: "This single pre-state pinning is what makes self-transclusion (`d_s = d`) well-defined... **The downstream claims X10(b) and X15 invoke this fact rather than re-establish it.**"

**Problem**: The final sentence enumerates downstream consumers of the pre-state-pinning fact and asserts how they use it. It advances no reasoning — it is bookkeeping about where the fact is later cited, exactly the forward-reference accretion this note's classifier targets. The substantive content (pre-state pinning makes self-transclusion well-defined) is already stated in the preceding sentence and is re-derived concretely in the self-transclusion worked example.

**Required**: Delete the use-site inventory sentence. State the pinning once; let X10(b)/X15 cite it without the section pre-announcing that they will.

### Issue 3: Composite-boundary reasoning imported into an elementary-transition contract

**ASN-0102, X14, "Premise (boundary B)" through the P4★/P4a/P7a discharges**: e.g. "`ValidComposite★` evaluates its coupling and composite-boundary properties at a composite boundary `B`... Two facts of `B` are all COPY needs", and the BD/(SL)/`Σ_clo` machinery built atop it.

**Problem**: COPY is defined as a *single elementary transition*. Per ValidComposite★ the couplings (J0/J1★/J1'★) and boundary properties (P4★/P4a/P7a) are evaluated only between a composite's initial and final states — they are the composite's obligation, not an elementary step's. X14 reconstructs the opening boundary `B`, the closing boundary `Σ_clo`, the `Old`/`New` split, and a two-horn dichotomy to discharge composite-level obligations inside COPY's own spec. This is what produces the Issue-1 circularity, and the embedded-vs-standalone case analysis (J1'★ case (ii), "rejection charged to the removing step") is composite-validity attribution that does not belong to COPY's per-step contract.

**Required**: Reduce X14 to what an elementary transition owes: its frame, the per-state invariants, the transition invariant P3, and the *local* recording fact (SL) — COPY records every address it lays into the content-subspace range. The statement that a composite embedding COPY remains coupling-valid follows from (SL) plus ValidComposite★'s own boundary checks; it need not be re-proved here with a private boundary apparatus.

## OUT_OF_SCOPE

(none — the four Open Questions are appropriately deferred to future ASNs, and the note does not specify INSERT/DELETE/REARRANGE/link/version/BEBE mechanics.)

VERDICT: REVISE
