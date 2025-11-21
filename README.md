# Enhanced-Monte-Carlo-Simulation-for-Pricing-and-Hedging-Barrier-Options
## Introduction
Monte Carlo simulation is common for pricing options and assessing their price sensitivities. However, it is susceptible to two drawbacks: slow convergence rates and the time discretization. The latter problem usually leads to extra bias when simulating path-dependent processes such as Barrier options pricing. 

Barrier options are a type of financial derivatives whose payoffs hinge on whether the underlying asset's price reaches a predetermined barrier level during the option's duration. They are typically classified as either knock-in or knock-out options. A knock out option comes into effect only when the underlying asset's price hits the barrier, while a knock-in option is activated in the inverse situation. These options are appealing for their lower costs and accurate price estimation is hence of practical importance. 

In our project, we addressed the bias resulting from time discretization in Barrier options pricing by leveraging the reflection principle. We then applied the insights gained from the previous section, combined with smoothing techniques, to analyze the Delta hedge of Barrier options.  
