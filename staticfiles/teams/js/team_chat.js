/* =========================
   TEAM CHAT JS
========================= */

document.addEventListener("DOMContentLoaded", function(){

    // AUTO SCROLL TO BOTTOM
    const messagesBox = document.querySelector(".messages");

    if(messagesBox){
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    // ENTER KEY SEND
    const input = document.querySelector(".chat-input");
    const form = document.querySelector(".chat-form");

    if(input && form){

        input.addEventListener("keypress", function(e){

            if(e.key === "Enter" && !e.shiftKey){

                e.preventDefault();

                if(input.value.trim() !== ""){
                    form.submit();
                }
            }

        });

    }

    // BUTTON LOADING EFFECT
    const sendBtn = document.querySelector(".send-btn");

    if(sendBtn){

        form.addEventListener("submit", function(){

            sendBtn.innerHTML = "Sending...";
            sendBtn.disabled = true;

        });

    }

    // MESSAGE ANIMATION
    const messages = document.querySelectorAll(".message");

    messages.forEach((msg,index)=>{

        msg.style.opacity = "0";
        msg.style.transform = "translateY(20px)";

        setTimeout(()=>{

            msg.style.transition = "0.4s";
            msg.style.opacity = "1";
            msg.style.transform = "translateY(0)";

        }, index * 50);

    });

});