#!/usr/bin/env python
"""
Script Cron para sincronização de tokens no Railway.

Este script é executado pelo Railway Cron a cada 2 minutos
para renovar os tokens do EcomHub.

Railway Cron Configuration:
- Schedule: */2 * * * *  (a cada 2 minutos)
- Command: python cron_sync_tokens.py
"""

import os
import sys
import logging
import json
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Importar funções do main
from main import create_driver, login_ecomhub, get_auth_cookies

def sync_tokens():
    """Executa sincronização única de tokens."""
    logger.info("=" * 60)
    logger.info("🔄 CRON JOB - SINCRONIZAÇÃO DE TOKENS")
    logger.info(f"Executado em: {datetime.now()}")

    driver = None
    try:
        # Obter tokens frescos
        logger.info("Obtendo tokens via Selenium...")
        driver = create_driver(headless=True)

        # Login
        login_success = login_ecomhub(driver)
        if not login_success:
            raise Exception("Falha no login EcomHub")

        # Extrair cookies
        cookies = get_auth_cookies(driver)

        # Extrair headers
        headers = {
            "Accept": "*/*",
            "Accept-Language": "pt-BR,pt;q=0.9",
            "Origin": "https://go.ecomhub.app",
            "Referer": "https://go.ecomhub.app/",
            "User-Agent": driver.execute_script("return navigator.userAgent;"),
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json"
        }

        # Preparar dados
        tokens_data = {
            "cookies": cookies,
            "cookie_string": "; ".join([f"{k}={v}" for k, v in cookies.items()]),
            "headers": headers,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "sync_type": "railway_cron"
        }

        logger.info(f"✅ Tokens obtidos: {list(cookies.keys())}")

        # Enviar para Chegou Hub (se configurado)
        chegou_hub_url = os.getenv("CHEGOU_HUB_WEBHOOK_URL")
        chegou_hub_key = os.getenv("CHEGOU_HUB_API_KEY")

        if chegou_hub_url:
            import requests

            headers_webhook = {"Content-Type": "application/json"}
            if chegou_hub_key:
                headers_webhook["Authorization"] = f"Bearer {chegou_hub_key}"

            try:
                response = requests.post(
                    chegou_hub_url,
                    json=tokens_data,
                    headers=headers_webhook,
                    timeout=10
                )

                if response.status_code in [200, 201, 202]:
                    logger.info(f"✅ Tokens enviados para Chegou Hub")
                else:
                    logger.error(f"❌ Erro ao enviar: Status {response.status_code}")

            except Exception as e:
                logger.error(f"❌ Erro ao enviar para Chegou Hub: {e}")
        else:
            logger.info("ℹ️ Chegou Hub não configurado - tokens obtidos mas não enviados")

        # Opcional: Salvar tokens em algum lugar (Redis, DB, etc)
        # Para que o servidor principal possa usar se necessário

        logger.info("✅ CRON JOB CONCLUÍDO COM SUCESSO")
        return True

    except Exception as e:
        logger.error(f"❌ ERRO NO CRON JOB: {e}")

        # Opcional: Enviar alerta de erro
        alert_webhook = os.getenv("ALERT_WEBHOOK_URL")
        if alert_webhook:
            try:
                import requests
                requests.post(alert_webhook, json={
                    "text": f"❌ Falha no Cron de Tokens: {e}",
                    "timestamp": datetime.utcnow().isoformat()
                }, timeout=5)
            except:
                pass

        return False

    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

if __name__ == "__main__":
    logger.info("Iniciando Cron Job de sincronização...")

    # Verificar se está habilitado
    if not os.getenv("TOKEN_SYNC_ENABLED", "false").lower() == "true":
        logger.info("TOKEN_SYNC_ENABLED=false - Cron job pulado")
        sys.exit(0)

    # Executar sincronização
    success = sync_tokens()

    if success:
        logger.info("✅ Cron job finalizado com sucesso")
        sys.exit(0)
    else:
        logger.error("❌ Cron job finalizado com erro")
        sys.exit(1)