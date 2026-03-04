import { queryGeneric } from "convex/server";

export const status = queryGeneric({
  args: {},
  handler: async () => {
    return {
      status: "ok",
      database: "connected",
      backend: "convex",
      timestampIso: new Date().toISOString(),
    };
  },
});
