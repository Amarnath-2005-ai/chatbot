$(document).ready(function() {
  // Day/Night toggle
  $("#toggle-theme").change(function() {
    if(this.checked) {
      $("body").addClass("night-mode");
    } else {
      $("body").removeClass("night-mode");
    }
  });

  // ChatGPT-style message rendering
  function appendMessage(text, sender) {
    const messageDiv = $('<div class="chatgpt-message ' + sender + '"></div>');
    const bubble = $('<div class="chatgpt-bubble"></div>').text(text);
    messageDiv.append(bubble);
    $("#response").append(messageDiv);
    $("#response").scrollTop($("#response")[0].scrollHeight);
  }

  function submitQuestion() {
    var question = $("#question").val();
    if (!question.trim()) return;
    appendMessage(question, 'user');
    $("#question").val("");
    $.ajax({
      type: "POST",
      url: "/chatbot",
      data: { question: question },
      success: function(result) {
        appendMessage(result.response, 'bot');
      },
      error: function() {
        appendMessage('Sorry, there was an error.', 'bot');
      }
    });
  }

  $(".chatgpt-input-row").on('submit', function(e) {
    e.preventDefault();
    submitQuestion();
  });

  $("#question").keypress(function(e) {
    if(e.which === 13 && !e.shiftKey) {
      e.preventDefault();
      submitQuestion();
    }
  });
});
