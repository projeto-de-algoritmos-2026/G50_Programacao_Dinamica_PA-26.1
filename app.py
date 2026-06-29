from flask import Flask, render_template, request, session, redirect, url_for
from algoritmos.lis import maior_subsequencia_crescente, reconstruir_lis

app = Flask(__name__)
app.secret_key = "chave_secreta_para_o_jogo_lis"

FASES = [
    {"nivel": 1, "sequencia": [10, 22, 9, 33, 21, 50, 41, 60]},
    {"nivel": 2, "sequencia": [3, 10, 2, 1, 20]},
    {"nivel": 3, "sequencia": [50, 3, 10, 7, 40, 80]},
    {"nivel": 4, "sequencia": [10, 22, 9, 33, 21, 50, 41, 60, 80, 21, 15, 90]},
    {"nivel": 5, "sequencia": [1, 2, 3, 4, 5, 0, 10]}
]

@app.route("/", methods=["GET", "POST"])
def index():
    if "fase_atual" not in session:
        session["fase_atual"] = 0

    fase_idx = session["fase_atual"]
    
    if fase_idx >= len(FASES):
        return redirect(url_for("fim_de_jogo"))

    fase_dados = FASES[fase_idx]
    sequencia = fase_dados["sequencia"]
    nivel = fase_dados["nivel"]

    vetor, dp, pre, indice_final = maior_subsequencia_crescente(sequencia)
    solucao = reconstruir_lis(vetor, pre, indice_final)

    resultado = None
    resposta_usuario = ""

    if request.method == "POST":
        resposta_usuario = request.form.get("resposta", "")
        try:
            tentativa = list(map(int, resposta_usuario.split()))
        except ValueError:
            tentativa = []

        if tentativa == solucao:
            resultado = "acertou"
        else:
            resultado = "errou"

    return render_template(
        "index.html",
        sequencia=sequencia,
        solucao=solucao,
        dp=dp,
        pre=pre,
        resultado=resultado,
        resposta=resposta_usuario,
        nivel=nivel
    )

@app.route("/fim")
def fim_de_jogo():
    return render_template("fim.html")

@app.route("/proxima")
def proxima_fase():
    if "fase_atual" in session:
        session["fase_atual"] += 1
    return redirect(url_for("index"))

@app.route("/reset")
def resetar_jogo():
    session["fase_atual"] = 0
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)