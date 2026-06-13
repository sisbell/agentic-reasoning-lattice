# Channel Assignment — ASN-0108 review-45

**Date:** 2026-06-13 07:33

## Issue 1: W5's claim statement buries the claim and forward-references downstream material
Reason: Purely editorial restructuring — disassembling a run-on sentence into a crisp claim plus separate scoping sentences, dropping a redundant aside, and replacing forward references with local statements. Every piece (the two scoped guarantees, clause 1's definition, the sufficiency-not-necessity point, the whole-pass scope) is already present in the note; nothing about design intent or implementation behavior is in question.

## Issue 2: The absolute-invariance / uniform-shift elaboration serves no claim
Reason: A pure deletion of a self-contained digression that no downstream claim consumes; the load-bearing point ("Both identity keys are therefore state-stable") already stands. No design intent or implementation evidence is needed to remove unused elaboration.
