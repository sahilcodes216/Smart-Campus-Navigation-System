/**
 * Main Application Script & Shared UI Controller
 * Conforms to PRD Section 5, 6, 7, 10, 11, 13
 */

export class AppState {
  constructor() {
    this.data = null;
    this.locations = [];
    this.categories = [];
    this.nodes = [];
    this.edges = [];
    this.isLoaded = false;
  }

  async loadData() {
    if (this.isLoaded) return this.data;
    try {
      const response = await fetch('./data/locations.json');
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      this.data = await response.json();
      this.locations = this.data.locations || [];
      this.categories = this.data.categories || [];
      this.nodes = this.data.nodes || [];
      this.edges = this.data.edges || [];
      this.isLoaded = true;
      return this.data;
    } catch (err) {
      console.error('Failed to load campus data:', err);
      showToast("We couldn't load campus data. Please refresh.", 5000);
      throw err;
    }
  }

  getLocationById(id) {
    return this.locations.find(l => l.id === id);
  }

  getCategoryById(id) {
    return this.categories.find(c => c.id === id);
  }
}

export const appState = new AppState();

/**
 * Toast Notification System (PRD Section 7, 11)
 */
export function showToast(message, duration = 2500) {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    container.setAttribute('aria-live', 'polite');
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="20 6 9 17 4 12"></polyline>
    </svg>
    <span>${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(8px)';
    toast.style.transition = 'opacity 200ms ease, transform 200ms ease';
    setTimeout(() => {
      if (toast.parentNode) toast.parentNode.removeChild(toast);
    }, 200);
  }, duration);
}

/**
 * Copy text to clipboard with fallback
 */
export async function copyToClipboard(text, successMessage = 'Link copied') {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
    } else {
      const textArea = document.createElement('textarea');
      textArea.value = text;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      document.execCommand('copy');
      textArea.remove();
    }
    showToast(successMessage);
  } catch (err) {
    console.warn('Clipboard write failed:', err);
    showToast('Failed to copy');
  }
}

/**
 * URL Param helpers
 */
export function getUrlParams() {
  const params = new URLSearchParams(window.location.search);
  return {
    q: params.get('q') || '',
    cat: params.get('cat') ? params.get('cat').split(',').filter(Boolean) : [],
    loc: params.get('loc') || '',
    from: params.get('from') || '',
    to: params.get('to') || ''
  };
}

export function updateUrlParam(key, value, replace = false) {
  const url = new URL(window.location.href);
  if (value && (Array.isArray(value) ? value.length > 0 : value.trim() !== '')) {
    url.searchParams.set(key, Array.isArray(value) ? value.join(',') : value);
  } else {
    url.searchParams.delete(key);
  }

  if (replace) {
    window.history.replaceState({}, '', url.toString());
  } else {
    window.history.pushState({}, '', url.toString());
  }
}

/**
 * Sticky header observer
 */
export function initHeaderScroll() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  const handleScroll = () => {
    if (window.scrollY > 15) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();
}

// Auto init on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  initHeaderScroll();
});
