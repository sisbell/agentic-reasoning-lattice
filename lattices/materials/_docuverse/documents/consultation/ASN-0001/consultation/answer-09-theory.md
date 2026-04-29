## Question 9 [theory]

> What does the theory say about the transfer of thermal energy through collisions between constituents?

# Transfer of Thermal Energy Through Collisions Between Constituents

The corpus treats thermal-energy transfer between different molecular constituents as a direct consequence of their **encounters** (collisions), and distinguishes it from the bulk motion of the gas.

## Mechanism and endpoint

Maxwell states the basic mechanism directly:

> "The effect of the mutual action of the molecules is not only to equalize the pressure in all directions, but, when molecules of different kinds are present, to communicate motion from the one kind to the other. I formerly showed that the final result in the case of hard elastic bodies is to cause the average *vis viva* of a molecule to be the same for all the different kinds of molecules." [1867-maxwell-dynamical-theory-of-gases]

The endpoint is formalized as the equipartition result (eq. 34):

$$M_1\overline{v_1^2} = M_2\overline{v_2^2}$$

which Maxwell emphasizes "is independent of the nature of the action between the molecules, as are all the other results relating to the final distribution of velocities." [1867-maxwell-dynamical-theory-of-gases]

## Definition of equal temperature

Thermal equilibrium between constituents is *defined* by zero net exchange of vis viva through collisions:

> "When the flow of *vis viva* from the one kind of molecules to the other is zero, the temperature is said to be the same." [1867-maxwell-dynamical-theory-of-gases]

## Rate of approach

In the "Equilibrium of Temperature between two Gases" section, Maxwell writes the equation governing the mutual transfer (eq. 94):

$$\tfrac{1}{2}\rho_1\frac{\partial}{\partial t}\beta_1(\overline{\xi_1^2}+\overline{\eta_1^2}+\overline{\zeta_1^2}) = \frac{k\rho_1\rho_2 A_1}{M_1+M_2}\left\{M_2(\overline{\xi_2^2}+\overline{\eta_2^2}+\overline{\zeta_2^2}) - M_1(\overline{\xi_1^2}+\overline{\eta_1^2}+\overline{\zeta_1^2})\right\}$$

Defining $Q_i = \tfrac{M_i}{M_1+M_2}(\overline{\xi_i^2}+\overline{\eta_i^2}+\overline{\zeta_i^2})$, the difference decays exponentially (eqs. 96–97):

$$Q_2-Q_1 = Ce^{-nt}, \quad n = \frac{2kA_1}{M_1+M_2}(M_2\rho_2\beta_2+M_1\rho_1\beta_1)\frac{1}{\beta_1\beta_2}$$

> "If, therefore, the gases are in contact and undisturbed, $Q_1$ and $Q_2$ will rapidly become equal. Now the state into which two bodies come by exchange of invisible agitation is called equilibrium of heat or equality of temperature." [1867-maxwell-dynamical-theory-of-gases]

The rate constant depends on $k$ (the coefficient of mutual interference between the two kinds), on $A_1$ (the collision-integral constant), and on the densities and masses. Under the $n=5$ force law used throughout, $V$ drops out, so the rate is independent of the relative velocity of the molecules.

## Internal vs. translational energy

Collisions also couple translation to internal motion. Following Clausius:

> "the energy of translation and the internal energy of the molecules arrive, by repeated small exchanges, at a final ratio, which we shall suppose to be that of 1 to $\beta - 1$." [1867-maxwell-dynamical-theory-of-gases]

Thus $\bar{E} = (\beta-1)(\overline{\xi^2}+\overline{\eta^2}+\overline{\zeta^2})$ (eq. 67), and the total invisible agitation per unit volume is $\tfrac{3}{2}\beta p$ (eq. 69).

## Collision-heating in diffusion

When the two constituents move relative to one another, the encounters contribute a positive heating term. From equation (117):

$$\ldots = k\rho_1\rho_2 A_1\left\{(u_1-u_2)^2+(v_1-v_2)^2+(w_1-w_2)^2\right\}$$

Maxwell identifies "the thermal effects of diffusion, and the communication of heat from one gas to the other" as what these right-hand terms represent [1867-maxwell-dynamical-theory-of-gases]. He further notes that under constant-volume interdiffusion "the heat due to the mutual action of the gases in diffusion will be exactly neutralized by the cooling of each gas as it expands."

## Consequence: Law of Equivalent Volumes

Because pressure per molecule is proportional to its vis viva, and collisions equalize mean vis viva across kinds at the same temperature:

> "equal volumes of different gases at equal pressures and temperatures contain equal numbers of molecules." [1867-maxwell-dynamical-theory-of-gases]

Maxwell flags this as a "necessary result of the Dynamical Theory of Gases; and it is so, whatever theory we adopt as to the nature of the action between the individual molecules" [1867-maxwell-dynamical-theory-of-gases].

## Scope note

The corpus treats inter-constituent transfer via binary encounters under the assumption that "we may neglect those cases in which three or more molecules are within each other's spheres of action at the same instant" [1867-maxwell-dynamical-theory-of-gases]. The detailed transfer rates (eqs. 36–39) are computed specifically for the inverse-fifth-power repulsion, which is "the only case which is consistent with the laws of viscosity of gases" [1867-maxwell-dynamical-theory-of-gases]; the equipartition endpoint itself, however, the corpus states does not depend on that choice.
