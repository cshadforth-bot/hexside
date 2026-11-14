// Shared card rendering for cards.html and print.html. Needs data.js loaded first.

const TIER={2:'#12a39a',4:'#f08a24',6:'#8a45c8'};
// 14px tiles of fabric texture, drawn once and shared by swatches, chips and garments.
const dk='rgba(0,0,0,.28)',lt='rgba(255,255,255,.45)';
const TEX={
D:`<path d="M-4 14L14 -4M0 18L18 0M-4 6L6 -4" stroke="${dk}" stroke-width="1.6"/><path d="M0 7L7 0" stroke="${lt}" stroke-width="1"/>`,
W:`<path d="M1 3l4 4 4-4 4 4M1 10l4 4 4-4 4 4" stroke="${dk}" stroke-width="1.6" fill="none"/>`,
S:`<rect width="14" height="14" fill="url(#sheen)"/><path d="M0 7Q7 3 14 7" stroke="${lt}" stroke-width="1.4" fill="none"/>`,
L:`<circle cx="7" cy="7" r="4.5" fill="none" stroke="#d99a6a" stroke-width="1.4"/><circle cx="7" cy="7" r="1.2" fill="#d99a6a"/><circle cx="0" cy="0" r="1.2" fill="#d99a6a"/><circle cx="14" cy="14" r="1.2" fill="#d99a6a"/>`,
C:`<path d="M0 3.5H14M0 10.5H14M3.5 0V14M10.5 0V14" stroke="${dk}" stroke-width="1.2"/>`,
K:`<path d="M2 2l2.5 5L7 2M9 2l2.5 5L14 2M2 9l2.5 5L7 9M9 9l2.5 5L14 9" stroke="${dk}" stroke-width="1.3" fill="none" transform="translate(-1 -1)"/>`};
function installDefs(el){el.innerHTML=`<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".25"/></linearGradient>`+
Object.keys(TEX).map(k=>`<pattern id="p${k}" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="${FABRICS[k][1]}"/>${TEX[k]}</pattern>`).join('')}
const fill=(f,w,h)=>`<rect width="${w}" height="${h}" fill="url(#p${f})"/>`;
// Garment silhouettes in a 100x100 box. paths = clip/fill shapes; extra = decoration drawn on top.
const MIR='transform="translate(100 0) scale(-1 1)"';
const G={
'Pocket Tee':{p:['M30 15L10 30 18 42 28 36V88H72V36L82 42 90 30 70 15Q50 26 30 15Z'],x:'<rect x="56" y="46" width="12" height="13" rx="2" fill="none" stroke="#fff" stroke-width="1.5" stroke-dasharray="3 2"/>'},
'Scarf':{p:['M12 22Q50 4 88 22V36Q50 20 12 36Z','M58 30H78L84 88H62Z'],x:'<path d="M64 88v8M70 88v8M76 88v8M82 88v8" stroke="#2b2118" stroke-width="1.6"/>'},
'Scrunchie':{p:['M50 10A40 40 0 1 0 50.01 10ZM50 32A18 18 0 1 1 49.99 32Z'],e:1},
'Tote Bag':{p:['M20 38H80L86 92H14Z'],x:'<path d="M36 38Q36 8 50 8Q64 8 64 38" fill="none" stroke="#2b2118" stroke-width="3.5"/>'},
'Beanie':{p:['M16 66Q16 20 50 20Q84 20 84 66Z','M12 66H88V84H12Z','M50 10m-8 0a8 8 0 1 0 16 0a8 8 0 1 0-16 0'],x:'<path d="M12 75H88" stroke="#fff" stroke-width="1.5" stroke-dasharray="3 2"/>'},
'Hankie':{p:['M50 6L94 50 50 94 6 50Z'],x:'<path d="M50 20L80 50 50 80 20 50Z" fill="none" stroke="#fff" stroke-width="1.5" stroke-dasharray="3 2"/>'},
'Denim Jacket':{p:['M32 12L8 28V84H24L26 52V90H74V52L76 84H92V28L68 12 50 28Z'],x:'<path d="M50 28V90M32 12L50 34 68 12" stroke="#fff" stroke-width="1.6" fill="none" stroke-dasharray="3 2"/>'},
'Cardigan':{p:['M34 12L10 30V86H26L28 56V92H72V56L74 86H90V30L66 12 50 38Z'],x:'<path d="M50 38V92" stroke="#2b2118" stroke-width="2.4"/><path d="M34 12L50 38 66 12" stroke="#fff" stroke-width="1.6" fill="none" stroke-dasharray="3 2"/><circle cx="45" cy="52" r="2.4" fill="#fff" stroke="#2b2118"/><circle cx="45" cy="68" r="2.4" fill="#fff" stroke="#2b2118"/><circle cx="45" cy="84" r="2.4" fill="#fff" stroke="#2b2118"/>'},
'Slip Dress':{p:['M36 8H41L43 28Q50 35 57 28L59 8H64L68 38 79 92H21L32 38Z']},
'Boiler Suit':{p:['M34 10L14 22 16 42 28 36 30 52 32 94H47L50 66 53 94H68L70 52 72 36 84 42 86 22 66 10Q50 24 34 10Z'],x:'<path d="M50 24V66" stroke="#fff" stroke-width="1.6" stroke-dasharray="3 2"/>'},
'Peacoat':{p:['M30 10L8 26 10 64H22L24 94H76L78 64H90L92 26 70 10 50 32Z'],x:'<path d="M50 32V94" stroke="#fff" stroke-width="1.6" stroke-dasharray="3 2"/><circle cx="56" cy="56" r="2.2" fill="#fff"/><circle cx="56" cy="72" r="2.2" fill="#fff"/>'},
'Kimono':{p:['M40 8L50 26 60 8 98 22V54H76V92H24V54H2V22Z'],x:'<path d="M24 60H76" stroke="#2b2118" stroke-width="6"/><path d="M24 60H76" stroke="#fff" stroke-width="1.2" stroke-dasharray="3 2"/>'},
'Pinafore':{p:['M30 10H38L40 34H60L62 10H70L74 42 86 92H14L26 42Z']},
'Shawl':{p:['M4 24Q50 0 96 24Q72 64 50 96Q28 64 4 24Z'],x:'<path d="M20 30Q50 14 80 30" stroke="#fff" stroke-width="1.5" fill="none" stroke-dasharray="3 2"/>'},
'Patchwork Coat':{p:['M30 10L6 30 8 68H22L16 94H84L78 68H92L94 30 70 10 50 30Z'],x:'<path d="M50 30V94" stroke="#fff" stroke-width="1.6" stroke-dasharray="3 2"/>'},
'Wedding Dress':{p:['M38 6H62L58 36 66 44 94 94H6L34 44 42 36Z'],x:'<path d="M50 44V94M36 60L22 94M64 60L78 94" stroke="#fff" stroke-width="1.2" fill="none" opacity=".8"/>'},
'Quilt':{p:['M8 12H92V88H8Z'],x:'<path d="M36 12V88M64 12V88M8 37H92M8 63H92" stroke="#fff" stroke-width="1.6" stroke-dasharray="4 2.5"/>'},
'Evening Gown':{p:['M40 6L44 24Q50 30 56 24L60 6 66 36 58 52 76 96H24L42 52 34 36Z'],x:'<path d="M50 30V52" stroke="#fff" stroke-width="1.4" stroke-dasharray="3 2"/>'},
};
let uid=0;
// The garment is cut from four triangles meeting at its centre, one per card edge: top, right, bottom, left.
function garment(c){
  const g=G[c.name]; const id='c'+(uid++);
  const shapes=g.p.map(s=>{const [d,tr]=s.split('|');return `<path d="${d}" ${tr||''} ${g.e?'clip-rule="evenodd" fill-rule="evenodd"':''}/>`}).join('');
  const tri=[[c.top,'0,0 100,0 50,50'],[c.right,'100,0 100,100 50,50'],[c.bottom,'100,100 0,100 50,50'],[c.left,'0,100 0,0 50,50']]
    .map(([f,pts])=>`<polygon points="${pts}" fill="url(#p${f})"/>`).join('');
  return `<svg viewBox="0 0 100 100"><defs><clipPath id="${id}">${shapes}</clipPath></defs>
  <g transform="translate(2 4)" opacity=".18"><g clip-path="url(#${id})"><rect width="100" height="100" fill="#000"/></g></g>
  <g clip-path="url(#${id})">${tri}<path d="M0 0L100 100M100 0L0 100" stroke="#fff" stroke-width="1.5" stroke-dasharray="3 2.2"/></g>
  <g fill="none" stroke="#2b2118" stroke-width="2.4" stroke-linejoin="round">${g.p.map(s=>{const [d,tr]=s.split('|');return `<path d="${d}" ${tr||''} ${g.e?'fill-rule="evenodd"':''}/>`}).join('')}</g></svg>`;
}
const band=(cls,f,inner)=>`<div class="band ${cls}"><svg viewBox="0 0 ${cls==='bt'||cls==='bb'?'252 38':'28 280'}" preserveAspectRatio="xMidYMid slice">${fill(f,252,280)}</svg>${inner}</div>`;
function cardHTML(c,i){
  const nm=f=>FABRICS[f][0], dot=f=>`<span class="dot" title="${nm(f)}">${nm(f)[0]}</span>`;
  return `<div class="c" style="--f:${FABRICS[c.top][1]}">
${band('bt',c.top,`<span class="pill">${nm(c.top)}</span>`)}
<div class="mid">${band('bl',c.left,dot(c.left))}
<div class="core"><h2><small>${String(i+1).padStart(2,'0')}</small>${c.name}</h2><div class="col">${c.collection}</div><div class="art">${garment(c)}</div><div class="e"><b>${c.effect[0]}</b>${c.effect[1]}</div></div>
${band('br',c.right,dot(c.right))}</div>
${band('bb',c.bottom,`<span class="pill">${nm(c.bottom)}</span>`)}</div>`}

// Card back: a patchwork of all six fabrics, stitched, with the name on a label.
function backHTML(){
  const order='DWSLKC'.split(''), cols=6, rows=8, pw=252/cols, ph=352/rows;
  let cells='';
  for(let r=0;r<rows;r++)for(let c=0;c<cols;c++){const f=order[(c*2+r*5+((r*c)%3))%6];
    cells+=`<rect x="${c*pw}" y="${r*ph}" width="${pw}" height="${ph}" fill="url(#p${f})"/>`;}
  let seams='';for(let c=1;c<cols;c++)seams+=`<path d="M${c*pw} 0V352"/>`;for(let r=1;r<rows;r++)seams+=`<path d="M0 ${r*ph}H252"/>`;
  return `<div class="c back"><svg viewBox="0 0 252 352" preserveAspectRatio="none">${cells}
  <g stroke="#fff" stroke-width="1.4" stroke-dasharray="4 3" opacity=".85">${seams}</g>
  <rect x="9" y="9" width="234" height="334" rx="8" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="6 4"/>
  <rect x="26" y="136" width="200" height="80" rx="14" fill="#2b1d3a" stroke="#fff" stroke-width="3"/>
  <text x="126" y="176" text-anchor="middle" font-family="Jost,Futura,sans-serif" font-weight="700" font-size="25" letter-spacing="2" fill="#fff">TEXTILESME</text>
  <text x="126" y="199" text-anchor="middle" font-family="Jost,Futura,sans-serif" font-weight="600" font-size="11" letter-spacing="3" fill="#f2b632">NOTHING IS WASTED</text></svg></div>`;
}

if(typeof window!=='undefined')window.TX={installDefs,cardHTML,backHTML};
