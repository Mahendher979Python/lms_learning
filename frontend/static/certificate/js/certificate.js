
document.addEventListener("DOMContentLoaded", function(){

    // DOWNLOAD BUTTON EFFECT
    const btn = document.getElementById("downloadBtn");

    if(btn){

        btn.addEventListener("click", function(){

            btn.innerHTML = "⬇ Downloading...";

            setTimeout(() => {

                btn.innerHTML =
                "⬇ Download Certificate";

            }, 3000);

        });

    }

    // FADE EFFECT
    const wrapper =
    document.querySelector(".certificate-wrapper");

    wrapper.style.opacity = "0";

    setTimeout(() => {

        wrapper.style.opacity = "1";
        wrapper.style.transition = "1s";

    }, 100);

});