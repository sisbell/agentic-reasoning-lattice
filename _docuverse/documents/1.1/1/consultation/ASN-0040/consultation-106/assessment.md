# Channel Assignment — ASN-0040 review-106

**Date:** 2026-05-29 04:34

## Issue 1: B8's proof rests on an unjustified — and false — "linear history" premise
Reason: Deciding fix (a) — asserting linearity as a model property — requires external grounding: Gregory tells us whether the implementation actually serializes baptism commits, and Nelson tells us whether a single sequential allocation authority was the design intent. Fix (b) alone (restricting B8 to a common transition path) would be internal, but justifying linearity rather than merely restricting the claim needs both channels.
Nelson question: Was tumbler baptism designed to occur through a single sequential allocation authority (linear history), or did the design contemplate concurrent/branching allocation from genesis?
Gregory question: Does udanax-green commit baptisms through a single serialized path (one persistent-store writer), so that no two baptismal commits can occur on divergent branches from the same state?
