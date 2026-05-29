# Review of ASN-0036

## REVISE

### Issue 1: Meta-prose claiming the document does not repeat itself
**ASN-0036, S8 existence proof, "Non-canonicality" paragraph**: "Whether such coarser runs occur and how many there are is operations-layer-determined ... This is the single statement of run-cardinality non-canonicality; the Postconditions corollary and Open Questions do not re-defer to the operations layer."
**Problem**: The clause after the semicolon advances no reasoning about correspondence runs. It is a claim about the document's own bookkeeping — a promise not to repeat a deferral elsewhere. This is exactly the accreted meta-prose the precise reader must skip past.
**Required**: Delete the sentence "This is the single statement ... operations layer." State the non-canonicality fact once and stop.

### Issue 2: Defensive prose explaining what is *not* invoked / *not* derived (S8a)
**ASN-0036, S8a proof and Preconditions**: "the conjuncts follow from this element-field commitment together with T0's ℕ-valued carrier, without appeal to T4's field-segment constraint (which governs whole N.0.U.0.D.0.E addresses, not bare fields)." and "(Note: S7c's `#E(a) ≥ 2` ... is the architectural parallel that motivates the depth-≥-2 definition for V-positions; the definition is an independent commitment about V-positions, not derived from S7b or S7c.)"
**Problem**: Both passages are reviser drift — they explain why a foundation clause is *not* used and why the depth bound is *not* derived from S7b/S7c. The argument needs the positive content (zeros = 0 and positivity follow from the element-field commitment + T0); the negations are defensive residue from prior cycles.
**Required**: State the derivation positively. Drop the "without appeal to T4" parenthetical and the "(Note: ... not derived from S7b or S7c)" clause; the Depends list already omits T4 and S7b/S7c, which is the correct place to record non-dependence.

### Issue 3: Parentheticals justifying why a precondition is omitted (OrdAddHom, OrdAddS8a)
**ASN-0036, OrdAddHom Preconditions**: "(The bound `actionPoint(w) ≤ m` is not stated separately: ActionPoint's contract in ASN-0034 already gives `1 ≤ actionPoint(w) ≤ #w`, and `#w = m` then forces `actionPoint(w) ≤ m`.)" and **OrdAddS8a Preconditions**: "(The `actionPoint(w) ≤ m` bound is inherited as derived at OrdAddHom above.)"
**Problem**: These explain document-internal sourcing of an omitted bound — defensive meta-prose plus an internal use-site back-reference. They do not advance the lemma.
**Required**: Either include the bound silently (it follows trivially) or drop the parentheticals. The cross-internal "inherited as derived at OrdAddHom above" should go.

### Issue 4: Duplicated derivation of D-SEQ
**ASN-0036, paragraph preceding D-SEQ vs. D-SEQ proof**: The pre-statement paragraph ("We now derive the general form. By D-CTG-depth (when m ≥ 3) or trivially (when m = 2 ...) ... D-CTG restricted to the last component forbids gaps ... S8-fin bounds the maximum ... Thus:") reproduces the entire argument that the proof then re-executes as Steps 1–4.
**Problem**: Two passages in the same section say the same thing. The pre-statement paragraph is the proof in miniature.
**Required**: Keep one. Either let the pre-statement paragraph stand as the proof, or reduce it to a one-line motivation and let Steps 1–4 carry the argument.

### Issue 5: Repeated deferral of link-subspace contiguity to a future ASN
**ASN-0036, "Arrangement contiguity"**: the opening ("link-subspace contiguity semantics are deferred to a future ASN"), the *Remark* (which re-discusses the link subspace and its identifier `S = 2`), and the post-D-CTG sentence ("they are not claimed to hold for the link subspace `S = 2` or any other subspace") all defer the same out-of-scope topic.
**Problem**: Three paragraphs in one section defer to the same downstream location — the compounding pattern the classifier flags.
**Required**: State the text-subspace restriction once. The *Remark*'s only load-bearing content (the `0` in `N.0.U.0.D.0.2.1` is a separator, not a subspace identifier) can be folded into S8a's definition; the rest is a restatement of the deferral.

### Issue 6: S9 trailing essay listing downstream guarantees "none is derived here"
**ASN-0036, S9**: "The asymmetry is deliberate and load-bearing: the downstream guarantees Nelson draws from it — link survivability, version reconstruction, transclusion integrity, origin traceability — all rest on S0's preservation of I-addresses, though none is derived here."
**Problem**: Forward-looking essay enumerating things the ASN explicitly does not derive. Combined with the dual statement that S9 is "the directional reading of S0" (stated in the bold claim and again in the Properties table as "no formal content beyond S0"), this is bloat around a corollary that has no independent content.
**Required**: Drop the "downstream guarantees ... none is derived here" sentence. One statement that S9 is the directional reading of S0 suffices.

### Issue 7: Redundant double-citation in subspace_I postcondition (b)
**ASN-0036, subspace_I Depends**: "T4 (HierarchicalParsing, ASN-0034) — positive-component constraint underwriting postcondition (b); T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — componentwise positivity within the element field, reinforcing postcondition (b)."
**Problem**: Postcondition (b) is `subspace_I(a) ≥ 1`. Two foundation citations are listed for the same one-step fact, with T10a.4 "reinforcing" — a use-site inventory rather than a load-bearing dependency.
**Required**: Cite the single clause that delivers `E(a)₁ ≥ 1` (T4's positive-component constraint on present fields, via S7b/T4b). Drop the "reinforcing" T10a.4 entry unless it discharges a step T4 does not.

### Issue 8: ValidInsertionPosition precondition incomplete for its own postcondition
**ASN-0036, ValidInsertionPosition (non-empty case), Preconditions vs. Postcondition (d)**: Preconditions list only "D-CTG holds on V_1(d)"; postcondition (d) asserts the explicit form `v = [1, 1, ..., 1 + j]`.
**Problem**: The explicit form (d) is derived from `min(V_1(d)) = [1, ..., 1]`, which is D-MIN, and the enumeration of positions relies on D-SEQ. These appear in Depends but not in Preconditions. A reader cannot discharge postcondition (d) from the stated preconditions alone.
**Required**: Add D-MIN (and D-SEQ) to the Preconditions, or weaken postcondition (d) to what D-CTG alone yields.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG/D-MIN, subtraction homomorphism, and depth-choice consequences
**Why out of scope**: These are correctly held in Open Questions (whether DELETE/INSERT/COPY/REARRANGE preserve D-CTG/D-MIN, the conditions for `ord(v ⊖ w) = ord(v) ⊖ w_ord`, and the round-trip property). They belong to the operations layer, which this ASN explicitly excludes. No revision needed — they are not claimed here.

### Topic 2: Link-subspace (S = 2) contiguity semantics
**Why out of scope**: Link addressing is deferred per the Scope section. The *substance* is correctly out of scope; only the triplicated deferral prose (Issue 5) is a finding.

VERDICT: REVISE
