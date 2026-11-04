import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Usuario  # Certifique-se de que a classe em models.py se chama Usuario
from app.security import gerar_hash  # Nome correto da função que descobrimos no seu security.py

# Garante que as tabelas estejam criadas
Base.metadata.create_all(bind=engine)


def criar_usuario_teste():
    db: Session = SessionLocal()

    # Configurações do seu usuário de teste
    email_teste = "admin@connectplus.com"
    senha_teste = "admin123"

    # Verifica se já existe o usuário
    try:
        usuario_existente = db.query(Usuario).filter(Usuario.email == email_teste).first()
        if usuario_existente:
            print(f"O usuário {email_teste} já existe no banco!")
            db.close()
            return

        # Cria o hash seguro e popula o objeto
        novo_usuario = Usuario(
            nome="Administrador",
            email=email_teste,
            senha_hash=gerar_hash(senha_teste)
        )

        db.add(novo_usuario)
        db.commit()
        print("==================================================")
        print(" USUÁRIO DE TESTE CRIADO COM SUCESSO!")
        print(f" Login/Email: {email_teste}")
        print(f" Senha: {senha_teste}")
        print("==================================================")
    except Exception as e:
        db.rollback()
        print(f"Erro ao interagir com a tabela/banco: {e}")
        print(
            "\n--> DICA: Se o erro for que 'Usuario' ou 'senha_hash' não existem com esse nome, cole aqui o seu arquivo app/models.py para ajustarmos!")
    finally:
        db.close()


if __name__ == "__main__":
    criar_usuario_teste()
