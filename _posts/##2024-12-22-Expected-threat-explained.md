---
title: "Expected threat - metric explained"
excerpt_separator: "<!--more-->"
categories:
  - Player analysis
  - Team analysis
  - Modelling football
tags:
  - International
---
------------
### Expected threat
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
If football metrics are not your cup of tea, you should click everywhere else, as fast as possible. For this will be a long one:)

In a low scoring sport like football, actions like shots and goals are rare. Most of the time the ball is moved around and ending up everywhere else than in goal. Expected threat is a metric used for evaluating those particular ball movements. And in this article I will dig into this metric and look at different approaches.
<div style="text-align:center; margin-bottom:20px;">
  <img src="https://github.com/user-attachments/assets/f5e85d9e-d250-4866-85a2-471bae04541d" alt="L4" style="max-width:80%;"/>
</div>
Except from ball receipts (25%), passes (28%) and carries (23%) are events that happens more often than every other action. And the difference from the starting and end point of those movements are laying the foundation for expeceted threat, or xT. 
<div style="text-align:center; margin-bottom:10px;">
  <img src="https://github.com/user-attachments/assets/830d66c8-dfe7-4625-9164-727fec1c6b15" alt="L4" style="max-width:80%;"/>
</div>
The metric origins from Sarah Rudd in 2011 who used markov chains. Then [Karun Sing](https://karun.in/blog/expected-threat.html) wrote a famous article in 2018. Newer articles by Tom Worville and David Sumpter have contributed to increase attention and knowledge. This article is heavily inspired by the Soccermatics template. 

When working with this type of metrics, there is important to know what they do measure - and what they dont. Understanding this is key to get the difference and being able to use the metrics in a way that contribute. There is different approaches for both calculate and use expected threat. In this article I will use the position based approach. Position based xT means a value is assigned to every position on the field.  
Expected threat is based on evaluation of scoring or if there is a bigger chance of scoring from the end location. "Chance of scoring" is here based on the expected goal model, giving each number on the field a value between 0 and 1. An area in front of the opposition goal is given a high value. An area far away from the goal is given a low value. Expected threat are the difference in value when the ball is moving between these areas.




Sources: 
[Statsbomb (2019) ]((https://github.com/statsbomb/open-data/blob/master/doc/StatsBomb%20Open%20Data%20Specification%20v1.1.pdf)
[Worville, T. (2021)]((https://www.nytimes.com/athletic/2751525/2021/08/06/introducing-expected-threat-or-xt-the-new-metric-on-the-block/)
[Sumpter, D. (2022)]((https://soccermatics.readthedocs.io/en/latest/lesson4/xTPos.html)
[Singh, K. (2018)]((https://karun.in/blog/expected-threat.html)
