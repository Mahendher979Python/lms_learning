/* =========================================
   BUY COURSE
========================================= */

function buyCourse(){

    const confirmBuy = confirm(
        "Do you want to buy this course?"
    );

    if(confirmBuy){

        const btn = document.querySelector(".buy");

        if(btn){

            btn.innerHTML = "⏳ Redirecting...";
            btn.disabled = true;
            btn.style.opacity = "0.8";

        }

        window.location.href =
        buyCourseUrl;

    }

}

/* =========================================
   VIDEO PROTECTION
========================================= */

const video = document.getElementById("mainVideo");

if(video){

    /* disable right click */

    video.addEventListener(
        "contextmenu",
        e => e.preventDefault()
    );

    /* auto save progress */

    video.addEventListener("timeupdate",()=>{

        localStorage.setItem(
            "video-progress",
            video.currentTime
        );

    });

    /* restore progress */

    window.addEventListener("load",()=>{

        const saved =
        localStorage.getItem("video-progress");

        if(saved){

            video.currentTime = saved;

        }

    });

}

/* =========================================
   BLOCK SHORTCUTS
========================================= */

document.addEventListener("keydown",function(e){

    /* Ctrl + S */

    if(e.ctrlKey && e.key.toLowerCase()==="s"){

        e.preventDefault();

    }

    /* Ctrl + U */

    if(e.ctrlKey && e.key.toLowerCase()==="u"){

        e.preventDefault();

    }

    /* Ctrl + Shift + I */

    if(
        e.ctrlKey &&
        e.shiftKey &&
        e.key.toLowerCase()==="i"
    ){

        e.preventDefault();

    }

});

/* =========================================
   BUTTON CLICK EFFECT
========================================= */

document.querySelectorAll(".btn")
.forEach(btn=>{

    btn.addEventListener("click",()=>{

        btn.style.transform="scale(0.95)";

        setTimeout(()=>{

            btn.style.transform="";

        },150);

    });

});

/* =========================================
   IMAGE ZOOM EFFECT
========================================= */

const thumbnail =
document.querySelector(".thumbnail");

if(thumbnail){

    thumbnail.addEventListener("mousemove",(e)=>{

        const rect =
        thumbnail.getBoundingClientRect();

        const x =
        ((e.clientX - rect.left) / rect.width) * 100;

        const y =
        ((e.clientY - rect.top) / rect.height) * 100;

        thumbnail.style.transformOrigin =
        `${x}% ${y}%`;

    });

}

/* =========================================
   FADE CONTENT
========================================= */

window.addEventListener("load",()=>{

    document.querySelectorAll(
        ".course-container > *"
    ).forEach((el,index)=>{

        el.style.opacity="0";
        el.style.transform="translateY(15px)";
        el.style.transition="0.5s ease";

        setTimeout(()=>{

            el.style.opacity="1";
            el.style.transform="translateY(0)";

        },index * 120);

    });

});