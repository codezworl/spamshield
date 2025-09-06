// DOM Elements
const messageInput = document.getElementById("message-input");
const checkMessageButton = document.getElementById("check-message-btn");
const resultContainer = document.getElementById("result-container");
const loadingOverlay = document.getElementById("loading-overlay");
const loadingSubtitle = document.getElementById("loading-subtitle");
const appContainer = document.getElementById("app-container");
const toastContainer = document.getElementById("toast-container");
const inputTypeRadios = document.querySelectorAll('input[name="input-type"]');

// Global Variables
let isChecking = false;

// Loading messages for typewriter effect
const loadingMessages = [
    "Initializing AI spam detection...",
    "Loading machine learning models...",
    "Made by Alyan Shahid",
    "Ready to analyze!"
];

// Typewriter Effect
const typewriterEffect = (element, text, speed = 50) => {
    return new Promise((resolve) => {
        element.textContent = '';
        let i = 0;
        
        const timer = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(timer);
                resolve();
            }
        }, speed);
    });
};

// Show Loading Screen
const showLoading = () => {
    if (loadingOverlay) {
        loadingOverlay.classList.add('show');
    }
};

// Hide Loading Screen
const hideLoading = () => {
    if (loadingOverlay) {
        loadingOverlay.classList.remove('show');
    }
};

// Show Initial Loader - 2 second loader
const showInitialLoader = async () => {
    console.log('Starting 2-second loader...');
    
    showLoading();
    
    for (let i = 0; i < loadingMessages.length; i++) {
        if (loadingSubtitle) {
            await typewriterEffect(loadingSubtitle, loadingMessages[i], 60);
            await new Promise(resolve => setTimeout(resolve, 400));
        }
    }
    
    await new Promise(resolve => setTimeout(resolve, 200));
    
    console.log('Hiding loader...');
    hideLoading();
};

// Show Toast Message
const showToast = (message, type = 'success') => {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        info: 'fas fa-info-circle'
    };
    
    toast.innerHTML = `
        <i class="${icons[type]}"></i>
        <span>${message}</span>
    `;
    
    if (toastContainer) {
        toastContainer.appendChild(toast);
        
        setTimeout(() => toast.classList.add('show'), 100);
        
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 3000);
    }
};

// Get API URL (works for both local and Vercel)
const getApiUrl = () => {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        // Check if we're on port 8000 (Python server) or 3000 (Vercel)
        if (window.location.port === '8000') {
            return 'http://localhost:8000/api/spam-check';
        }
        return 'http://localhost:3000/api/spam-check';
    }
    return '/api/spam-check';
};

// Check Spam using AI API
const checkSpamWithAI = async (text, type = 'message') => {
    try {
        const response = await fetch(getApiUrl(), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                type: type
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error checking spam:', error);
        throw error;
    }
};

// Display Results
const displayResults = (result) => {
    if (!resultContainer) return;

    const { is_spam, confidence, score, reasons, category, message_length, word_count } = result;

    let statusClass = 'safe';
    let statusIcon = 'fas fa-shield-check';
    let statusText = 'Safe Message';
    let statusDescription = 'This message appears to be legitimate.';

    if (category === 'low_risk') {
        statusClass = 'low-risk';
        statusIcon = 'fas fa-shield-alt';
        statusText = 'Low Risk';
        statusDescription = 'This message has some suspicious elements but appears mostly safe.';
    } else if (category === 'medium_risk') {
        statusClass = 'medium-risk';
        statusIcon = 'fas fa-exclamation-triangle';
        statusText = 'Medium Risk';
        statusDescription = 'This message contains several suspicious elements and may be spam.';
    } else if (category === 'high_risk') {
        statusClass = 'high-risk';
        statusIcon = 'fas fa-shield-virus';
        statusText = 'High Risk';
        statusDescription = 'This message is very likely to be spam or malicious.';
    }

    resultContainer.innerHTML = `
        <div class="result-content">
            <div class="result-header ${statusClass}">
                <i class="${statusIcon}"></i>
                <span>${statusText}</span>
            </div>
            
            <div class="result-stats">
                <div class="stat-item">
                    <div class="stat-label">Confidence</div>
                    <div class="stat-value">${Math.round(confidence * 100)}%</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Spam Score</div>
                    <div class="stat-value">${Math.round(score * 100)}%</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Message Length</div>
                    <div class="stat-value">${message_length}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Word Count</div>
                    <div class="stat-value">${word_count}</div>
                </div>
            </div>
            
            <div class="result-reasons">
                <div class="reasons-title">Analysis Details:</div>
                <p style="color: var(--text-secondary); margin-bottom: 1rem;">${statusDescription}</p>
                ${reasons.length > 0 ? `
                    <div class="reasons-title">Detected Issues:</div>
                    <ul class="reasons-list">
                        ${reasons.map(reason => `
                            <li class="reason-item">
                                <i class="fas fa-exclamation-circle"></i>
                                <span>${reason}</span>
                            </li>
                        `).join('')}
                    </ul>
                ` : `
                    <div class="reasons-title">No suspicious patterns detected</div>
                `}
            </div>
        </div>
    `;
};

// Handle Spam Check
const handleSpamCheck = async () => {
    if (isChecking) return;

    const text = messageInput.value.trim();
    if (!text) {
        showToast('Please enter a message to check', 'error');
        return;
    }

    if (text.length < 3) {
        showToast('Please enter a longer message for better analysis', 'error');
    return;
  }

    try {
        isChecking = true;
        checkMessageButton.disabled = true;
        checkMessageButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';

        // Get selected input type
        const selectedType = document.querySelector('input[name="input-type"]:checked').value;

        // Show loading state
        resultContainer.innerHTML = `
            <div class="result-placeholder">
                <i class="fas fa-spinner fa-spin"></i>
                <p>Analyzing message with AI...</p>
            </div>
        `;

        // Call AI API
        const result = await checkSpamWithAI(text, selectedType);

        if (result.success) {
            displayResults(result);
            
            // Show appropriate toast
            if (result.is_spam) {
                showToast(`Spam detected with ${Math.round(result.confidence * 100)}% confidence`, 'error');
            } else {
                showToast(`Message appears safe with ${Math.round(result.confidence * 100)}% confidence`, 'success');
            }
        } else {
            throw new Error(result.error || 'Unknown error occurred');
        }

    } catch (error) {
        console.error('Error:', error);
        
        resultContainer.innerHTML = `
            <div class="result-placeholder">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Error analyzing message. Please try again.</p>
            </div>
        `;
        
        showToast('Failed to analyze message. Please try again.', 'error');
    } finally {
        isChecking = false;
        checkMessageButton.disabled = false;
        checkMessageButton.innerHTML = `
            <span class="btn-text">Analyze with AI</span>
            <span class="btn-icon">
                <i class="fas fa-search"></i>
            </span>
        `;
    }
};

// Event Listeners
const initializeEventListeners = () => {
    // Check button
    if (checkMessageButton) {
        checkMessageButton.addEventListener('click', handleSpamCheck);
    }

    // Enter key on textarea
    if (messageInput) {
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                handleSpamCheck();
            }
        });
    }

    // Input type change
    inputTypeRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            const type = radio.value;
            const placeholder = type === 'email' 
                ? 'Enter email content here...' 
                : 'Enter your message here...';
            
            if (messageInput) {
                messageInput.placeholder = placeholder;
            }
        });
    });
};

// Initialize Application
const initializeApp = () => {
    console.log('Initializing SpamGuard AI...');
    
    initializeEventListeners();
    showInitialLoader();
};

// Start the application when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeApp);