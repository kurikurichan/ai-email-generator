"use client";

import { useDataStore, dataObject } from "../store";
import { useRouter } from "next/navigation";

export default function DataResults() {
  const data: dataObject[] | null = useDataStore((state) => state.data);

  function isHeader(text: string) {
    const headers = ["Name", "Job Role", "Email", "Company", "Message"];
    return headers.includes(text) ? true : false;
  }

  const clearData = useDataStore((state) => state.clearData);
  const router = useRouter();

  async function regenerate() {
    await clearData();
    router.push("/");
  }

  return (
    <div className="flex flex-col w-full items-center py-8">
      <div className="flex flex-col gap-2 border-2 border-purple-50 rounded bg-zinc-200 p-8 min-h-[200px] w-5/6">
        {!data || data.length === 0 ? (
          <p className="font-bold">
            No data available. Try personalizing some emails!
          </p>
        ) : (
          <div className="grid grid-cols-6">
            <div className="col-span-6">
              {data && (
                <span className="flex gap-4 justify-center items-center border-2 border-purple-50 rounded bg-purple-200 p-4 w-full">
                  <p>Not happy with your results?</p>
                  <button
                    className=" bg-purple-800 hover:bg-purple-600 text-zinc-100 font-semibold hover:text-white py-2 px-2 border border-purple-500 hover:border-transparent rounded"
                    onClick={regenerate}
                  >
                    Try again
                  </button>
                </span>
              )}
              {data &&
                data.map((row, index) => {
                  return (
                    <div key={index} className="grid grid-cols-6">
                      {Object.values(row).map((cell, columnIndex) => (
                        <div
                          key={columnIndex}
                          className={`px-4 py-2 border border-purple-200 overflow-wrap-normal break-words relative ${
                            isHeader(cell) ? "font-bold" : ""
                          } ${columnIndex === 4 ? "col-span-2" : ""}`}
                          style={{ whiteSpace: "pre-wrap" }}
                        >
                          {columnIndex === 4 && cell !== "Message" && (
                            <button
                              className="absolute bottom-2 right-2 bg-purple-800 hover:bg-purple-600 text-zinc-100 font-semibold hover:text-white py-2 px-2 border border-purple-500 hover:border-transparent rounded"
                              onClick={() => {
                                navigator.clipboard.writeText(cell);
                              }}
                            >
                              Copy!
                            </button>
                          )}
                          {cell}
                        </div>
                      ))}
                    </div>
                  );
                })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
