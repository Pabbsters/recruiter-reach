function extractJobInfo() {
  const title = document.title || "";
  const url = window.location.href;

  const roleSelectors = [
    'h1[class*="job"]', 'h1[class*="title"]', 'h1[class*="position"]',
    '[data-testid*="job-title"]', '[class*="job-title"]', 'h1'
  ];
  let role = "";
  for (const sel of roleSelectors) {
    const el = document.querySelector(sel);
    if (el && el.innerText.trim().length > 0) { role = el.innerText.trim(); break; }
  }

  const companySelectors = [
    '[class*="company"]', '[data-testid*="company"]',
    '[class*="employer"]', '[class*="org"]'
  ];
  let company = "";
  for (const sel of companySelectors) {
    const el = document.querySelector(sel);
    if (el && el.innerText.trim().length > 0) { company = el.innerText.trim(); break; }
  }

  // Fallback: parse from page title (e.g. "Job Title - Company | LinkedIn")
  if (!company && title.includes(" - ")) {
    company = title.split(" - ").slice(-1)[0].split("|")[0].trim();
  }
  if (!role && title.includes(" - ")) {
    role = title.split(" - ")[0].trim();
  }

  return { company, role, url };
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "GET_JOB_INFO") {
    sendResponse(extractJobInfo());
  }
});
