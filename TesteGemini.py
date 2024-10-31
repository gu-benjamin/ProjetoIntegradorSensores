import google.generativeai as genai
from query import *

# Conexao com a API
GOOGLE_API_KEY= ('AIzaSyDzh2rQ_ukoLvgVakAbTgddbweV8uoePb8')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

query = "SELECT * FROM tb_registro"  
df = conexao(query)  
df['tempo_registro'] = pd.to_datetime(df['tempo_registro'])


try:
    response = model.generate_content("Escreva um texto simples")

    if hasattr(response, 'content'):
            resposta = response.content
    elif hasattr(response, 'text'):
            resposta = response.text
    else:
            resposta = "Erro ao obter a resposta da API"
        
    print("Resposta da API Gemini:", resposta)

except Exception as e:
        print(f"Erro ao chamar a API Gemini: {str(e)}")