# 🎬 MovieDB - TMDB Desktop Client

![Flet](https://img.shields.io/badge/Flet-0.9.0+-blue) 
![Python](https://img.shields.io/badge/Python-3.7+-green)
![License](https://img.shields.io/badge/License-MIT-orange)

A sleek desktop application for discovering movies and TV shows, powered by the TMDB API with a Netflix-inspired interface.

## ✨ Features

- 🎥 Search movies & TV shows with instant results
- 🔄 Toggle between movie/TV show modes
- 💫 Netflix-style dark theme UI
- 🔍 Detailed view with ratings and overviews
- 🌐 Direct TMDB links for more information
- 🖥️ Native desktop experience with responsive design

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- TMDB API credentials

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lakregcz/MovieDB.git
   cd MovieDB
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Get your TMDB API keys:
   - Register at [TMDB](https://www.themoviedb.org/)
   - Get API key from [Settings](https://www.themoviedb.org/settings/api)
   - Generate read token from [API Tokens](https://www.themoviedb.org/settings/api/request-token)

4. Configure `MovieDB.py`:
   ```python
   API_KEY = "your_api_key_here"
   API_READ_ACCESS_TOKEN = "your_read_access_token_here"
   ```

---

## 🏃 Running the App

**Desktop Mode (Recommended):**
```bash
python MovieDB.py
```

**Web Browser Mode:**
```bash
python MovieDB.py --web
```

---

## 🎮 Usage Guide

| Action | How To |
|--------|--------|
| **Search Content** | Type query and press Enter |
| **Switch Modes** | Click Movies/TV Shows buttons |
| **View Details** | Click any result card |
| **Open TMDB Page** | Click "View on TMDB" in details |
| **Close Details** | Click outside modal or × button |

---

## 🛠️ Project Structure

```
MovieDB/
├── MovieDB.py          # Main application
├── README.md           # Documentation
└── requirements.txt    # Dependencies
```

---

## 📦 Dependencies

| Package | Version |
|---------|---------|
| flet | ≥0.9.0 |
| requests | ≥2.31.0 |

---

## ⚠️ Troubleshooting

**Problem: No results appearing**  
✅ Verify API keys are correct  
✅ Check internet connection  

**Problem: 401 Unauthorized errors**  
✅ Regenerate your API tokens  
✅ Ensure tokens are properly copied  

**Problem: Window not appearing**  
✅ Reinstall Python and Flet  
✅ Run as administrator if needed  

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.  
Note: TMDB API has its own [terms of service](https://www.themoviedb.org/documentation/api/terms-of-use).

---

## 🙏 Acknowledgments

- [The Movie Database](https://www.themoviedb.org/) for their excellent API
- [Flet](https://flet.dev/) team for the amazing Python framework

---

<div align="center">
  <sub>Built with ❤️ by lakregcz</sub>
</div>
```
