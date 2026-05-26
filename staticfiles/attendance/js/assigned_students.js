

// BUTTON CLICK EFFECT
document.querySelectorAll(".btn").forEach(btn=>{

    btn.addEventListener("click",function(){

        this.style.transform="scale(0.96)";

        setTimeout(()=>{
            this.style.transform="scale(1)";
        },120);

    });

});

// TABLE ROW HOVER EFFECT
document.querySelectorAll(".table tbody tr").forEach(row=>{

    row.addEventListener("mouseenter",()=>{

        row.style.transition="0.3s";
        row.style.transform="scale(1.002)";

    });

    row.addEventListener("mouseleave",()=>{

        row.style.transform="scale(1)";

    });

});

// MOBILE TABLE SCROLL SHADOW
const wrapper=document.querySelector(".table-wrapper");

if(wrapper){

    wrapper.addEventListener("scroll",()=>{

        if(wrapper.scrollLeft>0){
            wrapper.style.boxShadow="inset 10px 0 10px -10px rgba(0,0,0,0.2)";
        }else{
            wrapper.style.boxShadow="none";
        }

    });

}

