import pandas as pd
import numpy as np
from kd_tree import KDTree
from sklearn.neighbors import KNeighborsClassifier

def data_preprocessing(data):
    # Replace 0 values with NaN
    data[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']] = data[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']].replace(0, np.NaN)

    # Replace NaN with median values
    data.loc[(data['Outcome'] == 0 ) & (data['Insulin'].isnull()), 'Insulin'] = 102.5
    data.loc[(data['Outcome'] == 1 ) & (data['Insulin'].isnull()), 'Insulin'] = 169.5

    data.loc[(data['Outcome'] == 0 ) & (data['Glucose'].isnull()), 'Glucose'] = 107
    data.loc[(data['Outcome'] == 1 ) & (data['Glucose'].isnull()), 'Glucose'] = 140

    data.loc[(data['Outcome'] == 0 ) & (data['SkinThickness'].isnull()), 'SkinThickness'] = 27
    data.loc[(data['Outcome'] == 1 ) & (data['SkinThickness'].isnull()), 'SkinThickness'] = 32

    data.loc[(data['Outcome'] == 0 ) & (data['BloodPressure'].isnull()), 'BloodPressure'] = 70
    data.loc[(data['Outcome'] == 1 ) & (data['BloodPressure'].isnull()), 'BloodPressure'] = 74.5

    data.loc[(data['Outcome'] == 0 ) & (data['BMI'].isnull()), 'BMI'] = 30.1
    data.loc[(data['Outcome'] == 1 ) & (data['BMI'].isnull()), 'BMI'] = 34.3

    # Split data into 70% train and 30% test data
    data_arr = data.to_numpy().tolist()
    train_arr, test_arr = data_arr[:int(len(data_arr)*0.7)], data_arr[int(len(data_arr)*0.7):]
    return train_arr, test_arr

def get_kd_tree(train_arr):
    # Create KDTree
    kd_tree = KDTree(train_arr, len(train_arr[0])-1)
    return kd_tree

def kd_tree_own(train_arr, test_arr, neigbours=5):
    # KNN Classifier using own KDTree
    kd_tree = KDTree(train_arr, len(train_arr[0])-1)
    y_pred = []
    y_actual = []
    for data_point in test_arr:
        neighbors = kd_tree.get_knn(data_point, neigbours)
        outcomes = [neighbor[1][-1] for neighbor in neighbors]
        y_pred.append(max(set(outcomes), key=outcomes.count))
        y_actual.append(data_point[-1])

    accuracy_own = sum([1 for i in range(len(y_pred)) if y_pred[i] == y_actual[i]]) / len(y_pred)
    return accuracy_own

def kd_tree_sklearn(train_arr, test_arr, neighbours=5):
    # KNN Classifier using sklearn
    neigh = KNeighborsClassifier(n_neighbors=neighbours)
    neigh.fit([data[:-1] for data in train_arr], [data[-1] for data in train_arr])
    y_pred = neigh.predict([data[:-1] for data in test_arr])
    y_actual = [data[-1] for data in test_arr]
    accuracy_sklearn = sum([1 for i in range(len(y_pred)) if y_pred[i] == y_actual[i]]) / len(y_pred)
    return accuracy_sklearn

if __name__ == "__main__":
    data = pd.read_csv('diabetes.csv')
    train_data, test_data = data_preprocessing(data)
    accuracy_own = kd_tree_own(train_data, test_data)
    accuracy_skl = kd_tree_sklearn(train_data, test_data)

    print ('KNN (own):', accuracy_own)
    print ('KNN (sklearn):', accuracy_skl)