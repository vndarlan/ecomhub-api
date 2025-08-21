# PROMPT PARA IA DO CHEGOU HUB - SISTEMA DE MÉTRICAS DE STATUS

## CONTEXTO
Preciso implementar um sistema de métricas para monitorar o tempo que pedidos ficam em cada status na plataforma EcomHub. O objetivo é identificar pedidos "presos" em determinados status por muito tempo, permitindo ação proativa antes que virem problemas de suporte.

## PROBLEMA A RESOLVER
A API da EcomHub não fornece histórico de mudanças de status dos pedidos, apenas o status atual de cada pedido. Para ter um controle efetivo do tempo que cada pedido fica em cada status, precisamos criar nosso próprio sistema de histórico fazendo sincronizações diárias e detectando mudanças.

## INTEGRAÇÃO COM API EXISTENTE
- **Endpoint disponível:** `POST /api/pedidos-status-tracking/`
- **Mesmo servidor:** Usar a mesma URL base dos outros endpoints do projeto ecomhub-efetividade
- **IMPORTANTE:** A API já filtra e retorna APENAS pedidos com status ativos (não finalizados)
- **Parâmetros de entrada:**
  ```json
  {
    "data_inicio": "2025-08-01",
    "data_fim": "2025-08-20", 
    "pais_id": "164"
  }
  ```
- **Resposta da API:**
  ```json
  {
    "status": "success",
    "pedidos": [apenas pedidos ativos - processing, shipped, issue, etc],
    "total_pedidos": 123,
    "data_sincronizacao": "2025-08-20 14:30:00",
    "pais_processado": "Espanha"
  }
  ```

**Status Ativos Retornados:**
- `processing` - Pedido sendo processado
- `shipped` - Em trânsito com transportadora
- `issue` - Com problemas de entrega
- `returning` - Retornando ao remetente

**Status Ignorados (Otimização):**
- `delivered`, `returned`, `cancelled` - Não retornados pela API

## DADOS IMPORTANTES DE CADA PEDIDO
Cada pedido na resposta contém:
- **id**: Identificador único do pedido (chave primária)
- **status**: Estado atual do pedido ("delivered", "processing", "shipped", etc.)
- **customerName**: Nome do cliente
- **customerEmail**: Email do cliente  
- **customerPhone**: Telefone do cliente
- **createdAt**: Data de criação do pedido
- **updatedAt**: Data da última atualização
- **shopifyOrderNumber**: Número do pedido no Shopify
- **produto_nome**: Nome do produto
- **shippingCountry**: País de entrega
- **price**: Valor do pedido
- **trackingUrl**: URL de rastreamento
- **E muitos outros campos...**

## LÓGICA PRINCIPAL DO SISTEMA

### 1. Estrutura de Dados Necessária
Criar duas entidades principais:

**Pedidos Atuais (Estado Atual):**
- ID do pedido (chave primária)
- Status atual
- Nome do cliente
- Email e telefone
- Data de criação
- Data de última atualização local
- Dados do produto
- País

**Histórico de Status (Mudanças ao Longo do Tempo):**
- ID do registro
- ID do pedido (referência)
- Status anterior
- Status novo
- Data da mudança
- Tempo que ficou no status anterior (em horas/dias)

### 2. Processo de Sincronização Diária
```
TODOS OS DIAS ÀS 8:00 DA MANHÃ:

1. Chamar API /api/pedidos-status-tracking/ 
   - Buscar pedidos dos últimos 30 dias (janela móvel)
   - Para cada país que queremos monitorar

2. Para cada pedido recebido:
   a) Verificar se já existe no banco local
   b) Se NÃO existe: 
      - Inserir como novo pedido
      - Status inicial = status atual
   c) Se JÁ existe:
      - Comparar status atual com status armazenado
      - Se mudou: 
        * Calcular tempo no status anterior
        * Registrar mudança no histórico
        * Atualizar status atual
      - Se não mudou:
        * Apenas atualizar data de última verificação

3. Gerar métricas e alertas baseados nos dados
```

### 3. Cálculo de Tempo em Status
```
Exemplo prático:

Dia 1: João faz pedido → status "pending" (primeira vez vendo)
Dia 2: Sincronização → João ainda "pending" (1 dia em pending)
Dia 3: Sincronização → João agora "processing" 
       → Registrar: ficou 2 dias em "pending"
       → Atualizar status para "processing"
Dia 10: Sincronização → João ainda "processing" (7 dias)
        → GERAR ALERTA: muito tempo em processing
```

### 4. Métricas e Alertas a Implementar

**Alertas por Tempo em Status:**
- 🟡 Alerta Amarelo: > 7 dias no mesmo status
- 🔴 Alerta Vermelho: > 14 dias no mesmo status
- ⚠️ Alerta Crítico: > 21 dias no mesmo status

**Métricas Principais:**
- Lista de pedidos com alertas (ordenado por tempo no status)
- Tempo médio por tipo de status
- Distribuição atual de pedidos por status
- Gráfico de pedidos "presos" por faixa de tempo
- Comparação por país/produto

**Dashboard Principal Deve Mostrar:**
```
🚨 ALERTAS CRÍTICOS
- João Silva (Pedido #16873) - 15 dias em "processing"
- Maria Santos (Pedido #16901) - 12 dias em "shipped" 

📊 DISTRIBUIÇÃO ATUAL
- Processing: 45 pedidos (tempo médio: 3.2 dias)
- Shipped: 32 pedidos (tempo médio: 5.1 dias)
- Delivered: 128 pedidos
- Com Problemas: 8 pedidos

📈 MÉTRICAS DE PERFORMANCE
- Tempo médio total: 8.5 dias (criação → entrega)
- Eficiência de entrega: 87%
- Pedidos problemáticos: 3.2%
```

### 5. Regras de Negócio Importantes

**Status Considerados Problemáticos se Muito Tempo:**
- "processing", "preparing_for_shipping" > 7 dias
- "shipped", "with_courier" > 10 dias
- "out_for_delivery" > 3 dias

**Status Finais (Não Alertar):**
- "delivered" (sucesso)
- "returned", "cancelled" (finalizados)

**Países para Monitorar:**
- 164: Espanha
- 41: Croácia  
- 66: Grécia
- 82: Itália
- 142: Romênia
- 44: República Checa
- 139: Polônia
- "todos": Todos os países

### 6. Funcionalidades do Dashboard

**Página Principal:**
- Cards com alertas críticos
- Gráficos de distribuição de status
- Lista de pedidos com mais tempo no status atual
- Filtros por país, produto, faixa de tempo

**Página de Detalhes do Pedido:**
- Histórico completo de mudanças de status
- Linha do tempo visual
- Dados do cliente e produto
- Link para tracking original

**Página de Configurações:**
- Ajustar limites de tempo para alertas
- Configurar países a monitorar
- Horário da sincronização diária

## EXEMPLO DE FLUXO COMPLETO

```
DIA 1 (12/08):
- João faz pedido #16873 → status "pending"
- Sistema registra: primeira vez vendo João

DIA 2 (13/08):  
- Sincronização 8h: João ainda "pending"
- Sistema calcula: 1 dia em "pending" (OK, sem alerta)

DIA 3 (14/08):
- Sincronização 8h: João agora "processing"
- Sistema registra mudança:
  * João ficou 2 dias em "pending" 
  * Status atual: "processing"
  * Data da mudança: 14/08 8:00

DIA 10 (21/08):
- Sincronização 8h: João ainda "processing"  
- Sistema calcula: 7 dias em "processing"
- 🟡 GERA ALERTA AMARELO: João há 7 dias em processing

DIA 17 (28/08):
- Sincronização 8h: João ainda "processing"
- Sistema calcula: 14 dias em "processing"  
- 🔴 GERA ALERTA VERMELHO: João há 14 dias em processing
- 📧 Notificar equipe de suporte
```

## RESULTADO ESPERADO
Um sistema completo que permite identificar rapidamente pedidos que estão "travados" em algum status, com métricas claras de performance e alertas automáticos para intervenção proativa da equipe de suporte.

O dashboard deve ser intuitivo para uso diário, mostrando imediatamente quais pedidos precisam de atenção e permitindo acompanhar a evolução das métricas ao longo do tempo.