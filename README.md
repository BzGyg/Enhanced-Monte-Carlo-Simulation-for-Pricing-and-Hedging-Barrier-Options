# Enhanced-Monte-Carlo-Simulation-for-Pricing-and-Hedging-Barrier-Options

## Introduction

This project implements an enhanced Monte Carlo simulation framework for pricing and hedging barrier options with improved accuracy. We address the discretization bias inherent in standard Monte Carlo methods by applying the reflection principle to estimate barrier-crossing probabilities between simulation steps. Additionally, we employ smoothing techniques to calculate option Delta for effective hedging strategies.

Our experiments use vanilla option data based on SPY US Equity from [Bloomberg](https://www.bloomberg.com/professional/products/bloomberg-terminal/) (starting April 16, 2024), with an initial asset price of 503.49 and strike price of 505. We test pricing accuracy across multiple tenors ranging from 3 to 136 days and various barrier levels, verifying that knock-in and knock-out prices sum to the vanilla option price. For Delta hedging experiments, we use actual SPY price movements with strike price of 512, comparing hedging errors between our enhanced method and crude Monte Carlo approximations across different barrier configurations.  

## Technical Details

**`mf796_Grp08_report.pdf`**: Project report.

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

- **`Simulation.ipynb`**: Code for experiments.

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
