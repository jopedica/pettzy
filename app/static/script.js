document.addEventListener("DOMContentLoaded", () => {
  const cards  = document.querySelectorAll(".service-card");
  const detail = document.getElementById("service-detail");
  if (!cards.length || !detail) return;

  const BRL = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

  function setActive(btn){
    cards.forEach(c => c.classList.toggle("is-active", c === btn));
  }

  function renderDetail(s){
    const icon  = s.icon || "banho.png";
    const desc  = s.description || "";
    const price = (s.price !== null && s.price !== undefined) ? BRL.format(s.price) : "—";

    detail.innerHTML = `
      <header class="services__header">
        <img src="/static/${icon}" alt="${s.name}" width="32" height="32">
        <h3>${s.name}</h3>
        <p class="muted">${desc}</p>
      </header>

      <p class="services__price">Preço médio: <strong>${price}</strong></p>
      <p class="services__info">Os preços podem variar conforme o profissional, localização e necessidades específicas do seu pet.</p>

      <a class="btn" href="#">Encontrar profissionais</a>
    `;
  }

  async function loadService(id){
    try{
      const res = await fetch(`/api/services/${id}`);
      if (!res.ok) return;
      const s = await res.json();
      renderDetail(s);
    }catch(e){ console.error(e); }
  }

  cards.forEach(btn => {
    btn.addEventListener("click", () => {
      setActive(btn);
      loadService(btn.dataset.id);
    });
  });
});

