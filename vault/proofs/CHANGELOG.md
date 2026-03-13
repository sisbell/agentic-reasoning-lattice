# Proof Modules — Changelog

## 2026-03-13: ASN-0034 restart — clean slate

ASN-0034 (Tumbler Algebra) converged, replacing ASN-0001 as the foundation. Removed all deprecated modules: AddressAllocation (ASN-0001 property proofs), Foundation (Two-Space state model), DocumentOntology (ASN-0029 types), TwoSpace (ASN-0026 properties). These will be regenerated fresh against ASN-0034 as each downstream ASN is redrafted.

Retained: TumblerAlgebra/TumblerAlgebra.dfy (shared definitions). ASN-0034 property proofs will be generated into TumblerAlgebra/ alongside the definitions module.
