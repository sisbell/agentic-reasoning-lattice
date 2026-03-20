# Enfilades

Source: Literary Machines, 1/33-1/38

## Semantic Intent

### What It Means

An **enfilade** is Xanadu's data structure for managing huge agglomerates of text and their arrangement. The name comes from the architectural term for a suite of rooms arranged in a row with doors aligned—suggesting how data flows through the structure.

From the user's perspective, enfilades are invisible machinery. What users experience is a system that handles text revision "very quickly and very cleanly," where linkages "keep up with all changes" automatically, and where the system "could conceivably scale up infinitely."

The key insight (Bill Barus's "eye in the pyramid") was making enfilades "efficiently ever-linkable"—a structure where links don't break when content changes, and where all changes leave the file "remaining in canonical order."

### User Guarantee

- **Fast revision** - Editing huge documents remains quick regardless of size
- **Links survive changes** - Linkages keep up with all changes automatically
- **Infinite scalability** - The system can grow indefinitely without degradation
- **Canonical order preserved** - Changes don't corrupt the internal structure

### Principle Served

**Literature can grow without bound.** The docuverse must accommodate unlimited text, unlimited links, and unlimited changes while remaining responsive. Enfilades make this possible by providing a "whole universe of poly-enfilade structures" that scale.

### How Users Experience It

Users don't see enfilades directly. They experience:
- Documents that edit smoothly regardless of size
- Links that never break due to editing
- A system that stays fast as it grows
- Version history that remains accessible

### Nelson's Words

> "the system we now call the first enfilade-- the Model T: a data structure that manages huge agglomerates of text and their arrangement in and out of core. With its attendant routines, the Model T enfilade handles the revision of serial data very quickly and very cleanly." (1/33)

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." (1/34, on Barus's contribution)

> "Barus's work, which we refer to jocundly as 'the eye in the pyramid,' made possible an efficiently ever-linkable enfilade, a whole universe of poly-enfilade structures." (1/34)

> "By various enfilade structures we were able to come up with a design that could conceivably scale up infinitely" (1/36)

> "we redesigned Barus's linking enfilade system, designed the historical trace enfilade, and formulated the general theory of enfilades" (1/36)

### Enfilade Types

Nelson mentions multiple enfilade types (1/36). The implementation defines three core types:

| Type | Nelson's term | Purpose | Address space |
|------|---------------|---------|---------------|
| **GRAN** (Granfilade) | "Model T" enfilade | Stores actual content | Istream (native bytes) |
| **POOM** (Positional) | "eye in the pyramid" | Maps V→I addresses | Vstream → Istream mapping |
| **SPAN** | - | Stores span ranges | Used by both |

Additionally mentioned by Nelson:
- **Linking enfilade** - Barus's design for links that track with changes
- **Historical trace enfilade** - for version history

### Relationship to Istream/Vstream

Enfilades implement the Istream/Vstream separation:

```
User requests Vstream position 5
        │
        ▼
   POOM enfilade
   (V→I mapping)
        │
        ▼
   "Position 5 = Istream address X"
        │
        ▼
   GRAN enfilade
   (content storage)
        │
        ▼
   Returns actual bytes from X
```

The "eye in the pyramid" insight (Barus) was making the POOM enfilade efficiently update when content is edited - so Vstream addresses don't break when the underlying Istream is reorganized.
