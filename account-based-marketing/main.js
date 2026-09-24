const enquiryForm = document.querySelector("#abm-enquiry-form");

if (enquiryForm) {
  enquiryForm.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!enquiryForm.reportValidity()) return;

    const details = new FormData(enquiryForm);
    const body = [
      `Website: ${details.get("website")}`,
      `Name: ${details.get("name")}`,
      `Email: ${details.get("email")}`,
      `Phone: ${details.get("phone")}`,
      `Target accounts or brief: ${details.get("brief") || "Not provided"}`,
    ].join("\n");
    const subject = "ABM strategy enquiry";
    const emailDraft = `mailto:marketing@digilari.com.au?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

    const status = document.querySelector("#form-status");
    if (status) {
      status.textContent = "Your email draft is ready. Please send it from your email app to complete your enquiry.";
      status.hidden = false;
    }
    window.location.href = emailDraft;
  });
}
