// Native WebGL: no CDN, texture downloads, model weights, or external libraries.
export default function ({ parentElement }) {
  const canvas = parentElement.querySelector("canvas");
  const fallback = parentElement.querySelector(".fallback");
  const showFallback = () => { canvas.hidden = true; fallback.hidden = false; };
  let gl;
  try {
    gl = canvas.getContext("webgl", { alpha: true, antialias: false, preserveDrawingBuffer: true });
  } catch (_) { showFallback(); return; }
  if (!gl) { showFallback(); return; }

  const palette = {
    robe: [0.25, 0.09, 0.13], fold: [0.36, 0.15, 0.18],
    shadow: [0.13, 0.11, 0.13], bronze: [0.58, 0.38, 0.20],
    gold: [0.76, 0.55, 0.28], skin: [0.62, 0.48, 0.34],
    beard: [0.60, 0.57, 0.48], hair: [0.41, 0.39, 0.34],
    eye: [0.055, 0.04, 0.035], pages: [0.73, 0.64, 0.45],
  };
  const voxels = new Map();
  const key = (x, y, z) => `${x},${y},${z}`;
  const put = (x, y, z, color) => voxels.set(key(x, y, z), { x, y, z, color: palette[color] });
  const box = (x0, x1, y0, y1, z0, z1, color) => {
    for (let x = x0; x <= x1; x++) for (let y = y0; y <= y1; y++)
      for (let z = z0; z <= z1; z++) put(x, y, z, color);
  };

  // Robe, shoulders and a stepped plinth. Each colored cell is solid geometry.
  for (let y = -11; y <= 4; y++) {
    const radius = y > 0 ? 10 - y : 8;
    for (let x = -radius; x <= radius; x++) for (let z = -4; z <= 3; z++) {
      if ((x * x) / (radius * radius) + (z * z) / 22 < 1.1)
        put(x, y, z, (Math.abs(x + y) % 5 === 0) ? "fold" : "robe");
    }
  }
  box(-9, 9, -14, -13, -5, 5, "shadow");
  box(-8, 8, -12, -12, -4, 4, "bronze");

  // Hood behind an ochre face, brows and a long square-cut sage's beard.
  for (let y = 3; y <= 13; y++) for (let x = -6; x <= 6; x++) for (let z = -5; z <= 2; z++) {
    if (x * x / 42 + (y - 8) ** 2 / 36 + (z + 1) ** 2 / 26 <= 1.2)
      put(x, y, z, Math.abs(x) > 4 ? "fold" : "robe");
  }
  for (let x = -4; x <= 4; x++) for (let y = 6; y <= 12; y++) for (let z = -1; z <= 4; z++) {
    if (x * x / 23 + (y - 9) ** 2 / 15 + (z - 1) ** 2 / 18 <= 1.15)
      put(x, y, z, "skin");
  }
  box(-3, -1, 11, 11, 4, 4, "hair");
  box(1, 3, 11, 11, 4, 4, "hair");
  put(-2, 10, 4, "eye"); put(2, 10, 4, "eye");
  box(0, 0, 8, 10, 4, 5, "skin");
  for (let y = -1; y <= 7; y++) {
    const width = Math.min(4, 2 + Math.floor((y + 1) / 3));
    for (let x = -width; x <= width; x++) for (let z = 3; z <= 5; z++)
      put(x, y, z, (x + y) % 3 === 0 ? "hair" : "beard");
  }
  box(-2, 2, 7, 7, 5, 5, "hair");
  // Stepped Hellenistic/Egyptian crown, rather than a modern wizard's hat.
  box(-5, 5, 12, 12, -2, 3, "gold");
  box(-4, 4, 13, 14, -2, 2, "bronze");
  box(-3, 3, 15, 15, -1, 2, "gold");
  box(-2, 2, 16, 16, 0, 1, "bronze");
  box(0, 0, 13, 15, 3, 3, "gold");
  // An ancient codex held against the robe.
  box(3, 8, -8, -3, 4, 5, "bronze");
  box(4, 7, -7, -4, 6, 6, "pages");
  box(2, 3, -5, -3, 5, 6, "skin");
  // Hermetic staff, with interlacing serpents and small wing-like shoulders.
  box(-9, -9, -10, 9, 2, 2, "bronze");
  for (let y = 3; y <= 10; y++) {
    const offset = Math.round(2 * Math.sin((y - 3) * 0.9));
    put(-9 + offset, y, 3, "gold"); put(-9 - offset, y, 3, "gold");
  }
  box(-12, -10, 10, 10, 2, 2, "gold");
  box(-8, -6, 10, 10, 2, 2, "gold");

  // Cull internal voxel faces; the entire statue uses one draw call.
  const faces = [
    [[1,0,0], [[.5,-.5,-.5],[.5,.5,-.5],[.5,.5,.5],[.5,-.5,.5]]],
    [[-1,0,0], [[-.5,-.5,.5],[-.5,.5,.5],[-.5,.5,-.5],[-.5,-.5,-.5]]],
    [[0,1,0], [[-.5,.5,-.5],[-.5,.5,.5],[.5,.5,.5],[.5,.5,-.5]]],
    [[0,-1,0], [[-.5,-.5,.5],[-.5,-.5,-.5],[.5,-.5,-.5],[.5,-.5,.5]]],
    [[0,0,1], [[-.5,-.5,.5],[.5,-.5,.5],[.5,.5,.5],[-.5,.5,.5]]],
    [[0,0,-1], [[.5,-.5,-.5],[-.5,-.5,-.5],[-.5,.5,-.5],[.5,.5,-.5]]],
  ];
  const vertices = [];
  for (const { x, y, z, color } of voxels.values()) for (const [normal, corners] of faces) {
    if (voxels.has(key(x + normal[0], y + normal[1], z + normal[2]))) continue;
    for (const index of [0, 1, 2, 0, 2, 3]) {
      const corner = corners[index];
      vertices.push((x + corner[0]) * .1, (y + corner[1] - 1) * .1, (z + corner[2]) * .1,
        ...normal, ...color);
    }
  }
  const shader = (type, source) => {
    const result = gl.createShader(type);
    gl.shaderSource(result, source); gl.compileShader(result);
    if (!gl.getShaderParameter(result, gl.COMPILE_STATUS)) {
      gl.deleteShader(result);
      throw new Error("Shader unavailable");
    }
    return result;
  };
  let program, buffer, vertex, fragment;
  try {
    vertex = shader(gl.VERTEX_SHADER, `
      attribute vec3 position, normal, color;
      uniform mat4 transform, rotation;
      varying vec3 shade;
      void main() {
        vec3 n = mat3(rotation) * normal;
        float light = .40 + .62 * max(dot(n, normalize(vec3(-.6, 1., 1.))), 0.);
        shade = color * light;
        gl_Position = transform * vec4(position, 1.);
      }`);
    fragment = shader(gl.FRAGMENT_SHADER, `
      precision mediump float;
      varying vec3 shade;
      void main() { gl_FragColor = vec4(shade, 1.); }`);
    program = gl.createProgram();
    gl.attachShader(program, vertex); gl.attachShader(program, fragment); gl.linkProgram(program);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error("Renderer unavailable");
    gl.useProgram(program);
    buffer = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);
    for (const [index, name] of ["position", "normal", "color"].entries()) {
      const location = gl.getAttribLocation(program, name);
      gl.enableVertexAttribArray(location);
      gl.vertexAttribPointer(location, 3, gl.FLOAT, false, 36, index * 12);
    }
  } catch (_) {
    if (buffer) gl.deleteBuffer(buffer);
    if (program) gl.deleteProgram(program);
    if (vertex) gl.deleteShader(vertex);
    if (fragment) gl.deleteShader(fragment);
    showFallback(); return;
  }

  const multiply = (a, b) => {
    const out = new Float32Array(16);
    for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++)
      for (let k = 0; k < 4; k++) out[c * 4 + r] += a[k * 4 + r] * b[c * 4 + k];
    return out;
  };
  const transformLocation = gl.getUniformLocation(program, "transform");
  const rotationLocation = gl.getUniformLocation(program, "rotation");
  const span = 1.85, aspect = canvas.width / canvas.height;
  const projection = new Float32Array([1/(span*aspect),0,0,0, 0,1/span,0,0, 0,0,-1/10,0, 0,0,0,1]);
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
  const initial = { yaw: -.24, pitch: -.08 };
  let yaw = initial.yaw, pitch = initial.pitch, targetYaw = yaw, targetPitch = pitch;
  let frame = 0, disposed = false, dragging = false, lastX = 0, lastY = 0;
  const clamp = (value, min, max) => Math.max(min, Math.min(max, value));
  const render = () => {
    frame = 0;
    if (disposed || gl.isContextLost()) return;
    const speed = reducedMotion.matches ? 1 : .22;
    yaw += (targetYaw - yaw) * speed; pitch += (targetPitch - pitch) * speed;
    if (Math.abs(yaw - targetYaw) + Math.abs(pitch - targetPitch) <= .001) {
      yaw = targetYaw; pitch = targetPitch;
    }
    const cy = Math.cos(yaw), sy = Math.sin(yaw), cx = Math.cos(pitch), sx = Math.sin(pitch);
    const ry = new Float32Array([cy,0,-sy,0, 0,1,0,0, sy,0,cy,0, 0,0,0,1]);
    const rx = new Float32Array([1,0,0,0, 0,cx,sx,0, 0,-sx,cx,0, 0,0,0,1]);
    const rotation = multiply(rx, ry);
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.enable(gl.DEPTH_TEST);
    gl.uniformMatrix4fv(rotationLocation, false, rotation);
    gl.uniformMatrix4fv(transformLocation, false, multiply(projection, rotation));
    gl.drawArrays(gl.TRIANGLES, 0, vertices.length / 9);
    // Expose orientation for accessibility/debugging without a Python rerun.
    canvas.dataset.yaw = yaw.toFixed(3); canvas.dataset.pitch = pitch.toFixed(3);
    if (Math.abs(yaw - targetYaw) + Math.abs(pitch - targetPitch) > .001) requestRender();
  };
  const requestRender = () => { if (!frame && !disposed) frame = requestAnimationFrame(render); };
  const move = event => {
    if (dragging) {
      targetYaw += (event.clientX - lastX) * .015;
      targetPitch = clamp(targetPitch + (event.clientY - lastY) * .008, -.55, .55);
      lastX = event.clientX; lastY = event.clientY;
    } else if (event.pointerType === "mouse") {
      const rect = canvas.getBoundingClientRect();
      targetYaw = initial.yaw + ((event.clientX - rect.left) / rect.width - .5) * .65;
      targetPitch = initial.pitch + ((event.clientY - rect.top) / rect.height - .5) * .3;
    } else return;
    requestRender();
  };
  const down = event => {
    if (event.button !== 0) return;
    dragging = true; lastX = event.clientX; lastY = event.clientY;
    canvas.setPointerCapture(event.pointerId);
  };
  const up = () => { dragging = false; };
  const reset = () => { targetYaw = initial.yaw; targetPitch = initial.pitch; requestRender(); };
  const leave = () => { if (!dragging) reset(); };
  const keyboard = event => {
    if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home'].includes(event.key)) return;
    event.preventDefault();
    if (event.key === 'Home') reset();
    if (event.key === 'ArrowLeft') targetYaw -= .2;
    if (event.key === 'ArrowRight') targetYaw += .2;
    if (event.key === 'ArrowUp') targetPitch = clamp(targetPitch - .12, -.55, .55);
    if (event.key === 'ArrowDown') targetPitch = clamp(targetPitch + .12, -.55, .55);
    requestRender();
  };
  const lost = event => { event.preventDefault(); cancelAnimationFrame(frame); showFallback(); };
  const listeners = { pointermove: move, pointerdown: down, pointerup: up,
    pointercancel: up, lostpointercapture: up, pointerleave: leave,
    dblclick: reset, keydown: keyboard, webglcontextlost: lost };
  for (const [name, listener] of Object.entries(listeners)) canvas.addEventListener(name, listener);
  requestRender();
  return () => {
    disposed = true; cancelAnimationFrame(frame);
    for (const [name, listener] of Object.entries(listeners)) canvas.removeEventListener(name, listener);
    gl.deleteBuffer(buffer); gl.deleteProgram(program); gl.deleteShader(vertex); gl.deleteShader(fragment);
    gl.getExtension("WEBGL_lose_context")?.loseContext();
  };
}
