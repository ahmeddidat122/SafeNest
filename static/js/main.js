// ===== SAFENEST MAIN FUNCTIONALITY =====

// Theme management
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);

    // Update theme toggle icon
    const icon = document.querySelector('.theme-toggle i');
    icon.className = newTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';

    showNotification(`Switched to ${newTheme} theme`, 'success');
}

// ===== NAVIGATION FUNCTIONALITY =====

// Mobile menu toggle
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const isOpen = navMenu.classList.contains('mobile-open');

    if (isOpen) {
        navMenu.classList.remove('mobile-open');
        mobileToggle.innerHTML = '<i class="fas fa-bars"></i>';
    } else {
        navMenu.classList.add('mobile-open');
        mobileToggle.innerHTML = '<i class="fas fa-times"></i>';
    }
}

// Enhanced dropdown functionality
function initializeDropdowns() {
    const dropdowns = document.querySelectorAll('.nav-dropdown');

    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.nav-dropdown-toggle');
        const menu = dropdown.querySelector('.nav-dropdown-menu');
        let timeout;

        // Mouse events for desktop
        dropdown.addEventListener('mouseenter', () => {
            clearTimeout(timeout);
            menu.style.opacity = '1';
            menu.style.visibility = 'visible';
            menu.style.transform = 'translateY(0)';
        });

        dropdown.addEventListener('mouseleave', () => {
            timeout = setTimeout(() => {
                menu.style.opacity = '0';
                menu.style.visibility = 'hidden';
                menu.style.transform = 'translateY(-10px)';
            }, 150);
        });

        // Click events for mobile
        toggle.addEventListener('click', (e) => {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                const isOpen = menu.style.opacity === '1';

                // Close all other dropdowns
                dropdowns.forEach(otherDropdown => {
                    if (otherDropdown !== dropdown) {
                        const otherMenu = otherDropdown.querySelector('.nav-dropdown-menu');
                        otherMenu.style.opacity = '0';
                        otherMenu.style.visibility = 'hidden';
                        otherMenu.style.transform = 'translateY(-10px)';
                    }
                });

                // Toggle current dropdown
                if (isOpen) {
                    menu.style.opacity = '0';
                    menu.style.visibility = 'hidden';
                    menu.style.transform = 'translateY(-10px)';
                } else {
                    menu.style.opacity = '1';
                    menu.style.visibility = 'visible';
                    menu.style.transform = 'translateY(0)';
                }
            }
        });
    });
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ===== AI ASSISTANT PAGE FUNCTIONALITY =====

let chatHistory = [];
let isTyping = false;

// Initialize AI Assistant (for dedicated page)
function initializeAIAssistant() {
    if (document.getElementById('ai-assistant-container')) {
        setupVoiceRecognition();
        setupChatEventListeners();
        addWelcomeMessage();
    }
}

// Add welcome message to AI Assistant page
function addWelcomeMessage() {
    const welcomeMessage = `Hello! I'm your SafeNest AI Assistant. I can help you with:

🏠 **Smart Home Control**
• Control lights, temperature, and devices
• Monitor energy usage and optimization
• Manage security systems and alerts

🏗️ **Architecture & Design**
• Generate floor plans and 3D models
• Recommend materials and layouts
• Building code compliance assistance

🤖 **Automation & Intelligence**
• Set up automated routines
• Voice and gesture commands
• Predictive analytics and suggestions

How can I assist you today?`;

    addMessageToChat(welcomeMessage, 'bot');
}

// Setup voice recognition for AI Assistant page
function setupVoiceRecognition() {
    const voiceBtn = document.getElementById('voiceBtn');
    if (!voiceBtn) return;

    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = function() {
            voiceBtn.classList.add('listening');
            voiceBtn.innerHTML = '<i class="fas fa-stop"></i>';
        };

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            const chatInput = document.getElementById('chatInput');
            if (chatInput) {
                chatInput.value = transcript;
                sendMessage();
            }
        };

        recognition.onend = function() {
            voiceBtn.classList.remove('listening');
            voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        };

        recognition.onerror = function(event) {
            showNotification('Voice recognition error: ' + event.error, 'error');
            voiceBtn.classList.remove('listening');
            voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        };

        voiceBtn.addEventListener('click', function() {
            if (this.classList.contains('listening')) {
                recognition.stop();
            } else {
                recognition.start();
            }
        });
    } else {
        voiceBtn.style.display = 'none';
    }
}

// Setup chat event listeners for AI Assistant page
function setupChatEventListeners() {
    const chatInput = document.getElementById('chatInput');
    if (!chatInput) return;

    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    chatInput.addEventListener('input', function() {
        // Show typing indicator to bot
        if (this.value.length > 0) {
            // Could add typing indicator here
        }
    });
}

// Initialize theme and all functionality
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.body.setAttribute('data-theme', savedTheme);

    // Initialize all functionality
    initializeDropdowns();
    initializeSmoothScrolling();
    initializeAIAssistant(); // Initialize AI Assistant for dedicated page
    initializeCallToActionButtons();

    // Mobile menu toggle event
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    if (mobileToggle) {
        mobileToggle.addEventListener('click', toggleMobileMenu);
    }

    // Gesture recognition (basic implementation)
    let gestureStartX, gestureStartY;

    document.addEventListener('touchstart', function(e) {
        gestureStartX = e.touches[0].clientX;
        gestureStartY = e.touches[0].clientY;
    });

    document.addEventListener('touchend', function(e) {
        const gestureEndX = e.changedTouches[0].clientX;
        const gestureEndY = e.changedTouches[0].clientY;

        const deltaX = gestureEndX - gestureStartX;
        const deltaY = gestureEndY - gestureStartY;

        // Swipe gestures
        if (Math.abs(deltaX) > 100) {
            if (deltaX > 0) {
                // Swipe right - toggle lights
                toggleAllLights();
            } else {
                // Swipe left - activate security
                activateSecurityMode();
            }
        }

        // Vertical swipes
        if (Math.abs(deltaY) > 100) {
            if (deltaY < 0) {
                // Swipe up - open chat
                toggleChat();
            }
        }
    });
});

// ===== AI ASSISTANT PAGE CHAT FUNCTIONALITY =====

// Focus on chat input (for AI Assistant page)
function focusChatInput() {
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.focus();
    }
}

// Send message to AI
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (!message) return;

    // Add user message to chat
    addMessageToChat(message, 'user');
    input.value = '';

    // Show typing indicator
    showTypingIndicator();

    try {
        // Send to AI backend
        const response = await fetch('/api/ai/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                message: message,
                history: chatHistory.slice(-10) // Send last 10 messages for context
            })
        });

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator();

        if (data.success) {
            // Add AI response to chat
            addMessageToChat(data.response, 'bot');

            // Execute any actions if suggested
            if (data.actions) {
                executeAIActions(data.actions);
            }
        } else {
            addMessageToChat('Sorry, I encountered an error. Please try again.', 'bot');
        }
    } catch (error) {
        removeTypingIndicator();
        addMessageToChat('Sorry, I\'m having trouble connecting. Please check your internet connection.', 'bot');
        console.error('Chat error:', error);
    }
}

// Add message to chat interface (AI Assistant page)
function addMessageToChat(message, sender) {
    const messagesContainer = document.getElementById('chatMessages');
    if (!messagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const timestamp = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

    // Format message with line breaks and markdown-like formatting
    const formattedMessage = message
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>');

    if (sender === 'user') {
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${formattedMessage}</p>
                <span class="message-time">${timestamp}</span>
            </div>
            <div class="message-avatar">
                <i class="fas fa-user"></i>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-shield-alt"></i>
            </div>
            <div class="message-content">
                <div>${formattedMessage}</div>
                <span class="message-time">${timestamp}</span>
            </div>
        `;
    }

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // Add to chat history
    chatHistory.push({
        message: message,
        sender: sender,
        timestamp: new Date().toISOString()
    });

    // Keep only last 50 messages in history
    if (chatHistory.length > 50) {
        chatHistory = chatHistory.slice(-50);
    }
}

// Show typing indicator
function showTypingIndicator() {
    if (isTyping) return;

    isTyping = true;
    const messagesContainer = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.id = 'typing-indicator';

    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-shield-alt"></i>
        </div>
        <div class="message-content">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;

    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Remove typing indicator
function removeTypingIndicator() {
    isTyping = false;
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Quick action buttons for AI Assistant page
function quickAction(action) {
    const actions = {
        'lights': 'Toggle all lights',
        'security': 'Show security status',
        'temperature': 'What\'s the current temperature?',
        'energy': 'Show energy usage and optimization',
        'design': 'Help me design a modern kitchen'
    };

    const message = actions[action];
    if (message) {
        const chatInput = document.getElementById('chatInput');
        if (chatInput) {
            chatInput.value = message;
            sendMessage();
        }
    }
}

// Execute AI suggested actions
function executeAIActions(actions) {
    actions.forEach(action => {
        switch(action.type) {
            case 'toggle_lights':
                toggleAllLights();
                break;
            case 'activate_security':
                activateSecurityMode();
                break;
            case 'set_temperature':
                if (action.value) {
                    setTemperature(action.value);
                }
                break;
            case 'show_notification':
                showNotification(action.message, action.level || 'info');
                break;
            case 'navigate':
                if (action.url) {
                    window.location.href = action.url;
                }
                break;
        }
    });
}

// ===== CALL-TO-ACTION BUTTON FUNCTIONALITY =====

function initializeCallToActionButtons() {
    // Get Started buttons
    document.querySelectorAll('[href*="get-started"], .btn-get-started').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            showGetStartedModal();
        });
    });

    // Service buttons
    document.querySelectorAll('.service-card a, .featured-service a').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const serviceName = this.closest('.service-card, .featured-service')?.querySelector('h3')?.textContent;
            if (serviceName) {
                trackServiceClick(serviceName);
            }
        });
    });

    // Contact/Consultation buttons
    document.querySelectorAll('[href*="consultation"], [href*="contact"]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            showConsultationModal();
        });
    });

    // Demo/Trial buttons
    document.querySelectorAll('.btn-demo, .btn-trial').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            startDemo();
        });
    });
}

// Show get started modal
function showGetStartedModal() {
    const modal = createModal('Get Started with SafeNest', `
        <div class="get-started-content">
            <h3>Choose Your Path</h3>
            <div class="path-options">
                <div class="path-option" onclick="selectPath('homeowner')">
                    <i class="fas fa-home"></i>
                    <h4>Homeowner</h4>
                    <p>Smart home automation and security</p>
                </div>
                <div class="path-option" onclick="selectPath('architect')">
                    <i class="fas fa-drafting-compass"></i>
                    <h4>Architect</h4>
                    <p>AI-powered design tools and consultation</p>
                </div>
                <div class="path-option" onclick="selectPath('developer')">
                    <i class="fas fa-code"></i>
                    <h4>Developer</h4>
                    <p>IoT integration and API access</p>
                </div>
            </div>
        </div>
    `);

    document.body.appendChild(modal);
    setTimeout(() => modal.classList.add('show'), 100);
}

// Show consultation modal
function showConsultationModal() {
    const modal = createModal('Schedule Consultation', `
        <div class="consultation-form">
            <form onsubmit="submitConsultation(event)">
                <div class="form-group">
                    <label>Name</label>
                    <input type="text" name="name" required>
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" name="email" required>
                </div>
                <div class="form-group">
                    <label>Service Interest</label>
                    <select name="service" required>
                        <option value="">Select a service</option>
                        <option value="smart-home">Smart Home Setup</option>
                        <option value="security">Security Systems</option>
                        <option value="architecture">AI Architecture Design</option>
                        <option value="energy">Energy Optimization</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Message</label>
                    <textarea name="message" rows="4" placeholder="Tell us about your project..."></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Schedule Consultation</button>
            </form>
        </div>
    `);

    document.body.appendChild(modal);
    setTimeout(() => modal.classList.add('show'), 100);
}

// Utility functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'times' : 'info'}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Device control functions
function activateSecurityMode() {
    fetch('/api/security/activate/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        showNotification('Security mode activated', 'success');
    });
}

function adjustTemperature() {
    const temp = prompt('Set temperature (°C):');
    if (temp) {
        setTemperature(parseInt(temp));
    }
}

function setTemperature(temp) {
    fetch('/api/devices/thermostat/set/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({temperature: temp})
    })
    .then(response => response.json())
    .then(() => {
        showNotification(`Temperature set to ${temp}°C`, 'success');
    })
    .catch(error => {
        console.error('Temperature control error:', error);
        showNotification('Failed to set temperature', 'error');
    });
}

// ===== ADDITIONAL UTILITY FUNCTIONS =====

// Create modal utility
function createModal(title, content) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>${title}</h3>
                <button class="modal-close" onclick="closeModal(this)">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                ${content}
            </div>
        </div>
    `;

    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal(modal.querySelector('.modal-close'));
        }
    });

    return modal;
}

// Close modal
function closeModal(button) {
    const modal = button.closest('.modal-overlay');
    modal.classList.remove('show');
    setTimeout(() => modal.remove(), 300);
}

// Select path in get started modal
function selectPath(path) {
    const pathUrls = {
        'homeowner': '/smart-home/',
        'architect': '/architecture/',
        'developer': '/api-docs/'
    };

    showNotification(`Welcome! Redirecting to ${path} section...`, 'success');
    setTimeout(() => {
        window.location.href = pathUrls[path] || '/';
    }, 1500);
}

// Track service clicks for analytics
function trackServiceClick(serviceName) {
    // Analytics tracking
    if (typeof gtag !== 'undefined') {
        gtag('event', 'service_click', {
            'service_name': serviceName,
            'page_location': window.location.href
        });
    }

    console.log(`Service clicked: ${serviceName}`);
}

// Submit consultation form
function submitConsultation(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        service: formData.get('service'),
        message: formData.get('message')
    };

    fetch('/api/consultation/submit/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showNotification('Consultation request submitted successfully!', 'success');
            closeModal(form.closest('.modal-overlay').querySelector('.modal-close'));
        } else {
            showNotification('Failed to submit request. Please try again.', 'error');
        }
    })
    .catch(error => {
        console.error('Consultation submission error:', error);
        showNotification('Network error. Please try again.', 'error');
    });
}

// Start demo functionality
function startDemo() {
    showNotification('Starting SafeNest demo...', 'info');

    // Open chat and send demo message
    toggleChat();
    setTimeout(() => {
        document.getElementById('chatInput').value = 'Start demo mode';
        sendMessage();
    }, 500);
}

// Toggle all lights function
function toggleAllLights() {
    fetch('/api/devices/lights/toggle-all/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(() => {
        showNotification('All lights toggled', 'success');
    })
    .catch(error => {
        console.error('Light control error:', error);
        showNotification('Failed to control lights', 'error');
    });
}