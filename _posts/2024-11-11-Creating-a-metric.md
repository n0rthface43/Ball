---
title: "Creating a football metric"
excerpt_separator: "<!--more-->"
categories:
  - Player analysis
  - Team analysis
  - Modelling football
tags:
  - Premier League
---
------------
### A machine learning model
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


### Context
During soccermatics course, I was tasked with creating a new football metric. This involved building a machine learning model, using it to evaluate players. In this article, I summarize the metric and the process behind it. As a part of the task, Leicester was the club we (my group) selected to "scout" for. Wyscout data from the 2017/2018 season were used.
### Introduction 
<div class="figure-text">
  <img src="https://github.com/user-attachments/assets/35ebe3fb-bd73-4841-ba97-034a8a02fd3e" alt="L1" style="margin-right: 20px; width: 40%;" />
  <p> In a low-scoring sport like football, every goal-scoring opportunity is crucial. Increasing the number and quality of chances can make a significant difference. The aim of this task was both simple and challenging: Identify passes that directly lead to goals and the players who make them.
  This goal led to formulating a machine learning problem: finding the goal probability for the next event after a pass. The result is a new metric, Direct-Expected Assist (Direct-xA), defined as the goal probability in the next event following a pass that leads to a shot. </p> 
</div>

Direct-expected assist (Direct-xA) measures the likelihood that the next event after a pass will be a goal. This article details how the metric was developed and which players could be valuable signings based on this metric. 
### Variables and Approach
When examining passes that lead to shots, start and end locations were chosen as variables. The pitch was divided into five vertical lanes to include half-spaces (Maric, 2014). Mpl-soccer was used to create pitches, and half-space lines were extended and a horizontal line through the penalty area was added. In addition to location, seven pass-type variables (cross, high cross, low cross, long ground, long high, long launch, and smart pass) from the wyscout data were selected. Certain pass types may increase the likelihood of a goal, aiding in scouting players who excel at delivering these passes. Descriptive statistics were generated for passes leading to shots and goals. Below the two figures show number of passes which directly led to shots (top figure), and passes which lead to goal (bottom figure) from the different areas.
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/a3ec810e-d733-46e3-bb40-d37e4c08c800" alt="L3" style="max-width:80%;"/>
</div>
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/dff2b8d3-7a75-41dd-bf10-21504a5efb3b" alt="L3" style="max-width:80%;"/>
</div>

### Data Processing
The Wyscout data included the top five European leagues from the 2017/2018 season. A big dataset which gave a good foundation for creating the model. Passes were filtered to those starting and ending in the final third. The probability for a goal in the next event later became the output variable in the logistic regression model.
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/3f98d6b8-87c9-4afc-9f8e-0d1b469a946f" alt="L4" style="max-width:80%;"/>
</div>
The figure shows goal probability for the next event given different start location areas for the pass. Numbers indicates the obvious, a pass closer to goal increase probability for a goal in next event. For the end location (figure below), the goal probability is even higher in areas closer to the goal. 
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/0dede729-cfa6-4e91-ad67-b43a45fe6208" alt="L5" style="max-width:80%;"/>
</div>
However, compared to start location the goal probability increase more (compared to start location) for the end location area closest to the goal (0.38). And the probability is also really high (0.17) for the area in the middle straight inside the 18-yard box. This figure have similarities with the classic xG-model, where the distance and angle to the goal are important as David Sumpter explain [here](https://soccermatics.readthedocs.io/en/latest/lesson2/introducingExpectedGoals.html).
The difference in my model is the inclusion of the pass type and location for the pass before the shot as variables. Some outliers (ex. high value in the right corner) result from very few samples from that spesific area. A low number of passes ending in the right corner with a rare goal can explain the high probability in the red corner. 
### Model development
One hot encoding was used for handling the nominal categories and creating dummy variables. Both the start and end areas each have 15 categories, one for each respective area on the pitch. The pass-types categories were represented with one category each. Each category was given a dummy variable (1 and 0).  To avoid the ‘dummy trap’ one dummy variable for each category was removed. The next step was using logistic regression to create a model. The data set was divided into training and test data, for training and testing the model on different data. This was all done by using functions from the sklearn-module. Lasso (penalty =’l1’) was used for regulation.
<div <div class="figure-text">
  <img src="https://github.com/user-attachments/assets/53710975-8951-40e1-b7c9-ee15e3f5c2c3" alt="L6" style="width:50%;"/> <p>
The first attempts gave no promising results. The message "Maximum Likelihood optimization failed to converge" occurred multiple times. This often happens due to multicollinearity.Crosses, types of long-passes, and areas on the side of the pitch for both start and end location were removed to get the model to converge (find stable coefficient estimates).This choice was based on the high p-values. Another tool was using an 'lbfgs' method from a statsmodels-module to optimize training of the model. </p> 
</div>

### Results
Finally, the model did converge with significant p-values. Results show smartpass significantly increased the likelihood for a pass giving a goal. Wyscout defines smartpass as a “A creative and penetrative pass that attempts to break the opposition's defensive lines to gain a significant advantage in attack” (Wyscout, 2024). 
<div 
  <img src="https://github.com/user-attachments/assets/35ebe3fb-bd73-4841-ba97-034a8a02fd3e" alt="L1" style="margin-right: 20px; width: 40%;" />
  <p>
<div class="figure-text">
  <img src="https://github.com/user-attachments/assets/662260ad-487b-49aa-9294-d9690525d534" alt="L8" style="margin-right:20px; width:50%;"/> <p> Adding a player with ability to deliver more smartpasses into these areas could add value to the team and increase goal probability. All six close-to-goal areas were significant for both start and end location. On the left is coefficients for start location and smart pass(pass type). The figure also illustrate the area just outside the 18-yard box were also significant for start locations.</p> 
</div>
<div class="figure-text">
  <img src="https://github.com/user-attachments/assets/9a20ed3e-7316-43e7-a13f-551a912f332c" alt="L14" style="margin-left: 10%; margin-right: 30px; width: 40%;" />
  <p style="margin-top: 20px;"> 
    For end location there is a really high value in front of the goal (0.88) and the area which include the penalty area. In a football context this makes sense, considering the increase in likelihood for scoring from these areas. No significant value outside the box. Receiving and shooting from those areas in next event does not increase likelihood for scoring.
  </p>
</div>

<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/6752a8ae-39f5-4e9e-8ce2-bb4e3147d294" alt="L5" style="max-width:80%;"/>
</div>
A ROC-test (receiver operating characteristic curve) was done to test the accuracy. A score of 0.75 shows selected variables are relevant for predicting goal probability, and better than a wild guess. The score also says there are other variables outside the model that might affect the outcome. Knowing the model measure passes that leads to shots in the next event, also means the model does not give information about all the events afterwards. When using the model, these limitations should be taken into account.

### Applying the model
Using the model gave direct expected assist for each player. The numbers are adjusted to per 90. There is a threshold for players with at least 300 minutes.  After normalizing for minutes,  the table show the direct expected assist per 90 (in the table below’ xA_per90’ is used as a shorter term for that). 

<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/96ceee42-020c-4763-aa1f-a44598f07016" alt="L18" style="max-width:100%;"/>
</div> 

Figure shows potential transfer targets. Players realistically available considering club, value and reputation are highlighted. Based on the model, signing Lorenzo Insigne is the top suggestion. A short-list with three names contains Lorenzo Insigne, Isaac Succes and Dominik Solanke. Karim Bellarabi might be an option, is 30 years of age, other options should be considered.  

![i](https://github.com/user-attachments/assets/ee307410-a85e-4172-904e-5cdba9361d22)

Lorenzo Insigne will cost around 60 m euros, and he will demand a high salary. He will be the most likely to produce most direct-expected assist per 90 from our targets. He also have played a lot of minutes, which makes him a safer option. Isaac Success is a budget option, with great numbers, but low minutes.

### Summarize
Analyzing the results still gave valuable insight about the Direct - expected assist. Findings suggest penetrating and creative passes (smartpass) and the importance of getting into areas close to goal for start location, and in front of goal for end location was important. Developing a machine learning model and create this metric was a great learning experience. I still would not use it for scouting, because I think such a metric metric should include events after the ball get into dangerous areas. Thanks to Ágúst and Nicole for great help in the process!

Sources 
Maric, R. (2014). The Half-Spaces. https://spielverlagerung.com/2014/09/16/the-half-spaces/
Wyscout, W. (2024). Smart pass. https://dataglossary.wyscout.com/smart_pass/

