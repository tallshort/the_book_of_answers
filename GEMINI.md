# The Book of Answers - Gemini Context

This document provides Instructional context for Gemini CLI interactions within the "The Book of Answers" project.

## Project Overview
"The Book of Answers" is a minimalist and mystic web application designed to provide guidance to users through a digital oracle experience. The app emphasizes ritual and focus, featuring a "Destiny Lock" mechanism that preserves a user's answer for 30 minutes.

### Main Technologies
- **Frontend**: Vanilla HTML5, CSS3, and JavaScript (ES6+). Uses Canvas for high-resolution social share card generation.
- **Backend**: Python 3.x serverless functions deployed on Vercel (`api/answer.py`).
- **Data**: JSON-based answer repository (`answers.json`) supporting 13 languages.
- **Platform**: Vercel (Hosting, Serverless Functions, Analytics).
- **PWA**: Fully Progressive Web App compatible with offline manifest and standalone mode.

### Architecture
- **API**: A single Python handler in `api/answer.py` manages answer selection and the 30-minute lock using both Cookies and server-side logic.
- **Frontend**: A single-file application (`index.html`) containing the core logic, UI states (Book Cover, Answer Reveal, Share Modal), and Canvas rendering for social sharing.
- **Multi-language**: Managed via a `UI_TEXT` object in the frontend and a standardized schema in `answers.json`.

## Building and Running

### Local Development
To run the project locally with serverless functions support:
```bash
vercel dev
```

### Deployment
- **Staging / Preview**:
  ```bash
  vercel
  ```
- **Production**:
  ```bash
  vercel --prod
  ```

## Development Conventions

### Coding Style
- **HTML/JS**: Maintain the single-file approach for the frontend to preserve minimalist simplicity.
- **CSS**: Use embedded `<style>` tags in `index.html`. Follow the existing mystic aesthetic (dark background, radial gradients, muted gold accent color `#a89f91`).
- **Python**: Use standard library modules (`http.server`, `json`, `random`, `cookies`) where possible to keep the backend lightweight and dependency-free.

### Key Mechanisms
- **Destiny Lock**: Answers are locked for 30 minutes per user (via IP/Cookie and Client-side LocalStorage).
- **Social Sharing**: High-resolution (1080x1920) cards are generated client-side via Canvas to avoid server-side image processing.
- **PWA Interaction**: Functional buttons (like Refresh and Share) are delayed by 2.5s after answer reveal to maintain user focus and mystery.

## Roadmap & TODOs
See `TODO.md` for planned features such as:
- Optional "Ask a Question" input ritual.
- Local history/fate足迹 tracking.
- Haptic feedback and improved mobile interactions.
- Enhanced offline capabilities.
