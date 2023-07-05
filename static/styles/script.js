




// ----------------------------------------------------------------------------
$('#dropdown').on('change', function() {
  // Get the selected option value
  var selectedOption = $(this).val();

  // Send an AJAX POST request to the Flask route
  $.ajax({
      type: 'POST',
      url: '/get_result_docInsight',
      data: {selected_option: selectedOption},
      success: function(response) {
          // Update the result element with the received response
        // response = JSON.stringify(response)
        console.log(response)
     
        var table = $('<table class="table-bordered">').addClass('table');
        var thead = $('<thead class="bg-dark text-light">').appendTo(table);
        var tbody = $('<tbody>').appendTo(table);

        // Create table headers based on JSON keys
        var headers = Object.keys(response);
        console.log(headers)
        var headerRow = $('<tr>').appendTo(thead);
        headers.forEach(function(header) {
            $('<th>').text(header).appendTo(headerRow);
        });

        // Create table rows and populate data
        var dataRow = $('<tr>').appendTo(tbody);
        headers.forEach(function(header) {
            $('<td>').text(response[header]).appendTo(dataRow);
        });

        // Append the table to the result div
        $('#docInsi_ResSumm_textArea').empty().append(table);


        //   $('#docInsi_ResSumm_textArea').text(response.result);
        //   $('#docInsi_ResSumm_textArea').html(tableData);
      }
  });
});

  
// $("#messageArea").click(function(){
//   const date = new date();
//   const hour = date.getHours();
//   const minute = date.getMinutes();
//   const str_time = hour + ":" + minute;
//   var rawText = $("#text").val();
//   console.log(rawText)

//     var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + user_input + '<span class="msg_time_send">'+ time + 
//   '</span></div><div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg"></div></div>';

//   $("#text").val("");
//   $("#messageFormeight").append(userHtml)

//   $.ajax({
//     data:{msg:rawText},
//     type:"POST",
//     url:"/get"
//   }).done(function(data){
//     var botHtml ='<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.ibb.co/fSNP7Rz/icons8-chatgpt-512.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">' + bot_response + '<span class="msg_time">' + time + '</span></div></div>';
//     $("#messageFormeight").append($.parseHTML(botHtml));
//   });
//     event.preventDefault();
// });


//  chat bot
$('#sendMessage').click(function () {
  if ($('#customQuestion').val() !== '') {
      $('#emptyChatBot').addClass('d-none')
      var sendMessageTemplate = `<div class="row">
          <div class="col">
          <div class="box arrow-right">
              ` + $('#customQuestion').val() + `
          </div>
          </div>
      </div>
      <div class="row loadingMessage">
          <div class="col">
              <div class="box arrow-left">
              Typing...
              </div>
          </div>
      </div>`;


      $('#messageBody').append(sendMessageTemplate)
      document.getElementById('messageBody').scrollTop = document.getElementById('messageBody').scrollHeight
      document.documentElement.scrollTop = document.documentElement.scrollHeight

      var data = {
          "text": $('#viewTranscriptContent').val(),
          "question": $('#customQuestion').val()
      }

      $('#customQuestion').val('')

      $.ajax({
          type: "POST",
          url: "/document_chatbot",
          contentType: "application/json",
          data: JSON.stringify(data),
          success: function (response) {
              var receiveMessageTemplate = `<div class="row">
                  <div class="col">
                  <div class="box arrow-left">
                      ` + response.document_chatbot + `
                  </div>
                  </div>
              </div>`;

              $('.loadingMessage').remove()
              $('#messageBody').append(receiveMessageTemplate)

              document.getElementById('messageBody').scrollTop = document.getElementById('messageBody').scrollHeight
              document.documentElement.scrollTop = document.documentElement.scrollHeight
          },
          error: function (error) {
              console.log(error);
          }
      })
  }
})

// GPT chat
$('#sendChatbotMessage').click(function () {
  if ($('#chatbotQuestion').val() !== '') {
      $('#emptyMsgChatBot').addClass('d-none')
      var sendMessageTemplate = `<div class="row">
          <div class="col">
          <div class="box arrow-right">
              ` + $('#chatbotQuestion').val() + `
          </div>
          </div>
      </div>
      <div class="row loadingChatbotMessage">
          <div class="col">
              <div class="box arrow-left">
              Typing...
              </div>
          </div>
      </div>`;


      $('#chatbotMessageBody').append(sendMessageTemplate)
      document.getElementById('chatbotMessageBody').scrollTop = document.getElementById('chatbotMessageBody').scrollHeight

      var data = {
          "question": $('#chatbotQuestion').val()
      }

      $('#chatbotQuestion').val('')

      $.ajax({
          type: "POST",
          url: "/global_chatbot",
          contentType: "application/json",
          data: JSON.stringify(data),
          success: function (response) {
              var receiveMessageTemplate = `<div class="row">
                  <div class="col">
                  <div class="box arrow-left">
                      ` + response.global_chatbot + `
                  </div>
                  </div>
              </div>`;

              $('.loadingChatbotMessage').remove()
              $('#chatbotMessageBody').append(receiveMessageTemplate)

              document.getElementById('chatbotMessageBody').scrollTop = document.getElementById('chatbotMessageBody').scrollHeight
          },
          error: function (error) {
              console.log(error);
          }
      })
  }
})

$('.showChatbot').click(function () {
  $('.chatBot').toggleClass('show')
  // If need to clear chat on closing chatbot
  // $('#chatbotMessageBody').html("")
});






