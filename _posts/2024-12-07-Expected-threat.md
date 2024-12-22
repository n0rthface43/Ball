---
title: "Using xT - looking for value - on three continents"
excerpt_separator: "<!--more-->"
categories:
  - Player analysis
  - Team analysis
  - Modelling football
tags:
  - International
---
------------
### Using xT - who adds most value 
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


What has Simon Adingra, Francisco Conceição and James Rodríguez in common? Hang on, and find out!  
Football is a low scoring sport, shots and goals rare. Passes (28%) and carries (23%) are events that happens more often. During Euros there were 45630 completed passes, and 44139 carries. 


That fact also increase the need for analyzing those passes and carries, looking for value. In this article I will look into which of those passes and carries adding value, using expected threat. 
Before delving into the analysis, there is need for clarifying what xT means. 
Position based xT. That means a value is assigned to every position on the field. 
An area in front of the opposition goal is given a high value. An area far away from the goal is given a low value. Expected threat are the difference in value when the ball is moving between these areas.
If you want to dig into more about the metric, there is brilliant articles from Karun Singh[Karun Sing](https://karun.in/blog/expected-threat.html) and David Sumpter. 

<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/f5e85d9e-d250-4866-85a2-471bae04541d" alt="L4" style="max-width:80%;"/>
</div>
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/830d66c8-dfe7-4625-9164-727fec1c6b15" alt="L4" style="max-width:80%;"/>
</div>

In this article I will use the expected threat, evaluating players from Copa America, Euro and Africa cup of nations. 
The idea behind expected threat have becoming popular since Karun Singh, (inspired by work from Sarah Rudd) introduced it in an article 
is the value(a number between 0 and 1) 


Sources: 
[Statsbomb (2019) ]((https://github.com/statsbomb/open-data/blob/master/doc/StatsBomb%20Open%20Data%20Specification%20v1.1.pdf)
[Worville, T. (2021)]((https://www.nytimes.com/athletic/2751525/2021/08/06/introducing-expected-threat-or-xt-the-new-metric-on-the-block/)
[Sumpter, D. (2022)]((https://soccermatics.readthedocs.io/en/latest/lesson4/xTPos.html)
[Singh, K. (2018)]((https://karun.in/blog/expected-threat.html)


