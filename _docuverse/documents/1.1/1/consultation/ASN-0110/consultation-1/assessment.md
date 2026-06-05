# Channel Assignment — ASN-0110 review-1

**Date:** 2026-06-04 22:48

## Issue 1: No concrete worked example
Reason: Fully derivable from the ASN. Every needed ingredient — coverage, the half-open overlap predicate, RE-witness, RE-result, RE-full, RE-role — is defined in the note, so a concrete instance with chosen tumblers can be computed internally without design intent or implementation evidence.

## Issue 2: Role-index range of the returned family is underspecified
Reason: The note cannot derive its own arity convention; this is a return-shape decision that should match what the operation actually returns and what the role structure was meant to be. Gregory gives the concrete return shape; Nelson confirms whether a fixed triple or open-ended family was intended.
Nelson question: Was RETRIEVEENDSETS designed to return a fixed-arity result (the from/to/type triple) or an open-ended role-indexed family extending to whatever link arities are present?
Gregory question: For a store mixing links of different arities, what does the udanax-green RETRIEVEENDSETS return as its result shape, and does it include positions for roles whose endset set is empty?

## Issue 3: No weakest-precondition analysis
Reason: Fully derivable from the ASN. K.λ is referenced (ASN-0093) and RE-result/RE-mono supply the postcondition machinery, so wp(K.λ, "e ∈ E₁(I, Σ')") can be computed from the note's own definitions.
