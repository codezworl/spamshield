#!/usr/bin/env python3
"""
Local development server for SpamGuard AI
Run this to test the spam detection API locally without Vercel
"""

import http.server
import socketserver
import json
import re
import urllib.parse
from typing import Dict, List, Tuple
import math

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

class SpamCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/spam-check':
            try:
                # Get content length
                content_length = int(self.headers['Content-Length'])
                
                # Read the request body
                post_data = self.rfile.read(content_length)
                
                # Parse JSON data
                data = json.loads(post_data.decode('utf-8'))
                
                # Extract text to check
                text = data.get('text', '').strip()
                text_type = data.get('type', 'message')  # 'message' or 'email'
                
                if not text:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    response = {
                        'error': 'No text provided',
                        'success': False
                    }
                    self.wfile.write(json.dumps(response).encode())
                    return
                
                # Check for spam
                result = spam_checker.classify_spam(text)
                result['type'] = text_type
                result['success'] = True
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(result).encode())
                
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {
                    'error': 'Invalid JSON data',
                    'success': False
                }
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {
                    'error': f'Internal server error: {str(e)}',
                    'success': False
                }
                self.wfile.write(json.dumps(response).encode())
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                'error': 'Endpoint not found',
                'success': False
            }
            self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                'status': 'healthy',
                'service': 'AI Spam Checker',
                'version': '1.0.0',
                'success': True
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            # Serve static files
            super().do_GET()

def run_server(port=8000):
    """Run the local development server"""
    print("🛡️ SpamGuard AI - Local Development Server")
    print("=" * 50)
    print(f"Starting server on http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    with socketserver.TCPServer(("", port), SpamCheckHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            print("Thank you for using SpamGuard AI!")

if __name__ == "__main__":
    import sys
    
    # Get port from command line argument or use default
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8000.")
    
    run_server(port)
