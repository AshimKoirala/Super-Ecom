// helper to insert product card HTML (server uses _product_card.html for product pages; for JS we build minimal card)
function buildCard(p) {
  const div = document.createElement("div");
  div.className = "bg-white rounded-2xl shadow-sm p-3 flex flex-col";
  div.innerHTML = `
    <a href="/product/${p.slug}">
      <div class="w-full aspect-[4/3] overflow-hidden rounded-xl flex items-center justify-center">
        <img src="${p.image}" alt="${
    p.title
  }" class="object-contain w-full h-full">
      </div>
      <h4 class="mt-3 text-sm font-semibold">${p.title}</h4>
      <div class="mt-2 text-orange-600 font-bold">$${p.price.toFixed(2)}</div>
    </a>
  `;
  return div;
}
window._internal = { buildCard };
