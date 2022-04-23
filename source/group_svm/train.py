#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project:     teambrainiac
# @Filename:    train.py
# @Author:      staceyrivet
# @Time:        4/6/22 7:30 PM
# @IDE:         PyCharm







from access_data import s3_upload
from process import transform_data
from sklearn.svm import SVC
from collections import defaultdict
from analysis import metrics







def run_grp_svm_model(data, mask_type, group_sub_ids, runs_train, runs_val, runs_test, norm, data_type, m_path_ind):
    """

    :param data:
    :param mask_type:
    :param group_sub_ids:
    :param runs_train:
    :param runs_val:
    :param runs_test:
    :param norm:
    :param svm_type:
    :return:
    """
    model_dict = defaultdict(list)

    if runs_val != False:
        X, y, X_v, y_v, X_t, y_t = transform_data(data, group_sub_ids, runs_train, runs_val, runs_test, norm)

        runs_id = [i + 1 for i in runs_train]

        if data_type == "AD_detrend":
            clf = SVC(C=5.0 #10
                      class_weight='balanced',
                      max_iter=1000,
                      random_state=42,
                      probability=True,
                      gamma='scale' #For adolescent
                      )
        else:
            clf = SVC(C=10.0,
                      class_weight='balanced',
                      max_iter=1000,
                      random_state=42,
                      probability = True,
                      gamma = 'auto'
                      )
        print(f"Fitting the model for {mask_type}...")
        clf.fit(X, y)

        model_dict['model'] = clf

        # Calculate metrics
        metrics_data = metrics(clf, X, y, X_v, y_v, X_t, y_t, data_type, runs_id, mask_type, m_path_ind)
    else:
        X, y, X_t, y_t = transform_data(data, group_sub_ids, runs_train, runs_val, runs_test, norm)

        runs_id = [i + 1 for i in runs_train]

        if data_type == "AD_detrend":
            clf = SVC(C=5.0 #10
                      class_weight='balanced',
                      max_iter=1000,
                      random_state=42,
                      probability=True,
                      gamma='scale' #For adolescent
                      )
        else:
            clf = SVC(C=10.0,
                      class_weight='balanced',
                      max_iter=1000,
                      random_state=42,
                      probability=True,
                      gamma = 'auto' # for young adult
                      )
        print(f"Fitting the model for {mask_type} on Train and then will Test...")
        clf.fit(X, y)

        model_dict['model'] = clf

        # Calculate metrics
        metrics_data = metrics(clf, X, y, False, False, X_t, y_t, data_type, runs_id, mask_type, m_path_ind)


    # Return metrics data
    return model_dict, metrics_data