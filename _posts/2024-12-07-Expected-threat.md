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

<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/f5e85d9e-d250-4866-85a2-471bae04541d" alt="L4" style="max-width:80%;"/>
</div>
Football is a low scoring sport, where shots and goals are rare. During Euro 45630 passes and 44139 carries were completed. What happens most often in a football match is passes and carries [Statsbomb]([https://github.com/statsbomb/open-data/blob/master/doc/StatsBomb%20Open%20Data%20Specification%20v1.1.pdf]). In this article I will explore which of those passes and carries that adds value, and finding the best players conducting these actions. Expected threat, or xT will be the analytical framework for doing that. I will briefly go through position based expected threat. Finally I will evaluate players in different positions from Euro (2024) Copa America (2024) and Africa Cup of Nations (2023) will be analyzed. 
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/830d66c8-dfe7-4625-9164-727fec1c6b15" alt="L4" style="max-width:80%;"/>
</div>

In the Euros John Stones was top for highest number of passes, accumulating 526 passes through the tournament, with his teammate in defence Mark Guehi in fifth place. Going back 15 years, knowing this might increase the view on their passing ability. Moving beyond this statistics  Today expected threat exist in more ver
If you want to dig into more about the metric, there is brilliant articles from Karun Singh[Karun Sing](https://karun.in/blog/expected-threat.html), David Sumpter and Tom Worville.Each of them created a grid for the football pitch, with values.  
The idea behind expected threat have becoming popular since Karun Singh, (inspired by work from Sarah Rudd) introduced it in an article in 2018. 


For this article position based expected threat is used. Position bases expected threat means assigning a value to each location of the field. When the ball is moved from A to B, expected threat is the difference in value from those two positions. 
Position based expected threat is one of many approaches among the extended use of expected threat. 
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/ef130c0e-ba6a-47e9-ba91-7700d0e2c3ca" alt="L4" style="max-width:80%;"/>
</div>


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
[Wearebrighton(2024)]([https://www.wearebrighton.com/newsopinion/how-simon-adingra-and-ivory-coast-became-afcon-champions/]).
[Statsbomb]([https://github.com/statsbomb/open-data/blob/master/doc/StatsBomb%20Open%20Data%20Specification%20v1.1.pdf]).
[Worville, T. (2021)]([https://www.nytimes.com/athletic/2751525/2021/08/06/introducing-expected-threat-or-xt-the-new-metric-on-the-block/])
[Sumpter, D. (2022)]([https://soccermatics.readthedocs.io/en/latest/lesson4/xTPos.html])
[Singh, K. (2018)]([https://karun.in/blog/expected-threat.html])


