# NFL Final Score Predictor: What Can the 1st Half tell us about the final score?
Using statistics from the first half of an NFL game, this model predicts the final score of an NFL game. The two use cases are 1) to predict the winner of the game at halftime and 2) to place a bet at halftime against the halftime spread. Both use data trained from 1,341 historical games with mulitple features (see below) 

##### Univeristy of San Francisco MSDS: Intro to Machine Learning Project

##### Authors: Eddie Owens, Darren Thomas, Brian Wright, Tyler Ursuy

### Datasets:
Play-by-play data from 2009-2016:
https://www.kaggle.com/maxhorowitz/nflplaybyplay2009to2016#NFL%20Play%20by%20Play%202009-2017%20(v4).csv

NFL Betting Data:
https://www.kaggle.com/tobycrabtree/nfl-scores-and-betting-data#spreadspoke_scores.csv

### Model Selection
The ml_models folder contains notebooks exploring SVM, KNN, Decision Trees, Random Forests, and Linear Regression. Linear Regression and Random Forrest performed significantly better than SVM and KNN and therefore the notebookes have a deeper exploration of hyperparameter tuning. Our best model was a **bagging regressor**, which can be thought of as a random forest of linear regressions. `br_final_model_with_metrics.ipynb` includes experiements for variable selection, iterative fitting, and grid-searching which ultimately lead to the final model.

![Alt text](images/RMSE.png?raw=true "Title")
![Alt text](images/r_squared.png?raw=true "Title")

### Preprocessing Data:
Ran compile_data.py in terminal with 2 command line inputs: filepath to play by play data and filepath to spread data (e.g. python compile_data.py nfl.csv nflspread.csv) to generate nfl_cleaned.csv (in data folder)
*profootballreference.com was also scarped to ensure accuracte statistics (in data folder). 1,341 games matched and used for modeling.

### Features:
![Alt text](images/yppa.png?raw=true "Title")
![Alt text](images/ypra.png?raw=true "Title")

As evidenced by the two graphs above, total points scored by a team and yards per pass attempt have more of a linear relationship than yards per rush attempt. After calculating the p-values of every feature, yards lost due to a sack and fumble percentage were dropped from the model (p-values of .227 and .578 respectively, in images folder).

The following features remain:
Pregame features:
- Predicted scores (based on spread and over/under)

Halftime features:
- Score for each team
- Number of pass attempts
- Yards per pass attempt
- Completion percentage
- Rushing attempts
- Yards per rush
- Interception percentage
- Sack percentage
- Yards lost per sack
- Fumble percentage

### Confusion Matrix and Success Predicting Winner and Loser
In the view_of_prediction_success.ipynb, you can see our statistical success. This is a screenshot of a confusion matrix from the notebook

### Model results on week 15 Jaguars at Titans on December 6th, 2018:
![Alt text](images/titans_jags.png?raw=true "Title")

Code be found in TNF_prediction_12.6.18.ipynb. 

**To experiement with the halftime statistics on your own, use enter_statistics_and_place_bet.ipynb**

*Note: This model has a small sample size, but has correctly beaten the spread predictions 6 times in 8 samples*

