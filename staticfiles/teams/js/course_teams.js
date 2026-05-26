    function initiateReply(element) {
        const id = element.getAttribute('data-id');
        const user = element.getAttribute('data-user');
        const text = element.getAttribute('data-text');

        document.getElementById("reply_to_id").value = id;
        document.getElementById("replyUser").innerText = user;
        document.getElementById("replyText").innerText = text;
        document.getElementById("replyPreview").style.display = "flex";
        document.getElementById("msgInput").focus();
    }

    function cancelReply() {
        document.getElementById("reply_to_id").value = "";
        document.getElementById("replyPreview").style.display = "none";
    }

    function deleteMsg(id) {
        if (confirm("Delete this message?")) {
            // Standard delete logic
            fetch(`/teams/delete-message/${id}/`)
                .then(res => {
                    if(res.ok) location.reload();
                    else alert("Failed to delete.");
                });
        }
    }

    function searchChats() {
        let input = document.getElementById('chatSearchInput').value.toLowerCase();
        document.querySelectorAll('#chatList .chat-item').forEach(item => {
            let name = item.querySelector('.chat-name').textContent.toLowerCase();
            item.style.display = name.includes(input) ? "flex" : "none";
        });
    }

    function showFileName(input) {
        const display = document.getElementById('fileNameDisplay');
        if (input.files && input.files[0]) {
            display.innerText = "📎 " + input.files[0].name;
            display.style.display = "inline";
        }
    }

    function switchView(view) {
        document.querySelectorAll('.sidebar-view').forEach(v => v.classList.remove('active'));
        document.querySelectorAll('.rail-item').forEach(i => i.classList.remove('active'));
        document.getElementById('view-' + view).classList.add('active');
        document.getElementById('rail-' + view).classList.add('active');
    }

    function openPopup() { 
        document.getElementById("popup").style.display="block"; 
        document.getElementById("overlay").style.display="block"; 
    }
    function closePopup() { 
        document.getElementById("popup").style.display="none"; 
        document.getElementById("overlay").style.display="none"; 
    }

    function toggleMembers() {
        let d = document.getElementById("membersDropdown");
        d.style.display = d.style.display === "block" ? "none" : "block";
    }

    function meet() { 
        const roomId = "{% if team %}{{ team.id }}{% else %}{{ course.id }}{% endif %}";
        window.open(`https://meet.jit.si/TeamsProLMS_Room_${roomId}`, '_blank'); 
    }

    function loadStudents() {
        let id = document.getElementById("trainerSelect").value;
        let box = document.getElementById("studentsBox");
        if (!id) return;
        fetch("/teams/get-students/?trainer_id=" + id)
        .then(r => r.json())
        .then(data => {
            box.innerHTML = "";
            data.forEach(s => {
                box.innerHTML += `<label style="display:flex; align-items:center; gap:8px; font-size:13px; margin-bottom:5px; cursor:pointer;">
                    <input type="checkbox" name="students" value="${s.id}"> ${s.username}</label>`;
            });
        });
    }

    const vp = document.getElementById("chatViewport");
    if (vp) vp.scrollTop = vp.scrollHeight;