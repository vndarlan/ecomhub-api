# 🚀 Configuração Manual do Cron no Railway

## Passo a Passo no Painel do Railway

### 1. Acesse seu projeto no Railway

### 2. Na aba lateral, clique em "Cron Jobs"

### 3. Clique em "New Cron Job" ou "Add Cron Job"

### 4. Preencha os campos:

```
Name: Token Sync
Schedule: */2 * * * *
Command: python cron_sync_tokens.py
Service: (selecione seu serviço principal)
```

### 5. Clique em "Add" ou "Create"

## ✅ Verificação

Após criar, você verá na aba "Cron Jobs":
- Nome: Token Sync
- Schedule: */2 * * * * (Every 2 minutes)
- Status: Active
- Last Run: (horário da última execução)
- Next Run: (próxima execução em ~2 minutos)

## 📊 Monitoramento

1. **Ver logs do Cron:**
   - Clique no cron job criado
   - Selecione "View Logs"

2. **Logs esperados:**
```
🔄 CRON JOB - SINCRONIZAÇÃO DE TOKENS
Executado em: 2024-11-08 15:30:00
Obtendo tokens via Selenium...
✅ Login realizado com sucesso!
✅ Tokens obtidos: ['token', 'e_token', 'refresh_token']
✅ CRON JOB CONCLUÍDO COM SUCESSO
```

## 🔧 Troubleshooting

### Se o Cron não executar:
1. Verifique se o comando está correto: `python cron_sync_tokens.py`
2. Confirme que o arquivo `cron_sync_tokens.py` existe no root do projeto
3. Verifique as variáveis de ambiente:
   - `TOKEN_SYNC_ENABLED=true`
   - `ECOMHUB_EMAIL=seu_email`
   - `ECOMHUB_PASSWORD=sua_senha`

### Se der erro de execução:
- Verifique os logs do cron job
- Confirme que as dependências estão instaladas (selenium, etc.)
- Verifique se o Chrome está disponível no container

## 📝 Notas

- O Cron executará a cada 2 minutos
- Tokens do EcomHub expiram em 3 minutos
- Margem de segurança: 1 minuto
- Os logs do cron são separados dos logs do servidor principal