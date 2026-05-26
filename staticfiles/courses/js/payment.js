/* ===== GET CSRF TOKEN ===== */
function getCookie(name) {

    let cookieValue = null;

    if (document.cookie) {

        document.cookie.split(';').forEach(c => {

            c = c.trim();

            if (c.startsWith(name + '=')) {

                cookieValue = decodeURIComponent(
                    c.substring(name.length + 1)
                );
            }
        });
    }

    return cookieValue;
}

/* ===== PAYMENT BUTTON ===== */
const payBtn = document.getElementById("pay-btn");

payBtn.onclick = function(e) {

    e.preventDefault();

    payBtn.classList.add("loading");
    payBtn.innerHTML = "Processing...";

    const options = {

        key: razorpayKey,

        amount: razorpayAmount,

        currency: "INR",

        name: "LMS Platform",

        description: courseTitle,

        order_id: razorpayOrderId,

        method: {
            upi: true,
            card: false,
            netbanking: false,
            wallet: false
        },

        upi: {
            flow: "intent"
        },

        handler: function (response) {

            fetch(paymentSuccessUrl, {

                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },

                body: JSON.stringify({

                    razorpay_payment_id:
                        response.razorpay_payment_id,

                    razorpay_order_id:
                        response.razorpay_order_id,

                    razorpay_signature:
                        response.razorpay_signature,

                    user_id: currentUserId
                })
            })

            .then(res => res.json())

            .then(data => {

                if (data.status === "success") {

                    alert("✅ Payment Successful!");

                    window.location.href =
                        studentCoursesUrl;

                } else {

                    alert("❌ Payment verification failed");

                    resetButton();
                }
            })

            .catch(err => {

                console.error(err);

                alert("❌ Server error");

                resetButton();
            });
        },

        modal: {

            ondismiss: function () {

                alert("⚠️ Payment cancelled");

                resetButton();
            }
        },

        theme: {
            color: "#2563eb"
        }
    };

    const rzp = new Razorpay(options);

    rzp.open();
};

/* ===== RESET BUTTON ===== */
function resetButton(){

    payBtn.classList.remove("loading");

    payBtn.innerHTML = "Pay Now";
}