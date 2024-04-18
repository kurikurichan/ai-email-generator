import Link from "next/link";

export default function Sidebar() {
  return (
    <div className="bg-blue-950 min-h-screen w-24 flex flex-col items-center py-4">
      <Link href="/">
        <button className="rounded-full w-8 h-8 bg-blue-800 hover:bg-blue-600 text-white font-bold py-2 p-4 flex items-center justify-center mb-4" title="Create">✏️</button>
      </Link>
      <Link href="/results">
        <button className="rounded-full w-8 h-8 bg-blue-800 hover:bg-blue-600 text-white font-bold py-2 p-4 flex items-center justify-center mb-4" title="Results">📝</button>
      </Link>
    </div>
  );
}
