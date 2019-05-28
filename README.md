# NFL_score_predictor
Using statistics from the first half of an NFL game, this model predicts the final score. In the view_of_prediction_success.ipynb, you can see our statistical success and can also be viewed in this screenshot:

Univeristy of San Francisco MSDS: Intro to Machine Learning Project

Authors: Eddie Owens, Darren Thomas, Brian Wright, Tyler Ursuy


### More on model selection:
The Regression Models folder contains notebooks exploring different algorithms including SVM, KNN, Decision Trees, Random Forests, and Linear Regression. SVM and KNN performed significantly worse than Linear Regression and RF, so these were abandoned quickly. DT and RF notebook explores hyperparameter tuning as an attempt to outperform linear regression. We found that it took intense tuning and longer runtimes just to get close to linear regression results. This lead us to choose linear regression using a bagging regressor, which is comparable to a random forest of linear regressions. Linear_Regression.ipynb includes experiments using different datasets and variables. Linear_Regression_Tuning.ipynb includes experiments for variable selection, iterative fitting, grid-searching, and leads to a final model.

![Alt text](images/titans_jags.png?raw=true "Title")
