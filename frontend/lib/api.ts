export interface FetchOptions {
  query?: Record<string, string | number | undefined>;
}

export function buildApiUrl(path: string, options?: FetchOptions): string {
  const params = new URLSearchParams();
  if (options?.query) {
    Object.entries(options.query).forEach(([key, value]) => {
      if (value !== undefined && value !== "") {
        params.set(key, String(value));
      }
    });
  }
  return params.size > 0 ? `${path}?${params.toString()}` : path;
}
