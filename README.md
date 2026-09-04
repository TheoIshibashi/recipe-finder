Recipe Finder

API backend em FastAPI que consome a TheMealDB para buscar receitas — reconstrução de um projeto de estudo anterior, dessa vez sem banco de dados local, consumindo dados de uma API externa em tempo real.

Stack
FastAPI — framework web
httpx — cliente HTTP assíncrono, usado para chamar a TheMealDB
Pydantic — validação e serialização dos dados
python-dotenv — carregamento de variáveis de ambiente

Sem banco de dados: os dados vêm sempre ao vivo da API externa.

Como rodar
Clone o repositório e entre na pasta do projeto.
Crie e ative um ambiente virtual:
bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
Instale as dependências:
bash
   pip install -r requirements.txt
Copie o arquivo de exemplo de variáveis de ambiente:
bash
   cp .env.example .env

O valor padrão (MEALDB_API_KEY=1) já é a chave de teste pública da TheMealDB — não precisa de cadastro para rodar o projeto localmente.

Suba o servidor:
bash
   uvicorn app.main:app --reload
Acesse a documentação interativa (Swagger UI) em http://127.0.0.1:8000/docs.
Endpoints
Método	Rota	Descrição	Status
GET	/health	Health check da API	✅ Pronto
GET	/recipes/random	Retorna uma receita aleatória	✅ Pronto
GET	/recipes/search?name=	Busca receitas por nome	🚧 Planejado
GET	/recipes/{recipe_id}	Detalhes completos de uma receita por id	🚧 Planejado
GET	/recipes/by-ingredient?ingredient=	Lista receitas que usam um ingrediente	🚧 Planejado
GET	/categories	Lista as categorias de receitas disponíveis	🚧 Planejado
Estrutura do projeto
app/
├── main.py            # instância do FastAPI, registro de rotas, /health
├── config.py           # variáveis de ambiente (MEALDB_API_KEY, PROJECT_NAME)
├── mealdb_client.py     # comunicação HTTP assíncrona com a TheMealDB
├── schemas.py            # modelos Pydantic + funções de parsing do JSON da API
└── routes.py              # endpoints da API
Limitações conhecidas da API gratuita

A TheMealDB tem uma chave de teste pública (1) gratuita e sem necessidade de cadastro, mas com algumas restrições em relação à versão paga:

Filtro por múltiplos ingredientes ao mesmo tempo não está disponível (só um ingrediente por busca).
Endpoints da API V2 (mais recentes) exigem chave paga.

Essas limitações vieram da própria documentação oficial e moldaram o escopo dos endpoints deste projeto.

Créditos

Dados de receitas fornecidos por TheMealDB.