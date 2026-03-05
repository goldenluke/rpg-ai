# 🌍 Procedural RPG Engine
### Narrativa Procedural • Mundo Vivo • IA Semântica

Um **motor experimental de RPG procedural** que combina **simulação de mundo**, **narrativa gerada por IA** e **sistemas emergentes**.

Inspirado em:

- AI Dungeon  
- Dwarf Fortress  
- RimWorld  
- Roguelikes clássicos  

---

# ✨ Ideia do Projeto

Criar um **RPG infinito**, onde:

- o mundo evolui sozinho
- eventos emergem naturalmente
- a narrativa responde às ações do jogador
- a história nunca se repete

Fluxo conceitual:

```
jogador age
    ↓
evento no mundo
    ↓
motor narrativo interpreta
    ↓
IA gera narrativa
    ↓
história evolui
```

---

# 🧠 Arquitetura

```
Procedural RPG
│
├── QWAN Narrative Engine
│
├── World Simulation
│   ├── cidades
│   ├── NPCs
│   ├── facções
│   ├── quests
│   └── eventos
│
├── Combat System
│
├── Procedural Dungeons
│
├── Monster Generator
│
├── Persistent Narrative Memory
│
└── Web Interface
```

---

# 🧠 Motor Narrativo (QWAN)

O motor utiliza **embeddings semânticos** para interpretar o tom da narrativa.

Exemplo:

```
entrada do jogador
"eu ataco o monstro"

↓ embeddings

detecção: combate

↓ narrativa gerada

"O impacto do seu golpe ecoa pelo salão..."
```

Tipos de narrativa detectados:

- combate  
- magia  
- drama  
- exploração  
- neutro  

---

# 🌍 Simulação de Mundo

O mundo possui **simulação contínua**.

A cada ciclo:

- novas cidades podem surgir
- NPCs aparecem
- facções ganham poder
- quests são criadas
- eventos históricos são registrados

Exemplo de eventos:

```
Cidade fundada: Aldoria
Novo NPC apareceu: mercador
Nova quest: Explore ruínas
Facção surgiu: Ordem da Chama
```

---

# ⚔️ Sistema de Combate

Combate inspirado em **D&D**.

```
rolagem d20
    ↓
checagem de sucesso
    ↓
cálculo de dano
    ↓
estado do inimigo muda
```

Boss possui **fases adaptativas**:

```
HP > 80  → fase 1
HP > 40  → fase 2
HP < 40  → fase 3
```

Cada fase muda o comportamento do inimigo.

---

# 🏰 Dungeons Procedurais

Dungeons são geradas dinamicamente.

Estrutura:

```
salas
armadilhas
monstros
tesouros
```

Exemplo:

```
Dungeon encontrada com 7 salas
```

---

# 🐉 Gerador de Monstros

Monstros são criados proceduralmente.

Tipos possíveis:

```
Goblin
Troll
Hidra
Aranha Gigante
Espectro
```

Cada criatura possui:

```
HP
nível
tipo
dano
```

---

# 🎒 Inventário

Jogadores podem possuir:

```
espada
poções
artefatos
ouro
```

Itens surgem de:

- loot
- exploração
- quests
- eventos

---

# 💾 Memória Persistente

A narrativa é armazenada no servidor.

Endpoint:

```
/api/world/history
```

Mesmo após recarregar a página:

```
história continua
```

Fluxo:

```
jogador escreve
      ↓
motor narrativo responde
      ↓
evento salvo
      ↓
histórico reconstruído
```

---

# 🌐 Interface Web

Interface moderna construída com:

```
TailwindCSS
Django
JavaScript
```

Inclui:

- painel de narrativa
- sistema de combate
- inventário
- estado do mundo
- eventos procedurais

---

# 📡 API

### RPG

```
POST /api/rpg/analisar-cena
POST /api/rpg/combate
```

### Mundo

```
GET /api/world/state
GET /api/world/history
GET /api/world/monster
GET /api/world/dungeon
GET /api/world/faction
GET /api/world/map
```

---

# 🚀 Como Rodar

### 1️⃣ Clonar o repositório

```
git clone https://github.com/seuusuario/procedural-rpg
cd procedural-rpg
```

---

### 2️⃣ Criar ambiente virtual

```
python -m venv venv
```

Linux / Mac

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

---

### 3️⃣ Instalar dependências

```
pip install -r requirements.txt
```

---

### 4️⃣ Rodar servidor

```
python manage.py runserver
```

---

### 5️⃣ Abrir no navegador

```
http://127.0.0.1:8000
```

---

# 📊 Estado do Mundo

O painel mostra a evolução do mundo:

```
Cidades
NPCs
Facções
Quests
Eventos
```

Atualizado automaticamente.

---

# 🔮 Roadmap

Planejado para o projeto:

- mapa procedural explorável
- multiplayer persistente
- economia dinâmica
- NPCs com memória
- guerras entre facções
- narrativa contextual baseada em histórico
- IA que cria quests complexas

Objetivo final:

```
criar um RPG infinito
```

---

# 🧪 Status do Projeto

Projeto **experimental de pesquisa em narrativa procedural**.

Explora:

- inteligência artificial narrativa
- sistemas complexos
- jogos emergentes
- simulação procedural

---

# 📜 Licença

MIT License

---

# 👨‍💻 Autor

<<<<<<< HEAD
Lucas Dourado

Projeto exploratório envolvendo:

- IA narrativa
- simulação procedural
- sistemas emergentes
- design de jogos experimentais
=======
Lucas Dourado  
>>>>>>> 901aea80dab37bc6e55b9ebfe8bc2463173faf3f
