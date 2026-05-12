import os
from faker import Faker
fake = Faker(locale="fr_FR")

# Faker.seed(0)
repertoire = os.path.dirname(__file__)
file = os.path.join(repertoire, "motsEtDate.md")
with open(file, "w+") as f:
    # f.write(fake.sentence(nb_words=200))  # pb
    for i in range(100):
        f.write("# title\n")
        # f.write(fake.sentence(nb_words=10) + "\n") # pb
        f.write("[label](link.md)\n") # evite bien le link
