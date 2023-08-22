import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.pipeline import make_pipeline
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor



def main():

    skaters_train = pd.read_csv("training/skaters_train.csv")
    skaters_valid = pd.read_csv("valid/skaters_valid.csv")

    # centres
    c_train = skaters_train.loc[ skaters_train['Pos'] == 'C']
    c_valid = skaters_valid.loc[ skaters_valid['Pos'] == 'C']
    print("\n***** Centres model scores: *****\n")
    pipelines(c_train, c_valid, "C")
    free_agents(c_train, c_valid, "C")
    canucks(c_train, c_valid, "C")
    print("\n")

    # wingers
    w_train = skaters_train.loc[(skaters_train['Pos'] == 'LW') | (skaters_train['Pos'] == 'RW') | (skaters_train['Pos'] == 'F')]
    w_valid = skaters_valid.loc[(skaters_valid['Pos'] == 'LW') | (skaters_valid['Pos'] == 'RW') | (skaters_valid['Pos'] == 'F')]
    print("***** Wingers model scores: *****\n")
    pipelines(w_train, w_valid, "W")
    free_agents(w_train, w_valid, "W")
    canucks(w_train, w_valid, "W")
    print("\n")

    # defencemen
    d_train = skaters_train.loc[ skaters_train['Pos'] == 'D']
    d_valid = skaters_valid.loc[ skaters_valid['Pos'] == 'D']
    print("***** Defencemen model scores: *****\n")
    pipelines(d_train, d_valid, "D")
    free_agents(d_train, d_valid, "D")
    canucks(d_train, d_valid, "D")
    print("\n")




# examining different models 
def pipelines(train, valid, pos): 

    y = (train['CAP_HIT_%'] )
    X = train.drop(['CAP HIT', 'CAP_HIT_%', 'player', 'Pos'], axis=1)

    y_test = (valid['CAP_HIT_%'] )
    y_names = (valid[['player', 'CAP_HIT_%']].copy().reset_index() )
    X_test = valid.drop(['CAP HIT', 'CAP_HIT_%', 'player', 'Pos'], axis=1)


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

    print("Random Forest Model score for the 2022-2023 Season: " + str(rf_model.score(X_test, y_test)))
    print("Gradient Model score for the 2022-2023 Season: " + str(gradient_model.score(X_test, y_test)))
    print("Neural Model score for the 2022-2023 Season: " + str(neural_model.score(X_test, y_test)))
    print("K Neighbor Model score for the 2022-2023 Season: " + str(kn_model.score(X_test, y_test)))
    print("Decision Tree Model score for the 2022-2023 Season: " + str(decision_model.score(X_test, y_test)))

    #The two best models are Random Forest and Gradient Boosting so we will do a voting regressor based on those two
    voting_model = make_pipeline (
        StandardScaler(),
        MinMaxScaler(),
        VotingRegressor([
        ('gb', GradientBoostingRegressor(n_estimators=50,max_depth=2, min_samples_leaf=0.1)),
        ('rf', RandomForestRegressor(30, max_depth=4)),])
    )
    voting_model.fit(X, y)
    print("Voting Model score for the 2022-2023 Season: " + str(voting_model.score(X_test, y_test)))
    
    if (pos == 'C'):
        plt.figure()
        plt.plot(y_names['CAP_HIT_%'], 'b^')
        for i in range(len(y_names)):
            plt.text(i, y_names.loc[i, 'CAP_HIT_%'],y_names.loc[i, 'player'], fontsize=6 )
        plt.plot(voting_model.predict(X_test), "ys")
        plt.title("Predicted and Actual Centre Cap Hit Values for 2022-2023 Season")
        plt.legend(["Actual Cap Hit", "Predicted Cap hit"])
        plt.xlabel("Samples")
        plt.ylabel("Cap Hit Value")
        plt.savefig("centre.png")

    elif (pos == 'W'):
        plt.figure()
        plt.plot(y_names['CAP_HIT_%'], 'b^')
        for i in range(len(y_names)):
            plt.text(i, y_names.loc[i, 'CAP_HIT_%'],y_names.loc[i, 'player'], fontsize=6 )
        plt.plot(voting_model.predict(X_test), "ys")
        plt.title("Predicted and Actual Winger Cap Hit Values for 2022-2023 Season")
        plt.legend(["Actual Cap Hit", "Predicted Cap hit"])
        plt.xlabel("Samples")
        plt.ylabel("Cap Hit Value")
        plt.savefig("winger.png")

    elif (pos == 'D'):
        plt.figure()
        plt.plot(y_names['CAP_HIT_%'], 'b^')
        for i in range(len(y_names)):
            plt.text(i, y_names.loc[i, 'CAP_HIT_%'],y_names.loc[i, 'player'], fontsize=6 )
        plt.plot(voting_model.predict(X_test), "ys")
        plt.title("Predicted and Actual Defencemen Cap Hit Values for 2022-2023 Season")
        plt.legend(["Actual Cap Hit", "Predicted Cap hit"])
        plt.xlabel("Samples")
        plt.ylabel("Cap Hit Value")
        plt.savefig("defence.png")
    
    else:
        return #Goalie


# testing the model

# predicting the salaries for 2022-2023 free agents
def free_agents(train, valid, pos):
    
    salary_cap_2324 = 83500000

    freeAgents = pd.read_csv("raw/free_agents_2023.csv")
    freeAgents.rename(columns={"PLAYER":"player"}, inplace=True)
    freeAgents = freeAgents.drop(['POS.','AGE','TYPE','FROM','TO','YRS','DOLLARS'], axis=1)
    freeAgents['AVERAGE'] = freeAgents['AVERAGE'].str.replace(r'[^\d]', '', regex=True).astype(int)

    canucks = pd.read_csv("raw/canucks2223.csv", encoding='ISO-8859-1')

    train = train.assign(Salary=train['CAP_HIT_%'] * salary_cap_2324)

    X = train.drop(['CAP HIT', 'CAP_HIT_%', 'player', 'Pos', 'Salary'], axis=1)
    y = (train['Salary'] )

    valid = pd.merge(valid, freeAgents, on="player", how="inner")
    valid['Salary'] = valid['AVERAGE']

    X_test = valid.drop(['CAP HIT', 'CAP_HIT_%', 'player', 'Pos', 'Salary', 'AVERAGE'], axis=1)
    y_test = valid['Salary'] 

    y_names = (valid[['player', 'Salary']].copy().reset_index() )

    #The two best models are Random Forest and Gradient Boosting so we will do a voting regressor based on those two
    voting_model = make_pipeline (
        StandardScaler(),
        MinMaxScaler(),
        VotingRegressor([
        ('gb', GradientBoostingRegressor(n_estimators=50,max_depth=2, min_samples_leaf=0.1)),
        ('rf', RandomForestRegressor(30, max_depth=4)),])
    )
    voting_model.fit(X, y)

    
    if (pos == 'C'):

        print("Voting Model score (FA C) for the 2022-2023 Season: " + str(voting_model.score(X_test, y_test)))

        plt.figure()
        plt.plot(y_names['Salary'], 'b^')
        for i in range(len(y_names)):
            plt.text(i, y_names.loc[i, 'Salary'],y_names.loc[i, 'player'], fontsize=6 )
        plt.plot(voting_model.predict(X_test), "ys")
        plt.title("Predicted and Actual Centre Salaries for 2022-2023 Season")
        plt.legend(["Actual Salary", "Predicted Salary"])
        plt.xlabel("Samples")
        plt.ylabel("Salary Value")
        plt.savefig("centre_fa.png")

    elif (pos == 'W'):

        print("Voting Model score (FA W) for the 2022-2023 Season: " + str(voting_model.score(X_test, y_test)))

        plt.figure()
        plt.plot(y_names['Salary'], 'b^')
        for i in range(len(y_names)):
            plt.text(i, y_names.loc[i, 'Salary'],y_names.loc[i, 'player'], fontsize=6 )
        plt.plot(voting_model.predict(X_test), "ys")
        plt.title("Predicted and Actual Winger Salaries for 2022-2023 Season")
        plt.legend(["Actual Salary", "Predicted Salary"])
        plt.xlabel("Samples")
        plt.ylabel("Salary Value")
        plt.savefig("winger_fa.png")

    elif (pos == 'D'):

        print("Voting Model score (FA D) for the 2022-2023 Season: " + str(voting_model.score(X_test, y_test)))

        plt.figure()
        plt.plot(y_names['Salary'], 'b^')
        for i in range(len(y_names)):
            plt.text(i, y_names.loc[i, 'Salary'],y_names.loc[i, 'player'], fontsize=6 )
        plt.plot(voting_model.predict(X_test), "ys")
        plt.title("Predicted and Actual Defence Salaries for 2022-2023 Season")
        plt.legend(["Actual Salary", "Predicted Salary"])
        plt.xlabel("Samples")
        plt.ylabel("Salary Value")
        plt.savefig("defence_fa.png")

    else: 
        return #goalies


# predicting salaries of 2023-2024 (current) Vancouver Canucks based on their performance in 2022-2023
def canucks(train, valid, pos):
    
    salary_cap_2223 = 82500000

    canucks = pd.read_csv("raw/canucks2223.csv", encoding='ISO-8859-1')
    canucks['PLAYER'] = canucks['PLAYER'].str.replace(r'^\d+\. ', '', regex=True)

    train = train.assign(Salary=train['CAP_HIT_%'] * salary_cap_2223)

    X = train.drop(['CAP HIT', 'CAP_HIT_%', 'player', 'Pos', 'Salary'], axis=1)
    y = (train['Salary'] )

    valid = valid[ valid['player'].isin(canucks['PLAYER']) ] 
    valid = valid.assign(Salary=valid['CAP HIT'])

    X_test = valid.drop(['CAP HIT', 'CAP_HIT_%', 'player', 'Pos', 'Salary'], axis=1)
    y_test = valid['Salary'] 

    y_names = (valid[['player', 'Salary']].copy().reset_index() )

    #The two best models are Random Forest and Gradient Boosting so we will do a voting regressor based on those two
    voting_model = make_pipeline (
        StandardScaler(),
        MinMaxScaler(),
        VotingRegressor([
        ('gb', GradientBoostingRegressor(n_estimators=50,max_depth=2, min_samples_leaf=0.1)),
        ('rf', RandomForestRegressor(30, max_depth=4)),])
    )
    voting_model.fit(X, y)

    
    if (pos == 'C'):

        print("Voting Model score (Canucks C) for the 2022-2023 Season: " + str(voting_model.score(X_test, y_test)))

        plt.figure()
        plt.plot(y_names['Salary'], 'b^')
        for i in range(len(y_names)):
            plt.text(i, y_names.loc[i, 'Salary'],y_names.loc[i, 'player'], fontsize=6 )
        plt.plot(voting_model.predict(X_test), "ys")
        plt.title("Predicted and Actual Centre Salaries for 2022-2023 Season")
        plt.legend(["Actual Salary", "Predicted Salary"])
        plt.xlabel("Samples")
        plt.ylabel("Salary Value")
        plt.savefig("centre_van.png")

    elif (pos == 'W'):

        print("Voting Model score (Canucks W) for the 2022-2023 Season: " + str(voting_model.score(X_test, y_test)))

        plt.figure()
        plt.plot(y_names['Salary'], 'b^')
        for i in range(len(y_names)):
            plt.text(i, y_names.loc[i, 'Salary'],y_names.loc[i, 'player'], fontsize=6 )
        plt.plot(voting_model.predict(X_test), "ys")
        plt.title("Predicted and Actual Winger Salaries for 2022-2023 Season")
        plt.legend(["Actual Salary", "Predicted Salary"])
        plt.xlabel("Samples")
        plt.ylabel("Salary Value")
        plt.savefig("winger_van.png")

    elif (pos == 'D'):

        print("Voting Model score (Canucks D) for the 2022-2023 Season: " + str(voting_model.score(X_test, y_test)))

        plt.figure()
        plt.plot(y_names['Salary'], 'b^')
        for i in range(len(y_names)):
            plt.text(i, y_names.loc[i, 'Salary'],y_names.loc[i, 'player'], fontsize=6 )
        plt.plot(voting_model.predict(X_test), "ys")
        plt.title("Predicted and Actual Defence Salaries for 2022-2023 Season")
        plt.legend(["Actual Salary", "Predicted Salary"])
        plt.xlabel("Samples")
        plt.ylabel("Salary Value")
        plt.savefig("defence_van.png")

    else: 
        return #goalies



if __name__ == '__main__':
    main()