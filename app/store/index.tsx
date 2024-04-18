import { create } from "zustand";

interface State {
  data: dataObject[] | null;
  loadData: () => Promise<void>;
  clearData: () => void;
}

export interface dataObject {
  name: string;
  jobRole: string;
  email: string;
  company: string;
  message: string;
}

export const useDataStore = create<State>((set) => ({
  data: null,
  loadData: async () => {
    try {
      const res = await fetch("/api/emails/");
      if (!res.ok) throw res.statusText;
      //if data, redirect to next page with data
      // also maybe do local storage with data to save it
      let results: dataObject[] = await res.json();
      set({ data: results });
    } catch (e) {
      console.error(e);
    }
  },
  clearData: () => {
    set({ data: null });
  },
}));
