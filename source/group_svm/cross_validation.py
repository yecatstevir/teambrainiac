#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project:     teambrainiac
# @Filename:    cross_validation.py
# @Author:      staceyrivet
# @Time:        3/30/22 10:49 PM
# @IDE:         PyCharm






from sklearn.svm import SVC
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import TimeSeriesSplit, HalvingGridSearchCV
from sklearn.exceptions import ConvergenceWarning
import warnings
import tqdm
from access_data import s3_upload
from collections import defaultdict






def time_series_cv(X, y, max_train, test_size, splits, gd_srch, param_dict, file_name):

    """
    :param X            : nd.array shape (time points, 237979)
    :param y            : nd.array shape (time points, )
    :param max_train    : (int) max size to allow training set for splits
    :param test_size    : (int) max size to allow test split
    :param splits       : (int) number of times to split for cross validation
    :param gd_srch      : (bool) perform grid search or not
    :param param_dict   : Dictionary of Parameters to pass to grid search, otherwise False
    :param file_name    : (string) path to save metric data gathered from gridsearch
    :return             : prints accuracy scores and mean accuracy score over all cross validation runs
    """

    tscv = TimeSeriesSplit(
        max_train_size=max_train,
        n_splits=splits,
        test_size=test_size
    )
    accuracy_ = []
    it = 0

    if gd_srch == True:
        grid_dict = defaultdict(list)
        with warnings.catch_warnings():
            warnings.simplefilter(
                "ignore",
                category=ConvergenceWarning
            )
            clf = SVC(
                random_state = 42,
                class_weight = 'balanced'
            )

            param_search = param_dict
            grid = HalvingGridSearchCV(
                estimator= clf,
                cv = tscv,
                param_grid = param_search
            )
            # Fit data to grid
            grid.fit(X, y)
            print("Uploading gridsearch results to cloud...")
            grid_dict['grid_search'].append(grid.cv_results_)

            #Upload to S3
            s3_upload(grid_dict, file_name, 'pickle')
            print("Best parameters: ", grid.best_params_)
            print('Best estimator: ', grid.best_estimator_)
            print("Best score: ", grid.best_score_)
            print("CV results: ", grid.cv_results_)

    else:

        for train_index, test_index in tqdm.tqdm(tscv.split(X)):
            it += 1
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

            with warnings.catch_warnings():
                warnings.simplefilter(
                    "ignore",
                    category=ConvergenceWarning
                )
                clf = SVC(
                    C=5.0,
                    class_weight='balanced',
                    max_iter=1000,
                    random_state=42
                )
                print(f"Fitting Classifier for iteration number {it}")
                clf.fit(X_train, y_train)

            print("Predicting...")
            y_pred = clf.predict(X_test)

            # Model Accuracy
            score = accuracy_score(y_test, y_pred)
            print(f"Cross Validation Split {it} Accuracy score:", score)
            accuracy_.append(score)

        print("Mean Accuracy: {}".format(np.mean(accuracy_)))
