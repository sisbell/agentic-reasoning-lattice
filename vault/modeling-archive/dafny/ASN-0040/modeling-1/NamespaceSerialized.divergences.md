# Divergences — B4 (NamespaceSerialized)

- **Line 22**: The ASN uses temporal precedence (≺) over concurrent events. The sequential functional model has no concurrency primitive. Temporal precedence is captured as registry set inclusion: commit(β₁) ≺ read(β₂) iff β₁.commitRegistry ⊆ β₂.readRegistry — the observable consequence of one operation completing before another begins.
