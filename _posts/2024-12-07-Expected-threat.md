---
title: "Using xT on three continents"
excerpt_separator: "<!--more-->"
categories:
  - Player analysis
  - Team analysis
  - Modelling football
tags:
  - International
---
------------
### Using xT - pass and carry
------------
<style>
  /* Generell stil for bilder og tekst ved siden av hverandre */
  .figure-text {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    margin-top: 20px;
  }

  /* Gjør bildene responsive */
  .figure-text img {
    width: 40%; /* Bildene tar 40% av bredden */
    max-width: 300px; /* Begrens maksimal bredde på PC */
  }

  /* Teksten ved siden av bildene */
  .figure-text p {
    flex: 1; /* Teksten tar resten av plassen */
    margin: 0;
  }

  /* Responsiv tilpasning for smale skjermer */
  @media screen and (max-width: 768px) {
    .figure-text {
      flex-direction: column; /* Stable bildet og teksten vertikalt */
      align-items: center; /* Midtstill innholdet */
    }

    .figure-text img {
      width: 100%; /* Bildene tar hele bredden på smale skjermer */
      max-width: none; /* Fjern maksimal breddebegrensning */
    }

    .figure-text p {
      text-align: center; /* Juster teksten til midten */
    }
  }
</style>
Football is a low-scoring sport where goals are rare, but <em>passes </em> and <em> carries </em>  dominate the action. During EURO last summer, an incredible 45,630 passes and 44,139 carries were completed. This article explores which of these actions add the most value—and identifies the players excelling at them. Using <em> position-based expected threat </em> (xT), I will answer key questions, such as:
- Is there a correlation between xT and winning?
- Which teams and players created the most xT per game during EURO 2024?
- Who excelled at xT from carries?
There are different types of expected threat. On-ball-value, possession-value, position- and action-based expected threat are a few. They all have in common ending up giving a value to either the position on the pitch or action on the ball. I will briefly go through position-based expected threat before using the metric to evaluate players. 
### Position-based expected threat
Position-based expected threat assigns a <em> value </em> to each point on the pitch. That value is the expected threat, or xT. This value is the probability of scoring either directly from that position, or after moving the ball elsewhere before ball is lost or out of play. David Sumpter from Twelve have written a great article about this. You can read more [here](([https://soccermatics.readthedocs.io/en/latest/lesson4/xTPos.html])).  
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/203f262a-a956-484a-b12f-3b65a1e2f393" alt="L4" style="max-width:80%;"/>
</div> Figure 1. Grid fromt The Athletic. Worville, Tom. (2021)

The grid above is an example with xT values for all locations on the pitch, divided into bins. Attacking from left to right, values obviously increase close to opposition goal. xT-values is set from 0.0 - 1.0. Outside the box location(A) have a value of 0,034. This means scoring directly from here or scoring after moving the ball to another location is given a 3,4 % chance. If ball is moved from (A) to (B) we can calculate xT. The xT-value is the difference between those two values. <br>
$$
xT = xT(B) - xT(A) \\[5pt]
xT = 0.134 - 0.0134 = 0.1
$$
The player moving the ball is credited with 0,1 xT, increasing the chance for his team scoring by 10 %. 

### The grid
While the grid in Figure 1 uses a 16x12 layout, this analysis uses a 12x8 grid based from McKay Johns'work. Credit to McKay for his valuable sharing and contributions. The grid is bases on data from multiple seasons. The numbers in the grid represent values from each location on the pitch. Calculating probabilities of the ball moving to different locations is the foundation for calculating xT. "Moving the ball" can be splitted into three different actions; passes, carries and dribbles. Dribbles on avergage only make up 0.94% of football match events, while passes (28%) and carries (23%) are what happens most often in a match [(Hudl/Statsbomb).([https://github.com/statsbomb/open-data/blob/master/doc/StatsBomb%20Open%20Data%20Specification%20v1.1.pdf]). With a foundational understanding of xT, let’s dive into real-world applications. 

### xT and Winning: Is There a Connection?
Using data from the Premier League 2017/2018 season, I investigated whether teams with higher xT-values consistently performed better, measured with leaguerank. Here only passes are measured, since carries were not implmented in the Statsbomb data at this point.  
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/87e0375a-8bd5-417c-92bd-25f6924c5a9b" alt="L4" style="max-width:90%;"/>
</div> 
The results indicate that top teams generate significantly more xT. The old "Top Six" teams stand apart from the rest, underscoring the influence of xT on league outcomes. Carrying out a correlation test gave more information about the size of connection between xT and league rank.   
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/c63e9dd3-5d22-4603-bde4-01f78be73cc2" alt="L4" style="max-width:80%;"/>
</div> Figure 3. Pearson correlation for xT and leaguerank PL 2017/2018
In this context the correlation coefficient measures the linear relationship between xT and leaguerank. Pearson correlation is measured from -1 to 1 where 1 meaning xT-value explaining all league ranks, 0 meaning there is no connection, and -1 is negative correlation (Leaguerank is flipped for the correlation test, avoiding negative correlation-value (high xT and low leaguerank(1.place is originally low league rank, so here it was flipped)). There is a strong relationship (0.785) between xT and leaguerank. Teams that accumulated more xT were more likely to finish higher in the table. After establishing xT’s relevance for 2017/2018, let’s now apply this lens to modern football and EURO 2024.
### EURO 2024 
For this analysis xT is split into passes and carries. 
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/e195b057-a81b-4d99-9a13-5767713ed259" alt="L4" style="max-width:80%;"/>
</div> 
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/3af088bd-38cb-49a4-99e5-58b6338d3171" alt="L4" style="max-width:80%;"/>
</div> 

<div style="text-align:center;">
  <img src="ACC_xT_pass_carries](https://github.com/user-attachments/assets/25dd981d-7530-4b69-b9d5-bff10cd8a163" alt="L4" style="max-width:80%;"/>
</div> 




Sources:   
[Wearebrighton(2024)](https://www.wearebrighton.com/newsopinion/how-simon-adingra-and-ivory-coast-became-afcon-champions/)  
(([https://www.wearebrighton.com/newsopinion/how-simon-adingra-and-ivory-coast-became-afcon-champions/])).

[Statsbomb](https://github.com/statsbomb/open-data/blob/master/doc/StatsBomb%20Open%20Data%20Specification%20v1.1.pdf)  
(([https://github.com/statsbomb/open-data/blob/master/doc/StatsBomb%20Open%20Data%20Specification%20v1.1.pdf])).

[Worville, T. (2021)](https://www.nytimes.com/athletic/2751525/2021/08/06/introducing-expected-threat-or-xt-the-new-metric-on-the-block/)  
(([https://www.nytimes.com/athletic/2751525/2021/08/06/introducing-expected-threat-or-xt-the-new-metric-on-the-block/])).

[Sumpter, D. (2022)](https://soccermatics.readthedocs.io/en/latest/lesson4/xTPos.html)  
(([https://soccermatics.readthedocs.io/en/latest/lesson4/xTPos.html])).

[Singh, K. (2018)](https://karun.in/blog/expected-threat.html)  
(([https://karun.in/blog/expected-threat.html])).

[Soccerment](https://soccerment.com/expected-threat/)  
(([https://soccerment.com/expected-threat/])).


