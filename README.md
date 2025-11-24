# Enhanced-Monte-Carlo-Simulation-for-Pricing-and-Hedging-Barrier-Options

## Introduction

This project implements an enhanced Monte Carlo simulation framework for pricing and hedging barrier options with improved accuracy. We address the discretization bias inherent in standard Monte Carlo methods by applying the reflection principle to estimate barrier-crossing probabilities between simulation steps. Additionally, we employ smoothing techniques to calculate option Delta for effective hedging strategies.

Our experiments use vanilla option data based on SPY US Equity from [Bloomberg](https://www.bloomberg.com/professional/products/bloomberg-terminal/) (starting April 16, 2024), with an initial asset price of 503.49 and strike price of 505. We test pricing accuracy across multiple tenors ranging from 3 to 136 days and various barrier levels, verifying that knock-in and knock-out prices sum to the vanilla option price. For Delta hedging experiments, we use actual SPY price movements with strike price of 512, comparing hedging errors between our enhanced method and crude Monte Carlo approximations across different barrier configurations.  

**`mf796_Grp08_report.pdf`**: Project report.

## Key Formulas

### Notation

| Symbol | Description |
|--------|-------------|
| $S(t)$ | Asset price at time $t$ |
| $B$ | Barrier level |
| $K$ | Strike price |
| $\sigma$ | Implied volatility |
| $r$ | Risk-free interest rate |
| $q$ | Dividend yield |
| $T$ | Time to expiration |
| $\Delta t$ | Time step size |
| $\tau_B$ | First hitting time of barrier $B$ |
| $N$ | Total number of simulation steps |

### Log-Space Transformation

For computational convenience, we work in log-space:
$$Z(t) = \ln(S(t)), \quad b = \ln(B)$$

The log-price follows:
$$dZ(t) = \left(\mu - q - \frac{\sigma^2}{2}\right)dt + \sigma dW(t)$$

---

### Barrier Hitting Probability (Reflection Principle)

The probability of hitting barrier $B$ between two adjacent time steps, given endpoints:

$$p(t_i \leq \tau_B \leq t_{i+1}|S(t_i), S(t_{i+1})) = \exp\left(-\frac{2(\ln(S(t_{i+1})) - \ln(B))(\ln(S(t_i)) - \ln(B))}{\sigma^2\Delta t}\right)$$

> **Note:** This formula is derived from the reflection principle of Brownian motion. Values exceeding 1 should be capped at 1.

---

### Corrected Barrier Option Pricing

The probability that the barrier is **not** hit during the entire simulation:

$$P(\{\tau_B > T|S(t_0), S(t_1)...S(t_N)\}) = \prod_{i=0}^{N-1}\left(1 - p(t_i \leq \tau_B \leq t_{i+1}|S(t_i), S(t_{i+1}))\right)^+$$

where $(x)^+ = \max(x, 0)$.

**Knock-Out Option:**
$$V_{knock-out}(t) = e^{-(T-t)r}\mathbb{E}\left[V_{vanilla} \cdot P\{\tau_B > T|S(t_0), S(t_1)...S(t_N)\}\right]$$

**Knock-In Option:**
$$V_{knock-in}(t) = e^{-(T-t)r}\mathbb{E}\left[V_{vanilla} \cdot P\{\tau_B \leq T|S(t_0), S(t_1)...S(t_N)\}\right]$$

where:
$$P\{\tau_B \leq T|S(t_0), S(t_1)...S(t_N)\} = 1 - P\{\tau_B > T|S(t_0), S(t_1)...S(t_N)\}$$

---

### Delta Calculation with Smoothing

#### The Problem
The payoff of a down-and-out call option involves indicator functions:
$$V(0) = e^{-rT}\mathbb{E}\left[H(S_{min} - B) \cdot R(S(T) - K)\right]$$

where $S_{min}$ is the path minimum, $H(x)$ is the Heaviside function, and $R(x) = \max(x, 0)$ is the ramp function.

Since $H(x)$ is non-differentiable at $x=0$, we cannot directly compute $\Delta = \frac{\partial V}{\partial S(0)}$.

#### Smoothing Functions

**Smoothed Heaviside:**
$$H_\epsilon(x) = \frac{\tanh\left(\frac{x}{\epsilon}\right) + 1}{2}$$

**Smoothed Ramp:**
$$R_\epsilon(x) = \int_{-\infty}^{x} H_\epsilon(u) \, du$$

As $\epsilon \to 0$, these converge to the true indicator and ramp functions.

#### Sampling the Path Minimum

Using the reflection principle, we can sample $S_{min}$ directly without simulating the full path:

$$S_{min} = \exp\left(\frac{1}{2}\left(\ln S(0) + \ln S(T) - \sqrt{(\ln S(0) - \ln S(T))^2 - 2\sigma^2 T \ln(U_1)}\right)\right)$$

where $U_1 \sim \text{Uniform}(0, 1)$.

The terminal price is sampled as:
$$S(T) = S(0) \exp\left(\left(\mu - q - \frac{\sigma^2}{2}\right)T + \sigma\sqrt{T}\Phi^{-1}(U_2)\right)$$

where $U_2 \sim \text{Uniform}(0, 1)$ and $\Phi^{-1}$ is the inverse standard normal CDF.

#### Smoothed Delta

$$\Delta_\epsilon = e^{-rT} \int_0^1 \int_0^1 \frac{d\left(H_\epsilon(S_{min} - B) \cdot R_\epsilon(S(T) - K)\right)}{dS(0)} \, dU_1 \, dU_2$$

> **Constraint:** Ensure $(\ln S(0) - \ln S(T))^2 - 2\sigma^2 T \ln(U_1) > 0$ during sampling.

---

### Verification Identity

For any barrier $B$:
$$V_{vanilla} = V_{knock-in}(B) + V_{knock-out}(B)$$

This identity provides an internal consistency check. Since $V_{vanilla}$ is obtained from market prices (not simulated), the error measures the absolute accuracy of our Monte Carlo method.

## Data

### Pricing Experiments
- **`cdatas.csv`** & **`pdatas.csv`**: Call & Put prices of vanilla options with multiple strikes and tenors.
- **`call_data.py`** & **`put_data.py`**: Data extractors of the above 2.
- **`spy_call_put.xlsx`**: Call & Put prices of vanilla options with strike 505.

### Hedging Experiments
- **`cdatas_sen.csv`** & **`pdatas_sen.csv`**: Call & Put prices of vanilla options with various strike price of 512 and multiple tenors.
- **`call_data_sen.py`** & **`put_data_sen.py`**: Data extractors of the above 2.
- **`SPY.xlsx`**: SPY index.

## Results

**`Simulation.ipynb`**: Code for experiments.

### Pricing Accuracy
**Strike: 505 | Initial Asset Price: 503.49**

Errors measured across 5 barrier levels (Up: 510, 530, 550, 600, 650 | Down: 490, 470, 450, 400, 350):

| Tenor (days) | Up Call |         | Up Put  |         | Down Call |         | Down Put |         |
|--------------|---------|---------|---------|---------|-----------|---------|----------|---------|
|              | Crude   | Corrected | Crude | Corrected | Crude   | Corrected | Crude  | Corrected |
| 3            | 1.438   | 0.693   | 65.788  | 0.429   | 1.697     | 0.681   | 9.515    | 0.511   |
| 14           | 4.487   | 0.457   | 146.377 | 0.193   | 5.991     | 0.371   | 65.207   | 0.406   |
| 31           | 6.751   | 0.451   | 179.165 | 0.698   | 8.889     | 0.556   | 102.173  | 0.371   |
| 45           | 8.252   | 0.563   | 202.463 | 0.579   | 11.186    | 0.766   | 130.235  | 0.484   |
| 66           | 9.420   | 0.691   | 222.847 | 0.202   | 13.296    | 0.731   | 154.540  | 0.511   |
| 73           | 9.490   | 0.386   | 223.416 | 0.895   | 15.214    | 0.946   | 155.357  | 0.338   |
| 94           | 9.831   | 0.983   | 238.750 | 0.943   | 15.270    | 1.288   | 171.931  | 0.646   |
| 106          | 9.428   | 0.696   | 244.064 | 0.952   | 17.998    | 0.606   | 175.667  | 0.427   |
| 122          | 11.232  | 0.835   | 253.462 | 0.918   | 19.459    | 0.967   | 187.500  | 0.863   |
| 136          | 12.303  | 0.877   | 258.839 | 0.763   | 19.691    | 1.388   | 189.586  | 1.379   |
| **Mean**     | **8.586** | **0.978** | **214.668** | **0.682** | **14.072** | **1.072** | **146.796** | **0.659** |

The corrected method significantly reduces pricing errors, particularly for put options.

### Delta Hedging Performance
**Initial Price: 514.865 | End Price: 503.485 | Strike: 512**

Absolute hedging errors comparing crude and corrected Delta methods:

| Barrier | Type | Crude Call | Corrected Call | Crude Put | Corrected Put | Hit Barrier? |
|---------|------|------------|----------------|-----------|---------------|--------------|
| 517     | In   | 3.067      | 0.644          | 7.417     | 5.346         | Yes          |
|         | Out  | 2.934      | 0.047          | 11.681    | 10.374        | Yes          |
| 550     | In   | 0.000      | 0.000          | 1.020     | 1.020         | No           |
|         | Out  | 9.160      | 0.525          | 3.863     | 3.858         | No           |
| 507     | In   | 9.160      | 1.225          | 3.923     | 3.858         | Yes          |
|         | Out  | 0.000      | 0.000          | 1.020     | 1.020         | Yes          |
| 460     | In   | 9.160      | 0.000          | 8.588     | 3.858         | No           |
|         | Out  | 0.000      | 0.000          | 1.020     | 1.020         | No           |

The enhanced Delta hedge demonstrates superior performance, especially for call options and knock-out scenarios.

## References
- Papatheodorou, B. (2005). Enhanced Monte Carlo Methods for Pricing and Hedging Exotic Options. University of Oxford.
- Shreve, S. (2000). Stochastic Calculus for Finance II. Springer.
