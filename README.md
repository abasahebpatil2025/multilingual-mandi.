# Multilingual Mandi

A Streamlit-based web application that serves as a linguistic bridge for local agricultural traders, enabling seamless communication and negotiation between buyers and sellers across different languages.

## Features

- **Multi-language Support**: Supports Marathi, Hindi, and English with real-time translation
- **Market Price Discovery**: Current market rates for agricultural crops
- **AI-Powered Negotiation**: Intelligent negotiation assistance using Google Gemini AI
- **Secure Configuration**: Environment-based API key management

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd multilingual-mandi
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google Gemini API key
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Configuration

The application requires a Google Gemini API key. Get your API key from [Google AI Studio](https://ai.google.dev/) and add it to your `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

## Project Structure

```
multilingual-mandi/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration management
├── gemini_client.py      # Google Gemini AI client
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── services/            # Business logic services
├── models/              # Data models
└── pages/               # Streamlit page components
```

## Development Status

This project is currently under development. Core functionality is being implemented incrementally:

- [x] Task 1: Project structure and configuration management
- [ ] Task 2: Google Gemini AI client integration
- [ ] Task 3: Translation service layer
- [ ] Task 4: Market rate system
- [ ] Task 5: Negotiation assistant
- [ ] Task 6: Streamlit user interface
- [ ] Task 7: Integration and error handling
- [ ] Task 8: Documentation and project setup

## License

This project is licensed under the MIT License - see the LICENSE file for details.