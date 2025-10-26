"use client";

import { useEffect, useMemo, useState } from "react";
import useSWR from "swr";

interface DocumentItem {
  id: number;
  so_ky_hieu: string;
  ten_hang?: string | null;
  mo_ta_hang?: string | null;
  ma_hs?: string | null;
  ngay_ban_hanh?: string | null;
  co_quan_ban_hanh?: string | null;
  nguon_pdf?: string | null;
}

interface DocumentResponse {
  total: number;
  items: DocumentItem[];
}

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function HomePage() {
  const [keyword, setKeyword] = useState("");
  const [maHS, setMaHS] = useState("");
  const [page, setPage] = useState(0);
  const limit = 10;

  const query = useMemo(() => {
    const params = new URLSearchParams();
    if (keyword) params.set("keyword", keyword);
    if (maHS) params.set("ma_hs", maHS);
    params.set("limit", String(limit));
    params.set("offset", String(page * limit));
    return `/api/v1/documents?${params.toString()}`;
  }, [keyword, maHS, page]);

  const { data, isLoading } = useSWR<DocumentResponse>(query, fetcher, {
    revalidateOnFocus: false
  });

  useEffect(() => {
    setPage(0);
  }, [keyword, maHS]);

  return (
    <main className="mx-auto flex min-h-screen max-w-5xl flex-col gap-6 px-6 py-10">
      <header className="flex flex-col gap-2">
        <h1 className="text-3xl font-semibold text-sky-700">
          Tra cứu kết quả phân tích phân loại & mã HS
        </h1>
        <p className="text-slate-600">
          Dữ liệu được thu thập tự động từ Tổng cục Hải quan, hỗ trợ tra cứu nhanh theo tên hàng,
          mô tả và mã HS 2022.
        </p>
      </header>

      <section className="grid gap-4 rounded-lg bg-white p-5 shadow">
        <div className="grid gap-2">
          <label htmlFor="keyword" className="text-sm font-medium text-slate-700">
            Từ khoá
          </label>
          <input
            id="keyword"
            type="text"
            placeholder="Ví dụ: máy in 3D, bột cà phê"
            value={keyword}
            onChange={(event) => setKeyword(event.target.value)}
            className="rounded border border-slate-300 px-3 py-2 text-base text-slate-900 focus:border-sky-500 focus:outline-none focus:ring-2 focus:ring-sky-200"
          />
        </div>

        <div className="grid gap-2">
          <label htmlFor="ma-hs" className="text-sm font-medium text-slate-700">
            Mã HS
          </label>
          <input
            id="ma-hs"
            type="text"
            placeholder="Ví dụ: 8477.80.39"
            value={maHS}
            onChange={(event) => setMaHS(event.target.value)}
            className="rounded border border-slate-300 px-3 py-2 text-base text-slate-900 focus:border-sky-500 focus:outline-none focus:ring-2 focus:ring-sky-200"
          />
        </div>
      </section>

      <section className="flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-slate-800">Kết quả</h2>
          <span className="text-sm text-slate-500">
            {isLoading ? "Đang tải..." : `${data?.total ?? 0} văn bản`}
          </span>
        </div>

        <div className="grid gap-3">
          {data?.items.map((item) => (
            <article key={item.id} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
              <div className="flex flex-col gap-1">
                <div className="flex items-center justify-between gap-4">
                  <h3 className="text-lg font-semibold text-slate-900">{item.so_ky_hieu}</h3>
                  {item.ma_hs && <span className="rounded bg-sky-100 px-3 py-1 text-sm font-medium text-sky-700">Mã HS: {item.ma_hs}</span>}
                </div>
                {item.ten_hang && <p className="text-base text-slate-800">{item.ten_hang}</p>}
                {item.mo_ta_hang && <p className="text-sm text-slate-600">{item.mo_ta_hang}</p>}
                <div className="flex flex-wrap items-center gap-3 text-sm text-slate-500">
                  {item.co_quan_ban_hanh && <span>Cơ quan: {item.co_quan_ban_hanh}</span>}
                  {item.ngay_ban_hanh && <span>Ngày ban hành: {new Date(item.ngay_ban_hanh).toLocaleDateString("vi-VN")}</span>}
                  {item.nguon_pdf && (
                    <a href={item.nguon_pdf} target="_blank" rel="noopener noreferrer" className="text-sky-600">
                      Tải PDF gốc
                    </a>
                  )}
                </div>
              </div>
            </article>
          ))}
          {!isLoading && (data?.items.length ?? 0) === 0 && (
            <p className="rounded border border-dashed border-slate-300 p-6 text-center text-slate-500">
              Không có dữ liệu phù hợp. Hãy thử với từ khoá hoặc mã HS khác.
            </p>
          )}
        </div>

        {data && data.total > limit && (
          <div className="flex items-center justify-between">
            <button
              type="button"
              className="rounded border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
              onClick={() => setPage((prev) => Math.max(prev - 1, 0))}
              disabled={page === 0}
            >
              Trang trước
            </button>
            <span className="text-sm text-slate-500">Trang {page + 1}</span>
            <button
              type="button"
              className="rounded border border-sky-500 bg-sky-500 px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-50"
              onClick={() => setPage((prev) => prev + 1)}
              disabled={(page + 1) * limit >= data.total}
            >
              Trang tiếp
            </button>
          </div>
        )}
      </section>
    </main>
  );
}
