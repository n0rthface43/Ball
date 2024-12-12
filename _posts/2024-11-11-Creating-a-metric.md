---
title: "Creating a metric"
excerpt_separator: "<!--more-->"
categories:
  - Player analysis
  - Team analysis
  - Modelling football
tags:
  - Premier League
---
------------
### A machine learning model - in football
------------
### Context
During soccermatics course, I was tasked with creating a new football metric. This involved building a machine learning model, using it to evaluate players. In this article, I summarize the metric and the process behind it. As a part of the task, Leicester was the club we (my group) selected to "scout" for. Wyscout data from the 2017/2018 season were used.
### Introduction 
<div style="display: flex; align-items: flex-start;">
  <img src="https://github.com/user-attachments/assets/35ebe3fb-bd73-4841-ba97-034a8a02fd3e" alt="L1" style="margin-right:20px; width:40%;"/> <p>In a low-scoring sport like football, every goal-scoring opportunity is crucial. Increasing the number and quality of chances can make a significant difference. The aim of this task was both simple and challenging: Identify passes that directly lead to goals and the players who make them.
This goal led to formulating a machine learning problem: finding the goal probability for the next event after a pass. The result is a new metric, Direct-Expected Assist (Direct-xA), defined as the goal </p> </div> probability in the next event following a pass that leads to a shot. Direct-expected assist (Direct-xA) measures the likelihood that the next event after a pass will be a goal. This article details how the metric was developed and which players could be valuable signings based on this metric. When examining passes that lead to shots, start and end locations were chosen as variables. The pitch was divided into five vertical lanes to include half-spaces (Maric, 2014). Mpl-soccer was used to create pitches, and half-space lines were extended and a horizontal line through the penalty area was added.
### Variables and Approach
In addition to location, seven pass-type variables (cross, high cross, low cross, long ground, long high, long launch, and smart pass) were selected. Certain pass types may increase the likelihood of a goal, aiding in scouting players who excel at delivering these passes. Descriptive statistics were generated for passes leading to shots and goals. The rectangular areas formed the basis for heatmaps. Below figures show number of passes which directly led to shots(top figure and passes which lead to goal(bottom figure) from the different areas.
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/a3ec810e-d733-46e3-bb40-d37e4c08c800" alt="L3" style="max-width:80%;"/>
</div>
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/dff2b8d3-7a75-41dd-bf10-21504a5efb3b" alt="L3" style="max-width:80%;"/>
</div>

### Data Processing
The Wyscout data included the top five European leagues from the 2017/2018 season, which gave a good foundation for creating the model. Passes were filtered to those starting and ending in the final third, as goals often arise from these areas.
The probability for a goal in the next event later became the output variable in the logistic regression model.
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/3f98d6b8-87c9-4afc-9f8e-0d1b469a946f" alt="L4" style="max-width:80%;"/>
</div>
The figure shows goal probability for the next event given the start location of the pass. The probability is highest near the goal, decreasing further away.
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/0dede729-cfa6-4e91-ad67-b43a45fe6208" alt="L5" style="max-width:80%;"/>
</div>
For the end location, the goal probability is even higher in areas closer to the goal. However, compared to start location the goal probability increases a lot for the end location (right figure) area closest to the goal (0.38). And the probability is also really high (0.17) for the area in the middle straight inside the 18-yard box. In a football context this last figure (end location) is confirming knowledge about the importance of the shot location and the classic xG-model. Some outliers (ex. high value in the right corner) result from very few samples from that spesific area. A very low number of passes ending in the right corner with a rare goal can explain the high probability in the red corner.
### Model development
One hot encoding was used for handling the nominal categories and creating dummy variables. Both the start and end areas each have 15 categories, one for each respective area on the pitch. The pass-types categories were represented with one category each. 
Each category was given a dummy variable (1 and 0).  To avoid the ‘dummy trap’ one dummy variable for each category was removed. The next step was using logistic regression to create a model. The data set was divided into training and test data, for training and testing the model on different data. This was all done by using functions from the sklearn-module. Lasso (penalty =’l1’) was used for regulation.
<div style="display:flex; justify-content:space-between; align-items:flex-start; gap:30px;">
  <img src="https://github.com/user-attachments/assets/53710975-8951-40e1-b7c9-ee15e3f5c2c3" alt="L6" style="width:40%;"/> <p>
The first attempts gave no promising results. The message "Maximum Likelihood optimization failed to converge" occurred multiple times.</p> </div>

This often happens due to multicollinearity.  To help decide which features to remove, a VIF-test (Variance Inflation Factor) was carried out to check for multicollinearity among the features. That test gave some high values (see figure above on the right side). Crosses, types of long-passes, and areas on the side of the pitch for both start and end location were removed to get the model to converge (find stable coefficient estimates). This choice was based on the combination of high VIF-values and high p-values. Another tool was using an 'lbfgs' method from a statsmodels-module to optimize training of the model. 

### Results
After multiple changes in the selection of features, the model did converge, and the results showed multiple significant p-values. Smartpass significantly increased the likelihood for a pass giving a goal. Wyscout defines smartpass as a “A creative and penetrative pass that attempts to break the opposition's defensive lines to gain a significant advantage in attack” (Wyscout, 2024).  
Adding a player with ability to deliver more smartpasses into these areas could add value to the team and increase goal probability. 
<div style="display: flex; align-items:flex-start;">
  <img src="https://github.com/user-attachments/assets/662260ad-487b-49aa-9294-d9690525d534" alt="L8" style="margin-right:20px; width:40%;"/> <p> All six close-to-goal areas were significant for both start and end location. Areas just outside the 18-yard box were also significant for start locations.</p> </div>
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/e8477f16-c8ff-4e31-90fc-72f4c21795a3" alt="L14" style="max-width:90%;"/>
</div>
All coefficients for the six areas close to the box were significant, for both start and end location. See values in their respective areas on the pitch (start location on the left and end location on the right).  In addition, the areas straight outside the 18-yard box were significant for the start location.  There is a high value in front of the goal for the end location, which in a football context makes sense, considering the increase in likelihood for scoring from these areas.

![L12](https://github.com/user-attachments/assets/6752a8ae-39f5-4e9e-8ce2-bb4e3147d294)
A ROC-test (receiver operating characteristic curve) was done to test the accuracy. A score of 0.75 shows selected variables are relevant for predicting goal probability, and better than a wild guess. The score also says there are other variables outside the model that might affect the outcome. Knowing the model measure passes that leads to shots in the next event, also means the model does not give information about all the events afterwards. When using the model, these limitations should be taken into account.

### Applying the model
Using the model gave direct expected assist for each player. The numbers are adjusted to per 90. There is a threshold for players with at least 300 minutes.  After normalizing for minutes,  the table show the direct expected assist per 90 (in the table below’ xA_per90’ is used as a shorter term for that). 
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/53d215d1-5635-4c49-a689-f7ff7f97b40a" alt="L13" style="max-width:100%;"/>
</div>
Before signing someone, current Leicester players had to be evaluated. The figure shows direct xA per 90 for current midfielders. One problem were the different task within the team.  Wilfried Ndidi for example, is playing in central midfield and tasked with performing on other metrics, and as a consequence score low on this metric. Therefore, to create a benchmark, top three midfielders performers on the metric from each club in premier league laid the foundation for an average score per 90 which is equal to 0.026. Leicesters top three performers on this metric gave following list: 
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/e8477f16-c8ff-4e31-90fc-72f4c21795a3" alt="L14" style="max-width:100%;"/>
</div>
Based on this evaluation, a suggestion would be consider upgrade Mark Albrighton

Figure: Calculating benchmark
![L14](https://github.com/user-attachments/assets/e8477f16-c8ff-4e31-90fc-72f4c21795a3)

Possible transfers in
<div style="text-align:center;">
  <img src="https://github.com/user-attachments/assets/96ceee42-020c-4763-aa1f-a44598f07016" alt="L18" style="max-width:100%;"/>
</div>    
Players realistically available considering club, value and reputation is highlighted. Based on the model, signing Lorenzo Insigne is my suggestion. A short-list with three names contains Lorenzo Insigne, Isaac Succes and Dominik Solanke. Karim Bellarabi might be an option, but as he is 30 years of age, I suggest other options. Lorenzo Insigne will cost around 60 m euros, and he will demand a high salary. He will be the most likely to produce most direct-expected assist per 90 from our targets. He also have played a lot of minutes, which makes him a safr option. Isaac Success is a budget option, with great numbers, but low minutes.

Sources 
Maric, R. (2014). The Half-Spaces. https://spielverlagerung.com/2014/09/16/the-half-spaces/
Wyscout, W. (2024). Smart pass. https://dataglossary.wyscout.com/smart_pass/

