import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import pandas as pd
import shutil
import smtplib
from email.message import EmailMessage
import mimetypes

CONFIG_PATH = "config.json"
CONTATOS_DIR = "contatos"
SUBPASTAS = ["agencias", "clientes"]

# Cria as subpastas se não existirem
for subpasta in SUBPASTAS:
    os.makedirs(os.path.join(CONTATOS_DIR, subpasta), exist_ok=True)

def abrir_tela_principal(config):
    root = tk.Tk()
    root.title("Envio de Propostas - Metrópoles")
    root.geometry("500x700")

    anexos_paths = []

    tk.Label(root, text="Assunto do e-mail:").pack(pady=(10, 0))
    entry_assunto = tk.Entry(root, width=60)
    entry_assunto.pack()

    tk.Label(root, text="Corpo do e-mail:").pack(pady=(10, 0))
    text_corpo = tk.Text(root, width=60, height=10)
    text_corpo.pack()

    tk.Label(root, text="E-mail em cópia (CC):").pack(pady=(10, 0))
    entry_cc = tk.Entry(root, width=60)
    entry_cc.pack()

    tk.Label(root, text="Tipo de envio:").pack(pady=(10, 0))
    tipo_envio_var = tk.StringVar(value="agencias")
    frame_tipo = tk.Frame(root)
    frame_tipo.pack()
    tk.Radiobutton(frame_tipo, text="Agências", variable=tipo_envio_var, value="agencias").pack(side="left", padx=5)
    tk.Radiobutton(frame_tipo, text="Clientes", variable=tipo_envio_var, value="clientes").pack(side="left", padx=5)

    tk.Label(root, text="Segmento (selecionado):").pack(pady=(10, 0))
    segmento_var = tk.StringVar()
    entry_segmento = tk.Entry(root, textvariable=segmento_var, width=40, state="readonly")
    entry_segmento.pack()

    def selecionar_arquivo():
        caminho = filedialog.askopenfilename(
            title="Selecionar arquivo de contatos",
            filetypes=[("Arquivos CSV", "*.csv")]
        )
        if not caminho:
            return

        nome_segmento = os.path.splitext(os.path.basename(caminho))[0]
        subpasta = tipo_envio_var.get()
        pasta_destino = os.path.join(CONTATOS_DIR, subpasta)
        os.makedirs(pasta_destino, exist_ok=True)
        caminho_destino = os.path.join(pasta_destino, nome_segmento + ".csv")

        try:
            shutil.copy(caminho, caminho_destino)
            df = pd.read_csv(caminho_destino)
            segmento_var.set(nome_segmento)
            text_corpo.delete("1.0", tk.END)
            messagebox.showinfo("Sucesso", f"Arquivo carregado como '{nome_segmento}.csv'")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao processar arquivo: {e}")

    def selecionar_anexos():
        caminhos = filedialog.askopenfilenames(title="Selecionar anexos")
        if caminhos:
            anexos_paths.clear()
            anexos_paths.extend(caminhos)
            nomes = [os.path.basename(c) for c in caminhos]
            messagebox.showinfo("Anexos selecionados", f"Arquivos:{chr(10).join(nomes)}")

    def gerar_assinatura():
        return """
        <div style="font-family: Arial; font-size: 12px; display: flex; align-items: center;">
          <img class="logo" src="https://ci3.googleusercontent.com/meips/ADKq_NaX6Grba4uPD9NzgZR3lrr3jsTQwD7oLVm1R09zw4sPwHeCJw6SYeUN1Yg8-QBdk_sMGrNO8x6g1VmKiwWuaE930fPekwkW2oNEb4utYg=s0-d-e1-ft#http://files.metropoles.com/assinatura-email/M-email.gif"
           style="margin-right:12px; max-height:50px">
          <div>
            <strong style="font-family: sans-serif; font-size: 20px; color: red;">Caio Correa</strong><br>
            Executivo de Negócios<br>
            <span style="color: gray;">tel: +55 61 99304-0370</span><br>
            <div style="margin-top:5px;">
              <a href="https://www.facebook.com/metropolesdf/"><img src="./assets/facebook.png" alt="facebook"></a>
              <a href="https://www.instagram.com/metropolesdf/"><img src="./assets/insta.png" alt="Instagram"></a>
              <a href="https://twitter.com/Metropoles"><img src="./assets/twitter.png" alt="Twitter"></a>
              <a href="https://www.youtube.com/metropolesdf"><img src="./assets/ytb.png" alt="Youtube"></a>
              <a href="https://www.linkedin.com/company/metr%C3%B3poles"><img src="./assets/linkedin.png" alt="Linkedin"></a>
              <img src="./assets/Metropoles.png" alt="Metrópoles" style="margin-left:50px;">
            </div>
          </div>
        </div>
        """

    def enviar_emails():
        assunto = entry_assunto.get()
        corpo = text_corpo.get("1.0", tk.END).strip()
        segmento = segmento_var.get()
        email_copia = entry_cc.get().strip()
        tipo_envio = tipo_envio_var.get()

        if not assunto or not corpo or not segmento:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        config["assunto_email"] = assunto
        config["corpo_email"] = corpo
        config["segmento"] = [segmento]
        config["email_copia"] = email_copia
        config["tipo_envio"] = tipo_envio

        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar config.json: {e}")
            return

        caminho_csv = os.path.join(CONTATOS_DIR, tipo_envio, segmento + ".csv")

        try:
            df = pd.read_csv(caminho_csv)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler o CSV de contatos: {e}")
            return

        email_remetente = config.get("email_remetente")
        senha_app = config.get("senha_app")

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(email_remetente, senha_app)
                enviados = 0

                for _, row in df.iterrows():
                    nome = row.get("nome", "").strip()
                    email_destino = row.get("email", "").strip()
                    if not nome or not email_destino:
                        continue

                    corpo_personalizado = corpo.replace("{{nome}}", nome) + gerar_assinatura()

                    msg = EmailMessage()
                    msg["Subject"] = assunto
                    msg["From"] = email_remetente
                    msg["To"] = email_destino
                    if email_copia:
                        msg["Cc"] = email_copia

                    msg.add_alternative(corpo_personalizado, subtype="html")

                    for caminho_anexo in anexos_paths:
                        tipo, _ = mimetypes.guess_type(caminho_anexo)
                        tipo = tipo or 'application/octet-stream'
                        with open(caminho_anexo, "rb") as f:
                            msg.add_attachment(f.read(), maintype=tipo.split("/")[0], subtype=tipo.split("/")[1], filename=os.path.basename(caminho_anexo))

                    smtp.send_message(msg)
                    enviados += 1

            messagebox.showinfo("Sucesso", f"E-mails enviados com sucesso para {enviados} contatos!")

        except Exception as e:
            messagebox.showerror("Erro no envio", f"Ocorreu um erro ao enviar os e-mails:\n{e}")

    tk.Button(root, text="Selecionar arquivo de contatos", command=selecionar_arquivo).pack(pady=10)
    tk.Button(root, text="Selecionar anexos", command=selecionar_anexos).pack(pady=5)
    tk.Button(root, text="ENVIAR E-MAILS", command=enviar_emails, bg="green", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

    root.mainloop()

def abrir_tela_login():
    login = tk.Tk()
    login.title("Login - Metrópoles")
    login.geometry("400x250")

    tk.Label(login, text="E-mail do remetente:").pack(pady=(20, 0))
    entry_email = tk.Entry(login, width=40)
    entry_email.pack()

    tk.Label(login, text="Senha do app (Gmail):").pack(pady=(10, 0))
    entry_senha = tk.Entry(login, width=40, show="*")
    entry_senha.pack()

    def fazer_login():
        email = entry_email.get().strip()
        senha = entry_senha.get().strip()
        if not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        config = {
            "email_remetente": email,
            "senha_app": senha
        }

        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar config.json: {e}")
            return

        login.destroy()
        abrir_tela_principal(config)

    tk.Button(login, text="Login", command=fazer_login, bg="blue", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
    login.mainloop()

if __name__ == "__main__":
    try:
        config = {}
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)

        if config.get("email_remetente") and config.get("senha_app"):
            abrir_tela_principal(config)
        else:
            abrir_tela_login()

    except Exception as e:
        import traceback
        print("Erro ao iniciar a aplicação:")
        traceback.print_exc()
        input("Pressione ENTER para fechar...")