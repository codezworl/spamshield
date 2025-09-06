# 🛡️ SpamGuard AI - Advanced Spam Detection System

A powerful AI-powered spam detection system that can analyze messages and emails for spam content using advanced machine learning algorithms.

## ✨ Features

- 🤖 **AI-Powered Detection**: Advanced pattern recognition and machine learning
- 📧 **Message & Email Support**: Analyze both messages and email content
- 🎯 **Risk Classification**: Safe, Low Risk, Medium Risk, High Risk categories
- 📊 **Detailed Analysis**: Confidence scores, spam scores, and detailed reasons
- 🎨 **Beautiful UI**: Modern dark theme with smooth animations
- 🚀 **Vercel Ready**: Deploy instantly to Vercel
- 📱 **Responsive Design**: Works on all devices

## 🚀 Quick Start

### Local Development

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Navigate to the project directory**:
   ```bash
   cd spamchecker
   ```

3. **Start the development server**:
   ```bash
   vercel dev
   ```

4. **Open your browser** and go to `http://localhost:3000`

5. **Test the API** (optional):
   ```bash
   python test_api.py
   ```

### Deploy to Vercel

1. **Push to GitHub** repository
2. **Connect to Vercel** and import your repository
3. **Deploy** - Vercel will automatically detect the Python API

## 🔧 API Endpoints

### POST `/api/spam-check`
Analyze text for spam content.

**Request Body:**
```json
{
  "text": "Your message or email content here",
  "type": "message" // or "email"
}
```

**Response:**
```json
{
  "success": true,
  "is_spam": false,
  "confidence": 0.95,
  "score": 0.15,
  "category": "safe",
  "reasons": ["No suspicious patterns detected"],
  "message_length": 45,
  "word_count": 8
}
```

### GET `/api/health`
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "AI Spam Checker",
  "version": "1.0.0",
  "success": true
}
```

## 🧠 AI Detection Categories

1. **Financial Scams** - Money offers, investments, crypto schemes
2. **Urgency Tactics** - "Act now", "Limited time" pressure
3. **Suspicious Links** - Shortened URLs, suspicious domains
4. **Personal Info Requests** - Password, SSN, credit card requests
5. **Email Spam Patterns** - Newsletter, promotion patterns
6. **Machine Learning** - Advanced pattern recognition

## 📊 Risk Categories

- **Safe** (0-20%): Legitimate content
- **Low Risk** (20-40%): Some suspicious elements
- **Medium Risk** (40-70%): Likely spam
- **High Risk** (70-100%): Definitely spam

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python 3.9+ (Serverless Functions)
- **Deployment**: Vercel
- **AI**: Custom machine learning algorithms
- **Styling**: Modern CSS with glassmorphism effects

## 📁 Project Structure

```
spamchecker/
├── api/
│   └── spam_check.py      # Python API endpoint
├── index.html             # Main HTML file
├── style.css              # Styling and animations
├── script.js              # Frontend JavaScript
├── vercel.json            # Vercel configuration
├── requirements.txt       # Python dependencies
├── test_api.py           # Local testing script
└── README.md             # This file
```

## 🎨 UI Features

- **Shield Loader**: Unique 2-second loading animation
- **Dark Theme**: Professional purple/blue gradient design
- **Responsive**: Mobile-first responsive design
- **Animations**: Smooth transitions and hover effects
- **Toast Notifications**: User feedback for all actions
- **Real-time Analysis**: Instant spam detection results

## 🔍 Usage Examples

### Basic Message Analysis
```javascript
const response = await fetch('/api/spam-check', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: "Congratulations! You won $1000!",
    type: "message"
  })
});
```

### Email Content Analysis
```javascript
const response = await fetch('/api/spam-check', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: "URGENT: Verify your account now!",
    type: "email"
  })
});
```

## 🚨 Error Handling

The API includes comprehensive error handling:
- Invalid JSON data
- Missing text input
- Server errors
- Network timeouts

## 📱 Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Made by Alyan Shahid**

---

🛡️ **SpamGuard AI** - Protecting you from spam with the power of AI!
