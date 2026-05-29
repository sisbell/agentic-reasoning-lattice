# Channel Assignment — ASN-0045 review-16

**Date:** 2026-05-28 19:58

## Issue 1: Summary status contradicts the per-predicate Depends clauses
Reason: Internal consistency fix. The body's Depends clauses already establish the correct provenance (definitions coined by ASN-0045; T4c supplies only level names); the Summary must be brought into line with text already present. No design-intent or implementation evidence is in question.

## Issue 2: Account rename equivalence invokes T4c without discharging T4c's preconditions
Reason: The required fix is a proof-structure step internal to the foundation already cited (T4-valid → T4b via T3, licensing T4c). The dependency chain and the precondition relationships all live in ASN-0034 content the ASN already references; no external design intent or code evidence is needed.
