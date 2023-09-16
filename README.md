# afl_prediction

In this project I train a machine learning model to predict the outcome of AFL matches. 

The project is contained in the Jupyter notebook 'afl.ipynb'.

The outline is as follows:
1. Obtain basic match data using the PyAFL package.
2. Extract a variety of features we want to use to predict match outcomes, such as number of points scored by and against each team and relative performance of each team.
3. Perform a brief data exploration
4. Create a test and training set.
5. Prepare the data for the machine learning models; remove missing values, remove drawed matches, and remove any features that can only be known after a game is played.
6. Implement and test four models using cross validation: random forest, logistic regression, state vector machine, and a simple neural network.
7. Also try some ensemble methods such as voting, bagging, and boosting models.
8. Evaluate the best performing models ont he test set.
9. Launch the model; create an AFL predictor class that is trained on all matches already played.
