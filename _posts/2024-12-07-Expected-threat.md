---
title: "Using xT - on three continents"
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
In a low scoring sport like football, shots and goals are rare. What happens most often in a football match are During EURO last summer 45630 passes and 44139 carries were completed. In this article I will explore which passes and carries that adds value, and finding the players best at conducting those passes and carries. Expected threat, or xT will be the metric used. More spesifically I will use position-based expected threat, and try answering following questions: 
- Is there any correlation between position-based xT and winning?
- Which teams and players created most threat per game in EURO 2024?
- Who are best in xT for carries?
Finally I will use xT to evaluate players in different positions from Euro (2024) Copa America (2024) and Africa Cup of Nations (2023). Was Messi top? And who are best for carries? Hang on and find out! 

There are different types of expected threat. On-ball-value, possession-value, position- and action-based expected threat are a few. They all have in common ending up giving a value to either the position on the pitch or action on the ball. I will briefly go through position-based expected threat before using the metric to evaluate players. 

The basics of position-based expected threat is setting a value to each point or location on the pitch. And that value is the expected threat, or xT. xT tell us if moving the ball from one to another location on the pitch increase or decrease the chance of scoring before ball get lost to opposition or get out of play.
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/203f262a-a956-484a-b12f-3b65a1e2f393" alt="L4" style="max-width:80%;"/>
</div> Figure 1. Expected threat grid. Worville, Tom. (2021)([https://www.nytimes.com/athletic/2751525/2021/08/06/introducing-expected-threat-or-xt-the-new-metric-on-the-block/])

The grid above is an example with xT values for all locations on the pitch, divided into bins. Attacking from left to right, values increase close to opposition goal. xT-values is set from 0.0 - 1.0. Outside the box one location(A) have a value of 0,034. This means scoring directly from here or scoring after moving the ball to another location is given a 3,4 % chance. If ball is moved from (A) to (B) we can calculate xT. The xT-value is the difference between those two values.  
xT = xT(B)-xT(A) 
xT =0,134-0,0134 = 0,1 
The player moving the ball is credited with 0,1 xT. 0,1 means the player increased the chance for his team scoring by 10 %. "Moving" the ball can be splitted into three different actions; passes, carries and dribbles. Dribbles on avergage only make up 0.94% of match events, while passes (28%) and carries (23%) are what happens most often in a match [(Hudl/Statsbomb).]([https://github.com/statsbomb/open-data/blob/master/doc/StatsBomb%20Open%20Data%20Specification%20v1.1.pdf]). For this analysis I will focus on passes and carries when evaluating players.            
For this analysis I have used a 12 x 8 grid, shared by Mc Kay Johns. Credit to him for both explaining and sharing. The grid is bases on data from multiple seasons. First I want to know if this metric is relevant at all, so testing it on Premier League season 2017/2018.  

Is there any correlation between xT and winning?
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/87e0375a-8bd5-417c-92bd-25f6924c5a9b" alt="L4" style="max-width:80%;"/>
</div> 
The figure indicates the best teams clearly accumulate more xT then the rest. Also interesting to see the gap between the old top six, and how far away the rest were (I think we can assume that is different today:)). A correlation test between league rank and xT can give us more information about the connection. 
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/c63e9dd3-5d22-4603-bde4-01f78be73cc2" alt="L4" style="max-width:80%;"/>
</div> 
0,75 is a suprisingly big correlation (correlation is measured from 0-1 where 1 is full corrrelation, meaning xT explaining all league ranks). I say that because newere and more popular metrics like on-ball-value and other types of action-based expected threat are more popular then position-based. That correlation does tell the metric is relevant. Now lets use this on EURO 2024.  



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

