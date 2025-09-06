#!/usr/bin/env python3
"""
Test script for the SpamGuard AI API
Run this to test the spam detection locally
"""

import json
import urllib.request
import urllib.parse

def test_spam_api():
    """Test the spam detection API"""
    
    # Test cases
    test_cases = [
        {
            "text": "Congratulations! You have won $1000! Click here to claim your prize now!",
            "type": "message",
            "expected": "spam"
        },
        {
            "text": "Hi, how are you doing today? I hope you're having a great day!",
            "type": "message", 
            "expected": "safe"
        },
        {
            "text": "URGENT: Your account will be closed in 24 hours. Verify your password immediately!",
            "type": "email",
            "expected": "spam"
        },
        {
            "text": "Thank you for your email. I'll get back to you by tomorrow regarding the project.",
            "type": "email",
            "expected": "safe"
        }
    ]
    
    print("🛡️ SpamGuard AI - Local API Test")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}:")
        print(f"Text: {test_case['text'][:50]}...")
        print(f"Type: {test_case['type']}")
        print(f"Expected: {test_case['expected']}")
        
        try:
            # Prepare the request
            data = json.dumps({
                "text": test_case["text"],
                "type": test_case["type"]
            }).encode('utf-8')
            
            # Make the request
            req = urllib.request.Request(
                'http://localhost:8000/api/spam-check',
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if result.get('success'):
                    is_spam = result.get('is_spam', False)
                    confidence = result.get('confidence', 0)
                    category = result.get('category', 'unknown')
                    score = result.get('score', 0)
                    
                    print(f"✅ Result: {'SPAM' if is_spam else 'SAFE'}")
                    print(f"   Category: {category}")
                    print(f"   Confidence: {confidence:.2%}")
                    print(f"   Spam Score: {score:.2%}")
                    
                    # Check if result matches expectation
                    expected_spam = test_case['expected'] == 'spam'
                    if is_spam == expected_spam:
                        print("   ✅ Test PASSED")
                    else:
                        print("   ❌ Test FAILED")
                        
                else:
                    print(f"❌ API Error: {result.get('error', 'Unknown error')}")
                    
        except urllib.error.URLError as e:
            print(f"❌ Connection Error: {e}")
            print("   Make sure the Vercel dev server is running!")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")

def test_health_endpoint():
    """Test the health endpoint"""
    print("\n🏥 Testing Health Endpoint...")
    
    try:
        with urllib.request.urlopen('http://localhost:8000/api/health') as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('success'):
                print("✅ Health check passed!")
                print(f"   Service: {result.get('service', 'Unknown')}")
                print(f"   Version: {result.get('version', 'Unknown')}")
            else:
                print("❌ Health check failed!")
                
    except urllib.error.URLError as e:
        print(f"❌ Health check failed: {e}")
        print("   Make sure the Vercel dev server is running!")

if __name__ == "__main__":
    print("Starting SpamGuard AI API Tests...")
    print("Make sure to run 'vercel dev' in the spamchecker directory first!")
    print()
    
    # Test health endpoint first
    test_health_endpoint()
    
    # Test spam detection
    test_spam_api()
    
    print("\n💡 To run the API locally:")
    print("   Option 1 - With Vercel:")
    print("   1. cd spamchecker")
    print("   2. vercel dev")
    print("   3. python test_api.py")
    print()
    print("   Option 2 - With Python server:")
    print("   1. cd spamchecker")
    print("   2. python local_server.py")
    print("   3. python test_api.py")
