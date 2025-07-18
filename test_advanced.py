# test_advanced.py - Teste mais robusto
import requests
import time
import json

def test_server_connection():
    """Testa se o servidor está rodando"""
    try:
        print("🔍 Testando conexão com servidor...")
        response = requests.get("http://localhost:8001", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor está rodando!")
            print(f"📊 Resposta: {response.json()}")
            return True
        else:
            print(f"❌ Servidor respondeu com status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Servidor não está rodando na porta 8001")
        print("💡 Execute primeiro: python main.py")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_selenium_automation():
    """Testa a automação Selenium"""
    print("\n🤖 Iniciando teste da automação Selenium...")
    
    data = {
        "data_inicio": "2025-07-10", 
        "data_fim": "2025-07-17",
        "pais_id": "164"  # Espanha
    }
    
    print(f"📋 Dados do teste: {json.dumps(data, indent=2)}")
    print("⏳ Enviando requisição... (pode demorar alguns minutos)")
    
    try:
        response = requests.post(
            "http://localhost:8001/api/processar-ecomhub/", 
            json=data,
            timeout=300  # 5 minutos timeout
        )
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Automação executada com sucesso!")
            print(f"📈 Status: {result.get('status')}")
            print(f"📝 Mensagem: {result.get('message')}")
            
            dados = result.get('dados_processados', [])
            stats = result.get('estatisticas', {})
            
            print(f"\n📊 Estatísticas:")
            print(f"   - Total registros: {stats.get('total_registros', 0)}")
            print(f"   - Total produtos: {stats.get('total_produtos', 0)}")
            
            if dados and len(dados) > 0:
                print(f"\n📋 Primeiros 3 resultados:")
                for i, item in enumerate(dados[:3]):
                    print(f"   {i+1}. {item}")
            
            return True
        else:
            print(f"❌ Erro na automação: {response.status_code}")
            try:
                error_data = response.json()
                print(f"📋 Detalhes: {error_data}")
            except:
                print(f"📋 Resposta: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout! A automação demorou mais de 5 minutos")
        return False
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def main():
    print("🚀 TESTE AUTOMAÇÃO ECOMHUB SELENIUM")
    print("=" * 50)
    
    # Teste 1: Conexão com servidor
    if not test_server_connection():
        print("\n💡 SOLUÇÃO:")
        print("1. Abra outro terminal")
        print("2. Execute: set ENVIRONMENT=local (Windows)")
        print("3. Execute: python main.py")
        print("4. Deixe o servidor rodando e execute este teste novamente")
        return
    
    # Teste 2: Automação Selenium
    print("\n" + "=" * 50)
    success = test_selenium_automation()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("✅ A automação está funcionando corretamente")
    else:
        print("❌ TESTE FALHOU")
        print("🔧 Verifique os logs do servidor para mais detalhes")

if __name__ == "__main__":
    main()