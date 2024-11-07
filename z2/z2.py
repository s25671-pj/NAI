"""
Poniższy kod zawiera implementację logiki rozmytej dla systemu odpowiedzialnogo za (automatyczną) zmianę biegów.
Wykonane przez: Michał Krokoszyński i Dawid Nowakowski

Instrukcja przygotowania środowiska 
________________________________________
----------INSTALACJA PYTHON-------------
________________________________________
Windows:
1. Ze strony python.org/downloads pobierz najnowszą wersję Pythona dla systemu Windows.
2. Uruchom instalator, zaznacz "Add Python to PATH".
3. Kliknij "Install Now".

macOS:
0. Jeśli nie posiadasz Homebrew, w terminalu:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
1. Wykonaj w terminalu: brew install python

Linux (Ubuntu/Debian):
W terminalu wpisz:
1. sudo apt update
2. sudo apt install python3 python3-pip
________________________________________
----INSTALACJA NIEZBĘDNYCH BIBLIOTEK----
________________________________________
1. W terminalu wykonaj: 
1.1. pip install numpy
1.2. pip install scikit-fuzzy
1.3. pip install scipy
1.4. pip install networkx
2. Przejdź w terminalu do katalogu zawierającego TEN plik
3. Wykonaj: python z2.py
* z2.py = nazwa TEGO pliku
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def Decission(inputSpeed, inputTorque, inputGear):
    """
    Definiujemy wartości graniczne dla
    wejścia: prędkości momentu obrotowego i obecnego biegu
    wyjścia: zmiana biegu
                    
    speed = prędkość w przedziale <0; 121)
    torque = moment obrotowy w przedziale <0; 8001)
    gear = obecny bieg w przedziale <0; 6)
    shift = zmiana biegu w przedziale <-1;2) decyzja: -1 (niższy), 0 (nie zmieniać), 1 (wyższy)

    Fuzzification - definicja rozmytych zbiorów
	Definiujemy jakie wartości należą należą do jakich kategorii membership function (low, medium, high)
    i dodatkowo wyjścia (down, stay, up)
	    speed['low'], speed['medium'], speed['high']
		torque['low'], torque['medium'], torque['high']
		gear['low'], gear['medium'], gear['high']
		shift['down'], shift['stay'], shift['up']

	rules = tablica wielowymiarowa zawierająca możliwe scenariusze rezultatu wyjścia dla podanych wartości wejściowych
    
    gear_ctrl = tworzenie systemu sterowania
    gear_sim = tworzy obiekt, który jest symulatorem sterowania

	Przekazanie wartości z parametrów funkcji:
    gear_sim.input['speed'] = inputSpeed
    gear_sim.input['torque'] = inputTorque
    gear_sim.input['gear'] = inputGear

    gear_sim.compute() = przeprowadza symulację

    decision = przechowuje output dla przekazanych danych wejściowych
	"""
    speed = ctrl.Antecedent(np.arange(0, 121, 1), 'speed')
    torque = ctrl.Antecedent(np.arange(0, 8001, 1), 'torque')
    gear = ctrl.Antecedent(np.arange(1, 6, 1), 'gear')
    shift = ctrl.Consequent(np.arange(-1, 2.1, 1), 'shift')

    speed['low'] = fuzz.trapmf(speed.universe, [0, 0, 25, 50])
    speed['medium'] = fuzz.trimf(speed.universe, [25, 50, 75])
    speed['high'] = fuzz.trapmf(speed.universe, [50, 75, 120, 120])

    torque['low'] = fuzz.trapmf(torque.universe, [0, 0, 2000, 4000])
    torque['medium'] = fuzz.trimf(torque.universe, [2000, 4000, 6000])
    torque['high'] = fuzz.trapmf(torque.universe, [4000, 6000, 8000, 8000])

    gear['low'] = fuzz.trapmf(gear.universe, [1, 1, 2, 3])
    gear['medium'] = fuzz.trimf(gear.universe, [2, 3, 4])
    gear['high'] = fuzz.trapmf(gear.universe, [3, 4, 5, 5])

    shift['down'] = fuzz.trimf(shift.universe, [-1, -1, 0])
    shift['stay'] = fuzz.trimf(shift.universe, [-1, 0, 1])
    shift['up'] = fuzz.trimf(shift.universe, [0, 1, 1])

    rules = [
        ctrl.Rule(speed['low'] & torque['low'] & gear['low'], shift['stay']),
        ctrl.Rule(speed['low'] & torque['low'] & gear['medium'], shift['down']),
        ctrl.Rule(speed['low'] & torque['low'] & gear['high'], shift['down']),
        
        ctrl.Rule(speed['low'] & torque['medium'] & gear['low'], shift['stay']),
        ctrl.Rule(speed['low'] & torque['medium'] & gear['medium'], shift['down']),
        ctrl.Rule(speed['low'] & torque['medium'] & gear['high'], shift['down']),
        
        ctrl.Rule(speed['low'] & torque['high'] & gear['low'], shift['stay']),
        ctrl.Rule(speed['low'] & torque['high'] & gear['medium'], shift['stay']),
        ctrl.Rule(speed['low'] & torque['high'] & gear['high'], shift['down']),
        
        ctrl.Rule(speed['medium'] & torque['low'] & gear['low'], shift['up']),
        ctrl.Rule(speed['medium'] & torque['low'] & gear['medium'], shift['down']),
        ctrl.Rule(speed['medium'] & torque['low'] & gear['high'], shift['down']),
        
        ctrl.Rule(speed['medium'] & torque['medium'] & gear['low'], shift['up']),
        ctrl.Rule(speed['medium'] & torque['medium'] & gear['medium'], shift['stay']),
        ctrl.Rule(speed['medium'] & torque['medium'] & gear['high'], shift['down']),
        
        ctrl.Rule(speed['medium'] & torque['high'] & gear['low'], shift['up']),
        ctrl.Rule(speed['medium'] & torque['high'] & gear['medium'], shift['up']),
        ctrl.Rule(speed['medium'] & torque['high'] & gear['high'], shift['stay']),
        
        ctrl.Rule(speed['high'] & torque['low'] & gear['low'], shift['up']),
        ctrl.Rule(speed['high'] & torque['low'] & gear['medium'], shift['up']),
        ctrl.Rule(speed['high'] & torque['low'] & gear['high'], shift['stay']),
        
        ctrl.Rule(speed['high'] & torque['medium'] & gear['low'], shift['up']),
        ctrl.Rule(speed['high'] & torque['medium'] & gear['medium'], shift['up']),
        ctrl.Rule(speed['high'] & torque['medium'] & gear['high'], shift['stay']),
        
        ctrl.Rule(speed['high'] & torque['high'] & gear['low'], shift['up']),
        ctrl.Rule(speed['high'] & torque['high'] & gear['medium'], shift['up']),
        ctrl.Rule(speed['high'] & torque['high'] & gear['high'], shift['stay']),
    ]

    gear_ctrl = ctrl.ControlSystem(rules)
    gear_sim = ctrl.ControlSystemSimulation(gear_ctrl)

    gear_sim.input['speed'] = inputSpeed
    gear_sim.input['torque'] = inputTorque
    gear_sim.input['gear'] = inputGear

    gear_sim.compute()

    decision = gear_sim.output['shift']
    print("Decyzja dla ({0}, {1}, {2}) to:".format(inputSpeed, inputTorque, inputGear), decision)

    if decision > 0.5:
        print("Zmień bieg na wyższy.")
    elif decision < -0.5:
        print("Zmień bieg na niższy.")
    else:
        print("Nie zmieniać biegu.")
    print("\n")
        
        
Decission(70, 4000, 3)
Decission(20, 2000, 2)
Decission(20, 2000, 4)
