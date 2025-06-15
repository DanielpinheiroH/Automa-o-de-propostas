import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
import os
import pandas as pd
import smtplib
from email.message import EmailMessage
import mimetypes

CONFIG_PATH = "config.json"
CONTATOS_DIR = "contatos"
SUBPASTAS = ["agencias", "clientes"]

# Cria subpastas se não existirem
for subpasta in SUBPASTAS:
    os.makedirs(os.path.join(CONTATOS_DIR, subpasta), exist_ok=True)

def gerar_assinatura():
    return '''
    <div style="font-family: Arial; font-size: 12px; display: flex; align-items: center;">
        <img class="logo" src="https://ci3.googleusercontent.com/meips/ADKq_NaX6Grba4uPD9NzgZR3lrr3jsTQwD7oLVm1R09zw4sPwHeCJw6SYeUN1Yg8-QBdk_sMGrNO8x6g1VmKiwWuaE930fPekwkW2oNEb4utYg=s0-d-e1-ft#http://files.metropoles.com/assinatura-email/M-email.gif"
        style="margin-right:10px; max-height:50px">
        <div>
            <h2 style="margin:0px;font-family:arial,Geogrotesque-SemiBold;font-size:12px;text-transform:uppercase;color:rgb(172,27,13)">caio corrêa</h2>
            <h3 style="margin:2px 0 0;font-family:georgia,Merriweather;font-size:14px;color:rgb(59,16,19);letter-spacing:0px">Executivo de Negócios</h3>        
            <a href="tel:+55%2061%2099304-0370" style="color:rgb(167,160,161);margin:5px 0px 0px;padding:0px" target="_blank">tel:+55 61 99304-0370</a><br><br>
            <hr style="margin: 0; padding: 0; background-color: rgb(229,229,229); height: 2px; border: none; width: 500px; clear: both;">
            <div style="margin-top:5px;">
                <a href="https://www.facebook.com/metropolesdf/"><img src="https://raw.githubusercontent.com/DanielpinheiroH/Automa-o-de-propostas/refs/heads/JonatasTavares1-patch-1/assets/facebook.png" alt="facebook"></a>
                <a href="https://www.instagram.com/metropolesdf/"><img src="https://raw.githubusercontent.com/DanielpinheiroH/Automa-o-de-propostas/refs/heads/JonatasTavares1-patch-1/assets/insta.png" alt="Instagram"></a>
                <a href="https://twitter.com/Metropoles"><img src="https://raw.githubusercontent.com/DanielpinheiroH/Automa-o-de-propostas/refs/heads/JonatasTavares1-patch-1/assets/twitter.png" alt="Twitter"></a>
                <a href="https://www.youtube.com/metropolesdf"><img src="https://raw.githubusercontent.com/DanielpinheiroH/Automa-o-de-propostas/refs/heads/JonatasTavares1-patch-1/assets/ytb.png" alt="Youtube"></a>
                <a href="https://www.linkedin.com/company/metr%C3%B3poles"><img src="https://raw.githubusercontent.com/DanielpinheiroH/Automa-o-de-propostas/refs/heads/JonatasTavares1-patch-1/assets/linkedin.png" alt="Linkedin"></a>
                <img src="https://raw.githubusercontent.com/DanielpinheiroH/Automa-o-de-propostas/refs/heads/JonatasTavares1-patch-1/assets/Metropoles.png" alt="Metrópoles" style="margin-left:300px;">
            </div>
        </div>
    </div>
    '''

def abrir_tela_principal(config):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Envio de Propostas - Metrópoles")
    root.geometry("600x750")

    anexos_paths = []

    ctk.CTkLabel(root, text="Assunto do e-mail:").pack(pady=(10, 0))
    entry_assunto = ctk.CTkEntry(root, width=500)
    entry_assunto.pack(pady=5)

    ctk.CTkLabel(root, text="Corpo do e-mail:").pack(pady=(10, 0))
    text_corpo = ctk.CTkTextbox(root, width=500, height=180)
    text_corpo.pack(pady=5)

    ctk.CTkLabel(root, text="E-mail em cópia (CC):").pack(pady=(10, 0))
    entry_cc = ctk.CTkEntry(root, width=500)
    entry_cc.pack(pady=5)

    ctk.CTkLabel(root, text="Tipo de envio:").pack(pady=(10, 0))
    tipo_envio_var = ctk.StringVar(value="agencias")
    frame_radio = ctk.CTkFrame(root)
    frame_radio.pack(pady=5)
    ctk.CTkRadioButton(frame_radio, text="Agências", variable=tipo_envio_var, value="agencias").pack(side="left", padx=10)
    ctk.CTkRadioButton(frame_radio, text="Clientes", variable=tipo_envio_var, value="clientes").pack(side="left", padx=10)

    ctk.CTkLabel(root, text="Segmento (selecionado):").pack(pady=(10, 0))
    segmento_var = ctk.StringVar()
    entry_segmento = ctk.CTkEntry(root, textvariable=segmento_var, width=400, state="disabled")
    entry_segmento.pack(pady=5)

    def selecionar_arquivo():
        subpasta = tipo_envio_var.get()
        initial_dir = os.path.join(CONTATOS_DIR, subpasta)
        caminho = filedialog.askopenfilename(
            title="Selecionar arquivo de contatos",
            filetypes=[("Arquivos CSV", "*.csv")],
            initialdir=initial_dir
        )
        if not caminho:
            return
        nome_segmento = os.path.splitext(os.path.basename(caminho))[0]
        segmento_var.set(nome_segmento)
        text_corpo.delete("1.0", "end")
        messagebox.showinfo("Arquivo selecionado", f"Segmento carregado: {nome_segmento}")

    def selecionar_anexos():
        caminhos = filedialog.askopenfilenames(title="Selecionar anexos")
        if caminhos:
            anexos_paths.clear()
            anexos_paths.extend(caminhos)
            nomes = [os.path.basename(c) for c in caminhos]
            messagebox.showinfo("Anexos selecionados", f"Arquivos:\n{chr(10).join(nomes)}")

    def enviar_emails():
        assunto = entry_assunto.get()
        corpo = text_corpo.get("1.0", "end").strip().replace("\n", "<br>")
        segmento = segmento_var.get()
        email_copia = entry_cc.get().strip()
        tipo_envio = tipo_envio_var.get()

        if not assunto or not corpo or not segmento:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
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
                            msg.add_attachment(
                                f.read(), maintype=tipo.split("/")[0],
                                subtype=tipo.split("/")[1], filename=os.path.basename(caminho_anexo)
                            )

                    smtp.send_message(msg)
                    enviados += 1

            messagebox.showinfo("Sucesso", f"E-mails enviados com sucesso para {enviados} contatos!")

        except Exception as e:
            messagebox.showerror("Erro no envio", f"Ocorreu um erro ao enviar os e-mails:\n{e}")

    ctk.CTkButton(root, text="Selecionar Contatos", command=selecionar_arquivo).pack(pady=10)
    ctk.CTkButton(root, text="Selecionar Anexos", command=selecionar_anexos).pack(pady=5)
    ctk.CTkButton(root, text="ENVIAR E-MAILS", command=enviar_emails, fg_color="green", text_color="white").pack(pady=20)

    root.mainloop()

def abrir_tela_login():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    login = ctk.CTk()
    login.title("Login - Metrópoles")
    login.geometry("400x250")

    ctk.CTkLabel(login, text="E-mail do remetente:").pack(pady=(20, 0))
    entry_email = ctk.CTkEntry(login, width=300)
    entry_email.pack()

    ctk.CTkLabel(login, text="Senha do app (Gmail):").pack(pady=(10, 0))
    entry_senha = ctk.CTkEntry(login, width=300, show="*")
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

        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        login.destroy()
        abrir_tela_principal(config)

    ctk.CTkButton(login, text="Login", command=fazer_login, fg_color="blue", text_color="white").pack(pady=20)
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
