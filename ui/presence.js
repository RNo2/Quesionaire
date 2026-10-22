// Decorative background only: no overlay captures clicks, focus or scrolling.
export default function () {
  const scene = document.querySelector('.stApp');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  if (!scene) return;
  let frame = 0, x = 0, y = 0;
  const paint = () => {
    frame = 0;
    scene.style.setProperty('--presence-x', `${x.toFixed(2)}px`);
    scene.style.setProperty('--presence-y', `${y.toFixed(2)}px`);
  };
  const move = event => {
    if (motion.matches || event.pointerType !== 'mouse') return;
    x = (event.clientX / innerWidth - .5) * 9;
    y = (event.clientY / innerHeight - .5) * 5;
    if (!frame) frame = requestAnimationFrame(paint);
  };
  const reset = () => {
    x = y = 0;
    if (!frame) frame = requestAnimationFrame(paint);
  };
  document.addEventListener('pointermove', move, { passive: true });
  document.addEventListener('pointerleave', reset);
  motion.addEventListener('change', reset);
  return () => {
    cancelAnimationFrame(frame);
    document.removeEventListener('pointermove', move);
    document.removeEventListener('pointerleave', reset);
    motion.removeEventListener('change', reset);
    scene.style.removeProperty('--presence-x');
    scene.style.removeProperty('--presence-y');
  };
}
