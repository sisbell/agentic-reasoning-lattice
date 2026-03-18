# Divergences — P4 (ProvenanceBounds)

- **Line 32**: WF is an explicit precondition requiring arrangements exist only for allocated documents. The ASN treats this structurally (M is total with M(d) = ∅ for d ∉ E_doc), but the Dafny partial-map model needs it to link pre-existing arrangement entries back to E_doc membership in the inductive step.
