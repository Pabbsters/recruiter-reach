let jobInfo = null;

chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  chrome.tabs.sendMessage(tabs[0].id, { type: "GET_JOB_INFO" }, (info) => {
    if (chrome.runtime.lastError || !info) {
      document.getElementById("status").textContent = "Could not read page.";
      return;
    }
    jobInfo = info;
    const { company, role } = info;
    if (company || role) {
      document.getElementById("status").textContent =
        `${role || "Unknown Role"} @ ${company || "Unknown Company"}`;
      document.getElementById("reach-btn").disabled = false;
    } else {
      document.getElementById("status").textContent = "No job info found on this page.";
    }
  });
});

document.getElementById("reach-btn").addEventListener("click", () => {
  const btn = document.getElementById("reach-btn");
  const result = document.getElementById("result");
  const error = document.getElementById("error");

  btn.disabled = true;
  btn.textContent = "Sending...";
  result.textContent = "";
  error.textContent = "";

  chrome.runtime.sendMessage({ type: "REACH_OUT", data: jobInfo }, (res) => {
    btn.textContent = "Send Outreach";
    if (res && res.success && res.data && res.data.success) {
      result.textContent = `Sent to ${res.data.email_sent_to}`;
      btn.textContent = "Sent!";
    } else {
      error.textContent = res?.data?.error || "Backend not running — start with ./start.sh";
      btn.disabled = false;
    }
  });
});
