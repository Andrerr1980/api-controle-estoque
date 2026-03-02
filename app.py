from flask import Flask, request, jsonify
from models import db, Produto

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///estoque.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return {"mensagem": "API Controle de Estoque funcionando!"}

@app.route("/produtos", methods=["POST"])
def criar_produto():
    dados = request.json
    novo_produto = Produto(
        nome=dados["nome"],
        quantidade=dados["quantidade"],
        preco=dados["preco"]
    )
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify(novo_produto.to_dict()), 201

@app.route("/produtos", methods=["GET"])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([p.to_dict() for p in produtos])

@app.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    produto = Produto.query.get_or_404(id)
    dados = request.json
    produto.nome = dados["nome"]
    produto.quantidade = dados["quantidade"]
    produto.preco = dados["preco"]
    db.session.commit()
    return jsonify(produto.to_dict())

@app.route("/produtos/<int:id>", methods=["DELETE"])
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return {"mensagem": "Produto removido com sucesso"}

if __name__ == "__main__":
    app.run(debug=True)