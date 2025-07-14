$(document).ready(function() {
  // Theme switching
  const themeSwitch = $('#theme-switch');
  const body = $('body');
  
  // Check for saved theme preference
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
      body.attr('data-theme', savedTheme);
      themeSwitch.prop('checked', savedTheme === 'dark');
  }
  
  themeSwitch.change(function() {
      if (this.checked) {
          body.attr('data-theme', 'dark');
          localStorage.setItem('theme', 'dark');
      } else {
          body.attr('data-theme', 'light');
          localStorage.setItem('theme', 'light');
      }
  });

  // Chat functionality
  const messageContainer = $('#message-container');
  const messageForm = $('#message-form');
  const userInput = $('#user-input');
  
  // Add smooth scrolling to bottom
  function scrollToBottom() {
      messageContainer.animate({
          scrollTop: messageContainer[0].scrollHeight
      }, 300);
  }
  
  // Add message to chat
  function addMessage(content, sender) {
      const messageDiv = $(`
          <div class="message ${sender}">
              <div class="message-bubble">
                  <p>${content}</p>
              </div>
          </div>
      `);
      
      messageContainer.append(messageDiv);
      scrollToBottom();
  }
  
  // Show typing indicator
  function showTyping() {
      const typingDiv = $(`
          <div class="message bot">
              <div class="typing-indicator">
                  <div class="typing-dot"></div>
                  <div class="typing-dot"></div>
                  <div class="typing-dot"></div>
              </div>
          </div>
      `);
      
      messageContainer.append(typingDiv);
      scrollToBottom();
      return typingDiv;
  }
  
  // Handle form submission
  messageForm.on('submit', function(e) {
      e.preventDefault();
      const message = userInput.val().trim();
      
      if (message) {
          addMessage(message, 'user');
          userInput.val('');
          
          // Show typing indicator
          const typingIndicator = showTyping();
          
          // Send to server
          $.ajax({
              type: 'POST',
              url: '/chatbot',
              contentType: 'application/json',
              data: JSON.stringify({ message: message }),
              success: function(response) {
                  typingIndicator.remove();
                  addMessage(response.response, 'bot');
              },
              error: function() {
                  typingIndicator.remove();
                  addMessage("Sorry, I'm having trouble connecting. Please try again later.", 'bot');
              }
          });
      }
  });
  
  // Allow shift+enter for new lines
  userInput.on('keydown', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          messageForm.trigger('submit');
      }
  });
  
  // Focus input on load
  userInput.focus();
});