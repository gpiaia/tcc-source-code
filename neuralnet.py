from sklearn import linear_model, model_selection, metrics
import pandas as pd

# Carrega os elementos do dataset
dataset = pd.read_csv('Datasets/data_PID.csv')
x = dataset.iloc[:, [5,8]].values
y = dataset.iloc[:, 2].values

# Cria um objeto Perceptron
perceptron = linear_model.Perceptron(tol=1e-3, random_state=0)

# Split em conjunto de treino e teste
x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.2, random_state=0)

# Treinamento
classificador = perceptron.fit(x_train, y_train)

# Validação
y_predict = classificador.predict(x_test)

# Acurácia
print(metrics.accuracy_score(y_test, y_predict))