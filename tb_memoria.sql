
CREATE TABLE tb_memoria(
    id INT AUTO_INCREMENT PRIMARY KEY,
    prompt LONGTEXT,
    resposta_gemini LONGTEXT
);

SELECT * FROM tb_memoria;

INSERT INTO tb_memoria (prompt, resposta_gemini) VALUES
("Memória: Olá Gemini! Essa é a sua memória, antes de cada resposta considere as informações contidas nela", "resposta: Entendido"),
("Prompts: Dentro de cada prompt vai existir o texto: Esse é o contexto inicial antes de cada prompt: Considere a seguinte base de dado:Não retorne esse texto nas respostas. Isso significa que os dados da tabela registro sempre serão entregues para você antes das perguntas.", "resposta: Entendido"),
("Contexto: Você está sendo aplicado em um dashboard da biblioteca streamlit, nele contém gráficos com dados de temperatura, umidade, co2, pressão, altitude, poeira, tempo de registro e regiões que está sendo feita a coleta de dados via sensores.", "resposta: Entendido");
