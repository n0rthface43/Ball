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
### Creating a metric
------------

Introduction
In 
In a low scoring sport like football, every goal opportunity is valuable. Increasing the number of chances and size of each chance can make a huge difference. With that in mind, the aim for this task was as simple and difficult as it sounds: Finding passes that directly create goals and identifying players who make these passes.  The aim led to formulation of a machine learning problem: Finding the goal probability for the next event after a pass. Solving this problem ended in a new metric; Direct – expected assist.  Direct - expected assist is the goal probability in the next event, for a pass leading to a shot. This report looks at how that metric was built, and which players should be on the club’s radar.
When looking into passes leading to shots, start and end location were chosen as variables. For measuring start and end locations, a pitch divided into five vertical lanes was used. This was done to include the half spaces (the areas between the center and wide channels), in the analysis (Maric, 2014). Modules from mpl-soccer were used for creating the pitch, and lines from the half spaces were extended and a horizontal line added through the penalty area. In addition to start and end locations, seven more variables with different pass-types were selected (cross, high cross, low cross, long ground, long high, long launch and smartpass). Specific types of passes could increase the likelihood for the pass leading to a goal, and that knowledge about can help scout the player with ability to deliver those passes.

Data-processing
The data from Wyscout included the big five leagues from the 2017/2018 season. The passes were filtered for starting and ending in the final third. This was mainly because the passes which led to goals mostly occurred in the final third. All pre-shot events that were passes laid the foundation for the rest of the analysis. 
        
Descriptive statistics of passes that led to shots and goals were made, with start location as a variable. The rectangular areas were used for a heat map showing the number of passes from each area; passes leading to a shot on the left and passes leading to goal on the right. Probability for goal was later used as the output variable for the logistic regression. 
         
The two above figures show probability for a pass in the next event to become a goal. For start location (left figure) the heatmap indicates highest probability for goal in next event when pass starts in areas closest to the goal. Probabilty was also high in the other areas inside the 18-yard box, and then decrease more outside the box, along the byline and further from goal vertically. However, compared to start location the goal probability increases a lot for the end location (right figure) area closest to the goal (0.38). And the probability is also really high (0.17) for the area in the middle straight inside the 18-yard box. In a football context this last figure (end location) is confirming knowledge about the importance of the shot location and the classic xG-model. What looks a bit odd, however, is the high probability in the area on the right corner; this number (0.33) does not makes sense in a football context, and looks like an outlier. Checking the opposite corner, ‘nan’-values is the result because no passes ended there and gave a goal in next event. A very low number of passes ending in the right corner with a rare goal can explain the high probability in the red corner.
Model development
One hot encoding was used for handling the nominal categories and creating dummy variables. Both the start and end areas each have 15 categories, one for each respective area on the pitch. The pass-types categories were represented with one category each. 
Each category was given a dummy variable (1 and 0).  To avoid the ‘dummy trap’ one dummy variable for each category was removed. The next step was using logistic regression to create a model. The data set was divided into training and test data, for training and testing the model on different data. This was all done by using functions from the sklearn-module. Lasso (penalty =’l1’) was used for regulation.
The first attempts gave no promising results. The message "Maximum Likelihood optimization failed to converge" occurred multiple times.  This often happens due to multicollinearity.  To help decide which features to remove, a VIF-test (Variance Inflation Factor) was carried out to check for multicollinearity among the features. That test gave some high values (see figure above on the right side).   Crosses, types of long-passes, and areas on the side of the pitch for both start and end location were removed to get the model to converge (find stable coefficient estimates). This choice was based on the combination of high VIF-values and high p-values. Another tool was using an 'lbfgs' method from a statsmodels-module to optimize training of the model. 
Results
After multiple changes in the selection of features, the model did converge, and the results showed multiple significant p-values. Smartpass significantly increased the likelihood for a pass giving a goal. Wyscout defines smartpass as a “A creative and penetrative pass that attempts to break the opposition's defensive lines to gain a significant advantage in attack” (Wyscout, 2024).  
Adding a player with ability to deliver more smartpasses into these areas could add value  to the team and increase goal probability. All coefficients for the six areas close to the box were significant, for both start and end location. See values in their respective areas on the pitch (start location on the left and end location on the right).  In addition, the areas straight outside the 18-yard box were significant for the start location.  There is a high value in front of the goal for the end location, which in a football context makes sense, considering the increase in likelihood for scoring from these areas. 

A ROC-test (receiver operating characteristic curve) was done to test the accuracy. A score of 0.75 shows selected variables are relevant for predicting goal probability, and better than a wild guess. The score also says there are other variables outside the model that might affect the outcome. Knowing the model measure passes that leads to shots in the next event, also means the model does not give information about all the events afterwards. When using the model, these limitations should be taken into account.
Applying the model
Using the model gave direct expected assist for each player. The numbers are adjusted to per 90. There is a threshold for players with at least 300 minutes.  After normalizing for minutes,  the table show the direct expected assist per 90 (in the table below’ xA_per90’ is used as a shorter term for that). Before signing someone, current Leicester players had to be evaluated. On top left figure are direct xA per 90 for current midfielders at the club. One problem were the different task within the team.  Wilfried Ndidi for example, is playing in central midfield and tasked with performing on other metrics, and as a consequence score low on this metric. Therefore, to create a benchmark, top three midfielders performers on the metric from each club in premier league laid the foundation for an average score per 90 which is equal to 0.026. Leicesters top three performers on this metric gave following list: 
Based on this evaluation, a suggestion would be consider upgrade Mark Albrighton. 
Figure: Calculating benchmark

Possible transfers in
        
Players realistically available considering club, value and reputation is highlighted. Based on the model, signing Lorenzo Insigne is my suggestion. A short-list with three names contains Lorenzo Insigne, Isaac Succes and Dominik Solanke. Karim Bellarabi might be an option, but as he is 30 years of age, I suggest other options. Lorenzo Insigne will cost around 60 m euros, and he will demand a high salary. He will be the most likely to produce most direct-expected assist per 90 from our targets. He also have played a lot of minutes, which makes him a safr option. Isaac Success is a budget option, with great numbers, but low minutes.

Sources 
Maric, R. (2014). The Half-Spaces. https://spielverlagerung.com/2014/09/16/the-half-spaces/
Wyscout, W. (2024). Smart pass. https://dataglossary.wyscout.com/smart_pass/

