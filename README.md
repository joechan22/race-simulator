<!--
 * @Author: Joe
 * @Date: 2024-01-19 21:57:47
 * @LastEditors: joe skchan222@gmail.com
 * @LastEditTime: 2024-01-21 12:56:39
 * @FilePath: /race-simulator/README.md
 * @Description: 
 * 
 * Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
-->
# race-simulator

Simple computer simulation for horse racing based on beta distribution.

```python
>>> from simulation import simulator
>>> s = simulator(filename='stats.csv')
>>> result = s.run_simulation(simulation=1000)
>>> s.getWinProb(result)
```

### Basic Usage
1. Update the stats.csv with statistics of win and lose for each horse in the race
2. execute the run_simulation() with the number of simulation, recommend more than 1000


### Limitations
- probability of some horse will be 0 due to no change to win according to the ranking