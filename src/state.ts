import { store, type StoreType } from "@global-state/core";
import { sync } from "@global-state/core/lib/store";
import { persistent } from "@global-state/sources"

export type State = {
  cache: {
    svg: string
    strokes: Stroke[]
  }
}

export type Stroke = {
  angles: Float32Array
  radii: Float32Array
};

export interface Point {
  x: number
  y: number
}

const initial: State = {
  cache: {
    svg: "",
    strokes: [],
  }
}

export const state = store(initial)

export const cache = state.select(
  s => s.cache,
  (s, v) => {
    s.cache = v
  },
  {
    svg: (s, value: string) => {
      s.svg = value
    },
    strokes: (s, value: Stroke[]) => {
      s.strokes = value
    }
  }
)

sync<StoreType<typeof cache>>(cache, persistent("cache", {
  svg: "",
  strokes: [],
}))
