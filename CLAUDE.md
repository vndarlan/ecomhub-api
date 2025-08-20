# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Idioma
Claude deve sempre se comunicar em português brasileiro (PT-BR) ao trabalhar neste projeto.

## Development Commands

### Running the Application
- **Development (local)**: `ENVIRONMENT=local python main.py` (runs on port 8001, visible browser)
- **Production**: `python main.py` (runs headless Chrome, port from ENV or 8001)
- **Docker**: `docker build -t ecomhub . && docker run -p 8001:8001 ecomhub`
- **Testing API directly**: `python test_api_direct.py`

### Installation
```bash
pip install -r requirements.txt
```

### Key Environment Variables
- `ENVIRONMENT=local` - Enables visible Chrome browser for debugging
- `PORT` - Server port (defaults to 8001)

## Architecture Overview

### Core Application Structure
This is a **FastAPI-based web automation service** that uses **Selenium** to scrape EcomHub data and provide effectiveness analytics for e-commerce orders across multiple countries.

**Main Components:**
- `main.py` - FastAPI server with Selenium automation for EcomHub login and data extraction
- `test_api_direct.py` - Testing script for API functionality
- `Dockerfile` + `railway.toml` - Production deployment on Railway platform

### Data Flow Architecture
1. **Authentication**: Selenium logs into EcomHub web interface to obtain session cookies
2. **API Extraction**: Uses authenticated cookies to call EcomHub's internal API directly (`https://api.ecomhub.app/api/orders`)
3. **Data Processing**: Two processing modes:
   - **Total View**: All statuses displayed individually 
   - **Optimized View**: Statuses grouped into categories (Finalizados, Transito, Problemas, etc.)
4. **Multi-country Support**: Handles individual countries or "todos" (all countries) in a single request

### Key Technical Details

**Supported Countries (PAISES_MAP):**
- Spain (164), Croatia (41), Greece (66), Italy (82), Romania (142), Czech Republic (44), Poland (139)
- Special "todos" option processes all countries with country identification in results

**Chrome Driver Configuration:**
- **Local**: Uses ChromeDriverManager, visible browser
- **Production/Railway**: Uses system Chrome with headless mode and specific Railway optimizations

**API Endpoint:** `POST /api/processar-ecomhub/`
- Parameters: `data_inicio` (YYYY-MM-DD), `data_fim` (YYYY-MM-DD), `pais_id` (country ID or "todos")
- Returns: Both total and optimized data views with effectiveness calculations

### Security Note
**Contains hardcoded credentials** in `main.py` lines 39-40:
- `LOGIN_EMAIL = "saviomendesalvess@gmail.com"`
- `LOGIN_PASSWORD = "Chegou123!"`

These should be moved to environment variables for production use.

### Data Processing Logic
The application calculates effectiveness metrics by:
- Extracting product names from nested `ordersItems.productsVariants.products.name`
- Tracking delivery statuses and grouping them into success/failure categories
- Computing effectiveness percentages (delivered/total orders)
- Supporting country-specific analysis when processing "todos" requests