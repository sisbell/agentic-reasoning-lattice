# Review of ASN-0075

## REVISE

### Issue 1: Use-site pointer padding the finiteness/termination argument
**ASN-0075, "The SHOWDELETIONS Operation" (wp paragraph)**: "...whose membership tests are bounded by the finite arrangements (S8-fin, ASN-0036) and the finite relation `R ⊆ dom(C) × E_doc` (P7, ASN-0047); D-ORD records the finiteness of each output half where it is consumed."
**Problem**: The termination argument is already complete at the semicolon — C-fin gives the finite index set, S8-fin and P7 bound the membership tests. The trailing clause "D-ORD records the finiteness of each output half where it is consumed" is a pure use-site cross-reference to a downstream claim; it advances no step of the wp argument and is exactly the kind of pointer the reader must skip past. This is the use-site-inventory pattern the anti-bloat pass targets.
**Required**: Delete the clause "; D-ORD records the finiteness of each output half where it is consumed."

### Issue 2: Observationality asserted three times across three sections
**ASN-0075, SHOWDELETIONS definition vs. wp section vs. "Observational Frame"**: definition site — "it writes no state component (D-OBS)"; wp section — "Because SHOWDELETIONS writes no state component (D-OBS), wp computations for state-level predicates pass through unchanged..."; then the full statement at D-OBS.
**Problem**: The single fact "writes no state component" is stated three times in different words across three sections. The wp-section use is load-bearing (it derives the pass-through rule), but the definition-site pre-assertion `(D-OBS)` is a forward reference that duplicates a claim with its own dedicated section, leaving two restatements of one fact before D-OBS is reached. This is the "same thing in different words" / forward-deferral accretion pattern.
**Required**: State observationality once at D-OBS. Drop the parenthetical pre-assertion at the definition site; the definition can simply describe what the operation reads and returns without pre-claiming the frame result.

## OUT_OF_SCOPE

### Topic 1: Per-occurrence (Vstream-position) deletion visibility
**Why out of scope**: The note correctly scopes out distinguishing which of several V-positions holding a shared I-address was removed — this is a Vstream concern, not an I-address-set classification, and the note states this explicitly rather than hand-waving it.

### Topic 2: Multi-document SHOWDELETIONS, span presentation, restoration coupling
**Why out of scope**: The Open Questions raising >2-document generalisation, contiguous-span presentation, and restoration guarantees are genuine future territory, not gaps in the binary observational operation specified here.

VERDICT: REVISE
