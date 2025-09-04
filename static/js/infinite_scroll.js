// Generic infinite scroll loader
window.initInfiniteScroll = function (opts = {}) {
  const container = document.getElementById(opts.containerId || "productGrid");
  if (!container) return;
  let page = 1;
  const per_page = opts.per_page || 24;
  const api = opts.api || "/api/products";
  const extra = opts.extraParams || {};
  let loading = false;
  let done = false;

  function buildUrl() {
    const u = new URL(window.location.origin + api);
    u.searchParams.set("page", page);
    u.searchParams.set("per_page", per_page);
    Object.entries(extra).forEach(([k, v]) => {
      if (v) u.searchParams.set(k, v);
    });
    return u.toString();
  }

  async function loadNext() {
    if (loading || done) return;
    loading = true;
    const loader =
      document.getElementById("loading") ||
      document.getElementById("shopLoading");
    if (loader) loader.classList.remove("hidden");
    try {
      const res = await fetch(buildUrl());
      if (!res.ok) throw new Error("Network error");
      const items = await res.json();
      if (!items || items.length === 0) {
        done = true;
      }
      items.forEach((p) => {
        const node = window._internal.buildCard(p);
        container.appendChild(node);
      });
      page++;
    } catch (err) {
      console.error(err);
    } finally {
      loading = false;
      if (loader) loader.classList.add("hidden");
    }
  }

  // initial load
  loadNext();

  // scroll listener
  window.addEventListener("scroll", () => {
    if (loading || done) return;
    if (
      window.innerHeight + window.scrollY >=
      document.body.offsetHeight - 600
    ) {
      loadNext();
    }
  });
};
