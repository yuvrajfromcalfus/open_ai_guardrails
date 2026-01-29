from groq import Groq

client = Groq()

models = client.models.list()

for m in models.data:
    print(m.id)
