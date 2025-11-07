# 🚀 DEPLOY COM RAILWAY CRON - GUIA RÁPIDO

## ✅ **STATUS: PRONTO PARA DEPLOY**

Todas as configurações foram feitas para usar **Railway Cron Job** em vez de thread.

---

## 📋 **CHECKLIST PARA DEPLOY**

### 1️⃣ **Adicionar Variáveis no Railway Dashboard**

```env
# OBRIGATÓRIAS
ECOMHUB_EMAIL=saviomendesalvess@gmail.com
ECOMHUB_PASSWORD=Chegou123!
TOKEN_SYNC_ENABLED=true

# OPCIONAIS (adicionar quando Chegou Hub estiver pronto)
CHEGOU_HUB_WEBHOOK_URL=
CHEGOU_HUB_API_KEY=
```

### 2️⃣ **Fazer Commit e Push**

```bash
git add .
git commit -m "feat: add railway cron job for token sync"
git push
```

### 3️⃣ **Railway vai detectar automaticamente:**
- ✅ `railway.json` com configuração do cron
- ✅ Cron executará `python cron_sync_tokens.py` a cada 2 minutos
- ✅ Logs separados para o cron job

---

## 🔍 **O QUE FOI CONFIGURADO**

### **Arquivos Modificados:**

| Arquivo | Mudança |
|---------|---------|
| `main.py` | Thread comentada (linhas 1456-1472) |
| `main.py` | Credenciais agora usam variáveis de ambiente |
| `cron_sync_tokens.py` | **NOVO** - Script que o cron executa |
| `railway.json` | **NOVO** - Configura cron no Railway |

### **Como Funciona:**

```
Railway Cron (*/2 * * * *)
    ↓ a cada 2 minutos
Executa: python cron_sync_tokens.py
    ↓
Login via Selenium (15-20 seg)
    ↓
Obtém tokens frescos
    ↓
Envia para Chegou Hub (se configurado)
    ↓
Finaliza
```

---

## 📊 **MONITORAMENTO NO RAILWAY**

Após o deploy, você verá:

### **Na aba Services:**
```
ecomhub-api (Running) ✅
└── Logs do servidor principal
```

### **Na aba Cron Jobs:**
```
Token Sync - A cada 2 minutos
├── Schedule: */2 * * * *
├── Last run: 2 minutes ago ✅
├── Next run: in 45 seconds
└── View Logs → (logs isolados do cron)
```

---

## 🔍 **LOGS ESPERADOS**

### **No Cron Job (a cada 2 min):**
```
🔄 CRON JOB - SINCRONIZAÇÃO DE TOKENS
Executado em: 2024-11-07 15:30:00
Obtendo tokens via Selenium...
✅ Login realizado com sucesso!
✅ Tokens obtidos: ['token', 'e_token', 'refresh_token']
ℹ️ Chegou Hub não configurado - tokens obtidos mas não enviados
✅ CRON JOB CONCLUÍDO COM SUCESSO
```

### **No Servidor Principal:**
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

---

## ⚡ **TIMELINE DE EXECUÇÃO**

```
00:00:00 - Cron executa → Obtém tokens (válidos por 3 min)
00:02:00 - Cron executa → Obtém tokens (válidos por 3 min)
00:04:00 - Cron executa → Obtém tokens (válidos por 3 min)
00:06:00 - Cron executa → Obtém tokens (válidos por 3 min)
... continua 24/7
```

**Margem de segurança:** 1 minuto (tokens duram 3, renovamos a cada 2)

---

## 🚨 **TROUBLESHOOTING**

### **"Cron não está executando"**
- Verifique se `TOKEN_SYNC_ENABLED=true` nas variáveis
- Verifique logs do cron job no Railway

### **"Tokens expirando"**
- Considere mudar cron para `* * * * *` (a cada 1 minuto)
- Edite `railway.json` → `schedule: "* * * * *"`

### **"Login falhando"**
- Verifique credenciais nas variáveis do Railway
- Verifique se EcomHub não mudou interface

### **"Chegou Hub não recebe tokens"**
- Configure `CHEGOU_HUB_WEBHOOK_URL` e `CHEGOU_HUB_API_KEY`
- Verifique logs do cron para ver se está enviando

---

## ✅ **VANTAGENS DO CRON**

| Aspecto | Benefício |
|---------|-----------|
| **Isolamento** | Não afeta servidor principal |
| **Logs** | Separados e fáceis de debugar |
| **Recursos** | Só usa quando executa |
| **Falhas** | Não derruba a API |
| **Railway** | Integração nativa |

---

## 📝 **PRÓXIMOS PASSOS**

1. **Deploy no Railway** (commit + push)
2. **Verificar logs** do cron após 2 minutos
3. **Testar endpoint** `/api/auth` para confirmar
4. **Configurar Chegou Hub** quando estiver pronto
5. **Monitorar** por 24h para garantir estabilidade

---

## 🎯 **RESUMO FINAL**

✅ Thread desabilitada no main.py
✅ Cron job configurado no railway.json
✅ Script cron_sync_tokens.py pronto
✅ Credenciais usando variáveis de ambiente
✅ Documentação completa

**PRONTO PARA DEPLOY!** 🚀