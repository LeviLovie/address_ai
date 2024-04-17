import csv
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

dataset_file_name = "dataset.csv"
model_file_name = "model.keras"
epochs = 100

data = []
data_not_tuples = []
with open(dataset_file_name, 'r', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='\\')
    for row in spamreader:
        data.append((row[0], row[1], int(row[2])))
        data_not_tuples.append(row[0])
        data_not_tuples.append(row[1])

X_text = [x1 + x2 for x1, x2, _ in data]
Y = np.array([label for _, _, label in data])

tokenizer = Tokenizer(char_level=True)
tokenizer.fit_on_texts(data_not_tuples)
max_sequence_length = max([len(x) for x in X_text])
with open('max_sequence_length.txt', 'w') as f:
    f.write(str(max_sequence_length))
print(f"Max sequence length: {max_sequence_length}")

X_indices = tokenizer.texts_to_sequences(X_text)
X_indices = pad_sequences(X_indices, padding='post', maxlen=max_sequence_length)

vocab_size = len(tokenizer.word_index) + 1

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, 32),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

class ThresholdCallback(tf.keras.callbacks.Callback):
    def __init__(self, threshold):
        super(ThresholdCallback, self).__init__()
        self.threshold = threshold

    def on_epoch_end(self, epoch, logs=None):
        val_acc = logs.get('accuracy')
        if val_acc >= self.threshold:
            self.model.stop_training = True

callback = ThresholdCallback(0.85)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_indices, Y, epochs=epochs, batch_size=1, callbacks=[callback])

loss, accuracy = model.evaluate(X_indices, Y)
print(f"Loss: {loss}, Accuracy: {accuracy}")
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
model.save(model_file_name)
