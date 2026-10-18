/* Only public pages are recorded. Never pass session data to this module. */
(function () {
  'use strict';
  const config = __CONFIG__;
  const strings = __STRINGS__;
  const key = 'ccviewer_analytics_v1';
  const maxAge = 180 * 24 * 60 * 60 * 1000;
  let active = false;
  let loaded = false;
  let privateMode = false;
  let banner;
  let preferences;
  const eligible = /^[a-zA-Z0-9]+$/.test(config.projectId) &&
    location.protocol === 'https:' && config.allowedHosts.includes(location.hostname) &&
    !location.search && !location.hash && navigator.doNotTrack !== '1' &&
    navigator.globalPrivacyControl !== true;
  const events = new Set(['file_picker_open', 'folder_picker_open', 'paste_open', 'help_open', 'github_open']);

  function savedChoice() {
    try {
      const saved = JSON.parse(localStorage.getItem(key));
      return saved && Date.now() - saved.at < maxAge && saved.at <= Date.now() ? saved.choice : null;
    } catch (_) { return null; }
  }
  function save(choice) {
    try { localStorage.setItem(key, JSON.stringify({ choice, at: Date.now() })); } catch (_) {}
  }
  function start() {
    if (!eligible || active || privateMode) return;
    active = true;
    loaded = true;
    window.clarity = window.clarity || function () {
      (window.clarity.q = window.clarity.q || []).push(arguments);
    };
    window.clarity('consentv2', { analytics_Storage: 'granted', ad_Storage: 'denied' });
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.clarity.ms/tag/' + config.projectId;
    document.head.appendChild(script);
  }
  function stop() {
    if (!active) return;
    window.clarity('stop');
    active = false;
  }
  function withdraw() {
    window.clarity('consentv2', { analytics_Storage: 'denied', ad_Storage: 'denied' });
    stop();
    // Also clear first-party cookies if stop() has already reset the SDK queue.
    for (const name of ['_clck', '_clsk']) {
      document.cookie = name + '=; Max-Age=0; Path=/; SameSite=Lax';
      document.cookie = name + '=; Max-Age=0; Path=/; Domain=' + location.hostname + '; SameSite=Lax';
      if (location.hostname.endsWith('.ccviewer.top')) {
        document.cookie = name + '=; Max-Age=0; Path=/; Domain=ccviewer.top; SameSite=Lax';
      }
    }
    location.reload();
  }
  function privateView() {
    privateMode = true;
    stop();
    if (banner) banner.hidden = true;
  }
  function event(name) {
    if (active && !privateMode && events.has(name)) window.clarity('event', name);
  }
  window.ccviewerAnalytics = { privateView, event };

  document.addEventListener('DOMContentLoaded', function () {
    if (!eligible) return;
    const style = document.createElement('style');
    style.textContent = '.analytics-banner{position:fixed;bottom:16px;left:16px;right:16px;max-width:640px;z-index:1000;padding:18px;background:#161b22;color:#e6edf3;border:1px solid #6e7681;border-radius:10px;box-shadow:0 8px 30px #0006;font:14px/1.6 system-ui}.analytics-banner[hidden],.analytics-preferences[hidden]{display:none}.analytics-banner p{margin:0 0 12px}.analytics-banner a{color:#58a6ff}.analytics-banner button,.analytics-preferences{font:inherit;background:#1c2128;color:#e6edf3;border:1px solid #6e7681;border-radius:6px;padding:6px 12px;cursor:pointer}.analytics-banner button{margin:4px 8px 0 0}.analytics-preferences{position:fixed;bottom:12px;right:12px;z-index:999;font-size:12px}.analytics-banner button:focus-visible,.analytics-preferences:focus-visible{outline:2px solid #58a6ff;outline-offset:3px}';
    document.head.appendChild(style);
    banner = document.createElement('section');
    banner.className = 'analytics-banner';
    banner.setAttribute('aria-label', strings.analyticsSettings);
    const text = document.createElement('p');
    text.textContent = strings.analyticsNotice + ' ';
    const privacy = document.createElement('a');
    privacy.href = 'https://www.microsoft.com/privacy/privacystatement';
    privacy.target = '_blank';
    privacy.rel = 'noopener noreferrer';
    privacy.textContent = strings.analyticsPrivacy;
    text.appendChild(privacy);
    banner.appendChild(text);
    function button(label, action) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.textContent = label;
      btn.onclick = action;
      banner.appendChild(btn);
      return btn;
    }
    button(strings.analyticsAccept, function () {
      save('granted'); start(); banner.hidden = true; preferences.focus();
    });
    const reject = button(strings.analyticsReject, function () {
      save('denied');
      if (loaded) {
        // A fresh document removes the downloaded third-party code as well.
        withdraw();
      }
      banner.hidden = true; preferences.focus();
    });
    document.body.appendChild(banner);
    preferences = document.createElement('button');
    preferences.type = 'button';
    preferences.className = 'analytics-preferences';
    preferences.textContent = strings.analyticsSettings;
    preferences.onclick = function () { banner.hidden = false; reject.focus(); };
    document.body.appendChild(preferences);
    const choice = savedChoice();
    banner.hidden = privateMode || choice === 'granted' || choice === 'denied';
    if (choice === 'granted') start();
    window.addEventListener('storage', function (e) {
      if (e.key === key && loaded && savedChoice() !== 'granted') {
        withdraw();
      }
    });
    document.addEventListener('click', function (e) {
      const link = e.target.closest('a[href]');
      if (!link) return;
      if (link.hasAttribute('data-guide')) event('help_open');
      if (link.hostname === 'github.com') event('github_open');
    });
  });
})();
