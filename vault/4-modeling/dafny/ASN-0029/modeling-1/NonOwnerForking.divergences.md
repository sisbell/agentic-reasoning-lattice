# Divergences — D16 (NonOwnerForking)

- **Line 18**: predicate(State, DocId) cannot express the transition response (fork creation involves pre/post states and an actor). We model D16 as a transition predicate with additional parameters for actor and publication maps. The account function is bodyless (axiom) per D3: account is computable from the address alone.
