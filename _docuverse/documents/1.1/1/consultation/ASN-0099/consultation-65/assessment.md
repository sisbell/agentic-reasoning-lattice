# Channel Assignment — ASN-0099 review-65

**Date:** 2026-06-04 13:25

## Issue 1: The two meta-lemmas' relationship is stated twice, wrapped in use-site inventory
Reason: Internal. This is a deduplication of two paragraphs stating the same containment relationship between the two named lemmas; both lemma bodies are already present in the ASN and downstream sites cite whichever they use. No design intent or implementation evidence is needed.

## Issue 2: F2-V ∧ F3-V carries defensive justification and re-explains the conformance-pair structure
Reason: Internal. The F2/F3 conformance pattern and the variant predicates are all already stated in the ASN; the fix removes meta-commentary about citability, fault-pinning, and routing rationale. Nothing turns on Nelson's intent or udanax-green behavior.

## Issue 3: F4(b) and the "Realizability discharge" repeat the same realizability framing
Reason: Internal. The realizability principle and the five witnesses are fully present in the ASN; consolidating three restatements into one is a structural edit requiring no external input.

## Issue 4: Implementation-mechanics rationale lodged in "Local Atomicity"
Reason: Internal. The abstract guarantee (SequentialTransitionAxiom + "next query reflects the commit") is already stated; removing the background-index lag narrative is a deletion of implementation rationale. The LM 2/46 "without appreciable delay" intent is already correctly characterized in the ASN as a non-formalized reader-experience commitment, so no Nelson clarification is needed.
