📧 Automação de Envio de Propostas - Metrópoles
Sistema em Python com interface gráfica para automação do envio de propostas personalizadas por e-mail, segmentadas por público-alvo (ex: bets, crypto, saúde).

✨ Funcionalidades
✅ Interface desktop simples (Tkinter)
✅ Personalização de:

Assunto do e-mail

Corpo do e-mail

Segmento (dropdown automático)
✅ Envio em massa para todos os contatos de um segmento
✅ Anexo automático da proposta correspondente ao segmento
✅ Logs detalhados de execução e falhas
✅ Compatível com Gmail, Outlook, SMTP corporativo
✅ Totalmente offline (não é web), ideal para operação interna

📂 Estrutura do projeto
plaintext
Copiar
Editar
/automacao_envio_propostas/
│
├── contatos/              # CSVs com contatos por segmento
│   ├── bets.csv
│   ├── crypto.csv
│   ├── saude.csv
│
├── propostas/             # PDFs de proposta por segmento
│   ├── bets.pdf
│   ├── crypto.pdf
│   ├── saude.pdf
│
├── logs/                  # Logs automáticos da execução
│   ├── log_YYYY-MM-DD.txt
│
├── config.json            # Gerado automaticamente pela interface
├── main.py                # Script principal de envio
├── interface.py           # Interface gráfica desktop (Tkinter)
├── requirements.txt       # Dependências do projeto
└── executar.bat           # Executa main.py (opcional)
⚙️ Pré-requisitos
Python 3.8 ou superior

Conta de e-mail com suporte a SMTP (ex: Gmail com senha de aplicativo)

Instalação das dependências do projeto

📋 Instalação passo a passo
1️⃣ Clone o projeto ou copie a estrutura
bash
Copiar
Editar
git clone https://github.com/seu-usuario/automacao_envio_propostas.git
cd automacao_envio_propostas
2️⃣ (Opcional) Crie um ambiente virtual
bash
Copiar
Editar
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
3️⃣ Instale as dependências
bash
Copiar
Editar
pip install -r requirements.txt
Se necessário, instale o Tkinter manualmente (geralmente já vem com Python):

bash
Copiar
Editar
pip install tk
🚀 Como usar
1️⃣ Abra a interface gráfica
bash
Copiar
Editar
python interface.py
2️⃣ Preencha os campos
Assunto do e-mail

Corpo do e-mail (suporta {nome} para personalização)

Segmento (dropdown com os segmentos detectados automaticamente em /contatos/)

3️⃣ Clique em ENVIAR E-MAILS
O sistema gera config.json com suas opções

Executa main.py automaticamente

Envia o e-mail com:

Assunto escolhido

Corpo personalizado para cada contato

Proposta correspondente (propostas/segmento.pdf)

📨 Lógica de envio
1️⃣ Para cada contato no CSV contatos/segmento.csv:

cs
Copiar
Editar
Nome,Email
João Silva,joao@email.com
Maria Souza,maria@email.com
...
2️⃣ Envia:

plaintext
Copiar
Editar
Assunto: [assunto escolhido]
Corpo: Olá João Silva,
[corpo do e-mail]
Anexo: propostas/segmento.pdf
🔍 Exemplo prático
Segmento bets
contatos/bets.csv

cs
Copiar
Editar
Nome,Email
João Silva,joao@teste.com
Maria Souza,maria@teste.com
propostas/bets.pdf

Ao selecionar "bets" e clicar em enviar:

Contato	Anexo enviado
João Silva (joao@...)	bets.pdf
Maria Souza (maria@...)	bets.pdf

📝 Sobre config.json
Gerado automaticamente pela interface:

json
Copiar
Editar
{
  "email_remetente": "seu-email@dominio.com",
  "senha_app": "senha-de-aplicativo",
  "assunto_email": "Seu assunto",
  "corpo_email": "Olá {nome},\n\nTexto do e-mail.\n\nAtt,",
  "segmento": ["bets"]
}
🔒 Segurança: senha de aplicativo
Gmail:
Ative 2FA na conta

Gere uma senha de aplicativo em:
https://myaccount.google.com/security

Use essa senha no campo "senha_app".

📝 Logs
Todos os eventos (envios, erros, validações) são registrados em:

bash
Copiar
Editar
/logs/log_YYYY-MM-DD.txt
Exemplo:

plaintext
Copiar
Editar
09:00:01 - ✅ E-mail enviado para João Silva <joao@email.com>
09:00:05 - ✅ E-mail enviado para Maria Souza <maria@email.com>
🛠️ Possíveis melhorias (roadmap)
✅ Multi-segmento (enviar para mais de um segmento de uma vez)
✅ Barra de progresso
✅ Confirmação de envio antes de começar
✅ Pré-visualização da lista de contatos antes do envio
✅ Configuração dinâmica de servidor SMTP (Outlook, SMTP personalizado)

🤝 Contribuição
Projeto interno da equipe Metrópoles.
Para sugestões e melhorias, entrar em contato com o time de TI.

📝 Licença
Projeto interno - uso restrito.

