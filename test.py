import csv
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

test_dataset_file_name = "test_dataset.csv"
model = load_model("model.keras")

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

with open('max_sequence_length.txt', 'r') as f:
    max_sequence_length = int(f.read())

def predict(input_text_1, input_text_2):
    input_text = input_text_1 + " " + input_text_2
    input_sequence = tokenizer.texts_to_sequences([input_text])
    padded_sequence = pad_sequences(input_sequence, padding='post', maxlen=max_sequence_length)
    prediction = model.predict(padded_sequence, verbose=0)
    return prediction[0, 0]

test_data = []
with open(test_dataset_file_name, 'r', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='\\')
    for row in spamreader:
        test_data.append((row[0], row[1], row[2] == "1"))

results = []
for input_text_1, input_text_2, expected_result in test_data:
    prediction = round(predict(input_text_1, input_text_2) * 100)
    prediction_bool = prediction >= 50
    if expected_result == True:
        expected_result_shown = ">=50%"
    else:
        expected_result_shown = " <50%"
    
    input_text_1_shown = ("'" + input_text_1 + "'").ljust(57)
    input_text_2_shown = ("'" + input_text_2 + "'").ljust(57)
    prediction_shown = str(prediction).ljust(3)
    if prediction_bool == expected_result:
        results.append(True)
        print(f"{input_text_1_shown} & {input_text_2_shown} => Prediction: {prediction_shown}% (expected: {expected_result_shown}) => \033[1;32mCorrect\033[0m")
    else:
        results.append(False)
        print(f"{input_text_1_shown} & {input_text_2_shown} => Prediction: {prediction_shown}% (expected: {expected_result_shown}) => \033[1;31mIncorrect\033[0m")

accuracy = np.mean(results)
print(f"Accuracy: \033[1m{accuracy * 100:.2f}%\033[0m")
