const sectionLinks = [...document.querySelectorAll('.page-nav-links a')];
const sections = sectionLinks.map(link => document.querySelector(link.getAttribute('href'))).filter(Boolean);
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    const visible = entries.filter(entry => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!visible) return;
    sectionLinks.forEach(link => link.classList.toggle('is-active', link.hash === `#${visible.target.id}`));
  }, {rootMargin: '-160px 0px -55% 0px', threshold: [0, .2, .5]});
  sections.forEach(section => observer.observe(section));
}

// This static preview prepares an email draft; it does not claim a submission.
document.querySelectorAll('[data-enquiry-form]').forEach(form => {
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const details = new FormData(form);
    const topic = form.dataset.topic;
    const body = [
      `Enquiry: ${topic}`,
      `Name: ${details.get('name')}`,
      `Website: ${details.get('website')}`,
      `Email: ${details.get('email')}`,
      `Phone: ${details.get('phone')}`,
      '',
      `Goals: ${details.get('goal') || 'To discuss'}`
    ].join('\n');
    const draft = `mailto:marketing@digilari.com.au?subject=${encodeURIComponent(`${topic} enquiry`)}&body=${encodeURIComponent(body)}`;
    const status = form.querySelector('.enquiry-status');
    status.replaceChildren(document.createTextNode('Your enquiry is ready in your email app. Send the email to complete it. If it did not open, '));
    const fallback = document.createElement('a');
    fallback.href = draft;
    fallback.textContent = 'open your enquiry draft';
    status.append(fallback, document.createTextNode(', or call 1300 859 358.'));
    status.hidden = false;
    window.location.href = draft;
  });
});
