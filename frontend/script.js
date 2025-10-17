const uploadBtn = document.getElementById('uploadBtn');
const askBtn = document.getElementById('askBtn');
const responseDiv = document.getElementById('response');

// Placeholder upload function
uploadBtn.addEventListener('click', async () => {
  const fileInput = document.getElementById('pdfFile');
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a PDF file first!");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("http://127.0.0.1:8000/upload", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  alert(data.message || "File uploaded successfully!");
});

// Placeholder chat function
askBtn.addEventListener('click', async () => {
  const question = document.getElementById('question').value;

  if (!question) {
    alert("Please type a question!");
    return;
  }

  const res = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });

  const data = await res.json();
  responseDiv.innerText = data.answer || "Response will appear here...";
});
