import { describe, expect, it } from "vitest";
import { buildApiUrl } from "../lib/api";

describe("buildApiUrl", () => {
  it("ghép tham số truy vấn đúng", () => {
    const url = buildApiUrl("/api/v1/documents", {
      query: { keyword: "máy in", limit: 10 }
    });
    expect(url).toBe("/api/v1/documents?keyword=m%C3%A1y+in&limit=10");
  });

  it("bỏ qua giá trị undefined", () => {
    const url = buildApiUrl("/api/v1/documents", {
      query: { keyword: undefined, ma_hs: "84778039" }
    });
    expect(url).toBe("/api/v1/documents?ma_hs=84778039");
  });
});
