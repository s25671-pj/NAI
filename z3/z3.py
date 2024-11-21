"""
Ponizszy kod zawiera implementacje (logiki KMeans - algorytm klastrowania) funkcji do rekomendacji i antyrekomendacji na podstawie bazy danych
Wykonane przez: Michał Krokoszyński i Dawid Nowakowski

__
----INSTALACJA NIEZBĘDNYCH BIBLIOTEK----
__
W terminalu wykonaj:
1.1. pip install pandas
1.2. pip install scikit-learn
2. Przejdź w terminalu do katalogu zawierającego TEN plik
3. Wykonaj: python z3.py *
4. Podaj id usera, dla którego chcesz wygenerować rekomendacje i anty-rekomendacje.
* z3.py = nazwa TEGO pliku


"""

import json
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Wczytanie ocen użytkowników z pliku JSON
with open('./movies_db.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Konwersja danych JSON do DataFrame
df = pd.DataFrame(data).transpose()

# Konwersja wszystkich wartości na numeryczne, zastępując nieprawidłowe dane NaN
df = df.apply(pd.to_numeric, errors='coerce')

# Normalizacja ocen użytkowników: odjęcie średniej i podzielenie przez odchylenie standardowe
normalized_df = (df - df.mean(axis=1).values.reshape(-1, 1)) / df.std(axis=1).values.reshape(-1, 1)

# Zastąpienie wartości NaN zerami do celów klastrowania
normalized_df = normalized_df.fillna(0)

# Zastosowanie algorytmu K-Means do podziału użytkowników na 3 klastry
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(normalized_df)

# Dodanie etykiet klastrów do oryginalnego DataFrame
df['Cluster'] = clusters


def generate_recommendations(target_user, df, normalized_df, top_n):
    """
    Generowanie rekomendacji i antyrekomendacji dla danego użytkownika.

    Argumenty funkcji:
        - target_user: Użytkownik, dla którego generowane są rekomendacje.
        - df: Wejciowy DataFrame z ocenami.
        - normalized_df: Znormalizowany DataFrame używany do klastrowania.

    Wynik działania funcji:
        - recommendations: Top N polecanych filmów.
        - anti_recommendations: Top N niepolecanych filmów.
    """
    # Pobranie klastra użytkownika
    user_cluster = df.loc[target_user, 'Cluster']

    # Pobranie użytkowników z tego samego klastra
    cluster_users = df[df['Cluster'] == user_cluster].index

    # Obliczenie średnich ocen filmów w klastrze
    cluster_ratings = df.loc[cluster_users].drop(columns=['Cluster']).mean(axis=0)

    # Pobranie filmów już ocenionych przez użytkownika
    rated_movies = df.loc[target_user].drop(labels=['Cluster']).dropna().index

    # Wykluczenie filmów już ocenionych przez użytkownika
    cluster_ratings = cluster_ratings.drop(rated_movies, errors='ignore')

    # Sortowanie filmów według średnich ocen dla rekomendacji i antyrekomendacji
    recommendations = cluster_ratings.sort_values(ascending=False).head(top_n)
    anti_recommendations = cluster_ratings.sort_values(ascending=True).head(top_n)

    return recommendations.index.tolist(), anti_recommendations.index.tolist()


# Wyświetlanie listy użytkowników z numeracją
users = list(df.index)
print("Dostępni użytkownicy:")
for idx, user in enumerate(users, start=1):
    print(f"{idx}. {user}")

# Wybór użytkownika na podstawie podanego numeru
try:
    selection = int(input("Wybierz numer użytkownika, dla którego chcesz wygenerować rekomendacje: ").strip()) - 1
    if selection < 0 or selection >= len(users):
        raise ValueError("Nieprawidłowy numer użytkownika.")
    target_user = users[selection]
except ValueError as e:
    print(f"Błąd: {e}. Spróbuj ponownie.")
else:
    # Generowanie rekomendacji dla wybranego użytkownika
    recommendations, anti_recommendations = generate_recommendations(target_user, df, normalized_df, 5)
    print(f"\nRekomendacje: {recommendations}")
    print(f"Antyrekomendacje: {anti_recommendations}")

