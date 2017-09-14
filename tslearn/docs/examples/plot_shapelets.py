# -*- coding: utf-8 -*-
"""
Learning Shapelets
==================

This example illustrates the use of the "Learning Shapelets" method for a time series classification task.

More information on the method can be found at: <http://fs.ismll.de/publicspace/LearningShapelets/>.
"""

# Author: Romain Tavenard
# License: BSD 3 clause

import numpy
from sklearn.metrics import accuracy_score
from keras.optimizers import Adagrad

from tslearn.datasets import CachedDatasets
from tslearn.preprocessing import TimeSeriesScalerMinMax
from tslearn.shapelets import ShapeletModel, grabocka_params_to_shapelet_size_dict

numpy.random.seed(0)
X_train, y_train, X_test, y_test = CachedDatasets().load_dataset("Trace")
X_train = TimeSeriesScalerMinMax().fit_transform(X_train)
X_test = TimeSeriesScalerMinMax().fit_transform(X_test)

shapelet_sizes = grabocka_params_to_shapelet_size_dict(ts_sz=X_train.shape[1],
                                                       n_classes=len(set(y_train)),
                                                       l=0.1,
                                                       r=2)


# Nearest neighbor classification
shp_clf = ShapeletModel(n_shapelets_per_size=shapelet_sizes,
                        optimizer=Adagrad(lr=.1),
                        weight_regularizer=.01,
                        verbose_level=0)
shp_clf.fit(X_train, y_train)
predicted_labels = shp_clf.predict(X_test)
print("Correct classification rate:", accuracy_score(y_test, predicted_labels))
