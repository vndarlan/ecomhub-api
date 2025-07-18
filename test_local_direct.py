from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from collections import defaultdict

def test_automation_local():
    """Teste local direto da automação"""
    
    # Configurar Chrome
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # 1. LOGIN
        print("🔐 Fazendo login...")
        driver.get("https://go.ecomhub.app/login")
        time.sleep(3)
        
        email_field = driver.find_element(By.ID, "input-email")
        email_field.send_keys("saviomendesalvess@gmail.com")
        
        password_field = driver.find_element(By.ID, "input-password")
        password_field.send_keys("Chegou123!")
        
        login_button = driver.find_element(By.CSS_SELECTOR, "a[role='button'].btn.tone-default")
        login_button.click()
        
        time.sleep(5)
        print(f"✅ Login OK - URL: {driver.current_url}")
        
        # 2. NAVEGAR PARA PEDIDOS
        print("🌐 Navegando para pedidos...")
        orders_url = "https://go.ecomhub.app/orders?conditions.orders.date.start=2025-07-10&conditions.orders.date.end=2025-07-17&conditions.orders.shippingCountry_id=164&page=0"
        driver.get(orders_url)
        time.sleep(8)
        
        print(f"✅ Página carregada - URL: {driver.current_url}")
        
        # 3. EXTRAIR DADOS
        print("📊 Extraindo dados...")
        rows = driver.find_elements(By.CSS_SELECTOR, "tr.has-rowAction")
        print(f"✅ Encontrou {len(rows)} pedidos")
        
        orders_data = []
        for i, row in enumerate(rows[:5]):  # Só primeiros 5 para teste
            cells = row.find_elements(By.CSS_SELECTOR, "td")
            if len(cells) >= 7:
                order = {
                    'numero_pedido': cells[0].text.strip(),
                    'produto': cells[1].text.strip(),
                    'data': cells[2].text.strip(),
                    'warehouse': cells[3].text.strip(),
                    'pais': cells[4].text.strip(),
                    'preco': cells[5].text.strip(),
                    'status': cells[6].text.strip()
                }
                orders_data.append(order)
                print(f"  {i+1}. {order['produto'][:30]} - {order['status']}")
        
        # 4. PROCESSAR EFETIVIDADE
        print("\n📈 Calculando efetividade...")
        product_counts = defaultdict(lambda: {"Total": 0, "Delivered": 0})
        
        for order in orders_data:
            produto = order['produto'][:20]  # Abreviar nome
            status = order['status']
            
            product_counts[produto]["Total"] += 1
            if status.lower() in ['entregue', 'delivered', 'finalizado']:
                product_counts[produto]["Delivered"] += 1
        
        print("\n📋 RESULTADO:")
        print("-" * 60)
        for produto, counts in product_counts.items():
            total = counts["Total"]
            delivered = counts["Delivered"]
            efetividade = (delivered / total * 100) if total > 0 else 0
            print(f"{produto:25} | {total:3} | {delivered:3} | {efetividade:5.1f}%")
        
        input("\n⏸️ Pressione Enter para fechar...")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        input("⏸️ Pressione Enter para fechar...")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    test_automation_local()