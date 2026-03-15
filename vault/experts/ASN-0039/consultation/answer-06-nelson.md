## Question 6 [nelson]

> Is there a design limit on how many positions can be baptized beneath a single parent position, or must the addressing scheme support unbounded growth at every level?

### Nelson's Answer

No limit. The addressing scheme is explicitly designed for unbounded growth at every level:

> "A tumbler consists of a series of integers. Each integer has no upper limit; since its number base is irrelevant, we call it a 'digit.'" (4/19)

Each digit position can grow without bound. There is no maximum node count, no maximum account count, no maximum document count.

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." (4/19)

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." (4/19)

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." (4/19)

Nelson designed the system for indefinite proliferation:

- Allow the network to grow unpredictably
- Allow documents and versions to proliferate indefinitely
- Keep all addresses permanently valid

The unbounded digit guarantees this. Item 2 can have children 2.1, 2.2, 2.3, ... 2.1000000, ... with no architectural limit. The only constraint is physical resources, not address space design.
