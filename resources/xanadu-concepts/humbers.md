# Humbers

Source: Literary Machines, 4/13-4/14 (pages 180-181)

## Semantic Intent

### What It Means

A humber is a variable-length binary number designed to efficiently represent integers of any size. The name stands for "humungous number" - reflecting its ability to handle values from zero to astronomically large quantities. The key insight is that most numbers in practice are small, so humbers are optimized to be compact for common cases while seamlessly expanding to accommodate rare large values.

### User Guarantee

Numbers in the Xanadu addressing system will work correctly regardless of size. Users never need to worry about running out of address space or encountering overflow errors - the system scales from small personal documents to a universal docuverse without artificial limits.

### Principle Served

Humbers solve the "accordion" problem of addressing: how to design an address format that is both compact (for the billions of small incremental addresses) and unbounded (for the potentially immense total address space). Without variable-length numbers, the system would either waste space on small addresses or impose arbitrary limits on large ones.

### How Users Experience It

- Small document addresses are compact and efficient
- The addressing system has no practical upper limit
- No "address exhaustion" problems as the docuverse grows
- All addresses work identically regardless of their magnitude
- Zero is naturally represented (useful for tumbler boundaries)

### Nelson's Words

> "Humber stands for 'humungous number.' Humbers are numbers we have designed for this system, a notation for positive integers."
> — page 4/13

> "They are a data structure of the class usually called Bignums, that is, a way of representing numbers that may range up to very great size; but we have tailored them also to be very small in their representation when they represent small quantities. Thus the humber is an accordion-like notation, very short when a number is small, and as large as it needs to be when the number is big."
> — page 4/13

> "Small incremental humbers are one byte long. But very large humbers adhere to the same format; thus only one set of 'humber arithmetic' routines is necessary."
> — page 4/13

> "The Completeness bit is zero if the actual number is within the byte, 1 if it is not; this choice makes an all-zero byte a true zero (a fact which will be seen to be a useful choice for the tumbler mechanism)."
> — page 4/13

> "[H]umbers... are short most of the time (when needed for small incrementation) and stretch out whenever needed without any change in the generalized manipulation routines."
> — page 4/14

### Attribution

> "Humbers are the work of Roger Gregory, Mark Miller and Stuart Greene, done in the summer of 1979."
> — page 4/13 (footnote)
