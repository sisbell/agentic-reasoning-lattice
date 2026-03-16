# Divergences — O1b (PrefixInjective)

- **Line 18**: With Principal modeled as a datatype whose sole field is the prefix tumbler, injectivity holds by construction (structural equality). The ASN treats Principal as an abstract identity with pfx as a separate mapping; the Dafny model collapses these, making O1b a tautology. This is sound: any model satisfying the abstract version also satisfies this one, and vice versa.
