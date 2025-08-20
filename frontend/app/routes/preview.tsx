import { Route } from "react-router";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Overview of website and it's capabilities" },
    { name: "preview", content: "Welcome to the preview" },
  ];
}

export default function Preview() {
  return (
        <main className="flex items-center justify-center pt-16 pb-4">
            <div className="flex-1 flex flex-col items-center gap-16 min-h">Hello</div>
        </main>
    );
}

