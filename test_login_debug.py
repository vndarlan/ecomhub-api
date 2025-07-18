from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

def test_login_selectors():
    """Testa os seletores específicos do EcomHub"""
    
    options = Options()
    options.add_argument("--no-sandbox")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        print("🌐 Navegando para EcomHub...")
        driver.get("https://go.ecomhub.app/login")
        time.sleep(5)
        
        # Testar campo email
        try:
            email_field = driver.find_element(By.ID, "input-email")
            print("✅ Campo email encontrado!")
            email_field.send_keys("saviomendesalvess@gmail.com")
            print("✅ Email digitado!")
        except Exception as e:
            print(f"❌ Erro no campo email: {e}")
            
        # Testar campo senha
        try:
            password_field = driver.find_element(By.ID, "input-password")
            print("✅ Campo senha encontrado!")
            password_field.send_keys("Chegou123!")
            print("✅ Senha digitada!")
        except Exception as e:
            print(f"❌ Erro no campo senha: {e}")
            
        # Testar botão login
        try:
            login_button = driver.find_element(By.CSS_SELECTOR, "a[role='button'].btn.tone-default")
            print("✅ Botão login encontrado!")
            print("⏳ Aguardando 3 segundos para clicar...")
            time.sleep(3)
            login_button.click()
            print("✅ Botão clicado!")
            
            # Aguardar redirecionamento
            time.sleep(5)
            print(f"🔗 URL após login: {driver.current_url}")
            
        except Exception as e:
            print(f"❌ Erro no botão login: {e}")
            
        input("⏸️ Pressione Enter para fechar o browser...")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    test_login_selectors()