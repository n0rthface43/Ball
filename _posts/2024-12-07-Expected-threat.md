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
Football is a low-scoring sport where goals are rare, but passes and carries dominate the action. During EURO last summer, an incredible 45,630 passes and 44,139 carries were completed. This article explores which of these actions add the most value—and identifies the players excelling at them. Using position-based expected threat (xT), I will answer key questions, such as:
- Is there a correlation between xT and winning?
- Which teams and players created the most xT per game during EURO 2024?
- Who excelled at xT from carries?

There are different types of expected threat. On-ball-value, possession-value, position- and action-based expected threat are a few. They all have in common ending up giving a value to either the position on the pitch or action on the ball. I will briefly go through position-based expected threat before using the metric to evaluate players. 
### Position-based expected threat
Position-based expected threat assigns a value to each point on the pitch. That value is the expected threat, or xT. This value is the probability of scoring, either directly from that position or after moving the ball elsewhere. 

<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/203f262a-a956-484a-b12f-3b65a1e2f393" alt="L4" style="max-width:80%;"/>
</div> Figure 1. Grid fromt The Athletic. Worville, Tom. (2021)

The grid above is an example with xT values for all locations on the pitch, divided into bins. Attacking from left to right, values obviously increase close to opposition goal. xT-values is set from 0.0 - 1.0. Outside the box one location(A) have a value of 0,034. This means scoring directly from here or scoring after moving the ball to another location is given a 3,4 % chance. If ball is moved from (A) to (B) we can calculate xT, using values from both locations. The xT-value is the difference between those two values. 
xT = xT(B)-xT(A) 
xT =0,134-0,0134 = 0,1 
The player moving the ball is credited with 0,1 xT. 0,1 means the player increased the chance for his team scoring by 10 %. 

### The grid
While the grid in Figure 1 uses a 16x12 layout, this analysis uses a 12x8 grid based on McKay Johns' work. Credit to McKay for his valuable contributions in sharing and explaining the methodology. The grid is bases on data from multiple seasons. When calculating xT moving of the ball is a requirement. "Moving" the ball can be splitted into three different actions; passes, carries and dribbles. Dribbles on avergage only make up 0.94% of football match events, while passes (28%) and carries (23%) are what happens most often in a match [(Hudl/Statsbomb).([https://github.com/statsbomb/open-data/blob/master/doc/StatsBomb%20Open%20Data%20Specification%20v1.1.pdf]). With a foundational understanding of xT, let’s dive into real-world applications. 

### xT and Winning: Is There a Connection?
Using data from the Premier League 2017/2018 season, I investigated whether teams with higher xT- values consistently performed better, measured with leaguerank. The results, illustrated in Figure 2, suggest that top teams generate significantly more xT. The old "Top Six" teams stand apart from the rest, underscoring the influence of xT on league outcomes. 
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/87e0375a-8bd5-417c-92bd-25f6924c5a9b" alt="L4" style="max-width:80%;"/>
</div> 
A correlation test between league ranks and xT values shows a strong relationship (0.75). This means teams that create higher xT are more likely to finish higher in the table. Let’s now apply this lens to EURO 2024.

The figure indicates the best teams clearly accumulate more xT then the rest. Also interesting to see the gap between the old top six, and how far away the rest were (I think we can assume that is different today:)). A correlation test between league rank and xT can give us more information about the connection.  
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/c63e9dd3-5d22-4603-bde4-01f78be73cc2" alt="L4" style="max-width:80%;"/>
</div> Figure 2. xT from passes and leaguerank PL 2017/2018  
Correlation is measured from 0-1 where 1 meaning xT-value explaining all league ranks and 0 meaning there is no connection. Leaguerank is flipped for the correlation test, for avoiding negative correlationvalue (high xT and low leaguerank). After establishing xT’s relevance for league football, let’s evaluate its role in international tournaments

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
[Wearebrighton(2024)](([https://www.wearebrighton.com/newsopinion/how-simon-adingra-and-ivory-coast-became-afcon-champions/])).
[Statsbomb](([https://github.com/statsbomb/open-data/blob/master/doc/StatsBomb%20Open%20Data%20Specification%20v1.1.pdf])).
[Worville, T. (2021)](([https://www.nytimes.com/athletic/2751525/2021/08/06/introducing-expected-threat-or-xt-the-new-metric-on-the-block/]))
[Sumpter, D. (2022)](([https://soccermatics.readthedocs.io/en/latest/lesson4/xTPos.html]))
[Singh, K. (2018)](([https://karun.in/blog/expected-threat.html]))
[Soccerment](([https://soccerment.com/expected-threat/]))

