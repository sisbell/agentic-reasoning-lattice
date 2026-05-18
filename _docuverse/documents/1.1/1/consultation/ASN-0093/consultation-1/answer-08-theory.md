## Question 8 [theory]

> Are content and link sub-allocators under each document part of a single global allocator tree rooted at the universal allocator, or do they stand as independent allocator chains per document?

# Single Global Allocator Tree

Content and link sub-allocators under each document are **part of a single global tumbler tree** rooted at the universal allocator — they are not independent allocator chains.

## The Unification Principle

Nelson is unambiguous that all addressing forms one continuous forking structure:

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. **Thus all numeration in the docuverse is compressed into a single mechanism.**" — 4/19

> "So the docuverse is all really one big forking document." — 4/18

## How the Forking Cascades

The same baptism mechanism operates at every level. Each owner controls allocation below their address:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." — 4/17

> "The owner of a given item controls the allocation of the numbers under it." — 4/20

## The Document-Internal Layer

Sub-allocators within a document (bytes and links) sit on the same tumbler line, distinguished by subspace separators within the element field:

- Bytes: `N.0.U.0.D.V.0.1.position`
- Links: `N.0.U.0.D.V.0.2.serial`

These are simply additional forks under the document/version node. The link allocator's permanent creation-order addresses (4/31: "the links designated by a tumbler address are in their permanent order of arrival") and the byte allocator's V-stream positions are both extensions of the same universal forking tree, delegated to the document owner.

## What This Means Structurally

| Level | Allocated by | Position in tree |
|-------|--------------|------------------|
| Universal | (root, digit 1) | "the entire docuverse" — 4/38 |
| Node | Project Xanadu / network | forks under 1 |
| Account | Node owner | forks under node |
| Document | Account owner | forks under account |
| Version | Document owner | forks under document |
| Bytes (0.1.*) | Document/version owner | forks under version |
| Links (0.2.*) | Document/version owner | forks under version |

Ownership is delegated, but the **address space itself remains unified**. There is no separate allocator namespace per document — only delegated authority over a subtree of the one universal forking structure.
