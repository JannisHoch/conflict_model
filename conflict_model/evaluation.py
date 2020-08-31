import os, sys
from sklearn import metrics
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

def evaluate_prediction(y_test, y_pred, y_prob, X_test, clf, out_dir):
    """[summary]

    Args:
        y_test ([type]): [description]
        y_pred ([type]): [description]
        y_prob ([type]): [description]
    """    

    print("Accuracy: {0:0.3f}".format(metrics.accuracy_score(y_test, y_pred)))
    print("Precision: {0:0.3f}".format(metrics.precision_score(y_test, y_pred)))
    print("Recall: {0:0.3f}".format(metrics.recall_score(y_test, y_pred)))
    print('F1 score: {0:0.3f}'.format(metrics.f1_score(y_test, y_pred)))
    print('Brier loss score: {0:0.3f}'.format(metrics.brier_score_loss(y_test, y_prob[:, 1])))
    print('Cohen-Kappa score: {0:0.3f}'.format(metrics.cohen_kappa_score(y_test, y_pred)))
    print('')

    print(metrics.classification_report(y_test, y_pred))
    print('')

    fig, ax = plt.subplots(1, 1, figsize=(20,10))
    disp = metrics.plot_precision_recall_curve(clf, X_test, y_test, ax=ax)
    plt.savefig(os.path.join(out_dir, 'precision_recall_curve.png'), dpi=300)
    plt.close()
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 7))
    metrics.plot_confusion_matrix(clf, X_test, y_test, ax=ax)
    plt.savefig(os.path.join(out_dir, 'confusion_matrix.png'), dpi=300)
    plt.close()

    fig, ax = plt.subplots(1, 1, figsize=(20,10))
    metrics.plot_roc_curve(clf, X_test, y_test, ax=ax)
    plt.savefig(os.path.join(out_dir, 'ROC_curve.png'), dpi=300)               
    plt.close()

def get_average_hit(df, global_df):

    ID_count = df.ID.value_counts().to_frame().rename(columns={'ID':'ID_count'})
    ID_count['ID'] = ID_count.index.values
    ID_count.set_index(ID_count.ID, inplace=True)
    ID_count = ID_count.drop('ID', axis=1)

    hit_count = df.overall_hit.groupby(df.ID).sum().to_frame().rename(columns={'overall_hit':'total_hits'})

    df_temp = pd.merge(ID_count, hit_count, on='ID')

    df_temp['average_hit'] = df_temp.total_hits / df_temp.ID_count

    df_hit = pd.merge(df_temp, global_df, on='ID', how='left')

    gdf_hit = gpd.GeoDataFrame(df_hit, geometry=df_hit.geometry)

    return df_hit, gdf_hit