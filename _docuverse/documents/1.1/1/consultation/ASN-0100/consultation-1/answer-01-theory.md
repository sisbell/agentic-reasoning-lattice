## Question 1 [theory]

> Was INSERT intended as a substrate-level elementary transition, or as a user-facing composite built from K.α, K.μ⁺, K.μ⁻, and K.ρ?

INSERT was intended as a **user-facing FEBE command**, not as substrate-level elementary transitions. It is one of the 17 protocol operations in XU.87.1, presented at the protocol surface where users invoke it.

I characterized this whole class plainly:

> "FEBE includes instructions for insertion in a document, deletion from a document, and rearrangements of unlimited size. These are conceptually simple." [LM 4/61]

The FEBE specification covers both content addition and arrangement update in a single user-invoked operation:

> "This inserts <text set> in document <doc id> at <doc vsa>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

The notation K.α, K.μ⁺, K.μ⁻, K.ρ is not my vocabulary — that is substrate decomposition I never specified in Literary Machines. What I did insist on was that protocol complexity belongs hidden beneath the user:

> "None of these commands are to be seen by the user. The user's concerns are to be seen on the screen; the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things." [LM 4/61]

So the design intent locates INSERT at the protocol surface. The user's contract is FEBE-level: invoke INSERT, receive the semantic effect — content added at a position, downstream v-addresses shifted. Whether an implementation realizes it as a single elementary transition, or composes it from finer kernel operations (allocation, mapping addition/removal, relational update), is an architectural choice I left to implementors.

NEED_RAW: Literary Machines does not specify a substrate kernel beneath FEBE. Any claim about INSERT-as-composite over K.α/K.μ⁺/K.μ⁻/K.ρ is a downstream analytical decomposition — consistent with my design intent (which permits invisible internal mechanics), but not authored by me.
