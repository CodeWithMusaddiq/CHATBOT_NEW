// frontend/script.js

const API_URL = "http://127.0.0.1:8000";

// Upload PDF
document.getElementById("uploadBtn").addEventListener("click", async () => {
  const fileInput = document.getElementById("pdfFile");
  const uploadStatus = document.getElementById("uploadStatus");

  if (!fileInput.files.length) {
    alert("Please choose a PDF file first!");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  uploadStatus.innerText = "⏳ Uploading and processing...";
  uploadStatus.className = "status-message loading";

  try {
    const response = await fetch(`${API_URL}/upload/`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (response.ok) {
      uploadStatus.innerText = `✅ ${data.message}\n📊 Document ID: ${data.document_id}`;
      uploadStatus.className = "status-message";
      console.log("Upload success:", data);
      
      // Clear file input
      fileInput.value = "";
      
      // Refresh document list
      loadDocuments();
    } else {
      uploadStatus.innerText = "❌ Upload failed: " + data.detail;
      uploadStatus.className = "status-message";
      console.error("Upload error:", data);
    }
  } catch (error) {
    console.error("Error:", error);
    uploadStatus.innerText = "⚠️ Failed to connect to server. Is the backend running?";
    uploadStatus.className = "status-message";
  }
});

// Ask Question
document.getElementById("askBtn").addEventListener("click", async () => {
  const questionInput = document.getElementById("question");
  const responseDiv = document.getElementById("response");

  if (!questionInput.value.trim()) {
    alert("Please enter a question!");
    return;
  }

  responseDiv.innerHTML = "💬 Thinking...";
  responseDiv.className = "response-box loading";

  try {
    const response = await fetch(`${API_URL}/chat/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: questionInput.value }),
    });

    const data = await response.json();
    console.log("Chat response:", data);

    if (response.ok) {
      let answerHTML = `<b>🤖 Answer:</b><br><br>${data.answer}`;
      
      if (data.sources && data.sources.length > 0) {
        answerHTML += `<br><br><b>📚 Sources:</b> ${data.sources.join(", ")}`;
      }
      
      answerHTML += `<br><br><small>`;
      answerHTML += `Found ${data.matches} relevant chunks`;
      if (data.top_similarity) {
        answerHTML += ` | Best match: ${(data.top_similarity * 100).toFixed(1)}%`;
      }
      answerHTML += `</small>`;
      
      responseDiv.innerHTML = answerHTML;
      responseDiv.className = "response-box";
    } else {
      responseDiv.innerHTML = "⚠️ Error: " + data.detail;
      responseDiv.className = "response-box";
    }
  } catch (error) {
    console.error("Error:", error);
    responseDiv.innerHTML = "⚠️ Failed to reach server. Make sure the backend is running on port 8000.";
    responseDiv.className = "response-box";
  }
});

// Load Documents List
async function loadDocuments() {
  const docsList = document.getElementById("documentsList");
  
  try {
    const response = await fetch(`${API_URL}/chat/documents`);
    const data = await response.json();

    if (data.count === 0) {
      docsList.innerHTML = "<p><i>No documents uploaded yet.</i></p>";
      return;
    }

    let html = "";
    data.documents.forEach((doc, index) => {
      const date = new Date(doc.uploaded_at).toLocaleString();
      html += `
        <div class="document-item">
          <strong>${index + 1}. ${doc.filename}</strong><br>
          <small>Uploaded: ${date} | Chunks: ${doc.chunk_count || 0}</small>
        </div>
      `;
    });

    docsList.innerHTML = html;
  } catch (error) {
    console.error("Error loading documents:", error);
    docsList.innerHTML = "<p><i>Error loading documents</i></p>";
  }
}

// List Documents Button
document.getElementById("listDocsBtn").addEventListener("click", loadDocuments);

// Load documents on page load
window.addEventListener('load', loadDocuments);