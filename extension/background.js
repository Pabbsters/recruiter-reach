chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "REACH_OUT") {
    fetch("http://localhost:5050/reach", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(msg.data),
    })
      .then((r) => r.json())
      .then((data) => sendResponse({ success: true, data }))
      .catch((err) => sendResponse({ success: false, error: err.message }));
    return true; // keep message channel open for async response
  }
});
