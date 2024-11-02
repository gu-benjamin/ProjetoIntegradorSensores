import google.generativeai as genai
from query import *
import pandas as pd
import mysql.connector



# Conexao com a API
GOOGLE_API_KEY= ('AIzaSyDzh2rQ_ukoLvgVakAbTgddbweV8uoePb8')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Define o modelo para a tabela tb_memoria
class Memoria(conexao.Model):
    __tablename__ = 'tb_memoria'
    id = conexao.Column(conexao.Integer, primary_key=True, autoincrement=True)
    prompt = conexao.Column(conexao.Text, unique=True, nullable=False)
    resposta_gemini = conexao.Column(conexao.Text, nullable=False)
    
# Verifica se o prompt já está na memória
def check_memory(prompt):
    memoria = Memoria.query.filter_by(prompt=prompt).first()
    return memoria.resposta_gemini if memoria else None

# Salva um novo prompt e sua resposta na memória
def save_to_memory(prompt, response):
    new_entry = Memoria(prompt=prompt, resposta_gemini=response)
    conexao.session.add(new_entry)
    conexao.session.commit()

#--------------Prompt----------------

#Select no banco de dados
query = "SELECT * FROM tb_registro"  
df = conexao(query)  
df['tempo_registro'] = pd.to_datetime(df['tempo_registro'])    

# Formatação do prompt
prompt = f"A partir desta base de dados: {df.to_string()} faça uma análise comparando entre a região de São Paulo com a região do Grande ABC, analisando as diferenças entre elas"


# Verifica se o prompt já foi respondido e está na memória
response_text = check_memory(prompt)
if response_text:
        print("Resposta recuperada da memória:")
        print(response_text)
else:
        # Gera uma nova resposta usando o modelo Gemini
        response = model.generate_content(prompt)
        response_text = response.text if hasattr(response, 'text') else "Erro: Resposta inválida do Gemini."

# Armazena o novo prompt e resposta na memória
save_to_memory(prompt, response_text)

print("Resposta gerada pelo Gemini:")
print(response_text)