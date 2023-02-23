export function distance(x: number, y: number): number {
  return Math.sqrt(x * x + y * y);
};

export function atan(x: number, y: number): number {
  const angle = Math.atan(Math.abs(y / x));
  // quadrant 1
  if (x > 0 && y >= 0) {
    return angle;
  }
  // quadrant 2
  if (x <= 0 && y > 0) {
    return Math.PI - angle;
  }
  // quadrant 3
  if (x < 0 && y <= 0) {
    return angle + Math.PI;
  }
  // quadrant 4
  if (x >= 0 && y < 0) {
    return 2 * Math.PI - angle;
  }
  // (0, 0)
  return 0;
};
