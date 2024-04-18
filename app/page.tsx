"use client";
import Image from "next/image";
import { useRouter } from "next/navigation";

import { useState } from "react";
import { useDataStore } from "./store";
import Spinner from "./components/spinner";

export default function Home() {
  const [buttonClicked, setButtonClicked] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);

  const router = useRouter();
  const loadData = useDataStore((state) => state.loadData);

  const handleNewEmail = (e: React.MouseEvent) => {
    e.preventDefault();
    setButtonClicked(true);
  };

  const handleCancel = (e: React.MouseEvent) => {
    e.preventDefault();
    setButtonClicked(false);
  };

  const handleSubmit = async (e: React.MouseEvent) => {
    e.preventDefault();
    setLoading(true);
    await loadData();
    router.push("/results");
  };

  return (
    <div className="flex flex-col gap-8 w-full justify-center items-center py-8">
      <div className="flex flex-col gap-2 border-2 border-purple-50 rounded bg-zinc-200 p-8 h-96 w-5/6">
        {buttonClicked ? (
          <div className="flex flex-col justify-between h-full">
            <div className="flex flex-col gap-3">
              <p>
                I want to create a personalized email for all leads found in
                leads.csv.
              </p>
              <p>Personalize content based on their job role.</p>
            </div>
            <div className="flex justify-between items-center">
              <button
                className="bg-transparent hover:bg-blue-600 text-blue-800 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded"
                onClick={handleCancel}
              >
                Cancel
              </button>
              <button
                className="bg-blue-600 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded flex items-center gap-2"
                onClick={handleSubmit}
              >
                Let&apos;s Go
                {loading ? <Spinner /> : <p>★:･☆</p>}
              </button>
            </div>
          </div>
        ) : (
          <>
            <p className="font-bold">Hey Guest!👋</p>
            <p className="text-slate-500">What would you like to do today?</p>
            <Image
              className="self-end bg-transparent"
              src="/bot.png"
              quality={100}
              width={100}
              height={100}
              alt="robot guy"
            />
          </>
        )}
      </div>
      <div className="bg-zinc-200 w-full rounded h-4/6 flex flex-col items-center">
        <div className="self-start p-6 font-bold">
          <h1>Explore</h1>
        </div>
        <div
          className="flex flex-col items-center justify-center gap-3 p-4 rounded w-[300px] h-[300px] cursor-pointer"
          onClick={handleNewEmail}
        >
          <Image
            className="rounded-full"
            src="/papericon.jpg"
            width={100}
            height={100}
            alt="Icon with paper and an orange background"
          />
          <p>Personalized Emails</p>
        </div>
      </div>
    </div>
  );
}
