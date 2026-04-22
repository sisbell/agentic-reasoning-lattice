You are generating focused questions for a theorist working
from Maxwell's dynamical theory of gases (1867).

Maxwell thinks about molecular velocity, vis viva, elastic
collision, equilibrium, pressure, temperature, and the ratio
of total to translational energy (β). He derives what MUST
hold for a system of colliding elastic bodies — independent
of any specific substance.

## Your Task

Given the inquiry below, generate exactly {num_questions}
focused questions for the theorist. Each question must:

1. Target ONE theoretical prediction or ONE derived consequence
2. Use the corpus's vocabulary — vis viva, molecular velocity,
   elastic collision, equilibrium, pressure, temperature, β
3. Cover a distinct aspect — no overlap between questions
4. NOT ask for specific numeric values or measurement results
5. NOT use modern terminology the corpus does not employ
   (degrees of freedom, equipartition, statistical mechanics,
   entropy, Boltzmann constant)

## Inquiry

{inquiry}
{out_of_scope}

## Output Format

Return ONLY the numbered questions, one per line. No preamble, no explanation.

1. What does the theory predict about the average vis viva of a molecule in a system at thermal equilibrium?
2. How does the theory connect the pressure of a gas to the velocities of its constituent molecules?
3. What must hold about the distribution of molecular velocities after sufficiently many elastic collisions?