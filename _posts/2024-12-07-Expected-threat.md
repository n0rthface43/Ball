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
In football, we often talk about goals and shots, but what if the most important actions happen long before the ball reaches the net? With expected threat we can quantify how teams and players create dangerous situations – and perhaps even predict who will win. During EURO last summer, 45,630 passes and 44,139 carries were completed. This article explores which of these actions add the most value and identifies the players and teams excelling at them. Using <em> position-based expected threat </em> (xT), I will explore questions such as:
- Is there a connection between xT and winning?
- Which teams and players created most xT per game during EURO 2024?
- Which player positions are most efficient at creating xT?
### Position-based expected threat
Position-based expected threat assigns a <em> value </em> to each point on the pitch. That value is the expected threat: xT. This value is the probability of scoring either directly from that position, or after moving the ball elsewhere before ball is lost or out of play. We can think of xT as a way to measure how ‘dangerous’ a specific ball move is. If you move the ball from a harmless position to a more threatening one, your team’s chances of scoring increase. These types of moves can be calculated and quantified, which gives us the xT value. <br> 
### The grid
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/203f262a-a956-484a-b12f-3b65a1e2f393" alt="L4" style="max-width:80%;"/>
</div> Figure 1. Grid from The Athletic. Worville, Tom. (2021)
xT values are calculated using a grid. The grid above is an example with 16x12 bins, each containing xT for that area. xT values are set from 0-1. A value of 1 means that every action from that location would result in a goal, either directly from a shot, or indirectly after moving the ball elsewhere. The values obviously increase the closer we get to the opposition goal (attacking from left to right in figure). Location (A) has a value of 0.034. This means that there is a 3.4% chance of scoring directly from here or scoring after moving the ball to another location. If the ball is moved from (A) to (B), we can calculate xT as follows:
\[xT = xT(B) - xT(A) \\[5pt]
xT = 0.134 - 0.034 = 0.1
\]
The player moving the ball is credited with 0.1 xT, increasing the team's chance of scoring by 10%. 
While the grid in Figure 1 uses a 16x12 layout, this analysis uses a 12x8 grid, taken from McKay Johns' github (link in description). Credit to him for his valuable sharing and contributions. The grid is based on data from multiple seasons. The numbers in the grid represent values for each location on the pitch. Calculating probabilities of the ball moving to different locations is the foundation for calculating xT. "Moving the ball" can be split into three different football actions: passes, carries and dribbles. David Sumpter from Twelve has written an article about this, where he covers it more in-depth: [here](([https://soccermatics.readthedocs.io/en/latest/lesson4/xTPos.html])). <br>
With a foundational understanding of xT, let’s move into real-world applications. 

### xT and Winning: Is There a Connection?
Using data from the Premier League 2017/2018 season, I investigated whether teams with higher xT values consistently performed better, measured with leaguerank. Here, I only measure passes, as carries were not a part of the Statsbomb data at that point.  
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/8091bea4-22c1-4166-b3f1-62cba2c1dffb" alt="L4" style="max-width:90%;"/>
</div> 

The results indicate that top teams generate significantly more xT. The old "Top Six" teams stand apart from the rest, underscoring the influence of xT on league outcomes. Carrying out a correlation test gave more information about the size of connection. There are definately more factors affecting the outcome, but there is reason to argue that xT is relevant.  
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/c63e9dd3-5d22-4603-bde4-01f78be73cc2" alt="L4" style="max-width:80%;"/>
</div> Figure 3. Pearson correlation for xT and leaguerank PL 2017/2018 <br>
The correlation coefficient measures the linear relationship between xT and leaguerank. Pearson correlation is measured from -1 to 1, where 1 meaning xT value explaining all league ranks, 0 meaning there is no connection, and -1 is negative correlation. Here, leaguerank is flipped to avoid negative correlation (1st place would originally mean low league rank, and combination of high xT and low leaguerank would then give negative correlation). There is a strong relationship (0.785) between xT and leaguerank. Teams that accumulated more xT were more likely to finish higher in the table. After establishing xT’s relevance for 2017/2018, let’s apply this to present time and EURO 2024.
### EURO 2024
Here are three examples of different passes and their xT values during EURO 2024. These passes had some of the highest xT values in the tournament.
{% include video id="YS2X1fw62Ko" provider="youtube" %}
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/e1745eb0-a848-4914-ac6b-a65865f9f56b" alt="L4" style="max-width:80%;"/>
</div> <br>
<div style="text-align:center;">
Francisco Conceição (Portugal) leads the xT chart: The threshold for minutes is set to a minimum of 150, and he was effective while playing (played 202 minutes). I split xT into separate charts for passes and carries, which gives a more clear picture of the two different actions.
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/6d5e85de-f2b5-41d0-94c4-0d51581c8198" alt="L4" style="max-width:80%;"/>
</div> <br>
One observation from this figure is the much higher number of xT created by passes, compared to carries. Passing is an easier way to get the ball into dangerous areas, unless your name is Jeremy Doku. Doku is a clear example of a player tasked with carrying the ball and creting chances. A comparison between players make more sense for players in similar position and roles (original positions is taken from Hudl/Statsbomb lineups). From those positions, I then made six groups.  
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/4a9c89d7-fd05-4d3c-b66e-d7cae55b0bc5" alt="L4" style="max-width:80%;"/>
</div> 
The figure above indicates a high amount of carries for wingers, as well as passes and carries for both defence and central midfielders. The low average for forwards could maybe be explained by low involvement. The wingers and CMs stand out for carries. Accumulating xT might be easier for a winger or a central midfielder who recieves the ball wider or deeper. 
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/f8e2690c-975a-4b59-a2ba-7ee2fed5a203" alt="L4" style="max-width:80%;"/>
</div> <br>
Wingers are top for carries, and high for passes as well. This confirms Doku's special ability of running with the ball. It also shows top passers like Eriksen and Tadic, as well as players who excell at doing both, like Conceição and Williams.  
<br>
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/4f352477-0ec7-420b-a12d-254f71b5c046" alt="L4" style="max-width:80%;"/>
</div>
In center midfield we see many players scoring high for both passes and carries. Baumgartner (Switzerland) stands out with extrordinary high xT from passes, and Bruno for carries. The numbers are even more impressive for players who reached the final stages of the tournament (like Pedri, Olmo and Simons), who managed to deliver high xT numbers for more games.

### Summing up: Advantages and limitations
As I have shown in this article, xT is all about assigning a value to each location on the pitch, and finding the difference between the start and end location after moving the ball. This value difference is the expected threat, which tells us if the moving action increased or decreased the chance of scoring a goal. This way, even a pass on your own half can be measured as valuable, which in my opinion is one of the great properties that xT contains: xT measures ball movements that are not shots or goals (shots is less than 1% of the events). Another property, is that xT is quite simple both to implement and understand, and it can provide useful information about teams and players. One limitation with xT, however, is that it only uses the location of the ball, and does not take other factors into account (i.e. position of opponents and teammates, type of pass, pressure, passage of play, etc.) That is where an action based model like on-ball-value or other possession value models come into play and can add valuable context. More of that in a later article.



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


