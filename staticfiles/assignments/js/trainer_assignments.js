let qCount = 0;

function toggleType(val) {
    document.getElementById('mcqSection').style.display = (val === 'mcq') ? 'block' : 'none';
    document.getElementById('pdfSection').style.display = (val === 'pdf') ? 'block' : 'none';
    document.getElementById('gformSection').style.display = (val === 'gform') ? 'block' : 'none';

    if (val === 'mcq' && qCount === 0) addQuestion();
}

function addQuestion() {
    qCount++;
    const container = document.getElementById("questionsContainer");
    const div = document.createElement("div");
    div.className = "premium-q-card";
    div.id = "q_block_" + qCount;
    div.innerHTML = `
    <h4 style="margin-bottom:16px;">Question ${qCount}</h4>

    <input type="text"
           name="q_${qCount}_text"
           class="premium-form-input"
           placeholder="Enter question..."
           style="margin-bottom:12px;">

    <div class="premium-form-group" style="margin-bottom:12px;">
        <label>Question Timer (Seconds)</label>
        <input type="number"
               name="q_${qCount}_time"
               class="premium-form-input"
               value="30"
               min="1">
    </div>

    <div id="q_${qCount}_opts" style="margin-top:12px;"></div>

    <button type="button"
            class="premium-btn"
            style="padding:10px 18px; font-size:13px; margin-top:12px;"
            onclick="addOption(${qCount})">
        + Add Choice
    </button>
`;
    container.appendChild(div);
    addOption(qCount);
    addOption(qCount);
}

function addOption(qNum) {
    const container = document.getElementById(`q_${qNum}_opts`);
    const idx = container.children.length + 1;
    const div = document.createElement("div");
    div.style.display = 'flex';
    div.style.alignItems = 'center';
    div.style.gap = '12px';
    div.style.marginBottom = '10px';
    div.innerHTML = `
    <input type="radio" name="q_${qNum}_correct" value="${idx}">
    <input type="text" name="q_${qNum}_opt_${idx}" class="premium-form-input" placeholder="Option ${idx}" style="flex:1;">
`;
    container.appendChild(div);
}

window.onload = () => toggleType('mcq');
