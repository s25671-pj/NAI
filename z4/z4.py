"""
Ponizszy kod zawiera implementację drzewa decyzyjnego i SVM do klasyfikacji danych.
Wykonane przez: Michał Krokoszyński i Dawid Nowakowski

__
----INSTALACJA NIEZBĘDNYCH BIBLIOTEK----
__
W terminalu wykonaj:
1.1. pip install pandas
1.2. pip install scikit-learn
1.3. pip install matplotlib
1.4. pip install seaborn
2. Przejdź w terminalu do katalogu zawierającego TEN plik
3. Wykonaj: python z4.py *

* z4.py = nazwa TEGO pliku


"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns


def load_scale_provided_data(path, sep):
    """
    Wczytuje dane z pliku i wykonuje skalar wartości.
    Zwraca przeskalowane wartości atrybutów oraz klasyfikację/status.

    path - ścieżka do pliku z danymi
    sep - rodzaj separatora w pliku z danymi

    """
    data = pd.read_csv(path, sep=sep)
    x = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    scalar = StandardScaler()
    x_scal = scalar.fit_transform(x)
    return x_scal, y


def learn_classification(x, y, dataset):
    """
    Uczy i wartościuje klasyfikacje (drzewo decyzyjne i SVM) na danych.

        x - wartości atrybutów
        y - status/ranga
        dataset - nazwa zbioru danych
    """
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.6, random_state=33)

    classifiers = {
        "Decision Tree": DecisionTreeClassifier(random_state=33),
        "SVM": SVC(kernel='linear', random_state=33)
    }

    for name, clf in classifiers.items():
        clf.fit(x_train, y_train)
        y_pred = clf.predict(x_test)
        print(f"\n{dataset} - {name} Classification:")
        print(classification_report(y_test, y_pred))

def visualize_data(x, y, col1, col2, columns_names, dataset_name):
    """
    Wizualizuje dane na wykres.

    x - wartości atrybutów
    y - status/ranga
    col1 - pierwsza os wykresu
    col2 - druga os wykresu
    columns_names - lista zawierajaca nazwy kolumn
    dataset_name - nazwa zbioru danych
    """
    df = pd.DataFrame({
        columns_names[col1]: x[:, col1],
        columns_names[col2]: x[:, col2],
        "Class": y
    })

    plt.figure(figsize=(10, 8))
    scatter_plot = sns.scatterplot(
        data=df, 
        x=columns_names[col1], 
        y=columns_names[col2], 
        hue="Class", 
        palette="tab10", 
        alpha=0.7
    )
    scatter_plot.set_title(f"{dataset_name} Visualization")
    scatter_plot.set_xlabel(columns_names[col1])
    scatter_plot.set_ylabel(columns_names[col2])
    plt.legend(title="Class", bbox_to_anchor=(1, 1), loc='upper left')
    plt.show()
    

if __name__ == "__main__":
    
    seeds_columns = [
        "Area",
        "Perimeter",
        "Compactness",
        "Length",
        "Width",
        "Asymmetry",
        "GrooveLength"
    ]
    
    mushroom_columns = [
        "cap-diameter",
        "cap-shape",
        "gill-attachment",
        "gill-color",
        "stem-height",
        "stem-width",
        "stem-color",
        "season"
    ]

    print("Klasyfikacja jakości nasiona")
    x_seeds, y_seeds = load_scale_provided_data("seeds_dataset.txt", r'\s+')
    learn_classification(x_seeds, y_seeds, "Seeds Dataset")
    visualize_data(x_seeds, y_seeds, 0, 3, seeds_columns, "Seeds Dataset")
    
    print("Klasyfikacja grzyba czy jest trujący")
    x_mushroom, y_mushroom = load_scale_provided_data("mushroom.csv", ',')
    learn_classification(x_mushroom, y_mushroom, "Mushroom Dataset")
    visualize_data(x_mushroom, y_mushroom, 0, 4, mushroom_columns, "Mushroom Dataset")
    

