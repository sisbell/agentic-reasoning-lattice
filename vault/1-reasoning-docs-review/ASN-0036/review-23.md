# Rebase Review of ASN-0036

## REVISE

### Issue 1: D-SEQ registry and heading omit D-CTG-depth dependency
**ASN-0036, D-SEQ heading and Properties Introduced table**: "COROLLARY; from D-CTG, D-MIN, S8-fin, S8-depth"
**Problem**: The body derivation explicitly invokes D-CTG-depth: "By D-CTG-depth (when m ≥ 3) or trivially (when m = 2...)". D-CTG-depth is a genuine dependency for the m ≥ 3 case, and it carries transitive foundation dependencies (T0(a), T1 from ASN-0034) that are absent from D-SEQ's dependency list. Both the bold heading and the registry entry omit D-CTG-depth.
**Required**: Add D-CTG-depth to D-SEQ's dependency list in both the heading and the registry. This makes the transitive ASN-0034 dependencies (T0(a), T1) traceable.

### Issue 2: S8 registry omits T1 (ASN-0034)
**ASN-0036, Properties Introduced table**: "theorem from S8-fin, S8a, S2, S8-depth, T5, T10, TA5(c), TA7a (ASN-0034)"
**Problem**: The S8 uniqueness proof explicitly invokes T1 by name in two places — "giving t > v + 1 by T1" and "s.3 < s.3.1 < s.4 by T1 prefix extension." The convention within this ASN is to list T1 when explicitly invoked (D-CTG-depth does so). S8's registry entry does not list T1.
**Required**: Add T1 to S8's foundation dependency list in the registry entry.

### Issue 3: S4 cites T2 for equality decidability; T3 is the direct property
**ASN-0036, Content identity section**: "The structural test for shared identity is address equality, decidable from the addresses alone (T2, ASN-0034) without value comparison."
**Problem**: T2 (IntrinsicComparison) states that the *order relation* is computable from tumblers alone. The claim here is about *equality* decidability. T3 (CanonicalRepresentation) directly provides the equality criterion: `a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b`. A reader verifying the citation finds an order property where an equality property is claimed.
**Required**: Cite T3 (or T3 alongside T2) for equality decidability.

VERDICT: REVISE
