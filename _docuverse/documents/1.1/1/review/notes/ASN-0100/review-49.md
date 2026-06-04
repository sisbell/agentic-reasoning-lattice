# Review of ASN-0100

## REVISE

### Issue 1: INS.M-exhaustive is multiply-deferred and entangles the S2 proof
**ASN-0100, Formal Contract (Effect — Arrangement, exhaustiveness clause) and §Verifying / Arrangement functionality**: "The exhaustiveness clause is a property of the post-state... It is established in §Atomicity (the uniqueness argument...)" / "The S2 functionality argument in §Arrangement functionality below depends on this exhaustiveness." / §functionality: "exhaust V_{s_C}(d') by INS.M-exhaustive."
**Problem**: The exhaustiveness fact is stated in the contract, then deferred forward to §Atomicity, then pointed at again from §functionality, then re-announced in the claims table. This is exactly the forward-reference accretion pattern (multiple paragraphs in different sections deferring to the same downstream location). Worse, S2 (functionality) — the one genuinely non-trivial per-state invariant at the K.μ⁺ step — is proved in §functionality but rests on a fact "established in §Atomicity," while §Atomicity's own "After step 3's K.μ⁺" bullet verifies S8a/S8-depth/S3★/S8-fin/S8★/J0 but never independently discharges S2 at that intermediate. The reader must triangulate across three sections to confirm the regions exhaust dom(M'(d))∩s_C.
**Required**: Establish exhaustiveness inline at the effect specification (it follows directly from the composite construction: K.α/K.ρ frame M, K.μ⁻ only removes, K.μ⁺ adds exactly Insertion ∪ Shifted-right), and have §Atomicity's K.μ⁺ bullet explicitly cite the §functionality disjointness for S2. Remove the redundant forward pointers.

### Issue 2: The provenance couplings are discharged twice
**ASN-0100, §Verifying / "Provenance (R, P4★, P4a, P7a)" and §Atomicity / "After each of the n K.ρ firings of step 4"**: Both passages derive J1★, P4★, P4a, P7 (and the J1'★ relationship) for the same K.ρ firings, in different words.
**Problem**: P4★, P4a, P7a are composite-boundary properties discharged once at the boundary; re-deriving them inside the §Atomicity per-step bullet duplicates the §Provenance proof. This is the "two paragraphs say the same thing in different words" pattern.
**Required**: Keep the full discharge in one location (§Provenance) and have the §Atomicity bullet cite it, noting only that the K.ρ intermediate is the boundary state at which the obligation comes due.

### Issue 3: J0/J1★/J1'★ discharge restated across worked-example instances and the general proof
**ASN-0100, §A Worked Example ("Provenance discharge (J1★, J1'★)" interior case; "Discharge of J0, J1★, J1'★" empty case) and §Verifying / Provenance**
**Problem**: The interior worked example and the empty-case worked example each re-trace J0, J1★, J1'★ in full, and §Provenance proves them generally a third time. Concrete instances are welcome, but the two worked-example discharges restate the same three coupling arguments at length rather than exhibiting the numeric instance and citing the general proof.
**Required**: In the worked examples, show the concrete pairs entering R' and cite the general §Provenance discharge for the coupling logic, rather than re-deriving J0/J1★/J1'★ prose per example.

## OUT_OF_SCOPE

### Topic 1: COPY contrast and version-chain corollary
**Why out of scope**: §INSERT vs. COPY and INS.identity.version touch version derivation and COPY. As written they are framed as INSERT *identity* properties (fresh allocation, distinct origin) and explicitly defer COPY/version mechanics, so they are legitimate INSERT consequences rather than claims about the excluded operations — no revision required, but the boundary is worth keeping crisp so future edits do not let COPY/version mechanics accrete here.

VERDICT: REVISE
