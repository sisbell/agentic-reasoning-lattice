# Transclusion

Source: Literary Machines, Chapter 2 (2/32-2/40)

## Semantic Intent

### What It Means

Transclusion is **inclusion by reference, not copy**. When you include content from another document:

- You see the original content (not a copy)
- The original stays where it is, owned by its creator
- Changes to the original appear in your view
- The connection to the source is always visible and traceable

Nelson's term: "windows" or "quote-links"

### User Guarantee

> "Document A can include Document B, even though Document B is owned by someone else."

When you transclude:
- You see the content as if it were in your document
- The original owner retains ownership and control
- Attribution is automatic and permanent
- If the original is updated, you can see the updates

This is NOT copying. The content exists once; you're creating a view of it.

### Principle Served

**Reference, not copy.** The fundamental problem with copying is that copies diverge from originals, lose attribution, and break the connection. Transclusion maintains the connection forever.

This enables:
- **Automatic attribution** - always know the source
- **Royalties** - pay the creator for views
- **Living documents** - updates propagate
- **No orphaned copies** - everything traces back

### How Users Experience It

- Include a passage from someone else's document
- The passage appears in your document as a "window"
- Readers can click through to the original
- Original author gets credit (and potentially payment)
- If you want a frozen copy, you explicitly create one

### Nelson's Words

On what it is:
> "Someone else may create a document which quotes it as much as desired. This mechanism we call the quote-window or quote-link. Through a 'window' in the new document we see a portion of the old."

On compound documents:
> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material."

On ownership:
> "Each compound document is like the other documents: it has an owner and receives royalties."

On the window metaphor:
> "Think of the present document as a sheet of glass. It may have writing printed on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely."

---

## Related Concepts

| Concept | Relationship |
|---------|--------------|
| [i-space-v-space](i-space-v-space.md) | Transclusion creates Vstream mapping to existing Istream content |
| [windowing](windowing.md) | The visual metaphor for transclusion |
| [correspondence](correspondence.md) | Transcluded content corresponds to original |
| [documents](documents.md) | Original owner retains ownership; compound docs have their own owner |
| [spans](spans.md) | Transclusion targets are specified as spans |
| [versions](versions.md) | CREATENEWVERSION is effectively transclusion of entire document |

## FEBE Operations

| Operation | How transclusion applies |
|-----------|-------------------------|
| **COPY** | The transclusion operation - reference, not copy |
| **CREATENEWVERSION** | New version transcludes all content from source |
| **FINDDOCSCONTAINING** | Finds all documents that transclude specified content |

See [Concept-Operation Map](../concept-operation-map.md) for full mapping.
