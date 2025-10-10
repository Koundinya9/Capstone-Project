# � CEO AI Assistant

### AI-Powered Financial Intelligence Platform

CEO AI Assistant is a sophisticated Streamlit application that provides comprehensive financial analysis and intelligence through advanced AI agents. Designed for executives, investors, analysts, and financial professionals who need quick, accurate, and actionable financial insights.

The platform leverages multiple specialized AI agents working together to analyze financial documents, research companies, assess risks, and provide investment recommendations with professional-grade accuracy.

---
## 📊 Financial Analysis AI Features

* **Multi-Input Analysis:** Analyze companies by name or upload financial documents (PDFs, annual reports, 10-K filings, earnings reports)

* **Comprehensive Analysis Suite:**
    * **Financial Document Analyzer:** Extract and analyze key financial metrics from uploaded documents
    * **Company Research Specialist:** In-depth fundamental analysis of public companies
    * **Financial Ratio Analyst:** Calculate and interpret liquidity, profitability, efficiency, and leverage ratios
    * **Investment Advisor:** Generate buy/sell recommendations with detailed rationale
    * **Risk Assessment Specialist:** Comprehensive risk evaluation across multiple categories
    * **Market Comparison Analyst:** Benchmark companies against industry peers

* **Interactive AI Chat:** Ask follow-up questions about the analysis with context-aware responses

* **Professional Reports:** Generate and download comprehensive analysis reports and investment recommendations

The platform employs a multi-agent AI architecture with specialized financial analysis agents:

* **Financial Document Analyzer:** Extract and interpret key metrics from PDFs, annual reports, and 10-K filings
* **Company Research Specialist:** Comprehensive fundamental analysis of public companies  
* **Financial Ratio Analyst:** Calculate and interpret liquidity, profitability, efficiency, and leverage ratios
* **Investment Advisor:** Generate buy/sell recommendations with detailed investment thesis
* **Risk Assessment Specialist:** Multi-dimensional risk evaluation (financial, operational, market, strategic)
* **Market Comparison Analyst:** Benchmark companies against industry peers and market indices
* **Trend Analysis Agent:** Identify patterns and trajectories in historical financial data

---
## 💡 Key Features

* **Multi-Format Document Support:** Process PDFs, CSV files, and text documents simultaneously
* **Dual Analysis Modes:** Upload financial documents OR research companies by name
* **Interactive AI Chat:** Ask follow-up questions with full context awareness  
* **Professional Reporting:** Generate executive-ready analysis reports and presentations
* **Advanced Visualizations:** Automatic chart generation for CSV financial data
* **Session Management:** Save, organize, and revisit multiple analysis sessions
* **Export Capabilities:** Download comprehensive reports in multiple formats

---
## 💻 Built With

* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Framework:** [CrewAI](https://www.crewai.com/)
* **LLMs:** [Google Gemini](https://ai.google.dev/) & [Groq Llama](https://groq.com/)
* **Core Libraries:** `streamlit`, `crewai`, `langchain-groq`, `langchain-google-genai`, `pypdf`, `streamlit-local-storage`

---
## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

* **Python 3.11:** The application is built and tested with Python 3.11. You can download it from the [official Python website](https://www.python.org/).
* **API Keys:** You will need API keys from both of the following services:
    * [Google AI Studio](https://aistudio.google.com/) for the Gemini API Key.
    * [GroqCloud](https://console.groq.com/) for the Groq API Key.

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/ceo-ai-assistant.git](https://github.com/your-username/ceo-ai-assistant.git)
    cd ceo-ai-assistant
    ```
2.  **Create and activate a virtual environment:**
    ```sh
    # Create the venv
    python3.11 -m venv .venv

    # Activate the venv (macOS/Linux)
    source .venv/bin/activate

    # Or, activate the venv (Windows)
    .\.venv\Scripts\activate
    ```
3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```
4.  **Set up your environment variables:**
    * Create a file named `.env` in the root of your project directory.
    * Add your API keys to the `.env` file as follows:
        ```env
        GEMINI_API_KEY="your_google_api_key_here"
        GROQ_API_KEY="your_groq_api_key_here"
        ```

---
## 📖 Usage

With your virtual environment active, run the following command in your terminal:

```sh
streamlit run Home.py
```

---
### Using CEO AI Assistant

The application features a streamlined 4-tab interface designed for comprehensive financial analysis:

* **📊 Analysis Tab:**  
  Upload financial documents (PDFs, CSVs) or enter company names for research.  
  The AI processes your input and provides initial analysis and insights.  
  Track progress through the analysis pipeline with visual indicators.

* **📈 Key Metrics Tab:**  
  View extracted financial metrics, calculated ratios, and risk assessments.  
  Generate detailed ratio analysis and comprehensive risk evaluation reports.  
  Visualize financial data with automatic chart generation for CSV uploads.

* **💬 AI Chat Tab:**  
  Interactive conversation with context-aware financial analysis AI.  
  Ask follow-up questions about the analysis, request clarifications, or explore specific aspects.  
  Get explanations in plain language or technical detail as needed.

* **📋 Reports Tab:**  
  Generate professional investment recommendations with detailed rationale.  
  Download comprehensive analysis reports in multiple formats.  
  Export chat history and key findings for presentations or documentation.

---
