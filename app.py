from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Caminho inicial da imagem
current_image = "images/default.png"


@app.route("/")
def home():
    global current_image
    return render_template("index.html", image_path=current_image)


@app.route("/trocar_imagem", methods=["POST"])
def trocar_imagem():
    global current_image
    # Receba o novo caminho da imagem a partir de um formulário ou lógica
    new_image = request.form.get("new_image", "images/default.jpg")
    current_image = new_image
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
