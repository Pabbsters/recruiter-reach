let jobInfo = null;

chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  chrome.tabs.sendMessage(tabs[0].id, { type: "GET_JOB_INFO" }, (info) => {
    if (chrome.runtime.lastError || !info) {
      document.getElementById("status").textContent = "Could not read page — edit fields manually.";
    } else {
      jobInfo = info;
      document.getElementById("company-input").value = info.company || "";
      document.getElementById("role-input").value = info.role || "";
      document.getElementById("status").textContent = "Edit if needed, then send.";
    }
    document.getElementById("reach-btn").disabled = false;
  });
});

document.getElementById("reach-btn").addEventListener("click", () => {
  const btn = document.getElementById("reach-btn");
  const result = document.getElementById("result");
  const error = document.getElementById("error");

  const company = document.getElementById("company-input").value.trim();
  const role = document.getElementById("role-input").value.trim();
  const url = jobInfo ? jobInfo.url : window.location.href;

  if (!company || !role) {
    error.textContent = "Please fill in company and role.";
    return;
  }

  jobInfo = { ...jobInfo, company, role, url };

  btn.disabled = true;
  btn.textContent = "Sending...";
  result.textContent = "";
  error.textContent = "";

  chrome.runtime.sendMessage({ type: "REACH_OUT", data: jobInfo }, (res) => {
    btn.textContent = "Send Outreach";
    if (res && res.success && res.data && res.data.success) {
      result.textContent = `Sent to ${res.data.email_sent_to}`;
      btn.textContent = "Sent!";
    } else if (res?.data?.error) {
      error.textContent = res.data.error;
      btn.textContent = "No email found";
    } else {
      error.textContent = "Backend not running — start with: python3 -m backend.server";
      btn.disabled = false;
      btn.textContent = "Send Outreach";
    }
  });
});
