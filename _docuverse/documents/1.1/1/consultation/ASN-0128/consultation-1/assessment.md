# Channel Assignment — ASN-0128 review-1

**Date:** 2026-06-10 15:34

## Issue 1: Where the idem check lives — transition relation or operation surface — is unresolved, and the blanket transfer claim depends on the answer
Reason: The note's own text already implies the answer (idem is "read by the operations and predicates of this note, never by the gate"), so the locus is the surface operation with `→_sh` unchanged and P5 preserved; the projection lemma is formal work following ASN-0126's existing apparatus. Fix is internal.

## Issue 2: I1's dedup-hit branch is underdetermined and silently violates the inherited Emit_K contract
Reason: The ordering and uniqueness-invariant gaps are internal formal work (the review sketches the induction), but whether the home document participates in link identity — cross-home versus per-home dedup — is a normative design decision the ASN cannot derive from its own content.
Nelson question: In the design, is a link's identity tied to the document it lives in — i.e., are two links with identical endsets homed in different documents two distinct links, or the same assertion stated twice?

## Issue 3: "Enforced precondition" P-tgt contradicts Open Question 3's fallback-admit option, and the fallback re-enables total sterilization through the wrapper
Reason: The review demonstrates rejection semantics is forced by the note's own load-bearing containment claims, so the fix (fix rejection in S3/DR, restrict OQ3 to gate refinement) is fully determined internally.

## Issue 4: B2's `tip`/`chain` are ill-defined under branching and cycles, which the note's own text shows are possible
Reason: Choosing between restricting B2 to functional/acyclic states versus defining it on general digraphs depends on whether supersession was meant to be linear or branching — a design-intent question — and on whether the implementation enforces single successors or prevents cycles.
Nelson question: Was document supersession intended to be a strictly linear chain per document, or does the design admit branching (one document superseded by multiple variants)?
Gregory question: Does udanax-green's versioning or link machinery allow a document to have multiple direct successors, and does anything in the code prevent cyclic successor/link structures?

## Issue 5: The predicate layer is typed at addresses while the data is spans — coverages are infinite address sets, and "the G-address" is ill-typed
Reason: The choice between a canonical span-to-address convention and retyping results as span sets should follow what the implementation's query surface actually returns, which is evidence Gregory holds.
Gregory question: What do udanax-green's link-query operations (find-links-from-to, follow-link, retrieve-endsets) return — link tumbler addresses, spans/spec-sets, or both — and how do results denote endset contents?

## Issue 6: D1's formula and B1's implicit exclusion define `members(K)` twice, and "audit view" conflates two different escape hatches
Reason: The view taxonomy (audit/active/default), the definition-versus-rewrite restructuring, and adding B1×B2 to the open questions are all derivable from the note's existing definitions of `L_K` and `A_K`. Fix is internal.

## Issue 7: B4 promises wall-clock semantics over a state that has no clock
Reason: Whether to introduce a time component or restate B4 ordinally hinges on whether the implementation's state actually records wall-clock time anywhere — empirical evidence about udanax-green's state, not design philosophy.
Gregory question: Does udanax-green's persistent state record wall-clock timestamps anywhere (e.g., at document, version, or link creation), or is all ordering purely structural (chain indices, tumbler order)?

## Issue 8: The three shipped registrations have no designated coverage classes
Reason: The parameter mechanics follow ASN-0086's `s_L`/`s_C` precedent internally, but whether the shipped classes should be open substrate parameters or fixed conventional addresses depends on whether the implementation reserves conventional tumblers for standard link types.
Gregory question: Does udanax-green reserve conventional tumbler addresses for standard link types (e.g., jump links, quote links), and if so, what are they and where are they defined?

## Issue 9: I4's unconditional "the winner produces the active tuple" is false in the born-nullified case that I5 is careful to exclude
Reason: The fix is exactly the caveat I5 already carries, plus a superscript correction — both stated in the review and derivable from the note's own I3/I5. Internal.

## Issue 10: DR's antichain step is applied to an address that is not yet a link address, and the wp claim names no postcondition
Reason: The review supplies both the post-state instantiation and the alternative state-local argument, and naming the wp's postcondition is a matter of making the note's existing "wp Case-1 parallelism" explicit. Internal.

## Issue 11: "B2/B3" names a lemma citation and a behavior pair simultaneously
Reason: Purely editorial disambiguation — qualify the citation as ASN-0126's lemmas. Internal.

## Issue 12: Reference to a non-foundation ASN
Reason: The note already describes the deferred territory in its own words ("composition rules over the atomic default predicates and the behavior-unlocked predicates"); dropping the number is editorial. Internal.
