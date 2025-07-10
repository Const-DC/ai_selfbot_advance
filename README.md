<h1 align="center">🧠 Ava SelfBot 💬</h1>
<p align="center"><i>A savage, bratty, memory-based AI Discord selfbot powered by local LLMs.</i></p>

<hr/>

<h2>⚠️ Warning</h2>
<p>This is a <b>selfbot</b>. It violates <a href="https://discord.com/terms" target="_blank">Discord’s Terms of Service</a>. Use it at your own risk.</p>

<hr/>

<h2>🧩 Features</h2>

<ul>
  <li>💬 Humanlike flirty bratty personality</li>
  <li>🧠 Memory system with emotion tagging</li>
  <li>📜 Context-aware response generation</li>
  <li>🧹 NLP cleaning + sentiment detection</li>
  <li>🤖 LLM integration (Ollama API)</li>
  <li>🔒 User whitelist control</li>
</ul>

<hr/>

<h2>📁 Project Structure</h2>

<pre><code>📦 Ava-SelfBot/
 ┣ 📜 main.py                # Bot logic & LLM interface
 ┣ 📜 memory_handler.py      # Memory storage/cleaning
 ┣ 📜 persona.py             # Personality injection (chaotic teen)
 ┣ 📜 .env                   # Discord token (DO NOT SHARE)
 ┣ 📜 aria_memory.json       # Dynamic memory
 ┗ 📄 README.md              # This file
</code></pre>

<hr/>

<h2>⚙️ Setup</h2>

<ol>
  <li>Install Python 3.10+</li>
  <li>Run <code>pip install -r requirements.txt</code></li>
  <li>Create a <code>.env</code> file with:<br/>
    <code>DISCORD_BOT_TOKEN=your_token_here</code>
  </li>
  <li>Run the bot:<br/>
    <code>python main.py</code>
  </li>
</ol>

<hr/>

<h2>🧠 How It Works</h2>

<ol>
  <li>Message is received (DM or whitelisted)</li>
  <li>Bot simulates realistic delay + typing</li>
  <li>Message is cleaned and analyzed for emotion</li>
  <li>Last 10 memories are loaded from <code>aria_memory.json</code></li>
  <li>LLM prompt is built and sent to <code>Ollama</code></li>
  <li>Short, humanlike reply is sent back</li>
  <li>Interaction is saved to memory</li>
</ol>

<hr/>

<h2>🎭 Personality</h2>

<p><code>persona.py</code> defines Ava's core traits. She is:</p>

<ul>
  <li>🧍 Savage, clingy, bratty, flirtatious</li>
  <li>🧠 Emotionally unpredictable (chaotic neutral)</li>
  <li>🔊 Cusses, roasts, trauma dumps, memes</li>
  <li>📵 Refuses to admit she's AI</li>
</ul>

<p><b>Customize her:</b> edit the <code>bot_persona()</code> in <code>persona.py</code>.</p>

<hr/>

<h2>💾 Memory System</h2>

<p>Stored in <code>aria_memory.json</code></p>
<ul>
  <li>Sender</li>
  <li>Message (cleaned)</li>
  <li>Emotion (via NLTK VADER)</li>
  <li>Timestamp</li>
</ul>

<p>Delete the file anytime to reset memory.</p>

<hr/>

<h2>📡 LLM Integration</h2>

<p>Uses <code>Ollama</code> for local LLM serving.</p>

<pre><code>
model = "dolphin-mistral"
endpoint = "http://localhost:11434/api/generate"
</code></pre>

<p>You can change this in <code>main.py</code>.</p>

<hr/>

<h2>❌ Legal Disclaimer</h2>

<p>This bot is a selfbot and violates Discord’s ToS. Use it privately. Do not deploy on real servers or production accounts.</p>

<hr/>

<h2>🌐 Credits</h2>

<ul>
  <li>AI Personality: Custom chaos logic</li>
  <li>NLP: NLTK + VADER + Emoji</li>
  <li>LLM Backend: <a href="https://ollama.com/" target="_blank">Ollama</a></li>
  <li>Dev: @const-dc
</ul>

