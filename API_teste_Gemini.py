from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask("registro")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:525748@127.0.0.1/bd_medidor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


mybd1 = SQLAlchemy(app) 

            
class Registro(mybd1.Model):
    __tablename__ = 'tb_registro'
    id = mybd1.Column(mybd1.Integer, primary_key=True, autoincrement=True)
    temperatura = mybd1.Column(mybd1.Numeric(10, 2))
    pressao = mybd1.Column(mybd1.Numeric(10, 2))
    altitude = mybd1.Column(mybd1.Numeric(10, 2))
    umidade = mybd1.Column(mybd1.Numeric(10, 2))
    co2 = mybd1.Column(mybd1.Numeric(10, 2))
    poeira = mybd1.Column(mybd1.Numeric(10, 2))
    tempo_registro = mybd1.Column(mybd1.DateTime)
    regiao = mybd1.Column(mybd1.String(100))
 
    # Método para converter o registro em JSON
    def to_json(self):
     return {
        "id": self.id,
        "temperatura": float(self.temperatura) if self.temperatura is not None else None,
        "pressao": float(self.pressao) if self.pressao is not None else None,
        "altitude": float(self.altitude) if self.altitude is not None else None,
        "umidade": float(self.umidade) if self.umidade is not None else None,
        "co2": float(self.co2) if self.co2 is not None else None,
        "poeira": float(self.poeira) if self.poeira is not None else None,
        "tempo_registro": self.tempo_registro.isoformat() if self.tempo_registro else None,
        "regiao": self.regiao
    }
    
# Seleciona todos os registros
@app.route('/registro', methods=['GET'])
def selecionar_registros():
    registros = Registro.query.all()
    registros_json = [registro.to_json() for registro in registros]
    
    return gera_response(200, 'registros', registros_json)

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

if __name__ == '__main__':
    with app.app_context():
        mybd1.create_all()
        app.run(port=5000, host="localhost", debug=True)
