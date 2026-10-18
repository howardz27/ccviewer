/* Load the standard Clarity tag on the deployed site. */
(function () {
  'use strict';
  const config = __CONFIG__;
  const eligible = /^[a-zA-Z0-9]+$/.test(config.projectId) &&
    location.protocol === 'https:' && config.allowedHosts.includes(location.hostname);
  const events = new Set(['file_picker_open', 'folder_picker_open', 'paste_open', 'help_open', 'github_open']);

  window.ccviewerAnalytics = {
    event(name) {
      if (eligible && events.has(name)) window.clarity('event', name);
    }
  };
  if (!eligible) return;

  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src='https://www.clarity.ms/tag/'+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, 'clarity', 'script', config.projectId);

  document.addEventListener('click', function (e) {
    const link = e.target.closest('a[href]');
    if (!link) return;
    if (link.hasAttribute('data-guide')) window.ccviewerAnalytics.event('help_open');
    if (link.hostname === 'github.com') window.ccviewerAnalytics.event('github_open');
  });
})();
