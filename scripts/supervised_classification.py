# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      supervised_classification.py                       ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: Branly, Tran Quoc <->                          ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://github.com/StephaneBranly              +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2022/05/31 18:39:04 by Branly, Tran Quoc   ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

from .utils import *

import numpy as np
import category_encoders as ce
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn import preprocessing

from sklearn.model_selection import cross_val_score

from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier


def split_train_test(data, test_ratio):
    np.random.seed(42)
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]


def separate_features_target(data, type_target):
    X_cols = []
    for col in data.columns:
        if col != type_target:
            X_cols.append(col)

    return data[X_cols], data[type_target]


def display_scores(scores, model, kernel):
    print(
        f"Mean accuracy of {model} {kernel} \t: {couleurs.KO}{round(scores.mean(), 3)}{couleurs.FIN} \t Standard deviation : {couleurs.ATTENTION}{round(scores.std(), 3)}{couleurs.FIN}"
    )


def cross_validation(X_train, y_train, model="", kernel="", folds=1, hyperparam=1):

    cv = RepeatedStratifiedKFold(n_splits=folds, n_repeats=3, random_state=1)

    if model == "LDA":
        scores = LDA_cross_validation_accuracy(X_train, y_train, cv)
    elif model == "QDA":
        scores = QDA_cross_validation_accuracy(X_train, y_train, cv)
    elif model == "NB":
        scores = NB_cross_validation_accuracy(X_train, y_train, cv)
    elif model == "KNN":
        scores = KNN_cross_validation_accuracy(X_train, y_train, cv, hyperparam)
    elif model == "RF":
        scores = RF_cross_validation_accuracy(X_train, y_train, cv)
    elif model == "Mutiple_Logistic_reg":
        scores = Mutiple_Logistic_reg_cross_validation_accuracy(X_train, y_train, cv)
    elif model == "Decision_tree":
        scores = Decision_tree_cross_validation_accuracy(X_train, y_train, cv)

    display_scores(scores, model, kernel)
    return scores


def prepare_inputs_oe(X, X_train, X_test, X_val, cols):
    """
        prepare input data
    this function takes the input data for the train and test sets and encodes
    it using an ordinal enconding"""
    oe = ce.OrdinalEncoder(cols=cols)
    oe.fit(X)
    X_train_oe = oe.transform(X_train)
    X_test_oe = oe.transform(X_test)
    X_val_oe = oe.transform(X_val)
    return X_train_oe, X_val_oe, X_test_oe


def prepare_inputs_ohe(X, X_train, X_test, X_val, cols):
    oe = ce.OneHotEncoder(cols=cols)
    oe.fit(X)
    X_train_ohe = oe.transform(X_train)
    X_val_ohe = oe.transform(X_val)
    X_test_ohe = oe.transform(X_test)
    return X_train_ohe, X_val_ohe, X_test_ohe


def prepare_targets(y, y_train, y_val, y_test):
    """The prepare_targets() integer encodes the output data for the train and test sets."""
    le = preprocessing.LabelEncoder()
    le.fit(y)
    y_train_enc = le.transform(y_train)
    y_val_enc = le.transform(y_val)
    y_test_enc = le.transform(y_test)
    return y_train_enc, y_val_enc, y_test_enc


def KNN_cross_validation_accuracy(X_train, y_train, cv, hyperparam):
    model = KNeighborsClassifier(n_neighbors=hyperparam)
    # evaluate model
    scores = cross_val_score(
        model, X_train, y_train, scoring="accuracy", cv=cv, n_jobs=-1
    )
    return scores


def NB_cross_validation_accuracy(X_train, y_train, cv):
    model = GaussianNB()
    # evaluate model
    scores = cross_val_score(
        model, X_train, y_train, scoring="accuracy", cv=cv, n_jobs=-1
    )
    return scores


def Mutiple_Logistic_reg_cross_validation_accuracy(X_train, y_train, cv):
    model = LogisticRegression(multi_class="multinomial", solver="lbfgs")
    # evaluate model
    scores = cross_val_score(
        model, X_train, y_train, scoring="accuracy", cv=cv, n_jobs=-1
    )
    return scores


def Decision_tree_cross_validation_accuracy(X_train, y_train, cv):
    tree_model = DecisionTreeClassifier(criterion="entropy")
    # evaluate model
    scores = cross_val_score(
        tree_model, X_train, y_train, scoring="accuracy", cv=cv, n_jobs=-1
    )

    return scores


def LDA_cross_validation_accuracy(X_train, y_train, cv):
    model = LinearDiscriminantAnalysis()
    # evaluate model
    scores = cross_val_score(
        model,
        X_train,
        y_train,
        scoring="accuracy",
        cv=cv,
        n_jobs=-1,
        error_score="raise",
    )
    return scores


def QDA_cross_validation_accuracy(X_train, y_train, cv):
    model = QuadraticDiscriminantAnalysis()
    # evaluate model
    scores = cross_val_score(
        model,
        X_train,
        y_train,
        scoring="accuracy",
        cv=cv,
        n_jobs=-1,
        error_score="raise",
    )
    return scores


def RF_cross_validation_accuracy(X_train, y_train, cv):
    best_model_RF = RandomForestClassifier(
        n_estimators=1400,
        max_depth=80,
        max_features="sqrt",
        min_samples_leaf=1,
        min_samples_split=5,
        bootstrap=False,
        n_jobs=-1,
    )
    # evaluate model
    scores = cross_val_score(
        best_model_RF, X_train, y_train, scoring="accuracy", cv=cv, n_jobs=-1
    )

    return scores
