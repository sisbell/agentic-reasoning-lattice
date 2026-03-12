# Proof Imports

Maps each ASN to the additional proof modules its generated properties need.
TumblerAlgebra and Foundation are always injected automatically. The Dafny
generator reads all listed modules and injects their source into the prompt.

| ASN | Additional proof modules |
|-----|-------------------------|
| ASN-0001 | |
| ASN-0026 | AddressAllocation |
| ASN-0029 | AddressAllocation, TwoSpace, DocumentOntology |
