import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.pipeline import make_pipeline
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor




#Given the stats for the past 4 seasons, try and predict the caphit % for the 2022-2023 season of eligible goalies
def main():
    
    goalies_train = pd.read_csv("training/goalies_train.csv")
    goalies_valid = pd.read_csv("valid/goalies_valid.csv")


    y = (goalies_train['CAP_HIT_%'] )
    X = goalies_train.drop(['CAP_HIT_%', 'player'], axis=1)

    yTest = (goalies_valid['CAP_HIT_%'] )
    yNames = (goalies_valid[['player', 'CAP_HIT_%']].copy() )
    XTest = goalies_valid.drop(['CAP_HIT_%', 'player'], axis=1)

    rf_model = make_pipeline(
        StandardScaler(),   
        MinMaxScaler(),
        RandomForestRegressor(100, max_depth=8)
    )
    rf_model.fit(X, y)

    gradient_model = make_pipeline(
        StandardScaler(),
        MinMaxScaler(),
        GradientBoostingRegressor(n_estimators=50,max_depth=2, min_samples_leaf=0.1)
    )
    gradient_model.fit(X, y)

    neural_model = make_pipeline(
        StandardScaler(),
        MinMaxScaler(),
        MLPRegressor(hidden_layer_sizes=(10, 10),activation='logistic', solver='lbfgs')
    )
    neural_model.fit(X, y)

    kn_model = make_pipeline(
        StandardScaler(),
        MinMaxScaler(),
        KNeighborsRegressor(5)
    )
    kn_model.fit(X, y)

    decision_model = make_pipeline(
        StandardScaler(),
        MinMaxScaler(),
        DecisionTreeRegressor(max_depth=30)
    )
    decision_model.fit(X, y)

    print("Random Forest Model score for the 2022-2023 Season: " + str(rf_model.score(XTest, yTest)))
    print("Gradient Model score for the 2022-2023 Season: " + str(gradient_model.score(XTest, yTest)))
    print("Neural Model score for the 2022-2023 Season: " + str(neural_model.score(XTest, yTest)))
    print("K Neighbor Model score for the 2022-2023 Season: " + str(kn_model.score(XTest, yTest)))
    print("Decision Tree Model score for the 2022-2023 Season: " + str(decision_model.score(XTest, yTest)))

    #The two best models are Random Forest and Gradient Boosting so we will do a voting regressor based on those two

    voting_model = make_pipeline (
        StandardScaler(),
        MinMaxScaler(),
        VotingRegressor([
        ('gb', GradientBoostingRegressor(n_estimators=50,max_depth=2, min_samples_leaf=0.1)),
        ('rf', RandomForestRegressor(30, max_depth=4)),])
    )
    
    voting_model.fit(X, y)
    print("Voting Model score for the 2022-2023 Season: " + str(voting_model.score(XTest, yTest)))

    plt.figure()
    plt.plot(yTest, 'b^')
    for i in range(len(yNames)):
        plt.text(i, yNames.loc[i, 'CAP_HIT_%'],yNames.loc[i, 'player'], fontsize=6 )
    plt.plot(voting_model.predict(XTest), "ys")
    plt.title("Predicted and Actual Goalie Cap Hit Values for 2022-2023 Season")
    plt.legend(["Actual Cap Hit", "Predicted Cap hit"])
    plt.xlabel("Samples")
    plt.ylabel("Cap Hit Value")
    plt.savefig('goalie.png')



    compareSalary(goalies_train, goalies_valid)



def compareSalary(train, valid):

    salaryCap2223 = 82500000

    freeAgents = pd.read_csv("raw/free_agents_2023.csv")
    freeAgents.rename(columns={"PLAYER":"player"}, inplace=True)
    freeAgents = freeAgents.drop(['POS.','AGE','TYPE','FROM','TO','YRS','DOLLARS'], axis=1)
    freeAgents['AVERAGE'] = freeAgents['AVERAGE'].str.replace(r'[^\d]', '', regex=True).astype(int)

    train['Salary'] = (train['CAP_HIT_%'] * salaryCap2223)

    X = train.drop(['CAP HIT', 'CAP_HIT_%', 'player', 'Salary'], axis=1)
    y = (train['Salary'] )

    valid = pd.merge(valid, freeAgents, on="player", how="inner")
    valid['Salary'] = valid['AVERAGE']

    XTest = valid.drop(['CAP HIT', 'CAP_HIT_%', 'player', 'Salary', 'AVERAGE'], axis=1)
    yTest = valid['Salary'] 

    yNames = (valid[['player', 'Salary']].copy().reset_index() )


    #The two best models are Random Forest and Gradient Boosting so we will do a voting regressor based on those two
    voting_model = make_pipeline (
        StandardScaler(),
        MinMaxScaler(),
        VotingRegressor([
        ('gb', GradientBoostingRegressor(n_estimators=50,max_depth=2, min_samples_leaf=0.1)),
        ('rf', RandomForestRegressor(30, max_depth=4)),])
    )
    voting_model.fit(X, y)

    print("Voting Model score (FA) for the 2022-2023 Season: " + str(voting_model.score(XTest, yTest)))
    
    plt.figure()
    plt.plot(yNames['Salary'], 'b^')
    for i in range(len(yNames)):
        plt.text(i, yNames.loc[i, 'Salary'],yNames.loc[i, 'player'], fontsize=6 )
    plt.plot(voting_model.predict(XTest), "ys")
    plt.title("Predicted and Actual Salaries for 2022-2023 Season")
    plt.legend(["Actual Salary", "Predicted Salary"])
    plt.xlabel("Samples")
    plt.ylabel("Salary Value")
    plt.legend
    plt.savefig("goalie_fa.png")



if __name__ == '__main__':
    main()