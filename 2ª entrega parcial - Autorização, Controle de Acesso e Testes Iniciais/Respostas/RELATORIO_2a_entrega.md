# Relatório da 2ª Entrega — Autorização, Controle de Acesso e Testes Iniciais

**Projeto:** Central de Comunicados Corporativos — ConnectPlus (API em FastAPI)
**Disciplina:** Projeto Disciplina — 2AV
**Grupo:**

| Integrante | Matrícula |
|---|---|
| David William Dos Santos Guedes Alcoforado | 01926604 |
| Júlio Silvestre de Lima Simão | 01888262 |
| Maria Fernanda Barbosa Dos Santos | 01898944 |
| Raquel Macêdo De França | 01910871 |
| Sarah Leticia Souza Da Silva | 01910076 |
| Ygor Da Silva Alves | 01902390 |

**Prazo:** 12/11/2026 às 23:59
**Repositório:** https://github.com/ygor-sys/api-connectplus

## 1. Objetivo
Aplicar permissões aos recursos da API e iniciar a implementação dos testes automatizados, mantendo os requisitos da 1ª parcial funcionando.

## 2. Solução
API em Python + FastAPI, SQLite (SQLAlchemy), JWT (Bearer) e senhas com bcrypt.

- `app/` — código da API
- `docs/MATRIZ_PERMISSOES.md` — matriz de permissões
- `tests/` — `conftest.py`, `test_autenticacao.py`, `test_autorizacao.py`, `test_comunicados.py`
- `pytest.ini` — configuração do Pytest (`-v`)

## 3. Perfis
| Perfil | Permissões |
|---|---|
| Administrador | Publica, edita e exclui os próprios comunicados; consulta todos |
| Colaborador | Consulta comunicados e os próprios dados |

Contas de demonstração: `admin@connectplus.com`, `admin2@connectplus.com` (administradores) e `colaborador@connectplus.com`.

## 4. Matriz de permissões
| Endpoint | Anônimo | Colaborador | Administrador | Proteção |
|---|---|---|---|---|
| POST /auth/login | Permitido | Permitido | Permitido | Pública |
| GET /auth/me | 401 | Permitido (só os próprios dados) | Permitido (só os próprios dados) | `usuario_atual` |
| GET /comunicados | 401 | Permitido | Permitido | `usuario_atual` |
| GET /comunicados/{id} | 401 | Permitido | Permitido | `usuario_atual` |
| POST /comunicados | 401 | 403 | Permitido | `somente_admin` |
| PUT /comunicados/{id} | 401 | 403 | Só o autor (outro admin: 403) | `somente_admin` + `_exigir_autor` |
| DELETE /comunicados/{id} | 401 | 403 | Só o autor (outro admin: 403) | `somente_admin` + `_exigir_autor` |

Endpoints protegidos: 6 (3 exclusivos de administrador e 3 para qualquer autenticado).

## 5. Controle de acesso
- **401 Unauthorized:** sem identificação (sem token, token inválido ou credenciais erradas) — `usuario_atual` em `app/deps.py`.
- **403 Forbidden:** identificado, porém sem permissão — `somente_admin` em `app/deps.py`.
- **Operações incompatíveis com o perfil:** o colaborador não publica, edita nem exclui (403).
- **Acesso aos próprios recursos:** `/auth/me` devolve só os dados do dono do token; um administrador só edita/exclui comunicados que ele mesmo criou (`_exigir_autor`, 403 para outro admin).
- O autor do comunicado vem do token; `autor_id` e `perfil` no corpo são rejeitados (422); respostas não expõem senha nem hash.

## 6. Testes automatizados (Pytest)
Ambiente com banco SQLite temporário (`tests/conftest.py`). **22 testes**, todos aprovados.

**Autenticação (6):** login admin retorna token; senha errada 401; e-mail inexistente 401; `/auth/me` sem token 401; token inválido 401; `/auth/me` não expõe senha.

**Autorização (9):** admin publica e vira autor; colaborador não publica/edita/exclui (403); sem token é 401 e não 403; autor/perfil no corpo é 422; admin 2 não edita nem exclui comunicado de outro admin (403); admin 2 lê (200).

**Funcionalidades (7):** colaborador lista (200); listar sem token 401; inexistente 404; título ausente/vazio 422; admin atualiza (200); admin exclui e depois 404; dados persistem após reiniciar a aplicação.

**Resultado de `python -m pytest`:** `22 passed, 1 warning` (aviso de depreciação do `httpx`, sem efeito no resultado).

![pytest -v](../evidencias/01_pytest_v_22_passed.png)

## 7. Requisições: acessos permitidos e negados (Swagger)

**POST /comunicados como administrador — 201 Created**
![POST admin 201](../evidencias/02_swagger_post_admin_201.png)

**PUT /comunicados/1 como administrador 2 (não é o autor) — 403 Forbidden**
![PUT admin2 403](../evidencias/03_swagger_put_admin2_403.png)

**PUT /comunicados/1 como administrador autor — 200 OK**
![PUT admin 200](../evidencias/05_swagger_put_admin_200.png)

**POST /comunicados como colaborador — 403 Forbidden**
![POST colaborador 403](../evidencias/06_swagger_post_colaborador_403.png)

**GET /comunicados sem autenticação — 401 Unauthorized**
![GET sem token 401](../evidencias/07_swagger_get_sem_token_401.png)

**Endpoints protegidos (cadeados no Swagger)**
![Endpoints protegidos](../evidencias/10_swagger_endpoints_protegidos_cadeados.png)

**PUT em comunicado inexistente — 404 Not Found**
![PUT 404](../evidencias/11_swagger_put_inexistente_404.png)

## 8. GitHub
Código enviado para https://github.com/ygor-sys/api-connectplus (branch `main`).

![git push](../evidencias/04_git_push_sucesso.png)

![Repositório no GitHub](../evidencias/09_github_repositorio.png)

Estrutura da pasta `tests/` no repositório:

![Pasta tests no GitHub](../evidencias/08_github_pasta_tests.png)

## 9. Atendimento aos requisitos
| # | Requisito | Situação |
|---|---|---|
| 1 | Manter a 1ª parcial funcionando | Atendido (testes de funcionalidades) |
| 2 | Dois perfis com permissões distintas | Atendido |
| 3 | Matriz de permissões | Seção 4 |
| 4 | Controle de acesso em 4+ endpoints | Atendido (6) |
| 5 | Impedir operações incompatíveis com o perfil | Atendido (403) |
| 6 | Acesso aos próprios recursos | Atendido (`/auth/me` e regra do autor) |
| 7 | Diferenciar 401 e 403 | Atendido |
| 8 | Ambiente de testes com Pytest | Atendido |
| 9 | 8+ testes automatizados | Atendido (22) |
| 10 | Demonstrar a execução dos testes | Seção 6 |

## 10. Como executar
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
python -m pytest
```
Swagger: http://127.0.0.1:8000/docs
