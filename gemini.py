
import google.generativeai as genai
from query import *

GOOGLE_API_KEY= ('AIzaSyDzh2rQ_ukoLvgVakAbTgddbweV8uoePb8')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

query = "SELECT * FROM tb_registro"  # Consulta com o banco de dados.
df = conexao(query)  
df['tempo_registro'] = pd.to_datetime(df['tempo_registro'])

print(df.to_string())
# print(f"A partir desta base de dados: {df.to_string()} mostre o que contém nela e o que você compreende e quantas linhas possui e quantas você lê")
# response = model.generate_content(f"A partir desta base de dados: {df.to_string()} faça uma analise comparando entre a região de São Paulo com a região do Grande ABC, analisando as diferenças entre elas")
# response = model.generate_content(f"A partir desta base de dados: {df.to_string()} mostre o que contém nela e o que você compreende e quantas linhas possui e quantas você lê")

# print(response.text)