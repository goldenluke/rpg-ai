# 🧠 RPG AI Multiplayer
### D&D Engine + QWAN Narrative System + Discord Integration

Sistema multiplayer de RPG inspirado em D&D, com:

- ⚔️ Combate estruturado (HP, Mana, Stats)
- 🧠 Motor narrativo QWAN (metaestado dinâmico)
- 🤖 Bot Discord multiplayer
- 🔌 WebSocket em tempo real
- 🏰 Suporte a salas cooperativas
- 🐉 Boss adaptativo
- 📊 Arquitetura escalável

---

# 🌊 Conceito

O RPG AI Multiplayer é um sistema híbrido que combina:

- Mecânica clássica de RPG (D20, atributos, dano)
- Processamento semântico via embeddings
- Metaestado narrativo (QWAN)
- Multiplayer por canal Discord

Cada canal do Discord funciona como uma dungeon independente.

---

# 🧠 QWAN — Quality Without A Name

O sistema narrativo usa embeddings semânticos para calcular o regime narrativo.

### Similaridade Vetorial

Dado um texto do jogador:

$$
\vec{t} = \text{MiniLM}(texto)
$$

E âncoras semânticas:

$$
\vec{a}_{combate}, \vec{a}_{magia}, \vec{a}_{drama}
$$

A similaridade é:

$$
\text{sim}(\vec{t}, \vec{a}) =
\frac{\vec{t} \cdot \vec{a}}
{\|\vec{t}\| \|\vec{a}\|}
$$

---

### Regime Narrativo

O regime é determinado por:

$$
\text{Regime} =
\begin{cases}
\text{Épico} & \text{se } \|\vec{t}\| > \theta \\
\text{Tenso} & \text{se } sim_{combate} > 0.6 \\
\text{Místico} & \text{se } sim_{magia} > 0.6 \\
\text{Calmo} & \text{caso contrário}
\end{cases}
$$

O regime altera:

- Descrição do dano
- Tom da narrativa
- Reação do boss
- Evolução do combate

---

# ⚔️ Sistema de Combate

Baseado em D20.

### Rolagem

$$
R = \text{rand}(1, 20)
$$

$$
Total = R + Modificador
$$

---

### Dano

Se:

$$
Total \geq Defesa
$$

Então:

$$
HP_{inimigo} = HP_{inimigo} - Dano
$$

Mana é consumida conforme:

$$
Mana_{novo} = Mana - Custo_{magia}
$$

---

# 🏰 Multiplayer

Cada canal Discord = 1 sala.

Estrutura interna:

```
ROOMS = {
  channel_id: {
    players: {user_id: session_id},
    turn_order: [],
    current_turn: user_id,
    guild: None
  }
}
```

Turno avança circularmente:

$$
turno_{novo} = (turno_{atual} + 1) \mod n
$$

---

# 🐉 Boss Cooperativo

Cada sala possui:

- HP
- Fases
- Regime adaptativo
- Estado emocional (futuro)

Transição de fase:

$$
\text{Fase 2 se } HP < 70\%
$$

$$
\text{Fase 3 se } HP < 40\%
$$

---

# 🤖 Discord Bot

Comandos disponíveis:

```
/criar nome classe
/narrar texto
/acao tipo
/status
```

### Fluxo:

1. Jogador cria personagem
2. Entra automaticamente na sala (canal)
3. Turnos são controlados
4. Combate cooperativo
5. Narrativa adaptativa via QWAN

---

# 📦 Instalação

## 1️⃣ Clonar projeto

```bash
git clone https://github.com/seuusuario/rpg-ai
cd rpg-ai
```

---

## 2️⃣ Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configurar .env

```
DISCORD_TOKEN=SEU_TOKEN
API_BASE_URL=http://127.0.0.1:8000/api/rpg
```

---

## 5️⃣ Rodar servidor Django

```bash
python manage.py runserver
```

---

## 6️⃣ Rodar Bot Discord

```bash
python bot_main.py
```

---

# 🧩 Estrutura do Projeto

```
rpg-ai/
 ├── api/
 │   ├── engine.py
 │   ├── views.py
 │   ├── consumers.py
 │   ├── routing.py
 │   └── models.py
 ├── bot_main.py
 ├── core/
 │   ├── settings.py
 │   ├── asgi.py
 │   └── urls.py
 ├── templates/
 ├── requirements.txt
 └── README.md
```

---

# 🔌 WebSocket

Conexão multiplayer:

```
ws://localhost:8000/ws/rpg/<room_id>/
```

Permite:

- Broadcast de narrativa
- Chat cooperativo
- Atualização em tempo real
- Boss automático

---

# 📊 Roadmap

- [ ] Persistência em PostgreSQL
- [ ] Redis Channel Layer
- [ ] Sistema de Guildas
- [ ] Boss adaptativo por metaestado
- [ ] Modo PvP
- [ ] Mapa procedural
- [ ] IA emergente multiagente

---

# 🧬 Visão

Este projeto explora:

- Sistemas adaptativos
- Narrativa emergente
- Integração Discord + AI
- Metaestabilidade em jogos cooperativos

Não é apenas um RPG.
É uma arquitetura de narrativa viva.

---

# 🛡 Licença

MIT License

---

# 🌌 Autor

Lucas Dourado  
Medicina | Ciência de Dados | Engenharia Narrativa
