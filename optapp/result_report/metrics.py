from math import sqrt

import numpy as np


from sklearn import metrics as skmetrics

def multiclass_recall(y_true, y_pred):
    """
    Calculate the recall metric.

    Classification metric.

    The recall is the ratio ``tp / (tp + fn)`` where ``tp`` is the number of
    true positives and ``fn`` the number of false negatives. The recall is
    intuitively the ability of the classifier to find all the positive samples.

    Parameters
    ----------
    y_true: array-like of shape = (n_samples) or (n_samples, n_outputs)
        True labels comming from the evaluation set
    y_pred: array-like of shape = (n_samples) or (n_samples, n_outputs)
        Labels predicted by your model
    
    Returns
    -------
    array like float
        In case of binary classification returns the recall. 
        In multiclass classification returns the recall for each class
    """
    return skmetrics.recall_score(y_true, y_pred, average=None)

def multiclass_precision(y_true, y_pred):
    """
    Calculate the precision metric.

    Classification metric.

    The precision is the ratio ``tp / (tp + fp)`` where tp is the number of true 
    positives and fp the number of false positives. 
    The precision is intuitively the ability of the classifier not to label as 
    positive a sample that is negative.

    Parameters
    ----------
    y_true: array-like of shape = (n_samples) or (n_samples, n_outputs)
        True labels comming from the evaluation set
    y_pred: array-like of shape = (n_samples) or (n_samples, n_outputs)
        Labels predicted by your model
    
    Returns
    -------
    array like float
        In case of binary classification returns the precision. 
        In multiclass classification returns the precision of each class.
    """
    return skmetrics.precision_score(y_true, y_pred, average=None)


def multiclass_f1(y_true, y_pred):
    """
    Compute the F1 score, also known as balanced F-score or F-measure.

    Classification metric.

    The F1 score can be interpreted as a weighted average of the precision and
    recall, where an F1 score reaches its best value at 1 and worst score at 0.
    The relative contribution of precision and recall to the F1 score are
    equal. The formula for the F1 score is::

        F1 = 2 * (precision * recall) / (precision + recall)

    In the multi-class and multi-label case, this is the average of
    the F1 score of each class.

    Parameters
    ----------
    y_true: array-like of shape = (n_samples) or (n_samples, n_outputs)
        True labels comming from the evaluation set
    y_pred: array-like of shape = (n_samples) or (n_samples, n_outputs)
        Labels predicted by your model
    
    Returns
    -------
    list of float
        F1 score of each class
    """
    return skmetrics.f1_score(y_true, y_pred, average=None)

def recall(y_true, y_pred):
    """
    Calculate the recall metric.

    Classification metric.

    The recall is the ratio ``tp / (tp + fn)`` where ``tp`` is the number of
    true positives and ``fn`` the number of false negatives. The recall is
    intuitively the ability of the classifier to find all the positive samples.

    Parameters
    ----------
    y_true: array-like of shape = (n_samples) or (n_samples, n_outputs)
        True labels comming from the evaluation set
    y_pred: array-like of shape = (n_samples) or (n_samples, n_outputs)
        Labels predicted by your model
    
    Returns
    -------
    float
        In case of binary classification returns the recall. 
        In multiclass classification return the mean of all recalls
    """
    cm = skmetrics.confusion_matrix(y_true, y_pred)
    diag = np.diag(cm)
    sum_ = np.sum(cm, axis=1)
    recall = np.ones((len(diag)))
    np.divide(diag, sum_, out=recall, where=sum_!=0)
    return float(np.mean(recall))


def accuracy(y_true, y_pred):
    """
    Calculate the accuracy metric.

    Classification metric.

    In multilabel classification, this function computes subset accuracy: the set of labels predicted for a sample must exactly match the corresponding set of labels in y_true.

    Parameters
    ----------
    y_true: array-like of shape = (n_samples) or (n_samples, n_outputs)
        True labels comming from the evaluation set
    y_pred: array-like of shape = (n_samples) or (n_samples, n_outputs)
        Labels predicted by your model
    
    Returns
    -------
    float
        return the fraction of correctly classified samples
        The best performance is 1
    """
    return skmetrics.accuracy_score(y_true, y_pred)
    
def precision(y_true, y_pred):
    """
    Calculate the precision metric.

    Classification metric.

    The precision is the ratio ``tp / (tp + fp)`` where tp is the number of true 
    positives and fp the number of false positives. 
    The precision is intuitively the ability of the classifier not to label as 
    positive a sample that is negative.

    Parameters
    ----------
    y_true: array-like of shape = (n_samples) or (n_samples, n_outputs)
        True labels comming from the evaluation set
    y_pred: array-like of shape = (n_samples) or (n_samples, n_outputs)
        Labels predicted by your model
    
    Returns
    -------
    float
        In case of binary classification returns the precision. 
        In multiclass classification return the mean of all precisions.
    """
    cm = skmetrics.confusion_matrix(y_true, y_pred)
    diag = np.diag(cm)
    sum_ = np.sum(cm, axis=0)
    precision = np.ones((len(diag)))
    np.divide(diag, sum_, out=precision, where=sum_!=0)
    return float(np.mean(precision))


def f1(y_true, y_pred):
    """
    Compute the F1 score, also known as balanced F-score or F-measure.

    Classification metric.

    The F1 score can be interpreted as a weighted average of the precision and
    recall, where an F1 score reaches its best value at 1 and worst score at 0.
    The relative contribution of precision and recall to the F1 score are
    equal. The formula for the F1 score is::

        F1 = 2 * (precision * recall) / (precision + recall)

    In the multi-class and multi-label case, this is the average of
    the F1 score of each class.

    Parameters
    ----------
    y_true: array-like of shape = (n_samples) or (n_samples, n_outputs)
        True labels comming from the evaluation set
    y_pred: array-like of shape = (n_samples) or (n_samples, n_outputs)
        Labels predicted by your model
    
    Returns
    -------
    float
        F1 score
    """
    recall_ = recall(y_true, y_pred)
    precision_ = precision(y_true, y_pred)
    return 2 * (precision_ * recall_) / (precision_ + recall_)

def mae(y_true, y_pred):
    """
    Mean absolute error regression loss.

    Parameters
    ----------
    y_true: array-like of shape = (n_samples) or (n_samples, n_outputs)
        True labels comming from the evaluation set
    y_pred: array-like of shape = (n_samples) or (n_samples, n_outputs)
        Labels predicted by your model
    
    Returns
    -------
    float
        average of all predictions errors.
        MAE output is non-negative floating point. The best value is 0.0. 
    """
    return skmetrics.mean_absolute_error(y_true, y_pred)

def mse(y_true, y_pred):
    """
    Mean squared error regression loss


    Parameters
    ----------
    y_true: array-like of shape = (n_samples) or (n_samples, n_outputs)
        True labels comming from the evaluation set
    y_pred: array-like of shape = (n_samples) or (n_samples, n_outputs)
        Labels predicted by your model
    
    Returns
    -------
    float
        A non-negative floating point value (the best value is 0.0) 
    """
    return skmetrics.mean_squared_error(y_true, y_pred)

def rmse(y_true, y_pred):
    """
    Root Mean squared error regression loss

    Parameters
    ----------
    y_true: array-like of shape = (n_samples) or (n_samples, n_outputs)
        True labels comming from the evaluation set
    y_pred: array-like of shape = (n_samples) or (n_samples, n_outputs)
        Labels predicted by your model
    
    Returns
    -------
    float
        A non-negative floating point value (the best value is 0.0) 
    """
    return sqrt(skmetrics.mean_squared_error(y_true, y_pred))

str_to_metric_fn = {
    'recall': recall,
    'precision': precision,
    'f1': f1,
    'mae': mae,
    'mse': mse,
    'rmse': rmse,
    'multiclass_recall': multiclass_recall,
    'multiclass_precision': multiclass_precision,
    'multiclass_f1': multiclass_f1,
    'accuracy': accuracy,
    'acc': accuracy
} 