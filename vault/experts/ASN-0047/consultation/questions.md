# Sub-Questions — State Transitions

**Inquiry:** What are the primitive ways system state can change? Given permanent stores and mutable arrangements, what transitions are possible and what invariants must each preserve?

1. [nelson] You describe the docuverse as containing "nothing except documents and their arbitrary links." If these are the only two things stored, what are the ways the docuverse can change?
2. [nelson] What is the minimal set of distinct ways the system's collection of documents can grow — can documents only be created, or can they also be split or merged?
3. [gregory] What specific system property (transclusion tracking, link semantics, version comparison) depends on origin-based rather than value-based identity?
4. [gregory] The three storage tiers have different mutability contracts: granfilade (append-only), spanfilade (write-only), and document arrangements (fully mutable) — was this three-tier mutability hierarchy an explicit design
5. [gregory] When you look across all eight FEBE state-modifying commands, how many distinct kinds of state modification do they actually perform — not how many commands exist, but how many underlying state changes?
