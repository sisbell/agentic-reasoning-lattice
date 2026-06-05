# Review of ASN-0100

## REVISE

### Issue 1: Optional "Supplementary characterization" and the claim that exists to feed it

**ASN-0100, §Verifying the Invariants / Per-subspace span decomposition (S8★)**: "S8★ asks only for existence, but it is worth recording the shape the canonical decomposition takes over the Insertion region `{(shift(p, k), a_k) : 0 ≤ k < n}`: these `n` placements collapse into a single length-`n` run `(p, a_0, n)`."

**Problem**: This paragraph is self-admittedly beyond what the invariant requires — S8★ existence and content-subspace uniqueness are fully discharged by the C1a/M12 instantiation in the preceding paragraph. The run-merge characterization adds nothing the contract needs. Moreover, it is the *only* load-bearing consumer of claim INS.chain-shift's I-side result (`a_{k+1} = shift(a_k, 1)`, hence `a_k = shift(a_0, k)`): the placement effects (INS.M-insert) use `shift(p, k)` on the V-side, not the I-side. So INS.chain-shift — a full claim with a multi-step inductive proof (TA5-SigValid → TA5 → OrdinalShift → TS3) — exists primarily to support an explicitly-non-required paragraph.

**Required**: Either delete the supplementary characterization and the I-side portion of INS.chain-shift, or show a contract/invariant obligation that genuinely requires `a_k = shift(a_0, k)`. If the only remaining uses are the worked-example flavor sentences ("a_1 = shift(a_0, 1)"), those do not justify carrying the claim.

### Issue 2: Repeated deferral of the S8a / depth discharge to §Effect Two

**ASN-0100, §Verifying the Invariants / Post-state V-position well-formedness**: "All three regions satisfy S8a (claim **S8a**), established for the post-state at §Effect Two: Placement." — and §D-CTG★ empty case: "each Insertion position satisfies S8a by claim **S8a**, established at §Effect Two: Placement."

**Problem**: Multiple sections defer the same verification back to §Effect Two without adding content — the named "multiple paragraphs defer to the same downstream location" pattern. The S8a and INS.inv.depth discharge is fully done in §Effect Two; the later bullets are pure back-pointers, forcing the reader to context-switch to confirm a claim that has already been closed.

**Required**: Discharge S8a/INS.inv.depth once, in the section that verifies invariants (where the reader expects it), and drop the duplicate back-references — or, if §Effect Two is the intended home, remove the re-citations rather than restating "(claim S8a), established at §Effect Two."

### Issue 3: OrdinalShiftBase convention restated at every use-site

**ASN-0100, multiple sections**: the parenthetical "(with `shift(t, 0) = t`)" / "with `shift(p, 0) = p`" recurs across the precondition unpacking, the ValidInsertionPosition unpacking, §Effect Two, the worked examples, and the D-CTG★ empty case.

**Problem**: OrdinalShiftBase (ASN-0058) is a foundation convention already set up once in the bolded "Notational convention" paragraph. Re-emitting it at each use-site is the "two paragraphs say the same thing in different words" noise pattern.

**Required**: State the convention once and rely on it; remove the per-site restatements.

## OUT_OF_SCOPE

None. The "Bounding the Scope" section correctly defers DELETE, COPY, REARRANGE, link-subspace insertion, version derivation, and replication, consistent with this ASN's scope.

VERDICT: REVISE
