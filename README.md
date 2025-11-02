# Tehran House Price Prediction Web App

A **Django** web app that predicts house prices based on features like area, room count, parking availability, and address.

## Tech Stack

**Backend:** Django  
**ML:** scikit-learn, pandas, joblib  
**Frontend:** HTML, CSS, JavaScript (+Tom Select)

## Work Report

I tested **CatBoost**, **XGBoost**, **LinearRegression** and **RandomForest**.  
The MAE was similar in all models, but the R2 was worse in the CatBoost (~0.6) compared to the other three models (~0.9).
The MAE though was quite high for all models I tried and no matter how much I tried to lower that I wasn't successful.  
It's either me whose knowledge is lacking or the data that's limiting.  
I suspect that the answer is the data, because it has problems that I will list them below:

- Small dataset size
- Low feature diversity
- 192 distinct addresses (~18 houses per address on average, which makes it quite hard for the model to learn, given that the address is the most important feature when it comes to houses in Tehran)
- Imbalance in warehouse and elevator features (they are mostly 0)
  A funny thing that also happened was that not having elevator makes the house cost more, because the houses that don't have elevator are most likely a detached house which cost more.

Anyway, I used **RandomForest** as the final model because it performed slightly better and also because I like it better.  
But there is also an inevitable problem with RandomForest, which is that beyond the training data, it cannot extrapolate. So when you pass unusual data (like an area of 1000m²) that it hasn't seen in the training data, it cannot give a plausible estimation. That's because it's a tree-based model and doesn't create a weighted formula for everything like linear regression does. The best solution would be to make a hybrid model that can switch between RandomForest and another model that doesn't have this problem of extrapolation, which I didn’t do since I didn’t find it necessary for this purpose.
