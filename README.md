# Enhanced-Monte-Carlo-Simulation-for-Pricing-and-Hedging-Barrier-Options

## Introduction

This project implements an enhanced Monte Carlo simulation framework for pricing and hedging barrier options with improved accuracy. We address the discretization bias inherent in standard Monte Carlo methods by applying the reflection principle to estimate barrier-crossing probabilities between simulation steps. Additionally, we employ smoothing techniques to calculate option Delta for effective hedging strategies.

Our experiments use vanilla option data based on SPY US Equity from [Bloomberg](https://www.bloomberg.com/professional/products/bloomberg-terminal/) (starting April 16, 2024), with an initial asset price of 503.49 and strike price of 505. We test pricing accuracy across multiple tenors ranging from 3 to 136 days and various barrier levels, verifying that knock-in and knock-out prices sum to the vanilla option price. For Delta hedging experiments, we use actual SPY price movements with strike price of 512, comparing hedging errors between our enhanced method and crude Monte Carlo approximations across different barrier configurations.  

## Technical Details

- **`mf796_Grp08_report.pdf`**: Project report.
- **`Simulation.ipynb`**: Code for experiments.

## Data

### Pricing Experiments
- **`cdatas.csv`** & **`pdatas.csv`**: Call & Put prices of vanilla options with multiple strikes and tenors.
- **`call_data.py`** & **`put_data.py`**: Data extractors of the above 2.
- **`spy_call_put.xlsx`**: Call & Put prices of vanilla options with strike 505.

### Hedging Experiments
- **`cdatas_sen.csv`** & **`pdatas_sen.csv`**: Call & Put prices of vanilla options with various strike price of 512 and multiple tenors.
- **`call_data_sen.py`** & **`put_data_sen.py`**: Data extractors of the above 2.
- **`SPY.xlsx`**: SPY index.
