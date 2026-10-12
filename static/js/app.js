// GemmaStudio Client Application
document.addEventListener("DOMContentLoaded", () => {
    // Elements
    const chatContainer = document.getElementById("chatContainer");
    const welcomeHero = document.getElementById("welcomeHero");
    const messagesList = document.getElementById("messagesList");
    const chatForm = document.getElementById("chatForm");
    const promptInput = document.getElementById("promptInput");
    const sendBtn = document.getElementById("sendBtn");
    const newChatBtn = document.getElementById("newChatBtn");
    
    // Model & Settings
    const modelSelect = document.getElementById("modelSelect");
    const modelBadge = document.getElementById("modelBadge");
    const activeModelTitle = document.getElementById("activeModelTitle");
    const thinkingHighBtn = document.getElementById("thinkingHighBtn");
    const thinkingMinimalBtn = document.getElementById("thinkingMinimalBtn");
    const thinkingBadge = document.getElementById("thinkingBadge");
    const personaSelect = document.getElementById("personaSelect");
    const systemInstruction = document.getElementById("systemInstruction");
    const tokenTimer = document.getElementById("tokenTimer");

    // Attachments
    const attachBtn = document.getElementById("attachBtn");
    const fileInput = document.getElementById("fileInput");
    const attachmentContainer = document.getElementById("attachmentContainer");
    const imagePreview = document.getElementById("imagePreview");
    const removeAttachmentBtn = document.getElementById("removeAttachmentBtn");

    // Status & Settings Modal
    const statusDot = document.getElementById("statusDot");
    const statusText = document.getElementById("statusText");
    const openSettingsBtn = document.getElementById("openSettingsBtn");
    const settingsModal = document.getElementById("settingsModal");
    const closeSettingsBtn = document.getElementById("closeSettingsBtn");
    const apiKeyInput = document.getElementById("apiKeyInput");
    const saveToEnvCheckbox = document.getElementById("saveToEnvCheckbox");
    const saveKeyBtn = document.getElementById("saveKeyBtn");
    const togglePasswordBtn = document.getElementById("togglePasswordBtn");

    // Snippets Modal
    const openSnippetBtn = document.getElementById("openSnippetBtn");
    const snippetModal = document.getElementById("snippetModal");
    const closeSnippetBtn = document.getElementById("closeSnippetBtn");
    const closeSnippetFooterBtn = document.getElementById("closeSnippetFooterBtn");
    const snippetCode = document.getElementById("snippetCode");
    const copySnippetBtn = document.getElementById("copySnippetBtn");
    const exportChatBtn = document.getElementById("exportChatBtn");

    // History & Tabs Elements
    const tabControlsBtn = document.getElementById("tabControlsBtn");
    const tabHistoryBtn = document.getElementById("tabHistoryBtn");
    const tabControlsContent = document.getElementById("tabControlsContent");
    const tabHistoryContent = document.getElementById("tabHistoryContent");
    const historyCountBadge = document.getElementById("historyCountBadge");
    const historyFilteredCount = document.getElementById("historyFilteredCount");
    const historySearchInput = document.getElementById("historySearchInput");
    const clearSearchBtn = document.getElementById("clearSearchBtn");
    const clearAllHistoryBtn = document.getElementById("clearAllHistoryBtn");
    const historyList = document.getElementById("historyList");
    const navHistoryToggleBtn = document.getElementById("navHistoryToggleBtn");

    // State
    let conversationHistory = []; // { role, text, images }
    let currentSessionId = null;
    let currentSessionTitle = null;
    let fullSessionMessages = []; // { role, text, thoughts, duration_seconds, model, images, timestamp }
    let currentImageBase64 = null;
    let currentThinkingLevel = "high";
    let isGenerating = false;
    let snippetData = { python: "", javascript: "", curl: "" };
    let currentSnippetTab = "python";

    // Persona Presets
    const PERSONAS = {
        default: "",
        tea_master: "You are a wise Kyoto tea master. Speak calmly and poetically, using nature metaphors. Keep answers under 3 sentences.",
        code_architect: "You are a Principal Software Architect. Focus on performance, clean patterns, and edge-case handling. Provide production-ready code with algorithmic complexity analysis.",
        math_tutor: "You are an algorithmic mathematician. Break down problems step-by-step with rigorous analytical reasoning.",
        custom: ""
    };

    // Initialize marked with highlight.js
    marked.setOptions({
        highlight: function(code, lang) {
            const language = hljs.getLanguage(lang) ? lang : 'plaintext';
            return hljs.highlight(code, { language }).value;
        },
        breaks: true
    });

    // 1. Initial Status Check
    checkApiStatus();
    loadHistoryList();

    async function checkApiStatus() {
        try {
            const res = await fetch("/api/status");
            const data = await res.json();
            if (data.has_key) {
                statusDot.className = "status-dot dot-green";
                statusText.textContent = `API Ready (${data.masked_key})`;
            } else {
                statusDot.className = "status-dot dot-yellow";
                statusText.textContent = "API Key Missing";
            }
        } catch (err) {
            statusDot.className = "status-dot dot-red";
            statusText.textContent = "Server Offline";
        }
    }

    // 2. Model Selection Handling
    modelSelect.addEventListener("change", (e) => {
        const val = e.target.value;
        activeModelTitle.textContent = val;
        if (val === "gemma-4-26b-a4b-it") {
            modelBadge.textContent = "Recommended MoE";
        } else {
            modelBadge.textContent = "Dense / Heavy Reasoning";
        }
    });

    // 3. Thinking Mode Toggle
    thinkingHighBtn.addEventListener("click", () => {
        currentThinkingLevel = "high";
        thinkingHighBtn.classList.add("active");
        thinkingMinimalBtn.classList.remove("active");
        thinkingBadge.textContent = "HIGH";
        thinkingBadge.className = "badge badge-accent";
    });

    thinkingMinimalBtn.addEventListener("click", () => {
        currentThinkingLevel = "minimal";
        thinkingMinimalBtn.classList.add("active");
        thinkingHighBtn.classList.remove("active");
        thinkingBadge.textContent = "MINIMAL";
        thinkingBadge.className = "badge";
    });

    // 4. Persona Selection
    personaSelect.addEventListener("change", (e) => {
        const val = e.target.value;
        if (PERSONAS[val] !== undefined) {
            systemInstruction.value = PERSONAS[val];
        }
        if (val === "custom") {
            systemInstruction.focus();
        }
    });

    systemInstruction.addEventListener("input", () => {
        const currentText = systemInstruction.value.trim();
        let matchedKey = null;
        for (const [key, text] of Object.entries(PERSONAS)) {
            if (key !== "default" && key !== "custom" && text.trim() === currentText) {
                matchedKey = key;
                break;
            }
        }
        if (matchedKey) {
            personaSelect.value = matchedKey;
        } else if (currentText) {
            personaSelect.value = "custom";
        } else {
            personaSelect.value = "default";
        }
    });

    // 5. Image Attachment Handling
    attachBtn.addEventListener("click", () => fileInput.click());

    // Interactive Navbar Tags
    const tagMultimodal = document.getElementById("tagMultimodal");
    if (tagMultimodal) {
        tagMultimodal.addEventListener("click", () => {
            fileInput.click();
        });
    }

    const tagGeminiHosted = document.getElementById("tagGeminiHosted");
    if (tagGeminiHosted) {
        tagGeminiHosted.addEventListener("click", () => {
            window.open("https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api", "_blank");
        });
    }

    fileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) handleImageFile(file);
    });

    function handleImageFile(file) {
        if (!file.type.startsWith("image/")) {
            alert("Please select a valid image (PNG, JPG, WebP).");
            return;
        }
        const reader = new FileReader();
        reader.onload = (event) => {
            currentImageBase64 = event.target.result;
            imagePreview.src = currentImageBase64;
            attachmentContainer.style.display = "block";
            promptInput.focus();
        };
        reader.readAsDataURL(file);
    }

    removeAttachmentBtn.addEventListener("click", () => {
        currentImageBase64 = null;
        fileInput.value = "";
        attachmentContainer.style.display = "none";
    });

    // Drag and drop image onto chat input
    promptInput.addEventListener("dragover", (e) => e.preventDefault());
    promptInput.addEventListener("drop", (e) => {
        e.preventDefault();
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleImageFile(e.dataTransfer.files[0]);
        }
    });

    // Paste image from clipboard
    document.addEventListener("paste", (e) => {
        const items = e.clipboardData.items;
        for (let item of items) {
            if (item.type.indexOf("image") !== -1) {
                const blob = item.getAsFile();
                handleImageFile(blob);
                break;
            }
        }
    });

    // Auto-grow textarea
    promptInput.addEventListener("input", () => {
        promptInput.style.height = "auto";
        promptInput.style.height = Math.min(promptInput.scrollHeight, 160) + "px";
    });

    // Enter to submit (Shift+Enter for newline)
    promptInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event("submit"));
        }
    });

    // 6. Chat Submit
    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const text = promptInput.value.trim();
        const image = currentImageBase64;

        if (!text && !image) return;
        if (isGenerating) return;

        // Hide welcome hero
        welcomeHero.style.display = "none";

        // Append user message to UI
        appendUserMessage(text, image);

        // Clear input & attachment
        promptInput.value = "";
        promptInput.style.height = "auto";
        if (image) {
            currentImageBase64 = null;
            fileInput.value = "";
            attachmentContainer.style.display = "none";
        }

        // Show model typing placeholder
        const placeholderId = appendLoadingMessage();

        isGenerating = true;
        sendBtn.disabled = true;
        const startTime = Date.now();
        tokenTimer.textContent = "Gemma is thinking...";

        try {
            // Guarantee persona is passed if a preset is selected, even if textarea was blank
            let sysInstruction = systemInstruction.value.trim();
            if (!sysInstruction && personaSelect.value && PERSONAS[personaSelect.value]) {
                sysInstruction = PERSONAS[personaSelect.value];
                systemInstruction.value = sysInstruction;
            }

            const payload = {
                model: modelSelect.value,
                prompt: text,
                images: image ? [image] : [],
                messages: conversationHistory,
                thinking_level: currentThinkingLevel,
                system_instruction: sysInstruction
            };

            const res = await fetch("/api/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
            tokenTimer.textContent = `Completed in ${elapsed}s`;

            removeElement(placeholderId);

            if (data.success) {
                // Add to history
                conversationHistory.push({
                    role: "user",
                    text: text,
                    images: image ? [image] : []
                });
                conversationHistory.push({
                    role: "model",
                    text: data.text
                });

                if (!currentSessionId) {
                    currentSessionId = "session_" + Date.now();
                }

                fullSessionMessages.push({
                    role: "user",
                    text: text,
                    images: image ? [image] : [],
                    timestamp: new Date().toISOString()
                });
                fullSessionMessages.push({
                    role: "model",
                    text: data.text,
                    thoughts: data.thoughts || null,
                    duration_seconds: data.duration_seconds || null,
                    model: data.model,
                    timestamp: new Date().toISOString()
                });

                appendModelMessage(data.text, data.thoughts, data.duration_seconds, data.model);

                // Auto-save session to history/ on disk
                saveCurrentSessionToDisk();
            } else {
                appendErrorMessage(data.error || "Failed to generate response.", text, image);
                if (data.error && data.error.includes("API Key")) {
                    settingsModal.classList.add("open");
                }
            }
        } catch (err) {
            removeElement(placeholderId);
            appendErrorMessage(`Network or server error: ${err.message}`, text, image);
            tokenTimer.textContent = "Failed";
        } finally {
            isGenerating = false;
            sendBtn.disabled = false;
            promptInput.focus();
        }
    });

    // 7. Message Rendering Helpers
    function appendUserMessage(text, image) {
        const msgDiv = document.createElement("div");
        msgDiv.className = "chat-message user";

        let imgHtml = "";
        if (image) {
            imgHtml = `<img src="${image}" class="message-image-thumb" alt="attached image">`;
        }

        msgDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fa-solid fa-user"></i>
            </div>
            <div class="message-body">
                <div class="message-header">
                    <span class="sender-name">You</span>
                </div>
                ${imgHtml}
                <div class="message-text">${escapeHtml(text)}</div>
            </div>
        `;
        messagesList.appendChild(msgDiv);
        scrollToBottom();
    }

    function appendModelMessage(text, thoughts, duration, model) {
        const msgDiv = document.createElement("div");
        msgDiv.className = "chat-message model";

        let thoughtsHtml = "";
        if (thoughts && thoughts.trim().length > 0) {
            thoughtsHtml = `
                <div class="thinking-accordion open">
                    <div class="thinking-header" onclick="this.parentElement.classList.toggle('open')">
                        <span class="thinking-title">
                            <i class="fa-solid fa-brain"></i> Gemma's Internal Thinking Process
                        </span>
                        <i class="fa-solid fa-chevron-down thinking-toggle-icon"></i>
                    </div>
                    <div class="thinking-content">${escapeHtml(thoughts)}</div>
                </div>
            `;
        }

        let parsedContent = marked.parse(text || "*(No text response)*");
        if (typeof DOMPurify !== "undefined") {
            parsedContent = DOMPurify.sanitize(parsedContent);
        }

        msgDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fa-solid fa-atom"></i>
            </div>
            <div class="message-body">
                <div class="message-header">
                    <span class="sender-name">Gemma 4</span>
                    <span class="message-meta">${model} • ${duration || 0}s</span>
                </div>
                ${thoughtsHtml}
                <div class="message-text">${parsedContent}</div>
            </div>
        `;

        messagesList.appendChild(msgDiv);
        addCopyButtons(msgDiv);
        scrollToBottom();
    }

    function appendLoadingMessage() {
        const id = `loading-${Date.now()}`;
        const msgDiv = document.createElement("div");
        msgDiv.className = "chat-message model";
        msgDiv.id = id;

        msgDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fa-solid fa-atom"></i>
            </div>
            <div class="message-body">
                <div class="message-header">
                    <span class="sender-name">Gemma 4</span>
                    <span class="message-meta">Running reasoning model...</span>
                </div>
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        messagesList.appendChild(msgDiv);
        scrollToBottom();
        return id;
    }

    function appendErrorMessage(errText, retryText, retryImage) {
        const msgDiv = document.createElement("div");
        msgDiv.className = "chat-message model";

        let retryHtml = "";
        if (retryText) {
            retryHtml = `
                <div style="margin-top: 10px;">
                    <button class="btn btn-outline-sm retry-btn" style="border-color: rgba(239, 68, 68, 0.5); color: #fca5a5;">
                        <i class="fa-solid fa-rotate-right"></i> Retry Prompt
                    </button>
                </div>
            `;
        }

        msgDiv.innerHTML = `
            <div class="message-avatar" style="background: var(--danger)">
                <i class="fa-solid fa-triangle-exclamation"></i>
            </div>
            <div class="message-body">
                <div class="message-header">
                    <span class="sender-name" style="color: var(--danger)">Error</span>
                </div>
                <div class="message-text" style="color: #fca5a5;">${escapeHtml(errText)}</div>
                ${retryHtml}
            </div>
        `;

        if (retryText) {
            const retryBtn = msgDiv.querySelector(".retry-btn");
            if (retryBtn) {
                retryBtn.onclick = () => {
                    msgDiv.remove();
                    promptInput.value = retryText;
                    if (retryImage) {
                        currentImageBase64 = retryImage;
                        imagePreview.src = retryImage;
                        attachmentContainer.style.display = "block";
                    }
                    chatForm.dispatchEvent(new Event("submit"));
                };
            }
        }

        messagesList.appendChild(msgDiv);
        scrollToBottom();
    }

    function removeElement(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function escapeHtml(str) {
        if (!str) return "";
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function addCopyButtons(container) {
        const preBlocks = container.querySelectorAll("pre");
        preBlocks.forEach((pre) => {
            if (pre.querySelector(".copy-code-btn")) return;
            const btn = document.createElement("button");
            btn.className = "copy-snippet-btn";
            btn.innerHTML = `<i class="fa-regular fa-copy"></i> Copy`;
            btn.onclick = () => {
                const code = pre.querySelector("code") ? pre.querySelector("code").innerText : pre.innerText;
                navigator.clipboard.writeText(code);
                btn.innerHTML = `<i class="fa-solid fa-check"></i> Copied!`;
                setTimeout(() => {
                    btn.innerHTML = `<i class="fa-regular fa-copy"></i> Copy`;
                }, 2000);
            };
            pre.appendChild(btn);
        });
    }

    // 8. Quick Prompt Cards
    document.querySelectorAll(".quick-prompt-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            const prompt = btn.getAttribute("data-prompt");
            const thinking = btn.getAttribute("data-thinking");
            const persona = btn.getAttribute("data-persona");

            if (prompt) promptInput.value = prompt;
            if (thinking === "high") thinkingHighBtn.click();
            if (persona && personaSelect) {
                personaSelect.value = persona;
                personaSelect.dispatchEvent(new Event("change"));
            }
            promptInput.focus();
        });
    });

    // 8b. Feature Cards (Thinking Process, Vision Understanding, Exportable Code)
    const cardThinking = document.getElementById("cardThinking");
    const cardVision = document.getElementById("cardVision");
    const cardExport = document.getElementById("cardExport");

    if (cardThinking) {
        cardThinking.addEventListener("click", () => {
            thinkingHighBtn.click();
            promptInput.value = "Write an optimized Python algorithm to detect a cycle in a directed graph with O(V+E) time complexity.";
            promptInput.focus();
            promptInput.style.height = "auto";
            promptInput.style.height = Math.min(promptInput.scrollHeight, 160) + "px";
        });
        cardThinking.addEventListener("keydown", (e) => {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                cardThinking.click();
            }
        });
    }

    if (cardVision) {
        cardVision.addEventListener("click", () => {
            fileInput.click();
            if (!promptInput.value.trim()) {
                promptInput.value = "Analyze this image in detail: identify all objects, extract any visible text, and explain the key concepts.";
            }
            promptInput.focus();
        });
        cardVision.addEventListener("keydown", (e) => {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                cardVision.click();
            }
        });
    }

    if (cardExport) {
        cardExport.addEventListener("click", () => {
            openSnippetBtn.click();
        });
        cardExport.addEventListener("keydown", (e) => {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                cardExport.click();
            }
        });
    }

    // 9. Tab Switching (Controls vs History)
    function switchSidebarTab(tabName) {
        if (tabName === "controls") {
            if (tabControlsBtn) tabControlsBtn.classList.add("active");
            if (tabHistoryBtn) tabHistoryBtn.classList.remove("active");
            if (tabControlsContent) tabControlsContent.style.display = "flex";
            if (tabHistoryContent) tabHistoryContent.style.display = "none";
        } else {
            if (tabHistoryBtn) tabHistoryBtn.classList.add("active");
            if (tabControlsBtn) tabControlsBtn.classList.remove("active");
            if (tabHistoryContent) tabHistoryContent.style.display = "flex";
            if (tabControlsContent) tabControlsContent.style.display = "none";
            loadHistoryList(historySearchInput ? historySearchInput.value.trim() : "");
            if (historySearchInput) setTimeout(() => historySearchInput.focus(), 60);
        }
    }

    if (tabControlsBtn) tabControlsBtn.addEventListener("click", () => switchSidebarTab("controls"));
    if (tabHistoryBtn) tabHistoryBtn.addEventListener("click", () => switchSidebarTab("history"));
    if (navHistoryToggleBtn) {
        navHistoryToggleBtn.addEventListener("click", () => {
            const isHistoryActive = tabHistoryBtn && tabHistoryBtn.classList.contains("active");
            switchSidebarTab(isHistoryActive ? "controls" : "history");
        });
    }

    // 9b. Auto-Save Session to Disk
    async function saveCurrentSessionToDisk() {
        if (!currentSessionId || fullSessionMessages.length === 0) return;
        try {
            const firstUserMsg = fullSessionMessages.find((m) => m.role === "user");
            const autoTitle = currentSessionTitle || (firstUserMsg ? (firstUserMsg.text.length > 42 ? firstUserMsg.text.slice(0, 42) + "..." : firstUserMsg.text) : "Untitled Chat");

            const res = await fetch("/api/history/save", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    id: currentSessionId,
                    title: autoTitle,
                    model: modelSelect.value,
                    thinking_level: currentThinkingLevel,
                    system_instruction: systemInstruction.value.trim(),
                    messages: fullSessionMessages
                })
            });
            const data = await res.json();
            if (data.success && data.title) {
                currentSessionTitle = data.title;
                loadHistoryList(historySearchInput ? historySearchInput.value.trim() : "");
            }
        } catch (err) {
            console.warn("Could not save session to disk:", err);
        }
    }

    // 9c. Load History List with Search Filter
    let searchDebounceTimer = null;
    async function loadHistoryList(query = "") {
        if (!historyList) return;
        try {
            const url = query ? `/api/history?q=${encodeURIComponent(query)}` : "/api/history";
            const res = await fetch(url);
            const data = await res.json();
            if (!data.success) return;

            const sessions = data.sessions || [];
            if (historyCountBadge) historyCountBadge.textContent = data.total !== undefined ? data.total : sessions.length;
            if (historyFilteredCount) historyFilteredCount.textContent = sessions.length;

            if (sessions.length === 0) {
                historyList.innerHTML = `
                    <div class="history-empty">
                        <i class="fa-regular fa-comments"></i>
                        <p>${query ? `No chats found matching "<strong>${escapeHtml(query)}</strong>"` : "No chat history yet.<br>Start chatting to see sessions saved here."}</p>
                    </div>
                `;
                return;
            }

            historyList.innerHTML = "";
            sessions.forEach((s) => {
                const item = document.createElement("div");
                item.className = `history-item ${s.id === currentSessionId ? "active" : ""}`;
                item.setAttribute("data-session-id", s.id);

                const timeStr = formatRelativeTime(s.updated_at || s.created_at);
                const shortModel = (s.model || "gemma").replace("gemma-4-", "").replace("-it", "");

                item.innerHTML = `
                    <div class="history-item-top">
                        <div class="history-item-title" title="${escapeHtml(s.title)}">
                            <i class="fa-regular fa-message" style="margin-right: 6px; font-size: 0.72rem; color: #60a5fa;"></i>${escapeHtml(s.title)}
                        </div>
                        <button type="button" class="history-delete-btn" title="Delete conversation" data-id="${s.id}">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </div>
                    ${s.preview ? `<div class="history-item-preview">${escapeHtml(s.preview)}</div>` : ""}
                    <div class="history-item-meta">
                        <span class="history-item-model">${escapeHtml(shortModel)}</span>
                        <span>${timeStr} • ${s.message_count} msgs</span>
                    </div>
                `;

                // Click on item loads that full session
                item.addEventListener("click", (e) => {
                    if (e.target.closest(".history-delete-btn")) return;
                    loadSession(s.id);
                });

                // Delete session
                const delBtn = item.querySelector(".history-delete-btn");
                if (delBtn) {
                    delBtn.addEventListener("click", async (e) => {
                        e.stopPropagation();
                        if (confirm(`Delete "${s.title}" from saved history?`)) {
                            await deleteSession(s.id);
                        }
                    });
                }

                historyList.appendChild(item);
            });
        } catch (err) {
            console.error("Error loading history list:", err);
        }
    }

    function formatRelativeTime(isoStr) {
        if (!isoStr) return "";
        try {
            const date = new Date(isoStr);
            const now = new Date();
            const diffMs = now - date;
            const diffMin = Math.floor(diffMs / 60000);
            if (diffMin < 1) return "Just now";
            if (diffMin < 60) return `${diffMin}m ago`;
            const diffHours = Math.floor(diffMin / 60);
            if (diffHours < 24) return `${diffHours}h ago`;
            const diffDays = Math.floor(diffHours / 24);
            if (diffDays < 7) return `${diffDays}d ago`;
            return date.toLocaleDateString(undefined, { month: "short", day: "numeric" });
        } catch {
            return "";
        }
    }

    // 9d. Restore Session into Chat Area
    async function loadSession(sessionId) {
        try {
            const res = await fetch(`/api/history/${sessionId}`);
            const data = await res.json();
            if (!data.success || !data.session) {
                alert("Could not load session.");
                return;
            }

            const session = data.session;
            currentSessionId = session.id;
            currentSessionTitle = session.title;
            fullSessionMessages = session.messages || [];
            conversationHistory = [];

            // Clear chat UI
            messagesList.innerHTML = "";
            welcomeHero.style.display = "none";

            // Restore settings if present
            if (session.model && modelSelect.querySelector(`option[value="${session.model}"]`)) {
                modelSelect.value = session.model;
                activeModelTitle.textContent = session.model;
            }
            if (session.thinking_level) {
                if (session.thinking_level === "high") thinkingHighBtn.click();
                else thinkingMinimalBtn.click();
            }
            if (session.system_instruction !== undefined) {
                systemInstruction.value = session.system_instruction;
                systemInstruction.dispatchEvent(new Event("input"));
            }

            // Restore messages into UI
            fullSessionMessages.forEach((msg) => {
                if (msg.role === "user") {
                    conversationHistory.push({
                        role: "user",
                        text: msg.text,
                        images: msg.images || []
                    });
                    appendUserMessage(msg.text, msg.images && msg.images.length > 0 ? msg.images[0] : null);
                } else if (msg.role === "model") {
                    conversationHistory.push({
                        role: "model",
                        text: msg.text
                    });
                    appendModelMessage(msg.text, msg.thoughts, msg.duration_seconds, msg.model || session.model);
                }
            });

            // Highlight active in list
            document.querySelectorAll(".history-item").forEach((el) => {
                el.classList.toggle("active", el.getAttribute("data-session-id") === sessionId);
            });

            tokenTimer.textContent = `Restored (${fullSessionMessages.length} msgs)`;
            promptInput.focus();
        } catch (err) {
            alert(`Error restoring session: ${err.message}`);
        }
    }

    // 9e. Delete Session
    async function deleteSession(sessionId) {
        try {
            const res = await fetch(`/api/history/${sessionId}`, { method: "DELETE" });
            const data = await res.json();
            if (data.success) {
                if (currentSessionId === sessionId) {
                    newChatBtn.click();
                } else {
                    loadHistoryList(historySearchInput ? historySearchInput.value.trim() : "");
                }
            }
        } catch (err) {
            alert(`Error deleting session: ${err.message}`);
        }
    }

    // 9f. Clear All History
    if (clearAllHistoryBtn) {
        clearAllHistoryBtn.addEventListener("click", async () => {
            if (!confirm("Are you sure you want to permanently clear ALL saved chat history files from disk?")) return;
            try {
                const res = await fetch("/api/history/clear", { method: "POST" });
                const data = await res.json();
                if (data.success) {
                    newChatBtn.click();
                    loadHistoryList();
                }
            } catch (err) {
                alert(`Error clearing history: ${err.message}`);
            }
        });
    }

    // 9g. Real-Time Search across Prompts and Titles
    if (historySearchInput) {
        historySearchInput.addEventListener("input", (e) => {
            const val = e.target.value.trim();
            if (clearSearchBtn) clearSearchBtn.style.display = val ? "block" : "none";
            clearTimeout(searchDebounceTimer);
            searchDebounceTimer = setTimeout(() => {
                loadHistoryList(val);
            }, 200);
        });
    }

    if (clearSearchBtn) {
        clearSearchBtn.addEventListener("click", () => {
            historySearchInput.value = "";
            clearSearchBtn.style.display = "none";
            loadHistoryList();
            historySearchInput.focus();
        });
    }

    // 9h. New Session Button
    newChatBtn.addEventListener("click", () => {
        if (conversationHistory.length > 0 && !currentSessionId) {
            saveCurrentSessionToDisk();
        }
        currentSessionId = null;
        currentSessionTitle = null;
        fullSessionMessages = [];
        conversationHistory = [];
        messagesList.innerHTML = "";
        welcomeHero.style.display = "block";
        tokenTimer.textContent = "";
        currentImageBase64 = null;
        fileInput.value = "";
        attachmentContainer.style.display = "none";
        promptInput.value = "";
        promptInput.focus();
        document.querySelectorAll(".history-item").forEach((el) => el.classList.remove("active"));
        switchSidebarTab("controls");
    });

    // 10. Settings Modal Handling
    openSettingsBtn.addEventListener("click", () => settingsModal.classList.add("open"));
    closeSettingsBtn.addEventListener("click", () => settingsModal.classList.remove("open"));

    togglePasswordBtn.addEventListener("click", () => {
        const isPassword = apiKeyInput.type === "password";
        apiKeyInput.type = isPassword ? "text" : "password";
        togglePasswordBtn.innerHTML = isPassword ? '<i class="fa-regular fa-eye-slash"></i>' : '<i class="fa-regular fa-eye"></i>';
    });

    saveKeyBtn.addEventListener("click", async () => {
        const key = apiKeyInput.value.trim();
        if (!key) {
            alert("Please provide a valid Gemini API key.");
            return;
        }
        try {
            saveKeyBtn.disabled = true;
            saveKeyBtn.textContent = "Saving...";
            const res = await fetch("/api/set-key", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    api_key: key,
                    save_to_env: saveToEnvCheckbox.checked
                })
            });
            const data = await res.json();
            if (data.success) {
                statusDot.className = "status-dot dot-green";
                statusText.textContent = `API Ready (${data.masked_key})`;
                settingsModal.classList.remove("open");
                apiKeyInput.value = "";
            } else {
                alert(data.error || "Failed to save key");
            }
        } catch (err) {
            alert(`Error: ${err.message}`);
        } finally {
            saveKeyBtn.disabled = false;
            saveKeyBtn.textContent = "Save Key";
        }
    });

    // 11. Code Snippets Modal
    openSnippetBtn.addEventListener("click", async () => {
        snippetModal.classList.add("open");
        snippetCode.textContent = "# Generating code snippet...";

        try {
            const res = await fetch("/api/code-snippet", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    model: modelSelect.value,
                    prompt: promptInput.value.trim() || "What is the water formula?",
                    thinking_level: currentThinkingLevel,
                    system_instruction: systemInstruction.value.trim(),
                    has_image: !!currentImageBase64
                })
            });
            snippetData = await res.json();
            renderSnippetTab(currentSnippetTab);
        } catch (err) {
            snippetCode.textContent = `# Error fetching snippets: ${err.message}`;
        }
    });

    closeSnippetBtn.addEventListener("click", () => snippetModal.classList.remove("open"));
    closeSnippetFooterBtn.addEventListener("click", () => snippetModal.classList.remove("open"));

    document.querySelectorAll(".tab-btn").forEach((tab) => {
        tab.addEventListener("click", () => {
            document.querySelectorAll(".tab-btn").forEach((t) => t.classList.remove("active"));
            tab.classList.add("active");
            currentSnippetTab = tab.getAttribute("data-tab");
            renderSnippetTab(currentSnippetTab);
        });
    });

    function renderSnippetTab(lang) {
        snippetCode.textContent = snippetData[lang] || "// Not available";
        snippetCode.className = `language-${lang === "curl" ? "bash" : lang}`;
        hljs.highlightElement(snippetCode);
    }

    copySnippetBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(snippetCode.innerText);
        copySnippetBtn.innerHTML = `<i class="fa-solid fa-check"></i> Copied!`;
        setTimeout(() => {
            copySnippetBtn.innerHTML = `<i class="fa-regular fa-copy"></i> Copy`;
        }, 2000);
    });

    // 12. Export Chat as Markdown
    exportChatBtn.addEventListener("click", () => {
        if (conversationHistory.length === 0) {
            alert("No conversation messages to export yet.");
            return;
        }

        let md = `# GemmaStudio Conversation Export\n`;
        md += `*Generated: ${new Date().toLocaleString()}*\n`;
        md += `*Model: ${modelSelect.value} | Thinking Mode: ${currentThinkingLevel}*\n\n---\n\n`;

        conversationHistory.forEach((msg) => {
            const speaker = msg.role === "user" ? "### User" : "### Gemma 4";
            md += `${speaker}\n\n${msg.text}\n\n`;
        });

        const blob = new Blob([md], { type: "text/markdown" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `gemma-session-${Date.now()}.md`;
        a.click();
        URL.revokeObjectURL(url);
    });

    // 13. Gemma Experiment & Code Validation Studio
    const navExperimentBtn = document.getElementById("navExperimentBtn");
    const experimentModal = document.getElementById("experimentModal");
    const closeExperimentBtn = document.getElementById("closeExperimentBtn");
    const closeExperimentFooterBtn = document.getElementById("closeExperimentFooterBtn");
    const suiteSelect = document.getElementById("suiteSelect");
    const runBenchmarkBtn = document.getElementById("runBenchmarkBtn");
    const exportMarkdownBtn = document.getElementById("exportMarkdownBtn");
    const exportJsonBtn = document.getElementById("exportJsonBtn");
    const suiteDesc = document.getElementById("suiteDesc");
    const suiteCaseCount = document.getElementById("suiteCaseCount");
    const suiteModel = document.getElementById("suiteModel");
    const benchmarkProgressWrap = document.getElementById("benchmarkProgressWrap");
    const benchmarkProgressBar = document.getElementById("benchmarkProgressBar");
    const progressStatusText = document.getElementById("progressStatusText");
    const progressPercentText = document.getElementById("progressPercentText");
    const benchmarkResultsBody = document.getElementById("benchmarkResultsBody");

    let suiteList = [];
    let latestRunReport = null;

    async function loadSuites() {
        try {
            const res = await fetch("/api/experiments/suites");
            const data = await res.json();
            if (data.success && data.suites) {
                suiteList = data.suites;
                // Populate suiteSelect
                suiteSelect.innerHTML = suiteList.map(s => `
                    <option value="${s.id}">${escapeHtml(s.name)}</option>
                `).join("");
                updateSuiteInfo();
            }
        } catch (e) {
            console.error("Failed to load suites", e);
        }
    }

    function updateSuiteInfo() {
        const id = suiteSelect.value;
        const suite = suiteList.find(s => s.id === id);
        if (suite) {
            suiteDesc.textContent = suite.description;
            suiteCaseCount.innerHTML = `<i class="fa-solid fa-vial"></i> ${suite.test_cases.length} Test Cases`;
            suiteModel.innerHTML = `<i class="fa-solid fa-microchip"></i> Active: ${modelSelect.value}`;
        }
    }

    if (navExperimentBtn) {
        navExperimentBtn.addEventListener("click", () => {
            experimentModal.classList.add("open");
            loadSuites();
        });
    }

    if (closeExperimentBtn) {
        closeExperimentBtn.addEventListener("click", () => experimentModal.classList.remove("open"));
    }
    if (closeExperimentFooterBtn) {
        closeExperimentFooterBtn.addEventListener("click", () => experimentModal.classList.remove("open"));
    }
    if (suiteSelect) {
        suiteSelect.addEventListener("change", updateSuiteInfo);
    }

    if (runBenchmarkBtn) {
        runBenchmarkBtn.addEventListener("click", async () => {
            const suiteId = suiteSelect.value;
            const modelId = modelSelect.value;

            runBenchmarkBtn.disabled = true;
            exportMarkdownBtn.disabled = true;
            exportJsonBtn.disabled = true;
            benchmarkProgressWrap.style.display = "block";
            benchmarkProgressBar.style.width = "20%";
            progressStatusText.textContent = "Connecting to Gemini API & sending test prompts...";
            progressPercentText.textContent = "20%";

            benchmarkResultsBody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center text-muted">
                        <div class="typing-dots" style="justify-content: center; padding: 12px 0;">
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                        </div>
                        Executing genuine Gemma 4 inference... Please wait.
                    </td>
                </tr>
            `;

            try {
                benchmarkProgressBar.style.width = "50%";
                progressPercentText.textContent = "50%";

                const res = await fetch("/api/experiments/run", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        suite_id: suiteId,
                        model: modelId
                    })
                });

                benchmarkProgressBar.style.width = "90%";
                progressPercentText.textContent = "90%";

                const data = await res.json();
                benchmarkProgressBar.style.width = "100%";
                progressPercentText.textContent = "100%";

                if (data.success) {
                    latestRunReport = data;
                    renderBenchmarkResults(data.results);
                    exportMarkdownBtn.disabled = false;
                    exportJsonBtn.disabled = false;
                    progressStatusText.textContent = `Completed! ${data.results.length} tests finished.`;
                } else {
                    benchmarkResultsBody.innerHTML = `
                        <tr>
                            <td colspan="6" class="text-center" style="color: #f87171;">
                                <i class="fa-solid fa-triangle-exclamation"></i> Error: ${escapeHtml(data.error || "Benchmark run failed")}
                            </td>
                        </tr>
                    `;
                    progressStatusText.textContent = "Benchmark run failed.";
                }
            } catch (err) {
                benchmarkResultsBody.innerHTML = `
                    <tr>
                        <td colspan="6" class="text-center" style="color: #f87171;">
                            <i class="fa-solid fa-triangle-exclamation"></i> Network/API Error: ${escapeHtml(err.message)}
                        </td>
                    </tr>
                `;
                progressStatusText.textContent = "Connection error.";
            } finally {
                runBenchmarkBtn.disabled = false;
            }
        });
    }

    function renderBenchmarkResults(results) {
        if (!results || results.length === 0) {
            benchmarkResultsBody.innerHTML = `
                <tr><td colspan="6" class="text-center text-muted">No results returned.</td></tr>
            `;
            return;
        }

        benchmarkResultsBody.innerHTML = results.map(r => {
            const isPass = r.status === "PASS";
            const statusBadge = isPass
                ? `<span class="badge-status-pass"><i class="fa-solid fa-check"></i> PASS</span>`
                : `<span class="badge-status-fail"><i class="fa-solid fa-xmark"></i> FAIL</span>`;
            
            const thinkingInfo = r.has_thoughts 
                ? `<span style="color: #c084fc;"><i class="fa-solid fa-brain"></i> Active (${r.thoughts_count || 1} parts)</span>` 
                : `<span class="text-muted">Direct</span>`;

            const latencyStr = r.latency_ms ? `${(r.latency_ms / 1000).toFixed(2)}s` : `<span class="text-muted">-</span>`;
            const outputPreview = r.error ? `Error: ${r.error}` : (r.response_sample || "").substring(0, 300);

            return `
                <tr>
                    <td>${statusBadge}</td>
                    <td><strong>${escapeHtml(r.suite_id || "-")}</strong></td>
                    <td style="max-width: 220px;">${escapeHtml(r.name || "-")}</td>
                    <td>${latencyStr}</td>
                    <td>${thinkingInfo}</td>
                    <td><div class="benchmark-output-cell">${escapeHtml(outputPreview)}</div></td>
                </tr>
            `;
        }).join("");
    }

    if (exportMarkdownBtn) {
        exportMarkdownBtn.addEventListener("click", async () => {
            if (!latestRunReport) return;
            try {
                const res = await fetch("/api/experiments/export", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ report: latestRunReport, format: "markdown" })
                });
                const blob = await res.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = `gemma4-benchmark-report-${Date.now()}.md`;
                a.click();
                URL.revokeObjectURL(url);
            } catch (e) {
                alert("Failed to export Markdown report: " + e.message);
            }
        });
    }

    if (exportJsonBtn) {
        exportJsonBtn.addEventListener("click", async () => {
            if (!latestRunReport) return;
            try {
                const res = await fetch("/api/experiments/export", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ report: latestRunReport, format: "json" })
                });
                const blob = await res.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = `gemma4-benchmark-report-${Date.now()}.json`;
                a.click();
                URL.revokeObjectURL(url);
            } catch (e) {
                alert("Failed to export JSON report: " + e.message);
            }
        });
    }
});

