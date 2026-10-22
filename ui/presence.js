// Authored low-resolution geometry: articulated stone, no raster portrait or CDN.
export default function () {
  const host = document.querySelector('.stApp');
  if (!host) return;
  const canvas = document.createElement('canvas');
  canvas.className = 'hermes-monument';
  canvas.setAttribute('aria-hidden', 'true');
  host.prepend(canvas);
  const ctx = canvas.getContext('2d');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let frame = 0, started = 0, yaw = 0, targetYaw = 0, raised = 0;
  const stone = ['#29282b','#373336','#494145','#5a4d4e','#70605b','#8b7768'];
  function poly(points, color) {
    ctx.fillStyle = color; ctx.beginPath();
    points.forEach(([x,y], i) => i ? ctx.lineTo(x,y) : ctx.moveTo(x,y));
    ctx.closePath(); ctx.fill();
  }
  function rect(x,y,w,h,c) {ctx.fillStyle=c;ctx.fillRect(x,y,w,h);}
  function arm(moving) {
    ctx.save();
    ctx.translate(moving ? -64 : 64, 142);
    if (!moving) ctx.scale(-1,1);
    // Shoulder and elbow rotate separately, so the hand rises as a jointed limb.
    ctx.rotate(moving ? raised * 0.70 : -0.06);
    poly([[0,-12],[-18,-9],[-29,11],[-26,53],[-7,65],[9,46],[12,7]],stone[2]);
    poly([[-18,-9],[-29,11],[-26,53],[-17,45],[-15,9]],stone[4]);
    poly([[0,-12],[12,7],[9,46],[-7,65],[-8,17]],stone[1]);
    poly([[-24,23],[-12,35],[5,31],[3,38],[-10,42]],stone[0]);
    ctx.translate(-16,53);
    ctx.rotate(moving ? raised * 2.25 : 0.12);
    poly([[-11,-5],[9,-3],[13,36],[7,58],[-8,59],[-15,27]],stone[3]);
    poly([[-11,-5],[-5,2],[-4,50],[-8,59],[-15,27]],stone[5]);
    poly([[6,0],[13,36],[7,58],[1,52],[2,16]],stone[1]);
    // Palm and separate, block-cut fingers; the raised palm faces outward.
    poly([[-9,51],[8,51],[11,69],[7,80],[-8,80],[-13,68]],stone[4]);
    rect(-10,73,4,17,stone[4]); rect(-4,76,4,19,stone[5]);
    rect(2,75,4,17,stone[3]);rect(8,71,3,16,stone[2]);
    poly([[-9,57],[-17,58],[-22,69],[-18,73],[-10,66]],stone[3]);
    rect(-8,60,12,3,stone[2]);
    ctx.restore();
  }
  function statue() {
    // Broad silhouette and heavy robe keep the presence monumental.
    poly([[-39,119],[-72,127],[-91,151],[-82,215],[-110,340],[110,340],[82,215],[91,151],[72,127],[39,119]],stone[0]);
    poly([[-39,119],[-72,127],[-82,215],[-110,340],[-52,340],[-31,178]],stone[2]);
    poly([[39,119],[72,127],[82,215],[110,340],[52,340],[31,178]],'#211f24');
    poly([[-38,135],[-54,182],[-43,279],[-27,340],[-17,210]],stone[3]);
    poly([[-59,169],[-70,205],[-75,315],[-62,259]],stone[1]);
    poly([[38,139],[55,185],[44,279],[27,340],[17,210]],stone[1]);
    poly([[-29,167],[0,196],[32,166],[18,280],[-15,280]],'#302a30');
    for(let i=0;i<7;i++) poly([[-56+i*17,251],[-66+i*19,340],[-62+i*19,340]], i%2?stone[1]:stone[0]);
    arm(false); arm(true);
    ctx.save();ctx.translate(Math.round(yaw*2),0);
    // Faceted ancient headdress, bronze rim, severe face.
    poly([[-42,18],[-52,51],[-47,109],[-60,139],[-31,155],[31,155],[60,139],[47,109],[52,51],[42,18],[0,2]],stone[1]);
    poly([[-42,18],[-52,51],[-47,109],[-60,139],[-43,136],[-33,47]],stone[3]);
    poly([[42,18],[52,51],[47,109],[60,139],[43,136],[33,47]],'#242229');
    for(let i=0;i<7;i++){
      poly([[-47+i*2,53+i*11],[-35+i,56+i*11],[-36+i,60+i*11],[-48+i*2,57+i*11]],'#79634e');
      poly([[47-i*2,53+i*11],[35-i,56+i*11],[36-i,60+i*11],[48-i*2,57+i*11]],'#493d38');
    }
    poly([[-37,36],[-30,26],[30,26],[37,36],[33,81],[22,101],[-20,103],[-34,83]],stone[3]);
    poly([[-30,26],[-37,36],[-34,83],[-20,103],[-15,73],[-24,49]],stone[4]);
    poly([[11,32],[30,26],[37,36],[33,81],[22,101],[13,74]],stone[1]);
    poly([[-40,30],[-36,20],[36,20],[40,30],[31,36],[-31,36]],'#5c4e41');
    rect(-33,29,65,3,'#947952');
    poly([[-9,21],[-9,10],[-3,5],[4,5],[10,11],[10,21],[4,28],[-4,28]],'#86704d');
    rect(-4,10,7,11,'#302b2a');rect(-1,25,3,13,'#a58b61');
    poly([[-29,45],[-13,43],[-5,50],[-9,54],[-27,52]],stone[1]);
    poly([[6,50],[14,43],[29,46],[27,53],[10,54]],'#1b1a20');
    rect(-25,52,14,4,'#111218');rect(12,52,13,4,'#111218');
    rect(-23,52,5,1,'#8d7963');rect(14,52,4,1,'#66574d');
    poly([[-3,48],[-9,70],[-3,74],[10,70],[4,66],[3,49]],stone[4]);
    poly([[3,49],[4,66],[10,70],[4,73],[1,69]],stone[1]);
    poly([[-26,72],[-35,90],[-28,123],[-13,146],[0,162],[17,142],[31,115],[35,88],[24,72],[14,80],[-12,80]],stone[2]);
    poly([[-23,74],[-10,77],[0,74],[13,77],[24,74],[19,87],[5,85],[0,89],[-8,85],[-19,88]],stone[4]);
    rect(-10,83,23,3,'#201d23');
    // Chisel marks follow beard strands, with a deterministic stone grain.
    for(let i=0;i<95;i++){
      const y=90+(i*17%63), x=(i*29%55)-27;
      if(Math.abs(x) < (159-y)*0.44) rect(x,y,2,4+(i%7),stone[1+(i%4)]);
    }
    poly([[-27,90],[-30,111],[-18,134],[-13,133],[-19,105]],stone[4]);
    poly([[24,93],[28,111],[14,143],[8,149],[16,115]],stone[1]);
    // Fine chips use the same palette, avoiding photorealistic surface detail.
    for(let i=0;i<35;i++){
      const x=(i*23%57)-28,y=36+(i*13%43);
      if(y<44 || Math.abs(x)>18) rect(x,y,1+(i%2),1,i%3?stone[3]:stone[5]);
    }
    ctx.restore();
  }
  const ease = t => t*t*(3-2*t);
  function draw(now=performance.now()) {
    frame=0;
    if(started){
      const elapsed=(now-started)/1000;
      raised=motion.matches ? .85 : elapsed<3.2 ? ease(elapsed/3.2) : elapsed<5 ? 1 : elapsed<8.5 ? 1-ease((elapsed-5)/3.5) : 0;
      if(elapsed>=8.5 && !motion.matches) started=0;
    }
    yaw += (targetYaw-yaw)*.09;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    const scale=innerWidth<640
      ? Math.min(canvas.width/280,canvas.height/340)
      : Math.max(canvas.width/390,canvas.height/390);
    ctx.save();ctx.translate(canvas.width/2+Math.round(yaw*3),-4*scale);ctx.scale(scale,scale);
    statue();ctx.restore();
    canvas.dataset.pose=raised>.2?'raising':'rest';
    if(!motion.matches && (started || Math.abs(targetYaw-yaw)>.01)) frame=requestAnimationFrame(draw);
  }
  function requestDraw(){if(!frame)frame=requestAnimationFrame(draw);}
  function resize(){
    // A genuinely coarse framebuffer, enlarged with nearest-neighbor sampling.
    canvas.width=Math.max(64,Math.round(innerWidth/5));
    canvas.height=Math.max(160,Math.round(innerHeight/5));
    ctx.imageSmoothingEnabled=false;requestDraw();
  }
  function awaken(){started=performance.now();canvas.dataset.awakenings=String(1+Number(canvas.dataset.awakenings||0));requestDraw();}
  function submit(event){
    const input=document.querySelector('[data-testid="stTextInput"] input');
    if(event.key==='Enter' && !event.isComposing && event.target===input && input.value.trim()) awaken();
  }
  function pointer(event){
    if(motion.matches || event.pointerType!=='mouse')return;
    targetYaw=(event.clientX/innerWidth-.5)*2;requestDraw();
  }
  function touch(event){
    if(event.target.closest('input,button,a,[data-testid="stForm"],.st-key-answer'))return;
    if(event.clientY<innerHeight*.42)awaken();
  }
  function reset(){targetYaw=0;requestDraw();}
  document.addEventListener('keydown',submit,true);
  document.addEventListener('pointermove',pointer,{passive:true});
  document.addEventListener('pointerdown',touch,{passive:true});
  document.addEventListener('pointerleave',reset);
  window.addEventListener('resize',resize);
  motion.addEventListener('change',requestDraw);
  resize();
  return () => {
    cancelAnimationFrame(frame);canvas.remove();
    document.removeEventListener('keydown',submit,true);
    document.removeEventListener('pointermove',pointer);
    document.removeEventListener('pointerdown',touch);
    document.removeEventListener('pointerleave',reset);
    window.removeEventListener('resize',resize);
    motion.removeEventListener('change',requestDraw);
  };
}
