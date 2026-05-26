// =========================
// STUDENT ATTENDANCE JS
// =========================

// ROW HOVER EFFECT
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
const tableWrapper=document.querySelector(".table-wrapper");

if(tableWrapper){

    tableWrapper.addEventListener("scroll",()=>{

        if(tableWrapper.scrollLeft>0){

            tableWrapper.style.boxShadow=
            "inset 10px 0 10px -10px rgba(0,0,0,0.2)";

        }else{

            tableWrapper.style.boxShadow="none";

        }

    });

}

// AUTO HIGHLIGHT TODAY ROW
const today=new Date().toISOString().split("T")[0];

document.querySelectorAll(".table tbody tr").forEach(row=>{

    const firstCell=row.querySelector("td");

    if(firstCell){

        const rowDate=firstCell.innerText.trim();

        if(rowDate===today){

            row.style.background="#dcfce7";

        }

    }

});