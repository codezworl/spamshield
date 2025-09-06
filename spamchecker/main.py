from flask import Flask, render_template, request, jsonify
import json
import re
from typing import Dict, List, Tuple
import os

# Define the Flask application
app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = 'supersecretkey'  # Needed for flashing messages

class SpamChecker:
    def __init__(self):
        # Enhanced spam patterns with weights
        self.spam_patterns = {
            # Financial spam
            'money_offers': {
                'patterns': [
                    r'\b(?:free|win|earn|make money|get rich|cash|dollars?|money)\b',
                    r'\b(?:investment|profit|return|guaranteed|risk-free)\b',
                    r'\b(?:lottery|prize|winner|congratulations|claim)\b',
                    r'\b(?:bitcoin|crypto|trading|forex|stocks?)\b'
                ],
                'weight': 0.8
            },
            # Urgency and pressure
            'urgency': {
                'patterns': [
                    r'\b(?:urgent|asap|immediately|limited time|act now|hurry)\b',
                    r'\b(?:expires|deadline|last chance|don\'t miss)\b',
                    r'\b(?:click here|call now|order now|buy now)\b'
                ],
                'weight': 0.7
            },
            # Suspicious links and domains
            'suspicious_links': {
                'patterns': [
                    r'https?://(?:bit\.ly|tinyurl|short\.link|t\.co)',
                    r'https?://[a-z0-9-]+\.(?:tk|ml|ga|cf)',
                    r'\b(?:click|link|url|website|site)\b.*https?://'
                ],
                'weight': 0.9
            },
            # Personal information requests
            'personal_info': {
                'patterns': [
                    r'\b(?:password|account|login|verify|confirm)\b',
                    r'\b(?:ssn|social security|credit card|bank account)\b',
                    r'\b(?:personal|private|confidential|sensitive)\b'
                ],
                'weight': 0.8
            },
            # Common spam phrases
            'spam_phrases': {
                'patterns': [
                    r'\b(?:dear friend|valued customer|congratulations)\b',
                    r'\b(?:you have won|you are selected|you qualify)\b',
                    r'\b(?:no obligation|no cost|free trial|free gift)\b',
                    r'\b(?:act now|limited offer|exclusive deal)\b'
                ],
                'weight': 0.6
            },
            # Email-specific spam indicators
            'email_spam': {
                'patterns': [
                    r'\b(?:unsubscribe|opt-out|remove|stop)\b',
                    r'\b(?:newsletter|promotion|offer|deal)\b',
                    r'\b(?:spam|junk|bulk|mass)\b'
                ],
                'weight': 0.5
            }
        }
        
        # Legitimate patterns (reduce spam score)
        self.legitimate_patterns = {
            'patterns': [
                r'\b(?:thank you|please|sorry|hello|hi|greetings)\b',
                r'\b(?:meeting|appointment|schedule|business)\b',
                r'\b(?:family|friend|colleague|team)\b',
                r'\b(?:work|project|task|assignment)\b'
            ],
            'weight': -0.3
        }

    def extract_features(self, text: str) -> Dict[str, any]:
        """Extract features from text for spam detection"""
        text_lower = text.lower()
        
        features = {
            'length': len(text),
            'word_count': len(text.split()),
            'uppercase_ratio': sum(1 for c in text if c.isupper()) / len(text) if text else 0,
            'exclamation_count': text.count('!'),
            'question_count': text.count('?'),
            'number_count': len(re.findall(r'\d+', text)),
            'link_count': len(re.findall(r'https?://', text)),
            'email_count': len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)),
            'phone_count': len(re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)),
            'spam_score': 0.0
        }
        
        return features

    def calculate_spam_score(self, text: str) -> Tuple[float, List[str]]:
        """Calculate spam score and return reasons"""
        text_lower = text.lower()
        spam_score = 0.0
        reasons = []
        
        # Check spam patterns
        for category, data in self.spam_patterns.items():
            for pattern in data['patterns']:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                if matches:
                    spam_score += data['weight'] * len(matches)
                    reasons.append(f"Contains {category.replace('_', ' ')}: {', '.join(matches[:3])}")
        
        # Check legitimate patterns (reduce score)
        for pattern in self.legitimate_patterns['patterns']:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                spam_score += self.legitimate_patterns['weight'] * len(matches)
        
        # Additional heuristics
        features = self.extract_features(text)
        
        # Length-based scoring
        if features['length'] < 10:
            spam_score += 0.2
            reasons.append("Very short message")
        elif features['length'] > 1000:
            spam_score += 0.1
            reasons.append("Very long message")
        
        # Uppercase ratio
        if features['uppercase_ratio'] > 0.3:
            spam_score += 0.3
            reasons.append("Excessive uppercase letters")
        
        # Exclamation marks
        if features['exclamation_count'] > 3:
            spam_score += 0.2
            reasons.append("Too many exclamation marks")
        
        # Links
        if features['link_count'] > 2:
            spam_score += 0.4
            reasons.append("Multiple suspicious links")
        
        # Numbers (potential phone numbers, amounts)
        if features['number_count'] > 5:
            spam_score += 0.2
            reasons.append("Excessive numbers")
        
        # Normalize score to 0-1 range
        spam_score = max(0.0, min(1.0, spam_score))
        
        return spam_score, reasons[:5]  # Return top 5 reasons

    def classify_spam(self, text: str) -> Dict[str, any]:
        """Classify text as spam or not spam"""
        if not text or not text.strip():
            return {
                'is_spam': False,
                'confidence': 0.0,
                'score': 0.0,
                'reasons': ['Empty message'],
                'category': 'empty'
            }
        
        spam_score, reasons = self.calculate_spam_score(text)
        
        # Determine classification
        if spam_score >= 0.7:
            category = 'high_risk'
            is_spam = True
            confidence = spam_score
        elif spam_score >= 0.4:
            category = 'medium_risk'
            is_spam = True
            confidence = spam_score
        elif spam_score >= 0.2:
            category = 'low_risk'
            is_spam = False
            confidence = 1 - spam_score
        else:
            category = 'safe'
            is_spam = False
            confidence = 1 - spam_score
        
        return {
            'is_spam': is_spam,
            'confidence': round(confidence, 2),
            'score': round(spam_score, 2),
            'reasons': reasons,
            'category': category,
            'message_length': len(text),
            'word_count': len(text.split())
        }

# Global spam checker instance
spam_checker = SpamChecker()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/spam-check', methods=['POST'])
def spam_check():
    """API endpoint for spam checking"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        text_type = data.get('type', 'message')
        
        if not text:
            return jsonify({
                'error': 'No text provided',
                'success': False
            }), 400
        
        # Check for spam
        result = spam_checker.classify_spam(text)
        result['type'] = text_type
        result['success'] = True
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'success': False
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Spam Checker',
        'version': '1.0.0',
        'success': True
    })

if __name__ == '__main__':
    app.run(debug=True)
