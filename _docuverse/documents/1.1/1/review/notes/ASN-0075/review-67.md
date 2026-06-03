# Review of ASN-0075

## REVISE

### Issue 1: Termination of SHOWDELETIONS asserted without derivation
**ASN-0075, "The SHOWDELETIONS Operation"**: "The operation always terminates with `q` true when its precondition holds."
**Problem**: Termination is a guarantee stated without grounding. Both output sets are set-builder comprehensions ranging over `dom(C)` and testing membership in `ran(M(d_A))`, `ran(M(d_B))`, and `R`. Termination depends on `|dom(C)| < ∞` (C-fin, ASN-0047) and finite arrangements (S8-fin, ASN-0036); without those, the comprehension is not obviously computable. The ASN invokes C-fin elsewhere (D-ORD) but the termination claim cites nothing.
**Required**: Ground the termination claim in C-fin and S8-fin, as D-ORD already does for output finiteness.

### Issue 2: Worked example forward-references claims before they are stated
**ASN-0075, "A Worked Example"**: "The claims D-EXH, D-IDENT, D-ORIG, and D-SYM can be checked concretely against the resulting state."
**Problem**: D-IDENT, D-ORIG, and D-SYM are introduced only in later sections (Identity Preservation, Origin Traceability, Symmetry). A reader meeting "*Verifying the claims on this state*" must skip downstream to find the statements being verified. The example verifies labels that do not yet exist in reading order.
**Required**: Move the worked example after the claim sections it verifies, or state D-IDENT/D-ORIG/D-SYM before the example, so each verification follows its claim.

### Issue 3: Decorative consequence in D-OBS
**ASN-0075, "Observational Frame"**: "Consequences: SHOWDELETIONS is repeatable on the same state (yields identical results); and it commutes with other observational queries."
**Problem**: "Commutes with other observational queries" names no queries and gives no precise sense of "commutes." It does not advance the observationality argument — the load-bearing consequences (repeatability, D-STORE) stand without it. This is exactly the decorative consequence the anti-bloat pass targets.
**Required**: Either make the commutation claim precise (which queries, what equality holds) or drop it.

## OUT_OF_SCOPE

### Topic 1: Per-occurrence (V-position-level) deletion detection
The "Classification is at I-address-set granularity" paragraph correctly scopes out distinguishing which of several V-positions holding the same I-address was removed. This is a Vstream concern (REARRANGE/DELETE mechanics) and belongs to a future ASN. The current placement as a stated non-goal is appropriate, not a finding.

### Topic 2: Witness-span finite presentation and restoration semantics
The Open Questions about span-based presentation, restoration operations, and >2-document families are genuine future territory, not gaps in this ASN.

VERDICT: REVISE
