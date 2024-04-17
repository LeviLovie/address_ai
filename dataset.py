import csv
import time
import random
from faker import Faker
from wonderwords import RandomWord
from alive_progress import alive_bar

sample_amount = 10000
sample_data_file_name = "dataset.csv"
test_data_amount = 50
test_data_file_name = "test_dataset.csv"

r = RandomWord()
faker=Faker()

def generate_address():
    return faker.address().replace("\n", " ").replace(",", "")

def random_substring(input_string):
    words = input_string.split()
    num_words_to_cut = min(4, len(words))
    words_to_remove_indices = random.sample(range(len(words)), num_words_to_cut)
    remaining_words = [word for idx, word in enumerate(words) if idx not in words_to_remove_indices]
    result = ' '.join(remaining_words)
    return result

with open(sample_data_file_name, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\\', quoting=csv.QUOTE_MINIMAL)
    with alive_bar(sample_amount) as bar:
        for i in range(0, sample_amount):
            address = generate_address()
            # spamwriter.writerow([address, address, 1])
            spamwriter.writerow([address, random_substring(address), 1])
            # spamwriter.writerow([address, random_substring(generate_address()), 0])
            spamwriter.writerow([address, generate_address(), 0])
            bar()

with open(test_data_file_name, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\\', quoting=csv.QUOTE_MINIMAL)
    with alive_bar(test_data_amount) as bar:
        for i in range(0, test_data_amount):
            address = generate_address()
            # spamwriter.writerow([address, address, 1])
            spamwriter.writerow([address, random_substring(address), 1])
            # spamwriter.writerow([address, random_substring(generate_address()), 0])
            spamwriter.writerow([address, generate_address(), 0])
            bar()
