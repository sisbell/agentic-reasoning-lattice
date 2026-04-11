## Open Questions

What constraints must the content store's value domain `Val` satisfy — must all entries be uniform in type, or must `Val` support heterogeneous content (text, links, media) as first-class distinctions?

Must the span decomposition of an arrangement have a unique maximal form (fewest possible runs), or can multiple valid decompositions of different cardinality coexist for the same arrangement?

What must the system guarantee about the computability of the sharing inverse — given an I-address, what is the cost bound for determining which documents currently reference it?

Under what conditions, if any, may the referential integrity invariant S3 be temporarily violated — must it hold at every observable state, or only at quiescent states between operations?

What abstract property distinguishes content that exists but is unreachable from all current arrangements from content that exists and is reachable — and must the system maintain this distinction as queryable state?

Under what conditions do operations guarantee non-trivial correspondence runs (length > 1) — must sequential content creation produce a single run, or is the singleton decomposition the only structure guaranteed without operation-level constraints?

Does each well-formed editing operation (DELETE, INSERT, COPY, REARRANGE) preserve D-CTG and D-MIN?

What invariants must the displacement mechanism satisfy so that insertion at a ValidInsertionPosition preserves D-CTG, D-MIN, and S2?

Under what conditions does the choice of initial depth m for an empty subspace affect the expressiveness of subsequent arrangements?

What must an operation guarantee about existing V-to-I mappings when it inserts at a position that coincides with an occupied V-position?

Under what conditions on w does the subtraction homomorphism ord(v ⊖ w) = ord(v) ⊖ w_ord hold, given TA7a's conditional S-membership results for subtraction?

What are the precise conditions for the round-trip property (ord(v) ⊕ w_ord) ⊖ w_ord = ord(v)?
