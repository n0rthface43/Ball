---
title: "Using xT - and the connection with winning?"
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
- Is there a connection between xT and winning?
- Which teams and players created most xT per game during EURO 2024?
- Which player positions are most efficient at creating xT?<br> Inside football analytics there are different versions of expected threat. On-ball-value, possession-value, position- and action-based expected threat are examples. I will briefly go through position-based expected threat before using the metric to evaluate players. <br>
### Position-based expected threat
Position-based expected threat assigns a <em> value </em> to each point on the pitch. That value is the expected threat, or xT. This value is the probability of scoring either directly from that position, or after moving the ball elsewhere before ball is lost or out of play. David Sumpter from Twelve have written a great article about this. You can read more [here](([https://soccermatics.readthedocs.io/en/latest/lesson4/xTPos.html])).  
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/203f262a-a956-484a-b12f-3b65a1e2f393" alt="L4" style="max-width:80%;"/>
</div> Figure 1. Grid from The Athletic. Worville, Tom. (2021)

The grid above is an example with xT values divided into bins. xT-values are set from 0-1. A value of 1.0 means that every action from that location would result in a goal, either directly from a shot or indirectly after moving the ball elsewhere. Values obviously increase closer to the opposition goal (Attacking from left ot right in figure).
Location (A) has a value of 0.034. This means scoring directly from here or scoring after moving the ball to another location has a 3.4% chance. If the ball is moved from (A) to (B), we can calculate xT as follows:
\[
xT = xT(B) - xT(A) \\[5pt]
xT = 0.134 - 0.034 = 0.1
\]

The player moving the ball is credited with 0.1 xT, increasing the team's chance of scoring by 10%.


### The grid
While the grid in Figure 1 uses a 16x12 layout, this analysis uses a 12x8 grid taken from McKay Johns' github (link in description). Credit to him for his valuable sharing and contributions. The grid is bases on data from multiple seasons. The numbers in the grid represent values for each location on the pitch. Calculating probabilities of the ball moving to different locations is the foundation for calculating xT. "Moving the ball" can be splitted into three different football actions; passes, carries and dribbles. Dribbles on avergage only make up 0.94% of football match events, while passes (28%) and carries (23%) are what happens most often in a match [(Hudl/Statsbomb).([https://github.com/statsbomb/open-data/blob/master/doc/StatsBomb%20Open%20Data%20Specification%20v1.1.pdf]). With a foundational understanding of xT, let’s dive into real-world applications. 

### xT and Winning: Is There a Connection?
Using data from the Premier League 2017/2018 season, I investigated whether teams with higher xT-values consistently performed better, measured with leaguerank. Here only passes are measured, since carries were not implmented in the Statsbomb data at this point.  
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/8091bea4-22c1-4166-b3f1-62cba2c1dffb" alt="L4" style="max-width:90%;"/>
</div> 

The results indicate that top teams generate significantly more xT. The old "Top Six" teams stand apart from the rest, underscoring the influence of xT on league outcomes. Carrying out a correlation test gave more information about the size of connection.   
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/c63e9dd3-5d22-4603-bde4-01f78be73cc2" alt="L4" style="max-width:80%;"/>
</div> Figure 3. Pearson correlation for xT and leaguerank PL 2017/2018 <br>
In this context the correlation coefficient measures the linear relationship between xT and leaguerank. Pearson correlation is measured from -1 to 1 where 1 meaning xT-value explaining all league ranks, 0 meaning there is no connection, and -1 is negative correlation (Leaguerank is flipped to avoid negative correlation (1.place would originally mean low league rank where high xT and low leaguerank would have give negative correlation, so here it was flipped in purpose of avoiding negative values)). There is a strong relationship (0.785) between xT and leaguerank. Teams that accumulated more xT were more likely to finish higher in the table. After establishing xT’s relevance for 2017/2018, let’s now apply this lens to modern football and EURO 2024.
### EURO 2024 
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/e1745eb0-a848-4914-ac6b-a65865f9f56b" alt="L4" style="max-width:80%;"/>
</div> <br>
Francisco Conceição (Portugal) leading the chart. He just got himself into this list after playing 202 minutes (threshold for minutes is set to minimum 150). Splitting xT into separate charts for passes and carries gives a more clear picture about different abilities.
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/6d5e85de-f2b5-41d0-94c4-0d51581c8198" alt="L4" style="max-width:80%;"/>
</div> <br>

One observation from this, is the much higher number of xT created by passes compared to carries. Passing is an easier way to get the ball into dangerous areas, unless your name is Jeremy Doku (or Messi). Doku is en example of a player tasked with carrying the ball and creting chances. A comparison between players for xT-numbers makes more sense for players in similar position and roles (original positions is taken from Hudl/Statsbomb lineups). From those positions I made six groups.  
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/4a9c89d7-fd05-4d3c-b66e-d7cae55b0bc5" alt="L4" style="max-width:80%;"/>
</div> 
This give more information about what xT-numbers to expect from players in different positions. The figure indicates high carries for wingers, passing and carries for both defence, and central midfielders. The low average for forwards is interesting. Starting actions in a position far up the pitch will give a high xT for the starting position, which might make it more difficult getting the ball to an even more dangerous location, which would be easier for a winger or a central midfielder recieving ball wider or deeper. The wingers and CMs also stand out for carries. Checking spesific positions will tell us who the best players for xT are in spesific positions. 
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/f8e2690c-975a-4b59-a2ba-7ee2fed5a203)" alt="L4" style="max-width:80%;"/>
</div> <br>
WIngers are top for carries, and high for passes as well. This confirms Dokus special ability of running with the ball. It also show top passers like Eriksen and Tadic. And players who excel at doing both, like Conceição and Williams.  
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/f8e2690c-975a-4b59-a2ba-7ee2fed5a203)" alt="L4" style="max-width:80%;"/>
</div> <br>

<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/4f352477-0ec7-420b-a12d-254f71b5c046)" alt="L4" style="max-width:80%;"/>
</div>
In center midfield we see a lot of players are high for both. Baumgartner (Switzerland) stands out with extrordinary high xT from passing, and Bruno for carries. The numbers are more impressive for players reaching the final stages and playing more minutes, because they have managed to delivered high xT numbers for more games.

### Advantages and limitations
To summarize, xT is as all about assigning a value to each location on the pitch, and finding the difference in those value for start and endlocation after moving the ball. That value tell if the action increases the chance of scoring a goal, and even a pass on your own half can be measured as valuable in this way. And that is the great ability xT contain. It measure something in football which is not a shot or goal, and that can be a good thing (shots is less than 1% of the events). Using the difference in location between action-start and stop, give a simple number which tells if your action increased or decreased the chance for scoring. Another benefit is that xT is quite simple to both implement and understand. If you have the grid, you can find the xT with basic event data (must contain location for passes and carries). A third benefit, is the many possibility for using it. Here we have used it for evaluating both team and players. The limitation with xT is that it only use the location of the ball. It does not take other factors into account, like where the opposition are, type of pass, pressure, passage of play etc. That is where an action based models comes into play. For exammple possession-value or on-ball-value explore. And that will make the content for another article! 




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


