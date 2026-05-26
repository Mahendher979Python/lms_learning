

/* =========================
   BUTTON PRESS EFFECT
========================= */

document.querySelectorAll("button").forEach(btn=>{

    btn.addEventListener("mousedown",()=>{

        btn.style.transform="scale(0.92)";

    });

    btn.addEventListener("mouseup",()=>{

        btn.style.transform="";

    });

});

/* =========================
   3D CARD EFFECT
========================= */

document.querySelectorAll(".user-card").forEach(card=>{

    card.addEventListener("mousemove",(e)=>{

        const rect=card.getBoundingClientRect();

        const x=e.clientX-rect.left;
        const y=e.clientY-rect.top;

        const centerX=rect.width/2;
        const centerY=rect.height/2;

        const rotateX=((y-centerY)/25);
        const rotateY=((centerX-x)/25);

        card.style.transform=`
            rotateX(${rotateX}deg)
            rotateY(${rotateY}deg)
            translateY(-8px)
        `;

    });

    card.addEventListener("mouseleave",()=>{

        card.style.transform="";

    });

});

/* =========================
   GLOW FOLLOW EFFECT
========================= */

document.querySelectorAll(".user-card").forEach(card=>{

    card.addEventListener("mousemove",(e)=>{

        const rect=card.getBoundingClientRect();

        const x=e.clientX-rect.left;
        const y=e.clientY-rect.top;

        card.style.background=`
            radial-gradient(circle at ${x}px ${y}px,
            rgba(255, 255, 255, 0.12),
            rgba(255, 255, 255, 0.04) 60%)
        `;

    });

    card.addEventListener("mouseleave",()=>{

        card.style.background="rgba(255, 255, 255, 0.04)";

    });

});

