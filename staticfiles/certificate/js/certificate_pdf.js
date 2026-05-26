document.addEventListener("DOMContentLoaded", () => {

    // SMOOTH LOAD ANIMATION
    const certificate = document.querySelector(".certificate");

    if(certificate){

        certificate.style.opacity = "0";
        certificate.style.transform = "translateY(20px)";

        setTimeout(() => {

            certificate.style.transition =
                "all 0.6s ease";

            certificate.style.opacity = "1";

            certificate.style.transform =
                "translateY(0)";

        },100);

    }

    // PRINT BUTTON
    const printBtn =
        document.getElementById("printCertificate");

    if(printBtn){

        printBtn.addEventListener("click", () => {

            window.print();

        });

    }

});