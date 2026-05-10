---
caste: producer
scope: lattice
---

# Lattice Bootstrap

Lattice-bootstrap is a producer agent whose primary substrate effect is provisioning the canonical agent corpus into a lattice's authorial subtree: per fire, it picks the first canonical spec under `lattice-bootstrap/agents/` whose target path isn't yet registered for the active `(node, user)` and emits the agent doc body, the path registration, and the agent / `agent.caste.<v>` / `agent.scope.<v>` classifiers. The runner walks fires-until-quiescence; when every canonical spec is provisioned, the agent skips.

## Triggers

- A lattice doc exists in the substrate, AND
- At least one canonical agent spec under `lattice-bootstrap/agents/` has no corresponding registered doc in the lattice's `(node, user)` subtree.
