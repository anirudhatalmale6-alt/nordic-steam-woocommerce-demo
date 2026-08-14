/* Nordic Steam Co. — demo interactions.
   In the WooCommerce build these are handled by Woo core, the wishlist plugin
   and the reviews plugin; here they're mocked with localStorage so the demo clicks. */

const S = {
  get cart(){ try { return JSON.parse(localStorage.getItem('ns_cart')) || []; } catch(e){ return []; } },
  set cart(v){ localStorage.setItem('ns_cart', JSON.stringify(v)); },
  get wish(){ try { return JSON.parse(localStorage.getItem('ns_wish')) || []; } catch(e){ return []; } },
  set wish(v){ localStorage.setItem('ns_wish', JSON.stringify(v)); }
};

const money = n => '$' + n.toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2});

function toast(msg){
  const t = document.getElementById('toast');
  if(!t) return;
  t.textContent = msg; t.classList.add('on');
  clearTimeout(t._t); t._t = setTimeout(()=>t.classList.remove('on'), 2200);
}

function paintCounts(){
  const cart = S.cart;
  const total = cart.reduce((s,i)=>s + i.price * i.qty, 0);
  const count = cart.reduce((s,i)=>s + i.qty, 0);
  document.querySelectorAll('[data-cart-total]').forEach(e=>e.textContent = money(total));
  document.querySelectorAll('[data-cart-count]').forEach(e=>e.textContent = count);
  document.querySelectorAll('[data-wish-count]').forEach(e=>e.textContent = S.wish.length);
}

function addToCart(name, price, qty){
  qty = qty || 1;
  const cart = S.cart;
  const hit = cart.find(i=>i.name === name);
  if(hit) hit.qty += qty; else cart.push({name, price, qty});
  S.cart = cart; paintCounts();
  toast(qty + ' × ' + name + ' added to cart');
}

function toggleWish(name){
  const w = S.wish;
  const i = w.indexOf(name);
  if(i > -1){ w.splice(i,1); toast('Removed from wishlist'); }
  else { w.push(name); toast('Saved to wishlist'); }
  S.wish = w; paintCounts();
}

function demoSearch(e){
  e.preventDefault();
  const q = e.target.querySelector('input').value.trim();
  location.href = 'shop.html' + (q ? '?s=' + encodeURIComponent(q) : '');
  return false;
}

/* ---- live chat ---- */
function toggleChat(){
  const w = document.getElementById('chatwin');
  const b = document.querySelector('.chatbtn');
  const open = w.classList.toggle('on');
  b.style.display = open ? 'none' : 'flex';
}
function chatSend(e){
  e.preventDefault();
  const input = document.getElementById('chatinput');
  const body = document.getElementById('chatbody');
  const txt = input.value.trim();
  if(!txt) return false;
  const me = document.createElement('div');
  me.className = 'bubble me'; me.textContent = txt; body.appendChild(me);
  input.value = '';
  body.scrollTop = body.scrollHeight;
  setTimeout(()=>{
    const r = document.createElement('div');
    r.className = 'bubble';
    r.textContent = 'Thanks — an agent will pick this up in a moment. (Demo widget: the live build wires this to Tidio / Tawk.to or WhatsApp.)';
    body.appendChild(r); body.scrollTop = body.scrollHeight;
  }, 700);
  return false;
}

/* ---- product tabs ---- */
function showTab(btn, id){
  document.querySelectorAll('.tabnav button').forEach(b=>b.classList.remove('on'));
  document.querySelectorAll('.tabpane').forEach(p=>p.classList.remove('on'));
  btn.classList.add('on');
  document.getElementById(id).classList.add('on');
}

/* ---- gallery ---- */
function pickImage(btn, src){
  document.querySelectorAll('.gallery .thumbs button').forEach(b=>b.classList.remove('on'));
  btn.classList.add('on');
  document.querySelector('.gallery .main img').src = src;
}

/* ---- qty ---- */
function bump(el, d){
  const input = el.parentNode.querySelector('input');
  input.value = Math.max(1, (parseInt(input.value,10) || 1) + d);
}

/* ---- reviews: star picker, filter, sort, submit ---- */
let pickedRating = 0;
function pickStar(n){
  pickedRating = n;
  document.querySelectorAll('.starpick button').forEach((b,i)=>b.classList.toggle('on', i < n));
}
function filterReviews(chip, stars){
  document.querySelectorAll('.rv-toolbar .chip').forEach(c=>c.classList.remove('on'));
  chip.classList.add('on');
  document.querySelectorAll('.review').forEach(r=>{
    r.style.display = (stars === 'all' || r.dataset.stars === String(stars) ||
      (stars === 'photo' && r.dataset.photos === '1')) ? '' : 'none';
  });
}
function sortReviews(sel){
  const list = document.getElementById('rvlist');
  if(!list) return;
  const items = [...list.querySelectorAll('.review')];
  const key = sel.value;
  items.sort((a,b)=>{
    if(key === 'high') return b.dataset.stars - a.dataset.stars;
    if(key === 'low')  return a.dataset.stars - b.dataset.stars;
    if(key === 'helpful') return b.dataset.helpful - a.dataset.helpful;
    return a.dataset.age - b.dataset.age;   // newest
  });
  items.forEach(i=>list.appendChild(i));
}
function markHelpful(btn){
  const n = btn.querySelector('b');
  n.textContent = parseInt(n.textContent,10) + 1;
  btn.disabled = true; btn.style.color = 'var(--ok)';
}
function submitReview(e){
  e.preventDefault();
  const note = document.getElementById('rvnotice');
  if(!pickedRating){ note.className = 'notice on'; note.textContent = 'Please choose a star rating first.'; return false; }
  note.className = 'notice on';
  note.innerHTML = '<b>Thanks!</b> Your review was submitted and is now awaiting moderation. ' +
    'In the live store this lands in WooCommerce → Comments, where you approve, reply or spam-flag it. ' +
    'Verified buyers can be set to auto-publish.';
  e.target.reset(); pickStar(0);
  return false;
}

/* ---- init ---- */
document.addEventListener('DOMContentLoaded', ()=>{
  paintCounts();
  const page = document.body.dataset.page;
  document.querySelectorAll('.mainmenu a').forEach(a=>{
    if(a.dataset.nav === page) a.classList.add('on');
  });
  document.addEventListener('click', e=>{
    const bw = document.querySelector('.browse-wrap');
    if(bw && !bw.contains(e.target)) bw.classList.remove('open');
  });
});
