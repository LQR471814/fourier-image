<script lang="ts">
  import { cache, type Point, type Stroke } from "./state";
  import { atan, distance } from "./utils";

  const strokeLength = (stroke: Stroke) => {
    if (stroke.angles.length === 0) {
      return 0;
    }
    let length = 0;
    for (let i = 1; i < stroke.angles.length; i++) {
      const x1 = stroke.radii[i - 1] * Math.cos(stroke.angles[i - 1]);
      const y1 = stroke.radii[i - 1] * Math.sin(stroke.angles[i - 1]);

      const x2 = stroke.radii[i] * Math.cos(stroke.angles[i]);
      const y2 = stroke.radii[i] * Math.sin(stroke.angles[i]);

      length += distance(x2 - x1, y2 - y1);
    }
    return length;
  };

  const strokes = (
    samples: number,
    options = {
      jumpRadius: 0.025,
      minStrokeLength: 0.1,
    }
  ): Stroke[] => {
    const svg = document.querySelector("svg");
    if (!svg) {
      throw new Error("could not find svg");
    }

    const { width, height } = svg.viewBox.baseVal;

    const averageWidth = (width + height) / 2;
    const step = averageWidth / samples;
    let jumpRadius = averageWidth * options.jumpRadius;
    if (jumpRadius < step) {
      jumpRadius = step;
    }
    const minStrokeLength = averageWidth * options.minStrokeLength;

    console.log(step, jumpRadius, width, height);

    const center = {
      x: width / 2,
      y: height / 2,
    };

    const strokes: Stroke[] = [];
    const path = document.querySelectorAll("path");
    for (const p of path) {
      const values = Math.floor(p.getTotalLength() / step);

      let stroke: Stroke = {
        angles: new Float32Array(values),
        radii: new Float32Array(values),
      };

      const updateStroke = () => {
        stroke.angles = stroke.angles.subarray(0, strokeIndex);
        stroke.radii = stroke.radii.subarray(0, strokeIndex);
      };

      let lastPoint: Point = {
        x: -Infinity,
        y: -Infinity,
      };
      let strokeIndex = 0;
      for (let i = 0; i < values; i++) {
        const point = p.getPointAtLength(i * step);
        const distanceFromLast = distance(
          point.x - lastPoint.x,
          point.y - lastPoint.y
        );

        // on new stroke (this runs directly on the first loop)
        if (distanceFromLast > jumpRadius) {
          updateStroke();

          const length = strokeLength(stroke)
          if (length >= minStrokeLength) {
            strokes.push(stroke);
            console.log("new stroke");
          }

          strokeIndex = 0;

          stroke = {
            angles: new Float32Array(values),
            radii: new Float32Array(values),
          };
        }
        lastPoint = point;

        const rx = point.x - center.x;
        // this is done because positive = further down in computer graphics
        const ry = -(point.y - center.y);

        stroke.angles[strokeIndex] = atan(rx, ry);
        stroke.radii[strokeIndex] = distance(rx, ry);

        strokeIndex++;
      }

      updateStroke();
      const length = strokeLength(stroke)
      if (length >= minStrokeLength) {
        strokes.push(stroke);
      }
    }

    return strokes;
  };

  const objToArray = (obj: any) => {
    const keys = Object.keys(obj);
    const arr = new Float32Array(keys.length);
    for (const k of keys) {
      arr[parseInt(k)] = obj[k];
    }
    return Array.from(arr);
  };
</script>

<main class="flex gap-4 p-4">
  <div class="fixed top-4 left-4 flex gap-4 items-start">
    <textarea
      class="std-textarea"
      on:change={(e) => {
        cache.actions.svg(e.currentTarget.value);
      }}>{$cache.svg}</textarea
    >
    <button
      class="std-button"
      on:click={() => {
        const result = strokes(100);
        cache.actions.strokes(result);
        console.log(result);
      }}
    >
      calculate
    </button>
    <button
      class="std-button"
      on:click={() => {
        navigator.clipboard.writeText(
          JSON.stringify(
            $cache.strokes.map((s) => {
              return {
                angles: objToArray(s.angles),
                radii: objToArray(s.radii),
              };
            })
          )
        );
      }}
    >
      copy strokes
    </button>
  </div>
  <div class="flex-1 flex justify-center">
    {@html $cache.svg}
  </div>
</main>
