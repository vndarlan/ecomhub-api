# 🚀 Deploy no Railway - Sistema de Sincronização de Tokens

## ⚡ Duas Opções de Implementação

### **Opção 1: Railway Cron Job (RECOMENDADO) ✅**

**Vantagens:**
- Execução isolada e independente
- Não afeta o servidor principal
- Melhor para debugging
- Logs separados no Railway
- Escala melhor

**Como funciona:**
```
Railway Cron (a cada 2 minutos)
    ↓
Executa: python cron_sync_tokens.py
    ↓
Obtém tokens via Selenium
    ↓
Envia para Chegou Hub
    ↓
Finaliza
```

### **Opção 2: Thread em Background (JÁ IMPLEMENTADO)**

**Vantagens:**
- Mais simples
- Já está pronto
- Tudo em um único serviço

**Como funciona:**
```
main.py inicia
    ↓
Se TOKEN_SYNC_ENABLED=true
    ↓
Inicia thread em background
    ↓
Thread roda a cada 2 minutos
```

---

## 🎯 **COMO CONFIGURAR CADA OPÇÃO**

### **Para usar OPÇÃO 1 - Cron Job (Recomendado):**

#### 1. No código `main.py`, DESABILITE a thread:
```python
# Comente ou remova estas linhas (linhas 1457-1469):
# if os.getenv("TOKEN_SYNC_ENABLED", "false").lower() == "true":
#     ...thread code...
```

#### 2. No Railway, adicione as variáveis:
```env
ECOMHUB_EMAIL=saviomendesalvess@gmail.com
ECOMHUB_PASSWORD=Chegou123!
TOKEN_SYNC_ENABLED=true
CHEGOU_HUB_WEBHOOK_URL=  # quando tiver
CHEGOU_HUB_API_KEY=       # quando tiver
```

#### 3. O Railway detectará o `railway.json` automaticamente
- Cron job será criado
- Executará a cada 2 minutos
- Você verá nos logs: "Cron: Token Sync - A cada 2 minutos"

---

### **Para usar OPÇÃO 2 - Thread (Já pronto):**

#### 1. Delete o arquivo `railway.json` (ou renomeie)

#### 2. Mantenha o código atual em `main.py` (linhas 1457-1469)

#### 3. No Railway, adicione as variáveis:
```env
ECOMHUB_EMAIL=saviomendesalvess@gmail.com
ECOMHUB_PASSWORD=Chegou123!
TOKEN_SYNC_ENABLED=true
TOKEN_DURATION_MINUTES=3
SYNC_INTERVAL_MINUTES=2
CHEGOU_HUB_WEBHOOK_URL=  # quando tiver
CHEGOU_HUB_API_KEY=       # quando tiver
```

---

## 📊 **COMPARAÇÃO**

| Aspecto | Cron Job | Thread |
|---------|----------|--------|
| **Isolamento** | ✅ Processo separado | ❌ Mesmo processo |
| **Logs** | ✅ Separados | ❌ Misturados |
| **Recursos** | ✅ Libera após executar | ❌ Sempre em memória |
| **Debugging** | ✅ Mais fácil | ❌ Mais difícil |
| **Falhas** | ✅ Não afeta servidor | ❌ Pode afetar |
| **Railway** | ✅ Nativo | ⚠️ Funciona mas não ideal |

---

## 🔍 **MONITORAMENTO NO RAILWAY**

### Com Cron Job:
```
Railway Dashboard
├── Services
│   └── ecomhub-api (servidor principal)
└── Crons
    └── Token Sync - A cada 2 minutos
        ├── Last run: 2 min ago ✅
        ├── Next run: in 30 seconds
        └── Logs (isolados)
```

### Com Thread:
```
Railway Dashboard
└── Services
    └── ecomhub-api
        └── Logs (tudo misturado)
            ├── [FastAPI] Request logs...
            ├── [Token Sync] Sincronização...
            └── [FastAPI] More requests...
```

---

## 📝 **MINHA RECOMENDAÇÃO**

Use **Cron Job** porque:

1. **Tokens de 3 minutos** são críticos - se falhar, você tem logs claros
2. **Selenium pode travar** - não afetará o servidor principal
3. **Railway foi feito para isso** - cron jobs são nativos
4. **Mais profissional** - separação de responsabilidades

---

## 🚨 **IMPORTANTE**

Independente da opção escolhida:

1. **SEMPRE configure as credenciais** como variáveis de ambiente
2. **REMOVA do hardcode** em `main.py` (linhas 63-64)
3. **Monitore os logs** nas primeiras horas
4. **Considere SYNC_INTERVAL_MINUTES=1** se tiver problemas (renovação a cada minuto)

---

## ✅ **CHECKLIST PARA DEPLOY**

- [ ] Escolher: Cron Job ou Thread
- [ ] Adicionar variáveis no Railway
- [ ] Fazer commit e push para GitHub
- [ ] Railway faz deploy automático
- [ ] Verificar logs
- [ ] Testar endpoint `/api/auth`
- [ ] Confirmar renovação a cada 2 min

---

## 🆘 **TROUBLESHOOTING**

### "Tokens expirando antes da renovação"
→ Mude para `SYNC_INTERVAL_MINUTES=1`

### "Cron não está executando"
→ Verifique se `railway.json` está na raiz
→ Verifique se `TOKEN_SYNC_ENABLED=true`

### "Thread não iniciou"
→ Verifique logs do deploy
→ Confirme que linha 1457-1469 estão ativas

### "Selenium failing"
→ Normal às vezes, tem retry automático
→ Se persistir, verifique credenciais